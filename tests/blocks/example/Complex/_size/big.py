from bempy.example import Parent


class Modificator(Parent()):
    def init(self, big_mod_arg=0):
        print(self.name + ':', 'big modificator init with big_mod_arg =', big_mod_arg)
        self.big_mod_arg = big_mod_arg


