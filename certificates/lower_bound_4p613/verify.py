#!/usr/bin/env python3
"""Rebuild and replay the exact 4.613 packing certificate using no numerical solver.

Default: both accumulation engines, their controls, and the exact restricted-
dictionary obstruction. --source also replays Levy's retained source control.
The engines share the geometric partition, not the accumulation implementation.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, sys
from fractions import Fraction as F
from pathlib import Path
from make_exact_input import compile_record

ROOT = Path(__file__).resolve().parent
SUMMARY = re.compile(r'EXACT_CERTIFICATE_VALID atoms (\d+) directions (\d+) total_mass (\d+/\d+) minimum (\d+/\d+) slabs (\d+)')
SOURCE_BLOB = 'f454e44dee1f2318af45e02efdfff5fcd7dbfbe1'

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replay(exe: Path, path: Path, out: Path, name: str) -> dict:
    record = json.loads(path.read_text(encoding='utf-8'))
    if record.get('n') != 17:
        raise ValueError('This kernel certifies n=17 only.')
    if record.get('angle_limit') != '207107/500000':
        raise ValueError('The theorem uses the prescribed rational direction net.')
    mass = sum((F(row[2]) for row in record['atoms']), F(0))
    if mass != F(record['total_mass']):
        raise ValueError('Declared total mass differs from the sum of atom weights.')
    inp = out / (name + '.input.txt')
    compile_record(record, inp)
    log = out / (name + '.log')
    with log.open('w', encoding='utf-8') as stream:
        run = subprocess.run([str(exe), str(inp)], stdout=stream, stderr=subprocess.STDOUT)
    text = log.read_text(encoding='utf-8')
    match = SUMMARY.search(text)
    if run.returncode or match is None:
        raise RuntimeError(f'Exact replay refused {path.name}; inspect {log}')
    n, directions, total, minimum, slabs = match.groups()
    if int(n) != len(record['atoms']) or int(directions) != record['direction_steps'] + 1:
        raise ValueError('Replay dimensions differ from the certificate.')
    if F(total) != mass or F(minimum) < 1:
        raise ValueError('Inconsistent replay mass.')
    L, B = F(record['outer_side']), F(record['square_side'])
    h = F(record['angle_limit']) / record['direction_steps']
    square = L*L*(1+h*h)/(B*B*(1+h)**2)
    print(name + ': ' + match.group(0), flush=True)
    return dict(atoms=int(n), directions=int(directions), total_mass=str(F(total)),
                minimum_mass=str(F(minimum)), slabs=int(slabs), outer_side=str(L),
                core_side=str(B), weak_endpoint_squared=str(square),
                certificate_sha256=digest(path), log_sha256=digest(log))

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tree-only', action='store_true', help='Omit the direct accumulation cross-check.')
    ap.add_argument('--source', action='store_true', help='Also replay the retained 4.59 upstream source control.')
    ap.add_argument('--output', type=Path, default=ROOT / '.replay')
    ap.add_argument('--compiler', default=os.environ.get('CXX', 'g++'))
    args = ap.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    expected = json.loads((ROOT/'result.json').read_text())
    best = ROOT/'best-certificate.json'
    for path, field in [(best, 'certificate_sha256'), (ROOT/'exact_sweep.cpp', 'checker_sha256')]:
        if digest(path) != expected[field]:
            raise ValueError(f'Byte identity mismatch: {path.name}')
    source = ROOT/'source'/'jlevy-certificate.json'
    data = source.read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if blob != SOURCE_BLOB:
        raise ValueError('Upstream source byte identity mismatch.')
    diagnostic = ROOT/'diagnostic'/'verify_obstruction.py'
    with (out/'diagnostic-controls.log').open('w') as stream:
        subprocess.run([sys.executable, str(diagnostic.with_name('test_obstruction.py'))],
                       stdout=stream, stderr=subprocess.STDOUT, check=True)
    with (out/'restricted-dictionary.log').open('w') as stream:
        subprocess.run([sys.executable, str(diagnostic), 'verify',
                        str(diagnostic.with_name('restricted-dictionary-obstruction.json'))],
                       stdout=stream, stderr=subprocess.STDOUT, check=True)
    results = {}
    modes = ['tree'] if args.tree_only else ['tree', 'direct']
    for mode in modes:
        exe = out/('exact_cover_' + mode)
        cmd = [args.compiler, '-O3', '-std=c++17', str(ROOT/'exact_sweep.cpp'), '-o', str(exe)]
        if mode == 'direct':
            cmd.insert(1, '-DDIRECT_PREFIX_CHECK')
        subprocess.run(cmd, check=True)
        with (out/('controls-' + mode + '.log')).open('w') as stream:
            subprocess.run([sys.executable, str(ROOT/'test_checker.py'), str(exe)],
                           stdout=stream, stderr=subprocess.STDOUT, check=True)
        results['best-' + mode] = replay(exe, best, out, 'best-' + mode)
        with (out/('controls-ablation-' + mode + '.log')).open('w') as stream:
            subprocess.run([sys.executable, str(ROOT/'diagnostic'/'test_ablation.py'), str(exe),
                            '--log', str(out/('ablation-' + mode + '.log'))],
                           stdout=stream, stderr=subprocess.STDOUT, check=True)
        if args.source:
            results['source-' + mode] = replay(exe, source, out, 'source-' + mode)
    actual = results['best-tree']
    for field in ('atoms', 'directions', 'total_mass', 'minimum_mass', 'slabs',
                  'outer_side', 'core_side', 'weak_endpoint_squared'):
        if str(actual[field]) != str(expected[field]):
            raise ValueError('Result metadata mismatch: ' + field)
    strict = F(expected['strict_decimal_bound'])
    if strict <= F('4.610028617263') or strict*strict >= F(actual['weak_endpoint_squared']):
        raise ValueError('Claimed strict improvement is not below the proved endpoint.')
    if not args.tree_only:
        for label in (['best', 'source'] if args.source else ['best']):
            if (out/(label+'-tree.log')).read_bytes() != (out/(label+'-direct.log')).read_bytes():
                raise ValueError('Accumulation engines disagree: ' + label)
    (out/'replay-results.json').write_text(json.dumps(results, indent=2)+'\n')
    print('VERIFIED strict bound: s(17) > ' + expected['strict_decimal_bound'])
    print('VERIFIED weak endpoint: s(17) >= sqrt(' + expected['weak_endpoint_squared'] + ')')
    print('EXACT_REPLAY_AND_DIAGNOSTIC_PASSED')

if __name__ == '__main__':
    main()
