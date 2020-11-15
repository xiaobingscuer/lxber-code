#!/usr/bin/python
# coding=utf-8

"""
责任链模式

1. 解决 多个处理程序，但不知道是哪个

2. 责任链用于让多个对象来处理单个请求时，或者用于预先不知道应该由哪个对象（来自某个对象链）来处理某个特定请求时
    其原则如下所示。
    (1) 存在一个对象链（链表、树或任何其他便捷的数据结构）。
    (2) 我们一开始将请求发送给链中的第一个对象。
    (3) 对象决定其是否要处理该请求。
    (4) 对象将请求转发给下一个对象。
    (5) 重复该过程，直到到达链尾。

3. 如果所有请求都能被单个处理程序处理，责任链就没那么有用了，除非确实
    不知道会是哪个程序处理请求。这一模式的价值在于解耦。客户端与所有处理程序（一个处理程
    序与所有其他处理程序之间也是如此）之间不再是多对多关系，客户端仅需要知道如何与链的起
    始节点（标头）进行通信。

4. 在无法预先知道处理程序的数量和类型时，该模式有助于对请求/处理事件进行建模。
    适合使用责任链模式的系统例子包括基于事件的系统、采购系统和运输系统。
    在责任链模式中，发送方可直接访问链中的首个节点。若首个节点不能处理请求，则转发给
    下一个节点，如此直到请求被某个节点处理或者整个链遍历结束。这种设计用于实现发送方与接
    收方（多个）之间的解耦。

"""


class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Widget:
    def __init__(self, parent=None):
        self.parent = parent

    def handle(self, event):
        handler = 'handle_{}'.format(event)
        if hasattr(self, handler):
            method = getattr(self, handler)
            method(event)
        elif self.parent:
            self.parent.handle(event)
        elif hasattr(self, 'handle_default'):
            self.handle_default(event)


class MainWindow(Widget):
    def handle_close(self, event):
        print('MainWindow: {}'.format(event))

    def handle_default(self, event):
        print('MainWindow Default: {}'.format(event))


class SendDialog(Widget):
    def handle_paint(self, event):
        print('SendDialog: {}'.format(event))


class MsgText(Widget):
    def handle_down(self, event):
        print('MsgText: {}'.format(event))


def main():
    mw = MainWindow()
    sd = SendDialog(mw)
    msg = MsgText(sd)

    for e in ('down', 'paint', 'unhandled', 'close'):
        evt = Event(e)
        print('\nSending event -{}- to MainWindow'.format(evt))
        mw.handle(evt)
        print('Sending event -{}- to SendDialog'.format(evt))
        sd.handle(evt)
        print('Sending event -{}- to MsgText'.format(evt))
        msg.handle(evt)


if __name__ == '__main__':
    main()

