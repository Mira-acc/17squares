# Recentered cores and intersection-trigger charges

This note derives new mathematics from the previously established coverage theorem. It does not rerun the parent certificate, launch a packing search, or establish a new global coverage calculation.

## 1. Analytic sharpening

The parent-aware certificate with JSON SHA-256
`5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3`
has outer side `L=4613/1000`, parent side `A=3999/4000`, and counting surplus `4433/500000000`.

Its existing coverage theorem implies the slightly stronger bound

$$s(17)>\frac{46129999999859}{9997499999900}
=4.6141535384166456968083685491\ldots.$$

The increment over `18452/3999` is only

$$\frac{1281341}{39980002499600100}
=3.2049547771109234\ldots\times10^{-11}.$$

This is a small analytical corollary, not a substantial new numerical search result.

### Exact transfer formula

Use coordinates centred at the container centre. Suppose an old core of side `B_j` at angle `theta_j` is known to have charge at least `gamma` at every centre in `[-d_j,d_j]^2`. For a new parent of side `a` and angle `phi`, write

$$f=\cos\phi+\sin\phi,\qquad
w_j=B_j\bigl(|\cos(\theta_j-\phi)|+|\sin(\theta_j-\phi)|\bigr).$$

Assume `H>=af` and `d_j>=0`. In a new square container of side `H`, every legal parent centre can be served by this core if and only if

$$w_j+f[H-af-2d_j]_+<a.$$

Sufficiency follows by clamping each parent-centre coordinate into the old centre domain. The core-centre displacement in either parent-normal coordinate is at most `f[H-af-2d_j]_+/2`. Necessity follows by considering the extreme parent centre `(q,q)`, with `q=(H-af)/2`: every old core centre has both coordinates at most `d_j`, so projection on `(cos phi,sin phi)` cannot be smaller than `f(q-d_j)` when `q>d_j`.

Thus cores need not remain concentric with their parents. They only need to remain strictly inside them, and their new centres must be centres already covered by the old theorem.

### Finite scalar corollary used here

For old catalogue row `j`, let `m_j` be its least parent width factor, `G_j` its greatest core-to-parent projection factor, and

$$\eta_j=A-B_jG_j>0,\qquad d_j=(L-Am_j)/2.$$

Set

$$\varepsilon=10^{-11},\qquad \delta=141/10^{13},\qquad
a=A-\varepsilon,\qquad H=L-\delta.$$

If `F_j` bounds the parent width factor throughout the row, the sufficient condition is

$$\eta_j>\varepsilon+F_j[\varepsilon F_j-\delta]_+.$$

Use the exact endpoint maximum for `F_j`, except when the interval crosses the unique maximum of `f`, where `1414213563/10^9>sqrt(2)` is a rational upper bound. These 4,391 scalar inequalities have positive minimum residual

$$\frac{3156837929188515937426608335639966497291}
{2009206832324365552240070870206040941943769650000000000}>0.$$

No old point weights, core shapes, or covered centre domains have changed. Every new parent receives one old covered core, shifted inward where needed. Selected closed cores in disjoint parent interiors remain disjoint, so the old counting surplus still excludes seventeen parents. Scaling and compactness give the strict rational bound above.

Only the finite angular/domain expressions are evaluated for this corollary. Their underlying translation-coverage premises are inherited from the source proof.

### A cap on using this particular library without new coverage information

At parent angle zero, put `W_j=B_j(c(t_j)+s(t_j))`. The transfer condition requires `a>W_j` and `H<2a+2d_j-W_j`. Therefore the ratio obtainable by assigning one of the old covered cores to every parent is bounded by

$$\max_j\max\{2,1+2d_j/W_j\}
=\frac{783497431270959447209451212282201903}
{169803068915384203003727378193801903}
=4.61415353842273443435\ldots.$$

This is only a cap on reusing the fixed core/domain library in the same container axes, including translations and uniform rescaling. It is NOT an upper bound on `s(17)`, on the actual measure, on new core shapes, or on stronger charges. It explains why a meaningful larger step needs additional information.

## 2. A spatial charge built from pairwise-overlap witnesses

Let `T_1,...,T_m` be nonempty finite point sets with `T_i intersect T_j` nonempty for every pair. Define

$$C_T(K)=\mathbf1\{T_i\subseteq K\text{ for some }i\}.$$

Then every disjoint family of closed cores satisfies

$$\sum_\ell C_T(K_\ell)\le1.$$

Indeed two activated cores would contain intersecting triggers. If they select the same trigger, its nonemptiness gives the same contradiction. This resource has budget one.

A two-of-three threshold atom is the special case of the three two-element subsets of a three-point set. More generally a trigger family has budget at most its matching number. The threshold family of all `k`-subsets of `S` recovers `floor(|S|/k)`. The threshold antecedent is credited to Joshua Levy's squares project; no historical novelty claim is made for general intersecting-family inequalities.

### Compile a robust pose clique

For at least two pairwise-interior-overlapping squares `V_1,...,V_m`, choose a rational point

$$p_{ij}=p_{ji}\in\operatorname{int}V_i\cap\operatorname{int}V_j$$

for each pair, and set `T_i={p_ij:j != i}`. Every source square contains its own trigger, while every pair of triggers shares its designated witness. This compiles a pose clique into a charge based solely on containment of fixed spatial points. The budget applies to arbitrary cores, not only the source poses or their neighbourhoods.

A numerical separation from positive spatial mass additionally requires an
explicit fractional family with pointwise load at most one and trigger charge
greater than one. The exploratory numerical example is not included as a
verified result because its witness artifacts are not retained in this package.

## 3. The coverage geometry stays two-dimensional

At fixed core direction and side `B`, rotate every trigger point to `(u_p,v_p)`. Capturing an entire trigger is equivalent to the centre lying in the rectangle

$$[\max u_p-B/2,\min u_p+B/2]\times
[\max v_p-B/2,\min v_p+B/2].$$

The atom's charge is the indicator of the union of at most `m` such rectangles. A rectangle union has an exact `O(m^2)` open-cell decomposition by vertical slabs and merged vertical intervals. Its pieces remain one resource, not independent budget items. Closed-boundary counts must use the union predicate rather than double-counting seams.

Hence the existing parent-aware approach can use

$$C(K)=\mu(K)+\sum_r w_r C_{T^{(r)}}(K),\qquad
\mathcal B=\mu(\mathbb R^2)+\sum_r w_r.$$

A new global result would follow from universal selected-core charge at least `gamma` and `mathcal B<17 gamma`. That new global coverage inequality has NOT been computed here.

## Status

The tiny displayed bound is an analytic consequence of the existing coverage certificate. The new intersection-trigger resource is an exact finite construction with a proved budget and a fixed-direction coverage representation. There is no new large-scale replay, no claimed bound at 4.67, and no proof of global Bidwell optimality in this note. The larger opportunity is that compatibility information can now be expressed in the same fixed-direction rectangle language as the existing spatial checker.

The package replay checks the scalar sharpening with `sharpening.py`; its
translation-coverage premise is verified by the full C++ replay.
