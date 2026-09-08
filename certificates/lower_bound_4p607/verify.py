#!/usr/bin/env python3
"""Rebuild and replay exact 17-square certificates; no solver/network required."""
from __future__ import annotations
import argparse,hashlib,json,os,re,subprocess
from fractions import Fraction as F
from pathlib import Path
from make_exact_input import compile_record

ROOT=Path(__file__).resolve().parent
SOURCE_BLOB='f454e44dee1f2318af45e02efdfff5fcd7dbfbe1'
SUMMARY=re.compile(r'EXACT_CERTIFICATE_VALID atoms (\d+) directions (\d+) total_mass (\d+/\d+) minimum (\d+/\d+) slabs (\d+)')

def digest(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replay(exe:Path, record_path:Path, output:Path, name:str)->dict:
    raw=record_path.read_bytes();record=json.loads(raw)
    if record.get('n')!=17:raise ValueError('This kernel only certifies n=17.')
    mass=sum(F(row[2]) for row in record['atoms'])
    if F(record['total_mass'])!=mass:raise ValueError('Declared total_mass does not match atoms.')
    integer_input=output/(name+'.input.txt');compile_record(record,integer_input)
    log=output/(name+'.log')
    with log.open('w') as stream:
        run=subprocess.run([str(exe),str(integer_input)],stdout=stream,stderr=subprocess.STDOUT,check=False)
    text=log.read_text();match=SUMMARY.search(text)
    if run.returncode or match is None:raise RuntimeError(f'Exact replay refused {record_path}; see {log}')
    atoms,directions,total,minimum,slabs=match.groups()
    if F(total)!=mass or F(minimum)<1:raise ValueError('Inconsistent replay summary.')
    L=F(record['outer_side']);B=F(record['square_side']);h=F(record['angle_limit'])/record['direction_steps']
    endpoint_squared=L*L*(1+h*h)/(B*B*(1+h)**2)
    print(f'{name}: s(17) > {L}; {match.group(0)}',flush=True)
    return {'certificate_sha256':hashlib.sha256(raw).hexdigest(),'outer_side':str(L),
            'total_mass':str(F(total)),'minimum_mass':str(F(minimum)),
            'atoms':int(atoms),'directions':int(directions),'slabs':int(slabs),
            'weak_endpoint_squared':str(endpoint_squared),'log_sha256':digest(log)}

def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--direct',action='store_true',help='Also replay the direct prefix-sum accumulation engine.')
    ap.add_argument('--output',type=Path,default=ROOT/'.replay')
    ap.add_argument('--compiler',default=os.environ.get('CXX','g++'))
    args=ap.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    record=json.loads((ROOT/'result.json').read_text())
    source=ROOT/'source'/'jlevy-certificate.json';data=source.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob!=SOURCE_BLOB:raise ValueError('Upstream source-byte identity check failed.')
    best=ROOT/'best-certificate.json'
    if digest(best)!=record['certificate_sha256']:raise ValueError('Best-certificate byte identity check failed.')
    results={}
    for mode in (['tree','direct'] if args.direct else ['tree']):
        executable=out/('exact_cover_'+mode)
        cmd=[args.compiler,'-O3','-std=c++17',str(ROOT/'exact_sweep.cpp'),'-o',str(executable)]
        if mode=='direct':cmd.insert(1,'-DDIRECT_PREFIX_CHECK')
        subprocess.run(cmd,check=True)
        with (out/f'controls-{mode}.log').open('w') as stream:
            subprocess.run(['python3',str(ROOT/'test_checker.py'),str(executable)],stdout=stream,stderr=subprocess.STDOUT,check=True)
        results['source-'+mode]=replay(executable,source,out,'source-'+mode)
        results['best-'+mode]=replay(executable,best,out,'best-'+mode)
    actual=results['best-tree']
    for field in ('total_mass','minimum_mass','atoms','directions','slabs','weak_endpoint_squared'):
        if str(actual[field])!=str(record[field]):raise ValueError(f'Result mismatch: {field}')
    strict=F(record['strict_decimal_bound'])
    if strict<=0 or strict*strict>=F(actual['weak_endpoint_squared']):
        raise ValueError('Strict decimal bound is not below the proved radical endpoint.')
    if args.direct:
        for label in ['source','best']:
            if (out/(label+'-tree.log')).read_bytes()!=(out/(label+'-direct.log')).read_bytes():
                raise ValueError('Accumulation engines disagree: '+label)
    (out/'replay-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print('VERIFIED strict bound: s(17) > '+record['strict_decimal_bound'])
    print('VERIFIED weak endpoint: s(17) >= sqrt('+record['weak_endpoint_squared']+')')
if __name__=='__main__':main()
