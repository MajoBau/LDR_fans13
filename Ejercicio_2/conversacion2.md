# Conversación con la IA — Ejercicio 2 (Impresora con prioridades)

Equipo: LDR_fans13
IA: Claude (Anthropic)

---

## Usuario

Eres un programador competitivo experto (nivel ICPC). Resuelve el siguiente problema.

LENGUAJE: Python

ENUNCIADO:
Una impresora recibe trabajos con prioridad y procesa Q órdenes en orden:
- ADD id p: agrega el trabajo id con prioridad p (los id nunca se repiten en ADD). No imprime nada.
- BOOST id x: si el trabajo está pendiente, su prioridad sube x e imprime OK; si no, NO.
- CANCEL id: si está pendiente, lo elimina e imprime OK; si no, NO.
- PRINT k: imprime, en una línea separados por espacio, hasta k trabajos pendientes, de mayor a menor prioridad, y los elimina. Si no hay ninguno imprime VACIA.

Lo que debes descubrir con la caja negra: cómo desempata la impresora cuando dos trabajos tienen la misma prioridad, si BOOST cambia algo más que la prioridad, y si las prioridades cambian con el tiempo.

Entrada: línea 1: Q. Luego Q líneas, una orden cada una.
Salida: una línea por cada BOOST, CANCEL y PRINT.

Ejemplo 1 — Entrada:
```
17
ADD 8 4
CANCEL 8
PRINT 2
PRINT 2
PRINT 1
BOOST 8 1
ADD 12 2
PRINT 1
PRINT 1
ADD 26 4
ADD 13 3
CANCEL 21
PRINT 3
BOOST 26 1
ADD 15 3
BOOST 13 1000000000000000000
BOOST 26 1000000000000000000
```
Salida:
```
OK
VACIA
VACIA
VACIA
NO
12
VACIA
NO
26 13
NO
NO
NO
```

Ejemplo 2 — Entrada:
```
18
ADD 21 1
BOOST 21 1000000000000000000
CANCEL 1
PRINT 1
ADD 9 1
BOOST 9 3
PRINT 1000000
BOOST 9 2
PRINT 2
PRINT 1000000
BOOST 9 1
ADD 28 1
PRINT 1
BOOST 21 1000000000000000000
ADD 2 4
ADD 1 2
CANCEL 28
PRINT 3
```
Salida:
```
OK
NO
21
OK
9
NO
VACIA
VACIA
NO
28
NO
NO
2 1
```

RESTRICCIONES: Q ≤ 10^6; 1 ≤ id ≤ 2·10^6; 1 ≤ p ≤ 10^9; 1 ≤ x ≤ 10^18; 1 ≤ k ≤ 10^6. Tiempo / memoria: 10 s / 256 MB.

REQUISITOS DEL CÓDIGO: stdin/stdout exacto, I/O rápido (sys.stdin.buffer), enteros de 64 bits, casos límite, sin recursión profunda.

ENTREGA: 1. Idea del algoritmo en 3–5 líneas y complejidad. 2. Código completo en un solo bloque. 3. Traza breve del ejemplo 1.

---

## IA (Claude)

El código da exactamente la salida esperada en los dos ejemplos y procesa 10⁶ órdenes aleatorias en unos 2 s (límite 10 s).

Los ejemplos no muestran las tres reglas ocultas: nunca hay empate de prioridad pendiente, y ningún BOOST con OK cambia el orden respecto a otro trabajo. Por eso el código **supone** lo siguiente, con una bandera para cada regla:
- **Desempate:** gana el que llegó primero (FIFO). Si es por id menor: `TIE_BY_ID = True`.
- **BOOST:** solo cambia la prioridad. Si además manda el trabajo al final de su nivel: `BOOST_RESETS_TIME = True`.
- **Paso del tiempo:** las prioridades no cambian solas. Si hay envejecimiento (+1 por orden en espera): `AGING = True` (basta ordenar por `p − llegada`).

### 1. Idea del algoritmo
- Min-heap con borrado perezoso; cada trabajo se codifica en un solo entero `((−p)·2²¹ + desempate)·2²¹ + id`.
- `cur[id]` guarda la clave vigente; BOOST inserta una clave nueva y las viejas o canceladas se descartan al sacarlas.
- PRINT saca del heap hasta juntar k válidos o vaciarlo. Los enteros de Python no se desbordan aunque la prioridad pase de 10¹⁸.
- **Complejidad:** O(Q log Q) tiempo, O(Q) memoria; cada entrada entra y sale una sola vez aunque k sea grande.

### 2. Código
Ver `codigo2.py` en esta carpeta.

### 3. Traza del ejemplo 1
| Orden | Estado pendiente | Salida |
|---|---|---|
| ADD 8 4 / CANCEL 8 | {} | OK |
| PRINT 2, PRINT 2, PRINT 1 | entrada muerta de 8 se descarta | VACIA ×3 |
| BOOST 8 1 | 8 no está pendiente | NO |
| ADD 12 2 / PRINT 1 | {12:2} → sale 12 | 12 |
| PRINT 1 | {} | VACIA |
| ADD 26 4, ADD 13 3 / CANCEL 21 | {26:4, 13:3}; 21 nunca existió | NO |
| PRINT 3 | salen 26 y 13 | 26 13 |
| BOOST 26 1 | ya se imprimió | NO |
| ADD 15 3 / BOOST 13 10¹⁸ | ya se imprimió | NO |
| BOOST 26 10¹⁸ | ya se imprimió | NO |

Pruebas propuestas para la caja negra:
- **Desempate:** `ADD 5 1, ADD 3 1, PRINT 2` → `5 3` = FIFO; `3 5` = por id.
- **BOOST:** `ADD 1 1, ADD 2 2, BOOST 1 1, PRINT 2` → si sale `1 2`, activar `BOOST_RESETS_TIME`.
- **Envejecimiento:** separar dos ADD con órdenes de relleno y ver si el más antiguo gana pese a menor prioridad.

---

## Usuario

(Adjunta `Ronda1_Basica.zip` con la caja negra de cada problema) haz todas las pruebas necesarias

---

## IA (Claude) — Pruebas con la caja negra (B2/caja_linux)

Primero comprobé que la caja reproduce los dos ejemplos (OK). Luego, pruebas dirigidas:

**Desempate**
| Entrada | Caja | Conclusión |
|---|---|---|
| `ADD 5 1, ADD 3 1, PRINT 2` | `5 3` | No es por id menor |
| `ADD 3 1, ADD 5 1, PRINT 2` | `3 5` | Gana el que llegó primero |

**BOOST**
| Entrada | Caja | Conclusión |
|---|---|---|
| `ADD 1 1, ADD 2 2, BOOST 1 1, PRINT 2` | `2 1` | El trabajo con BOOST pierde el empate |
| `ADD 2 1, ADD 1 2, BOOST 2 1, PRINT 2` | `1 2` | Igual, aunque haya llegado antes |
| `ADD 1 1, ADD 2 2, BOOST 1 1, ADD 3 2, PRINT 3` | `2 1 3` | BOOST le pone como marca de tiempo el momento del BOOST: queda detrás del 2 pero delante del 3 |

**Envejecimiento**
- `ADD 1 1`, 100 × `CANCEL 99`, `ADD 2 2`, `PRINT 2` → `2 1`: las órdenes que no son PRINT no envejecen.
- `ADD 1 1`, 11 trabajos de prioridad 100 impresos con 11 × `PRINT 1`, `ADD 2 3`, `PRINT 2` → `1 2`: **sí hay envejecimiento**.
- Barrido con m órdenes `PRINT 1` y luego `ADD 2 p2`: el 2 gana solo si `p2 > 1 + m` (m=1→3, m=2→4, m=3→5, m=4→6, m=6→8). Con `p2 = 1 + m` gana el 1 (empate → el más antiguo).
- Con una sola orden `PRINT m` (imprime m trabajos) el umbral siempre es `p2 > 2`: **cuenta cada orden PRINT, no cada trabajo impreso**.
- `PRINT 1, PRINT 1` con la cola vacía y luego `ADD 1 1, ADD 2 p2`: no afecta a trabajos que aún no existían.
- 3 PRINT, luego `BOOST 1 1`, `ADD 2 p2`: el 2 gana solo si `p2 > 5`, así que BOOST **conserva** el envejecimiento acumulado.

### Reglas descubiertas
- Cada orden **PRINT suma +1** a la prioridad de todos los trabajos que siguen pendientes.
- Empate → gana el que se tocó antes (ADD o último BOOST).
- BOOST suma x y mueve el trabajo al final de su nivel, sin reiniciar el envejecimiento.

### Cambio de algoritmo
- Prioridad efectiva = `p + (PRINTs desde su ADD)`. Entre pendientes basta ordenar por `base = p − PRINTs_al_hacer_ADD` (BOOST suma a `base`).
- Min-heap con clave entera `((−base)·2²¹ + tiempo)·2²¹ + id` y borrado perezoso (`cur[id]` = clave vigente).
- Primera versión: 314 MB en el peor caso (más de 256 MB). Se cambió a lectura por líneas y listas indexadas por id → **118 MB**.
- Complejidad: O(Q log Q) tiempo, O(Q) memoria.

El código final está en `codigo2.py`.

---

## Verificación ejecutada

- Ejemplos 1 y 2: salida idéntica.
- **Prueba diferencial contra la caja negra:** 5000 entradas aleatorias (prioridades pequeñas para forzar empates, BOOST de hasta 10¹⁸, ids inexistentes, PRINT con k grande) → **0 diferencias**.
- Rendimiento con Q = 10⁶: 1.6–2.5 s, máximo 118 MB (límite 10 s / 256 MB).

## Lo que descubrimos (resumen)

1. Desempate: gana el más antiguo (por llegada o por su último BOOST).
2. BOOST mueve el trabajo al final de su nivel de prioridad.
3. Cada orden PRINT envejece +1 a todos los pendientes.
