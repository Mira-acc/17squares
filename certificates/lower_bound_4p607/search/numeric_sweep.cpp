// Exploratory floating-point separation oracle. NOT a proof checker.
#include <algorithm>
#include <cmath>
#include <vector>
#include <set>
#include <string>
#include <limits>
#include <cstring>
using namespace std;
struct Seg {
 int n; vector<double> mn,lazy; vector<int> arg;
 Seg(int sz){n=1;while(n<sz)n*=2;mn.assign(2*n,0);lazy.assign(2*n,0);arg.resize(2*n);for(int i=0;i<n;i++)arg[n+i]=i;for(int i=n-1;i;i--)arg[i]=arg[2*i];}
 void add(int l,int r,double v,int k,int a,int b){if(l>=b||r<=a)return;if(l<=a&&b<=r){mn[k]+=v;lazy[k]+=v;return;}int m=(a+b)/2;add(l,r,v,k*2,a,m);add(l,r,v,k*2+1,m,b);if(mn[2*k]<=mn[2*k+1]){mn[k]=mn[2*k]+lazy[k];arg[k]=arg[2*k];}else{mn[k]=mn[2*k+1]+lazy[k];arg[k]=arg[2*k+1];}}
 void add(int l,int r,double v){if(l<r)add(l,r,v,1,0,n);}
 pair<double,int> query(int l,int r,int k,int a,int b){if(l>=b||r<=a)return {1e100,-1};if(l<=a&&b<=r)return {mn[k],arg[k]};int m=(a+b)/2;auto x=query(l,r,2*k,a,m),y=query(l,r,2*k+1,m,b);auto z=(x.first<=y.first?x:y);z.first+=lazy[k];return z;}
 pair<double,int> query(int l,int r){return query(l,r,1,0,n);}
};
struct Event { double u; int i,sgn; bool operator<(const Event &a)const{return u<a.u;} };
extern "C" int sweep(int N,const double* X,const double* Y,const double* W,int nv,const int* ids,double L,double B,int steps,double* mins,unsigned char* out,int cap,int perdir){
 int nr=0; set<string> seen;
 for(int k=0;k<=steps;k++){
  double t=(207107.0/500000.0)*k/steps,c=(1-t*t)/(1+t*t),s=2*t/(1+t*t),H=(L-B*(c+s))/2;
  vector<double> U(N),V(N),vs={-100.0,100.0};vector<Event> ev;
  for(int i=0;i<N;i++){U[i]=c*X[i]+s*Y[i];V[i]=-s*X[i]+c*Y[i];vs.push_back(V[i]-B/2);vs.push_back(V[i]+B/2);ev.push_back({U[i]-B/2,i,1});ev.push_back({U[i]+B/2,i,-1});}
  sort(vs.begin(),vs.end());vector<double> uniq;for(double v:vs)if(uniq.empty()||v-uniq.back()>1e-12)uniq.push_back(v);vs.swap(uniq);sort(ev.begin(),ev.end());
  vector<int> lo(N),hi(N);for(int i=0;i<N;i++){lo[i]=lower_bound(vs.begin(),vs.end(),V[i]-B/2-1e-12)-vs.begin();hi[i]=lower_bound(vs.begin(),vs.end(),V[i]+B/2-1e-12)-vs.begin();}
  Seg seg(vs.size()-1);vector<char> active(N,0); double best=1e100;
  struct Candidate {double mass=1e100, umid=0; int cell=-1;};
  vector<Candidate> candidates(128);
  for(int j=0;j<(int)ev.size();){int end=j+1;while(end<(int)ev.size()&&ev[end].u-ev[j].u<1e-12)end++;
   for(int z=j;z<end;z++){int i=ev[z].i;seg.add(lo[i],hi[i],ev[z].sgn*W[i]);active[i]=(ev[z].sgn==1);}
   if(end==(int)ev.size())break;
   double a=max(ev[end-1].u,-H*(c+s)),b=min(ev[end].u,H*(c+s)); j=end;
   if(b-a<1e-12)continue;
   double vl,vh;
   if(s<1e-15){vl=-H;vh=H;}else{
    double ua=min(b,max(a,H*(c-s))),ub=min(b,max(a,-H*(c-s)));
    vl=max((c*ua-H)/s,(-H-s*ua)/c);vh=min((c*ub+H)/s,(H-s*ub)/c);
   }
   int l=upper_bound(vs.begin(),vs.end(),vl+1e-12)-vs.begin()-1;
   int r=lower_bound(vs.begin(),vs.end(),vh-1e-12)-vs.begin();
   l=max(l,0);r=min(r,(int)vs.size()-1);if(l>=r)continue;
   auto q=seg.query(l,r);best=min(best,q.first);
   if(q.first<1.0-1e-9){
    double mid=(a+b)/2;
    int bucket=max(0,min(127,int(128*(mid+H*(c+s))/(2*H*(c+s)))));
    if(q.first<candidates[bucket].mass)candidates[bucket]={q.first,mid,q.second};
   }
  }
  vector<pair<double,string>> bad;
  // Delay profile construction until after the sweep. The global minimum is
  // retained, plus one representative per u bucket, instead of constructing
  // an O(N)-length profile at every one of O(N) centre slabs.
  for(auto &p:candidates)if(p.cell>=0){
   string row(nv,0);
   for(int i=0;i<N;i++)if(U[i]-B/2<p.umid&&p.umid<U[i]+B/2&&lo[i]<=p.cell&&p.cell<hi[i])row[ids[i]]++;
   bad.push_back({p.mass,row});
  }
  mins[k]=best;sort(bad.begin(),bad.end());int added=0;
  for(auto &p:bad){if(nr>=cap)break;if(seen.insert(p.second).second){memcpy(out+nr*nv,p.second.data(),nv);nr++;if(++added>=perdir)break;}}
 }
 return nr;
}
