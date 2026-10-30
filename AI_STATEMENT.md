# AI collaboration statement

Team: <names>

Policy: AI output is a draft; every AI-generated function is covered by unit tests and every
member can explain it.

| # | Date | Member | Tool | Purpose |
|---|---|---|---|---|
| 1 |  |  |  |  |

## Entry 1
* **Prompt:**
* **Output (summary / paste):**
* **Problems found and how we resolved them:**
* **Modifications made by the team:**
* **Verification (tests, checks):**
## Entry 2
* **Date:** 2026-10-30
* **Member:** Saulo
* **Tool:** Gemini
* **Purpose:** Prototyping probability calculations for Part 2a-2d and modularizing into project structure.
* **Prompt:** "Generate code for probability calculations with team NIA digits [14, 75, 92, 99] and extrapolate to VS Code setup."
* **Output Summary:** Calculated M=43 (harmonic mean of digits) and system size N=143. Computed P(k=30), P(k=N/2), and cumulative probabilities ΔP.
* **Modifications Made by Team:** Modularized script into `src/combinatorics.py`, added wrapper `print_probability_report`, and linked default digits in `main.py`.
* **Verification:** Unit tests written in `tests/test_combinatorics.py` checking system size calculation and normalization condition sum(P_k) = 1.
## Entry 3
* **Date:** 2026-10-30
* **Member:** Saulo
* **Tool:** Gemini
* **Purpose:** Refactoring probability calculations into template signatures in `src/combinatorics.py`.
* **Prompt:** "Adapt probability logic to pre-defined function stubs in combinatorics.py."
* **Output Summary:** Implemented `harmonic_mean_M`, `ln_omega`, `prob`, `cumulative_prob`, `prob_array`, and `largest_N_with_float_omega`.
* **Modifications Made by Team:** Integrated log-gamma calculation `math.lgamma` to avoid numerical overflow when computing $P_k$ for $N > 100$.
* **Verification:** Unit tests written in `tests/test_combinatorics.py` verifying harmonic mean calculation and probability array normalization $\sum P_k = 1.0$.
## Entry 4
* **Date:** 2026-10-30
* **Member:** Saulo
* **Tool:** Gemini
* **Purpose:** Writing pytest suite for `tests/test_combinatorics.py`.
* **Prompt:** "Complete unit tests for combinatorics.py covering exact log-space match, symmetry, normalization, harmonic mean, and invalid input checks."
* **Output Summary:** Replaced pytest skips with active assertions testing log-space probability conversion, binomial symmetry, cumulative sum normalization, and zero-digit edge cases. Added input range check in `src/combinatorics.py`.
* **Modifications Made by Team:** Integrated `pytest.raises(ValueError)` check for $k < 0$ and $k > N$.
* **Verification:** `pytest` executed in terminal with all tests passing cleanly.
<<<<<<< HEAD
=======
## Entry 5
* **Date:** 2026-10-30
* **Member:** Saulo
* **Tool:** Gemini
* **Purpose:** Extrapolating Sections 2e-2k (Entropy changes, waiting times, likelihood ratios, Gaussian approximation, and Large-N limit) into project modules.
* **Prompt:** "Extrapolate thermodynamics code (2e-2k) into src/thermodynamics.py, tests/test_thermodynamics.py, main.py, and update AI_STATEMENT.md."
* **Output Summary:** Implemented `delta_S_over_kB`, `expected_waiting_time`, `likelihood_ratio`, `gauss_prob`, and `large_N_summary`. Evaluated likelihood ratios for $M \pm 10$ ($53$ and $33$ heads) and validated Gaussian accuracy at $N=143$.
* **Modifications Made by Team:** Handled log-space conversions for waiting time $t$ to avoid numerical overflow during $2^{143}$ calculations.
* **Verification:** `pytest` executed with 100% passing tests for entropy maximality, inverse waiting time scaling, and Gaussian approximation accuracy.
## Entry 6
* **Date:** 2026-10-30
* **Member:** Saulo
* **Tool:** Gemini
* **Purpose:** Extrapolating Sections 2e-2k (Entropy changes, waiting times, likelihood ratios, Gaussian approximation, and Large-N limit) into project modules.
* **Prompt:** "Extrapolate thermodynamics code (2e-2k) into src/thermodynamics.py, tests/test_thermodynamics.py, main.py, and update AI_STATEMENT.md."
* **Output Summary:** Implemented `delta_S_over_kB`, `expected_waiting_time`, `likelihood_ratio`, `gauss_prob`, and `large_N_summary`. Evaluated likelihood ratios for $M \pm 10$ ($53$ and $33$ heads) and validated Gaussian accuracy at $N=143$.
* **Modifications Made by Team:** Handled log-space conversions for waiting time $t$ to avoid numerical overflow during $2^{143}$ calculations.
* **Verification:** `pytest` executed with 100% passing tests for entropy maximality, inverse waiting time scaling, and Gaussian approximation accuracy.
>>>>>>> eac8442 (Update combinatorics and thermodynamics modules and tests for N=138 baseline)
