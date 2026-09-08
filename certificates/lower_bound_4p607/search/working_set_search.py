"""Exploratory row generation with a retained constraint pool and small LP working set."""
from optimizer import *
from scipy.sparse import load_npz, save_npz
L=float(sys.argv[1]);steps=int(sys.argv[2]);B=float(sys.argv[3])
key=f'{L}_{steps}'
if os.environ.get('FRESH'):
 w=np.load(os.environ['WARM'])['w'].copy();A=csr_matrix((0,nv))
else:
 w=np.load(ROOT/f'candidate_{key}.npz')['w'].copy();A=load_npz(ROOT/f'constraints_{key}.npz').tocsr()
seen={row.tobytes() for row in np.asarray(A.toarray(),dtype=np.uint8)}
active=set(np.where(A@w<1.002)[0].tolist())
# A small generic perturbation of the objective discourages cycling on a flat optimum.
rng=np.random.default_rng(17072026);objective=sz*(1+1e-5*rng.uniform(size=nv));target=1.000001
for it in range(20):
 tm=time.time();m,r=oracle(L,B,w,steps,8)
 mass=sz@w
 print('OUTER',it,'mass',mass,'min',m.min(),'pool',A.shape[0],'seconds',time.time()-tm,flush=True)
 if m.min()>0 and mass*target/m.min()<16.9998:
  w*=target/m.min();m*=target/m.min()
  np.savez(ROOT/f'candidate_{key}.npz',L=L,B=B,steps=steps,w=w,mins=m)
  print('NUMERICAL_CANDIDATE_READY mass',sz@w,'minimum',m.min(),flush=True);break
 new=[]
 for row in r:
  keyrow=row.tobytes()
  if keyrow not in seen:seen.add(keyrow);new.append(row)
 if new:A=vstack([A,csr_matrix(np.array(new))],format='csr')
 # Re-solve a small working set; restore ANY omitted pool constraint that fails.
 for inner in range(100):
  slack=A@w-target
  bad=np.where(slack < -1e-8)[0]
  if len(bad):active.update(bad[np.argsort(slack[bad])[:500]].tolist())
  if not active:active=set(np.argsort(slack)[:min(500,len(slack))].tolist())
  ix=np.array(sorted(active));AA=A[ix]
  tm=time.time();res=linprog(objective,A_ub=-AA,b_ub=-np.full(len(ix),target),bounds=(0,None),method='highs')
  if not res.success:raise RuntimeError(res.message)
  w=res.x;slack=A@w-target;bad=np.where(slack < -2e-8)[0]
  print(' LP',inner,'working',len(ix),'pool_violations',len(bad),'mass',sz@w,'seconds',time.time()-tm,flush=True)
  if not len(bad):
   active=set(ix[np.abs(res.ineqlin.marginals)>1e-9].tolist())
   active.update(np.argsort(slack)[:min(700,len(slack))].tolist())
   break
 else:raise RuntimeError('working-set limit reached')
 np.savez(ROOT/f'candidate_{key}.npz',L=L,B=B,steps=steps,w=w,mins=m)
 save_npz(ROOT/f'constraints_{key}.npz',A)
 if sz@w>17.001:print('FINITE_LP_EXCEEDS_17_NUMERICAL_ONLY',flush=True);break
