from bempy.example import Base

class Base(Base()):
    def prepare(self):
        print(self.name + ':', 'Child prepare')

