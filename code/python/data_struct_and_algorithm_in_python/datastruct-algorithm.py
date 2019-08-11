 
# data structure and algorithm in python
# 有价值的参考源：http://www.madmalls.com/blog/post/finding-the-largest-or-smallest-n-items-in-a-python3-collection/

class Module():

    def __init__(self, id, name, path):
        self.id = id
        self.name = name
        self.path = path

    def __str__(self):
        return str(self.id)+" "+self.name+" "+self.path

if __name__=='__main__':

    # 排序-自定义对象列表的排序
    # 1.借助列表的排序方法list.sort()
    # 2.使用sorted函数，该函数不改变原始容器的值，而是返回一个新建立的排好序的容器
    modules=[]
    for i in range(10):
        modules.append( Module(9-i,"xiaobing"+str(i),"D:\lxb\lxb-coder\python"))

    print("原始modules")
    for module in modules:
        print(module)
        
    modules.sort(key = lambda x:x.id, reverse = False)

    print("list.sort()排序后的modules")
    for module in modules:
        print(module)

    modules_new = sorted(modules, key = lambda x:x.id, reverse = True)

    print("sorted()排序后的modules")
    for module in modules:
        print(module)

    print("sorted()排序后的新的modules")
    for module in modules_new:
        print(module)

    

    
    
