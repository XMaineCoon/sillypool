class A:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return A()


print(type(A))
a = A
print(type(a))
a = A()
print(type(a))
b = a()
print(type(b))
