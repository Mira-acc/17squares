#!/usr/bin/env python3
"""Make a rational D4 dictionary combining scaled, wall-anchored and legacy sites.

Coordinates in the dictionary are normalized to an outer side of 4.59, since
optimizer.py subsequently multiplies all coordinates by target_side/4.59.
No geometric statement is asserted about this unweighted dictionary.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MIRA_POINTS=[
 ('0.967095','0.988674'),('1.584591','0.989280'),('2.477806','0.929750'),('3.452882','0.920541'),
 ('0.998081','1.794317'),('1.992852','1.799448'),('2.973306','1.794450'),('3.522479','1.795033'),
 ('0.925919','2.658468'),('1.494140','2.660211'),('2.483891','2.663100'),('3.452714','2.667020'),
 ('0.998038','3.524908'),('1.963307','3.513845'),('2.850741','3.459296'),('3.456188','3.456188')]
STRIP_COORDINATES=['.8','.9','.95','.98','.99','.9996','1.4','1.5','1.6','1.7','1.8','1.9','1.98','1.9992','2.1','2.2']

def build(side:F)->list[str]:
 if not F('4.5')<=side<=F('4.7'):raise ValueError('This experiment supports target sides in [4.5,4.7].')
 L0=F('4.59');Lm=F('4.450837');base=(ROOT/'orbits.txt').read_text().splitlines()
 if len(base)!=157:raise ValueError('Expected the 157 original Levy orbits.')
 anchored=[]
 for row in base:
  x,y,_=map(F,row.split());x=min(x,L0-x);y=min(y,L0-y)
  anchored.append(f'{x*L0/side} {y*L0/side} 0')
 vals=list(map(F,STRIP_COORDINATES))
 repairs=[(F('.9996'),y) for y in vals]+[(F('1.9992'),y) for y in vals if y>=F('1.4')]
 repairs += [(F('.9996'),F('.9996')),(F('1.9992'),F('1.9992'))]
 anchored += [f'{x*L0/side} {y*L0/side} 0' for x,y in repairs]
 legacy=[f'{F(x)*L0/Lm} {F(y)*L0/Lm} 0' for x,y in MIRA_POINTS]
 result=base+anchored+legacy
 assert len(result)==358
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('side');p.add_argument('output',type=Path);args=p.parse_args()
 args.output.write_text('\n'.join(build(F(args.side)))+'\n')
 print('358 D4 orbit variables: 157 scaled + 157 wall anchored + 28 strip + 16 legacy.')
