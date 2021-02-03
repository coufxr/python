# python
py的学习记录

### 二维列表排序方式
>sorted(listName,key=(lambda x:[y]))
 1. [~]中可以添加多个值，值的顺序为排序的优先级  
 2. [~]中可以遍历x，即：x:[x[0]]

### 文件夹中文件名的获取

### 1. 嵌套版  

##### 带路径获取
 ```python
def get_filepath(path):
    for root, dirs, files in os.walk(path, True):
        for name in files:
            filepath = os.path.join(root, name)
```
 - os.path.join(root, f)表示将文件夹路径和文件名相加

 ### 2. 不嵌套
1. 也带路径获取，但只会获取当前文件夹中，不包括下一级文件夹  
2. 使用了re 正则进行筛选匹配
 ```python
def get_filepath(path):
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if re.search(r'.xls$', filepath) != None:
            print(filepath)
```
### re 正则
```
re.match(r'[\u4e00-\u9fa5]', str)
```
- [\u4e00-\u9fa5] 匹配中文字符