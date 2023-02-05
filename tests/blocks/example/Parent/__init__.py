from bempy import Block
from bempy.example import Base

class Base(Block):
    inherited = [Base]

    def prepare(self):
        print(self.name + ':', 'Parent prepare')

