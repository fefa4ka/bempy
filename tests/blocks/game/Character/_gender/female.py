class Modificator:
    """
        A Female gender implementation
    """

    def init(self, fertility=100):
        """
            fertility -- is the capability to produce offspring through reproduction
        """
        self.fertility = fertility
        print(self.name + ': Female created with fertility =', fertility)
