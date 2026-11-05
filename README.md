# Simple Python Calculator

A minimal calculator project demonstrating a class-based Python module.

## Files

- `calculator.py` — calculator module with a `Calculator` class
- `main.py` — demo script that uses the calculator module

## Development Setup

Requires Python 3.12 or newer. From the project root (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

## Usage

Run the demo:

```bash
python main.py
```

Expected output:

```
10 + 4 = 14
10 - 4 = 6
10 * 4 = 40
10 / 4 = 2.5
```

## Calculator Methods

| Method                    | Description                    |
|---------------------------|--------------------------------|
| `calculator.add(a, b)`      | Returns the sum of a and b     |
| `calculator.subtract(a, b)` | Returns a minus b              |
| `calculator.multiply(a, b)` | Returns the product of a and b |
| `calculator.divide(a, b)`   | Returns a divided by b        |

> **Note:** `divide` raises a `ZeroDivisionError` with the message `"Cannot divide by zero"` when `b` is `0`.
