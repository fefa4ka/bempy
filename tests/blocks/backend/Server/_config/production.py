class Modificator:
    """
        A debug configuration
    """

    def init(self):
        self.config = 'remote'
        self.host = 'remote.host.com'

        print(self.name + ': Production configuration enabled')
