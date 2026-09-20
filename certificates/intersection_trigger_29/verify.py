"""Exact witness and pointwise-load verification for the supplied 29 poses.

The 71 reported activations are separately checked from pinned source poses.
"""
import csv
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def polygon(pose):
    x, y, c, s = pose[:4]
    return [(x+(c*u-s*v)/2, y+(s*u+c*v)/2)
            for u, v in ((-1,-1),(1,-1),(1,1),(-1,1))]


def margin(pose, point):
    x, y, c, s = pose[:4]
    dx, dy = point[0]-x, point[1]-y
    return F(1,2)-max(abs(c*dx+s*dy),abs(-s*dx+c*dy))


def maximum_load(poses):
    """Enumerate every open cell of the rational polygon arrangement.

    All vertex and segment-intersection abscissae are events. Between them,
    vertical edge order and every cell's covering set are invariant. At the
    rational midpoint, interval endpoint events enumerate all vertical cells.
    For open squares a boundary point's containing squares also contain a
    neighbourhood, so boundaries cannot have a larger load than an open cell.
    """
    polygons = [polygon(p) for p in poses]
    edges = [(poly[i],poly[(i+1)%4]) for poly in polygons for i in range(4)]
    events = {p[0] for poly in polygons for p in poly}
    for (a,b),(c,d) in itertools.combinations(edges,2):
        r,s = sub(b,a),sub(d,c)
        det = cross(r,s)
        if not det:
            continue  # Collinear overlap changes only at existing endpoints.
        t,u = cross(sub(c,a),s)/det,cross(sub(c,a),r)/det
        if 0 <= t <= 1 and 0 <= u <= 1:
            events.add(a[0]+t*r[0])
    ordered = sorted(events)
    best, witness = F(0), None
    for left,right in zip(ordered,ordered[1:]):
        x = (left+right)/2
        changes = {}
        for pose,poly in zip(poses,polygons):
            ys = []
            for a,b in zip(poly,poly[1:]+poly[:1]):
                if min(a[0],b[0]) < x < max(a[0],b[0]):
                    ys.append(a[1]+(x-a[0])*(b[1]-a[1])/(b[0]-a[0]))
            if ys:
                need(len(ys)==2, 'invalid polygon section')
                lo,hi = min(ys),max(ys)
                changes[lo] = changes.get(lo,F(0))+pose[4]
                changes[hi] = changes.get(hi,F(0))-pose[4]
        level = F(0)
        heights = sorted(changes)
        for y,next_y in zip(heights,heights[1:]):
            level += changes[y]
            if level > best:
                best,witness = level,(x,(y+next_y)/2)
    need(witness is not None, 'empty arrangement')
    recount = sum(p[4] for p in poses if margin(p,witness)>0)
    need(recount==best,'maximum witness recount mismatch')
    return best,witness,len(ordered)-1


def check():
    atom = json.loads((ROOT/'intersection-atom.json').read_text())
    with (ROOT/'clique-29-poses-with-weights.csv').open(newline='',encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    indices = [int(r['source_index']) for r in rows]
    need(indices==atom['pose_indices'] and len(set(indices))==29,'pose identities')
    poses = []
    for row,source in zip(rows,atom['source_poses']):
        geom = tuple(F(row[k]) for k in ('x','y','c','s'))
        weight = F(int(row['weight_numerator']),int(row['weight_denominator']))
        need(weight>=0 and weight==F(row['weight']),'invalid weight')
        need(list(geom)==list(map(F,source[:4])) and int(row['weight_numerator'])==source[4],'source/CSV mismatch')
        x,y,c,s = geom
        need(c*c+s*s==1,'nonunit rotation')
        need(max(abs(x),abs(y))+(abs(c)+abs(s))/2<=F(atom['outer_side'])/2,'pose outside container')
        poses.append((*geom,weight))
    points = [tuple(map(F,p)) for p in atom['points']]
    triggers = [set(t) for t in atom['triggers']]
    need(len(points)==len(set(points))==406,'point count')
    need(len(triggers)==29 and all(len(t)==28 for t in triggers),'trigger sizes')
    need(all(0<=i<len(points) for t in triggers for i in t),'invalid point index')
    pairs = {(i,j):k for i,j,k in atom['pair_witnesses']}
    need(len(atom['pair_witnesses'])==len(pairs)==406,'pair count')
    need(set(pairs)==set(itertools.combinations(range(29),2)),'incomplete pairs')
    for (i,j),k in pairs.items():
        need(triggers[i]&triggers[j]=={k},'missing shared pair witness')
    slack = min(margin(p,points[k]) for p,t in zip(poses,triggers) for k in t)
    need(slack==F(atom['source_pose_trigger_edge_margin']),'edge margin mismatch')
    need(slack>F(1,1000),'triggers do not fit side-0.998 cores')
    total = sum(p[4] for p in poses)
    need(total==F(atom['retained_clique_fractional_mass']) and total>1,'weight separation')
    load,witness,slabs = maximum_load(poses)
    need(load<=1,'pointwise load exceeds one')
    extra = check_additional(atom,points,triggers,poses)
    return {'status':'PASS_29_POSE_TRIGGER_SEPARATION','points':len(points),
            'triggers':len(triggers),'core_side':'499/500',
            'minimum_unit_square_edge_margin':str(slack),
            'fractional_mass':str(total),'maximum_pointwise_load':str(load),
            'positive_measure_cost_lower_bound':str(total/load),
            'maximum_load_witness':list(map(str,witness)),
            'arrangement_slabs':slabs,'additional_activations':extra,
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (ROOT/'intersection-atom.json',ROOT/'clique-29-poses-with-weights.csv')}}


def check_additional(atom,points,triggers,selected):
    raw=(ROOT/'sources/fractional-obstruction.dat').read_bytes()
    clraw=(ROOT/'sources/clique-certificate.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==atom['source_pose_sha256'],'source pose hash')
    need(hashlib.sha256(clraw).hexdigest()==atom['source_clique_sha256'],'source clique hash')
    clique=json.loads(clraw)
    need(clique['indices']==atom['pose_indices'],'source clique identities')
    denominator=clique['max_load_numerator']
    need(denominator==79999999999,'source weight denominator')
    fields=raw.decode().split();L=F(fields[0]);count=int(fields[1]);all_poses=[]
    need(len(fields)==2+4*count and L==F(atom['outer_side']),'source pose format')
    for i in range(count):
        x,y,t=map(F,fields[2+4*i:5+4*i]);weight=int(fields[5+4*i])
        need(weight>=0,'negative source weight')
        c,s=(1-t*t)/(1+t*t),2*t/(1+t*t)
        for swap in (0,1):
            for sx in (-1,1):
                for sy in (-1,1):
                    all_poses.append((sx*(y if swap else x),sy*(x if swap else y),
                                      sx*(s if swap else c),sy*(c if swap else s),F(weight,denominator)))
    need([all_poses[i] for i in atom['pose_indices']]==selected,'expanded CSV identity')
    activated=[];small=[];seen=set()
    for record in atom['additional_source_activations']:
        i=record['source_index'];k=record['trigger']
        need(i not in seen and 0<=i<len(all_poses) and 0<=k<len(triggers),'activation identity')
        seen.add(i);p=all_poses[i]
        need(p[4]==F(record['weight'],denominator),'activation weight')
        x,y,c,s=p[:4]
        need(max(abs(x),abs(y))+(abs(c)+abs(s))/2<=L/2,'activation outside container')
        slack=min(margin(p,points[j]) for j in triggers[k])
        need(slack>0 and slack==F(record['margin']),'activation margin')
        activated.append(p)
        if slack>=F(1,1000):small.append(i)
    need(len(activated)==71,'activation count')
    need(small==atom['source_side_499_over_500_activation_indices'] and len(small)==68,'small-core activation identities')
    total=sum(p[4] for p in activated)
    small_total=sum(all_poses[i][4] for i in small)
    need(total==F(atom['certified_fractional_activation_lower_bound']),'unit activation sum')
    need(small_total==F(atom['source_side_499_over_500_fractional_activation_lower_bound']),'small activation sum')
    load,witness,slabs=maximum_load(activated)
    need(load<=1,'additional-activation pointwise load exceeds one')
    return {'status':'PASS_71_ACTIVATIONS_AND_SUBSET_LOAD',
            'unit_activations':71,'small_core_activations':68,
            'unit_weight_sum':str(total),'small_core_weight_sum':str(small_total),
            'maximum_pointwise_load':str(load),'arrangement_slabs':slabs,
            'maximum_load_witness':list(map(str,witness)),
            'full_616_pose_load_checked':False}


if __name__=='__main__':
    print(json.dumps(check(),indent=2))
