from bempy import Block

class Base(Block):
    """
        A basic Database implementation
    """

    def init(self, name='default'):
        """
            name -- name of a database instance
        """

        print(self.name + ': Database connection with name =', name)
