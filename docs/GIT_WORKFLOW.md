# Git workflow (project guidelines, Phase 2 and 7)

## One-time setup (one team member)
1. Create the GitHub repository `StatPhys_Lab1_GroupX`, add every teammate as collaborator.
2. In *Settings -> Branches* add a rule for `main`: *Require a pull request before merging*
   and *Require approvals (1)*; optionally require the `tests` status check.
3. Push this skeleton:
   ```bash
   git init -b main
   git add . && git commit -m "Initial commit: environment, layout, README"
   git remote add origin git@github.com:<org>/StatPhys_Lab1_GroupX.git
   git push -u origin main
   ```

## Daily work (every member)
```bash
git switch main && git pull
git switch -c feature/<topic>          # e.g. feature/bitwise-enumeration
# ... edit, run `pytest -q` ...
git add <files> && git commit -m "Short imperative message"
git push -u origin feature/<topic>
```
Open a **Pull Request** on GitHub, request a teammate as reviewer, address comments, and merge
(prefer *Create a merge commit* so the branch history stays visible).

## Suggested branches / PRs
| Branch | Content | Suggested owner |
|---|---|---|
| `feature/combinatorics` | `src/combinatorics.py` + tests | member 1 |
| `feature/bitwise-enumeration` | `src/microstates.py` + tests | member 2 |
| `feature/thermodynamics` | `src/thermodynamics.py` + tests | member 3 |
| `feature/figures-and-main` | `src/plots.py`, `src/reporting.py`, `main.py` | member 4 |
| `feature/latex-report` | `report/main.tex` | all (one section each) |
| `feature/ci` | `.github/workflows/tests.yml` | any |

## Delivery (Phase 7)
```bash
git switch main && git pull
pytest -q && python main.py && (cd report && latexmk -pdf main.tex)
git add -A && git commit -m "Final report and results"      # via PR
git tag -a v1.0 -m "Final delivery" && git push origin v1.0
```
Submit the repository URL and `report/main.pdf` to Aula Global.

## Oral defence checklist (Phase 8)
* Be able to run `pytest -q` and `python main.py --quick` on your own laptop.
* Explain the commit log (`git log --oneline --graph`) and your own pull requests.
* Explain: `1 << N`, the generator, `int.bit_count`, the log-gamma formula, why 2^N overflows,
  why the Gaussian appears, why the Second Law is statistical.
