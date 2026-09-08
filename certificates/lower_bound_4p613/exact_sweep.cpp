// Exact weighted square-cover checker, C++17 + Boost.Multiprecision.
// Geometry: unbounded integers only. No floating-point operations.
#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <vector>
#include <map>
#include <tuple>
#include <iostream>
#include <fstream>
#include <string>
#include <stdexcept>
#include <numeric>
#include <limits>
using namespace std; using Z=boost::multiprecision::cpp_int; using I=long long;
static void require(bool b,const char*m){if(!b)throw runtime_error(m);}
// Two exact accumulation engines share the geometric partition. The direct
// prefix engine is an audit of accumulation, not an independent geometry proof.
#ifdef DIRECT_PREFIX_CHECK
struct Seg {
 vector<I> delta;
 Seg(int n):delta(n+1,0){}
 void add(int l,int r,I v){delta[l]+=v;delta[r]-=v;}
 pair<I,int> get(int l,int r){I sum=0,best=numeric_limits<I>::max();int at=-1;
   for(int i=0;i<r;i++){sum+=delta[i];if(i>=l&&sum<best){best=sum;at=i;}}
   return {best,at};
 }
};
#else
struct Seg {
 int n;vector<I>mn,lazy;vector<int>arg;
 Seg(int z){n=1;while(n<z)n*=2;mn.assign(2*n,0);lazy.assign(2*n,0);arg.resize(2*n);for(int i=0;i<n;i++)arg[n+i]=i;for(int i=n-1;i;i--)arg[i]=arg[2*i];}
 void add(int l,int r,I v,int k,int a,int b){if(l>=b||r<=a)return;if(l<=a&&b<=r){mn[k]+=v;lazy[k]+=v;return;}int m=(a+b)/2;add(l,r,v,2*k,a,m);add(l,r,v,2*k+1,m,b);int j=mn[2*k]<=mn[2*k+1]?2*k:2*k+1;mn[k]=mn[j]+lazy[k];arg[k]=arg[j];}
 void add(int l,int r,I v){if(l<r)add(l,r,v,1,0,n);}
 pair<I,int>get(int l,int r,int k,int a,int b){if(l>=b||r<=a)return {numeric_limits<I>::max()/4,-1};if(l<=a&&b<=r)return {mn[k],arg[k]};int m=(a+b)/2;auto x=get(l,r,2*k,a,m),y=get(l,r,2*k+1,m,b);auto z=x.first<=y.first?x:y;z.first+=lazy[k];return z;}
 pair<I,int>get(int l,int r){return get(l,r,1,0,n);}
};
#endif

struct Rat{Z a,b;};
static bool lt(const Rat&a,const Rat&b){return a.a*b.b<b.a*a.b;}
static int lower_r(const vector<Z>&v,const Rat&r){int a=0,b=v.size();while(a<b){int m=(a+b)/2;if(v[m]*r.b<r.a)a=m+1;else b=m;}return a;}
static int upper_r(const vector<Z>&v,const Rat&r){int a=0,b=v.size();while(a<b){int m=(a+b)/2;if(v[m]*r.b<=r.a)a=m+1;else b=m;}return a;}
struct Atom{Z x,y;I w;};struct Ev{Z u;int i,sgn;};
int main(int argc,char**argv){try{
 require(argc==2,"usage: exact_sweep input.txt");ifstream in(argv[1]);require(bool(in),"cannot read input");
 int N,steps;Z G,li,bi;I wd;in>>N>>steps>>G>>li>>bi>>wd;
 require(bool(in)&&N>0&&N<100000&&steps>0&&steps<=100000,"invalid dimensions");require(G>0&&li>0&&bi>0&&wd>0,"invalid scale");
 vector<Atom>a(N);map<pair<Z,Z>,I>measure;I total=0;
 for(auto &x:a){in>>x.x>>x.y>>x.w;require(bool(in)&&x.w>=0,"invalid atom");require(-li<=x.x&&x.x<=li&&-li<=x.y&&x.y<=li,"atom outside container");require(x.w<=1000000000000LL&&total<=1000000000000LL-x.w,"mass overflow refused");total+=x.w;measure[{x.x,x.y}]+=x.w;}
 string trailing;require(!(in>>trailing),"unexpected trailing input");
 require(Z(total)<Z(17)*wd,"total mass must be strictly less than 17");
 for(auto &x:measure){Z u=x.first.first,v=x.first.second;for(auto xy:{make_pair(u,v),make_pair(v,u)})for(int sx:{-1,1})for(int sy:{-1,1}){auto it=measure.find({sx*xy.first,sy*xy.second});require(it!=measure.end()&&it->second==x.second,"D4 symmetry failed");}}
 // h=207107/(500000*steps), B=2*bi/G.
 Z den=Z(500000)*steps,num=207107;
 require(Z(207107)*207107+Z(2)*207107*500000>=Z(500000)*500000,"direction net misses pi/4");
 require(Z(4)*bi*bi*(den+num)*(den+num)<G*G*(den*den+num*num),"strict angular containment failed");
 I global=numeric_limits<I>::max();unsigned long long slabs_total=0;
 for(int k=0;k<=steps;k++){
  long long p0=207107LL*k,q0=500000LL*steps,g=std::gcd(p0,q0);Z p=p0/g,q=q0/g;
  Z C=q*q-p*p,S=2*p*q,R=q*q+p*p;require(C>0&&S>=0,"unsupported direction");
  Z H=li*R-bi*(C+S);require(H>0,"empty centre domain");Z edge=H*(C+S),vertex=H*(C-S),K=R*R*H,half=bi*R*R;
  vector<Z>U(N),V(N),vs;vector<Ev>ev;vs.reserve(2*N+2);ev.reserve(2*N+2);
  // Sentinels cover the entire reachable v domain, not the atom support.
  vs.push_back(-edge-1);vs.push_back(edge+1);
  ev.push_back({-edge,-1,0});ev.push_back({edge,-1,0});
  for(int i=0;i<N;i++){U[i]=R*(C*a[i].x+S*a[i].y);V[i]=R*(-S*a[i].x+C*a[i].y);vs.push_back(V[i]-half);vs.push_back(V[i]+half);ev.push_back({U[i]-half,i,1});ev.push_back({U[i]+half,i,-1});}
  sort(vs.begin(),vs.end());vs.erase(unique(vs.begin(),vs.end()),vs.end());sort(ev.begin(),ev.end(),[](const Ev&a,const Ev&b){return a.u<b.u;});
  vector<int>lo(N),hi(N);for(int i=0;i<N;i++){lo[i]=lower_bound(vs.begin(),vs.end(),Z(V[i]-half))-vs.begin();hi[i]=lower_bound(vs.begin(),vs.end(),Z(V[i]+half))-vs.begin();}
  Seg seg(vs.size()-1);I best=numeric_limits<I>::max();unsigned long long slabs=0;
  for(size_t j=0;j<ev.size();){size_t end=j+1;while(end<ev.size()&&ev[end].u==ev[j].u)end++;
   for(size_t z=j;z<end;z++)if(ev[z].i>=0){int i=ev[z].i;seg.add(lo[i],hi[i],ev[z].sgn*a[i].w);}
   if(end==ev.size())break;Z left=max(ev[j].u,Z(-edge)),right=min(ev[end].u,edge);j=end;if(left>=right)continue;
   Rat vl,vh;
   if(S==0){vl={-H*R,1};vh={H*R,1};}else{
    Z ua=min(right,max(left,vertex)),ub=min(right,max(left,Z(-vertex)));
    Rat l1={C*ua-K,S},l2={-K-S*ua,C},h1={C*ub+K,S},h2={K-S*ub,C};vl=lt(l1,l2)?l2:l1;vh=lt(h1,h2)?h1:h2;
   }
   require(lt(vl,vh),"degenerate positive-width centre slab");
   int l=upper_r(vs,vl)-1,r=lower_r(vs,vh);require(l>=0&&r<=(int)vs.size()-1&&l<r,"range query invalid");
   auto z=seg.get(l,r);best=min(best,z.first);slabs++;
  }
  require(slabs>0,"no centre slabs visited");global=min(global,best);slabs_total+=slabs;
  cout<<"direction "<<k<<" minimum "<<best<<"/"<<wd<<" slabs "<<slabs<<"\n";
  if(best<wd){cout<<"CERTIFICATE_REFUSED underweight direction "<<k<<"\n";return 2;}
 }
 cout<<"EXACT_CERTIFICATE_VALID atoms "<<N<<" directions "<<steps+1<<" total_mass "<<total<<"/"<<wd<<" minimum "<<global<<"/"<<wd<<" slabs "<<slabs_total<<"\n";
 return 0;
 }catch(const exception&e){cerr<<"CERTIFICATE_REFUSED "<<e.what()<<"\n";return 1;}}
