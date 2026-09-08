"""Positive, boundary and refusal controls for the exact certificate checker."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import argparse,copy,json,subprocess,tempfile
from make_exact_input import compile_record

def case(L='3/2', B='19/20', weights=('1',), steps=180):
    return {'n':17,'outer_side':L,'square_side':B,'angle_limit':'207107/500000',
            'direction_steps':steps,'atoms':[[str(F(L)/2),str(F(L)/2),w] for w in weights]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('executable');args=ap.parse_args()
    exe=str(Path(args.executable).resolve());tests=[]
    tests.append(('central point covers every core',case(),True))
    tests.append(('duplicate atoms aggregate correctly',case(weights=('1/2','1/2')),True))
    tests.append(('closed boundary coverage is allowed',case('9/5','9/10',steps=5),True))
    tests.append(('one millionth larger exposes a hole',case('1800001/1000000','9/10',steps=5),False))
    tests.append(('underweight by one billionth',case(weights=('999999999/1000000000',)),False))
    tests.append(('zero covering mass',case(weights=('0',)),False))
    tests.append(('mass exactly seventeen is insufficient',case(weights=('17',)),False))
    tests.append(('unshrunken core is refused',case(B='1'),False))
    tests.append(('angular mesh too coarse is refused',case(B='99/100',steps=1),False))
    asym=case();asym['atoms'][0][0]='61/100';tests.append(('asymmetric measure is refused',asym,False))
    outside=case();outside['atoms'][0][0]='2';tests.append(('outside atom is refused',outside,False))
    neg=case(weights=('-1',));tests.append(('negative weights are refused',neg,False))
    with tempfile.TemporaryDirectory() as td:
        for name,record,accept in tests:
            p=Path(td)/'case.txt';compile_record(record,p)
            result=subprocess.run([exe,str(p)],capture_output=True,text=True,check=False)
            ok=result.returncode==0 and 'EXACT_CERTIFICATE_VALID' in result.stdout
            if ok!=accept:raise AssertionError((name,result.returncode,result.stdout,result.stderr))
            print('PASS',name)
        p=Path(td)/'case.txt';compile_record(case(),p);p.write_text(p.read_text()+'unexpected\n')
        result=subprocess.run([exe,str(p)],capture_output=True,text=True,check=False)
        assert result.returncode!=0 and 'unexpected trailing input' in result.stderr
        print('PASS unexpected trailing input is refused')
    print('13 CONTROLS PASSED')
if __name__=='__main__':main()
