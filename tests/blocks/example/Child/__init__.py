from bempy.example import Base

class Base(Base()):
    def init(self):
        print(self.name + ':', 'Child init')


