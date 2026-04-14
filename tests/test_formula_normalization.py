from belief_revision import Atom, Imply, Iff, Not, to_basic_connectives, simplify


def test_imply_elimination():
    p = Atom("p")
    q = Atom("q")
    result = to_basic_connectives(Imply(p, q))
    assert str(result) == "(¬p ∨ q)"


def test_iff_elimination():
    p = Atom("p")
    q = Atom("q")
    result = to_basic_connectives(Iff(p, q))
    assert str(result) == "((¬p ∨ q) ∧ (¬q ∨ p))"


def test_double_negation_simplifies():
    p = Atom("p")
    result = simplify(Not(Not(p)))
    assert result == p


def test_triple_negation_simplifies():
    p = Atom("p")
    result = simplify(Not(Not(Not(p))))
    assert str(result) == "¬p"