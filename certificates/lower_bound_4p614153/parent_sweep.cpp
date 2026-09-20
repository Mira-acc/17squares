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
#include <sstream>
#include <boost/rational.hpp>
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

using Q=boost::rational<Z>;
static Z gcdz(Z a,Z b){if(a<0)a=-a;if(b<0)b=-b;while(b!=0){Z r=a%b;a=b;b=r;}return a;}
static Z lcmz(const Z&a,const Z&b){return (a/gcdz(a,b))*b;}
static Q qabs(Q q){return q<0?-q:q;}
static string qs(const Q&q){return q.numerator().convert_to<string>()+"/"+q.denominator().convert_to<string>();}
struct Job {Z p,q,bn,bd,rn,rd;};
struct Result {I best;unsigned long long slabs;string line;};
Result check(const vector<Atom>&aa,const Job&job,int index){
 const int N=aa.size();
 Z p=job.p,q=job.q;
 require(q>0&&p>=0&&p<q&&job.bn>0&&job.bd>0&&job.rd>0,"bad rational job");
 Z G=lcmz(lcmz(Z(200000),Z(2)*job.bd),job.rd);
 Z li=Z(461300)*(G/200000),bi=job.bn*(G/(Z(2)*job.bd)),rg=job.rn*(G/job.rd);
 Z C=q*q-p*p,S=2*p*q,R=q*q+p*p;
 require(C>0&&S>=0&&rg*R>=bi*(C+S)&&rg<li,"invalid core/parent envelope");
 Z H=(li-rg)*R,edge=H*(C+S),vertex=H*(C-S),K=R*R*H,half=bi*R*R;
 vector<Z>U(N),V(N),vs;vector<Ev>ev;vs.reserve(2*N+2);ev.reserve(2*N+2);
 vs.push_back(-edge-1);vs.push_back(edge+1);ev.push_back({-edge,-1,0});ev.push_back({edge,-1,0});
 for(int i=0;i<N;i++){
  Z x=(2*aa[i].x-461300)*(G/200000),y=(2*aa[i].y-461300)*(G/200000);
  U[i]=R*(C*x+S*y);V[i]=R*(-S*x+C*y);
  if(aa[i].w>0){vs.push_back(V[i]-half);vs.push_back(V[i]+half);
  ev.push_back({U[i]-half,i,1});ev.push_back({U[i]+half,i,-1});}
 }
 sort(vs.begin(),vs.end());vs.erase(unique(vs.begin(),vs.end()),vs.end());
 sort(ev.begin(),ev.end(),[](const Ev&a,const Ev&b){return a.u<b.u;});
 vector<int>lo(N),hi(N);for(int i=0;i<N;i++){
  lo[i]=lower_bound(vs.begin(),vs.end(),Z(V[i]-half))-vs.begin();
  hi[i]=lower_bound(vs.begin(),vs.end(),Z(V[i]+half))-vs.begin();
 }
 Seg seg(vs.size()-1);I best=numeric_limits<I>::max();unsigned long long slabs=0;
 Z al,ar,bl,br;Rat ml,mh;
 for(size_t j=0;j<ev.size();){size_t end=j+1;while(end<ev.size()&&ev[end].u==ev[j].u)end++;
  for(size_t z=j;z<end;z++)if(ev[z].i>=0){int i=ev[z].i;seg.add(lo[i],hi[i],ev[z].sgn*aa[i].w);}
  if(end==ev.size())break;Z left=max(ev[j].u,Z(-edge)),right=min(ev[end].u,edge);j=end;if(left>=right)continue;
  Rat vl,vh;
  if(S==0){vl={-H*R,1};vh={H*R,1};}else{
   Z ua=min(right,max(left,vertex)),ub=min(right,max(left,Z(-vertex)));
   Rat l1={C*ua-K,S},l2={-K-S*ua,C},h1={C*ub+K,S},h2={K-S*ub,C};
   vl=lt(l1,l2)?l2:l1;vh=lt(h1,h2)?h1:h2;
  }
  require(lt(vl,vh),"degenerate reachable slab");
  int l=upper_r(vs,vl)-1,r=lower_r(vs,vh);require(l>=0&&r<=(int)vs.size()-1&&l<r,"invalid range");
  auto z=seg.get(l,r);if(z.first<best){best=z.first;al=left;ar=right;bl=vs[z.second];br=vs[z.second+1];ml=vl;mh=vh;}
 slabs++;
 }
 require(slabs>0,"no slabs");
 Q vlo=max(Q(bl),Q(ml.a,ml.b)),vhi=min(Q(br),Q(mh.a,mh.b));require(vlo<vhi,"bad witness v");Q v=(vlo+vhi)/2;
 Q ul=max(Q(al),(Q(-K)+Q(S)*v)/Q(C)),ur=min(Q(ar),(Q(K)+Q(S)*v)/Q(C));
 if(S>0){ul=max(ul,(Q(-K)-Q(C)*v)/Q(S));ur=min(ur,(Q(K)-Q(C)*v)/Q(S));}
 require(ul<ur,"bad witness u");Q u=(ul+ur)/2;
 I recount=0;vector<int>captured;for(int i=0;i<N;i++)if(abs(U[i]*u.denominator()-u.numerator())<=half*u.denominator()&&abs(V[i]*v.denominator()-v.numerator())<=half*v.denominator()){recount+=aa[i].w;captured.push_back(i);}
 require(recount==best,"witness membership recount failed");
 Q x=(Q(C)*u-Q(S)*v)/Q(G*R*R*R)+Q(4613,2000),y=(Q(S)*u+Q(C)*v)/Q(G*R*R*R)+Q(4613,2000);
 require(x>Q(job.rn,job.rd)&&x<Q(4613,1000)-Q(job.rn,job.rd)&&y>Q(job.rn,job.rd)&&y<Q(4613,1000)-Q(job.rn,job.rd),"witness outside parent envelope");
 ostringstream out;out<<"{\"index\":"<<index<<",\"minimum_units\":"<<best<<",\"slabs\":"<<slabs<<",\"x\":\""<<qs(x)<<"\",\"y\":\""<<qs(y)<<"\",\"direct_recount\":true}";
 return {best,slabs,out.str()};
}
int main(int argc,char**argv){try{
 require(argc==2,"usage: parent_sweep input.txt");ifstream in(argv[1]);require(bool(in),"cannot open input");
 int N,J;in>>N>>J;require(in&&N>0&&N<100000&&J>0&&J<100000,"invalid dimensions");
 vector<Atom>a(N);map<pair<Z,Z>,I>m;I total=0;
 for(auto&z:a){in>>z.x>>z.y>>z.w;require(in&&z.x>=0&&z.x<=461300&&z.y>=0&&z.y<=461300&&z.w>=0,"bad atom");require(z.w<=1000000000000LL&&total<=1000000000000LL-z.w,"mass overflow");total+=z.w;require(m.emplace(make_pair(z.x,z.y),z.w).second,"duplicate atom");}
 for(auto z:m)for(auto xy:{make_pair(z.first.first,z.first.second),make_pair(z.first.second,z.first.first)})for(int a0=0;a0<2;a0++)for(int b0=0;b0<2;b0++){
  Z x=a0?Z(461300-xy.first):xy.first,y=b0?Z(461300-xy.second):xy.second;auto it=m.find({x,y});require(it!=m.end()&&it->second==z.second,"D4 failure");
 }
 vector<Job>jobs(J);for(auto&j:jobs){in>>j.p>>j.q>>j.bn>>j.bd>>j.rn>>j.rd;require(bool(in),"short jobs");}string extra;require(!(in>>extra),"trailing data");
 vector<Result>results(J);vector<string>errors(J);
 #pragma omp parallel for schedule(dynamic)
 for(int j=0;j<J;j++){try{results[j]=check(a,jobs[j],j);}catch(const exception&e){errors[j]=e.what();}}
 I global=numeric_limits<I>::max();unsigned long long count=0;
 for(int j=0;j<J;j++){require(errors[j].empty(),errors[j].c_str());cout<<results[j].line<<"\n";global=min(global,results[j].best);count+=results[j].slabs;}
 cerr<<"EXACT_SWEEP_COMPLETE atoms "<<N<<" jobs "<<J<<" total_units "<<total<<" minimum_units "<<global<<" slabs "<<count<<"\n";
 return 0;
}catch(const exception&e){cerr<<"REFUSED "<<e.what()<<"\n";return 1;}}
