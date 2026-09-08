#!/usr/bin/env python3
"""Exploratory interior-point choice inside a finite feasible mass-budget slice."""
from adaptive_search import *
from scipy.optimize._highspy._core import _Highs,HighsStatus,HighsModelStatus
ap=argparse.ArgumentParser();ap.add_argument('prefix');ap.add_argument('output');ap.add_argument('--budget',type=float,default=16.998);a=ap.parse_args()
m=json.loads(Path(a.prefix+'.json').read_text());r=np.load(a.prefix+'.npz');sites=[tuple(map(F,p)) for p in m['sites']];p=Problem(float(m['L']),float(m['B']),sites);A=r['A'];poses=r['poses'];w=r['w'];target=1.000002
h=_Highs()
for k,v in [('output_flag',False),('threads',1),('solver','ipm'),('presolve','off'),('run_crossover','off'),('ipm_optimality_tolerance',1e-9)]:
 st=h.setOptionValue(k,v)
 if st!=HighsStatus.kOk:raise RuntimeError('Unsupported option '+k)
n=p.nv;h.addCols(n,np.zeros(n),np.zeros(n),np.full(n,np.inf),0,np.zeros(n+1,np.int32),np.array([],np.int32),np.array([],float))
# Rows near the current face initialize a finite working set; restore all violations.
active=set(np.where(A@w<1.00002)[0].tolist())
for it in range(10):
 ix=np.array(sorted(active));aa=csr_matrix(A[ix],dtype=float)
 if it==0:
  h.addRows(len(ix),np.full(len(ix),target),np.full(len(ix),np.inf),aa.nnz,aa.indptr.astype(np.int32),aa.indices.astype(np.int32),aa.data)
  h.addRows(1,np.array([-np.inf]),np.array([a.budget]),n,np.array([0,n],np.int32),np.arange(n,dtype=np.int32),p.sz)
 else:
  add=csr_matrix(A[new],dtype=float);h.addRows(len(new),np.full(len(new),target),np.full(len(new),np.inf),add.nnz,add.indptr.astype(np.int32),add.indices.astype(np.int32),add.data)
 t=time.time();h.run();status=h.getModelStatus();print('IPM',it,h.modelStatusToString(status),'seconds',time.time()-t,flush=True)
 if status!=HighsModelStatus.kOptimal:raise RuntimeError('No finite central feasible point')
 w=np.array(h.getSolution().col_value);v=A@w;bad=np.where(v<target-2e-8)[0];print('mass',p.sz@w,'pool_min',v.min(),'bad',len(bad),flush=True)
 if not len(bad):break
 new=bad[np.argsort(v[bad])[:2000]];active.update(new.tolist())
else:raise RuntimeError('IPM row restoration failed')
mins,rr,ps=p.sweep(w,2880,1.0000001,24);print('FULL_SWEEP_MIN',mins.min(),'mass',p.sz@w,'newrows',len(rr),flush=True)
np.savez_compressed(a.output+'.npz',w=w,A=np.r_[A,rr],poses=np.r_[poses,ps],steps=2880,L=p.L,B=p.B,mins=mins);Path(a.output+'.json').write_text(json.dumps(m)+'\n')
