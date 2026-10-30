# Statistical Physics -- Lab 1: Microstates of a System of Coins

Team: <names, NIAs, GitHub users>      Group: <X>      N = 100 + M = <fill in>

Empty project skeleton following the project guidelines. Every function raises
`NotImplementedError` until your team writes it. Work item by item:

| Item | Implement in | Run from `main.py` section | Report section |
|---|---|---|---|
| 1a N = 7 enumeration | `src/microstates.py` | `part1a` | 3.1 |
| 1b largest enumerable N | `src/microstates.py` | `part1b` | 3.2 |
| 1c distributions N = 20,50,80,100 | `src/combinatorics.py`, `src/plots.py` | `part1c` | 3.3 |
| 1d largest N for the distribution | `src/combinatorics.py` | `part1d` | 3.4 |
| 1e thermodynamic limit | `src/thermodynamics.py` | `part1e` | 3.5 |
| 2a-d probabilities | `src/combinatorics.py` | `part2_prob` | 4.1 |
| 2e-g entropy | `src/thermodynamics.py` | `part2_entropy` | 4.2 |
| 2h-j implications | `src/thermodynamics.py` | `part2_implications` | 4.3 |
| 2k N -> 1e23 | `src/thermodynamics.py` | `part2_large_n` | 4.4 |

## Setup
```bash
conda env create -f environment.yml && conda activate statphys_lab1
pytest -q            # tests are skipped until you write them
python main.py       # prints TODO for every unfinished section
```
Git rules: see `docs/GIT_WORKFLOW.md` (feature branches, reviewed PRs, tag `v1.0`).
Log every AI query in `AI_STATEMENT.md`.
