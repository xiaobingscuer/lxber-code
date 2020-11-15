#!/usr/bin/python
# coding=utf-8

"""
命令模式

1. 解决 在应用中实现撤销（等其他操作）功能,调用命令的对象与知道如何执行命令的对象解耦

2. 命令设计模式帮助我们将一个操作（撤销、重做、复制、粘贴等）封装成一个对象。
    简而言之，这意味着创建一个类，包含实现该操作所需要的所有逻辑和方法。这样做的优势如下所述：
    a. 我们并不需要直接执行一个命令。命令可以按照希望执行。
    b. 调用命令的对象与知道如何执行命令的对象解耦。调用者无需知道命令的任何实现细节。
    c. 如果有意义，可以把多个命令组织起来，这样调用者能够按顺序执行它们。例如，在实现一个多层撤销命令时，这是很有用的。

3. 许多开发人员以为撤销例子是命令模式的唯一应用案例。撤销操作确实是命令模式的杀手级特性，
    然而命令模式能做的实际上还有很多:
    1) GUI按钮和菜单项：前面提过的PyQt例子使用命令模式来实现按钮和菜单项上的动作。
    2) 其他操作：除了撤销，命令模式可用于实现任何操作。其中一些例子包括剪切、复制、粘贴、重做和文本大写。
    3) 事务型行为和日志记录：事务型行为和日志记录对于为变更记录一份持久化日志是很重
    要的。操作系统用它来从系统崩溃中恢复，关系型数据库用它来实现事务，文件系统用它来实现快照，
    而安装程序（向导程序）用它来恢复取消的安装。
    4) 宏：在这里，宏是指一个动作序列，可在任意时间点按要求进行录制和执行。流行的编辑器（比如，Emacs和Vim）都支持宏。

4. 命令模式。使用这种设计模式，可以将一个操作（比如，复制/粘贴）封装为一个对象。这样能提供很多好处，如下所述。
    1)我们可以在任何时候执行一个命令，而并不一定是在命令创建时。
    2)执行一个命令的客户端代码并不需要知道命令的任何实现细节。
    3)可以对命令进行分组，并按一定的顺序执行。

5. 虽然至今命令模式最广为人知的特性是撤销操作，但它还有更多用处。一般而言，要在运行
    时按照用户意愿执行的任何操作都适合使用命令模式。命令模式也适用于组合多个命令。这有助
    于实现宏、多级撤销以及事务。一个事务应该：要么成功，这意味着事务中所有操作应该都成功
    （提交操作）；要么如果至少一个操作失败，则全部失败（回滚操作）
"""

import os

verbose = True


class RenameFile:
    """ 命令类 """
    def __init__(self, path_src, path_dest):
        self.src, self.dest = path_src, path_dest

    def execute(self):
        if verbose:
            print("[renaming '{}' to '{}']".format(self.src, self.dest))
            os.rename(self.src, self.dest)

    def undo(self):
        if verbose:
            print("[renaming '{}' back to '{}']".format(self.dest, self.src))
            os.rename(self.dest, self.src)


class CreateFile:
    def __init__(self, path, txt='hello world\n'):
        self.path, self.txt = path, txt

    def execute(self):
        if verbose:
            print("[creating file '{}']".format(self.path))
            with open(self.path, mode='w', encoding='utf-8') as out_file:
                out_file.write(self.txt)

    def undo(self):
        delete_file(self.path)


class ReadFile:
    def __init__(self, path):
        self.path = path

    def execute(self):
        if verbose:
            print("[reading file '{}']".format(self.path))
        with open(self.path, mode='r', encoding='utf-8') as in_file:
            print(in_file.read(), end='')


def delete_file(path):
    """
    文件删除功能不是类。我们可以创建另一个函数来处理撤销操作，但创建一个类是更好的方式
    并且也让代码更统一
    """
    if verbose:
        print("deleting file '{}'".format(path))
    os.remove(path)


def main():
    orig_name, new_name = 'file1', 'file2'
    commands = []
    for cmd in CreateFile(orig_name), ReadFile(orig_name), RenameFile(orig_name, new_name):
        commands.append(cmd)
    [c.execute() for c in commands]
    answer = input('reverse the executed commands? [y/n] ')
    if answer not in 'yY':
        print("the result is {}".format(new_name))
        exit()
    for c in reversed(commands):
        try:
            c.undo()
        except AttributeError as e:
            pass


if __name__ == "__main__":
    main()
