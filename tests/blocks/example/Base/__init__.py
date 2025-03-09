from bempy import Block


class Base(Block):
    """
        Basic block. It accept argument 'some_arg' and have parameter 'some_param'.
    """
    some_param = 31337

    def init(self, some_arg=None):
        """
            some_param -- param description parsed by BEM Block
        """
        if some_arg is None:
            raise ValueError("some_arg is required")

        self.some_arg = some_arg
        self.some_param = 31337
        self.some_arg=some_arg
        print(self.name + ': Base init with param =', some_arg)

