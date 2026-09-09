#!/usr/bin/env python3
"""Scientific Markdown to PDF renderer.

Uses Pandoc's Markdown AST and ReportLab so it is intentionally independent of
an HTML browser.  Equations are rendered through pdflatex when possible (then
rasterised and tightly cropped); matplotlib's math renderer is a fallback.
"""
from __future__ import annotations
import argparse, hashlib, html, json, os, re, shutil, subprocess, sys, textwrap, unicodedata
from pathlib import Path
from collections import OrderedDict
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    PageBreak, Image, KeepTogether, LongTable, TableStyle, XPreformatted, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parent
TMP = ROOT / "tmp" / "formula-cache"
W, H = A4
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B = 2.05*cm, 2.05*cm, 1.75*cm, 1.85*cm
CONTENT_W = W - MARGIN_L - MARGIN_R
DASHES = str.maketrans({"–":"-", "—":"-", "−":"-", "‑":"-", "‐":"-", "‒":"-", "“":"\"", "”":"\"", "‘":"'", "’":"'", "…":"...", " ":" ", "≫":">>", "≪":"<<", "ℓ":"ell"})


def prose(s: str) -> str:
    """Use safe printable typography in ordinary text; math is never passed here."""
    return unicodedata.normalize("NFC", s).translate(DASHES)


def setup_fonts():
    serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    serifi = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
    if not Path(serifi).exists(): serifi = serif
    serifb = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    mono = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    paths = [("QSerif", serif), ("QSerifI", serifi), ("QSerifB", serifb), ("QMono", mono)]
    try:
        for name, path in paths:
            if Path(path).exists() and name not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(name, path))
        pdfmetrics.registerFontFamily("QSerif", normal="QSerif", bold="QSerifB", italic="QSerifI", boldItalic="QSerifB")
        return "QSerif", "QSerifI", "QSerifB", "QMono"
    except Exception:
        return "Times-Roman", "Times-Italic", "Times-Bold", "Courier"

SERIF, SERIFI, SERIFB, MONO = setup_fonts()

class Heading(Paragraph):
    def __init__(self, text, style, level, key):
        super().__init__(text, style)
        self.level, self.key, self.plain = level, key, re.sub("<[^>]+>", "", text)
    def drawOn(self, canvas, x, y, _sW=0):
        canvas.bookmarkHorizontalAbsolute(self.key, y + self.height)
        canvas.addOutlineEntry(self.plain, self.key, max(0, self.level - 2), False)
        self.canv._doctemplate.notify("TOCEntry", (self.level, self.plain, self.canv.getPageNumber(), self.key))
        return super().drawOn(canvas, x, y, _sW)

class Rule(Flowable):
    def __init__(self, width=CONTENT_W): super().__init__(); self.width=width; self.height=1
    def draw(self):
        self.canv.setStrokeColor(colors.HexColor("#929292")); self.canv.setLineWidth(.35)
        self.canv.line(0, .5, self.width, .5)

class PDFDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        frame = Frame(MARGIN_L, MARGIN_B, CONTENT_W, H-MARGIN_T-MARGIN_B, id="main", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id="scientific", frames=[frame], onPage=self.number_page))
    @staticmethod
    def number_page(canvas, doc):
        if canvas.getPageNumber() > 1:
            canvas.setFont(SERIF, 8)
            canvas.setFillColor(colors.HexColor("#4c4c4c"))
            canvas.drawCentredString(W/2, 1.02*cm, str(canvas.getPageNumber()))

class FormulaRenderer:
    def __init__(self):
        self.cache = TMP; self.cache.mkdir(parents=True, exist_ok=True)
        self.pdflatex = shutil.which("pdflatex")
        self.pdftoppm = "/usr/bin/pdftoppm" if Path("/usr/bin/pdftoppm").exists() else shutil.which("pdftoppm")
    def png(self, expr: str, display=True) -> Path | None:
        # Strip Pandoc delimiters but retain TeX exactness.
        expr = expr.strip()
        # Increment when sizing/normalisation changes: formula rasters encode
        # both typography and layout, so stale cache entries are not harmless.
        digest = hashlib.sha1(("formula-raster-v8|"+str(display)+expr).encode()).hexdigest()
        png = self.cache / (digest + ".png")
        if png.exists() and self._valid_png(png): return png
        if png.exists():
            # A stopped render can leave a zero/truncated cache file.  It is a
            # single deterministic scratch-cache target, safe to regenerate.
            png.unlink()
        if self.pdflatex and self.pdftoppm:
            tex = self.cache / (digest + ".tex")
            mode = r"\[\displaystyle " + expr + r" \]" if display else "$"+expr+"$"
            tex.write_text(r"""\documentclass[11pt]{article}
\usepackage[active,tightpage]{preview}
\usepackage{amsmath,amssymb,mathtools,bm}
\begin{document}\begin{preview}""" + mode + r"\end{preview}\end{document}", encoding="utf-8")
            p = subprocess.run([self.pdflatex, "-interaction=nonstopmode", "-halt-on-error", "-output-directory", str(self.cache), str(tex)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            pdf = self.cache / (digest + ".pdf")
            if p.returncode == 0 and pdf.exists():
                run = subprocess.run([self.pdftoppm, "-png", "-r", "200", "-singlefile", str(pdf), str(self.cache/digest)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if run.returncode == 0 and png.exists():
                    return self._crop(png)
        # matplotlib renders normal TeX grammar.  For aligned/cases environments,
        # render each mathematical row and compose them; this keeps the equation
        # legible when a minimal TeX install lacks a pdflatex format.
        return self._matplotlib_png(expr, png)
    def _matplotlib_png(self, expr: str, png: Path) -> Path | None:
        try:
            from matplotlib import mathtext
            from PIL import Image as PILImage
            from io import BytesIO
            def one(row):
                row = self._normalise_mathtext(row)
                row = row.strip().replace("&", "")
                buf=BytesIO(); mathtext.math_to_image("$"+row+"$",buf,dpi=220,format="png",color="black")
                return PILImage.open(BytesIO(buf.getvalue())).convert("RGBA")
            # Source display equations are commonly manually line-broken.  If
            # each physical row is self-contained, retain those rows rather
            # than shrinking one very wide raster to an unreadable size.
            semantic_rows=[x.strip().rstrip("\\\\").strip() for x in expr.splitlines() if x.strip()]
            if len(semantic_rows) > 1:
                try:
                    ims=[one(row) for row in semantic_rows]
                    width=max(im.width for im in ims); height=sum(im.height for im in ims)+7*(len(ims)-1)
                    image=PILImage.new("RGBA",(width+10,height+10),(255,255,255,255)); y=5
                    for im in ims:
                        image.alpha_composite(im,((width-im.width)//2+5,y)); y+=im.height+7
                    image.save(png)
                    return self._crop(png)
                except Exception:
                    pass
            try:
                image=one(expr)
            except Exception:
                # Common multiline environments only: retain every row instead of
                # degrading to raw source. Alignment markers have no semantic ink.
                cleaned=re.sub(r"\\begin\{(?:aligned|align\*?|cases|gather(?:ed)?)\}", "", expr)
                cleaned=re.sub(r"\\end\{(?:aligned|align\*?|cases|gather(?:ed)?)\}", "", cleaned)
                rows=[x.strip() for x in re.split(r"\\\\",cleaned) if x.strip()]
                if not rows: return None
                ims=[one(row) for row in rows]
                width=max(im.width for im in ims); height=sum(im.height for im in ims)+5*(len(ims)-1)
                image=PILImage.new("RGBA",(width+8,height+8),(255,255,255,255)); y=4
                for im in ims:
                    image.alpha_composite(im,((width-im.width)//2+4,y)); y+=im.height+5
            image.save(png)
            return self._crop(png)
        except Exception:
            return None
    @staticmethod
    def _normalise_mathtext(expr: str) -> str:
        """Small, lossless-enough bridge from common LaTex to mathtext.

        pdflatex is preferred whenever available.  This path only removes
        typographic sizing and turns textual operators into roman glyphs, both
        of which preserve the mathematical statement in matplotlib's parser.
        """
        # Mathtext is deliberately a compact TeX subset.  First normalise its
        # most frequent unbraced plain-TeX variants without changing meaning.
        expr = " ".join(expr.split())
        # Equation tags are labels, not part of the differential expression.
        # Keep their text visibly alongside the equation in mathtext fallback.
        expr = re.sub(r"\\tag\{([^{}]*)\}", lambda m: r"\qquad\mathrm{(" + m.group(1) + ")}", expr)
        # Literal delimiters are preferable to unmatched scalable delimiters
        # when a source display is manually broken across physical lines.
        expr = re.sub(r"\\(?:left|right)(?![A-Za-z])", "", expr)
        expr = FormulaRenderer._convert_plain_over(expr)
        expr = re.sub(r"\\(?:dfrac|tfrac)", lambda _m: r"\frac", expr)
        expr = re.sub(r"\\mathcal\s+([A-Za-z0-9])", lambda m: r"\mathcal{" + m.group(1) + "}", expr)
        expr = re.sub(r"\\mathfrak\s+([A-Za-z0-9])", lambda m: r"\mathfrak{" + m.group(1) + "}", expr)
        expr = re.sub(r"\\boldsymbol\s+([A-Za-z0-9])", lambda m: r"\mathbf{" + m.group(1) + "}", expr)
        expr = re.sub(r"\\boldsymbol\s*(\\[A-Za-z]+)", lambda m: r"\boldsymbol{" + m.group(1) + "}", expr)
        expr = re.sub(r"\\mathbf\s*([A-Za-z0-9])", lambda m: r"\mathbf{" + m.group(1) + "}", expr)
        expr = re.sub(r"\\sqrt\s*([A-Za-z0-9])", lambda m: r"\sqrt{" + m.group(1) + "}", expr)
        expr = re.sub(r"\\sqrt\s*(\\[A-Za-z]+)", lambda m: r"\sqrt{" + m.group(1) + "}", expr)
        # Two adjacent unbraced atom arguments are the conventional shorthand
        # used in the source for \frac14 and \frac m{r_h}.
        expr = re.sub(r"\\frac\s*([A-Za-z0-9])\s*([A-Za-z0-9])", lambda m: r"\frac{"+m.group(1)+"}{"+m.group(2)+"}", expr)
        expr = re.sub(r"\\frac\s*([A-Za-z0-9])\s*(\{)", lambda m: r"\frac{"+m.group(1)+"}"+m.group(2), expr)
        expr = re.sub(r"\\frac\s*(\{[^{}]*\})\s*([A-Za-z0-9])", lambda m: r"\frac"+m.group(1)+"{"+m.group(2)+"}", expr)
        expr = re.sub(r"\\frac\s*(\\[A-Za-z]+)\s*(\{)", lambda m: r"\frac{"+m.group(1)+"}"+m.group(2), expr)
        # \rm is plain TeX; turn its short alphabetic run into a roman group.
        expr = re.sub(r"\\rm\s+([A-Za-z]+)", lambda m: r"\mathrm{" + m.group(1) + "}", expr)
        # Only the exact primitive commands need expansion; do not corrupt
        # longer commands such as \lesssim or \geqslant.
        expr = re.sub(r"\\ge(?![A-Za-z])", r"\\geq", expr)
        expr = re.sub(r"\\le(?![A-Za-z])", r"\\leq", expr)
        expr = expr.replace(r"\Box", "□")
        # A box is presentational; remove only its balanced wrapper, not content.
        expr = FormulaRenderer._unwrap_command(expr, r"\boxed")
        expr = re.sub(r"\\(?:big|Big|bigg|Bigg)[lrmb]?", "", expr)
        # mathtext has no matrix environment.  Preserve row/column structure
        # in a parenthesised, semicolon-delimited mathematical expression.
        def matrix(m):
            rows=[" \\quad ".join(x.strip() for x in row.split("&")) for row in re.split(r"\\\\", m.group(1))]
            return r"\left( " + r" \, ; \, ".join(rows) + r" \right)"
        expr = re.sub(r"\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}", matrix, expr, flags=re.S)
        # mathtext does not implement \text or \operatorname.  Repeat so
        # simple adjacent forms are all converted; nested braces still fail and
        # are reported in diagnostics instead of silently printed as source.
        for _ in range(4):
            changed = re.sub(r"\\text\{([^{}]*)\}", lambda m: r"\mathrm{" + m.group(1).replace(" ", r"\ ") + "}", expr)
            changed = re.sub(r"\\operatorname\{([^{}]*)\}", lambda m: r"\mathrm{" + m.group(1) + "}", changed)
            if changed == expr: break
            expr = changed
        # MathText requires braces where TeX accepts an unbraced atom. Handle
        # Greek control sequences and nested numerators with balanced parsing.
        expr = FormulaRenderer._brace_arguments(expr)
        return expr
    @staticmethod
    def _brace_arguments(expr: str) -> str:
        arities = {"frac": 2, "boldsymbol": 1, "mathscr": 1, "mathbb": 1,
                   "mathcal": 1, "mathfrak": 1, "mathbf": 1}
        def atom(pos):
            while pos < len(expr) and expr[pos].isspace(): pos += 1
            start = pos
            if pos >= len(expr): return "", pos
            if expr[pos] == "{":
                depth = 1; pos += 1
                while pos < len(expr) and depth:
                    if expr[pos] == "{": depth += 1
                    elif expr[pos] == "}": depth -= 1
                    pos += 1
                return expr[start:pos], pos
            if expr[pos] == "\\":
                pos += 1
                while pos < len(expr) and expr[pos].isalpha(): pos += 1
                if pos == start + 1 and pos < len(expr): pos += 1
                return "{" + expr[start:pos] + "}", pos
            return "{" + expr[pos] + "}", pos + 1
        result = []; pos = 0
        while pos < len(expr):
            match = re.match(r"\\([A-Za-z]+)", expr[pos:])
            if not match or match.group(1) not in arities:
                result.append(expr[pos]); pos += 1; continue
            result.append(match.group(0)); pos += len(match.group(0))
            for _ in range(arities[match.group(1)]):
                arg, pos = atom(pos); result.append(arg)
        return "".join(result)
    @staticmethod
    def _unwrap_command(expr: str, command: str) -> str:
        """Remove a braced presentation command while retaining its payload."""
        out=[]; i=0
        while i < len(expr):
            if not expr.startswith(command, i): out.append(expr[i]); i += 1; continue
            j=i+len(command)
            while j < len(expr) and expr[j].isspace(): j += 1
            if j >= len(expr) or expr[j] != "{": out.append(expr[i]); i += 1; continue
            depth=1; k=j+1
            while k < len(expr) and depth:
                if expr[k]=="{": depth += 1
                elif expr[k]=="}": depth -= 1
                k += 1
            if depth: out.append(expr[i:]); break
            out.append(expr[j+1:k-1]); i=k
        return "".join(out)
    @staticmethod
    def _convert_plain_over(expr: str) -> str:
        r"""Recursively convert plain-TeX `{numerator \over denominator}`."""
        def over_at_top(s):
            depth=0; i=0
            while i < len(s):
                if s[i]=="{": depth += 1
                elif s[i]=="}": depth -= 1
                elif depth==0 and s.startswith(r"\over", i): return i
                i += 1
            return -1
        out=[]; i=0
        while i < len(expr):
            if expr[i] != "{": out.append(expr[i]); i+=1; continue
            depth=1; j=i+1
            while j < len(expr) and depth:
                if expr[j]=="{": depth+=1
                elif expr[j]=="}": depth-=1
                j+=1
            if depth: out.append(expr[i:]); break
            inner=FormulaRenderer._convert_plain_over(expr[i+1:j-1]); pos=over_at_top(inner)
            if pos >= 0:
                left=inner[:pos].strip(); right=inner[pos+len(r"\over"):].strip()
                out.append(r"\frac{"+left+"}{"+right+"}")
            else: out.append("{"+inner+"}")
            i=j
        return "".join(out)
    @staticmethod
    def _crop(path: Path) -> Path:
        try:
            from PIL import Image as PILImage, ImageChops
            im = PILImage.open(path).convert("RGBA")
            bg = PILImage.new("RGBA", im.size, (255,255,255,255))
            d = ImageChops.difference(im, bg).convert("L")
            # Alpha and near-black extent; white background from pdftoppm disappears.
            bbox = d.point(lambda x: 255 if x > 12 else 0).getbbox()
            if bbox:
                pad=5; bbox=(max(0,bbox[0]-pad),max(0,bbox[1]-pad),min(im.width,bbox[2]+pad),min(im.height,bbox[3]+pad))
                im.crop(bbox).save(path)
        except Exception: pass
        return path
    @staticmethod
    def _valid_png(path: Path) -> bool:
        try:
            from PIL import Image as PILImage
            with PILImage.open(path) as im:
                im.verify()
            return path.stat().st_size > 100
        except Exception:
            return False

class Renderer:
    def __init__(self, input_path: Path, refs: OrderedDict):
        self.input_path=input_path; self.base=input_path.parent; self.refs=refs
        self.refnums={k:i+1 for i,k in enumerate(refs)}; self.formulas=FormulaRenderer(); self.heading_ids={}; self.serial=0
        self.formula_failures=[]
        self.unknown_citations=[]
        self.layout_warnings=[]
        ss=getSampleStyleSheet()
        self.styles={
          "body": ParagraphStyle("body", parent=ss["BodyText"], fontName=SERIF, fontSize=10.5, leading=14, alignment=TA_JUSTIFY, spaceAfter=7, allowWidows=0, allowOrphans=0),
          "title": ParagraphStyle("title", parent=ss["Title"], fontName=SERIFB, fontSize=22, leading=28, alignment=TA_CENTER, spaceAfter=20),
          "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontName=SERIFB, fontSize=15.5, leading=20, spaceBefore=19, spaceAfter=8, keepWithNext=True),
          "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontName=SERIFB, fontSize=13, leading=17, spaceBefore=15, spaceAfter=6, keepWithNext=True),
          "h3": ParagraphStyle("h3", parent=ss["Heading3"], fontName=SERIFB, fontSize=11.2, leading=14, spaceBefore=11, spaceAfter=4, keepWithNext=True),
          "note": ParagraphStyle("note", parent=ss["BodyText"], fontName=SERIF, fontSize=7.5, leading=9.3, leftIndent=8, spaceBefore=-2, spaceAfter=5, textColor=colors.HexColor("#333333")),
          "code": ParagraphStyle("code", fontName=MONO, fontSize=7.5, leading=9, leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=8, backColor=colors.HexColor("#f1f1f1"), borderColor=colors.HexColor("#cfcfcf"), borderWidth=.35, borderPadding=5),
          "caption": ParagraphStyle("caption", fontName=SERIFI, fontSize=8.5, leading=11, alignment=TA_CENTER, spaceBefore=3, spaceAfter=9),
          "toc": ParagraphStyle("toc", fontName=SERIF, fontSize=10, leading=13, leftIndent=12, firstLineIndent=-12),
          "source": ParagraphStyle("source", fontName=SERIF, fontSize=8.6, leading=11.3, leftIndent=16, firstLineIndent=-16, spaceAfter=5),
        }
    def pandoc(self):
        cmd=["pandoc","--from","markdown+tex_math_dollars+tex_math_single_backslash+fenced_code_attributes","--to","json",str(self.input_path)]
        p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        if p.returncode: raise RuntimeError("pandoc failed: "+p.stderr)
        return json.loads(p.stdout)["blocks"]
    def _heading_key(self, label):
        base=re.sub(r"[^a-z0-9]+","-", prose(label).lower()).strip("-") or "section"
        n=self.heading_ids.get(base,0)+1; self.heading_ids[base]=n
        return base if n==1 else f"{base}-{n}"
    def inlines(self, xs, citations=None, math_max=145):
        out=[]
        for x in xs or []:
            t=x.get("t"); c=x.get("c")
            if t=="Str": out.append(escape(prose(c)))
            elif t in ("Space","SoftBreak","LineBreak"): out.append(" ")
            elif t=="Code": out.append("<font name='%s'>%s</font>"%(MONO,escape(c[1] if isinstance(c,list) else c)))
            elif t in ("Emph","Italic"): out.append("<i>%s</i>"%self.inlines(c,citations,math_max))
            elif t in ("Strong","Bold"): out.append("<b>%s</b>"%self.inlines(c,citations,math_max))
            elif t=="Strikeout": out.append(self.inlines(c,citations,math_max))
            elif t=="Quoted": out.append("&quot;"+self.inlines(c[1],citations,math_max)+"&quot;")
            elif t=="Link":
                target=c[2][0]; label=self.inlines(c[1],citations,math_max); out.append("<link href='%s' color='#222222'><u>%s</u></link>"%(escape(target,{'"':'&quot;'}),label))
            elif t=="Math":
                mode, expr=c; png=self.formulas.png(expr, display=False)
                if png:
                    try:
                        from PIL import Image as PI
                        # Formula rasters are made at 220dpi.  Map their native
                        # typographic size to PDF points; never impose a width
                        # floor (a one-letter inline symbol must stay small).
                        im=PI.open(png); native=72.0/220.0
                        ww=min(math_max, im.width*native); hh=im.height*native
                        if hh > 14:
                            factor=14.0/hh; ww*=factor; hh=14.0
                        if hh > 14.01:
                            self.layout_warnings.append({"kind":"inline_formula_overheight", "height_pt":round(hh,2), "expression":expr})
                        out.append("<img src='%s' width='%.1f' height='%.1f' valign='middle'/>"%(png,ww,hh))
                    except Exception:
                        self.formula_failures.append({"expression": expr, "mode": "inline", "reason": "formula image could not be embedded"})
                        out.append("<super>?</super>")
                else:
                    self.formula_failures.append({"expression": expr, "mode": "inline", "reason": "no TeX/mathtext renderer accepted this expression"})
                    out.append("<super>?</super>")
            elif t=="Cite":
                # c = [citations, formatted content]; cite numeric identifiers as superscript.
                keys=[]
                unknown=[]
                for cite in c[0]:
                    ident=cite.get("citationId","")
                    if ident in self.refnums: keys.append(ident)
                    else: unknown.append(ident)
                for ident in unknown:
                    self.unknown_citations.append({"id": ident, "rendered_content": re.sub("<[^>]+>", "", self.inlines(c[1], math_max=math_max))})
                if keys:
                    if citations is not None: citations.extend(keys)
                    nums=",".join(str(self.refnums[k]) for k in OrderedDict.fromkeys(keys))
                    out.append("<super>%s%s</super>"%(nums, ",?" if unknown else ""))
                else:
                    out.append("<super>?</super>")
            elif t=="Image":
                out.append("[Figure]")
            elif t=="Span": out.append(self.inlines(c[1],citations,math_max))
            elif t=="RawInline": pass
            else:
                # Robust fallback for new Pandoc inline variants.
                if isinstance(c,list): out.append(self.inlines(c,citations,math_max))
        return "".join(out)
    def citation_note(self, keys):
        keys=list(OrderedDict.fromkeys(k for k in keys if k in self.refs))
        if not keys: return None
        bits=[]
        for k in keys:
            r=self.refs[k]; authors=r.get("authors",r.get("author","")); authors="; ".join(authors) if isinstance(authors,list) else str(authors)
            date=str(r.get("date", "n.d.")); title=prose(str(r.get("title", k))); url=str(r.get("url", ""))
            label=f"{authors} ({date}), <i>{escape(title)}</i>" if authors else f"{date}, <i>{escape(title)}</i>"
            if url: label="<link href='%s' color='#222222'><u>%s</u></link>"%(escape(url,{'"':'&quot;'}),label)
            bits.append("<super>%d</super> %s"%(self.refnums[k],label))
        return Paragraph("; ".join(bits),self.styles["note"])
    def para(self, xs):
        cites=[]; body=self.inlines(xs,cites)
        result=[Paragraph(body or " ",self.styles["body"])]
        note=self.citation_note(cites)
        if note: result.append(note)
        return result
    def image_block(self, image):
        c=image["c"]; alt=self.inlines(c[1]); src=c[2][0]; path=(self.base/src).resolve()
        if not path.exists(): return [Paragraph("<i>[Missing figure: %s]</i>"%escape(prose(src)),self.styles["caption"])]
        try:
            ir=ImageReader(str(path)); iw,ih=ir.getSize(); maxw=CONTENT_W*.93; maxh=(H-MARGIN_T-MARGIN_B)*.62
            scale=min(maxw/iw,maxh/ih,1); im=Image(str(path),iw*scale,ih*scale); im.hAlign="CENTER"
            ret=[Spacer(1,4),im]
            if alt: ret.append(Paragraph(alt,self.styles["caption"]))
            return ret
        except Exception as e: return [Paragraph("<i>[Unreadable figure: %s]</i>"%escape(prose(src)),self.styles["caption"])]
    def code(self, text):
        fixed=[]
        for line in prose(text).splitlines() or [""]:
            indent=re.match(r"\s*",line).group(0); content=line[len(indent):]
            chunks=textwrap.wrap(content,width=max(18,90-len(indent)),break_long_words=True,break_on_hyphens=False,subsequent_indent=" "*len(indent)) or [""]
            fixed.extend([indent+z if i==0 else z for i,z in enumerate(chunks)])
        return [XPreformatted(escape("\n".join(fixed)),self.styles["code"])]
    def list_block(self, c, ordered=False):
        # OrderedList: [attrs, listitems]; BulletList: listitems. Each item is blocks.
        items=c[1] if ordered else c
        start=1
        if ordered and c and isinstance(c[0],list) and c[0]: start=c[0][0]
        story=[]
        for i, blocks in enumerate(items):
            prefix=(str(start+i)+". " if ordered else u"• ")
            first=True
            for b in blocks:
                sub=self.block(b)
                for f in sub:
                    if first and isinstance(f,Paragraph):
                        style=ParagraphStyle("list",parent=f.style,leftIndent=17,firstLineIndent=-14,spaceAfter=4)
                        f=Paragraph(prefix+f.text, style)
                        first=False
                    story.append(f)
        return story
    def cell_text(self, cell, math_max=72):
        # Pandoc Cell is [attr, alignment, rowspan, colspan, blocks].
        blocks = cell[4] if isinstance(cell, list) and len(cell) >= 5 else cell
        parts=[]
        for b in blocks:
            if b["t"] in ("Para","Plain"): parts.append(self.inlines(b["c"], math_max=math_max))
            elif b["t"]=="CodeBlock": parts.append("<font name='%s'>%s</font>"%(MONO,escape(b["c"][1])))
        return "<br/>".join(parts) or " "
    def blocks_text(self, blocks):
        return " ".join(self.inlines(b.get("c", [])) for b in blocks or [] if b.get("t") in ("Para", "Plain"))
    def table(self,c):
        # Pandoc 2.17+: attr, caption, colspecs, head, bodies, foot
        try:
            _, caption, specs, head, bodies, foot=c
            ncols=len(specs)
            rows=[]
            headrows=head[1]
            for row in headrows:
                rows.append([self.cell_text(cell, max(34, CONTENT_W/ncols-12)) for cell in row[1]])
            for body in bodies:
                for row in body[3]: rows.append([self.cell_text(cell, max(34, CONTENT_W/ncols-12)) for cell in row[1]])
            if foot and foot[1]:
                for row in foot[1]: rows.append([self.cell_text(cell, max(34, CONTENT_W/ncols-12)) for cell in row[1]])
            if not rows: return []
            # split very long cells into continuation rows, keeping LongTable rows bounded.
            expanded=[]
            for ri,row in enumerate(rows):
                if ri==0: expanded.append(row); continue
                chunks=[]
                for cell in row:
                    plain=re.sub("<[^>]*>","",cell)
                    # Preserve inline equation and link markup for normal cells;
                    # continuation splitting is only needed for genuinely tall cells.
                    pieces=([cell] if len(plain) <= 650 else textwrap.wrap(plain, 650, break_long_words=False)) or [plain]
                    chunks.append(pieces)
                for j in range(max(map(len,chunks))): expanded.append([arr[j] if j<len(arr) else "" for arr in chunks])
            data=[]
            for ri,row in enumerate(expanded):
                style=ParagraphStyle("th" if ri==0 else "td",parent=self.styles["body"],fontName=SERIFB if ri==0 else SERIF,fontSize=8.2,leading=10.2,spaceAfter=0,alignment=TA_LEFT)
                data.append([Paragraph(z,style) for z in row])
            widths=[CONTENT_W/ncols]*ncols
            first_header=re.sub("<[^>]*>","",rows[0][0]).strip()
            if ncols==4 and first_header=="ID":
                widths=[CONTENT_W*f for f in (.08,.32,.49,.11)]
            elif ncols==3 and first_header=="Step":
                widths=[CONTENT_W*f for f in (.10,.20,.70)]
            t=LongTable(data,colWidths=widths,repeatRows=1,splitByRow=1,hAlign="LEFT")
            t.setStyle(TableStyle([("GRID",(0,0),(-1,-1),.3,colors.HexColor("#a0a0a0")),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e4e4e4")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
            cap=self.blocks_text(caption[1]) if caption and len(caption)>1 and caption[1] else ""
            out=[t]
            if cap: out.append(Paragraph(cap,self.styles["caption"]))
            out.append(Spacer(1,6)); return out
        except Exception as e:
            return [Paragraph("<i>[Table could not be rendered: %s]</i>"%escape(prose(str(e))),self.styles["caption"])]
    def block(self,b):
        t=b.get("t"); c=b.get("c")
        if t in ("Para","Plain"):
            if len(c)==1 and c[0].get("t")=="Image": return self.image_block(c[0])
            return self.para(c)
        if t=="Header":
            lev, attr, xs=c; label=self.inlines(xs); key=attr[0] or self._heading_key(re.sub("<[^>]+>","",label))
            return [Heading(label,self.styles["h%d"%min(3,lev)],lev,key)]
        if t=="CodeBlock": return self.code(c[1])
        if t=="BulletList": return self.list_block(c)
        if t=="OrderedList": return self.list_block(c,True)
        if t=="BlockQuote":
            flows=[]
            for sub in c:
                for f in self.block(sub):
                    if isinstance(f,Paragraph): f.style=ParagraphStyle("quote",parent=f.style,leftIndent=18,rightIndent=12,textColor=colors.HexColor("#333333"))
                    flows.append(f)
            return flows
        if t=="HorizontalRule": return [Spacer(1,4),Rule(),Spacer(1,6)]
        if t=="Table": return self.table(c)
        if t=="Div":
            out=[]
            for sub in c[1]: out.extend(self.block(sub))
            return out
        if t=="RawBlock": return []
        # New/unsupported blocks are rendered as plain text if safely possible.
        return []
    def display_math_block(self, expr):
        png=self.formulas.png(expr, True)
        if not png:
            self.formula_failures.append({"expression": expr, "mode": "display", "reason": "no TeX/mathtext renderer accepted this expression"})
            return [Paragraph("Equation rendering unavailable; see renderer diagnostics.",self.styles["caption"])]
        try:
            from PIL import Image as PI
            im=PI.open(png); maxw=CONTENT_W*.88; maxh=H*.33
            native=72.0/220.0
            scale=min(native, maxw/im.width, maxh/im.height)
            effective=11.0*(scale/native)
            if effective < 8.5:
                self.layout_warnings.append({"kind":"display_formula_downscaled", "effective_font_pt":round(effective,2), "expression":expr})
            flow=Image(str(png),im.width*scale,im.height*scale); flow.hAlign="CENTER"
            return [Spacer(1,4),flow,Spacer(1,7)]
        except Exception:
            self.formula_failures.append({"expression": expr, "mode": "display", "reason": "formula image could not be embedded"})
            return [Paragraph("Equation rendering unavailable; see renderer diagnostics.",self.styles["caption"])]
    def transform_display_math(self, blocks):
        """Turn every Pandoc DisplayMath inline into its own block.

        Pandoc is allowed to group adjacent `$$...$$` forms in a single Para.
        Rendering that Para wholesale would make each display formula an inline
        145pt image, so split the paragraph while preserving all intervening
        text and every formula in order.
        """
        result=[]
        for b in blocks:
            if b.get("t") in ("Para", "Plain") and any(x.get("t")=="Math" and x["c"][0].get("t")=="DisplayMath" for x in b.get("c", [])):
                pending=[]
                for inline in b["c"]:
                    if inline.get("t")=="Math" and inline["c"][0].get("t")=="DisplayMath":
                        if pending: result.append({"t":"Para", "c":pending}); pending=[]
                        result.append({"t":"_DisplayMath", "c":inline["c"][1]})
                    else:
                        pending.append(inline)
                if pending: result.append({"t":"Para", "c":pending})
            elif b.get("t")=="Div":
                b=dict(b); b["c"]=[b["c"][0], self.transform_display_math(b["c"][1])]; result.append(b)
            else:
                result.append(b)
        return result
    def build(self, output: Path):
        blocks=self.transform_display_math(self.pandoc())
        story=[]
        # first heading is the simple cover title; other headings feed the TOC.
        first_header=None
        for b in blocks:
            if b.get("t")=="Header": first_header=b; break
        if first_header:
            title=self.inlines(first_header["c"][2]); story += [Spacer(1,H*.27),Paragraph(title,self.styles["title"]),PageBreak()]
        else:
            title="Quantum Electromagnetism and Gravitation"
        toc=TableOfContents(); toc.levelStyles=[ParagraphStyle("toc1",parent=self.styles["toc"],leftIndent=0),ParagraphStyle("toc2",parent=self.styles["toc"],leftIndent=15),ParagraphStyle("toc3",parent=self.styles["toc"],leftIndent=30)]
        story += [Paragraph("Contents",self.styles["h1"]),Spacer(1,3),toc,PageBreak()]
        skipped_title=False
        # Keep a short closing prose subsection intact before a forced
        # bibliography page break, avoiding a nearly empty continuation page.
        closing_index=max((i for i,b in enumerate(blocks) if b.get("t")=="Header"), default=len(blocks))
        closing_blocks=blocks[closing_index+1:]
        keep_closing=(bool(closing_blocks) and len(closing_blocks)<=4 and
                      all(b.get("t") in ("Para","Plain") for b in closing_blocks) and
                      sum(len(json.dumps(b)) for b in closing_blocks)<10000)
        closing=[]
        for i,b in enumerate(blocks):
            if b is first_header and not skipped_title: skipped_title=True; continue
            destination=closing if keep_closing and i>=closing_index else story
            if b.get("t")=="_DisplayMath": destination.extend(self.display_math_block(b["c"]))
            else: destination.extend(self.block(b))
        if closing: story.append(KeepTogether(closing))
        if self.refs:
            story += [PageBreak(),Heading("Sources",self.styles["h1"],1,"sources")]
            for ident,r in self.refs.items():
                authors=r.get("authors",r.get("author","")); authors="; ".join(map(str,authors)) if isinstance(authors,list) else str(authors)
                entries=[authors, str(r.get("date","n.d.")), "<i>%s</i>"%escape(prose(str(r.get("title",ident))))]
                for field in ("role","readdepth","access"):
                    if r.get(field): entries.append(escape(prose(str(r[field]))))
                url=str(r.get("url", "")); text=". ".join(str(x).rstrip(".") for x in entries if x)
                if url: text += ". <link href='%s' color='#222222'><u>%s</u></link>"%(escape(url,{'"':'&quot;'}),escape(prose(url)))
                story.append(Paragraph("<b>%d.</b> %s"%(self.refnums[ident],text),self.styles["source"]))
        output.parent.mkdir(parents=True,exist_ok=True)
        doc=PDFDoc(str(output),title=html.unescape(re.sub("<[^>]+>", "", title)),leftMargin=MARGIN_L,rightMargin=MARGIN_R,topMargin=MARGIN_T,bottomMargin=MARGIN_B)
        doc.multiBuild(story)
    def write_diagnostics(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        payload={
            "input": str(self.input_path),
            "formula_failures": self.formula_failures,
            "unknown_citations": self.unknown_citations,
            "layout_warnings": self.layout_warnings,
            "summary": {
                "formula_failures": len(self.formula_failures),
                "unknown_citations": len(self.unknown_citations),
                "layout_warnings": len(self.layout_warnings),
                "status": "clean" if not self.formula_failures and not self.unknown_citations and not self.layout_warnings else "review_required",
            },
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def load_refs(path: Path):
    raw=json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    if not isinstance(raw,dict): raise ValueError("references.json must be an object keyed by citation ID")
    return raw

def main():
    ap=argparse.ArgumentParser(description="Render scientific Pandoc Markdown as a paginated A4 PDF.")
    ap.add_argument("--input",required=True,type=Path); ap.add_argument("--references",required=True,type=Path); ap.add_argument("--output",required=True,type=Path)
    ap.add_argument("--diagnostics",type=Path, help="JSON sidecar path (default: output name with .diagnostics.json)")
    ns=ap.parse_args()
    if not ns.input.exists(): ap.error("input file not found: "+str(ns.input))
    if not ns.references.exists(): ap.error("references file not found: "+str(ns.references))
    renderer=Renderer(ns.input,load_refs(ns.references)); renderer.build(ns.output)
    diagnostics=ns.diagnostics or ns.output.with_suffix(".diagnostics.json")
    renderer.write_diagnostics(diagnostics)
    print(ns.output)
    print(diagnostics)
if __name__=="__main__": main()
