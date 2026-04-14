from belief_revision import (
    Atom,
    Imply,
    Iff,
    Not,
    And,
    Or,
    BeliefBase,
    TruthTableReasoner,
    ResolutionReasoner,
    revise,
    to_basic_connectives,
    simplify,
    to_nnf,
    to_cnf,
    extract_clauses,
    clause_set_to_string,
)


def main() -> None:
    p = Atom("p")
    q = Atom("q")
    r = Atom("r")

    print("Normalize p -> q:")
    print(to_basic_connectives(Imply(p, q)))
    print()

    print("Normalize p <-> q:")
    print(to_basic_connectives(Iff(p, q)))
    print()

    print("Simplify ¬¬p:")
    print(simplify(Not(Not(p))))
    print()

    print("NNF of ¬(p ∧ (q ∨ r)):")
    print(to_nnf(Not(And(p, Or(q, r)))))
    print()

    print("CNF of p ∨ (q ∧ r):")
    print(to_cnf(Or(p, And(q, r))))
    print()

    print("Clauses for (p ∧ q) -> r:")
    clauses = extract_clauses(Imply(And(p, q), r))
    print(clause_set_to_string(clauses))
    print()

    base = BeliefBase()
    base.add(p, priority=3, source="initial")
    base.add(Imply(p, q), priority=2, source="initial")
    base.add(q, priority=1, source="initial")

    tt_reasoner = TruthTableReasoner()
    res_reasoner = ResolutionReasoner()

    print("Initial belief base:")
    print(base)
    print()

    print("Truth-table: does base entail q?")
    print(tt_reasoner.entails(base, q))
    print()

    print("Resolution: does base entail q?")
    print(res_reasoner.entails(base, q))
    print()

    revised = revise(base, Not(q), res_reasoner, priority=100, source="new information")

    print("Revised by ¬q:")
    print(revised)
    print()

    print("Resolution: is revised base consistent?")
    print(res_reasoner.is_consistent(revised))
    print()

    print("Resolution: does revised base entail ¬q?")
    print(res_reasoner.entails(revised, Not(q)))


if __name__ == "__main__":
    main()