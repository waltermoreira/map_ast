
class Foo(object):

    def __init__(self, a, b):
        x = 4
        self.y = 'foo'
        self.u = {}
        print(self.y)

    def bar(self, a, b):
        print self.u

    def spam(self, x):
        self.u = 4
        def inner(y):
            return y + x

        self.x = inner(x)


class Bar(object):

    def __init__(self, a, b):
        pass
