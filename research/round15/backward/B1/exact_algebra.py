"""Independent exact rational quaternion and fundamental index algebra."""
from fractions import Fraction as Q
from collections import defaultdict
from math import comb


def multiply(a,b):
    a0,a1,a2,a3=a;b0,b1,b2,b3=b
    return (a0*b0-a1*b1-a2*b2-a3*b3,
      a0*b1+a1*b0+a2*b3-a3*b2,
      a0*b2-a1*b3+a2*b0+a3*b1,
      a0*b3+a1*b2-a2*b1+a3*b0)


def inverse(q):return (q[0],-q[1],-q[2],-q[3])


def rational_unit(seed):
    t=(Q(seed+1,3),Q(2*seed+1,5),Q(3*seed+2,7))
    norm=sum(x*x for x in t);den=1+norm
    result=((1-norm)/den,*(2*x/den for x in t))
    if sum(x*x for x in result)!=1:raise ValueError('unit quaternion construction failed')
    return result


def trace_word(word,links):
    out=(Q(1),Q(0),Q(0),Q(0))
    for edge,sign in word:
        if type(sign) is not int or sign not in(-1,1):raise ValueError('strict oriented link sign required')
        out=multiply(out,links[edge] if sign==1 else inverse(links[edge]))
    return out[0]


def reversed_word(word):return [(edge,-sign) for edge,sign in reversed(word)]


def gauge_links(edges,links,gauges):
    return {name:multiply(multiply(gauges[tail],links[name]),inverse(gauges[head]))
            for name,(tail,head) in edges.items()}


def contract_distinct_faces(words,selected):
    """Expand actual face indices, integrate each edge U/conjugate(U) pair."""
    if type(selected) is not tuple or len(set(selected))!=len(selected):
        raise ValueError('distinct selected face tuple required')
    occurrences=defaultdict(list);parent={}
    def find(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]];v=parent[v]
        return v
    def join(a,b):parent[find(a)]=find(b)
    for face in selected:
        word=words[face];length=len(word)
        for i in range(length):parent[(face,i)]=(face,i)
        for i,(edge,sign) in enumerate(word):
            before=(face,i);after=(face,(i+1)%length)
            # U^-1_ij=conjugate(U_ji), while positive occurrence is U_ij.
            occurrences[edge].append((sign,before,after) if sign==1 else(sign,after,before))
    if not selected:return {'value':Q(1),'color_loops':0,'paired_edges':0,'single_edge':None}
    single=next((edge for edge,items in occurrences.items() if len(items)==1),None)
    if single is not None:return {'value':Q(0),'color_loops':None,'paired_edges':None,'single_edge':single}
    for edge,items in occurrences.items():
        if len(items)!=2 or sorted(item[0] for item in items)!=[-1,1]:
            raise ValueError('edge contraction requires the declared opposite orientation pairing')
        (_,a,b),(_,c,d)=items;join(a,c);join(b,d)
    loops=len({find(v) for v in parent})
    return {'value':Q(2)**loops/Q(2)**(len(occurrences)+len(selected)),
            'color_loops':loops,'paired_edges':len(occurrences),'single_edge':None}


def one_haar(power):
    if type(power) is not int or power<0:raise ValueError('nonnegative strict integer degree required')
    if power%2:return Q(0)
    n=power//2;return Q(comb(2*n,n),(n+1)*4**n)


def missing_face_moment(powers):
    if len(powers)!=6 or any(type(n) is not int or n<0 for n in powers):
        raise ValueError('six nonnegative integer powers required')
    if not any(n==0 for n in powers):
        raise ValueError('missing-face factorization premise absent')
    out=Q(1)
    for n in powers:out*=one_haar(n)
    return out
