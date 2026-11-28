# Dense-grid simulation: keep the desktop gallery bottom edge straight (Raz 2026-11-28).
def pack(bigs, cols):
    cells={}; top=0; pos=[]
    for b in bigs:
        w=h=2 if b else 1
        while all((top,c) in cells for c in range(cols)): top+=1
        r=top
        while True:
            hit=None
            for c in range(cols-w+1):
                if all((r+y,c+x) not in cells for y in range(h) for x in range(w)): hit=(r,c);break
            if hit: break
            r+=1
        r,c=hit
        for y in range(h):
            for x in range(w): cells[(r+y,c+x)]=len(pos)
        pos.append((r,c,w))
    R=max(r for r,c in cells)+1
    holes=[(r,c) for r in range(R) for c in range(cols) if (r,c) not in cells]
    return R,holes,pos

def flatten(bigs, cols, tail=48, can_big=None):
    """Toggle as few big flags as possible near the end so dense packing leaves no holes (straight bottom edge)."""
    import itertools
    bigs=list(bigs); n=len(bigs)
    can_big = can_big or (lambda i: True)
    if not pack(bigs,cols)[1]: return bigs
    idx=[i for i in range(max(0,n-tail),n) if bigs[i] or can_big(i)]
    for k in (1,2,3):
        best=None
        for combo in itertools.combinations(reversed(idx),k):
            t=bigs[:]
            for i in combo: t[i]=not t[i]
            if not pack(t,cols)[1]:
                score=(sum(1 for i in combo if not bigs[i]), -min(combo))
                if best is None or score<best[0]: best=(score,t)
        if best: return best[1]
    raise AssertionError("cannot flatten")
