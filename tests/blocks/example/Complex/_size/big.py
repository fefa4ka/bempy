from bempy.example import Parent

class Modificator(Parent()):
    def prepare(self, big_mod_arg=0):
        print(self.name + ':', 'big modificator prepare with big_mod_arg =', big_mod_arg)

