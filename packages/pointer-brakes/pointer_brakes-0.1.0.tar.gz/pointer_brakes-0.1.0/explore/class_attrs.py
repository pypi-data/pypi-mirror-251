from typing import get_type_hints


class Foo:
    class_attr: int
    untyped_attr = "bar"

    def __init__(self):
        self.class_attr = 1
        self.undefined_attr = 2.0

    def __setattr__(self, name, value):
        if hasattr(self, name):
            object.__setattr__(self, name, value)
        elif name in get_type_hints(self):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(self, name)


foo1 = Foo()
foo2 = Foo()

foo1.class_attr = 22
Foo.class_attr = 59

foo3 = Foo()

print(f"DEBUG foo1.class_attr={foo1.class_attr} foo2.class_attr={foo2.class_attr} foo3.class_attr={foo3.class_attr}")
print(f"DEBUG type hints for foo3 {get_type_hints(foo3)}")
