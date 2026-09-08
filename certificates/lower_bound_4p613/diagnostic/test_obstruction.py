#!/usr/bin/env python3
"""Positive and deliberate-refusal controls for the exact LP-dual diagnostic."""
from __future__ import annotations
import contextlib,copy,io,json,subprocess,sys
from pathlib import Path
from verify_obstruction import verify_obstruction
ROOT=Path(__file__).resolve().parent

def run() -> None:
    original=json.loads((ROOT/'restricted-dictionary-obstruction.json').read_text())
    with contextlib.redirect_stdout(io.StringIO()):
        verify_obstruction(original)
    print('PASS original exact dual obstruction')
    tests=[]
    zero=copy.deepcopy(original)
    for p in zero['poses']:p['dual']='0'
    tests.append(('zero dual gives no obstruction',zero))
    huge=copy.deepcopy(original);huge['poses'][0]['dual']='1000000'
    tests.append(('infeasible dual multiplier is refused',huge))
    neg=copy.deepcopy(original);neg['poses'][0]['dual']='-1'
    tests.append(('negative dual multiplier is refused',neg))
    far=copy.deepcopy(original);far['poses'][0]['x']='100'
    tests.append(('core outside the container is refused',far))
    badangle=copy.deepcopy(original);badangle['poses'][0]['p']=0;badangle['poses'][0]['q']=0
    tests.append(('invalid direction is refused',badangle))
    badsite=copy.deepcopy(original);badsite['sites'][0]=['-1','0']
    tests.append(('support outside the container is refused',badsite))
    for name,record in tests:
        try:
            with contextlib.redirect_stdout(io.StringIO()):verify_obstruction(record)
        except (AssertionError,ValueError,RuntimeError,ZeroDivisionError):
            print('PASS '+name)
        else:
            raise RuntimeError('Invalid diagnostic accepted: '+name)
    result=subprocess.run([sys.executable,'-O',str(ROOT/'verify_obstruction.py'),'verify',
                           str(ROOT/'restricted-dictionary-obstruction.json')],capture_output=True,text=True)
    if result.returncode==0 or 'without Python optimization flags' not in result.stderr:
        raise RuntimeError('Optimized-Python mode was not explicitly refused')
    print('PASS optimized Python mode is refused')
    print('8 DIAGNOSTIC CONTROLS PASSED')
if __name__=='__main__':run()
