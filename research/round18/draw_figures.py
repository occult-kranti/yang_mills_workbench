"""Standalone scientific plots from accepted site data and original CSV hashes."""
from pathlib import Path
import hashlib,json,shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent;DIST=HERE.parents[1]/'dist'
def main():
 data=json.loads((HERE/'site-data.json').read_bytes());out=HERE/'figures';out.mkdir(exist_ok=True)
 if data.get('status')!='accepted' or data.get('loops_completed')!=6:raise ValueError('Complete accepted data required')
 for name,sha in data['csv_sha256'].items():
  if hashlib.sha256((DIST/name).read_bytes()).hexdigest()!=sha:raise ValueError('Changed plotted CSV '+name)
 records={}
 for key,p in data['plots'].items():
  fig,ax=plt.subplots(figsize=(8.2,4.7),layout='constrained')
  for s in p['series']:
   x,y=zip(*s['points']);ax.plot(x,y,marker='o',markersize=4,label=s['name'],linewidth=1.6)
  ax.set(title=p['title'],xlabel=p['xLabel'],ylabel=p['yLabel']);ax.grid(alpha=.22);ax.legend(fontsize=8)
  fig.savefig(out/(key+'.png'),dpi=160);fig.savefig(out/(key+'.svg'));plt.close(fig)
  records[key]={'csv':p['csv'],'caption':p['caption'],'png_sha256':hashlib.sha256((out/(key+'.png')).read_bytes()).hexdigest()}
 shutil.copy2(DIST/'next-collaboration.svg',out/'collaboration.svg')
 (HERE/'figure-records.json').write_text(json.dumps({'status':'generated','plots':records,'scope':'Exact accepted data converted to floating coordinates for plotting; visual review recorded separately.'},indent=2)+'\n')
if __name__=='__main__':main()
