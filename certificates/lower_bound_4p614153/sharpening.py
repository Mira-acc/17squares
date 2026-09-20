"""Exact scalar transfer checks; translation coverage is supplied by verify.py."""
from fractions import Fraction as F

EPSILON = F(1, 100000000000)
DELTA = F(141, 10000000000000)
SQRT2_UPPER = F(1414213563, 1000000000)


def check(c):
    from verify import validate, trig, need
    validate(c)
    L, A = F(c['L']), F(c['A'])
    need(0 < EPSILON < A and 0 < DELTA < L, 'invalid transfer parameters')
    need(SQRT2_UPPER**2 > 2, 'invalid sqrt(2) upper bound')
    need(L-DELTA > (A-EPSILON)*SQRT2_UPPER, 'empty legal-center domain')
    residuals, caps = [], []
    for row in c['entries']:
        lo, hi, t, B = map(F, row)
        widths = [sum(trig(u)) for u in (lo, hi)]
        ct, st = trig(t)
        factors = []
        for u in (lo, hi):
            cp, sp = trig(u)
            factors.append(ct*cp + st*sp + abs(st*cp-ct*sp))
        crosses_peak = lo*lo+2*lo <= 1 <= hi*hi+2*hi
        upper = SQRT2_UPPER if crosses_peak else max(widths)
        eta = A-B*max(factors)
        residual = eta-EPSILON-upper*max(EPSILON*upper-DELTA, F(0))
        need(residual > 0, 'recentered containment inequality failed')
        residuals.append(residual)
        diameter = L-A*min(widths)
        caps.append(max(F(2), 1+diameter/(B*(ct+st))))
    return {
        'status': 'PASS_EXACT_RECENTERING_INEQUALITIES',
        'target': str((L-DELTA)/(A-EPSILON)),
        'epsilon': str(EPSILON), 'delta': str(DELTA),
        'intervals': len(residuals),
        'minimum_scalar_slack': str(min(residuals)),
        'fixed_library_axis_cap': str(max(caps)),
    }
