from belief_revision import Atom, Not, And, Or, Imply, to_nnf, to_cnf, extract_clauses


def test_nnf_demorgan():
    p = Atom("p")
    q = Atom("q")
    r = Atom("r")

    result = to_nnf(Not(And(p, Or(q, r))))
    assert str(result) == "(¬p ∨ (¬q ∧ ¬r))"


def test_cnf_distribution():
    p = Atom("p")
    q = Atom("q")
    r = Atom("r")

    result = to_cnf(Or(p, And(q, r)))
    assert str(result) == "((p ∨ q) ∧ (p ∨ r))"


def test_clause_extraction_for_implication():
    p = Atom("p")
    q = Atom("q")
    r = Atom("r")

    clauses = extract_clauses(Imply(And(p, q), r))

    rendered = {frozenset(str(lit) for lit in clause) for clause in clauses}
    assert rendered == {frozenset({"¬p", "¬q", "r"})}