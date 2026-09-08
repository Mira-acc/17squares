#!/usr/bin/env python3
"""Spend mass slack on positive repairs, never removing existing atom weights.
Exploratory numerical procedure; resulting rationals require exact replay.
"""
from adaptive_search import *
parser=argparse.ArgumentParser();parser.add_argument('prefix');parser.add_argument('output');parser.add_argument('--steps',type=int,default=2880);parser.add_argument('--iterations',type=int,default=15);args=parser.parse_args()
r=np.load(args.prefix+'.npz');meta=json.loads(Path(args.prefix+'.json').read_text());sites=[tuple(map(F,p)) for p in meta['sites']];problem=Problem(float(meta['L']),float(meta['B']),sites);w=r['w'].copy();target=1.000002
poses=r['poses'].copy();A=r['A'].copy();initial_mass=problem.sz@w
for it in range(args.iterations):
 tm=time.time();mins,rows,pp=problem.sweep(w,args.steps,1.0000001,24);mass=problem.sz@w
 print('REPAIR_SWEEP',it,'mass',mass,'min',mins.min(),'rows',len(rows),'sec',time.time()-tm,flush=True)
 if mins.min()>0 and mass*target/mins.min()<16.9998:
  w*=target/mins.min();np.savez_compressed(args.output+'.npz',w=w,L=problem.L,B=problem.B,steps=args.steps,poses=poses,A=A,mins=mins);meta['monotone_repair']={'initial_mass':initial_mass,'final_mass':problem.sz@w,'iterations':it};Path(args.output+'.json').write_text(json.dumps(meta)+'\n');print('NUMERICAL_CANDIDATE_READY',problem.sz@w,flush=True);break
 if not len(rows):raise RuntimeError('No separating poses')
 rows,ix=np.unique(rows,axis=0,return_index=True);pp=pp[ix];rhs=target-rows@w;bad=rhs>0;rows=rows[bad];pp=pp[bad];rhs=rhs[bad]
 res=linprog(problem.sz,A_ub=-csr_matrix(rows,dtype=float),b_ub=-rhs,bounds=(0,None),method='highs')
 if not res.success:raise RuntimeError(res.message)
 cost=problem.sz@res.x;print('POSITIVE_REPAIR_COST',cost,'resulting_mass',mass+cost,flush=True)
 if mass+cost>=16.9998:print('REPAIR_EXCEEDS_BUDGET_NUMERICAL_ONLY',flush=True);break
 w+=np.maximum(res.x,0);A=np.r_[A,rows];poses=np.r_[poses,pp]
else:print('REPAIR_ITERATION_LIMIT',flush=True)
