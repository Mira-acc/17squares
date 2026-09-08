#!/usr/bin/env python3
"""Export a numerical iterate as untrusted rational certificate data.
Run the separate exact checker before making any theorem claim.
"""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction as F
import argparse,json,math,hashlib
import numpy as np

def export(prefix:Path,out:Path,denominator:int=10**9):
 meta=json.loads(prefix.with_suffix(prefix.suffix+'.json').read_text())
 p=np.load(str(prefix)+'.npz');L=F(meta['L']);B=F(meta['B']);steps=int(p['steps']);weights=p['w'];sites=[tuple(map(F,q)) for q in meta['sites']]
 if len(weights)!=len(sites):raise ValueError('Mismatched iterate and dictionary')
 atoms={};orbits=[]
 for j,((x,y),w) in enumerate(zip(sites,weights)):
  if not math.isfinite(float(w)):raise ValueError('Non-finite weight')
  z=F(math.ceil(max(0.,float(w))*denominator),denominator)
  if not z:continue
  orb=sorted({(a,b) for u,v in [(x,y),(y,x)] for a in [u,L-u] for b in [v,L-v]})
  for a,b in orb:atoms[a,b]=atoms.get((a,b),F(0))+z
  orbits.append({'index':j,'x':str(x),'y':str(y),'per_atom_weight':str(z),'size':len(orb),'mass':str(len(orb)*z)})
 total=sum(atoms.values());rec={'id':'Mira-17-squares-spatial-pricing-'+str(L),'n':17,'claim':'candidate only; exact replay required','outer_side':str(L),'square_side':str(B),'angle_limit':'207107/500000','direction_steps':steps,'total_mass':str(total),'symmetry':'D4','atoms':[[str(x),str(y),str(w)] for (x,y),w in sorted(atoms.items())],'provenance':{'parent_certificate':'Mira-Cult/17squares lower_bound_4p607, s(17)>4.607028598640','upstream':'Joshua Levy T-019 rational support and fractional weighted-cover method, CC BY 4.0 data','search_method':'Alternating separating core placements and LP-dual-priced new D4 support orbits; finite constraint pool retained','weight_rounding':'Upward to denominator '+str(denominator),'geometric_verifier':'Unchanged arbitrary-integer exact_sweep.cpp from 4p607; no optimization trusted','review_status':'Not externally peer reviewed'}}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(rec,indent=1)+'\n');out.with_name(out.stem+'-orbits.json').write_text(json.dumps(orbits,indent=1)+'\n');print('RATIONAL_CANDIDATE','L',L,'B',B,'steps',steps,'orbits',len(orbits),'atoms',len(atoms),'mass',total,'decimal',float(total),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('prefix',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args();export(args.prefix,args.output)
