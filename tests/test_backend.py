import unittest
from bempy import Block, bem_scope, get_created_blocks

class TestBackendBlocks(unittest.TestCase):
    """
    Test suite for BEMPy backend blocks.
    
    These tests verify the functionality of the Server and Database blocks
    in the backend scope, including their modifiers and initialization.
    """
    
    def setUp(self):
        """Set up test environment before each test method."""
        # Clear any existing blocks to avoid test interference
        Block.scope = []
    
    def test_bem_scope_backend_structure(self):
        """Test that the backend scope has the expected structure."""
        blocks = bem_scope()
        
        # Verify backend scope exists
        self.assertIn('backend', blocks, 'Backend scope should exist')
        
        # Verify Server block exists with expected modifiers
        self.assertIn('Server', blocks['backend'], 'Server block should exist')
        server_mods = blocks['backend']['Server']
        self.assertIn('backend', server_mods, 'Server should have backend modifiers')
        self.assertIn('config', server_mods, 'Server should have config modifiers')
        self.assertIn('extensions', server_mods, 'Server should have extensions modifiers')
        
        # Verify specific modifiers exist
        self.assertIn('flask', server_mods['backend'], 'Flask backend should exist')
        self.assertIn('django', server_mods['backend'], 'Django backend should exist')
        self.assertIn('debug', server_mods['config'], 'Debug config should exist')
        self.assertIn('production', server_mods['config'], 'Production config should exist')
        
        # Verify Database block exists with expected modifiers
        self.assertIn('Database', blocks['backend'], 'Database block should exist')
        db_mods = blocks['backend']['Database']
        self.assertIn('backend', db_mods, 'Database should have backend modifiers')
        self.assertIn('config', db_mods, 'Database should have config modifiers')
        
        # Verify specific modifiers exist
        self.assertIn('mongodb', db_mods['backend'], 'MongoDB backend should exist')
        self.assertIn('mysql', db_mods['backend'], 'MySQL backend should exist')
    
    def test_server_flask_debug(self):
        """Test creating a Flask server with debug configuration."""
        from bempy.backend import Server
        
        # Create a Flask server with debug configuration
        FlaskApp = Server(
            backend='flask',
            config='debug'
        )
        
        # Initialize the server with specific parameters
        server = FlaskApp(
            host='localhost',
            port=8080
        )
        
        # Verify server properties
        self.assertEqual(server.name, 'backend.Server', 'Server name should be backend.Server')
        self.assertEqual(server.mods.get('backend', []), ['flask'], 'Server backend should be flask')
        self.assertEqual(server.mods.get('config', []), ['debug'], 'Server config should be debug')
        self.assertEqual(server.config, 'local', 'Debug config should set config to local')
        self.assertEqual(server.host, 'localhost', 'Debug config should set host to localhost')
    
    def test_server_django_production(self):
        """Test creating a Django server with production configuration."""
        from bempy.backend import Server
        
        # Create a Django server with production configuration
        DjangoApp = Server(
            backend='django',
            config='production'
        )
        
        # Initialize the server with specific parameters
        server = DjangoApp(
            port=443
        )
        
        # Verify server properties
        self.assertEqual(server.mods.get('backend', []), ['django'], 'Server backend should be django')
        self.assertEqual(server.mods.get('config', []), ['production'], 'Server config should be production')
        self.assertEqual(server.config, 'remote', 'Production config should set config to remote')
        self.assertEqual(server.host, 'remote.host.com', 'Production config should set host to remote.host.com')
    
    def test_server_with_database_extension(self):
        """Test creating a server with database extension."""
        from bempy.backend import Server
        
        # Create a Flask server with debug configuration and database extension
        FlaskApp = Server(
            backend='flask',
            config='debug',
            extensions=['db']
        )
        
        # Initialize the server with specific parameters
        server = FlaskApp(
            host='localhost',
            port=8080,
            db='mongodb'
        )
        
        # Verify database connection
        self.assertTrue(hasattr(server, 'db'), 'Server should have a db attribute')
        self.assertEqual(server.db.name, 'backend.Database', 'Database name should be backend.Database')
        self.assertEqual(server.db.mods.get('backend', []), ['mongodb'], 'Database backend should be mongodb')
    
    def test_database_direct_creation(self):
        """Test creating a database directly."""
        from bempy.backend import Database
        
        # Create a MongoDB database with remote configuration
        MongoDb = Database(
            backend='mongodb',
            config='remote'
        )
        
        # Initialize the database with specific parameters
        db = MongoDb(
            name='test_db',
            host='db.example.com'
        )
        
        # Verify database properties
        self.assertEqual(db.name, 'backend.Database', 'Database name should be backend.Database')
        self.assertEqual(db.mods.get('backend', []), ['mongodb'], 'Database backend should be mongodb')
        self.assertEqual(db.mods.get('config', []), ['remote'], 'Database config should be remote')
    
    def test_get_created_blocks(self):
        """Test retrieving created blocks."""
        from bempy.backend import Server, Database
        
        # Create some blocks
        server = Server(backend='flask')(host='localhost')
        db = Database(backend='mongodb')(name='test_db')
        
        # Get all created blocks
        blocks = get_created_blocks(None)
        
        # Verify blocks were created and can be retrieved
        self.assertGreaterEqual(len(blocks), 2, 'At least two blocks should be created')
        
        # Find blocks by their references
        server_refs = [ref for ref, block in blocks.items() if block.name == 'backend.Server']
        db_refs = [ref for ref, block in blocks.items() if block.name == 'backend.Database']
        
        self.assertGreaterEqual(len(server_refs), 1, 'At least one Server block should be created')
        self.assertGreaterEqual(len(db_refs), 1, 'At least one Database block should be created')


if __name__ == '__main__':
    unittest.main()
