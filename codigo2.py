import sys, heapq

# Reglas descubiertas con la caja negra:
#  - Cada orden PRINT (imprima o no) suma +1 a la prioridad de todos los pendientes.
#    => prioridad efectiva = p + (PRINTs desde el ADD) ; ordenar por p - prints_al_agregar.
#  - Empate de prioridad efectiva: gana el que fue "tocado" antes (ADD o último BOOST).
#  - BOOST suma x y mueve el trabajo al final de su nivel (reinicia su marca de tiempo),
#    pero NO reinicia el envejecimiento acumulado.

def main():
    inp = sys.stdin.buffer
    first = inp.readline()
    while first and not first.strip():
        first = inp.readline()
    if not first:
        return
    q = int(first)
    SH = 1 << 21          # > 2*10^6 (ids) y > 10^6 (marcas de tiempo)
    MASK = SH - 1
    MAXID = 2000001
    base = [0] * MAXID    # p - prints_al_agregar (+ boosts)
    cur = [0] * MAXID     # clave vigente (0 = no pendiente; una clave nunca es 0)
    h = []
    push = heapq.heappush; pop = heapq.heappop
    out = []
    prints = 0
    t = 0
    while t < q:
        line = inp.readline()
        if not line:
            break
        w = line.split()
        if not w:
            continue
        op = w[0]
        if op == b'ADD':
            j = int(w[1]); b = int(w[2]) - prints
            base[j] = b
            k = ((-b) * SH + t) * SH + j
            cur[j] = k; push(h, k)
        elif op == b'BOOST':
            j = int(w[1])
            if cur[j]:
                b = base[j] + int(w[2]); base[j] = b
                k = ((-b) * SH + t) * SH + j
                cur[j] = k; push(h, k)
                out.append('OK')
            else:
                out.append('NO')
        elif op == b'CANCEL':
            j = int(w[1])
            if cur[j]:
                cur[j] = 0; out.append('OK')
            else:
                out.append('NO')
        else:  # PRINT
            k = int(w[1])
            res = []
            while h and len(res) < k:
                e = pop(h); j = e & MASK
                if cur[j] == e:
                    cur[j] = 0; res.append(str(j))
            out.append(' '.join(res) if res else 'VACIA')
            prints += 1
        t += 1
    sys.stdout.write('\n'.join(out) + ('\n' if out else ''))

main()
