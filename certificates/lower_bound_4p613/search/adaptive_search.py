#!/usr/bin/env python3
"""Exploratory row-and-column generation. All geometry here is floating point.
The output is only a candidate until independently rationalized and replayed.
"""
from __future__ import annotations
import os,sys,time,json,ctypes,argparse
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
ROOT=Path(__file__).resolve().parent
lib=ctypes.CDLL(str(ROOT/'discovery.so'))
d=ctypes.c_double;i=ctypes.c_int
P=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS');U=np.ctypeslib.ndpointer(dtype=np.uint8,flags='C_CONTIGUOUS');I=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS')
lib.pose_sweep.argtypes=[i,P,P,P,i,I,d,d,i,d,i,P,U,P];lib.pose_sweep.restype=i
lib.incidence.argtypes=[i,P,i,P,P,i,I,d,U]
lib.price_lines.argtypes=[i,P,P,d,d,i,P,P]
class Problem:
 def __init__(self,L,B,sites):self.L=L;self.B=B;self.sites=sites;self.expand()
 def expand(self):
  X=[];Y=[];ids=[];sz=[]
  L=F(str(self.L))
  for j,(x,y) in enumerate(self.sites):
   orb=sorted({(a,b) for u,v in [(x,y),(y,x)] for a in [u,L-u] for b in [v,L-v]})
   for a,b in orb:X.append(float(a-L/2));Y.append(float(b-L/2));ids.append(j)
   sz.append(len(orb))
  self.X=np.array(X);self.Y=np.array(Y);self.ids=np.array(ids,np.int32);self.sz=np.array(sz,dtype=float);self.nv=len(sz)
 def sweep(self,w,steps,threshold=1.,perdir=12):
  mins=np.zeros(steps+1);rows=np.zeros(((steps+1)*perdir,self.nv),np.uint8);poses=np.zeros(((steps+1)*perdir,4))
  n=lib.pose_sweep(len(self.X),self.X,self.Y,np.ascontiguousarray(w[self.ids]),self.nv,self.ids,self.L,self.B,steps,threshold,perdir,mins,rows,poses)
  return mins,rows[:n],poses[:n]
 def incidence(self,poses):
  out=np.zeros((len(poses),self.nv),np.uint8)
  if len(poses):lib.incidence(len(poses),np.ascontiguousarray(poses),len(self.X),self.X,self.Y,self.nv,self.ids,self.B,out)
  return out
 def price(self,poses,dual,iteration):
  rng=np.random.default_rng(79001+iteration)
  ys=np.r_[np.linspace(.5,self.L/2,700),rng.uniform(.5,self.L/2,300),[float(y) for x,y in self.sites],[float(x) for x,y in self.sites]]
  ys=np.unique(np.clip(ys,.00001,self.L/2-.000001));out=np.zeros((len(ys),3));lib.price_lines(len(poses),np.ascontiguousarray(poses),np.ascontiguousarray(dual),self.L,self.B,len(ys),ys,out)
  # Local line refinements to resolve thin high-value arrangement cells.
  for eps in [.003,.0003,.00003]:
   ys=np.unique(np.clip((out[np.argsort(-out[:,0])[:30],2,None]+np.linspace(-eps,eps,15)).ravel(),.00001,self.L/2-.000001));more=np.zeros((len(ys),3));lib.price_lines(len(poses),np.ascontiguousarray(poses),np.ascontiguousarray(dual),self.L,self.B,len(ys),ys,more);out=np.r_[out,more]
  return out[np.argsort(-out[:,0])]
def load_initial(L):
 from build_dictionary import build
 lines=build(F(str(L)));sites=[];L0=F('4.59');rat=F(str(L))/L0;weights=np.load(ROOT/'candidate_best.npz')['w'];w=[];seen={}
 for line,ww in zip(lines,weights):
  x,y,_=map(F,line.split());x*=rat;y*=rat;side=F(str(L));x=min(x,side-x);y=min(y,side-y);pair=tuple(sorted((x,y)))
  if pair in seen:w[seen[pair]]+=ww
  else:seen[pair]=len(sites);sites.append(pair);w.append(ww)
 return sites,np.array(w)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('L',type=float);ap.add_argument('--B',type=float,default=.99985);ap.add_argument('--steps',type=int,default=720);ap.add_argument('--final-steps',type=int,default=2880);ap.add_argument('--iterations',type=int,default=45);ap.add_argument('--name',default='adaptive');ap.add_argument('--resume');ap.add_argument('--no-columns',action='store_true');ap.add_argument('--seed');args=ap.parse_args();L=args.L;B=args.B;prefix=ROOT/(args.name+'-'+str(L));target=1.000002
 if args.resume:
  r=np.load(args.resume+'.npz');meta=json.loads(Path(args.resume+'.json').read_text());
  if F(meta['L'])!=F(str(L)) or F(meta['B'])!=F(str(B)):raise ValueError('--resume requires the saved L and B; use --seed to change geometry')
  sites=[tuple(map(F,p)) for p in meta['sites']];w=r['w'].copy();poses=r['poses'].copy();A=r['A'].copy();step=int(r['steps'])
 else:
  if args.seed:
   r=np.load(args.seed+'.npz');meta=json.loads(Path(args.seed+'.json').read_text());oldL=F(meta['L']);newL=F(str(L));sites=[];w=[];seen={}
   for pair,ww in zip(meta['sites'],r['w']):
    if ww<1e-10:continue
    x,y=map(F,pair)
    for a,b,z in [(x*newL/oldL,y*newL/oldL,ww),(x,y,0.)]:
     a=min(a,newL-a);b=min(b,newL-b);p=tuple(sorted((a,b)))
     if p in seen:w[seen[p]]+=z
     else:seen[p]=len(sites);sites.append(p);w.append(z)
   w=np.array(w)
  else:sites,w=load_initial(L)
  poses=np.zeros((0,4));A=np.zeros((0,len(sites)),np.uint8);step=args.steps
 problem=Problem(L,B,sites);active=set();seen={row.tobytes() for row in A};columns_rounds=0
 def save(it,mins):
  np.savez_compressed(str(prefix)+'.npz',w=w,poses=poses,A=A,L=L,B=B,steps=step,mins=mins)
  Path(str(prefix)+'.json').write_text(json.dumps({'L':str(L),'B':str(B),'sites':[[str(x),str(y)] for x,y in problem.sites],'iteration':it,'column_rounds':columns_rounds})+'\n')
 for it in range(args.iterations):
  tm=time.time();mins,rows,newposes=problem.sweep(w,step,threshold=(1.08 if not len(A) else 1.0000001),perdir=16)
  mass=problem.sz@w;mini=mins.min();print('SWEEP',it,'L',L,'steps',step,'vars',problem.nv,'atoms',len(problem.X),'mass',mass,'minimum',mini,'newposes',len(rows),'sec',time.time()-tm,flush=True)
  # A stronger net is required before any success is even provisional.
  if mini>0 and mass*target/mini<16.9997:
   w*=target/mini
   if step<args.final_steps:step=args.final_steps;print('PROMOTE_TO_FULL_NET',step,flush=True);continue
   save(it,mins);print('NUMERICAL_CANDIDATE_READY',mass*target/mini,flush=True);return
  add=[]
  for j,row in enumerate(rows):
   key=row.tobytes()
   if key not in seen:seen.add(key);add.append(j)
  if add:A=np.r_[A,rows[add]];poses=np.r_[poses,newposes[add]]
  if not len(A):raise RuntimeError('No pose constraints')
  # Check actual returned poses encode the same rows; this is a discovery check.
  if it==0 and len(add):
   chk=problem.incidence(newposes[add]);assert np.array_equal(chk,rows[add]),'pose incidence discrepancy'
  obj=problem.sz*(1+1e-5*np.random.default_rng(17).uniform(size=problem.nv))
  dual=None
  for inner in range(100):
   slack=A@w-target;bad=np.where(slack < -1e-8)[0]
   if len(bad):active.update(bad[np.argsort(slack[bad])[:1200]].tolist())
   if not active:active=set(np.argsort(slack)[:min(1200,len(slack))].tolist())
   ix=np.array(sorted(active));res=linprog(obj,A_ub=-csr_matrix(A[ix],dtype=float),b_ub=-np.full(len(ix),target),bounds=(0,None),method='highs')
   if not res.success:raise RuntimeError(res.message)
   w=res.x;slack=A@w-target;bad=np.where(slack< -2e-8)[0]
   if not len(bad):
    di=np.where(-res.ineqlin.marginals>1e-8)[0];dualposes=poses[ix[di]];dual=-res.ineqlin.marginals[di];active=set(ix[di].tolist());active.update(np.argsort(slack)[:min(1000,len(slack))]);break
  else:raise RuntimeError('LP working-set failed')
  print('LP','pool',len(A),'active',len(active),'inner',inner,'mass',problem.sz@w,'dual',len(dual),flush=True)
  # Spatial pricing is useful once the restricted LP is close to the budget.
  if not args.no_columns and it>=2 and problem.sz@w>16.995 and columns_rounds<16:
   tm=time.time();priced=problem.price(dualposes,dual,it);existing=set(problem.sites);newsites=[];column_profiles=set()
   for score,x,y in priced:
    if score<1.002 or len(newsites)>=16:break
    # Rational rounding is discovery only; final output is verified afresh.
    pair=tuple(sorted((F(str(round(float(x),8))),F(str(round(float(y),8))))))
    if pair in existing:continue
    tester=Problem(L,B,[pair]);profile=(tester.incidence(dualposes)[:,0]*(8//int(tester.sz[0]))).tobytes()
    if profile in column_profiles:continue
    if any(np.hypot(float(pair[0]-a),float(pair[1]-b))<.007 for a,b in newsites):continue
    newsites.append(pair);existing.add(pair);column_profiles.add(profile)
   print('PRICING','maximum',priced[0].tolist(),'added',len(newsites),'sec',time.time()-tm,flush=True)
   if newsites:
    newproblem=Problem(L,B,newsites);cols=newproblem.incidence(poses);A=np.c_[A,cols];problem.sites.extend(newsites);problem.expand();w=np.r_[w,np.zeros(len(newsites))];seen={row.tobytes() for row in A};columns_rounds+=1
  if it%3==0 or problem.sz@w>16.99:save(it,mins)
  if args.no_columns and problem.sz@w>17.002:print('RESTRICTED_DICTIONARY_OVER_BUDGET',flush=True);return
 save(it,mins);print('ITERATION_LIMIT',flush=True)
if __name__=='__main__':main()
