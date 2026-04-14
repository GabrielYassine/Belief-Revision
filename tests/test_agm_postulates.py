from belief_revision import Atom, Not, Or, Imply, BeliefBase, revise, expand


def logically_equivalent(base1, base2, atoms, reasoner):
    """
    Very small helper:
    treat two bases as equivalent if they entail the same test formulas.
    """
    test_formulas = list(atoms.values())

    for atom in list(atoms.values()):
        test_formulas.append(Not(atom))

    for f in test_formulas:
        if reasoner.entails(base1, f) != reasoner.entails(base2, f):
            return False
    return True


def test_success_postulate(res_reasoner, atoms):
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p, priority=3)
    base.add(Imply(p, q), priority=2)

    revised = revise(base, q, res_reasoner, priority=100)

    assert res_reasoner.entails(revised, q) is True


def test_consistency_postulate(res_reasoner, atoms):
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p, priority=3)

    revised = revise(base, q, res_reasoner, priority=100)

    assert res_reasoner.is_consistent(revised) is True


def test_vacuity_postulate(res_reasoner, atoms):
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p, priority=3)

    revised = revise(base, q, res_reasoner, priority=100)
    expanded = expand(base, q, priority=100)

    assert logically_equivalent(revised, expanded, atoms, res_reasoner)


def test_inclusion_postulate_weak_version(res_reasoner, atoms):
    """
    A practical implementation-oriented version:
    revised base should not contain completely unrelated beliefs out of nowhere.
    """
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p, priority=3)

    revised = revise(base, q, res_reasoner, priority=100)

    for formula in revised.formulas():
        assert formula == p or formula == q


def test_extensionality_postulate(res_reasoner, atoms):
    p = atoms["p"]
    q = atoms["q"]

    base = BeliefBase()
    base.add(p, priority=3)

    phi = Imply(p, q)
    psi = Or(Not(p), q)  # logically equivalent to p -> q

    revised_phi = revise(base, phi, res_reasoner, priority=100)
    revised_psi = revise(base, psi, res_reasoner, priority=100)

    assert logically_equivalent(revised_phi, revised_psi, atoms, res_reasoner)