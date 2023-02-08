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
            config=self.config
        )

        self.db = connector(self.host)

        print(self.name + ': Database connection with db =', db)
