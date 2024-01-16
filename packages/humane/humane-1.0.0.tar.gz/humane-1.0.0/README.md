# Humane

A collection of human-readable identifiers / hashes.

## Usage

```bash
pip install humane==1.0.0

humane id 1234567890
```

```python
from humane import human_id

x = human_id(1234567890)
```

## What humane identifiers are available?

### `human id`

- `<N>-<adjective>-<animal>-<verb>-<adverb>`
- Examples:
    - `5-proud-weasels-warn-knowledgeably`
    - `4-legal-shrews-check-sternly`
    - `9-perfect-monkeys-jam-justly <=> humane`

### `humane id --short`

- `<N>-<adjective>-<animal>`
- Examples:
    - `4-afraid-seahorses`
    - `7-clever-weasels`
    - `9-perfect-monkeys <=> humane`