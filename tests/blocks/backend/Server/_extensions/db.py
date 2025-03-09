from bempy.backend import Database


class Modificator:
    """
        A db backend connection implementation
    """

    def init(self, db='mysql'):
        """
            db -- type of database
        """

        connector = Database(
            backend=db,
            config=getattr(self, 'config', 'local')
        )

        self.db = connector(name=db, host=getattr(self, 'host', 'localhost'))

        print(self.name + ': Database connection with db =', db)
