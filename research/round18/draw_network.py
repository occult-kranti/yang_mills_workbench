"""Deterministic collaboration topology, not an executed-status authority."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[2]
rows=[('Initial advisor decision','Review inherited goals and freeze A1'),('A1 → A2','Dressed bridge → growing-family exception'),('Post-A advisor decision','Revise B and C from the two accepted A loops'),('B1 → B2','Complete omitted spectrum → full energy enclosure'),('C1 → C2','Complete central coordinates → surrounding integration'),('Next roadmap','Retain open homogeneous, bulk and continuum bridges')]
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="920" viewBox="0 0 900 920" role="img" aria-labelledby="title desc">','<title id="title">Three-role six-loop collaboration</title><desc id="desc">Forward and backward researchers report independently to the advisor. Each pair is sequential; a second advisor decision follows Goal A.</desc>','<rect width="900" height="920" rx="20" fill="#f7fafc"/>','<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#385777"/></marker></defs>']
for x,label,color in [(30,'Forward researcher','#17637a'),(335,'Advisor–skeptic','#49376e'),(640,'Backward researcher','#17637a')]:
 svg.append(f'<rect x="{x}" y="25" width="230" height="68" rx="12" fill="{color}"/><text x="{x+115}" y="65" text-anchor="middle" fill="white" font-size="19" font-family="sans-serif">{escape(label)}</text>')
svg += ['<path d="M260 60H332 M640 60H570" stroke="#385777" stroke-width="2.5" marker-end="url(#arrow)"/>','<text x="450" y="128" text-anchor="middle" font-size="16" font-family="sans-serif" fill="#34485c">Independent evidence → critique → accepted next contract</text>']
for i,(title,desc) in enumerate(rows):
 y=155+i*120
 if i:svg.append(f'<path d="M450 {y-25}V{y-5}" stroke="#385777" stroke-width="2" marker-end="url(#arrow)"/>')
 svg.append(f'<rect x="85" y="{y}" width="730" height="95" rx="12" fill="white" stroke="#b7c9d5"/><text x="450" y="{y+34}" text-anchor="middle" font-size="22" font-weight="bold" font-family="sans-serif" fill="#20384b">{escape(title)}</text><text x="450" y="{y+66}" text-anchor="middle" font-size="17" font-family="sans-serif" fill="#40586b">{escape(desc)}</text>')
svg.append('</svg>')
(ROOT/'dist/next-collaboration.svg').write_text('\n'.join(svg)+'\n')
