from bempy import Block

class Base(Block):
    """
        Basic block. It accept argument 'some_arg' and have parameter 'some_param'.
    """
    some_param = 31337

    def init(self, some_arg="str"):
        """
            some_param -- param description parsed by BEM Block
        """

        self.some_arg=some_arg
        print(self.name + ': Base init with param =', some_arg)

