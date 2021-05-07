# 装饰器
# 将被装饰的函数当做参数传替给与装饰器对应的函数（名称相同的函数），并返回包装后的被装饰的函数
# 被装饰器修饰的函数具有相同特定的功能
"""# 1、二阶装饰器"""
def a(func):
    def _wrapper(*args, **kwargs):
        content = func(*args, **kwargs)  # 调用b函数
        return '<b>%s</b>' % content
    return _wrapper
@a  # b函数会作为a函数的入参
def b():
    return 'helloword!'

'# 2、三阶装饰'
def c(bold=True):
    def _wrapper(func):
        def _wrapper(*args, **kwargs):
            content = func(*args, **kwargs)  # 调用b函数
            if bold:
                return '<b>%s</b>' % content
            else:
                return '<i>%s</i>' % content
        return _wrapper
    return _wrapper
@c(bold=False)
def d():
    return 'helloword!'
