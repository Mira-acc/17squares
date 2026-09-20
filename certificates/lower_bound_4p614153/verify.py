#!/usr/bin/env python3
"""Exact parent-aware lower-bound replay. No optimizer or network is used.

Default: hash-check, compile and replay certificate.json. --upstream additionally replays
all R012 envelopes. --direct repeats both with a different accumulator sharing
the same geometric partition. Outputs are written only into a new directory.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
import gzip
import base64
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
L=F(4613,1000)
ATOM_DIGEST='ae469399ced8580ddddcef6edc234cf9becd7e94df7752aa8b4f9cefcbaf3643'

def need(ok,message):
    if not ok: raise ValueError(message)

def read(path):
    path=Path(path)
    def pairs(items):
        d={}
        for k,v in items:
            need(k not in d,'duplicate JSON key');d[k]=v
        return d
    def bad(value): raise ValueError('nonfinite JSON constant')
    if path.name.endswith('.gz.b64'):
        if path.exists():
            encoded=path.read_text().strip()
        else:
            parts=sorted(path.parent.glob(path.name+'.part*'))
            need(parts,'certificate transport and split parts both missing')
            encoded=''.join(part.read_text() for part in parts)
        encoded=''.join(encoded.split())
        packed=base64.b64decode(encoded, validate=True)
        data=gzip.decompress(packed)
        if path.name == 'certificate.json.gz.b64':
            need(hashlib.sha256(data).hexdigest()=='5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3','decompressed certificate SHA-256 mismatch')
        text=data.decode('utf-8')
    else:
        data=path.read_bytes()
        if path.name == 'certificate.json':
            need(hashlib.sha256(data).hexdigest()=='5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3','certificate SHA-256 mismatch')
        text=data.decode('utf-8')
    return json.loads(text,object_pairs_hook=pairs,parse_constant=bad)

def frac(value):
    need(type(value) is str,'rational strings required')
    return F(value)

def trig(t):
    need(isinstance(t,F) and 0<=t<1,'invalid half-angle')
    return (1-t*t)/(1+t*t),2*t/(1+t*t)

def expand(rows):
    need(type(rows) is list and 0<len(rows)<100000,'invalid orbit list')
    d={}
    for row in rows:
        need(type(row) is list and len(row)==3 and all(type(v) is int for v in row),'integer orbit row required')
        x,y,w=row
        need(0<=x<=461300 and 0<=y<=461300 and 0<=w<=10**12,'invalid orbit coordinates or weight')
        images={(a,b) for u,v in ((x,y),(y,x)) for a in (u,461300-u) for b in (v,461300-v)}
        need(not images.intersection(d),'overlapping orbit rows')
        d.update({xy:w for xy in images})
    aa=[(x,y,w) for (x,y),w in sorted(d.items())]
    need(sum(w for x,y,w in aa)<=10**12,'weight accumulator budget')
    return aa

def validate(c):
    need(frac(c['L'])==L,'kernel is bound to L=4.613')
    A=frac(c['A']);need(0<A<L,'invalid parent side')
    need(frac(c['target'])==L/A,'incorrect claimed target')
    den=c['weight_denominator'];need(type(den) is int and den>0,'invalid weight denominator')
    aa=expand(c['orbits']);total=sum(w for x,y,w in aa)
    need(type(c['mass_units']) is int and total==c['mass_units'],'total mass mismatch')
    need(type(c['minimum_units']) is int and c['minimum_units']>=0,'invalid minimum')
    need(17*c['minimum_units']>total,'claimed minimum has insufficient counting margin')
    cursor=F();jobs=[];margins=[]
    need(type(c['entries']) is list and 0<len(c['entries'])<100000,'invalid interval count')
    for row in c['entries']:
        need(type(row) is list and len(row)==4,'invalid interval row')
        a,b,t,B=map(frac,row)
        need(a==cursor and 0<=a<b<1 and 0<B<A,'angle gap or invalid interval')
        ct,st=trig(t);widths=[];factors=[]
        for u in (a,b):
            cp,sp=trig(u);dot=ct*cp+st*sp;cross=abs(st*cp-ct*sp)
            need(dot>0 and dot>=cross,'relative angle exceeds pi/4')
            widths.append(cp+sp);factors.append(dot+cross)
        margin=A-B*max(factors);need(margin>0,'core not strictly interior for whole interval')
        r=A*min(widths)/2
        need(B*(ct+st)/2<=r<L/2,'invalid full parent-center envelope')
        jobs.append((t,B,r));margins.append(margin);cursor=b
    need(cursor*cursor+2*cursor>1,'angle union stops before pi/4')
    return aa,jobs,min(margins)

def upstream_certificate():
    j=read(ROOT/'upstream/catalogue.json');h=frac(j['h']);T=frac(j['T'])
    entries=j['low'].copy()
    for first,stop,B in j['ranges']:
        for k in range(first,stop):
            entries.append(list(map(str,(max(F(),(k-F(1,2))*h),min(T,(k+F(1,2))*h),k*h,F(B)))))
    rows=read(ROOT/'upstream/orbits.json');aa=expand(rows)
    canonical=json.dumps([[str(F(x,100000)),str(F(y,100000)),str(F(w,1000000))] for x,y,w in aa],separators=(',',':')).encode()
    need(hashlib.sha256(canonical).hexdigest()==ATOM_DIGEST,'R012 expanded measure identity failed')
    need(len(aa)==1616 and len(rows)==206 and len(entries)==2925,'R012 counts differ')
    need(j['A']=='99999/100000' and j['target']=='461300/99999','R012 parameters differ')
    c={'L':j['L'],'A':j['A'],'target':j['target'],'weight_denominator':1000000,
       'orbits':rows,'mass_units':16998760,'minimum_units':1000092,'entries':entries}
    validate(c);return c

def write_input(path,aa,jobs):
    with Path(path).open('w') as f:
        print(len(aa),len(jobs),file=f)
        for a in aa:print(*a,file=f)
        for t,B,r in jobs:print(t.numerator,t.denominator,B.numerator,B.denominator,r.numerator,r.denominator,file=f)

def compile_kernel(out,direct=False):
    compiler=os.environ.get('CXX','g++');need(shutil.which(compiler) is not None,'C++ compiler not found')
    binary=out/('sweep-direct' if direct else 'sweep-tree')
    command=[compiler,'-O3','-std=c++17','-fopenmp',str(ROOT/'parent_sweep.cpp'),'-o',str(binary)]
    if direct:command.insert(1,'-DDIRECT_PREFIX_CHECK')
    p=subprocess.run(command,text=True,capture_output=True)
    (out/(binary.name+'.build.log')).write_text(p.stdout+p.stderr)
    need(p.returncode==0,'C++ compilation failed: '+p.stderr[-2000:])
    return binary

def replay(c,name,binary,out,threads):
    aa,jobs,margin=validate(c);inp=out/(name+'.input.txt');write_input(inp,aa,jobs)
    env=dict(os.environ,OMP_NUM_THREADS=str(threads));start=time.monotonic()
    log=out/(name+'.jsonl');err=out/(name+'.log')
    with log.open('w') as f,err.open('w') as e:
        p=subprocess.run([str(binary),str(inp)],stdout=f,stderr=e,env=env)
    need(p.returncode==0,'exact translation replay refused: '+err.read_text()[-2000:])
    rows=[json.loads(s) for s in log.read_text().splitlines()]
    need(len(rows)==len(jobs),'incomplete translation replay')
    minima=[];slabs=0
    for i,row in enumerate(rows):
        need(row['index']==i and row['direct_recount'] is True,'missing or un-recounted envelope')
        need(type(row['minimum_units']) is int and row['minimum_units']>=0,'invalid minimum output')
        minima.append(row['minimum_units']);slabs+=row['slabs']
    gamma=min(minima);total=sum(w for x,y,w in aa)
    need(gamma>=c['minimum_units'] and 17*gamma>total,'coverage/counting condition failed')
    result={'status':'PASS_COMPLETE_PARENT_CATALOGUE','target':str(L/frac(c['A'])),
      'strict_lower_bound':True,'parent_side':c['A'],'atoms':len(aa),'positive_atoms':sum(w>0 for x,y,w in aa),
      'orbits':len(c['orbits']),'positive_orbits':sum(w>0 for x,y,w in c['orbits']),
      'intervals':len(jobs),'minimum':str(F(gamma,c['weight_denominator'])),
      'mass':str(F(total,c['weight_denominator'])),
      'counting_margin':str(F(17*gamma-total,c['weight_denominator'])),
      'minimum_containment_margin':str(margin),'center_slabs':slabs,
      'coverage_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'seconds':time.monotonic()-start}
    (out/(name+'.result.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(name,result['status'],result['target'],flush=True)
    return result,minima

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True)
    p.add_argument('--certificate',default=str(ROOT/'certificate.json'));p.add_argument('--threads',type=int,default=4)
    p.add_argument('--upstream',action='store_true');p.add_argument('--direct',action='store_true');args=p.parse_args()
    need(not sys.flags.optimize,'optimized Python not supported');need(1<=args.threads<=64,'threads must be 1..64')
    out=Path(args.output).resolve();need(not out.exists(),'output directory must be new');out.mkdir(parents=True)
    try:
        cases=[('new',read(args.certificate))]
        if args.upstream:cases.append(('r012',upstream_certificate()))
        tree=compile_kernel(out);reports=[]
        stored={}
        for name,c in cases:
            result,mins=replay(c,name+'-tree',tree,out,args.threads);stored[name]=mins;reports.append(result)
        from sharpening import check
        sharpening=check(cases[0][1])
        (out/'sharpening.result.json').write_text(json.dumps(sharpening,indent=2)+'\n')
        print(sharpening['status'],sharpening['target'],flush=True)
        if args.direct:
            direct=compile_kernel(out,True)
            for name,c in cases:
                result,mins=replay(c,name+'-direct',direct,out,args.threads)
                need(mins==stored[name],'accumulator minima disagree');reports.append(result)
        (out/'RESULT.json').write_text(json.dumps({'status':'PASS_ALL_REQUESTED_REPLAYS','reports':reports,'sharpening':sharpening},indent=2)+'\n')
    except BaseException as e:
        (out/'FAILURE.json').write_text(json.dumps({'status':'FAIL_OR_INCOMPLETE','error':str(e)})+'\n');raise

if __name__=='__main__':
    try:main()
    except Exception as e:print('REFUSED:',e,file=sys.stderr);sys.exit(1)
