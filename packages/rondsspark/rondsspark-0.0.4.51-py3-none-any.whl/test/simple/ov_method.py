class ObjectA:

    def __init__(self, obj):
        def f(*args, **kwargs):
            getattr(obj, 'method')(*args, **kwargs)

        setattr(self, 'method', f)

    def method2(self):
        print("Object A's method2")

    def method(self, a, b, c=1):
        print("Object A's method: %d, %d, %d" % (a, b, c))
        self.method2()

class ObjectB:

    def method2(self):
        print("Object B's method2")

    def method(self, a, b, c=1):
        print("Object B's method: %d, %d, %d" % (a, b, c))
        self.method2()


if __name__ == '__main__':
    objA = ObjectA(ObjectB())
    objA.method(1, 1, c=2)
