class Modificator:
    """
        A Django backend implementation
    """

    def init(self, port=8080):
        """
            port -- server's port
        """

        print(self.name + ': Django server created on port =', str(port))
