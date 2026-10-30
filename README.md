# Mixing Matters

**An interactive textbook and practical handbook on mixing in infectious-disease models.**

The audience includes beginners in mathematical epidemiology, infectious-disease researchers, public health practitioners, and community collaborators. The running example uses four fictional activity/partner-meeting groups, but the methods extend to contact matrices, networks, individual-based models, stochastic models, and movement systems.

## Open it

- **Instant preview:** open `index.html` in your browser. All styling, chapter content, and interactive tools use local HTML/CSS/JavaScript files; the website has no runtime dependencies or analytics.
- **GitHub Pages:** create a repository, upload the **contents** of this directory to the repository root, then open **Settings → Pages → Deploy from a branch**, select `main` and `/(root)`. The public address follows the pattern `https://YOUR-USERNAME.github.io/REPOSITORY/`.
- No access to your laptop, account credentials, or remote server is required to examine the files.

## What is inside?

- **15 teaching chapters**, from intuition, strata and partnership opportunities to reciprocity, assortativity, correlated dimensions, empirical estimation, dynamic networks, intervention modeling and AI.
- **Interactive tools**: matrix explorer (`explorer.html`), guided seven-step derivation (`walkthrough.html`), and model-selection decision guide (`decision.html`).
- **Quick references**: printable cheat sheet (`cheatsheet.html`), optional formal derivations (`technical.html`), searchable-by-browser glossary, and bibliography with resolvable DOI links (`references.html`).
- **Reproducible code**: base R and pure Python examples (`code/`), synthetic input data (`data/`), and property checks (`tests/`).
- **Teaching source**: `build_site.py` keeps chapters, bibliography, and site page templates together. It uses `markdown-it-py` and `jinja2` to regenerate the HTML (see `requirements-dev.txt`); regeneration is optional and not needed for hosting.

## Quick validation

```bash
python tests/test_mixing.py
python tests/test_extended.py
python tests/check_site.py   # requires beautifulsoup4
node --check assets/explorer.js
node --check assets/decision.js
node --check assets/walkthrough.js
```

Continuous integration (`.github/workflows/tests.yml`) runs these checks on GitHub. The Python tests check the three constructions on varied opportunity distributions and compare them with a deliberately flawed marginal-kernel product. A successful matrix test validates **internal algebraic properties**, not epidemiological predictions. The numerical models use positive group opportunity counts and assume undirected two-person partnerships unless a lesson explicitly states otherwise.

## Mathematical scope

1. **Joint proportionate mixing:** `M[i,j] = Q[j] / sum(Q)`.
2. **Exact-group preferred mixing:** `M[i,j] = epsilon * I(i==j) + (1-epsilon)*Q[j]/sum(Q)`, `0 <= epsilon <= 1`.
3. **Balanced two-axis affinities:** construct positive symmetric weights `W[i,j] = Q[i]*Q[j]/sum(Q)*exp(theta_r*I(same activity)+theta_m*I(same context))`; find positive `a` so `F[i,j] = a[i]*W[i,j]*a[j]` has row margins `Q`; set `M[i,j] = F[i,j]/Q[i]`. Parameters `theta` are *log-affinities*, not preferred-mixing epsilon values. This is an illustrative teaching construction, not a fitted or uniquely preferred model.

**Important:** `M` is a matrix of destination shares, while `F = diag(Q) M` is a matrix of expected partnership-end flows. For undirected partnerships, check `F[i,j] == F[j,i]` along with row normalization and nonnegativity. This does **not** imply that `M[i,j] == M[j,i]`.

When the activity and context distributions are correlated in the *opportunity* pool, multiplying marginal probabilities fails to recover joint proportionate mixing. When the joint opportunity pool factorizes exactly and each one-axis kernel is reciprocal with respect to its marginal opportunities, a product of those kernels **can** be reciprocal. Those conditions matter.

## Bibliography and intellectual honesty

The site contains a selective teaching bibliography, with verified DOI/publisher links, including Garnett & Anderson (1993), Mossong et al. (2008), Wallinga et al. (2006), Prem et al. (2017), Arregui et al. (2018), Rothblum & Schneider (1989), and network/concurrency/AI resources. Synthetic numerical examples are labeled; the site does not claim the examples are observations from Kenya or another study population.

This is **an educational resource**, not a systematic literature review or a peer-reviewed model. Scientific use requires project-specific empirical checks, uncertainty analysis, and appropriate consultation.

## Project status and future contributions

This release is a substantial, tested teaching edition. Further scholarly development could include a systematic reference audit, annotated implementations for selected empirical datasets, richer accessibility reviews, additional applications, and expert feedback on the more advanced mathematical sections. Findings should be version-controlled and peer reviewed before any claims of a validated epidemiological model.

## Attribution and license

Original site code and prose are released under MIT (see `LICENSE`), excluding third-party scientific articles. The site links to—not reproduces—third-party publications. No user data are embedded in the examples.
