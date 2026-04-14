from __future__ import annotations

from typing import Iterable, List, Set

from .base import BeliefBase
from .cnf import Clause, ClauseSet, extract_clauses
from .formula import Atom, Not, And, Or, Imply, Iff, Formula


class Reasoner:
    def entails(self, belief_base: BeliefBase, query: Formula) -> bool:
        raise NotImplementedError

    def is_consistent(self, belief_base: BeliefBase) -> bool:
        raise NotImplementedError


class TruthTableReasoner(Reasoner):
    def evaluate(self, formula: Formula, valuation: dict[str, bool]) -> bool:
        if isinstance(formula, Atom):
            return valuation[formula.name]
        if isinstance(formula, Not):
            return not self.evaluate(formula.child, valuation)
        if isinstance(formula, And):
            return self.evaluate(formula.left, valuation) and self.evaluate(formula.right, valuation)
        if isinstance(formula, Or):
            return self.evaluate(formula.left, valuation) or self.evaluate(formula.right, valuation)
        if isinstance(formula, Imply):
            return (not self.evaluate(formula.left, valuation)) or self.evaluate(formula.right, valuation)
        if isinstance(formula, Iff):
            return self.evaluate(formula.left, valuation) == self.evaluate(formula.right, valuation)
        raise TypeError(f"Unsupported formula type: {type(formula)!r}")

    def _all_valuations(self, atom_names: List[str]) -> Iterable[dict[str, bool]]:
        n = len(atom_names)
        for mask in range(1 << n):
            valuation: dict[str, bool] = {}
            for i, atom in enumerate(atom_names):
                valuation[atom] = bool((mask >> i) & 1)
            yield valuation

    def entails(self, belief_base: BeliefBase, query: Formula) -> bool:
        all_atoms: Set[str] = set(query.atoms())
        for formula in belief_base.formulas():
            all_atoms |= formula.atoms()

        atom_names = sorted(all_atoms)
        for valuation in self._all_valuations(atom_names):
            if all(self.evaluate(formula, valuation) for formula in belief_base.formulas()):
                if not self.evaluate(query, valuation):
                    return False
        return True

    def is_consistent(self, belief_base: BeliefBase) -> bool:
        all_atoms: Set[str] = set()
        for formula in belief_base.formulas():
            all_atoms |= formula.atoms()

        atom_names = sorted(all_atoms)
        for valuation in self._all_valuations(atom_names):
            if all(self.evaluate(formula, valuation) for formula in belief_base.formulas()):
                return True
        return False


class ResolutionReasoner(Reasoner):
    def entails(self, belief_base: BeliefBase, query: Formula) -> bool:
        clauses = self._belief_base_to_clauses(belief_base)
        clauses.extend(extract_clauses(Not(query)))
        return self._resolution_unsat(clauses)

    def is_consistent(self, belief_base: BeliefBase) -> bool:
        clauses = self._belief_base_to_clauses(belief_base)
        return not self._resolution_unsat(clauses)

    def _belief_base_to_clauses(self, belief_base: BeliefBase) -> ClauseSet:
        clauses: ClauseSet = []
        for formula in belief_base.formulas():
            clauses.extend(extract_clauses(formula))
        return clauses

    def _resolution_unsat(self, clauses: ClauseSet) -> bool:
        known: Set[Clause] = set(clauses)

        while True:
            new_resolvents: Set[Clause] = set()
            clause_list = list(known)

            for i in range(len(clause_list)):
                for j in range(i + 1, len(clause_list)):
                    resolvents = self._resolve(clause_list[i], clause_list[j])

                    if frozenset() in resolvents:
                        return True

                    new_resolvents |= resolvents

            if new_resolvents.issubset(known):
                return False

            known |= new_resolvents

    def _resolve(self, c1: Clause, c2: Clause) -> Set[Clause]:
        resolvents: Set[Clause] = set()

        for lit in c1:
            comp = lit.complement()
            if comp in c2:
                new_clause = (c1 - {lit}) | (c2 - {comp})

                if self._is_tautology(new_clause):
                    continue

                resolvents.add(frozenset(new_clause))

        return resolvents

    def _is_tautology(self, clause: Clause) -> bool:
        for lit in clause:
            if lit.complement() in clause:
                return True
        return False