from __future__ import annotations
from dataclasses import dataclass
from typing import Set

class Formula:

    def atoms(self) -> Set[str]:
        raise NotImplementedError

    def eliminate_implications(self) -> "Formula":
        raise NotImplementedError

@dataclass(frozen=True)
class Atom(Formula):
    name: str

    def atoms(self) -> Set[str]:
        return {self.name}

    def eliminate_implications(self) -> Formula:
        return self

    def __str__(self) -> str:
        return self.name

@dataclass(frozen=True)
class Not(Formula):
    child: Formula

    def atoms(self) -> Set[str]:
        return self.child.atoms()

    def eliminate_implications(self) -> Formula:
        return Not(self.child.eliminate_implications())

    def __str__(self) -> str:
        if isinstance(self.child, Atom):
            return f"¬{self.child}"
        return f"¬({self.child})"

@dataclass(frozen=True)
class And(Formula):
    left: Formula
    right: Formula

    def atoms(self) -> Set[str]:
        return self.left.atoms() | self.right.atoms()

    def eliminate_implications(self) -> Formula:
        return And(
            self.left.eliminate_implications(),
            self.right.eliminate_implications(),
        )

    def __str__(self) -> str:
        return f"({self.left} ∧ {self.right})"

@dataclass(frozen=True)
class Or(Formula):
    left: Formula
    right: Formula

    def atoms(self) -> Set[str]:
        return self.left.atoms() | self.right.atoms()

    def eliminate_implications(self) -> Formula:
        return Or(
            self.left.eliminate_implications(),
            self.right.eliminate_implications(),
        )

    def __str__(self) -> str:
        return f"({self.left} ∨ {self.right})"


@dataclass(frozen=True)
class Imply(Formula):
    left: Formula
    right: Formula

    def atoms(self) -> Set[str]:
        return self.left.atoms() | self.right.atoms()

    def eliminate_implications(self) -> Formula:
        # (φ → ψ) ≡ (¬φ ∨ ψ)
        return Or(Not(self.left.eliminate_implications()), self.right.eliminate_implications())

    def __str__(self) -> str:
        return f"({self.left} → {self.right})"

@dataclass(frozen=True)
class Iff(Formula):
    left: Formula
    right: Formula

    def atoms(self) -> Set[str]:
        return self.left.atoms() | self.right.atoms()

    def eliminate_implications(self) -> Formula:
        # (φ ↔ ψ) ≡ (φ → ψ) ∧ (ψ → φ)
        return And(
            Imply(self.left, self.right).eliminate_implications(),
            Imply(self.right, self.left).eliminate_implications(),
        )

    def __str__(self) -> str:
        return f"({self.left} ↔ {self.right})"