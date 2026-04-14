from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, List, Set

from .formula import Formula, Atom, Not, And, Or
from .normalize import to_basic_connectives, simplify


@dataclass(frozen=True)
class Literal:
    name: str
    is_negated: bool = False

    def __str__(self) -> str:
        return f"¬{self.name}" if self.is_negated else self.name

    def complement(self) -> "Literal":
        return Literal(self.name, not self.is_negated)


Clause = FrozenSet[Literal]
ClauseSet = List[Clause]


def to_nnf(formula: Formula) -> Formula:
    """
    Convert a formula to negation normal form.
    Assumes implication and biconditional have already been eliminated
    or calls the basic-normalization step first.
    """
    formula = simplify(to_basic_connectives(formula))
    return _to_nnf_internal(formula)


def _to_nnf_internal(formula: Formula) -> Formula:
    if isinstance(formula, Atom):
        return formula

    if isinstance(formula, Not):
        child = formula.child

        if isinstance(child, Atom):
            return formula

        if isinstance(child, Not):
            return _to_nnf_internal(child.child)

        if isinstance(child, And):
            return Or(
                _to_nnf_internal(Not(child.left)),
                _to_nnf_internal(Not(child.right)),
            )

        if isinstance(child, Or):
            return And(
                _to_nnf_internal(Not(child.left)),
                _to_nnf_internal(Not(child.right)),
            )

        raise TypeError(f"Unexpected formula inside Not in NNF conversion: {type(child)!r}")

    if isinstance(formula, And):
        return And(
            _to_nnf_internal(formula.left),
            _to_nnf_internal(formula.right),
        )

    if isinstance(formula, Or):
        return Or(
            _to_nnf_internal(formula.left),
            _to_nnf_internal(formula.right),
        )

    raise TypeError(f"Unsupported formula type in NNF conversion: {type(formula)!r}")


def to_cnf(formula: Formula) -> Formula:
    """
    Convert a formula to conjunctive normal form.
    Result uses only Atom, Not(atom), And, Or in CNF shape.
    """
    nnf = to_nnf(formula)
    return simplify(_to_cnf_internal(nnf))


def _to_cnf_internal(formula: Formula) -> Formula:
    if isinstance(formula, (Atom, Not)):
        return formula

    if isinstance(formula, And):
        return And(
            _to_cnf_internal(formula.left),
            _to_cnf_internal(formula.right),
        )

    if isinstance(formula, Or):
        left = _to_cnf_internal(formula.left)
        right = _to_cnf_internal(formula.right)
        return _distribute_or(left, right)

    raise TypeError(f"Unsupported formula type in CNF conversion: {type(formula)!r}")


def _distribute_or(left: Formula, right: Formula) -> Formula:
    """
    Distribute OR over AND:
    (A ∧ B) ∨ C  => (A ∨ C) ∧ (B ∨ C)
    A ∨ (B ∧ C)  => (A ∨ B) ∧ (A ∨ C)
    """
    if isinstance(left, And):
        return And(
            _distribute_or(left.left, right),
            _distribute_or(left.right, right),
        )

    if isinstance(right, And):
        return And(
            _distribute_or(left, right.left),
            _distribute_or(left, right.right),
        )

    return Or(left, right)


def extract_clauses(formula: Formula) -> ClauseSet:
    """
    Convert a CNF formula into a list of clauses.
    Each clause is a frozenset of Literal.
    """
    cnf_formula = to_cnf(formula)
    clauses: List[Clause] = []
    _collect_clauses(cnf_formula, clauses)
    return clauses


def _collect_clauses(formula: Formula, clauses: List[Clause]) -> None:
    if isinstance(formula, And):
        _collect_clauses(formula.left, clauses)
        _collect_clauses(formula.right, clauses)
        return

    literals: Set[Literal] = set()
    _collect_literals(formula, literals)
    clauses.append(frozenset(literals))


def _collect_literals(formula: Formula, literals: Set[Literal]) -> None:
    if isinstance(formula, Or):
        _collect_literals(formula.left, literals)
        _collect_literals(formula.right, literals)
        return

    if isinstance(formula, Atom):
        literals.add(Literal(formula.name, False))
        return

    if isinstance(formula, Not) and isinstance(formula.child, Atom):
        literals.add(Literal(formula.child.name, True))
        return

    raise ValueError(f"Formula is not a valid CNF clause literal structure: {formula}")


def clause_set_to_string(clauses: ClauseSet) -> str:
    parts = []
    for clause in clauses:
        literals = sorted((str(lit) for lit in clause), key=lambda s: s.replace("¬", ""))
        parts.append("{" + ", ".join(literals) + "}")
    return "[" + ", ".join(parts) + "]"