#!/usr/bin/env python3
"""Integrate only gated Round29 derivations, keeping every source immutable."""
from pathlib import Path
import hashlib,json,re,subprocess
def require(condition,message):
 if not condition:raise ValueError(message)
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'papers/draft-02';dest=OUT/'addenda/round29';dest.mkdir(parents=True,exist_ok=True)
findings=json.loads((ROOT/'research/round29/advisor/findings.json').read_text());r=json.loads((OUT/'registry/hnm-registry.json').read_text())
previous_locators={x['legacy_label']:x.get('printed_locator') for x in r['equations']}
r['contributions']=[x for x in r['contributions'] if x['round']!=29]
r['equations']=[x for x in r['equations'] if not x['legacy_label'].startswith('r29:')]

def tx(s):
 s=str(s).replace('–','--').replace('—','---').replace('→','to').replace('≤','<=').replace('≥','>=').replace('≠','!=').replace('∞','infinity').replace('×','x').replace('∈','in')
 return ''.join({'\\':r'\textbackslash{}','^':r'\textasciicircum{}','~':r'\textasciitilde{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}'}.get(c,c) for c in s)

MATH_CODE={
 '(pi,H_num_space,Omega)':r'(\pi,\mathcal H_{\rm num},\Omega)',
 'G=product_(v in V)SU(2)':r'G=\prod_{v\in V}\mathrm{SU}(2)',
 'U_(x,j) -> g_x U_(x,j) g_(x+e_j)^(-1)':r'U_{x,j}\longmapsto g_xU_{x,j}g_{x+e_j}^{-1}',
 'g -> beta_g(A)':r'g\longmapsto\beta_g(A)',
 'omega_num(A* beta_g(A))':r'\omega_{\rm num}(A^*\beta_g(A))',
 'P_G xi=int_G V_g xi dg':r'P_G\xi=\int_GV_g\xi\,dg',
 'P_G^2=P_G=P_G*':r'P_G^2=P_G=P_G^*',
 'X -> omega_num(B* X)':r'X\longmapsto\omega_{\rm num}(B^*X)',
 'P_G D(H_num) subset D(H_num)':r'P_GD(H_{\rm num})\subset D(H_{\rm num})',
 'H_num P_G=P_G H_num':r'H_{\rm num}P_G=P_GH_{\rm num}',
 'K_N=Hraw_N-Eraw_N=delta(Hhat_N-Ehat_N)':r'K_N=H_N^{\rm raw}-E_N^{\rm raw}=\delta(\widehat H_N-\widehat E_N)',
 'm_gap=delta/2=alpha/16':r'm_{\rm gap}=\delta/2=\alpha/16',
 'chi_(N,A)=(A-omega_N(A))Omega_N':r'\chi_{N,A}=(A-\omega_N(A))\Omega_N',
 '[m_gap,infinity)':r'[m_{\rm gap},\infty)',
 'chi_A=(pi(A)-a)Omega':r'\chi_A=(\pi(A)-a)\Omega',
 'f in C_c^infinity((-infinity,m_gap))':r'f\in C_c^\infty(({-\infty},m_{\rm gap}))',
 'f(E)=int_R fhat_hbar(t) exp(it E/hbar) dt':r'f(E)=\int_{\mathbb R}\widehat f_\hbar(t)e^{itE/\hbar}\,dt',
 'int f dnu_A=0':r'\int f\,d\nu_A=0',
 'nu_A((-infinity,m_gap))=0':r'\nu_A(({-\infty},m_{\rm gap}))=0',
 'H_phys intersect Omega-perp':r'\mathcal H_{\rm phys}\cap\Omega^\perp',
 'Omega-perp':r'\Omega^\perp',
 '1_[0,alpha/16)(H)=|Omega><Omega|':r'\mathbf1_{[0,\alpha/16)}(H)=|\Omega\rangle\langle\Omega|',
 'W=(1/2)Tr(U_(0,x) U_(e_x,z) U_(e_z,x)^(-1) U_(0,z)^(-1))':r'W=\tfrac12\operatorname{Tr}(U_{0,x}U_{e_x,z}U_{e_z,x}^{-1}U_{0,z}^{-1})',
 'P_R=P_0 tensor P_(e_z)':r'P_R=P_0\otimes P_{e_z}',
 '2||phi_b||=14|tau|':r'2\|\phi_b\|=14|\tau|',
 'epsilon=1-Tr(rho_R P_R)<=98|tau|':r'\varepsilon=1-\operatorname{Tr}(\rho_RP_R)\le98|\tau|',
 '2sqrt(1-overlap)':r'2\sqrt{1-\mathrm{overlap}}',
 'q_0 I+i q.sigma':r'q_0I+i\boldsymbol q\cdot\boldsymbol\sigma',
 'Tr(P_R W)=0':r'\operatorname{Tr}(P_RW)=0',
 'Tr(P_R W^2)=1/4':r'\operatorname{Tr}(P_RW^2)=1/4',
 '(pi(W)-omega_num(W))Omega':r'(\pi(W)-\omega_{\rm num}(W))\Omega',
 '[alpha/16,infinity)':r'[\alpha/16,\infty)',
 'U(t)e_j=e^(ijt)e_j':r'U(t)e_j=e^{ijt}e_j',
 '||U(pi/n)A U(pi/n)*-A||=2':r'\|U(\pi/n)AU(\pi/n)^*-A\|=2',
 'pi(x,y,z)=(floor(x/4),floor(y/2),z)':r'\pi(x,y,z)=(\lfloor x/4\rfloor,\lfloor y/2\rfloor,z)',
 'Hhat_N=sum_(b in Lambda_N)h_b + sum_(b+S subset Lambda_N)phi_b':r'\widehat H_N=\sum_{b\in\Lambda_N}h_b+\sum_{b+S\subset\Lambda_N}\phi_b',
 '||phi_b||=M=7|tau|':r'\|\phi_b\|=M=7|\tau|',
 'K_N=delta(Hhat_N-Ehat_N)':r'K_N=\delta(\widehat H_N-\widehat E_N)',
 'P_F=tensor_(b in F)P_b':r'P_F=\bigotimes_{b\in F}P_b',
 'omega_num(A)=Tr rho_F A':r'\omega_{\rm num}(A)=\operatorname{Tr}(\rho_F A)',
 'sum_(r>=1)(r+1)^-2<=1':r'\sum_{r\ge1}(r+1)^{-2}\le1',
 'sum_(X subset Lambda)Phi(X)':r'\sum_{X\subset\Lambda}\Phi(X)',
 'omega_num(T_t(A))=omega_num(A)':r'\omega_{\rm num}(\mathcal T_t(A))=\omega_{\rm num}(A)',
 'U_t pi(A)Omega=pi(T_t(A))Omega':r'U_t\pi(A)\Omega=\pi(\mathcal T_t(A))\Omega',
 'omega_num(A* T_t^D(A))':r'\omega_{\rm num}(A^*\mathcal T_t^D(A))',
 'omega_num(A* T_t(A))':r'\omega_{\rm num}(A^*\mathcal T_t(A))',
 '||(U_t-I)pi(A)Omega||^2=2omega_num(A*A)-2Re omega_num(A*T_t(A)) ->0':r'\|(U_t-I)\pi(A)\Omega\|^2=2\omega_{\rm num}(A^*A)-2\operatorname{Re}\omega_{\rm num}(A^*\mathcal T_t(A))\longrightarrow0',
 'U_t=exp(it H_num/hbar)':r'U_t=\exp(itH_{\rm num}/\hbar)',
 'c_(N,A)(t)=omega_N(A* T_t^N(A))=<A Omega_N,e^(itK_N/hbar)A Omega_N>':r'c_{N,A}(t)=\omega_N(A^*\mathcal T_t^N(A))=\langle A\Omega_N,e^{itK_N/\hbar}A\Omega_N\rangle',
 'c_A(t)=<pi(A)Omega,e^(itH_num/hbar)pi(A)Omega>':r'c_A(t)=\langle\pi(A)\Omega,e^{itH_{\rm num}/\hbar}\pi(A)\Omega\rangle',
 'int f dnu_(N,A)=0':r'\int f\,d\nu_{N,A}=0',
 'closure(pi(A_phys)Omega)':r'\overline{\pi(\mathcal A_{\rm phys})\Omega}',
 'chi_Lambda=(W-m_Lambda)Omega_Lambda':r'\chi_\Lambda=(W-m_\Lambda)\Omega_\Lambda',
 'chi=(pi(W)-m)Omega':r'\chi=(\pi(W)-m)\Omega',
 'int E^2 dnu_Lambda <= B2':r'\int E^2\,d\nu_\Lambda\le B_2',
 'mu1_Lambda=alpha omega_Lambda(1-W^2)':r'\mu_{1,\Lambda}=\alpha\omega_\Lambda(1-W^2)',
 's=alpha omega(1-W^2)':r's=\alpha\omega(1-W^2)',
 'F_L(E)=E theta(E/L)':r'F_L(E)=E\theta(E/L)',
 'Q_L(E)=E^2 theta(E/L)':r'Q_L(E)=E^2\theta(E/L)',
 'int Q_L dnu=lim_Lambda int Q_L dnu_Lambda<=B2':r'\int Q_L\,d\nu=\lim_\Lambda\int Q_L\,d\nu_\Lambda\le B_2',
 '0<=mu1_Lambda-int F_L dnu_Lambda<=B2/L':r'0\le\mu_{1,\Lambda}-\int F_L\,d\nu_\Lambda\le B_2/L',
 '0<=s-int F_L dnu<=B2/L':r'0\le s-\int F_L\,d\nu\le B_2/L',
 'int F_L dnu':r'\int F_L\,d\nu',
 'int E dnu=s':r'\int E\,d\nu=s',
 '||H_phys chi||^2<=B2':r'\|H_{\rm phys}\chi\|^2\le B_2',
 'chi_Lambda=(W-omega_Lambda(W))Omega_Lambda':r'\chi_\Lambda=(W-\omega_\Lambda(W))\Omega_\Lambda',
 'K_Lambda=Hraw_Lambda-Eraw_Lambda':r'K_\Lambda=H^{\rm raw}_\Lambda-E^{\rm raw}_\Lambda',
 '(R-S) intersect Z_+^3={0,e_z}':r'(R-S)\cap\mathbb Z_+^3=\{0,e_z\}',
 'T_R=alpha sum_(e owned by R)C_e':r'T_R=\alpha\sum_{e\text{ owned by }R}C_e',
 'Vsel_R=-sum_(selected faces in R)lambda_f W_f':r'V_R^{\rm sel}=-\sum_{\substack{f\text{ selected}\\ f\text{ in }R}}\lambda_fW_f',
 'B_R=sum_(b in R)Estrip_b':r'B_R=\sum_{b\in R}E_{{\rm strip},b}',
 'C_e=-sum_a X_ea^2':r'C_e=-\sum_aX_{ea}^2',
 '[C_e,W]u=(C_eW)u-2 sum_a(X_eaW)X_ea u':r'[C_e,W]u=(C_eW)u-2\sum_a(X_{ea}W)X_{ea}u',
 'sum_(e in p,a)(X_eaW)^2=1-W^2<=1':r'\sum_{e\in p,a}(X_{ea}W)^2=1-W^2\le1',
 '||W Omega||<=1':r'\|W\Omega\|\le1',
 '||u+v||^2<=2||u||^2+2||v||^2':r'\|u+v\|^2\le2\|u\|^2+2\|v\|^2',
 'O_(n,L)=[-n,L-n]^3':r'O_{n,L}=[-n,L-n]^3',
 'C_M=[-M,M]^3':r'C_M=[-M,M]^3',
 '||rho_(C_M,F)-rho_(C_M\',F)||_1 <= epsilon_n(F)':r'\|\rho_{C_M,F}-\rho_{C_{M\prime},F}\|_1\le\varepsilon_n(F)',
 'Tr_(F\'\\F) rho_(C_M,F\')=rho_(C_M,F)':r'\operatorname{Tr}_{F\prime\setminus F}\rho_{C_M,F\prime}=\rho_{C_M,F}',
 'omega_Z(A)=Tr(rho_F A)':r'\omega_{\mathbb Z}(A)=\operatorname{Tr}(\rho_F A)',
 '|omega_+(T_(b_n) A)-rho_(C_M,F)(A)| <= epsilon_n(F)||A||':r'|\omega_+(T_{b_n}A)-\rho_{C_M,F}(A)|\le\varepsilon_n(F)\|A\|',
 'rho_(C_M)(T_k A)=rho_(C_M-k)(A)':r'\rho_{C_M}(T_kA)=\rho_{C_M-k}(A)',
 '|omega_Z(T_k A)-omega_Z(A)|':r'|\omega_{\mathbb Z}(T_kA)-\omega_{\mathbb Z}(A)|',
 'H1=H_(A_n)+sum_{x in B_n\\A_n}h_x':r'H_1=H_{A_n}+\sum_{x\in B_n\setminus A_n}h_x',
 'H2=H_(B_n)':r'H_2=H_{B_n}',
 '7|tau|<=c_HTW(1,1)':r'7|\tau|\le c_{\mathrm{HTW}}(1,1)',
 'D(H_(0,B_n))=D(H_(0,D_n)) intersect D(H_(0,B_n\\D_n))':r'D(H_{0,B_n})=D(H_{0,D_n})\cap D(H_{0,B_n\setminus D_n})',
 'Tr rho_i T*[H_*,T]=<T Psi_i,(H_i-E_i)T Psi_i> >=0':r'\Tr(\rho_iT^*[H_*,T])=\langle T\Psi_i,(H_i-E_i)T\Psi_i\rangle\ge0',
 '|Tr((rho1-rho2)A)| <= exp(C1|Y| - C2 dist(Y,Z^3\\D_n)) ||A||':r'|\Tr((\rho_1-\rho_2)A)|\le e^{C_1|Y|-C_2\operatorname{dist}(Y,\mathbb Z^3\setminus D_n)}\|A\|',
 'P_M=(tensor_{x in M}Q_x)(tensor_{y outside M}P_y)':r'P_M=(\bigotimes_{x\in M}Q_x)(\bigotimes_{y\notin M}P_y)',
 'H_M=sum_{x in M}h_x>=|M|':r'H_M=\sum_{x\in M}h_x\ge |M|',
 'c_I in tensor_{x in I}Q_x H_x':r'c_I\in\bigotimes_{x\in I}Q_x\mathcal H_x',
 'hat(c_I)=|c_I><Omega_I| tensor I_outside':r'\widehat{c_I}=|c_I\rangle\langle\Omega_I|\otimes I_{I^c}',
 'C=sum_{I nonempty}hat(c_I)':r'C=\sum_{I\ne\varnothing}\widehat{c_I}',
 '||c||_a=max_u sum_{I contains u}||c_I||':r'\|c\|_a=\max_u\sum_{I\ni u}\|c_I\|',
 'N=union_j I_j':r'N=\bigcup_j I_j',
 'N\\X subset M subset N union X':r'N\setminus X\subset M\subset N\cup X',
 '||V_X|| product_j||c_{j,I_j}||':r'\|V_X\|\prod_j\|c_{j,I_j}\|',
 'sum_{I:I intersects X}||c_I||<=p||c||_a':r'\sum_{I:I\cap X\ne\varnothing}\|c_I\|\le p\|c\|_a',
 '2^p(2p)^k J product||c_j||_a':r'2^p(2p)^k J\prod_j\|c_j\|_a',
 'ad_C^8(V)Omega=8!|1111>':r'\operatorname{ad}_C^8(V)\Omega=8!|1111\rangle',
 'ad_C^9(V)=0':r'\operatorname{ad}_C^9(V)=0',
 '[C,H_0]=-sum_I hat(H_I c_I)':r'[C,H_0]=-\sum_I\widehat{H_Ic_I}',
 'psi(s)=e^{-C(s)}Omega_0':r'\psi(s)=e^{-C(s)}\Omega_0',
 "J G'(R)":r"J G'(R)",
 'e^{C(s)}phi=b_0 Omega_0+sum_{M nonempty} b_M':r'e^{C(s)}\phi=b_0\Omega_0+\sum_{M\ne\varnothing}b_M',
 'B=sum_M hat(b_M)':r'B=\sum_M\widehat{b_M}',
 'phi=(b_0+B)psi':r'\phi=(b_0+B)\psi',
 "||b||_a <= 2J G'(R)||b||_a < ||b||_a":r"\|b\|_a\le 2JG'(R)\|b\|_a<\|b\|_a",
 '(W_p-<W_p>)Omega_H':r'(W_p-\langle W_p\rangle)\Omega_H',
 '||u||^2+<u,H_0u>':r'\|u\|^2+\langle u,H_0u\rangle',
 '||phi_b||=7|tau|':r'\|\phi_b\|=7|\tau|',
}

def inline_math(code):
 """Typeset explicit mathematical code tokens; leave commands/paths as code."""
 if code in MATH_CODE:return MATH_CODE[code]
 if any(z in code for z in ['research/','/absolute/','check.py','report.md','--output','python','json','.py']):return None
 if code.endswith(('_','^')):return None
 code=code.replace('’',"'").replace('‘',"'")
 code=re.sub(r'\b(mu|C|B)([12])\b',r'\1_\2',code)
 tokens=set(re.findall(r'[A-Za-z][A-Za-z0-9]*',code))
 names={'alpha','lambda','tau','epsilon','delta','eta','beta','hbar','star','tilde','sum','strip','pi','Tr','KS','c1','c2','a0','E0','kalpha','klambda','kdelta','kE0','CI','Lambda','Omega','omega','chi','nu','mu','rho','psi','sigma','Phi','phi','varepsilon','num','Estrip','Vsel','norm','phys','diag','ref','vac','sup','inf','max','min','sqrt','log','exp'}
 if any(len(x)>2 and x not in names for x in tokens):return None
 if not (set('=<>_^')&set(code) or any(x in names for x in tokens) or (len(tokens)<=2 and len(code)<20)):return None
 out=re.sub(r'([A-Za-z]+)_\(([^()]*)\)',r'\1_{\2}',code)
 for a,b in [('²','^2'),('³','^3'),('⁴','^4'),('→',r'\to '),('<=',r'\le '),('>=',r'\ge '),('->',r'\to '),('||',r'\|')]:out=out.replace(a,b)
 out=re.sub(r'\^(-?\d+)',lambda m:'^{'+m[1]+'}',out)
 out=re.sub(r'Estrip_([A-Za-z0-9]+)',lambda m:r'E_{\mathrm{strip},'+m[1]+'}',out)
 out=re.sub(r'Vsel_([A-Za-z0-9]+)',lambda m:'V_{'+m[1]+r'}^{\mathrm{sel}}',out)
 for a,b in [('H_tilde',r'\widetilde H'),('E_tilde',r'\widetilde E'),('H_KS',r'H_{\mathrm{KS}}'),('E_strip,b',r'E_{\mathrm{strip},b}'),('E_star',r'E_\star'),('kalpha',r'k\alpha'),('klambda',r'k\lambda'),('kdelta',r'k\delta'),('kE0',r'kE_0'),('c1','c_1'),('c2','c_2'),('a0','a_0'),('E0','E_0')]:out=out.replace(a,b)
 # Do not touch already escaped command names.
 for name in ['alpha','lambda','tau','epsilon','delta','eta','beta','hbar','pi','Lambda','Omega','omega','chi','nu','mu','rho','psi','sigma','Phi','phi','varepsilon','sum','exp','max','min','sup','inf','log']:
  out=re.sub(r'(?<![A-Za-z\\])'+name+r'(?![A-Za-z0-9])',lambda m:'\\'+name,out)
 out=out.replace("C_M'","C_{M'}")
 for name in ['phys','ref','vac','diag','strip','num']:
  out=re.sub('_'+name+r'(?![A-Za-z0-9])',lambda m:r'_{\mathrm{'+name+'}}',out)
 out=out.replace('0..3',r'0,\ldots,3').replace('0..1',r'0,1')
 # Braces in the plain source denote visible finite sets, except generated TeX groups.
 out=re.sub(r'\{(0,[^}]*)\}',lambda m:r'\{'+m[1]+r'\}',out)
 for plain,index in [('ex','e_x'),('ey','e_y'),('ez','e_z')]:out=re.sub(r'\b'+plain+r'\b',index,out)
 if code.strip().startswith('{') and code.strip().endswith('}') and not out.startswith(r'\{'):out=r'\{'+out[1:-1]+r'\}'
 return out

def prose(s):
 parts=[]
 for token in re.split(r'(\s+)',str(s)):
  if not token or token.isspace():parts.append(token);continue
  tail=''
  while token and token[-1] in ',;:.':tail=token[-1]+tail;token=token[:-1]
  # Only formula-shaped tokens are converted inside prose; ordinary words remain text.
  m=inline_math(token) if any(ch in token for ch in '=<>^_') or token in ['alpha','alpha/16','tau','c1','c2','c1(S)','c2(S)','hbar','E_star'] else None
  parts.append((r'\('+m+r'\)' if m else tx(token))+tx(tail))
 return ''.join(parts)

def plain(node):
 if isinstance(node,dict):
  if node.get('t')=='Str':return node['c']
  if node.get('t') in ['Space','SoftBreak','LineBreak']:return ' '
  return plain(node.get('c',[]))
 if isinstance(node,list):return ''.join(plain(x) for x in node)
 return ''

ledger=[];inputs={}
for entry in sorted(findings['loops'],key=lambda x:x['sequence']):
 rid=entry['id'];lid=rid.lower();gate_path=ROOT/entry['evidence'];gate=json.loads(gate_path.read_text());source=ROOT/f'research/round29/forward/{lid}/report.md'
 for path in [gate_path,source]:inputs[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
 for name,digest in gate['bindings'].items():
  p=ROOT/name;require(p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest, (rid,name))
 source_text=source.read_text()
 # This source's projection notation resembles a Markdown link; preserve its
 # mathematical meaning in the new edition without changing the frozen report.
 source_text=source_text.replace('Q_(F,L)=1_[0,L](h_F)',r'\(Q_{F,L}=\mathbf1_{[0,L]}(h_F)\)')
 ast=json.loads(subprocess.check_output(['pandoc','-f','markdown+tex_math_single_backslash+tex_math_dollars','-t','json'],input=source_text,text=True))
 # Metadata on authorship/research isolation is described once in this manuscript.
 # Preserve the complete admitted report, including metadata paragraphs that may contain a verdict.
 n=0
 def walk(x):
  global n
  if isinstance(x,list):return [walk(y) for y in x]
  if not isinstance(x,dict):return x
  t=x.get('t');c=x.get('c')
  if t=='Header':
   level,attr,content=c;attr[0]='r29-'+lid+'-'+attr[0]
   if level==1:content=[{'t':'Str','c':'HNM '+rid+': '+entry['title'].removeprefix('HNM ')}]
   elif content and content[0].get('t')=='Str' and re.fullmatch(r'\d+\.',content[0]['c']):
    content=content[1:]
    if content and content[0].get('t')=='Space':content=content[1:]
   return {'t':t,'c':[level,attr,walk(content)]}
  if t=='Code':
   code=c[1].replace('²','^2').replace('³','^3').replace('⁴','^4');code=code.replace('c2s','c2 s').replace('c1g','c1 g');math=inline_math(code)
   if code.startswith(('https://','http://')):return {'t':'RawInline','c':['latex',r'\url{'+code+'}']}
   if code.startswith('research/'):return {'t':'RawInline','c':['latex',r'\repo{'+code+'}']}
   if math is not None:return {'t':'Math','c':[{'t':'InlineMath'},math]}
   return {'t':'Code','c':[c[0],code]}
  if t=='Str' and (any(ch in c for ch in '=<>^_') or c in ['alpha','Lambda','Omega','tau','hbar','omega','chi','rho','psi']):
   token=c;tail=''
   while token and token[-1] in ',;:.':tail=token[-1]+tail;token=token[:-1]
   math=inline_math(token)
   if math is not None:return {'t':'RawInline','c':['latex',r'\('+math+r'\)'+tx(tail)]}
  if t=='Math' and c[0]['t']=='DisplayMath':
   n+=1;math=c[1].strip();label=f'r29:{lid}:eq{n}';tag=re.search(r'\\tag\{([^}]+)\}',math)
   math=re.sub(r'(?<![A-Za-z\\])Vsel_R\b',lambda m:r'V_R^{\mathrm{sel}}',math)
   if rid=='AM2' and n==9:
    math=r"\begin{aligned}G(R)&<148/7,\qquad G'(R)<352,\\ J_0G(R)&<148/25000000<R,\\ J_0G'(R)&<77/781250,\qquad 2J_0G'(R)<77/390625<1.\end{aligned}\tag{HNM-AM2.9}"
   if not tag:math+='\n'+r'\tag{HNM-'+rid+'.U'+str(n)+'}'
   math+='\n'+r'\label{'+label+'}'
   math=re.sub(r'\n\s*\n','\n',math)
   r['equations'].append(dict(id='HNM-E-R29-'+rid+'-'+str(n).zfill(2),legacy_label=label,label_kind='equation',source='addenda/round29/'+lid+'.tex',contribution_ids=['HNM-C-'+rid],scope='Source-bound Round29 formula, subject to the admitted gate and original theorem premises.',printed_locator=previous_locators.get(label)))
   return {'t':'RawInline','c':['latex',r'\begin{equation}'+'\n'+math+'\n'+r'\end{equation}']}
  return {k:walk(v) for k,v in x.items()}
 # A runnable long command is a code block, not an unbreakable inline token.
 for i,b in enumerate(ast['blocks']):
  if b['t']=='Para' and plain(b).startswith('Reproduce:'):
   cmds=[z['c'][1] for z in b['c'] if z.get('t')=='Code']
   if cmds:
    command=cmds[0].replace(' --output ', ' \\\n  --output ')
    ast['blocks'][i]={'t':'RawBlock','c':['latex','Reproduce from the repository root:\n'+r'\begin{verbatim}'+'\n'+command+'\n'+r'\end{verbatim}']}
 ast=walk(ast)
 body=subprocess.check_output(['pandoc','-f','json','-t','latex','--wrap=none'],input=json.dumps(ast),text=True)
 body=body.replace('Henheik--Teufel--Wessel, arXiv:2106.13780v3',r'Henheik--Teufel--Wessel~\citep{henheik2022local}, arXiv:2106.13780v3')
 body=body.replace('Bauer et al., arXiv:2307.11829',r'Bauer et al.~\citep{bauer2023basis}, arXiv:2307.11829')
 body=body.replace('Yarotsky math-ph/0411042v1',r'Yarotsky~\citep{yarotsky2004quasiparticles}, math-ph/0411042v1')
 body=body.replace('Gauvin arXiv:2503.15539v3',r'Gauvin~\citep{gauvin2026}, arXiv:2503.15539v3')
 body=re.sub(r'(\\section\{[^}]+)(\})',lambda m:m[1]+r'\workstar'+m[2],body,count=1)
 body=re.sub(r'\\label\{(?!r29:)([^}]+)\}',lambda m:r'\label{r29:'+lid+':'+m[1]+'}',body)
 # Pandoc can request this macro for compact lists; supplied in the manuscript preamble.
 pre=r'\begin{quote}\small \textbf{Admission: '+tx(entry['status'].replace('_',' '))+'.} '+prose(entry['accepted'])+r'\par The typeset body below preserves the source-bound forward derivation. Its prospective language is historical; this boxed gate records the final reviewed verdict. The separately authored reverse and skeptical records remain linked. The common admission and attributed refinements are determined by the gate, not by a renamed equation.\end{quote}'+'\n'
 first=body.find('\n\n');body=body[:first+2]+pre+body[first+2:]
 body+='\n'+r'\subsection*{Final admitted limits and evidence}'+'\n'+r'\begin{itemize}'+'\n'
 for limit in entry['limitations']:body+=r'\item '+prose(limit)+'\n'
 body+=r'\end{itemize}'+'\n'+r'\repo{'+entry['evidence']+'}'+r'\par\repo{research/round29/reverse/'+lid+'/report.md}'+r'\par\repo{research/round29/skeptic/'+lid+'.md}'+'\n'
 if rid=='AQ2':
  body+='\n'+r'''\subsection*{Separately admitted reverse refinement}
The common synthesis uses the forward floor $61999/250000>1/5$. The same final gate explicitly admits the reverse derivation's sharper rational floor, under the same chosen state and coupling conditions:
\begin{equation}
\operatorname{Var}_{\omega_{\rm num}}(W)\ge\frac{3099951}{12500000}>\frac15.
\tag{HNM-AQ2.R1}\label{r29:aq2:reverse-variance}
\end{equation}
This refinement is attributed to \repo{research/round29/reverse/aq2/report.md} and its bound checks. It is not substituted into the frozen forward report and does not identify another state or establish literature priority.
'''
  r['equations'].append(dict(id='HNM-E-R29-AQ2-REV-01',legacy_label='r29:aq2:reverse-variance',label_kind='equation',source='addenda/round29/aq2.tex',contribution_ids=['HNM-C-AQ2'],scope='Separately attributed reverse refinement explicitly admitted by the AQ2 gate; same state and conditions.',printed_locator='HNM-AQ2.R1'))
 # A report's historical next-step suggestion is superseded by later gated chapters.
 body+='\n'+r'\emph{Sequencing note.} Prospective statements in this frozen derivation describe the moment of its admission. The final Round29 roadmap below governs subsequent work.'+'\n'
 (dest/(lid+'.tex')).write_text(body)
 title=entry['title'].removeprefix('HNM ')
 result_type={'AL1':'scoped obstruction or negative control','AL2':'scoped obstruction or negative control','AM1':'scoped obstruction or negative control','AM2':'scoped derivation','AN1':'application of established mathematics','AN2':'application of established mathematics','AO2':'application of established mathematics','AQ1':'application of established mathematics','AQ2':'application of established mathematics'}.get(rid,'scoped derivation')
 r['contributions'].append(dict(id='HNM-C-'+rid,legacy_id=rid,legacy_title=entry['title'],title=title,display_name='Hruday '+title[0].lower()+title[1:],classification=result_type,status=entry['status'],round=29,source_rounds=[29],equation_labels=[e['legacy_label'] for e in r['equations'] if e['contribution_ids']==['HNM-C-'+rid]],source_paths=[entry['evidence'],str(source.relative_to(ROOT)),f'research/round29/reverse/{lid}/report.md',f'research/round29/skeptic/{lid}.md'],application=entry['accepted'],limitation=' '.join(entry['limitations']),next=gate.get('decision','See current roadmap.'),priority=None,priority_status='unverified; HNM is a project alias, not a priority claim',summary=entry['accepted']))
 ledger.append(rid)
r['contribution_count']=len(r['contributions']);(OUT/'registry/hnm-registry.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
chapter=r'''\section{Round29: models, sources and the ten-investigation contract}
\label{sec:round29-overview}
The inherited Round28 roadmap selected the full physical-scale dictionary (AL), numerical homogeneous stability (AM), and a specified bulk-boundary comparison (AN). Each second investigation responds to its first skeptical review. The fourth and fifth goal pairs are selected only after those six admissions. This continuation preserves fixed positive $E_\star$ and $\hbar$, complete original interactions, the actual physical gauge completion, and the distinction between sufficient membership and an actual spectral gap. Two directions and a separate skeptic share inherited premises; their derivations and code are not independent physical observations or external human peer review.

The new literature pass records eleven selected primary sources in \repo{research/round29/experts/sources.json}. The comparison to \citet{gauvin2026} changes the novelty boundary described in Section~\ref{sec:editorial-front}. Earlier historical and unconventional source inventories remain available in the integrated addenda. No rumor, patent or institutional program is imported as a new Hamiltonian premise. The panel uses those historical methods as questions about inverse identification, full-system loading, representation, selection and actual observables.

Each following chapter carries its admitted forward derivation, common gate result, explicit limitations, and links to the separate reverse and skeptical records. An insufficient numerical radius or a failed bridge is retained as a limited completed investigation. A project label is not a missing proof step.
'''
source_data=json.loads((ROOT/'research/round29/experts/sources.json').read_text())
chapter=chapter.replace('eleven selected primary sources',str(len(source_data['sources']))+' selected primary sources')
source_lines=[r'\section{Round29 primary sources and reading boundaries}',r'This table records the selected source review used by the advisor. A screened source is not an admitted theorem transfer, and the list is not an exhaustive state-of-the-art or priority search.',r'\begingroup\footnotesize\setlength{\tabcolsep}{4pt}',r'\begin{longtable}{@{}p{46mm}p{60mm}p{46mm}@{}}',r'\toprule Primary source & Actual reading depth and use & Transfer limitation\\\midrule\endhead']
for source in source_data['sources']:
 authors=', '.join(source['authors'])
 a=r'\href{'+source['url']+'}{'+tx(source['title'])+'}'+r'\par '+tx(authors)+r'\par '+tx(source['version'])
 b=tx(source['reading_depth'])+r'\par '+tx(source['use'])
 source_lines.append(a+' & '+b+' & '+tx(source['limits'])+r'\\\addlinespace')
source_lines.extend([r'\bottomrule\end{longtable}\endgroup'])
(OUT/'sections/round29-sources.tex').write_text('\n'.join(source_lines)+'\n')
chapter+='\n'+r'\input{sections/round29-sources}'+'\n'
chapter+='\n'+r'\textbf{Current admitted count: '+str(len(ledger))+r'/10.} Publication requires the completed ten-gate source build.'+'\n'
if len(ledger)==10 and (OUT/'figures/round29-dependencies.pdf').exists():
 chapter+='\n'+r'''\begin{figure}[p]
\centering\includegraphics[width=\linewidth]{figures/round29-dependencies.pdf}
\caption{Current Round29 dependency projection. Solid arrows retain the canonical graph's scoped input relations; a dependency does not transfer every parent conclusion. Amber marks the limited AM1 outcome. External sources retain their authorship. The ten continuum scope-boundary edges are grouped on the labelled dashed rail: no branch reaches a continuum construction. The full graph retains equation nodes, earlier ancestors, future goals and source links; the companion projection record binds its exact source hash.}
\label{fig:round29-dependencies}
\par\small\repo{research/round29/network.json}\par\repo{figures/round29-dependencies.json}
\end{figure}
'''
for rid in ledger:chapter+='\n'+r'\clearpage\input{addenda/round29/'+rid.lower()+'}'+'\n'
chapter+='\n'+r'\input{sections/round29-calculator}'+'\n'
chapter+='\n'+r'\input{sections/round29-closeout}'+'\n'
(OUT/'sections/round29.tex').write_text(chapter)
close=OUT/'sections/round29-closeout.tex'
if not close.exists():close.write_text(r'\section{Current Round29 closeout}\label{sec:round29-closeout}'+'\n'+r'The final ten-gate closeout is not yet integrated. This editorial build is not a release.'+'\n')
(OUT/'round29-inputs.json').write_text(json.dumps({'admitted_loops':ledger,'sha256':inputs,'scope':'Exact gate and frozen forward-report inputs. The gate contains all producer, reverse and skeptic bindings.'},indent=2)+'\n')
print(json.dumps({'integrated_loops':ledger,'contributions':len(r['contributions']),'equations':len(r['equations'])}))
