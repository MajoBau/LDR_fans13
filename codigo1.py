import sys
from collections import deque

# Reglas descubiertas con la caja negra:
#  - "estable con tolerancia K": max - min <= K dentro del tramo (igualdad incluida).
#  - Los sensores son CIRCULARES: despues del sensor N sigue el sensor 1.
#  - "?" es comodin: cuenta en la racha y no impone restriccion.
#  - Aritmetica exacta: lecturas y K se pasan a enteros en millonesimas.

def to_micro(t):
    neg = t[:1] == b'-'
    if neg or t[:1] == b'+':
        t = t[1:]
    p = t.find(b'.')
    if p < 0:
        v = int(t) * 1000000
    else:
        ip = t[:p]
        fp = (t[p+1:] + b'000000')[:6]
        v = (int(ip) if ip else 0) * 1000000 + int(fp)
    return -v if neg else v

def solve(n, K, vals):
    if n == 0:
        return 0, 0
    arr = [None if t == b'?' else to_micro(t) for t in vals]
    # Si todo el anillo es estable, la respuesta es N 1.
    nums = [x for x in arr if x is not None]
    if not nums or max(nums) - min(nums) <= K:
        return n, 1
    # Ventana deslizante sobre el arreglo duplicado (longitud < N garantizada).
    dmax = deque(); dmin = deque()
    l = 0
    best, pos = 0, 0
    for r in range(2 * n):
        x = arr[r % n]
        if x is not None:
            while dmax and dmax[-1][0] <= x:
                dmax.pop()
            dmax.append((x, r))
            while dmin and dmin[-1][0] >= x:
                dmin.pop()
            dmin.append((x, r))
            while dmax[0][0] - dmin[0][0] > K:
                l += 1
                if dmax[0][1] < l: dmax.popleft()
                if dmin[0][1] < l: dmin.popleft()
        ln = r - l + 1
        if ln > best:
            best, pos = ln, l % n
        elif ln == best and l % n < pos:
            pos = l % n
    return best, pos + 1

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    T = int(data[idx]); idx += 1
    out = []
    for _ in range(T):
        n = int(data[idx]); idx += 1
        K = to_micro(data[idx]); idx += 1
        vals = data[idx:idx + n]; idx += n
        L, P = solve(n, K, vals)
        out.append("%d %d" % (L, P))
    sys.stdout.write("\n".join(out) + "\n")

main()
