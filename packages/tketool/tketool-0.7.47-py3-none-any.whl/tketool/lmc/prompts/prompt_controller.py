# pass_generate
import time

from tketool.files import *
import importlib.resources, os


def get_prompt(key: str, lang="english", return_details=False, folder=None):
    """
    `get_prompt`函数是用于获取提示文件的内容的函数。
    
    参数:
        key (str): 提示文件的键值。
        lang (str, 可选): 提示文件的语言版本，默认为 "english"。
        return_details (bool, 可选): 是否返回提示文件的详细内容，如果为 False，只返回文件中的模板字符串，默认为 False。
        folder (str, 可选): 提示文件所在的文件夹路径，默认为 None，表示提示文件在安装包中。
    
    返回:
        str 或 dict: 如果`return_details`为 True，返回提示文件的详细内容，类型为字典；否则只返回文件中的模板字符串，类型为字符串。
    
    raise:
        IOError: 如果无法找到指定的文件，或者读取文件出错。
    
    注意:
        此函数将尝试从指定的文件夹或安装的包中获取提示文件。所以如果你安装了此包，请确保提示文件存在于正确的位置，否则可能会引发 IOError。
    
    示例:
    
        get_prompt('welcome', return_details=True)
        # 返回 {'templatestr': 'Welcome to our system!', 'details': 'This is the welcome message showed to the user when they log in.'}
    """

    def get_file_path(lang, key):
        """
        这个函数是用来获取文件路径的。给定语言和键，它会构造出对应的文件路径。
        
        参数:
            lang: str类型。文件的语言，例如"english"、"chinese"等。
            key: str类型。文件的名称，不包含文件扩展名。例如，如果文件的全名为"example.txt"，那么键应该是"example"。
        
        返回:
            返回一个由importlib.resources.files('tketool').joinpath生成的文件路径。
        
        注意:
            这个函数假设所有的文件都存放在"lmc/prompts/templates"目录下，并且文件的扩展名都是".txt"。
            在非DEBUG模式下，这个函数会从tketool包中寻找文件。因此，这个函数只能在安装了tketool包的环境中运行。
        
        示例:
            get_file_path("chinese", "example")返回的是"lmc/prompts/templates/chinese/example.txt"
        """

        path = os.path.join("lmc", "prompts", "templates", lang, f"{key}.txt")
        # 非DEBUG模式，我们试图从安装的包中获取文件
        return importlib.resources.files('tketool').joinpath(path)

    if folder is None:
        path = get_file_path(lang, key)
    else:
        path = os.path.join(folder, lang, f"{key}.txt")
    doc = read_prompt_file(path)
    if return_details:
        return doc
    else:
        return doc['templatestr']


def read_prompt_file(path) -> dict:
    """
    这个函数的主要作用是读取给定路径下的文件，解析其内容并以字典的形式返回。文件的内容主要包括：版本号、介绍、参数和模板字符串。
    
    参数:
        path (str): 文件的路径。
    
    返回:
        dict: 一个字典，包含版本号（version）、介绍（description）、参数（params）和模板字符串（templatestr）。
    
    文件的格式应该如下：
    
        version 1.0
        这是介绍
        参数1: 参数值1
        参数2: 参数值2
        start
        这是模板字符串
    
    这个函数首先会读取文件的所有行，然后依次处理每一行。在处理过程中，首先会获取版本号，然后是介绍，接着是参数。参数的处理会持续到遇到以'start'开头的行为止。最后，从'start'开始后的所有行会被处理为模板字符串。
    
    示例:
    
        output = read_prompt_file('/path/to/file')
        print(output)
        # 输出:
        # {
        #     'version': '1.0',
        #     'description': '这是介绍',
        #     'params': {
        #         '参数1': '参数值1',
        #         '参数2': '参数值2'
        #     },
        #     'templatestr': '这是模板字符串'
        # }
    
    注意:
    
        如果文件的格式不符合预期，这个函数可能会产生不可预知的行为。例如，如果没有'start'这一行，那么所有的行都会被当作参数来处理。如果参数没有用':'来分隔，那么处理参数的部分可能会出错。
    
    """

    lines = read_file_lines(path)

    output_dict = {}
    params_dict = {}

    # 处理版本号
    version = lines[0].strip().split(' ')[1]
    output_dict['version'] = version

    # 处理介绍
    description = lines[1].strip()
    output_dict['description'] = description

    line_index = 2
    while True:
        current_line = lines[line_index].strip()

        # 当遇到固定的'start'时，停止处理参数
        if current_line.startswith("start"):
            break

        # 处理参数
        key_value = current_line.split(':')
        params_dict[key_value[0].strip()] = key_value[1].strip()

        line_index += 1

    output_dict['params'] = params_dict

    # 处理模板字符串
    template_str = '\n'.join(lines[line_index + 1:]).strip()
    output_dict['templatestr'] = template_str

    return output_dict


def write_prompt_file(path, version, des, params: {}, str_template):
    """
    这个函数是用于生成一个带有版本信息、描述、参数信息和模板的文件。通过这个函数，我们可以方便的创建用于自动生成文件的模板。
    
    参数:
        path (str): 要写入文件的路径。
        version (str): 版本信息。
        des (str): 文件描述信息。
        params (dict): 参数列表，字典形式，包含参数的名称和对应的值。
        str_template (str): 用于生成文件的模板。
    
    返回类型:
        无返回值。
    
    使用示例:
        ```python
        path = './prompt.txt'
        version = '1.0'
        des = 'This is a prompt file.'
        params = {'author': 'admin', 'date': '2021-01-01'}
        str_template = 'Hello, world!'
        write_prompt_file(path, version, des, params, str_template)
        ```
    """

    lines = []
    lines.append(f"version {version}")
    lines.append(des)
    for k, v in params.items():
        lines.append(f"{k}: {v}")
    lines.append("start:")
    lines.append(str_template)

    write_file_line(path, lines)
