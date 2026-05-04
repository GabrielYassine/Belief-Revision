import pytest

from belief_revision import (
    Atom,
    Imply,
    BeliefBase,
    TruthTableReasoner,
    ResolutionReasoner,
)


@pytest.fixture
def atoms():
    return {
        "p": Atom("p"),
        "q": Atom("q"),
        "r": Atom("r"),
        "s": Atom("s"),
    }


@pytest.fixture
def tt_reasoner():
    return TruthTableReasoner()


@pytest.fixture
def res_reasoner():
    return ResolutionReasoner()


@pytest.fixture
def sample_base(atoms):
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p, priority=3, source="initial")
    base.add(Imply(p, q), priority=2, source="initial")
    base.add(q, priority=1, source="initial")
    return base