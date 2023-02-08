import os

import unittest
from bempy import Block, bem_scope

def assert_base_instance(instance, some_arg):
    assert instance.some_param == 31337, "Block should have same_param = 31337"
    assert instance.some_arg == some_arg, "Block should save some_arg as parameter"
    assert get_params(instance).get('some_param', None)['value'] == 31337, "some_param in dict shoudl be 31337"

class TestMyModule(unittest.TestCase):
    def test_bem_scope(self):
        blocks = bem_scope()

        assert blocks.get('backend', False), 'Backend scope should exists'
        assert blocks['backend'].get('Server', None) != None, 'Server block should exists'
        assert blocks['backend'].get('Database', None) != None, 'Database block should exists'

    def test_server(self):
        from bempy.backend import Server

        FlaskApp = Server(
            backend='flask',
            config='debug',
            extensions=['db', 'cors']
        )

        app = FlaskApp(
            host='localhost',
            port=8080,
            db='mongodb'
        )


if __name__ == '__main__':
    unittest.main()
