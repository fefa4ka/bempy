import os

import unittest
from bempy import Block, bem_scope
from bempy.utils.args import get_arguments, get_params
from bempy.utils.parser import block_description, block_params_description

def assert_base_instance(instance, some_arg):
    assert instance.some_param == 31337, "Block should have same_param = 31337"
    assert instance.some_arg == some_arg, "Block should save some_arg as parameter"
    assert get_params(instance).get('some_param', None)['value'] == 31337, "some_param in dict shoudl be 31337"

class TestMyModule(unittest.TestCase):
    def test_bem_scope(self):
        blocks = bem_scope()

        assert blocks.get('example', False), 'Example scope should exists'
        assert blocks['example'].get('Base', None) != None, 'Base block should exists'

    def test_bem_build(self):
        from bempy.example import Base

        base = Base()
        instance = None

        try:
            instance = base()
            assert False, "Base block couldn't be created without argument"
        except:
            instance = base(some_arg="VALUE")

        description = block_description(base)
        assert description[0] == "\nBasic block. It accept argument 'some_arg' and have parameter 'some_param'.\n", 'Description should generated from block class docstring wrapped with \\n symbol'

        test_instance = Base(some_prop="PROP_VAL")(some_arg=12345)

        params_description = block_params_description(base)
        assert params_description.get('some_param', None) == 'param description parsed by BEM Block', 'some_param description should be set'

        assert_base_instance(instance, 'VALUE')
        assert instance.inherited == [], "Base block should not inherit something"
        assert instance.name == 'example.Base', 'Instance name should be example.Base'
        assert instance.mods == {}, "Mods should not set for Base block"
        assert instance.props == {}, "Props should not set for this instance"
        assert len(instance.files) == 2, "Only from two files block should be builded"
        assert instance.files[0] == 'blocks/example/Base/__init__.py', "Front file should be Base/__init__.py"
        assert instance.files[1] == 'base.py', "Last file should be bem/base.py"

        assert_base_instance(test_instance, 12345)
        assert test_instance.inherited == [], "Base block should not inherit something"
        assert test_instance.name == 'example.Base', 'Instance name should be example.Base'
        assert test_instance.mods == {}, "Mods should not set for Base block"
        assert len(test_instance.files) == 2, "Only from two files block should be builded"
        assert test_instance.props.get('some_prop', [None])[0] == 'PROP_VAL', "Should be some_prop = PROP_VAL"

    def test_bem_inherited_build(self):
        from bempy.example import Child, Parent

        Block = Parent()
        instance = Block(some_arg=9876)
        assert instance.name == 'example.Parent', 'Instance name should be example.Parent'
        assert len(instance.inherited) == 1, "Parent block should inherit Base block"
        assert len(instance.files) == 3, "Only from three files block should be builded"
        assert instance.files[0] == 'blocks/example/Parent/__init__.py', "Front file should be Parent/__init__.py"
        assert instance.files[1] == 'blocks/example/Base/__init__.py', "Middle file should be Base/__init__.py"
        assert instance.files[2] == 'base.py', "Last file should be bem/base.py"

        assert_base_instance(instance, 9876)

        instance_builded_parent = Child()(some_arg="some_str")

        assert_base_instance(instance_builded_parent, "some_str")
        assert instance_builded_parent.name == 'example.Child', 'Instance name should be example.Child'
        assert len(instance_builded_parent.inherited) == 0, "Parent block should not inherit Base block"
        assert len(instance_builded_parent.files) == 3, "Only from three files block should be builded"
        assert instance_builded_parent.files[0] == 'blocks/example/Child/__init__.py', "Front file should be Parent/__init__.py"
        assert instance_builded_parent.files[1] == 'blocks/example/Base/__init__.py', "Middle file should be Base/__init__.py"
        assert instance_builded_parent.files[2] == 'base.py', "Last file should be bem/base.py"

    def test_bem_modificator(self):
        from bempy.example import Complex

        # Note about Complex definition
        instance = Complex()(some_arg=123)
        assert_base_instance(instance, 123)
        assert instance.mods == {}, "Mods should not set for Base block"

        # Comple with small size
        instance_mod = Complex(size='small')(some_arg="new_str", small_mod_arg=132)
        assert 'small' in instance_mod.mods.get('size', []), "Mod should be size = small"

        assert_base_instance(instance_mod, "new_str")
        # Big Complex
        instance_another_mod = Complex(size='big')(some_arg=333, big_mod_arg=31337)
        assert_base_instance(instance_another_mod, 333)
        assert 'big' in instance_another_mod.mods.get('size', []), "Mod should be size = big"

        instance_multiply_mod = Complex(size=['small', 'big'])(some_arg=123, small_mod_arg=1111, big_mod_arg=31337)
        instance_multiply_mods = instance_multiply_mod.mods.get('size', [])
        assert 'small' in instance_multiply_mods and 'big' in instance_multiply_mods, "Mod should be size = small, big"
        instance_multiply_mod = Complex(size=['big', 'small'])(some_arg=123)


if __name__ == '__main__':
    unittest.main()
