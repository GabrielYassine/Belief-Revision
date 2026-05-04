# Belief Revision Engine

This project is a Python implementation of a small belief revision engine for propositional logic. It was made for the DTU Introduction to Artificial Intelligence belief revision assignment.

The engine stores a finite belief base, checks logical entailment, supports contraction and expansion, and defines revision using the Levi identity.

## What is included

The implementation includes:

- propositional formulas represented as syntax trees
- a belief base with priorities and optional source labels
- formula normalization
- conversion to negation normal form (NNF)
- conversion to conjunctive normal form (CNF)
- clause extraction
- a truth-table reasoner for small validation cases
- a resolution-based reasoner for entailment and consistency checking
- expansion, contraction, and revision operations
- automated tests, including AGM-inspired tests

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

Formulas are represented as recursive syntax trees. The available constructors are:

- `Atom`
- `Not`
- `And`
- `Or`
- `Imply`
- `Iff`

### Belief Base

The belief base stores explicit formulas. Each formula can also have a priority and a source label. Logical consequences are not stored directly; they are derived by a reasoner when needed.

The priority values are used during contraction. Lower-priority beliefs are removed before higher-priority beliefs.

### Reasoning

The project contains two reasoners:

- **`TruthTableReasoner`** — checks entailment by evaluating all valuations. This is mainly used for small examples and validation.
- **`ResolutionReasoner`** — checks entailment and consistency using CNF conversion, clause extraction, and resolution.

### Belief Change Operations

The project supports three belief change operations:

- **Expansion:** adds a formula to the belief base.
- **Contraction:** removes low-priority beliefs until the target formula is no longer entailed.
- **Revision:** first contracts by the negation of the new formula and then expands with the new formula.

Revision is implemented using the Levi identity:

```text
B * φ = (B ÷ ¬φ) + φ
```

## Requirements

- Python 3.10 or newer
- `pytest` for running the tests

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

The demo prints examples of:

- formula normalization
- NNF/CNF conversion
- clause extraction
- belief base reasoning
- a sample revision run

## Running the Tests

Run all tests with:

```bash
python -m pytest -q
```