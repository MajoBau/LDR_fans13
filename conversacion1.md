# Conversación con la IA — Ejercicio 1 (Racha estable de sensores)

Equipo: LDR_fans13
IA: Claude (Anthropic)

---

## Usuario

Eres un programador competitivo experto (nivel ICPC). Resuelve el siguiente problema.

LENGUAJE: Python

ENUNCIADO:
Una estación tiene N sensores. Cada sensor reporta una lectura decimal (hasta 6 decimales, puede ser negativa) o "?" si la lectura se perdió. Una racha es un tramo de sensores consecutivos que el sistema considera estable con tolerancia K.

Para cada caso, imprime la longitud de la racha más larga y la posición (de 1 a N) donde empieza. Si hay varias, la de menor posición.

Lo que debes descubrir con la caja negra: qué significa exactamente "estable con tolerancia K", qué cuenta como sensores "consecutivos" y qué hace el sistema con las "?".

ENTRADA/SALIDA DE EJEMPLO:
Entrada: línea 1: T. Por caso: una línea N K y una línea con N lecturas (decimal o ?).
Salida: por caso, una línea L P.

Ejemplo 1 — Entrada:
```
3
3 0.500000
-2.5 -2.5 2.5
7 8142465172666.218048
-512039822660.359888 -512039822660.35989 -512039822660.359889 -512039822660.359889 -512039822660.35989 -512039822660.359889 -8654504995326.577938
3 0.500000
1.500000 -1 -1.5
```
Salida:
```
2 1
6 1
2 2
```

Ejemplo 2 — Entrada:
```
2
5 5404369877138.611436
-5118909480930.611125 -5118909480930.611125 -5118909480930.611125 285460396208.000314 285460396208.000314
5 0.0
-7532612242812.331288 -6854978204203.068603 -2730587357333.559605 9000000000000.000000 9000000000000
```
Salida:
```
3 1
2 4
```

RESTRICCIONES: 1 ≤ T ≤ 10^5; suma de N ≤ 10^6; |lectura| ≤ 9·10^12; 0 ≤ K ≤ 1.8·10^13; K y las lecturas tienen hasta 6 decimales. Tiempo / memoria: 8 s / 256 MB.

REQUISITOS DEL CÓDIGO: stdin/stdout exacto, I/O rápido (sys.stdin.buffer), enteros de 64 bits, casos límite (n=0, n=1, máximos, repetidos, negativos), sin recursión profunda.

ENTREGA: 1. Idea del algoritmo en 3–5 líneas y complejidad. 2. Código completo en un solo bloque. 3. Traza breve del ejemplo 1.

---

## IA (Claude)

Analicé los ejemplos sin acceso a la caja negra. Las reglas quedan así:

- **Estable con tolerancia K:** `max − min ≤ K` dentro del tramo, con igualdad incluida. El caso 3 del ejemplo 1 lo muestra: `|−1 − (−1.5)| = 0.5 = K` y la respuesta es `2 2`.
- **Precisión:** el caso 2 del ejemplo 1 y el caso 1 del ejemplo 2 se deciden por 1–3 millonésimas. Ahí `float` falla, así que convierto todo a **enteros en millonésimas**, que dan aritmética exacta.
- **Consecutivos:** posiciones contiguas del arreglo.
- **"?":** los ejemplos no incluyen ninguna, así que es una **suposición sin verificar**: una "?" **corta la racha**. Si la caja negra la trata como comodín, basta poner `WILDCARD = True`. Si no hay racha válida (N=0 o todas "?"), imprimo `0 0`.

### 1. Idea del algoritmo
- Cada lectura se convierte al entero `±(a·10⁶ + b)` (máximo 9·10¹⁸).
- Ventana deslizante `[l, r]` con dos deques monótonos (máximo y mínimo).
- Al agregar `r`, avanzo `l` mientras `max − min > K`. Una "?" reinicia la ventana.
- Solo actualizo con longitud **estrictamente** mayor, así en empate queda la posición menor.
- **Complejidad:** O(suma N) en tiempo y O(N) en memoria.

### 2. Código
Ver `codigo1.py` en esta carpeta.

### 3. Traza del ejemplo 1 (valores en millonésimas)
- **Caso 1** (K = 500000): −2500000, −2500000, 2500000. En r=1 la diferencia es 0 → mejor 2 1. En r=2 la diferencia es 5000000 > K → `l` avanza a 3. Salida **2 1** ✓
- **Caso 2**: las posiciones 1–6 difieren a lo más 2 millonésimas → ventana [1,6]. En r=7 el mínimo es −8654504995326.577938; con el máximo de la posición 1 la diferencia es …666.218050 > K y con el de las posiciones 2..7 es …218049 > K, así que la ventana se reduce a [7,7]. Salida **6 1** ✓ (con `float` saldría mal).
- **Caso 3** (K = 500000): 1500000, −1000000, −1500000. En r=2 la diferencia es 500000 ≤ K → [2,3]. Salida **2 2** ✓

El ejemplo 2 también da `3 1` y `2 4`.

---

## Usuario

(Adjunta `Ronda1_Basica.zip` con la caja negra de cada problema) haz todas las pruebas necesarias

---

## IA (Claude) — Pruebas con la caja negra (B1/caja_linux)

Primero comprobé que la caja reproduce los dos ejemplos del enunciado (OK). Luego hice pruebas dirigidas, una por cada duda del enunciado:

| Prueba (N K / lecturas) | Caja negra | Qué demuestra |
|---|---|---|
| `5 0` / `1 1 ? 1 1` | `5 1` | La `?` no corta la racha |
| `1 0` / `?` | `1 1` | Una `?` sola es racha de longitud 1 |
| `3 0` / `? ? ?` | `3 1` | Solo `?` también es estable |
| `3 0` / `1 ? 2` | `2 1` | La `?` es comodín: se une a cualquier lado, pero 1 y 2 siguen sin poder ir juntos |
| `6 0` / `1 1 ? ? 1 1` | `6 1` | Varias `?` seguidas tampoco cortan |
| `2 1` / `0 1` | `2 1` | Diferencia exactamente K: sí es estable (≤) |
| `2 1` / `0 1.000001` | `1 1` | K + 10⁻⁶ ya no: hace falta aritmética exacta |
| `4 0` / `1 2 3 1` | `2 4` | **Los sensores son circulares**: la racha empieza en 4 y sigue en 1 |
| `3 1` / `0 1 2` | `2 1` | Se compara max − min de todo el tramo, no solo vecinos |
| `2 0` / `-0 0` | `2 1` | `-0` y `0` son iguales |

### Reglas descubiertas
- **Estable con tolerancia K:** `max − min ≤ K` en todo el tramo, igualdad incluida.
- **Consecutivos:** el arreglo es **circular** (después del sensor N viene el 1).
- **`?`:** comodín; cuenta en la longitud y no impone restricción.
- Si todo el anillo es estable, la respuesta es `N 1`.

### Cambio de algoritmo
- Las lecturas y K se pasan a enteros en millonésimas (exacto).
- Si `max − min ≤ K` en todo el anillo, se responde `N 1`.
- Si no, ninguna racha mide N, así que se recorre el arreglo **duplicado** (2N) con una ventana deslizante y dos deques monótonos (máximo y mínimo); las `?` no entran a los deques. Para cada longitud máxima se guarda la menor posición de inicio `l mod N`.
- Complejidad: O(N) por caso, O(suma N) total; memoria O(N).

El código final está en `codigo1.py`.

---

## Verificación ejecutada

- Ejemplos 1 y 2 del enunciado: salida idéntica a la esperada.
- **Prueba diferencial contra la caja negra:** 400 archivos aleatorios (hasta 20 casos cada uno; N hasta 40; enteros, decimales, valores de ±9·10¹², `-0`, muchas `?`, K variados incluido 0 y 1.8·10¹³) → **0 diferencias**.
- Rendimiento con N = 10⁶ (máximo): 2.2 s y 148 MB (límite 8 s / 256 MB).

## Lo que descubrimos (resumen)

1. Estable = `max − min ≤ K` (inclusive), con precisión de 10⁻⁶.
2. Los sensores forman un **círculo**.
3. La `?` es **comodín**.
