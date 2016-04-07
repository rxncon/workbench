import pytest
import rxncon.venntastic.sets as venn
import rxncon.core.rxncon_system as rxs
import rxncon.syntax.rxncon_from_string as rfs
import rxncon.semantics.molecule_instance as mins
import rxncon.semantics.molecule_definition as mdef
import rxncon.semantics.molecule_instance_from_rxncon as mifr
import rxncon.semantics.molecule_definition_from_rxncon as mdfr
import rxncon.semantics.molecule_definition as mdf
import rxncon.core.specification as spe

from rxncon.simulation.rule_based.molecule_from_string import mol_def_from_string, mol_instance_from_string


def test_commutative_diagram_for_complement_operation(mol_def, state_sets):
    for state_set in state_sets:
        mol_props_then_complement = venn.Complement(mifr.property_set_from_mol_def_and_state_set(mol_def, state_set))
        complement_then_mol_props = mifr.property_set_from_mol_def_and_state_set(mol_def, venn.Complement(state_set))

        print()
        print(mol_props_then_complement.simplified_form())
        print()
        print(complement_then_mol_props.simplified_form())

        #assert mol_props_then_complement.is_equivalent_to(complement_then_mol_props)


@pytest.fixture
def mol_def() -> mdef.MoleculeDefinition:
    reactions = [
        rfs.reaction_from_string('B_ppi_A_[x]'),
        rfs.reaction_from_string('C_ppi_A_[x]')
    ]

    rxnsys = rxs.RxnConSystem(reactions, [])
    mol_def_supervisor = mdfr.MoleculeDefinitionSupervisor(rxnsys)

    return mol_def_supervisor.mol_def_for_name('A')


@pytest.fixture
def state_sets():
    return [
        venn.PropertySet(rfs.state_from_string('A--B'))
    ]



@pytest.fixture
def molecule_instances():
    return [[mol_instance_from_string('C#ass/C_[dA]:A_[dC]', 'C#ass/C_[dA]:'),
             mol_instance_from_string('B#ass/B_[dA]:A_[dB]', 'B#ass/B_[dA]:'),
             mol_instance_from_string('A#ass/A_[dB]:B_[dA]', 'A#ass/A_[dB]:')],

            [mol_instance_from_string('A#ass/A_[dB]:B_[dA]', 'A#ass/A_[dB]:'),
             mol_instance_from_string('B#ass/B_[dA]:A_[dB]', 'B#ass/B_[dA]:'),
             mol_instance_from_string('C#ass/C_[dA]:A_[dC]', 'C#ass/C_[dA]:')],

            [mol_instance_from_string('A#ass/A_[dE]:E_[dA]', 'A#ass/A_[dE]:'),
             mol_instance_from_string('A#ass/A_[dD]:D_[dA]', 'A#ass/A_[dD]:'),
             mol_instance_from_string('A#ass/A_[dC]:C_[dA]', 'A#ass/A_[dC]:')],

            [mol_instance_from_string('A#ass/A_[dE/sE]:E_[dA]', 'A#ass/A_[dE/sE]:'),
             mol_instance_from_string('A#ass/A_[dD/sD]:D_[dA]', 'A#ass/A_[dD/sD]:'),
             mol_instance_from_string('A#ass/A_[dC/sC]:C_[dA]', 'A#ass/A_[dC/sC]:')],

            [mol_instance_from_string('A#ass/A_[rE]:E_[dA]', 'A#ass/A_[rE]:'),
             mol_instance_from_string('A#ass/A_[rD]:D_[dA]', 'A#ass/A_[rD]:'),
             mol_instance_from_string('A#ass/A_[rC]:C_[dA]', 'A#ass/A_[rC]:')],

            [mol_instance_from_string('A#ass/A_[rE]:E_[dA]', 'A#ass/A_[rE]:'),
             mol_instance_from_string('A#', 'A#'),
             mol_instance_from_string('A#ass/A_[rC]:C_[dA]', 'A#ass/A_[rC]:')],

            [mol_instance_from_string('A#ass/A_[rE]:E_[dA],mod/A_[(r)]:u~p', 'A#ass/A_[rE]:,mod/A_[(r)]:u'),
             mol_instance_from_string('A#', 'A#'),
             mol_instance_from_string('A#ass/A_[rC]:C_[dA]', 'A#ass/A_[rC]:')],

            [mol_instance_from_string('A#mod/A_[(r)]:u~p', 'A#mod/A_[(r)]:p'),
             mol_instance_from_string('A#mod/A_[(r)]:u~ub', 'A#mod/A_[(r)]:ub'),
             mol_instance_from_string('A#mod/A_[(r)]:u~ub~p', 'A#mod/A_[(r)]:u')]

            ]

@pytest.fixture
def expected_molecule_instances_ordering():
     return [[mol_instance_from_string('A#ass/A_[dB]:B_[dA]', 'A#ass/A_[dB]:'),
             mol_instance_from_string('B#ass/B_[dA]:A_[dB]', 'B#ass/B_[dA]:'),
             mol_instance_from_string('C#ass/C_[dA]:A_[dC]', 'C#ass/C_[dA]:')],

             [mol_instance_from_string('A#ass/A_[dB]:B_[dA]', 'A#ass/A_[dB]:'),
              mol_instance_from_string('B#ass/B_[dA]:A_[dB]', 'B#ass/B_[dA]:'),
              mol_instance_from_string('C#ass/C_[dA]:A_[dC]', 'C#ass/C_[dA]:')],

             [mol_instance_from_string('A#ass/A_[dC]:C_[dA]', 'A#ass/A_[dC]:'),
              mol_instance_from_string('A#ass/A_[dD]:D_[dA]', 'A#ass/A_[dD]:'),
              mol_instance_from_string('A#ass/A_[dE]:E_[dA]', 'A#ass/A_[dE]:')],

             [mol_instance_from_string('A#ass/A_[dC/sC]:C_[dA]', 'A#ass/A_[dC/sC]:'),
              mol_instance_from_string('A#ass/A_[dD/sD]:D_[dA]', 'A#ass/A_[dD/sD]:'),
              mol_instance_from_string('A#ass/A_[dE/sE]:E_[dA]', 'A#ass/A_[dE/sE]:')],

             [mol_instance_from_string('A#ass/A_[rC]:C_[dA]', 'A#ass/A_[rC]:'),
              mol_instance_from_string('A#ass/A_[rD]:D_[dA]', 'A#ass/A_[rD]:'),
              mol_instance_from_string('A#ass/A_[rE]:E_[dA]', 'A#ass/A_[rE]:')],

             [mol_instance_from_string('A#', 'A#'),
              mol_instance_from_string('A#ass/A_[rC]:C_[dA]', 'A#ass/A_[rC]:'),
              mol_instance_from_string('A#ass/A_[rE]:E_[dA]', 'A#ass/A_[rE]:')],

             [mol_instance_from_string('A#', 'A#'),
              mol_instance_from_string('A#ass/A_[rC]:C_[dA]', 'A#ass/A_[rC]:'),
              mol_instance_from_string('A#ass/A_[rE]:E_[dA],mod/A_[(r)]:u~p', 'A#ass/A_[rE]:,mod/A_[(r)]:u')],

             [mol_instance_from_string('A#mod/A_[(r)]:u~p', 'A#mod/A_[(r)]:p'),
              mol_instance_from_string('A#mod/A_[(r)]:u~ub~p', 'A#mod/A_[(r)]:u'),
              mol_instance_from_string('A#mod/A_[(r)]:u~ub', 'A#mod/A_[(r)]:ub'),
             ]
            ]

def test_molecule_instance_sorting(molecule_instances, expected_molecule_instances_ordering):
    for i, instances in enumerate(molecule_instances):
        assert sorted(instances) == expected_molecule_instances_ordering[i]
