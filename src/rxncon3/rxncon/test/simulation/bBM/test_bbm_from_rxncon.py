import rxncon.simulation.bBM.bbm_from_rxncon as bfr
import rxncon.input.quick.quick as quick
import rxncon.simulation.bBM.bBM_boolnet_exporter as bbe


def test_rule():
    rxncon_sys = quick.Quick("""A_ppi_B; ! <comp>
                               <comp>; AND A--C
                               <comp>; AND A--D
                               <comp>; AND A-{p}
                               A_ppi_C
                               A_ppi_D
                               C_p+_A
                               D_p-_A
                               E_p-_A
                            """)
    bbm_sys = bfr.bipartite_boolean_model_from_rxncon(rxncon_sys.rxncon_system)
    bbe_system = bbe.BoolNetSystem(bbm_sys)
    expected_str = """target, factors
A, A
B, B
C, C
D, D
E, E
A_ppi_B, (((A__C & A__D) & A_.p.) & (A & B))
A__B, (A__B | A_ppi_B)
A_ppi_C, (A & C)
A__C, (A__C | A_ppi_C)
A_ppi_D, (A & D)
A__D, (A__D | A_ppi_D)
C_pplus_A, (C & A)
A_.p., ((A_.p. & (! D_pminus_A & ! E_pminus_A)) | (C_pplus_A & (! D_pminus_A & ! E_pminus_A)))
D_pminus_A, (D & A)
E_pminus_A, (E & A)"""
    assert bbe_system.to_string() == expected_str


def test_convert_quantitative_contingencies_into_strict_contingencies():
    rxncon_sys = quick.Quick("""A_ppi_B; k- A-{P}; k+ A--C
                               A_ppi_C
                               D_p+_A""")
    bbm_sys = bfr.bipartite_boolean_model_from_rxncon(rxncon_sys.rxncon_system)
    bbe_system = bbe.BoolNetSystem(bbm_sys)
    expected_expression = """target, factors
A, A
B, B
C, C
D, D
A_ppi_B, ((A & B) & (A__C & ! A_.p.))
A__B, (A__B | A_ppi_B)
A_ppi_C, (A & C)
A__C, (A__C | A_ppi_C)
D_pplus_A, (D & A)
A_.p., (A_.p. | D_pplus_A)"""
    assert bbe_system.to_string() == expected_expression
