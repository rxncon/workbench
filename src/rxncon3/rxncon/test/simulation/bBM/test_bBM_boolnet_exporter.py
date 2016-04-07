import os
import time
import tempfile
import pytest

import rxncon.simulation.bBM.bipartite_boolean_model as bbm
import rxncon.simulation.bBM.bbm_from_rxncon as bfr
import rxncon.simulation.bBM.bBM_boolnet_exporter as bbe
import rxncon.syntax.rxncon_from_string as rfs
import rxncon.venntastic.sets as venn
import rxncon.input.quick.quick as qui


def test_generate_name():
    a_pplus_b = bbm.Node(rfs.reaction_from_string("a_p+_b"))
    assert bbe.string_from_reaction(a_pplus_b.value) == "a_pplus_b"

    a_dash_dash_b = bbm.Node(rfs.state_from_string("A--B"))
    assert bbe.string_from_inter_protein_interaction_state(a_dash_dash_b.value) == "A__B"

    b_intra = bbm.Node(rfs.state_from_string("b_[n]--[m]"))

    assert bbe.string_from_intra_protein_interaction_state(b_intra.value) == "b_.n.__.m."

    A_ppi_B = bbm.Node(rfs.reaction_from_string("A_[n]_ppi_B_[d/s(r)]"))

    assert bbe.string_from_reaction(A_ppi_B.value) == "A_.n._ppi_B_.d.s.r.."


def test_boolnet_string(rule_A__B, rule_A_ppi_B, rule_A_p, rule_C_pplus_A, initialConditions):
    bbm_system = bbm.BipartiteBooleanModel([rule_A__B, rule_A_ppi_B, rule_A_p, rule_C_pplus_A],
                                           initialConditions)

    bbe_system = bbe.BoolNetSystem(bbm_system)
    bbe_str = bbe_system.to_string()

    expected_str = """target, factors
A, A
B, B
C, C
A__B, (A_ppi_B | A__B)
A_ppi_B, ((A & B) & A_.p.)
A_.p., (C_pplus_A | A_.p.)
C_pplus_A, (C & A)"""

    assert bbe_str == expected_str


def test_boolnet_string_with_complement(rule_A__B, rule_A_ppi_B, rule_A_p_deg, rule_C_pplus_A, initialConditions):
    bbm_system = bbm.BipartiteBooleanModel([rule_A__B, rule_A_ppi_B, rule_A_p_deg, rule_C_pplus_A],
                                           initialConditions)

    bbe_system = bbe.BoolNetSystem(bbm_system)
    bbe_str = bbe_system.to_string()
    expected_str = """target, factors
A, A
B, B
C, C
A__B, (A_ppi_B | A__B)
A_ppi_B, ((A & B) & A_.p.)
A_.p., ((C_pplus_A | A_.p.) & (! D_pminus_A & ! E_pminus_A))
C_pplus_A, (C & A)"""

    assert bbe_str == expected_str


def test_strange_thing():
    quick_sys = qui.Quick("""
    A_trsc_B; ! <comp1>; x <comp2>; x <comp3>; x <comp4>
    <comp1>; AND C--D; AND C--E
    <comp2>; AND G--F; AND <comp4>
    <comp3>;AND H--F; AND <comp4>
    <comp4>; AND F--E; AND <comp1>""")

    bbm_sys = bfr.bipartite_boolean_model_from_rxncon(quick_sys.rxncon_system)
    bbe_system = bbe.BoolNetSystem(bbm_sys)
    print(bbe_system.to_string())





def test_to_file(rule_A__B, rule_A_ppi_B, rule_A_p_deg, rule_C_pplus_A, initialConditions):
    bbm_system = bbm.BipartiteBooleanModel([rule_A__B, rule_A_ppi_B, rule_A_p_deg, rule_C_pplus_A],
                                           initialConditions)

    bbe_system = bbe.BoolNetSystem(bbm_system)
    bbe_str = bbe_system.to_string()
    path = "{0}/test{1}.bool".format(tempfile.gettempdir(), time.time())
    bbe_system.to_file(path)
    assert os.path.exists(path)
    os.remove(path)


@pytest.fixture
def rule_A__B():

    value_A__B = venn.Union(venn.PropertySet(bbm.Node(rfs.reaction_from_string("A_ppi_B"))),
                            venn.PropertySet(bbm.Node(rfs.state_from_string("A--B"))),
                            )

    return bbm.Rule(bbm.Node(rfs.state_from_string("A--B")), bbm.Factor(value_A__B))


@pytest.fixture
def rule_A_ppi_B():
    value_A_ppi_B = venn.Intersection(venn.Intersection(venn.PropertySet(bbm.Node(rfs.reaction_from_string("A_ppi_B").components[0])),
                                                            venn.PropertySet(bbm.Node(rfs.reaction_from_string("A_ppi_B").components[1]))),
                                          venn.PropertySet(bbm.Node(rfs.state_from_string("A-{P}"))))
    return bbm.Rule(bbm.Node(rfs.reaction_from_string("A_ppi_B")), bbm.Factor(value_A_ppi_B))


@pytest.fixture
def rule_A_p():
    value_A_p = venn.Union(venn.PropertySet(bbm.Node(rfs.reaction_from_string("C_p+_A"))),
                           venn.PropertySet(bbm.Node(rfs.state_from_string("A-{P}"))))

    return bbm.Rule(bbm.Node(rfs.state_from_string("A-{P}")), bbm.Factor(value_A_p))


@pytest.fixture
def rule_A_p_deg():
    value_A_p_deg = venn.Intersection(venn.Union(venn.PropertySet(bbm.Node(rfs.reaction_from_string("C_p+_A"))),
                                                 venn.PropertySet(bbm.Node(rfs.state_from_string("A-{P}")))),
                                      venn.Intersection(venn.Complement(venn.PropertySet(bbm.Node(rfs.reaction_from_string("D_p-_A")))),
                                                        venn.Complement(venn.PropertySet(bbm.Node(rfs.reaction_from_string("E_p-_A")))))
                                      )

    return bbm.Rule(bbm.Node(rfs.state_from_string("A-{P}")), bbm.Factor(value_A_p_deg))


@pytest.fixture
def rule_C_pplus_A():
    value_C_pplus_A = venn.Intersection(venn.PropertySet(bbm.Node(rfs.reaction_from_string("C_p+_A").components[0])),
                                        venn.PropertySet(bbm.Node(rfs.reaction_from_string("C_p+_A").components[1])))
    return bbm.Rule(bbm.Node(rfs.reaction_from_string("C_p+_A")), bbm.Factor(value_C_pplus_A))


@pytest.fixture
def rule_D_pminus_A():
    value_D_pminus_A = venn.Intersection(venn.PropertySet(bbm.Node(rfs.reaction_from_string("D_p-_A").components[0])),
                                        venn.PropertySet(bbm.Node(rfs.reaction_from_string("D_p-_A").components[1])))
    return bbm.Rule(bbm.Node(rfs.reaction_from_string("D_p-_A")), bbm.Factor(value_D_pminus_A))


@pytest.fixture
def initialConditions():
    return [bbm.InitCondition(bbm.Node(rfs.reaction_from_string("A_ppi_B").components[0]), None),
                      bbm.InitCondition(bbm.Node(rfs.reaction_from_string("A_ppi_B").components[1]), None),
                      bbm.InitCondition(bbm.Node(rfs.reaction_from_string("C_p+_A").components[0]), None)
           ]


