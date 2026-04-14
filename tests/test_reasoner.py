from belief_revision import Atom, Not, Imply, BeliefBase


def test_truth_table_and_resolution_agree_on_entailment(tt_reasoner, res_reasoner, atoms):
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p)
    base.add(Imply(p, q))

    assert tt_reasoner.entails(base, q) is True
    assert res_reasoner.entails(base, q) is True


def test_truth_table_and_resolution_agree_on_non_entailment(tt_reasoner, res_reasoner, atoms):
    p = atoms["p"]
    q = atoms["q"]
    r = atoms["r"]

    base = BeliefBase()
    base.add(p)
    base.add(q)

    assert tt_reasoner.entails(base, r) is False
    assert res_reasoner.entails(base, r) is False


def test_inconsistent_base_detected(tt_reasoner, res_reasoner, atoms):
    p = atoms["p"]

    base = BeliefBase()
    base.add(p)
    base.add(Not(p))

    assert tt_reasoner.is_consistent(base) is False
    assert res_reasoner.is_consistent(base) is False


def test_consistent_base_detected(tt_reasoner, res_reasoner, atoms):
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p)
    base.add(Imply(p, q))

    assert tt_reasoner.is_consistent(base) is True
    assert res_reasoner.is_consistent(base) is True