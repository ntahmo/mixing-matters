# Contributing to Mixing Matters

Contributions that make the resource scientifically stronger and easier for beginners to understand are welcome.

## Reporting an issue

Please include the chapter or tool, the exact equation or sentence, what you think is incorrect or unclear, and the source or numerical counterexample that supports your concern. Distinguish mathematical errors from empirical uncertainties or alternative legitimate modeling assumptions.

## Proposing a teaching improvement

Prefer the sequence **real-world question → definitions and units → small numerical example → equation → verification → interpretation**. Write for people with epidemiological background who may not yet be comfortable with mixing matrices. Explain what assumptions would need to change for a different population.

## Citations

Link to primary research where practical; confirm that the work actually supports the claim. Provide complete bibliographic information and a DOI/persistent publisher URL. Do not use fabricated or AI-inferred references. Mark original derivations and toy examples as such.

## Reproducibility

If you change a mixing equation or numerical example, update the Python and R implementations as appropriate and rerun the tests. A new mixing construction should demonstrate nonnegative probabilities, row sums of one, reciprocity when undirected, and important limiting behavior. A model that does not satisfy a property should clearly explain why that property does not apply.

## Data and privacy

Never add identifiable participant data. This repository uses synthetic inputs. Contributions involving private program data must be converted to consented, non-identifiable, ethically shareable examples before publication.

## Build

Generated pages live in the repository and require no build step for hosting. To regenerate after editing `build_site.py`, install `requirements-dev.txt` and run `python build_site.py`. Then run the three Python checks in the README.
