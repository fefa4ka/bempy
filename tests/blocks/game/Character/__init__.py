from bempy import Block

class Base(Block):
    """
        A basic Character implementation
    """

    def init(self, level=1):
        """
            level -- The level of character
        """

        print(self.name + ': Character created with level =', level)
