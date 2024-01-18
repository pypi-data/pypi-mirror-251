class hello:
    print('HIII')
    def add(self, num1, num2):
        return num1 + num2

'''a = Hello()
result = a.add(5, 3)
print(result)
'''
class Hello:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}!")

    def add(self, num1, num2):
        return num1 + num2
