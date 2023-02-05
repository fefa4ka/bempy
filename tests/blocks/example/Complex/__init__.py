from bempy.example import Child

class Base(Child()):
    complex_param = 'lala'

    def prepare(self):
        print(self.name + ':', 'Complex prepare')


