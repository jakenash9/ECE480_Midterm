# ECE480_Midterm
Designing a SAT Solver for ECE 480A4

Process for running:
1) Run the SOP to CNF code using: 
`python cnf.py "SOP function"`
2) Run the SAT solver code using:
`python sat.py`

Notes:
- SOP input boolean function must use literals in the form of xA where A is the Ath number. 
- First literal must start at x1... x0 cannot be used
- AND gate: `.` OR gate: `+` NOT gate: `~`
- If SAT, all combinations of inputs are stored in `output.txt `