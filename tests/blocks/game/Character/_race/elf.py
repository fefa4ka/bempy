class Modificator:
    """
        A Elf race implementation
    """

    def init(self, mana=0):
        """
            mana -- The amount of mana
        """
        self.mana = mana
        print(self.name + ': Elf created with mana =', mana)
