from belief_revision import Atom, Not, Imply, BeliefBase, revise


def test_revision_accepts_new_information(res_reasoner, atoms):
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p, priority=3)
    base.add(Imply(p, q), priority=2)
    base.add(q, priority=1)

    revised = revise(base, Not(q), res_reasoner, priority=100)

    assert res_reasoner.entails(revised, Not(q)) is True


def test_revision_result_is_consistent(res_reasoner, atoms):
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p, priority=3)
    base.add(Imply(p, q), priority=2)
    base.add(q, priority=1)

    revised = revise(base, Not(q), res_reasoner, priority=100)

    assert res_reasoner.is_consistent(revised) is True


def test_higher_priority_belief_tends_to_survive(res_reasoner, atoms):
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p, priority=10)
    base.add(Imply(p, q), priority=2)
    base.add(q, priority=1)

    revised = revise(base, Not(q), res_reasoner, priority=100)

    assert p in revised.formulas()
    assert Not(q) in revised.formulas()