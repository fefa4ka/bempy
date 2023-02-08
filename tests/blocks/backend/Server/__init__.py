from bempy import Block

class Base(Block):
    """
        A basic Server implementation
    """

    def init(self, host='127.0.0.1'):
        """
            host -- target address
        """

        print(self.name + ': Server created with host =', host)
