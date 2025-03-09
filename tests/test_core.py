import unittest
from pathlib import Path
import os
import sys
from typing import Dict, Any, List

from bempy import Block, bem_scope, get_created_blocks
from bempy.builder import Build
from bempy.utils import merge, uniq_f7, safe_serialize
from bempy.utils.structer import (
    bem_blocks_path, get_block_class, lookup_block_class,
    mods_from_dict, mods_predefined, get_mod_classes, lookup_mod_classes
)


class TestCoreBlock(unittest.TestCase):
    """Test the core Block class functionality."""
    
    def setUp(self):
        """Set up test environment before each test method."""
        # Clear any existing blocks to avoid test interference
        Block.scope = []
    
    def test_block_initialization(self):
        """Test basic Block initialization."""
        # Create a simple block subclass
        class TestBlock(Block):
            def init(self, param1=None, param2=None):
                self.param1 = param1
                self.param2 = param2
        
        # Initialize the block
        block = TestBlock(param1="test", param2=123)
        
        # Verify block properties
        self.assertEqual(block.param1, "test")
        self.assertEqual(block.param2, 123)
        self.assertEqual(len(Block.scope), 1)
        self.assertEqual(Block.scope[0][1], block)
    
    def test_block_inheritance(self):
        """Test Block inheritance."""
        # Create parent block
        class ParentBlock(Block):
            def init(self, parent_param=None):
                self.parent_param = parent_param
        
        # Create child block that inherits from parent
        class ChildBlock(Block):
            inherited = [ParentBlock]
            
            def init(self, child_param=None):
                self.child_param = child_param
        
        # Initialize the child block
        block = ChildBlock(parent_param="parent", child_param="child")
        
        # Verify block properties
        self.assertEqual(block.parent_param, "parent")
        self.assertEqual(block.child_param, "child")
        self.assertEqual(len(block.inherited), 1)
    
    def test_block_string_representation(self):
        """Test Block string representation."""
        # Create a block with name and modifiers
        class TestBlock(Block):
            def init(self):
                pass
        
        block = TestBlock()
        block.name = "test.block"
        block.mods = {"type": ["special"], "size": ["large"]}
        
        # Verify string representation contains expected parts
        str_repr = str(block)
        self.assertIn("Test Block", str_repr)
        self.assertIn("Type Special", str_repr)
        self.assertIn("Size Large", str_repr)
        self.assertIn("#", str_repr)  # Should contain ID


class TestBuildClass(unittest.TestCase):
    """Test the Build class functionality."""
    
    def setUp(self):
        """Set up test environment before each test method."""
        Block.scope = []
    
    def test_build_simple_block(self):
        """Test building a simple block."""
        # Create a block using the Build class
        from bempy.example import Base
        
        # Build the block
        base_block = Base()
        instance = base_block(some_arg="test_value")
        
        # Verify block properties
        self.assertEqual(instance.name, "example.Base")
        self.assertEqual(instance.some_arg, "test_value")
        self.assertEqual(instance.some_param, 31337)
        self.assertEqual(instance.mods, {})
    
    def test_build_with_modifiers(self):
        """Test building a block with modifiers."""
        from bempy.example import Complex
        
        # Build the block with a size modifier
        complex_block = Complex(size="small")
        instance = complex_block(some_arg="test", small_mod_arg=42)
        
        # Verify block properties
        self.assertEqual(instance.name, "example.Complex")
        self.assertEqual(instance.some_arg, "test")
        self.assertEqual(instance.small_mod_arg, 42)
        self.assertEqual(instance.mods.get("size", []), ["small"])
    
    def test_build_with_multiple_modifiers(self):
        """Test building a block with multiple modifiers."""
        from bempy.game import Character
        
        # Build a character with multiple modifiers
        character = Character(
            gender="female",
            race="elf",
            abilities=["agility", "intelligence"]
        )
        
        # Initialize the character
        instance = character(level=10, fertility=80, mana=100)
        
        # Verify block properties
        self.assertEqual(instance.name, "game.Character")
        self.assertEqual(instance.level, 10)
        self.assertEqual(instance.fertility, 80)
        self.assertEqual(instance.mana, 100)
        self.assertEqual(instance.mods.get("gender", []), ["female"])
        self.assertEqual(instance.mods.get("race", []), ["elf"])
        self.assertEqual(instance.mods.get("abilities", []), ["agility", "intelligence"])


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_merge(self):
        """Test the merge function."""
        a = {"first": {"all_rows": {"pass": "dog", "number": "1"}}}
        b = {"first": {"all_rows": {"fail": "cat", "number": "5"}}}
        
        result = merge(b, a)
        
        expected = {"first": {"all_rows": {"pass": "dog", "fail": "cat", "number": "5"}}}
        self.assertEqual(result, expected)
    
    def test_uniq_f7(self):
        """Test the uniq_f7 function."""
        input_list = [1, 2, 3, 2, 1, 4, 5, 4]
        result = uniq_f7(input_list)
        
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(result, expected)
    
    def test_safe_serialize(self):
        """Test the safe_serialize function."""
        # Test with simple dict
        simple_dict = {"name": "test", "value": 123}
        result = safe_serialize(simple_dict)
        self.assertEqual(result, '{"name": "test", "value": 123}')
        
        # Test with non-serializable object
        class TestClass:
            pass
        
        complex_dict = {"name": "test", "obj": TestClass()}
        result = safe_serialize(complex_dict)
        self.assertIn('"name": "test"', result)
        self.assertIn('"obj": "<', result)
    
    def test_mods_from_dict(self):
        """Test the mods_from_dict function."""
        # Test with string values
        input_dict = {"type": "special", "size": "large"}
        result = mods_from_dict(input_dict)
        
        expected = {"type": ["special"], "size": ["large"]}
        self.assertEqual(result, expected)
        
        # Test with list values
        input_dict = {"type": ["special", "unique"], "size": "large"}
        result = mods_from_dict(input_dict)
        
        expected = {"type": ["special", "unique"], "size": ["large"]}
        self.assertEqual(result, expected)
        
        # Test with comma-separated string
        input_dict = {"type": "special,unique", "size": "large"}
        result = mods_from_dict(input_dict)
        
        expected = {"type": ["special", "unique"], "size": ["large"]}
        self.assertEqual(result, expected)


class TestScopeFunctions(unittest.TestCase):
    """Test scope-related functions."""
    
    def test_bem_scope(self):
        """Test the bem_scope function."""
        blocks = bem_scope()
        
        # Verify that the scope contains expected blocks
        self.assertIn("example", blocks)
        self.assertIn("game", blocks)
        self.assertIn("backend", blocks)
        
        # Verify that the example scope contains expected blocks
        self.assertIn("Base", blocks["example"])
        self.assertIn("Complex", blocks["example"])
        
        # Verify that the game scope contains expected blocks
        self.assertIn("Character", blocks["game"])
        
        # Verify that the Character block contains expected modifiers
        character = blocks["game"]["Character"]
        self.assertIn("gender", character)
        self.assertIn("race", character)
        self.assertIn("abilities", character)
        
        # Verify specific modifiers
        self.assertIn("female", character["gender"])
        self.assertIn("male", character["gender"])
        self.assertIn("elf", character["race"])
        self.assertIn("human", character["race"])
    
    def test_get_created_blocks(self):
        """Test the get_created_blocks function."""
        # Create some blocks
        from bempy.example import Base
        from bempy.game import Character
        
        base_instance = Base()(some_arg="test")
        character_instance = Character(gender="female")(level=5)
        
        # Get all created blocks
        blocks = get_created_blocks(None)
        
        # Verify that the blocks were created and can be retrieved
        self.assertGreaterEqual(len(blocks), 2)
        
        # Find blocks by their names
        base_blocks = [block for ref, block in blocks.items() if block.name == "example.Base"]
        character_blocks = [block for ref, block in blocks.items() if block.name == "game.Character"]
        
        self.assertEqual(len(base_blocks), 1)
        self.assertEqual(len(character_blocks), 1)
        
        # Verify block properties
        self.assertEqual(base_blocks[0].some_arg, "test")
        self.assertEqual(character_blocks[0].level, 5)


class TestBlockLookup(unittest.TestCase):
    """Test block lookup functions."""
    
    def test_get_block_class(self):
        """Test the get_block_class function."""
        # Look up an existing block
        file_path, block_class = get_block_class("example.Base")
        
        # Verify the block was found
        self.assertIsNotNone(file_path)
        self.assertIsNotNone(block_class)
        self.assertTrue(str(file_path).endswith("Base/__init__.py"))
        
        # Look up a non-existent block
        file_path, block_class = get_block_class("nonexistent.Block")
        
        # Verify the block was not found
        self.assertIsNone(file_path)
        self.assertIsNone(block_class)
    
    def test_get_mod_classes(self):
        """Test the get_mod_classes function."""
        # Get modifiers for a block
        mods = {"gender": ["female"], "race": ["elf"]}
        mods_json = safe_serialize(mods)
        
        files, classes, loaded_mods = get_mod_classes("game.Character", mods_json)
        
        # Verify the modifiers were found
        self.assertGreaterEqual(len(files), 2)
        self.assertEqual(len(classes), 2)
        self.assertEqual(loaded_mods.get("gender", []), ["female"])
        self.assertEqual(loaded_mods.get("race", []), ["elf"])


if __name__ == "__main__":
    unittest.main()
