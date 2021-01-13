from jinja2 import Environment, PackageLoader


def render(params: dict, template: str) -> str:
    """
    :param params: 渲染参数
    :param template: 模板文件名
    :return: 渲染后的文本文件
    """

    env = Environment(
        loader=PackageLoader('templates', ''),
    )
    template = env.get_template(template)
    return template.render(params)

# a = render({"sample_list": [123,456,789],"ctrl":"sdlfjsldfjlsdjfl"})
# print(a)
