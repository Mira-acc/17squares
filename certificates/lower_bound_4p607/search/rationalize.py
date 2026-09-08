"""Round exploratory orbit weights upward; the resulting file still needs exact replay."""
import json,math,sys,hashlib,os
from fractions import Fraction as F
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent

def rationalize(npz, out, denominator=10**8):
    p=np.load(npz);L=F(str(float(p['L'])));B=F(str(float(p['B'])));steps=int(p['steps']);weights=p['w']
    source=json.loads((ROOT/'jlevy-certificate.json').read_text());L0=F(source['outer_side']);q=L/L0;atoms=[]
    for w,line in zip(weights,Path(os.environ.get('ORBIT_FILE',str(ROOT/'orbits.txt'))).read_text().splitlines()):
        x,y,_=map(F,line.split());wi=F(math.ceil(max(0.0,float(w))*denominator),denominator)
        if not wi:continue
        orbit=sorted({(a,b) for x0,y0 in [(x,y),(y,x)] for a in [x0,L0-x0] for b in [y0,L0-y0]})
        atoms.extend([[str(q*a),str(q*b),str(wi)] for a,b in orbit])
    rec={'id':'Mira-17-squares-'+str(L),'n':17,'claim':'s(17) > '+str(L),'outer_side':str(L),'square_side':str(B),'angle_limit':'207107/500000','direction_steps':steps,'total_mass':str(sum(F(w) for x,y,w in atoms)),'symmetry':'D4','atoms':atoms,'provenance':{'source':'Joshua Levy, the squares project (https://github.com/jlevy/squares)','source_git_blob_sha1':'f454e44dee1f2318af45e02efdfff5fcd7dbfbe1','coordinate_change':'Uniform dilation by '+str(q),'weight_change':'LP reoptimization on source D4 orbits; upward rounding to denominator '+str(denominator),'source_data_license':'CC BY 4.0','verification_status':'Requires independent exact replay; declarations are not proof'}}
    Path(out).write_text(json.dumps(rec,indent=1)+'\n');print('atoms',len(atoms),'total',rec['total_mass'],float(F(rec['total_mass'])))
if __name__=='__main__':rationalize(sys.argv[1],sys.argv[2])
