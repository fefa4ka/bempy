class Modificator:
    """
        A debug configuration
    """

    def init(self):
        self.config = 'local'
        self.host = 'localhost'

        print(self.name + ': Debug configuration enabled')
