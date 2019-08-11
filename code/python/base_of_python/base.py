
# base of python

def get_attrs(atr1,atr2 = 2,*atr3,**atr4):
    print("atr1: ",atr1)
    print("atr2: ",atr2)
    print("atr3: ",atr3)
    print("atr4: ",atr4)
    return atr4

if __name__=='__main__':

    # 打印输出
    print("hello,python! I am %s" % "xiaobing")

    d = 3
    s = "today is %d day" % (d) +" in this week."
    print(s)

    print(None)
    print(NotImplemented)
    print(Ellipsis)

    # 三元表达式
    a = 10
    a = "lxber" if a > 3 else "xiaobing"
    print(a)


    # zip lambda map
    a = [1, 2, 3]
    b = [4, 5, 6]
    ab = zip(a, b) #zip，同位合并成tuple
    #print(list(ab)) # [(1,4),(2,5),(3,6)]
    for i,j in ab:
        print(i/2,j//2)

    add = lambda x, y : x + y # 使简单功能的代码实现更简单
    print(add(1,2))

    print(list(map(add,[1,2,3],[2,3,4]))) # map使函数和参数绑定在一起


    #  tuple & list & dict & set
    a_tuple = (1,2,3,4) # tuple与list的区别是tuple一旦创建便是不可变的，不可变是指指向元素的引用不变

    a_list = [4,5,6,7]
    b=[[1,2,3],[4,5,6],[7,8,9]]
    for i in range(3):
        for j in range(3):
            print(b[i][j])
            
    d={'name':'lixiaobing','age':27,'sex':'femeal'}
    print(d['name'])
    for k, v in d.items():
        print(k,v)

    dt = {}
    id = [2,3,4,5,6,7,8,9,10,11,12,13]
    seqid = ['d1','c1','a1','b1','b1','c1','c1','a1']
    seq = ['a','b','c','c','a','b','c','b']
    seq1 = ['a1','b1','c1','d1']

    ## 二级字典创建方式一：
    ## 第一步，先创建完整字典
    dt = {}
    for i in range(3):
        dt[seq[i]] = {}
        for sq in seq1:
            dt[seq[i]][sq] = []
        if 'total' not in dt[seq[i]]:
            dt[seq[i]]['total'] = i
    
    ## 第二步，通过数据为字典添加元素
    for i in range(len(seqid)):
        key = seq[i]
        key1 = seqid[i]
        data = id[i]
        dt[key][key1].append(data)

    for k,v in dt.items():
        print(k,v)

    ## 二级字典创建方式二：
    ## 通过数据直接创建字典并为字典添加元素
    dt = {}
    for i in range(len(seqid)):
        key = seq[i]
        key1 = seqid[i]
        data = id[i]
        if key not in dt:
            dt[key] = {}
        if key1 not in dt[key]:
            dt[key][key1] = []
        dt[key][key1].append(data)
            
    for k,v in dt.items():
        print(k,v)

    print(dt.get('a').get('c1')) #default:None

    if dt.get('a').get('c1') == None:
        print("if key is not in dict, the value is None")

    print(dt.get('a').get('c1', 0)) #default:0

    print(dt.get('d',{}).get('c1', 0)) #打印0,因此默认值和

    print(len([]))

    numbers=[2,1,2,4,3,3,1,4,4,6.6,5.5,7.7,7.7,5.5,6.6]
    chars=['a','a','b','b','c','c','c','z','z','o']
    content="welcome back to this tutorial"
    chars_content = chars + list(content)
    print(set(numbers)) # 元素为数值类型，set后可以保证有序
    print(set(chars)) # set去重，set后并不能保证顺序
    print(set(content))
    print(set(chars_content))

    print(set(content).difference(set(chars)))   # 补集
    print(set(content).intersection(set(chars))) # 交集
    print(set(content) | set(chars))   # 并集
    print(set(content) - set(chars))   # 补集
    print(set(content) & set(chars))   # 交集
    

    ## 异常处理，程序不因异常而中断
    # try...执行语句...except...(异常类型1,2..)...as e...异常处理...else...没异常时执行语句...
    try:
        file = open('file.txt','r+')
    except Exception as e:
        print(e)
        response = input('do you want to create a new file:')
        if response == 'y':
            file = open('file.txt','w+')
        else:
            pass
    else:
        file.write('hello')
        file.close()


    # 自调用实现单元测试，
    # if __name__='__main()__':
    #       code_here
    # 如果执行该脚本的时候，该 if 判断语句将会是 True,那么内部的代码将会执行。 如果外部调用该脚本，if 判断语句则为 False,内部代码将不会执行
    
    # 函数非默认参数、默认参数,默认参数必须在非默认参数后面

    # 可变参数,必须在特定参数和默认参数后面
    # def func_name(name, *args):
    #       for arg in args:
    #           ...
    # 调用示例：func_name(name,1,2) func_name(name,3,4,5,6)

    # 关键字参数，必须在最后面,
    # def func_name(name, **kvargs):
    #       for k, v in kvargs.items():
    #           ...
    # 调用示例，result=func_name(name, id=1, age=27,country='china')
    # 原理，对传入的参数函数内部自动封装成字典

    # 通过可变对象和关键字对象可以概括出函数参数的通用形式
    # def func_name(name, id=1, *args, **kvargs):
    #       ...

    atr1 = 1
    atr2 = 3
    atr3 = [1,2,3]
    atr4 = {'a':1,'b':2}
    get_attrs(atr1,atr2,atr3,atr4)
    get_attrs(atr1,atr3,atr4)
    get_attrs(atr1,*atr3,atr4)
    get_attrs(atr1,atr2,*atr4)
    get_attrs(atr1,atr2,**atr4)
    get_attrs(atr1,atr2,atr3,atr4,name = 'xiaobing',age = 27)
    

    # 可迭代对象，设置迭代器
    # 需要实现__iter__和__next__函数
    class Fib(object):
        def __init__(self, max):
            self.max = max
            self.n, self.a, self.b = 0,0,1

        def __iter__(self):
            return self

        def __next__(self):
            if self.n < self.max:
                r = self.b
                self.a, self.b = self.b, self.a+self.b
                self.n = self.n +1
                return r
            raise StopIteration()

    for i in Fib(5):
        print(i)

    # 可迭代对象，设置生成器yield
    # yield 语句每次 执行时，立即返回结果给上层调用者，而当前的状态仍然保留，以便迭代器下一次循环调用。这样做的 好处是在于节约硬件资源，在需要的时候才会执行，并且每次只执行一次
    def fib(max):
        a,b=0,1
        while max:
            r=b
            a,b=b,a+b
            max-=1
            yield r
    for i in fib(5):
        print(i)

    
    # 正则表达式
    # 字符串匹配
    pattern1 = 'cat'
    pattern2 = 'bird'
    string = "dog runs to cat"
    print(pattern1 in string)
    print(pattern2 in string)

    # 正则表达式的简单匹配
    # re.search()
    import re
    print(re.search(pattern1,string))
    print(re.search(pattern2,string))

    # 灵活匹配
    # []囊括可能的字符
    pattern = r"r[au]n"
    print(re.search(pattern,"dog runs to cat"))

    print(re.search(r"r[A-Z]n","dog runs to cat"))
    print(re.search(r"r[a-z]n","dog runs to cat"))
    print(re.search(r"r[0-9]n","dog r2ns to cat"))
    print(re.search(r"r[a-z0-9]n","dog runs to cat"))

    # 按类型匹配
    # \d : 任何数字
    # \D : 不是数字
    # \s : 任何 white space, 如 [\t\n\r\f\v]
    # \S : 不是 white space
    # \w : 任何大小写字母, 数字和 “” [a-zA-Z0-9]
    # \W : 不是 \w
    # \b : 空白字符 (只在某个字的开头或结尾)
    # \B : 空白字符 (不在某个字的开头或结尾)
    # \\ : 匹配 \
    # . : 匹配任何字符 (除了 \n)
    # ^ : 匹配开头
    # $ : 匹配结尾
    # ? : 前面的字符可有可无
    #
    # \d: 任何数字
    print(re.search(r"r\dn","run r4n"))
    # \D: 不是数字
    print(re.search(r"r\Dn","run r4n"))
    # \s: 任何空白字符
    print(re.search(r"r\sn","r\nn r4n"))
    # \S: 不是空白字符
    print(re.search(r"r\Sn","r\nn r4n"))
    # \w: [a-zA-Z0-9]
    print(re.search(r"r\wn","r\nn r4n"))
    # \W: 不是\w
    print(re.search(r"r\Wn","r\nn r4n"))
    # \b: 空白字符，但是只在某个字的开头或结尾
    print(re.search(r"\bruns\b","dog runs to cat"))
    # \B: 不是\b
    print(re.search(r"\Bruns\B","dog_runs_to cat"))
    # \\: 匹配特殊字符'\'
    print(re.search(r"runs\\","dog runs\ to cat"))
    # .: 匹配除了\n的字符
    print(re.search(r"r.n","r[ns to me"))
    # ^: 匹配开头
    print(re.search(r"^dog","dog runs to cat"))
    # $: 匹配结尾
    print(re.search(r"cat$","dog runs to cat"))
    # ?: ?前面的字符可有可无
    print(re.search(r"Mon(day)?","Monday"))
    print(re.search(r"Mon(day)?","Mon"))

    # 多行匹配
    string = """
dog runs to cat.
I run to dog

    """
    print(string)
    print(re.search(r"^I",string))
    print(re.search(r"^I",string,flags = re.MULTILINE)) #flags = re.MULTILINE

    # 重复匹配
    # *: 重复零次或多次
    # +：重复一次或多次
    # {n,n}: 重复n至m次
    # {n}: 重复n次
    #
    # *: 重复零次或多次
    print(re.search(r"ab*","a"))
    print(re.search(r"ab*","abbbbb"))
    # +：重复一次或多次
    print(re.search(r"ab+","a"))
    print(re.search(r"ab+","abbbbb"))
    # {n}: 重复n次
    print(re.search(r"ab{5}","abbbbb"))
    # {n,n}: 重复n至m次
    print(re.search(r"ab{2,10}","abbbbb"))

    # 分组()
    match = re.search(r"(\d+),Date:(.+)", "ID:021523,Date:Feb/12/2017")
    print(match.group())
    print(match.group(1))
    print(match.group(2))
    # 给分组起个名字(?P<name> )
    match = re.search(r"(?P<id>\d+),Date:(?P<date>.+)", "ID:021523,Date:Feb/12/2017")
    print(match.group("id"))
    print(match.group("date"))

    # findall: 找到所有的匹配项，不止第一个匹配项
    print(re.findall(r"r[ua]n","run ran ren"))
    # (a|b): a or b
    print(re.findall(r"(ran|run)","run ran ren"))

    # re.sub(): 替换匹配上的字符串,比python自带的string.replace()灵活
    print(re.sub(r"r[au]ns","catches","dog runs to cat")) # catches为替换后的值

    # re.split("xxx"): 分割字符
    print(re.split(r"[,;\.]","a;b,c.d;e"))

    # re.compile(): 重复使用正则模式
    compile_re = re.compile(r"r[ua]n")
    print(compile_re.search("dog ran to cat"))
    print(compile_re.search("dogs run to cats"))

    # 更多的正则，可以在网上搜索
    
          

    # 赋值= & 浅拷贝copy & 深拷贝deepcopy

    # 导包

    # python中的面向对象：封装、继承（派生）、多态

    # 对象设计

    # 日志

    
    
