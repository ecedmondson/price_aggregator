class Foo():
    subclass = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "name" in cls.__dict__:
            cls.subclass.append({cls.name: cls}

class Bar(Foo):
    name = "bar"

print(Foo.subclass)
b = Bar()
print(dir(b))
print(b.__class__)
