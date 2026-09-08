#!/usr/bin/env python3
"""Find an exact finite LP-dual obstruction for a restricted support dictionary.
The candidate dual uses floating point; verify_obstruction() uses integers/Fractions only.
This is NOT a packing obstruction: it diagnoses a particular weighted-core dictionary.
"""
from __future__ import annotations
import json,sys,math
from fractions import Fraction as F
from pathlib import Path

def orbit(x,y,L):return sorted({(a,b) for u,v in [(x,y),(y,x)] for a in [u,L-u] for b in [v,L-v]})
def matrix(record):
 if not __debug__:raise RuntimeError("Run this checker without Python optimization flags")
 L=F(record['L']);B=F(record['B']);sites=[tuple(map(F,p)) for p in record['sites']];orbits=[orbit(x,y,L) for x,y in sites];assert L>0 and B>0 and all(0<=x<=L and 0<=y<=L for x,y in sites);sz=[len(p) for p in orbits]
 G=math.lcm((L/2).denominator,(B/2).denominator,*(c.denominator for orb in orbits for pt in orb for c in pt))
 atoms=[(int((x-L/2)*G),int((y-L/2)*G),j) for j,orb in enumerate(orbits) for x,y in orb]
 rows=[]
 for ps in record['poses']:
  x,y=F(ps['x']),F(ps['y']);p,q=int(ps['p']),int(ps['q']);C=q*q-p*p;S=2*p*q;R=q*q+p*p
  assert C>0 and S>=0
  GG=math.lcm(G,x.denominator,y.denominator);sc=GG//G;xc=int(x*GG);yc=int(y*GG);li=int(L*GG/2);bi=int(B*GG/2)
  assert min(li-abs(xc),li-abs(yc))*R>=bi*(C+S),'Pose outside core domain'
  row=[0]*len(sites)
  for X,Y,j in atoms:
   dx=X*sc-xc;dy=Y*sc-yc
   if abs(C*dx+S*dy)<=bi*R and abs(-S*dx+C*dy)<=bi*R:row[j]+=1
  rows.append(row)
 return rows,sz

def verify_obstruction(record):
 A,sz=matrix(record);z=[F(p['dual']) for p in record['poses']];assert all(t>=0 for t in z)
 for j,s in enumerate(sz):assert sum(z[k]*row[j] for k,row in enumerate(A))<=s
 total=sum(z);assert total>17
 print('EXACT_RESTRICTED_DICTIONARY_OBSTRUCTION_VALID','orbits',len(sz),'poses',len(z),'dual_sum',str(total),'exceeds_17_by',str(total-17),flush=True)
 return total

def discover(prefix,out):
 import numpy as np
 from scipy.optimize import linprog
 from scipy.sparse import csr_matrix
 r=np.load(prefix+'.npz');meta=json.loads(Path(prefix+'.json').read_text());A=r['A'];w=r['w'];poses=r['poses'];L=F(meta['L']);sz=np.array([len(orbit(F(x),F(y),L)) for x,y in meta['sites']],float)
 ix=np.where(A@w<1.000004)[0];res=linprog(sz,A_ub=-csr_matrix(A[ix],dtype=float),b_ub=-np.ones(len(ix)),bounds=(0,None),method='highs');assert res.success
 di=np.where(-res.ineqlin.marginals>1e-8)[0];dual=-res.ineqlin.marginals[di];poses=poses[ix[di]];steps=int(r['steps']);rec={'kind':'restricted-D4-core-dictionary-obstruction','L':meta['L'],'B':meta['B'],'sites':meta['sites'],'poses':[]}
 for po,z in zip(poses,dual):
  x,y,c,s=po;k=round(s/(1+c)*steps/(207107/500000));t=F(207107*k,500000*steps)
  rec['poses'].append({'x':str(F(str(x))),'y':str(F(str(y))),'p':t.numerator,'q':t.denominator,'dual':str(F(math.floor(z*10**12),10**12))})
 exact,sz=matrix(rec);z=[F(p['dual']) for p in rec['poses']];maxload=max(sum(z[k]*row[j] for k,row in enumerate(exact))/s for j,s in enumerate(sz));factor=max(F(1),maxload)
 for p in rec['poses']:p['dual']=str(F(p['dual'])/factor)
 total=verify_obstruction(rec);rec['dual_sum']=str(total);rec['scope']='No D4-symmetric nonnegative weights on these sites can cover even these contained closed B-cores with total mass at most 17. This is not a ceiling on other supports or verification arguments.'
 Path(out).write_text(json.dumps(rec,indent=1)+'\n');print('dual decimal (report only)',float(total))
if __name__=='__main__':
 if sys.argv[1]=='verify':verify_obstruction(json.loads(Path(sys.argv[2]).read_text()))
 else:discover(sys.argv[1],sys.argv[2])
