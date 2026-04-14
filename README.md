# Belief Revision Engine

A Python implementation of a propositional belief revision engine for the DTU Intro to AI belief revision assignment.

## Current Status

The project currently includes:

- Propositional formula representation
- Belief base with priorities
- Formula normalization
- Conversion to negation normal form (NNF)
- Conversion to conjunctive normal form (CNF)
- Clause extraction
- Truth-table reasoning for small validation cases
- Resolution-based entailment and consistency checking
- Belief expansion
- Priority-based contraction
- Revision using the Levi identity
- Automated tests, including basic AGM-style checks

## Project Structure

```text
belief_revision/
    __init__.py
    base.py
    cnf.py
    formula.py
    normalize.py
    operators.py
    reasoner.py

tests/
    conftest.py
    test_agm_postulates.py
    test_cnf.py
    test_formula_normalization.py
    test_reasoner.py
    test_revision_basic.py

main.py
README.md
```

## Main Ideas

### Formula Representation

Formulas are represented as recursive syntax trees with the following constructors:

- `Atom`
- `Not`
- `And`
- `Or`
- `Imply`
- `Iff`

### Belief Base

The belief base stores explicit formulas together with optional metadata such as priority and source. Logical consequences are not stored directly; they are derived by a reasoner when needed.

### Reasoning

Two reasoners are currently included:

- **`TruthTableReasoner`** — Useful for checking small examples and validating behavior.
- **`ResolutionReasoner`** — The main reasoning engine. It uses CNF conversion and clause resolution to check entailment and consistency.

### Belief Change Operations

The project currently supports:

- **Expansion:** add a formula to the belief base
- **Contraction:** remove low-priority beliefs until the target formula is no longer entailed
- **Revision:** implemented using the Levi identity: `B * φ = (B ÷ ¬φ) + φ`

## Requirements

- Python 3.14 or another recent Python 3 version
- `pytest` for running the test suite

## Installation

Install `pytest` with:

```bash
python -m pip install pytest
```

## Running the Demo

Run the main example with:

```bash
python main.py
```

This will print:

- Normalization examples
- NNF/CNF examples
- Clause extraction examples
- Belief base reasoning examples
- A sample revision run

## Running the Tests

Run all tests with:

```bash
python -m pytest -q
```