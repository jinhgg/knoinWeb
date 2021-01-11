from jinja2 import Environment, PackageLoader


def render(params: dict) -> str:
    """
    :param params: 渲染参数
    :return: 渲染后的文本文件
    """

    env = Environment(
        loader=PackageLoader('templates', ''),
    )
    template = env.get_template('mngs_sh_template.sh')
    return template.render(params)


#a = render({"sample_list": [123,456,789],"ctrl":"sdlfjsldfjlsdjfl"})
#print(a)

