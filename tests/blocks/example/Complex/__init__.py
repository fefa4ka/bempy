from bempy.example import Child

class Base(Child()):
    complex_param = 'lala'

    def init(self):
        print(self.name + ':', 'Complex init')



