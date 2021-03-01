class Person:
    # 面对对象
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def cat(self):
        print(f'{self.name}正在吃臭豆腐')

    def run(self):
        print(f'{self.name}今年{self.age}岁了，正在跑步')


name = input('请输入名字:')
age = input('请输入你的年龄:')
p = Person(name, age)
p.cat()
p.run()
