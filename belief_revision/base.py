from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from .formula import Formula


@dataclass(frozen=True)
class BeliefEntry:
    formula: Formula
    priority: int = 0
    source: Optional[str] = None

    def __str__(self) -> str:
        if self.source:
            return f"[{self.priority}] {self.formula} (source={self.source})"
        return f"[{self.priority}] {self.formula}"


@dataclass
class BeliefBase:
    entries: List[BeliefEntry] = field(default_factory=list)

    def add(self, formula: Formula, priority: int = 0, source: Optional[str] = None) -> None:
        entry = BeliefEntry(formula=formula, priority=priority, source=source)
        if entry not in self.entries:
            self.entries.append(entry)

    def remove_formula(self, formula: Formula) -> None:
        self.entries = [entry for entry in self.entries if entry.formula != formula]

    def formulas(self) -> List[Formula]:
        return [entry.formula for entry in self.entries]

    def sorted_by_priority_lowest_first(self) -> List[BeliefEntry]:
        return sorted(self.entries, key=lambda entry: entry.priority)

    def copy(self) -> "BeliefBase":
        return BeliefBase(entries=self.entries.copy())

    def __str__(self) -> str:
        if not self.entries:
            return "{}"
        joined = ",\n  ".join(str(entry) for entry in self.entries)
        return "{\n  " + joined + "\n}"
