// Numerical research tools only; final claims require exact_sweep.cpp.
#include "numeric_sweep.cpp"
#include <omp.h>
extern "C" int pose_sweep(int N,const double*X,const double*Y,const double*W,int nv,const int*ids,double L,double B,int steps,double threshold,int perdir,double*mins,unsigned char*out,double*poses){
 std::vector<int> counts(steps+1);
 #pragma omp parallel for schedule(dynamic)
 for(int k=0;k<=steps;k++){
  double t=(207107.0/500000.0)*k/steps,c=(1-t*t)/(1+t*t),s=2*t/(1+t*t),H=(L-B*(c+s))/2,extent=H*(c+s);
  vector<double>U(N),V(N),vs={-100.,100.};vector<Event>ev;ev.push_back({-extent,-1,0});ev.push_back({extent,-1,0});
  for(int i=0;i<N;i++){U[i]=c*X[i]+s*Y[i];V[i]=-s*X[i]+c*Y[i];vs.push_back(V[i]-B/2);vs.push_back(V[i]+B/2);ev.push_back({U[i]-B/2,i,1});ev.push_back({U[i]+B/2,i,-1});}
  sort(vs.begin(),vs.end());vector<double>uniq;for(double v:vs)if(uniq.empty()||v-uniq.back()>1e-12)uniq.push_back(v);vs.swap(uniq);sort(ev.begin(),ev.end());
  vector<int>lo(N),hi(N);for(int i=0;i<N;i++){lo[i]=lower_bound(vs.begin(),vs.end(),V[i]-B/2-1e-12)-vs.begin();hi[i]=lower_bound(vs.begin(),vs.end(),V[i]+B/2-1e-12)-vs.begin();}
  struct Cand {double mass=1e100,a=0,b=0,vl=0,vh=0;int cell=-1;};vector<Cand>cand(128);Seg seg(vs.size()-1);double best=1e100;
  for(int j=0;j<(int)ev.size();){int end=j+1;while(end<(int)ev.size()&&ev[end].u-ev[j].u<1e-12)end++;
   for(int z=j;z<end;z++)if(ev[z].i>=0){int i=ev[z].i;seg.add(lo[i],hi[i],ev[z].sgn*W[i]);}
   if(end==(int)ev.size())break;
   double a=max(ev[end-1].u,-extent),b=min(ev[end].u,extent);j=end;if(b-a<1e-12)continue;
   double vl,vh;if(s<1e-15){vl=-H;vh=H;}else{double ua=min(b,max(a,H*(c-s))),ub=min(b,max(a,-H*(c-s)));vl=max((c*ua-H)/s,(-H-s*ua)/c);vh=min((c*ub+H)/s,(H-s*ub)/c);}
   int l=upper_bound(vs.begin(),vs.end(),vl+1e-12)-vs.begin()-1,r=lower_bound(vs.begin(),vs.end(),vh-1e-12)-vs.begin();l=max(l,0);r=min(r,(int)vs.size()-1);if(l>=r)continue;
   auto q=seg.query(l,r);best=min(best,q.first);
   if(q.first<threshold){int bucket=max(0,min(127,int(128*((a+b)/2+extent)/(2*extent))));if(q.first<cand[bucket].mass)cand[bucket]={q.first,a,b,vl,vh,q.second};}
  }
  mins[k]=best;sort(cand.begin(),cand.end(),[](const Cand&a,const Cand&b){return a.mass<b.mass;});set<string>seen;int count=0;
  for(auto&p:cand){if(p.cell<0||count>=perdir)break;
   double vlo=max(vs[p.cell],p.vl),vhi=min(vs[p.cell+1],p.vh);if(vhi-vlo<1e-13)continue;double v=(vlo+vhi)/2;
   double ua=p.a,ub=p.b;ua=max(ua,(-H+s*v)/c);ub=min(ub,(H+s*v)/c);if(s>1e-15){ua=max(ua,(-H-c*v)/s);ub=min(ub,(H-c*v)/s);}if(ub-ua<1e-13)continue;double u=(ua+ub)/2;
   string row(nv,0);for(int i=0;i<N;i++)if(fabs(U[i]-u)<B/2&&fabs(V[i]-v)<B/2)row[ids[i]]++;
   if(!seen.insert(row).second)continue;int idx=k*perdir+count++;memcpy(out+idx*nv,row.data(),nv);poses[4*idx]=c*u-s*v;poses[4*idx+1]=s*u+c*v;poses[4*idx+2]=c;poses[4*idx+3]=s;
  }
  counts[k]=count;
 }
 int count=0;for(int k=0;k<=steps;k++)for(int j=0;j<counts[k];j++){int src=k*perdir+j;memmove(out+count*nv,out+src*nv,nv);memmove(poses+4*count,poses+4*src,4*sizeof(double));count++;}return count;
}
// Sum orbit incidence at arbitrary stored feasible square poses.
extern "C" void incidence(int np,const double*poses,int na,const double*X,const double*Y,int nv,const int*ids,double B,unsigned char*out){
 #pragma omp parallel for schedule(static)
 for(int p=0;p<np;p++){auto row=out+p*nv;memset(row,0,nv);double x=poses[4*p],y=poses[4*p+1],c=poses[4*p+2],s=poses[4*p+3];for(int i=0;i<na;i++){double dx=X[i]-x,dy=Y[i]-y;if(fabs(c*dx+s*dy)<B/2&&fabs(-s*dx+c*dy)<B/2)row[ids[i]]++;}}
}
struct PriceEvent{double x,w;bool operator<(const PriceEvent&o)const{return x<o.x;}};
// For each scanline y in [0,L/2], maximize the symmetrized dual price
// on 0<x<y. The output is (score, uncentered x, uncentered y).
extern "C" void price_lines(int np,const double*poses,const double*dual,double L,double B,int ny,const double*ys,double*out){
 struct Square {double x,y,c,s,w;};vector<Square>sq;
 for(int p=0;p<np;p++){double x=poses[4*p],y=poses[4*p+1],c=poses[4*p+2],s=poses[4*p+3];for(int swap=0;swap<2;swap++)for(int sx:{-1,1})for(int sy:{-1,1}){sq.push_back({sx*(swap?y:x),sy*(swap?x:y),sx*(swap?s:c),sy*(swap?c:s),dual[p]/8});}}
 #pragma omp parallel for schedule(dynamic)
 for(int j=0;j<ny;j++){double yy=ys[j]-L/2;vector<PriceEvent>ev;ev.reserve(2*sq.size()+2);ev.push_back({-L/2,0});ev.push_back({yy,0});
  for(auto&q:sq){double lo=-L/2,hi=yy,dy=yy-q.y;bool ok=true;double aa[2]={q.c,-q.s},bb[2]={q.s*dy,q.c*dy};for(int k=0;k<2;k++){double a=aa[k],b=bb[k];if(fabs(a)<1e-14){if(fabs(b)>=B/2)ok=false;}else{double l=q.x+(-B/2-b)/a,h=q.x+(B/2-b)/a;if(l>h)std::swap(l,h);lo=max(lo,l);hi=min(hi,h);}}if(ok&&hi-lo>1e-12){ev.push_back({lo,q.w});ev.push_back({hi,-q.w});}}
  sort(ev.begin(),ev.end());double score=0,best=-1,x=0;
  for(int k=0;k<(int)ev.size();){int e=k+1;while(e<(int)ev.size()&&ev[e].x-ev[k].x<1e-12)e++;for(int z=k;z<e;z++)score+=ev[z].w;if(e<(int)ev.size()&&ev[e].x-ev[e-1].x>1e-11&&score>best){best=score;x=(ev[e].x+ev[e-1].x)/2;}k=e;}
  out[3*j]=best;out[3*j+1]=x+L/2;out[3*j+2]=ys[j];
 }
}
