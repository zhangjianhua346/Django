from django.template import Library
register = Library()
@register.filter
def markdown(value):
    """自定义Markdown过滤器，后面引用这个过滤器的变量就是这个value"""
    import markdown
    return markdown.markdown(value)

@register.filter
def splitstr(value,args):
    """自定义带参数的过滤器,{{ str|splitstr:'1,3' }}"""
    start,end = args.split(',')
    content = value.encode('utf-8').decode('utf-8')#将默认的UCode编码转换成utf-8编码解码
    return value[int(start):int(end)]