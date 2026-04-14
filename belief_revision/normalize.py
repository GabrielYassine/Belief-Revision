from __future__ import annotations

from .formula import Formula, Atom, Not, And, Or, Imply, Iff


def eliminate_implications(formula: Formula) -> Formula:
    """
    Remove -> and <-> from a formula.
    Result uses only Atom, Not, And, Or.
    """
    return formula.eliminate_implications()


def simplify(formula: Formula) -> Formula:
    """
    Small structural simplifier.

    Current rules:
    - recursively simplify children
    - ¬¬φ  ->  φ
    """
    if isinstance(formula, Atom):
        return formula

    if isinstance(formula, Not):
        child = simplify(formula.child)

        if isinstance(child, Not):
            return simplify(child.child)

        return Not(child)

    if isinstance(formula, And):
        left = simplify(formula.left)
        right = simplify(formula.right)
        return And(left, right)

    if isinstance(formula, Or):
        left = simplify(formula.left)
        right = simplify(formula.right)
        return Or(left, right)

    if isinstance(formula, Imply):
        left = simplify(formula.left)
        right = simplify(formula.right)
        return Imply(left, right)

    if isinstance(formula, Iff):
        left = simplify(formula.left)
        right = simplify(formula.right)
        return Iff(left, right)

    raise TypeError(f"Unsupported formula type: {type(formula)!r}")


def to_basic_connectives(formula: Formula) -> Formula:
    """
    Convenience function:
    1. eliminate -> and <->
    2. simplify the result
    """
    return simplify(eliminate_implications(formula))