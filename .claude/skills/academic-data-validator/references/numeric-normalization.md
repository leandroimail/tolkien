# Numeric Normalization Rules

How `extract_numeric_inventory.py` turns raw tokens into comparable values so the
reconciliation worksheet can cluster numbers that *mean* the same thing.

## Token kinds

| Kind | Example | Notes |
|------|---------|-------|
| `int` | `798`, `4701` | integer value |
| `float` | `0.80`, `12.5` | decimal value |
| `percent` | `92%`, `0,80 %` | value of the number; unit recorded as `%` |
| `ratio` | `30/75`, `442/450` | stores `numerator`, `denominator`, and the quotient as `value` |
| `year` | `2023` | 1900–2099 integers; **excluded** from clustering to reduce noise |
| `word-int` | `eleven`, `six`, `dois` | mapped to a digit value (EN + common PT-BR) |

## Word → digit

Supported: zero–twenty, the tens (thirty…ninety), hundred, thousand; plus common
PT-BR forms (um/uma, dois/duas, três…doze). `eleven` ≡ `11`, `six` ≡ `6`.

## Locale & separators

Both separators present → the **last** one is the decimal separator:
`4.701,5` → `4701.5`; `4,701.5` → `4701.5`.

Only comma present:
- `1,000` (one group of exactly 3 digits, short integer part) → thousands → `1000`.
- `0,80` → decimal → `0.80`.

Only dot present: standard decimal, except `4.701` is treated as `4701` when it
looks like a thousands group — verify ambiguous cases in the worksheet.

## Percentages

`92%` → value `92.0`, unit `%`. Percentage columns in tables are expected to sum to
~100 (±1) unless a Total row is present.

## Rounding / precision tolerance

- Clustering key rounds to 4 decimals.
- **Precision-variance warning**: two distinct cluster values within **2% relative**
  of each other are flagged as possibly the same quantity stated with different
  rounding (e.g., `0.80` vs `0.798`). The reviewer adjudicates.

## What is intentionally NOT asserted

The script never claims two numbers are the **same quantity** — only that they share
a value (a *candidate* cluster). Semantic identity ("the 798 in the abstract is the
same 798 as in Results") is decided in the agentic pass. This avoids false gates.
