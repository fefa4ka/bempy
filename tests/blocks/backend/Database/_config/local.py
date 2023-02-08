class Modificator:
    """
        A local db implementation
    """

    def init(self, host='/var/db'):
        """
            host -- path to db file
        """

        print(self.name + ': Local Database created from path =', host)
