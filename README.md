# Proyecto 3 — Simulador de Máquinas de Turing

Simulador de Máquinas de Turing (MT) de una cinta. Lee la descripción formal de la MT desde un archivo YAML, simula cada cadena de `inputs`, muestra la lista completa de descripciones instantáneas (IDs), la configuración final de la cinta y si la cadena fue aceptada o rechazada.

Video: (pendiente — enlace de YouTube no listado)

## Requisitos

- Python 3.10 o superior
- PyYAML

```powershell
py -m pip install -r requirements.txt
```

## Ejecución

Desde la raíz del repositorio:

```powershell
py main.py maquinas/reconocedora.yaml
py main.py maquinas/alteradora.yaml
```

Para guardar la salida en un archivo:

```powershell
py main.py maquinas/reconocedora.yaml > salida_reconocedora.txt
```

## Formato del archivo YAML

```yaml
mt:
  states: [q0, q1, qf]
  input_alphabet: [a, b]
  tape_alphabet: [a, b, B, X]
  initial_state: q0
  accept_states: [qf]
  transitions:
    - state: q0
      read: [a, B]     # [símbolo leído en la cinta, caché del estado]
      write: [a, X]    # [nueva caché del estado, símbolo que se escribe]
      move: R          # L, R o S
      next: q1
  inputs:
    - "aab"
```

Cada transición se interpreta como en el enunciado:

`state: q0, read: [a, B], write: [a, X], move: R, next: q1`  ⇒  δ([q0, B], a) = ([q1, a], X, R)

- El estado de la MT es un par `[estado, caché]`; la caché empieza en `B`.
- `B` es el blanco: debe estar en `tape_alphabet` y no en `input_alphabet`.
- Las transiciones también pueden escribirse en una línea: `- {state: q0, read: [a, B], write: [a, X], move: R, next: q1}` (es la misma estructura YAML).
- La MT debe ser determinista: no puede haber dos transiciones con el mismo estado, símbolo leído y caché.

## Salida

Para cada cadena:

```
   0     [q0, B] c a b c a
   1 |-  c [q0, c] a b c a
   2 |-  [q1, a] c c b c a
   ...
  32 |-  [qf, B] a a b c c
Cinta final: aabcc
Resultado: ACEPTADA
Motivo: la MT se detuvo en el estado de aceptacion qf
```

Cada ID tiene la forma `α [q, c] β`: `α` es lo que está a la izquierda de la cabeza, `[q, c]` el estado con su caché, y la cabeza está sobre el primer símbolo de `β`.

- **Aceptada**: la MT se detiene (no hay transición aplicable) en un estado de aceptación.
- **Rechazada**: la MT se detiene en un estado que no es de aceptación, la cadena tiene símbolos fuera del alfabeto de entrada, o la MT no se detiene en 10 000 pasos.

## Arquitectura

```
proyecto3/
├── main.py           # punto de entrada: lee el YAML, simula cada cadena e imprime los resultados
├── lector_yaml.py    # parsing y validación del YAML -> MaquinaTuring
├── maquina.py        # estructuras de datos: Transicion y MaquinaTuring
├── cinta.py          # cinta infinita en ambos sentidos
├── simulador.py      # ciclo de simulación y descripciones instantáneas
├── maquinas/
│   ├── reconocedora.yaml
│   └── alteradora.yaml
└── requirements.txt
```

Flujo: `archivo.yaml → lector_yaml.leer_mt() → MaquinaTuring → simulador.simular(mt, cadena) → Resultado (IDs, cinta final, aceptada) → main.py imprime`.

- **`maquina.py`**: `Transicion` guarda un renglón de δ. `MaquinaTuring` guarda la 7-tupla y un diccionario de transiciones con clave `(estado, símbolo, caché)`, así encontrar la transición de cada paso es una búsqueda directa.
- **`lector_yaml.py`**: carga el YAML con `BaseLoader` (todo se lee como texto, así `0`, `1`, `yes` o `no` no se convierten en números o booleanos) y valida estados, alfabetos, símbolos de cada transición, movimientos y determinismo.
- **`cinta.py`**: la cinta es un diccionario `posición → símbolo` que solo guarda las casillas que no son blanco; la cabeza puede moverse a posiciones negativas sin límite.
- **`simulador.py`**: parte de `[q0, B]` con la cabeza en el primer símbolo. En cada paso busca δ(estado, caché, símbolo leído); si no existe, la MT se detiene y se revisa si el estado es de aceptación. Si existe, escribe, mueve la cabeza, cambia estado y caché, y guarda la nueva ID.

## MT reconocedora: L = { ww | w ∈ {a, b}* }

Archivo: `maquinas/reconocedora.yaml`. No es un lenguaje libre de contexto.

Cinta: `a, b, B, X, Y, U, V, Z`. Estados: `q0 … q8, qf`.

Idea:

1. **Encontrar la mitad (q0–q3)**: marca el primer símbolo sin marcar de la izquierda (`a→X`, `b→Y`), va al final y marca el último sin marcar (`a→U`, `b→V`). Repite. Si la longitud es impar, `q2` encuentra una marca `X/Y` y no hay transición: rechaza. Al terminar, `X/Y` es la primera mitad y `U/V` la segunda.
2. **Regresar al inicio (q4)**.
3. **Comparar (q5–q8)**: `q5` toma el primer `X/Y`, lo cambia por `Z` y **guarda la letra en la caché** (`[q6, a]` o `[q6, b]`). `q6` va a la derecha hasta el primer `U/V`; si coincide con la caché lo cambia por `Z`, si no, rechaza. `q7/q8` regresan al siguiente `X/Y`. Si `q5` lee `Z`, todo coincidió: acepta.

| Cadena | Longitud | Resultado |
|---|--:|---|
| `aabaab` | 6 | aceptada (`w = aab`) |
| `abbabb` | 6 | aceptada (`w = abb`) |
| `aabab` | 5 | rechazada (longitud impar) |
| `abbaab` | 6 | rechazada (`abb ≠ aab`) |

Funciones de transición:

| # | δ |
|--:|---|
| 1 | δ([q0, B], a) = ([q1, B], X, R) |
| 2 | δ([q0, B], b) = ([q1, B], Y, R) |
| 3 | δ([q0, B], U) = ([q4, B], U, L) |
| 4 | δ([q0, B], V) = ([q4, B], V, L) |
| 5 | δ([q0, B], B) = ([qf, B], B, S) |
| 6 | δ([q1, B], a) = ([q1, B], a, R) |
| 7 | δ([q1, B], b) = ([q1, B], b, R) |
| 8 | δ([q1, B], U) = ([q2, B], U, L) |
| 9 | δ([q1, B], V) = ([q2, B], V, L) |
| 10 | δ([q1, B], B) = ([q2, B], B, L) |
| 11 | δ([q2, B], a) = ([q3, B], U, L) |
| 12 | δ([q2, B], b) = ([q3, B], V, L) |
| 13 | δ([q3, B], a) = ([q3, B], a, L) |
| 14 | δ([q3, B], b) = ([q3, B], b, L) |
| 15 | δ([q3, B], X) = ([q0, B], X, R) |
| 16 | δ([q3, B], Y) = ([q0, B], Y, R) |
| 17 | δ([q4, B], X) = ([q4, B], X, L) |
| 18 | δ([q4, B], Y) = ([q4, B], Y, L) |
| 19 | δ([q4, B], B) = ([q5, B], B, R) |
| 20 | δ([q5, B], X) = ([q6, a], Z, R) |
| 21 | δ([q5, B], Y) = ([q6, b], Z, R) |
| 22 | δ([q5, B], Z) = ([qf, B], Z, S) |
| 23 | δ([q6, a], X) = ([q6, a], X, R) |
| 24 | δ([q6, a], Y) = ([q6, a], Y, R) |
| 25 | δ([q6, a], Z) = ([q6, a], Z, R) |
| 26 | δ([q6, b], X) = ([q6, b], X, R) |
| 27 | δ([q6, b], Y) = ([q6, b], Y, R) |
| 28 | δ([q6, b], Z) = ([q6, b], Z, R) |
| 29 | δ([q6, a], U) = ([q7, B], Z, L) |
| 30 | δ([q6, b], V) = ([q7, B], Z, L) |
| 31 | δ([q7, B], Z) = ([q7, B], Z, L) |
| 32 | δ([q7, B], X) = ([q8, B], X, L) |
| 33 | δ([q7, B], Y) = ([q8, B], Y, L) |
| 34 | δ([q7, B], B) = ([q5, B], B, R) |
| 35 | δ([q8, B], X) = ([q8, B], X, L) |
| 36 | δ([q8, B], Y) = ([q8, B], Y, L) |
| 37 | δ([q8, B], Z) = ([q5, B], Z, R) |
| 38 | δ([q8, B], B) = ([q5, B], B, R) |

## MT alteradora: ordenar w ∈ {a, b, c}* (ordenamiento por inserción)

Archivo: `maquinas/alteradora.yaml`. Deja en la cinta los mismos símbolos de la entrada, ordenados (`a < b < c`). Implementa ordenamiento por inserción: cada símbolo fuera de lugar se va intercambiando hacia la izquierda hasta su posición, y la caché sirve para cargar el símbolo durante cada intercambio.

Entrada: `a, b, c`. Cinta: `a, b, c, B`. Estados: `q0 … q5, qf`.

| Estado | Qué hace |
|---|---|
| `q0` | Recorre la cinta a la derecha; la caché guarda el símbolo anterior. Si el anterior es menor o igual al actual, sigue. Si es mayor, encontró un par desordenado: escribe el anterior en la casilla actual, guarda el actual en la caché y retrocede. |
| `q1` | Escribe el símbolo de la caché en la casilla de la izquierda (el par quedó intercambiado) y se mueve una casilla más a la izquierda para seguir comparando. |
| `q2` | Compara el vecino de la izquierda con el símbolo que se está insertando (en la caché). Si el vecino es menor o igual, o es blanco, el símbolo ya está en su lugar y regresa a `q0`. Si es mayor, empieza otro intercambio: escribe el símbolo de la caché y carga el vecino. |
| `q3` | Escribe el vecino en la casilla de la derecha y vuelve a cargar en la caché el símbolo que se está insertando. |
| `q4` | Da un paso a la izquierda y regresa a `q2` para la siguiente comparación. |
| `q5` | `q0` llegó al final sin pares desordenados: la cadena está ordenada. Regresa al inicio y acepta en `qf`. |

| Entrada | Cinta final | Caso que muestra |
|---|---|---|
| `cabca` | `aabcc` | la última `a` recorre tres posiciones hacia la izquierda |
| `bcaab` | `aabbc` | dos inserciones largas seguidas |
| `ccbbaa` | `aabbcc` | peor caso: la cadena está al revés |
| `abacbc` | `aabbcc` | casi ordenada: solo dos intercambios |

Funciones de transición:

| # | δ |
|--:|---|
| 1 | δ([q0, B], a) = ([q0, a], a, R) |
| 2 | δ([q0, B], b) = ([q0, b], b, R) |
| 3 | δ([q0, B], c) = ([q0, c], c, R) |
| 4 | δ([q0, a], a) = ([q0, a], a, R) |
| 5 | δ([q0, a], b) = ([q0, b], b, R) |
| 6 | δ([q0, a], c) = ([q0, c], c, R) |
| 7 | δ([q0, b], a) = ([q1, a], b, L) |
| 8 | δ([q0, b], b) = ([q0, b], b, R) |
| 9 | δ([q0, b], c) = ([q0, c], c, R) |
| 10 | δ([q0, c], a) = ([q1, a], c, L) |
| 11 | δ([q0, c], b) = ([q1, b], c, L) |
| 12 | δ([q0, c], c) = ([q0, c], c, R) |
| 13 | δ([q0, B], B) = ([q5, B], B, L) |
| 14 | δ([q0, a], B) = ([q5, B], B, L) |
| 15 | δ([q0, b], B) = ([q5, B], B, L) |
| 16 | δ([q0, c], B) = ([q5, B], B, L) |
| 17 | δ([q1, a], b) = ([q2, a], a, L) |
| 18 | δ([q1, a], c) = ([q2, a], a, L) |
| 19 | δ([q1, b], c) = ([q2, b], b, L) |
| 20 | δ([q2, a], B) = ([q0, B], B, R) |
| 21 | δ([q2, a], a) = ([q0, a], a, R) |
| 22 | δ([q2, a], b) = ([q3, b], a, R) |
| 23 | δ([q2, a], c) = ([q3, c], a, R) |
| 24 | δ([q2, b], B) = ([q0, B], B, R) |
| 25 | δ([q2, b], a) = ([q0, a], a, R) |
| 26 | δ([q2, b], b) = ([q0, b], b, R) |
| 27 | δ([q2, b], c) = ([q3, c], b, R) |
| 28 | δ([q3, b], a) = ([q4, a], b, L) |
| 29 | δ([q3, c], a) = ([q4, a], c, L) |
| 30 | δ([q3, c], b) = ([q4, b], c, L) |
| 31 | δ([q4, a], a) = ([q2, a], a, L) |
| 32 | δ([q4, b], b) = ([q2, b], b, L) |
| 33 | δ([q5, B], a) = ([q5, B], a, L) |
| 34 | δ([q5, B], b) = ([q5, B], b, L) |
| 35 | δ([q5, B], c) = ([q5, B], c, L) |
| 36 | δ([q5, B], B) = ([qf, B], B, R) |
