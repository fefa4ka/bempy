class Modificator:
    """
        A Flask backend implementation
    """

    def init(self, port=8080):
        """
            port -- server's port
        """

        print(self.name + ': Flask server created on port =', str(port))
