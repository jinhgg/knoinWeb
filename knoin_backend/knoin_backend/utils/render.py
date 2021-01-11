from jinja2 import Environment, FileSystemLoader


def render(params: dict) -> str:
    """
    :param params: 渲染参数
    :return: 渲染后的文本文件
    """

    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(searchpath="../../templates")
    # 用加载器创建一个环境, 有了它才能读取模板文件
    env = Environment(loader=loader)
    # 调用 get_template() 方法加载模板并返回
    template = env.get_template('mngs_sh_template.sh')
    # 用 render() 方法渲染模板
    # 可以传递参数
    return template.render(params)


a = render({"sample_list": [123,456,789],"ctrl":"sdlfjsldfjlsdjfl"})
print(a)
