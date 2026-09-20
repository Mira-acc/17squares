#!/usr/bin/env python3
"""Exact diagnostic witnesses; these do not replace the universal replay."""
import json,sys
from fractions import Fraction as F
from pathlib import Path
import verify
sys.path.insert(0,str(verify.ROOT/'upstream'))
from sweep import direct_mass

def run():
    c=verify.upstream_certificate();aa=verify.expand(c['orbits']);aa=[(F(x,100000),F(y,100000),F(w,1000000)) for x,y,w in aa]
    j=verify.read(verify.ROOT/'diagnostics/fixed-measure-parent-counterexample.json')
    A,t=F(j['A']),F(j['t']);xy=(F(j['x']),F(j['y']));cp,sp=verify.trig(t);r=A*(cp+sp)/2
    verify.need(all(r<=z<=verify.L-r for z in xy),'counterexample center not parent-feasible')
    mass,ids=direct_mass(aa,A,t,xy)
    verify.need(mass==F(j['mass_units'],1000000) and ids==j['indices'],'parent recount mismatch')
    verify.need(17*mass<F(c['mass_units'],c['weight_denominator']),'no fixed-measure obstruction')
    result={'status':'PASS_EXACT_PARENT_COUNTEREXAMPLE','parent_side':str(A),'scaled_target':str(verify.L/A),
      'parent_half_angle':str(t),'closed_parent_mass':str(mass),'measure_mass':str(F(c['mass_units'],c['weight_denominator'])),
      'scope':'Fixed R012 measure and its uniform rescalings only; no restriction on other measures, placements or global lower bounds.'}
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':run()
