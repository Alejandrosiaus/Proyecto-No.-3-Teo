# Proyecto 3 — Simulador de Máquinas de Turing

SiSimulador de Máquinas de Turing de una cinta. Lee la MT desde un archivo YAML, simula cada cadena de `inputs` y muestra las descripciones instantáneas, la cinta final y si la cadena fue aceptada o rechazada.


Video: (https://www.youtube.com/watch?v=2HxMutj4Ryg)

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

- `reconocedora.yaml`: reconoce el lenguaje { ww | w ∈ {a, b}* }.
- `alteradora.yaml`: ordena una cadena sobre {a, b, c} (ordenamiento por inserción).

## Formato del YAML

```yaml
mt:
  states: [q0, q1, qf]
  input_alphabet: [a, b]
  tape_alphabet: [a, b, B]
  initial_state: q0
  accept_states: [qf]
  transitions:
    - state: q0
      read: [a, B]     # [símbolo leído, caché]
      write: [a, b]    # [nueva caché, símbolo a escribir]
      move: R          # L, R o S
      next: q1
  inputs:
    - "aab"
```

`B` es el blanco y la caché empieza en `B`. La transición del ejemplo es δ([q0, B], a) = ([q1, a], b, R).
