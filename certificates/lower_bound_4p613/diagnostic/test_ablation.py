#!/usr/bin/env python3
"""Reconstruct and exactly test removal of the 19 final-stage priced orbits."""
from __future__ import annotations
import argparse,collections,copy,json,re,subprocess,sys,tempfile
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from make_exact_input import compile_record

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('executable',type=Path)
    ap.add_argument('--log',type=Path,required=True)
    args=ap.parse_args()
    original=json.loads((ROOT/'best-certificate.json').read_text())
    provenance=json.loads((ROOT/'orbit-provenance.json').read_text())
    L=F(original['outer_side'])
    atoms=collections.defaultdict(F)
    for x,y,w in original['atoms']:atoms[F(x),F(y)]+=F(w)
    expanded=collections.defaultdict(F);removed=collections.defaultdict(F)
    norbits=0;natoms=0
    for q in provenance:
        x,y,z=F(q['x']),F(q['y']),F(q['per_atom_weight'])
        orbit={(a,b) for u,v in [(x,y),(y,x)] for a in (u,L-u) for b in (v,L-v)}
        if q['size']!=len(orbit) or F(q['mass'])!=len(orbit)*z:
            raise ValueError('Orbit metadata differs from exact expansion')
        for pt in orbit:expanded[pt]+=z
        if q['index']>=444:
            norbits+=1;natoms+=len(orbit)
            for pt in orbit:removed[pt]+=z
    if dict(atoms)!=dict(expanded):raise ValueError('Orbit ledger does not reconstruct the accepted measure')
    if (norbits,natoms)!=(19,152) or sum(removed.values())!=F('0.315664656'):
        raise ValueError('Final-stage orbit family does not match the recorded experiment')
    for pt,z in removed.items():
        atoms[pt]-=z
        if atoms[pt]<0:raise ValueError('Negative ablated weight')
    record=copy.deepcopy(original)
    record['atoms']=[[str(x),str(y),str(z)] for (x,y),z in sorted(atoms.items()) if z]
    mass=sum(atoms.values());record['total_mass']=str(mass)
    if mass!=F('16.682320324'):raise ValueError('Unexpected remaining mass')
    args.log.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        inp=Path(td)/'ablation.txt';compile_record(record,inp)
        with args.log.open('w') as stream:
            run=subprocess.run([str(args.executable.resolve()),str(inp)],stdout=stream,stderr=subprocess.STDOUT)
    text=args.log.read_text();match=re.search(r'direction 0 minimum (\d+/\d+) slabs',text)
    if run.returncode!=2 or not match or F(match.group(1))!=F('0.939043209'):
        raise RuntimeError('Expected exact ablation failure was not reproduced')
    if mass/F(match.group(1))<=17:raise RuntimeError('Uniform-rescaling diagnostic is inconsistent')
    print('EXACT_FINAL_ORBIT_ABLATION_VALIDATED removed_orbits 19 removed_atoms 152')
    print('remaining_mass 16.682320324 direction_0_minimum 0.939043209')
    print('This is failure of this fixed core test after deletion, not a limit on other reoptimizations.')
if __name__=='__main__':main()
