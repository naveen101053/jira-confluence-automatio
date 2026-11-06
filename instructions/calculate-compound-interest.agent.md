- Use `tools/compound_interest.py` when asked to calculate compound interest, future value of a deposit/investment, or interest earned.
  + Do not compute by hand or mental math — always run the tool.
  + Do not use for simple interest, loan amortization, or recurring contributions — the tool does not support them.
- Required inputs (ask the user if any is missing, do not guess):
  + principal — initial amount, `>= 0`.
  + annual rate — percent, not a fraction (`7.34` for 7.34%).
  + compounds per year — positive integer (`12` monthly, `4` quarterly, `2` semi-annual, `1` annual, `365` daily).
  + total years — number, decimals allowed.
- Convert inputs before invoking:
  + Strip currency symbols and thousands separators (`$15,847` → `15847`).
  + Convert years and months to years as `years + months/12`; pass the exact fraction (e.g. `(8 + 7/12)`), not a rounded value, to avoid cent-level drift.
- Invoke with positional arguments in this order:
  + `python tools/compound_interest.py <principal> <annual_rate_percent> <compounds_per_year> <years>`
  + Example: `python tools/compound_interest.py 15847 7.34 12 8.583333333333334`
  + PowerShell: arguments can be expressions, e.g. `python tools/compound_interest.py 15847 7.34 12 (103/12)`.
  + Use `python tools/compound_interest.py -h` to show usage.
- Tool output format:
  + `Final amount:    29,697.95`
  + `Interest earned: 13,850.95`
- If the tool exits with an argument error (negative value, zero compounds per year, non-numeric input), fix the inputs and rerun — do not fall back to manual calculation.
- Present results:
  + State the inputs used: principal, annual rate, compounding frequency, term (e.g. `8 years 7 months = 103 months`).
  + Show the formula: `A = P(1 + r/n)^(nt)`.
  + Show **Final amount** and **Total interest** in bold, as reported by the tool, rounded to 2 decimals, with currency symbol.
  + Note assumptions, e.g. partial years compound at the same frequency.
  + Keep the answer concise — no restating of the tool's raw output beyond the two figures.
