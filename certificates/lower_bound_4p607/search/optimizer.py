"""Exploratory only: LP weights and floating-point separation, no proof claims."""
from fractions import Fraction as F
from pathlib import Path
import ctypes, numpy as np, json, time, sys, os
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack
ROOT=Path(__file__).resolve().parent
f=ctypes.CDLL(str(ROOT/'numeric_sweep.so')).sweep
ptr=np.ctypeslib.ndpointer
f.argtypes=[ctypes.c_int,ptr(np.float64,flags='C_CONTIGUOUS'),ptr(np.float64,flags='C_CONTIGUOUS'),ptr(np.float64,flags='C_CONTIGUOUS'),ctypes.c_int,ptr(np.int32,flags='C_CONTIGUOUS'),ctypes.c_double,ctypes.c_double,ctypes.c_int,ptr(np.float64,flags='C_CONTIGUOUS'),ptr(np.uint8,flags='C_CONTIGUOUS'),ctypes.c_int,ctypes.c_int]
f.restype=ctypes.c_int
lines=Path(os.environ.get('ORBIT_FILE',str(ROOT/'orbits.txt'))).read_text().splitlines();L0=F('4.59');xs=[];ys=[];ids=[];weights=[];sz=[]
for j,line in enumerate(lines):
 x,y,w=map(F,line.split()); orb=sorted({(a,b) for x0,y0 in [(x,y),(y,x)] for a in [x0,L0-x0] for b in [y0,L0-y0]})
 for x,y in orb:xs.append(float(x-L0/2));ys.append(float(y-L0/2));ids.append(j)
 weights.append(float(w));sz.append(len(orb))
X0=np.array(xs);Y0=np.array(ys);ids=np.array(ids,np.int32);w0=np.array(weights);sz=np.array(sz);nv=len(sz)
def oracle(L=4.59,B=.9977,w=w0,steps=180,perdir=16,scale=True):
 X=np.ascontiguousarray(X0*(L/4.59 if scale else 1));Y=np.ascontiguousarray(Y0*(L/4.59 if scale else 1));W=np.ascontiguousarray(w[ids]);mins=np.zeros(steps+1);rows=np.zeros((min((steps+1)*perdir,50000),nv),np.uint8)
 n=f(len(X),X,Y,W,nv,ids,L,B,steps,mins,rows,len(rows),perdir)
 return mins,rows[:n]
if __name__=='__main__':
 mode=sys.argv[1] if len(sys.argv)>1 else 'check'
 if mode=='check':
  for L,B,steps in [(4.59,.9977,180),(4.59,.999,720),(4.591,.9994,720),(4.592,.9994,720),(4.595,.9994,720),(4.6,.9994,720)]:
   tm=time.time();m,r=oracle(L,B,steps=steps);print(L,B,steps,'min',m.min(),'angle-index',m.argmin(),'violations',len(r),'seconds',time.time()-tm,flush=True)
 else:
  L=float(sys.argv[2]);steps=int(sys.argv[3]) if len(sys.argv)>3 else 360;B=float(sys.argv[4]) if len(sys.argv)>4 else .99884
  w=(np.load(os.environ['WARM'])['w'].copy() if 'WARM' in os.environ else w0.copy());A=csr_matrix((0,nv));seen=set()
  for it in range(30):
   tm=time.time();m,r=oracle(L,B,w,steps,int(os.environ.get('PERDIR','16')))
   new=[]
   for row in r:
    key=row.tobytes()
    if key not in seen:seen.add(key);new.append(row)
   print(it,'L',L,'B',B,'mass',sz@w,'min',m.min(),'new',len(new),'totalrows',len(seen),'secs',time.time()-tm,flush=True)
   np.savez(ROOT/f'candidate_{L}_{steps}.npz',L=L,B=B,steps=steps,w=w,mins=m);
   from scipy.sparse import save_npz
   save_npz(ROOT/f'constraints_{L}_{steps}.npz',A)
   if m.min()>=1-1e-8:break
   if not new:break
   if it>0 and sz@w>17.01:print('FINITE_LP_EXCEEDS_17_NUMERICAL_ONLY',flush=True);break
   A=vstack([A,csr_matrix(np.array(new))],format='csr')
   res=linprog(sz,A_ub=-A,b_ub=-np.ones(A.shape[0])*(1+1e-6),bounds=(0,None),method='highs')
   if not res.success:print(res.message);break
   w=res.x
