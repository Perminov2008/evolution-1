class A:
    def __init__(self, x):
        self.x = x

    def change(self):
        a[0] = None
        a[2] = self


a = [A(1), A(2), None]
a[0].change()

for i in a:
    if i is not None:
        print(i.x)