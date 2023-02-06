from bempy import Block
from bempy.example import Base

class Base(Block):
    inherited = [Base]

    def init(self):
        print(self.name + ':', 'Parent init')


