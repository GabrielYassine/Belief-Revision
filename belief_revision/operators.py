from __future__ import annotations
from typing import Optional
from .base import BeliefBase
from .formula import Formula, Not
from .reasoner import Reasoner

def expand(belief_base: BeliefBase, formula: Formula, priority: int = 0, source: Optional[str] = None) -> BeliefBase:
    """Expansion: add a formula without removing anything."""
    new_base = belief_base.copy()
    new_base.add(formula, priority=priority, source=source)
    return new_base

def contract(belief_base: BeliefBase, formula: Formula, reasoner: Reasoner) -> BeliefBase:

    new_base = belief_base.copy()

    if not reasoner.entails(new_base, formula):
        return new_base

    for entry in new_base.sorted_by_priority_lowest_first():
        new_base.remove_formula(entry.formula)
        if not reasoner.entails(new_base, formula):
            return new_base

    return new_base



def revise(belief_base: BeliefBase, formula: Formula, reasoner: Reasoner, priority: int = 100, source: Optional[str] = None) -> BeliefBase:
    """
    Levi identity:
        B * φ := (B ÷ ¬φ) + φ
    """
    contracted = contract(belief_base, Not(formula), reasoner)
    return expand(contracted, formula, priority=priority, source=source)