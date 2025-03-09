from bempy import Block

class Base(Block):
    """
    A basic World implementation
    """

    def init(self, param1=None):
        """
        param1 -- Description of param1
        """
        
        print(self.name + ': World created with param1 =', param1)
