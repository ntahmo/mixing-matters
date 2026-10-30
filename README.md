# Mixing Matters

**An interactive textbook and practical handbook on mixing in infectious disease models.**

**[Explore the website](https://ntahmo.github.io/mixing-matters/)** · [Interactive matrix explorer](https://ntahmo.github.io/mixing-matters/explorer.html) · [References](https://ntahmo.github.io/mixing-matters/references.html)

## About

How do patterns of contact, partnership, and movement between people become mathematical representations of infectious disease transmission?

*Mixing Matters* helps make this process understandable and practical. It combines accessible explanations, step-by-step derivations, worked examples, interactive tools, and reproducible code. Readers can follow the lessons in order or consult individual topics as a modeling reference.

The resource is designed for students and researchers learning mathematical epidemiology, public health practitioners, and community collaborators participating in modeling research.

## Explore the resource

| Resource | What you'll find |
| --- | --- |
| **[Teaching chapters](https://ntahmo.github.io/mixing-matters/)** | Fifteen chapters, from population groups and partnership opportunities to mixing matrices, reciprocity, assortativity, empirical estimation, dynamic networks, intervention modeling, and AI. |
| **[Guided derivation](https://ntahmo.github.io/mixing-matters/walkthrough.html)** | A seven-step explanation of how to translate partner selection into mathematical expressions. |
| **[Mixing-matrix explorer](https://ntahmo.github.io/mixing-matters/explorer.html)** | Change inputs, compare mixing assumptions, and check normalization and reciprocity. |
| **[Model-selection guide](https://ntahmo.github.io/mixing-matters/decision.html)** | Identify reasonable mixing structures for different research questions and types of evidence. |
| **[Quick-reference sheet](https://ntahmo.github.io/mixing-matters/cheatsheet.html)** | Common scenarios, equations, mathematical checks, and pitfalls. |
| **[Technical notes](https://ntahmo.github.io/mixing-matters/technical.html)** | More formal derivations and mathematical details. |
| **[References](https://ntahmo.github.io/mixing-matters/references.html)** | Selected foundational and applied literature. |

The repository also includes reproducible **R and Python examples** (`code/`), **synthetic data** (`data/`), and **automated checks** (`tests/`).

## Approach

Each topic follows a consistent learning sequence:

**Real-world question → intuitive example → mathematical formulation → implementation → interpretation and checks.**

Throughout, we distinguish:

- **Evidence:** What empirical data reveal about population structure, contacts, partnerships, or movement.
- **Assumptions:** How researchers represent processes that are incompletely observed.
- **Mathematical requirements:** Conditions such as valid probabilities, consistent units, and reciprocal counts when modeling undirected partnerships.

The running example uses four fictional groups defined by activity and partner-meeting context. The underlying methods also apply to contact matrices, networks, individual-based models, stochastic models, and other transmission settings.

## Scientific foundations and limitations

The lessons draw on published research in mathematical epidemiology, social contact patterns, sexual partnership mixing, networks, and related fields. See the [references page](https://ntahmo.github.io/mixing-matters/references.html) for sources and further reading.

Numerical examples are **synthetic and educational**, not population estimates. Automated mathematical tests check properties of illustrative mixing constructions; they do **not** establish that a mixing assumption is empirically correct or that an epidemiological model is validated.

*Mixing Matters* is an evolving open educational resource, not a systematic review or peer-reviewed model. Applying the methods to a study requires data assessment, substantive expertise, uncertainty analysis, and appropriate validation.

The AI material addresses how AI can assist with explanation, coding, literature organization, and model checking while emphasizing independent verification of scientific claims and equations.

## Contributing and reuse

Suggestions, corrections, additional examples, and other contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) or [open an issue](https://github.com/ntahmo/mixing-matters/issues).

Original materials in this repository are shared under the [MIT License](LICENSE). Third-party publications remain subject to their respective rights.

## How to cite

If you use the resource in teaching or research, cite the website and the version or access date you used:

> Tahmo NB (October 2026). *Mixing Matters: An interactive textbook and practical handbook on mixing in infectious disease models.* https://ntahmo.github.io/mixing-matters/ (accessed YYYY-MM-DD).

A versioned scholarly citation can be added if the project receives an archived release or DOI.

---

**[Visit Mixing Matters](https://ntahmo.github.io/mixing-matters/)** · **[View the repository](https://github.com/ntahmo/mixing-matters)**
