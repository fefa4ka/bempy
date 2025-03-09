import unittest
from bempy import Block, bem_scope, get_created_blocks
from bempy.builder import Build
from bempy.utils import merge, uniq_f7, safe_serialize

class TestBEMPy(unittest.TestCase):
    """
    Comprehensive test suite for BEMPy core functionality.
    
    This test suite verifies the functionality of the BEMPy library,
    including block creation, modification, inheritance, and utility functions.
    """
    
    def setUp(self):
        """Set up test environment before each test method."""
        # Clear any existing blocks to avoid test interference
        Block.scope = []
    
    def assert_base_instance(self, instance, some_arg):
        """Helper method to verify Base block instance properties."""
        self.assertEqual(instance.some_param, 31337, "Block should have some_param = 31337")
        self.assertEqual(instance.some_arg, some_arg, "Block should save some_arg as parameter")
        self.assertEqual(instance.get_params().get('some_param', {}).get('value'), 31337, 
                         "some_param in dict should be 31337")
    
    def test_bem_scope(self):
        """Test the bem_scope function for discovering blocks."""
        blocks = bem_scope()
        
        # Verify example scope exists
        self.assertTrue(blocks.get('example', False), 'Example scope should exist')
        self.assertIsNotNone(blocks['example'].get('Base'), 'Base block should exist')
        
        # Verify block structure
        self.assertIn('Base', blocks['example'], 'Base block should be in example scope')
        self.assertIn('Child', blocks['example'], 'Child block should be in example scope')
        self.assertIn('Parent', blocks['example'], 'Parent block should be in example scope')
        self.assertIn('Complex', blocks['example'], 'Complex block should be in example scope')
        
        # Verify modifiers
        self.assertIn('size', blocks['example']['Complex'], 'Complex block should have size modifiers')
        self.assertIn('small', blocks['example']['Complex']['size'], 'Complex block should have small size')
        self.assertIn('big', blocks['example']['Complex']['size'], 'Complex block should have big size')
    
    def test_bem_build_basic(self):
        """Test basic block building functionality."""
        from bempy.example import Base
        
        # Create a Base block
        base = Base()
        
        # Test that Base block requires some_arg parameter
        with self.assertRaises(Exception):
            instance = base()
        
        # Create a valid instance
        instance = base(some_arg="VALUE")
        
        # Create another instance with property
        test_instance = Base(some_prop="PROP_VAL")(some_arg=12345)
        
        # Verify instance properties
        self.assert_base_instance(instance, 'VALUE')
        self.assertEqual(instance.inherited, [], "Base block should not inherit anything")
        self.assertEqual(instance.name, 'example.Base', 'Instance name should be example.Base')
        self.assertEqual(instance.mods, {}, "Mods should not be set for Base block")
        self.assertEqual(instance.props, {}, "Props should not be set for this instance")
        
        # Verify file structure
        self.assertEqual(len(instance.files), 2, "Block should be built from two files")
        self.assertEqual(instance.files[0], 'blocks/example/Base/__init__.py', 
                         "First file should be Base/__init__.py")
        self.assertEqual(instance.files[1], 'base.py', "Last file should be bem/base.py")
        
        # Verify second instance
        self.assert_base_instance(test_instance, 12345)
        self.assertEqual(test_instance.props.get('some_prop', [None])[0], 'PROP_VAL', 
                         "Should be some_prop = PROP_VAL")
    
    def test_bem_build_with_builder(self):
        """Test block building using the Build class directly."""
        # Create a block using the Build class
        base_block = Build('example.Base')
        instance = base_block(some_arg="DIRECT_BUILD")
        
        # Verify instance properties
        self.assert_base_instance(instance, 'DIRECT_BUILD')
        self.assertEqual(instance.name, 'example.Base', 'Instance name should match the build name')
    
    def test_bem_inherited_build(self):
        """Test block inheritance functionality."""
        from bempy.example import Child, Parent, Base
        
        # Create a Parent block (inherits from Base)
        parent_block = Parent()
        parent_instance = parent_block(some_arg=9876)
        
        # Verify parent instance properties
        self.assertEqual(parent_instance.name, 'example.Parent', 'Instance name should be example.Parent')
        self.assertEqual(len(parent_instance.inherited), 1, "Parent block should inherit Base block")
        self.assertIsInstance(parent_instance.inherited[0], type(Base), "Parent should inherit from Base")
        
        # Verify file structure
        self.assertEqual(len(parent_instance.files), 3, "Block should be built from three files")
        self.assertEqual(parent_instance.files[0], 'blocks/example/Parent/__init__.py', 
                         "First file should be Parent/__init__.py")
        self.assertEqual(parent_instance.files[1], 'blocks/example/Base/__init__.py', 
                         "Middle file should be Base/__init__.py")
        
        # Verify base functionality is inherited
        self.assert_base_instance(parent_instance, 9876)
        
        # Create a Child block (inherits from Parent)
        child_instance = Child()(some_arg="child_arg")
        
        # Verify child instance properties
        self.assert_base_instance(child_instance, "child_arg")
        self.assertEqual(child_instance.name, 'example.Child', 'Instance name should be example.Child')
        
        # Verify inheritance chain
        self.assertEqual(len(child_instance.files), 3, "Block should be built from three files")
    
    def test_bem_modificator(self):
        """Test block modifiers functionality."""
        from bempy.example import Complex
        
        # Create a basic Complex instance (no modifiers)
        basic_instance = Complex()(some_arg=123)
        self.assert_base_instance(basic_instance, 123)
        self.assertEqual(basic_instance.mods, {}, "Mods should not be set for basic instance")
        
        # Create a Complex instance with 'small' size modifier
        small_instance = Complex(size='small')(some_arg="new_str", small_mod_arg=132)
        self.assertIn('small', small_instance.mods.get('size', []), "Mod should be size = small")
        self.assert_base_instance(small_instance, "new_str")
        self.assertEqual(small_instance.small_mod_arg, 132, "small_mod_arg should be set")
        
        # Create a Complex instance with 'big' size modifier
        big_instance = Complex(size='big')(some_arg=333, big_mod_arg=31337)
        self.assert_base_instance(big_instance, 333)
        self.assertIn('big', big_instance.mods.get('size', []), "Mod should be size = big")
        self.assertEqual(big_instance.big_mod_arg, 31337, "big_mod_arg should be set")
        
        # Create a Complex instance with multiple modifiers
        multi_instance = Complex(size=['small', 'big'])(
            some_arg=123, small_mod_arg=1111, big_mod_arg=31337
        )
        multi_mods = multi_instance.mods.get('size', [])
        self.assertIn('small', multi_mods, "Multi-instance should have small modifier")
        self.assertIn('big', multi_mods, "Multi-instance should have big modifier")
        self.assertEqual(multi_instance.small_mod_arg, 1111, "small_mod_arg should be set")
        self.assertEqual(multi_instance.big_mod_arg, 31337, "big_mod_arg should be set")
        
        # Test modifier order (should not matter)
        reverse_instance = Complex(size=['big', 'small'])(some_arg=123)
        reverse_mods = reverse_instance.mods.get('size', [])
        self.assertIn('small', reverse_mods, "Reverse-instance should have small modifier")
        self.assertIn('big', reverse_mods, "Reverse-instance should have big modifier")
    
    def test_get_created_blocks(self):
        """Test retrieving created block instances."""
        from bempy.example import Base, Complex
        
        # Create some blocks
        base_instance = Base()(some_arg="test")
        complex_instance = Complex(size='small')(some_arg="test2")
        
        # Get all created blocks
        blocks = get_created_blocks(None)
        
        # Verify blocks were created and can be retrieved
        self.assertGreaterEqual(len(blocks), 2, 'At least two blocks should be created')
        
        # Find blocks by their names
        base_blocks = [block for ref, block in blocks.items() if block.name == 'example.Base']
        complex_blocks = [block for ref, block in blocks.items() if block.name == 'example.Complex']
        
        self.assertEqual(len(base_blocks), 1, 'One Base block should be created')
        self.assertEqual(len(complex_blocks), 1, 'One Complex block should be created')
    
    def test_utility_functions(self):
        """Test utility functions in the BEMPy library."""
        # Test merge function
        a = {'first': {'all_rows': {'pass': 'dog', 'number': '1'}}}
        b = {'first': {'all_rows': {'fail': 'cat', 'number': '5'}}}
        result = merge(b, a)
        expected = {'first': {'all_rows': {'pass': 'dog', 'fail': 'cat', 'number': '5'}}}
        self.assertEqual(result, expected, "merge function should combine dictionaries correctly")
        
        # Test uniq_f7 function
        input_list = [1, 2, 3, 2, 1, 4, 5, 4]
        result = uniq_f7(input_list)
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(result, expected, "uniq_f7 should remove duplicates while preserving order")
        
        # Test safe_serialize function
        simple_dict = {"name": "test", "value": 123}
        result = safe_serialize(simple_dict)
        self.assertEqual(result, '{"name": "test", "value": 123}', 
                         "safe_serialize should correctly serialize simple objects")
        
        # Test with non-serializable object
        class TestClass:
            pass
        
        complex_dict = {"name": "test", "obj": TestClass()}
        result = safe_serialize(complex_dict)
        self.assertIn('"name": "test"', result, "safe_serialize should include serializable parts")
        self.assertIn('"obj": "<', result, "safe_serialize should convert non-serializable objects to strings")


if __name__ == '__main__':
    unittest.main()
