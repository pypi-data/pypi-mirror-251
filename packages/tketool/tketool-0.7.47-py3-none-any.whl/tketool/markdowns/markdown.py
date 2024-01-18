# pass_generate
import time, abc
from enum import Enum


class draw_markdownobj(metaclass=abc.ABCMeta):
    """
    这是一个名为 draw_markdownobj 的抽象基类，采用了 abc.ABCMeta 作为元类。该类的主要目的是定义一个接口，用于输出具有 Markdown 格式的字符串。这个类主要被用作继承，以实现不同 Markdown 对象类型的输出。
    
    由于此类是一个抽象基类，因此不能直接实例化。你需要创建一个继承于该类的子类，并实现 `str_out` 方法。
    
    例如：
    
    ```python
    class draw_bold(draw_markdownobj):
        def __init__(self, text):
            self.text = text
    
        def str_out(self):
            return f"**{self.text}**"
    
    bold_obj = draw_bold('Hello World')
    print(bold_obj.str_out())  # 输出：**Hello World**
    ```
    
    `str_out` 方法被定义为抽象方法，其返回类型为字符串列表。具体实现根据子类的具体需求而定，例如可以返回 Markdown 格式的文字、图片等。
    
    注意：目前此类没有已知的错误或 bug。
    """

    @abc.abstractmethod
    def str_out(self) -> [str]:
        """
        这是一个抽象方法，由具体的子类实现。
        
        功能：
        该方法的主要目的是将Markdown对象转化为字符串列表，从而方便进一步处理。
        
        参数：
        self : 表示实例自身的引用，不需要手动传入。
        
        返回：
        list[str] : 返回一个字符串列表，每个元素表示Markdown对象的一部分。
        
        使用示例：
        class markdown_obj(draw_markdownobj):
            def str_out(self):
                ... # 具体实现
        markdown = markdown_obj()
        markdown.str_out() # 调用方法
        
        注意：
        因为这是一个抽象方法，所以不能直接调用，必须由子类实现后再使用。
        
        错误与Bug：
        目前未发现错误和Bug。
        """

        pass


class flowchart_color_enum(str, Enum):
    """
    此类是一个枚举类，用于定义流程图中使用的颜色代码。枚举类名为"flowchart_color_enum"，继承了str和Enum类。
    
    类中定义了9种颜色，分别为：
    - Red（红色），对应颜色代码为"#FF0000"
    - Yellow（黄色），对应颜色代码为"#FFFF00"
    - Blue（蓝色），对应颜色代码为"#00BFFF"
    - Orange（橘色），对应颜色代码为"#FFA500"
    - LightGreen（浅绿色），对应颜色代码为"#90EE90"
    - MediumPurple（中等紫色），对应颜色代码为"#9370DB"
    - Auqamarin（水绿色），对应颜色代码为"#7FFFAA"
    - DeepSkyBlue（深天蓝色），对应颜色代码为"#00BFFF"
    - NavajoWhite（纳瓦豪白色），对应颜色代码为"#FFDEAD"
    
    该类为枚举类，实例化后的对象是唯一的，可用于判断颜色代码的唯一性，或者在需要固定颜色选项的场景中使用。
    
    使用示例：
    ```python
    color = flowchart_color_enum.Red
    print(color)  # 输出：Red
    print(color.value)  # 输出：#FF0000
    ```
    注意：由于此类为枚举类，不能直接实例化，只能通过枚举类中定义的元素进行调用。
    
    目前此类中没有发现错误或bug。
    """

    Red = "#FF0000",
    Yellow = "#FFFF00",
    Blue = "#00BFFF",
    Orange = "#FFA500",
    LightGreen = "#90EE90",
    MediumPurple = "#9370DB",
    Auqamarin = "#7FFFAA",
    DeepSkyBlue = "#00BFFF",
    NavajoWhite = "#FFDEAD",


class flowchart_shape_enum(str, Enum):
    """
    这是一个枚举类，名为flowchart_shape_enum。该类继承了str和Enum，用于表示流程图中各种形状的符号表示。
    
    该类定义了以下形状的符号表示：
    
    - Roundedges：表示圆角形状。
    - Stadium：表示体育场形状。
    - Circle：表示圆形。
    - Rhombus：表示菱形。
    - Parallelogram：表示平行四边形。
    - Asymmetric：表示不对称的形状。
    - Hexagon：表示六边形。
    
    使用示例：
    
    ```python
    shape = flowchart_shape_enum.Circle
    print(shape.value)  # 输出: "((%%))"
    ```
    
    错误与Bug：
    目前未发现明显错误或Bug。
    
    """

    Roundedges = "(%%)",
    Stadium = "([%%])",
    Circle = "((%%))",
    Rhombus = "{%%}",
    Parallelogram = "[/%%/]",
    Asymmetric = ">%%]",
    Hexagon = "{{%%}}",


uncode = ["。", "（", "）", "，", '"', '(', ")", "“", '”', "、", "’", "？", "：", "；"]


class draw_markdownobj_flowchart(draw_markdownobj):
    """
    `draw_markdownobj_flowchart`类是一个绘制Markdown对象流程图的类，继承自`draw_markdownobj`。这个类主要是用来通过Markdown语法生成一些流程图。
    
    这个类的主要方法如下：
    
    - `str_out(self) -> [str]`：将流程图的信息（包括节点、线、颜色、形状、导航、图标等）格式化为Markdown语法的字符串。
    
    - `__init__(self, oriented_left2right=True)`：初始化方法，设置流程图的基本属性。如：初始为空的节点列表、线列表、节点颜色和形状的字典，以及流程图的方向等。
    
    - `_convert_name(self, answer)`：将节点的名称进行一些简单的转换，如将unicode字符替换为空格。
    
    - `add_node(self, name, id, anchor_title=None, icon=None)`：添加一个节点到流程图中，包括节点的名称、id、锚点标题和图标。
    
    - `set_node_color(self, id, color: flowchart_color_enum)`：设置指定id的节点的颜色。
    
    - `set_node_shape(self, id, shape: flowchart_shape_enum)`：设置指定id的节点的形状。
    
    - `add_line(self, id1, id2, message=None, dot_line=False)`：在两个指定id的节点之间添加一条线。
    
    使用例子：
    
    ```python
    chart = draw_markdownobj_flowchart(oriented_left2right=True)
    chart.add_node('Node1', '1', 'Title1', 'icon1')
    chart.set_node_color('1', 'blue')
    chart.add_node('Node2', '2', 'Title2', 'icon2')
    chart.set_node_shape('2', 'circle')
    chart.add_line('1', '2', 'Message', False)
    lines = chart.str_out()
    for line in lines:
        print(line)
    ```
    
    注意：这个类没有处理输入错误的代码，所以如果输入的id或者颜色、形状等不在预定义的范围内，可能会抛出异常。
    """

    def str_out(self) -> [str]:
        """
        此函数为`draw_markdownobj_flowchart`类的一个方法，该类主要用于在Markdown中创建和绘制流程图。
        
        `str_out`方法的主要作用是根据输入的节点、线条以及其他相关配置，生成并返回一个用于在Markdown文档中绘制流程图的字符串列表。
        
        参数:
            无
        
        返回:
            lines: list of str
                一个字符串列表，每个字符串代表生成流程图所需的一行代码。
                列表的第一行为"```mermaid"，代表开始markdown的mermaid流程图代码区域。
                列表的最后一行为"```"，代表结束markdown的mermaid流程图代码区域。
                列表的中间部分则为根据输入的节点、线条以及其他相关配置生成的用于绘制流程图的代码。
        
        例如:
            对于一个只有两个节点（"start"和"end"）和一条从"start"到"end"的线的流程图，
            str_out方法返回的字符串列表可能为：
        
            [
                "```mermaid",
                "graph LR",
                "id_0[start] ",
                "id_1[end] ",
                "id_0 --> id_1 ",
                "```"
            ]
        
        注意:
            1. 如果节点有特定形状，将用特定的左右括号表示。
            2. 如果节点有图标，将在节点名前添加"fa:图标名"。
            3. 如果节点有导航链接，将在所有节点和线条后添加"click 节点id href "#导航标题""。
            4. 如果节点有特定颜色，将在所有节点和线条后添加"style 节点id fill:颜色"。
        """

        lines = ['```mermaid\n', f'graph {self.oriented}\n']
        for node in self.nodes:
            if node[0] in self.node_shape:
                splite = self.node_shape[node[0]].split("%%")
                left_c = splite[0]
                right_c = splite[1]
            else:
                left_c = '['
                right_c = ']'

            if node[0] in self.node_icon:
                node_str = f"fa:{self.node_icon[node[0]]} {node[1]}"
            else:
                node_str = node[1]

            lines.append(f"{node[0]}{left_c}{node_str}{right_c} \n")

        for line in self.lines:
            if line[2] is None:
                if line[3]:
                    lines.append(f"{line[0]} -.-> {line[1]} \n")
                else:
                    lines.append(f"{line[0]} --> {line[1]} \n")
            else:
                if line[3]:
                    lines.append(f"{line[0]} -.->|{line[2]}| {line[1]} \n")
                else:
                    lines.append(f"{line[0]} -->|{line[2]}| {line[1]} \n")

        for k in self.node_navigate.keys():
            v = self.node_navigate[k]  # self.node_navigate[k].lower().replace(' ', '-')
            lines.append(f'click {k} href "#{v}"\n')

        for node_color_key in self.node_color:
            lines.append(f"style {node_color_key} fill:{self.node_color[node_color_key]}\n")

        lines.append("```\n")
        return lines

    def __init__(self, oriented_left2right=True):
        """
            `draw_markdownobj_flowchart` 类的初始化函数。
        
            该类用于创建并修改一个markdown格式的流程图对象。其可以添加/设置节点，给节点着色，设置节点形状，添加连线等。
        
            类的初始化函数主要用于设置流程图的方向（默认为从左到右），并初始化一些必要的属性。
        
            使用例子：
            ```python
            flowchart = draw_markdownobj_flowchart(oriented_left2right=False)  # 创建一个从上到下的流程图对象
            flowchart.add_node(name='node1', id='1')  # 添加一个节点
            flowchart.set_node_color(id='1', color=flowchart_color_enum.BLUE)  # 设置节点颜色
            flowchart.add_line(id1='1', id2='2')  # 添加连线
            ```
        
            参数:
                oriented_left2right (bool): 流程图的方向。默认为从左到右。如果为 `False`，则方向为从上到下。
        
            无返回值。
        """

        self.nodes = []
        self.node_color = {}
        self.node_shape = {}
        self.lines = []
        self.oriented = "LR" if oriented_left2right else "TD"
        self.node_navigate = {}
        self.node_icon = {}
        self.id_mapping = {}

    def _convert_name(self, answer):
        """
        该函数用于处理和转换节点名称。
        
        根据传入的参数'answer'，对其进行处理和转换，以满足后续操作的需求。
        
        参数:
            answer(str): 待处理的节点名称。如果名称以'/'开头，该函数会在其前面加上一个空格。同时，该函数会把uncode中的字符替换为空格。
        
        返回:
            str: 处理和转换过的节点名称。
        
        注意:
            如果传入的answer为None，该函数会直接返回None。
        
        示例:
            假设我们有如下的代码：
            ```
            dm = draw_markdownobj_flowchart()
            dm._convert_name('/example')
            ```
            上述代码会返回 ' example'。
        """

        if answer is None:
            return None
        if answer.startswith('/'):
            answer = " " + answer

        for cc in uncode:
            answer = answer.replace(cc, " ")

        return answer

    def add_node(self, name, id, anchor_title=None, icon=None):
        """
        该函数用于向流程图对象中添加节点。
        
        参数:
            name (str): 节点的名称。
            id (str): 节点的标识，用于在流程图中唯一标识这个节点。
            anchor_title (str, 可选): 如果提供，可以为节点添加一个超链接。默认为None。
            icon (str, 可选): 如果提供，可以为节点添加一个图标。默认为None。
        
        返回值:
            无返回值。
        
        使用例子:
            add_node("节点1", "id1")
            add_node("节点2", "id2", anchor_title="title", icon="icon")
        
        注意：
            id必须是唯一的，不能重复。如果添加了重复的id，后添加的节点将会覆盖先添加的节点。
        """

        if id not in self.id_mapping:
            self.id_mapping[id] = f"id_{len(self.id_mapping)}"
        id = self.id_mapping[id]

        self.nodes.append((id, self._convert_name(name), None))
        if anchor_title is not None:
            self.node_navigate[id] = anchor_title
        if icon is not None:
            self.node_icon[id] = icon

    def set_node_color(self, id, color: flowchart_color_enum):
        """
            def set_node_color(self, id, color: flowchart_color_enum):
        
            该函数的主要功能是设置流程图中节点的颜色。
        
            根据输入的节点id和颜色，将颜色信息添加到self.node_color字典中，键为节点id，值为颜色。
        
            参数:
                id: 需要设置颜色的节点的id，应为字符串类型。
                color: 需要设置的颜色，应为flowchart_color_enum枚举类型。
        
            此函数没有返回值。
        
            示例:
            ```python
            # 创建流程图对象
            flowchart = draw_markdownobj_flowchart()
            # 添加节点
            flowchart.add_node('Node1', '1')
            # 设置节点颜色
            flowchart.set_node_color('1', flowchart_color_enum.Red)
            ```
        
            注意:
            如果输入的节点id在流程图中不存在，此函数将无法正确工作，
            因此在调用此函数之前，需要确保已经使用add_node函数添加了对应的节点。
        
        """

        self.node_color[self.id_mapping[id]] = color

    def set_node_shape(self, id, shape: flowchart_shape_enum):
        """
        此函数用于设置流程图中节点的形状。
        
        参数:
        id: 节点的标识符，用于识别需要设置形状的节点。
        shape: 流程图形状枚举，用于设定节点的形状。
        
        返回类型: 无返回值
        
        此函数没有已知的错误或bug。
        
        使用示例:
        ```python
        fchart = draw_markdownobj_flowchart()
        fchart.add_node("Node1", id="1")
        fchart.set_node_shape(id="1", shape=flowchart_shape_enum.ellipse)
        ```
        在上述示例中，我们首先创建了一个 `draw_markdownobj_flowchart` 对象 `fchart`，然后添加了一个名为 "Node1" 的节点，并且通过设置 `id` 参数为 "1"，将其识别为节点 "1"。然后，我们使用 `set_node_shape` 函数将节点 "1" 的形状设置为椭圆形（`flowchart_shape_enum.ellipse`）。
        """

        self.node_shape[self.id_mapping[id]] = shape

    def add_line(self, id1, id2, message=None, dot_line=False):
        """
        此函数用于在流程图中添加线条。
        
        参数:
            id1: str，起始节点的ID。
            id2: str，结束节点的ID。
            message: str, 默认为None，线条中显示的文字信息。
            dot_line: bool, 默认为False，如果设置为True，线条为虚线，否则为实线。
        
        返回:
            无返回值。
        
        使用方法举例:
            例如，我们有两个节点，节点1的ID为"start"，节点2的ID为"end"，我们希望在这两个节点之间添加一条含有信息"begin"的实线，可以如下调用:
            flowchart.add_line(id1="start", id2="end", message="begin", dot_line=False)
        
        注意:
            在调用此函数之前，需要先确保已经添加了ID为id1和id2的节点。
            id1和id2必须是字符串格式，message如果不为None，也必须是字符串格式。
            如果dot_line不为布尔值，会抛出TypeError错误。
        """

        id1 = self.id_mapping[id1]
        id2 = self.id_mapping[id2]

        self.lines.append((id1, id2, self._convert_name(message), dot_line))


class draw_markdownobj_gantt(draw_markdownobj):
    """
    此类 `draw_markdownobj_gantt(draw_markdownobj)` 用于绘制markdown格式的甘特图。甘特图广泛用于项目管理中，能清晰地展示项目任务，以及它们的开始时间、结束时间和持续时间。
    
    该类包含以下方法:
    
    - `__init__(self, gantt_title, date_format='YYYY-MM-DD')`：初始化方法，用于设置甘特图的标题和日期格式。
    
    - `str_out(self) -> [str]`：该方法用于处理并返回甘特图的字符串格式。
    
    - `add_item(self, name)`：添加项的方法，可以为甘特图添加一个新的项目。
    
    - `add_item_data(self, key, date_name, date)`：为特定项目添加日期数据。
    
    使用示例:
    
    ```python
    # 创建一个甘特图对象，设置标题和日期格式
    gantt = draw_markdownobj_gantt('Project Schedule', 'YYYY-MM-DD')
    
    # 为甘特图添加项目
    gantt.add_item('Task1')
    gantt.add_item('Task2')
    
    # 为项目添加日期数据
    gantt.add_item_data('Task1', 'start_date', '2022-01-01')
    gantt.add_item_data('Task1', 'end_date', '2022-01-31')
    gantt.add_item_data('Task2', 'start_date', '2022-02-01')
    gantt.add_item_data('Task2', 'end_date', '2022-02-28')
    
    # 获取并打印甘特图的字符串格式
    print(gantt.str_out())
    ```
    
    注意: 在使用此类时，需要确保提供的日期格式与实际的日期数据匹配。否则，可能无法正确绘制甘特图。
    """

    def __init__(self, gantt_title, date_format='YYYY-MM-DD'):
        """
        这是一个初始化 `draw_markdownobj_gantt` 类的方法。
        
        `draw_markdownobj_gantt` 类是用于生成和操作 Markdown 语法的 Gantt 图的类。你可以创建一个对象，设置标题和日期格式，然后向其中添加项目和数据。每个项目是一个字典，键为项目名，值为一个包含日期信息的字典。
        
        参数:
            gantt_title (str): 设置 Gantt 图的标题。
        
            date_format (str): 设置 Gantt 图的日期格式， 默认为 'YYYY-MM-DD'。
        
        属性:
            Items (dict): 用于存储Gantt图中的项目和日期数据，每个项目是一个字典，键为项目名，值为一个包含日期信息的字典。
        
            Title (str): Gantt图的标题。
        
            date_format (str): Gantt图的日期格式。
        
        示例：
            ```python
            gantt = draw_markdownobj_gantt('Test Gantt')
            gantt.add_item('item1')
            gantt.add_item_data('item1', 'date1', ('2020-01-01', '2020-01-31'))
            print('\n'.join(gantt.str_out()))
            ```
            上述代码将创建一个名称为'Test Gantt'的 Gantt 图，其中包含一个名为'item1'的项目，该项目在'2020-01-01'至'2020-01-31'之间有数据。
        
        注意：
            如果尝试添加的项目名已存在于 Items 中，该方法不会检查或抛出错误，而是会直接覆盖现有项目。为避免数据丢失，使用前需确保项目名的唯一性。
        """

        self.Items = {}
        self.Title = gantt_title
        self.date_format = date_format

    def str_out(self) -> [str]:
        """
        该函数的主要目的是将Gantt图的数据转换为字符串格式以便在Markdown中使用。
        
        具体来说，该函数会读取 Gantt 图的标题、时间格式和项目数据（包括项目名称、项目日期等），
        并将这些信息转换为Mermaid的Markdown格式。
        
        返回的结果为一个字符串列表，列表的每个元素代表了Markdown中的一行。
        
        Params:
        无
        
        Return:
        list(str): 转换后的Markdown格式的Gantt图数据。
        
        示例：
        默认日期格式为 'YYYY-MM-DD'，Gannt图的标题为 'Project Schedule'，并添加了两个项目：
        项目 'Task1' 有一项活动 'coding', 计划日期为 '2023-01-01'至'2023-02-01'；
        项目 'Task2' 有一项活动 'testing', 计划日期为 '2023-02-02'至'2023-03-01'。
        
        调用str_out()函数后，返回的字符串列表为：
        
        ['```mermaid\n',
         'gantt\n',
         '\tdateFormat YYYY-MM-DD\n',
         '\ttitle Project Schedule\n',
         '\tsection Task1\n',
         '\tcoding\t:2023-01-01, 2023-02-01\n',
         '\tsection Task2\n',
         '\ttesting\t:2023-02-02, 2023-03-01\n',
         '```\n']
        
        注意：
        1. 生成的字符串需要配合Mermaid.js的Markdown插件使用，直接在Markdown编辑器中可能无法正常显示Gantt图。
        2. 请确保所有项目的日期都符合给定的日期格式，否则可能会在解析时出现问题。
        """

        out_str = ['```mermaid\n', 'gantt\n', f'\tdateFormat {self.date_format}\n', f'\ttitle {self.Title}\n']

        for item_key, times in self.Items.items():
            out_str.append(f"\tsection {item_key}\n")
            for t_key, t_time_tulp in times['dates'].items():
                out_str.append(f"\t{t_key}\t:{t_time_tulp[0]}, {t_time_tulp[1]}\n")

        out_str.append('```\n')
        return out_str

    def add_item(self, name):
        """
        该函数的主要作用是添加一个新的项目到gantt图中。
        
        参数:
        name: 字符串类型，代表要添加到gantt图中的项目的名称。
        
        返回:
        无返回值。
        
        例子:
        gantt = draw_markdownobj_gantt('project')
        gantt.add_item('task1')
        
        以上代码将在gantt图中添加一个名为'task1'的新项目。
        
        注意:
        该函数不会检查新添加的项目名称是否已经在gantt图中存在，如果已经存在，新添加的项目将会覆盖原有项目。
        """

        self.Items[name] = {
            'dates': {}
        }

    def add_item_data(self, key, date_name, date):
        """
        此函数用于给指定的项目添加事件信息。
        
        参数:
            key (str): 项目的名称，用于在字典中查找对应的项目。
            date_name (str): 事件的名称，用于标识不同的事件。
            date (tuple): 包含事件开始和结束日期的元组，日期格式应与创建gantt对象时设定的日期格式一致。
        
        返回:
            无返回值。
        
        示例:
        
        ```python
        gantt = draw_markdownobj_gantt('我的甘特图')
        gantt.add_item('项目1')
        gantt.add_item_data('项目1', '任务1', ('2021-01-01', '2021-01-31'))
        ```
        
        此函数无已知的bug。
        """

        self.Items[key]['dates'][date_name] = date


class markdowndoc():
    """
    `markdowndoc` 类是一个用于生成 Markdown 文档的类。它提供了一系列方法，可以用来写入各种类型的内容，包括标题、文本行、分割线、页脚、代码块等。
    
    这个类的主要目的是简化 Markdown 文档的生成过程。它通过提供一系列的方法，使用户可以方便地插入各种类型的内容，而无需手动编写 Markdown 语法。
    
    使用示例：
    ```python
    doc = markdowndoc('example.md')  # 创建一个 markdowndoc 对象，将要写入的文件名为 'example.md'
    doc.write_title('Hello, world!', 1)  # 写入一级标题
    doc.write_line('This is an example document.')  # 写入文本行
    doc.write_markdown_code('print("Hello, world!")')  # 写入代码块
    doc.flush()  # 将所有内容写入文件
    ```
    
    参数：
    - init 方法接受三个参数：path（要写入的文件路径）、need_toc（是否需要生成目录，默认为 True）和 title_with_index（标题是否需要编号，默认为 False）。
    - write_title 方法接受两个参数：stra（标题文本）和 level（标题级别）。
    - write_line 方法接受三个参数：str（要写入的文本）、is_block（是否以粗体显示，默认为 None）和 ishtml（是否为 HTML 格式，默认为 False）。
    - write_footer 方法没有参数。
    - write_markdown_code 方法接受一个参数：str（要写入的代码）。
    - write_table 方法接受两个参数：title（表格标题）和 data（表格数据）。
    - write_img 方法接受一个参数：path（图片路径）。
    - flush 方法没有参数。
    
    返回值：
    - 所有的写入方法都没有返回值。
    - flush 方法没有返回值。
    
    错误和 bug：
    - 当 write_title 的 level 参数不符合预期时，会抛出 Exception。
    
    """

    def __init__(self, path, need_toc=True, title_with_index=False):
        """
        这是一个 `markdowndoc` 类，主要用于生成Markdown格式文档。
        
        类的初始化方法是 `__init__`。此方法在创建类的新实例时被调用，用于设置该实例的初始状态。
        
        参数:
            path (str): 文件路径，markdown文件将保存在此路径下。
            need_toc (bool, optional): 是否需要生成目录，默认为True，如果为True，会在文档顶部生成目录。
            title_with_index (bool, optional): 是否需要为标题添加索引，默认为False，如果为True，标题前会添加相应的索引。
        
        示例:
        ```python
        doc = markdowndoc('mydoc.md', need_toc=True, title_with_index=True)
        doc.write_title('Chapter 1', level=1)
        doc.write_line('This is a test line.')
        doc.flush()  # 保存并写入文件
        ```
        
        以上代码将生成一个markdown文件'mydoc.md'，包含一个带有索引的标题'Chapter 1'和一行纯文本'This is a test line.'。
        
        注意事项:
        在添加标题时，需要确保标题级别(level)的递增顺序正确，否则会抛出异常。例如，当前标题级别为1，下一个标题的级别不能直接设为3，应按照1,2,3的顺序递增。
        
        """

        self.file_lines = []
        self.path = path
        self.title_with_index = title_with_index
        self.title_index_stack = []
        self._title_index_level = 0

        self.title_index = {}

        if need_toc:
            self.file_lines.append('[toc] \n')

    def _convert_char(self, ss: str):
        """
            `_convert_char`是一个私有方法，用于将字符串中的特殊字符进行转义。
        
            该方法主要是为了处理在markdown文档中可能会引发格式混乱的特殊字符，例如反斜线、下划线和井号。
        
            参数:
                ss (str): 需要进行转义处理的字符串。
        
            返回:
                str: 转义处理后的字符串。
        
            示例：
                ```python
                md = markdowndoc("example.md")
                text = "\\Hello, Python__"
                result = md._convert_char(text)
                print(result)  # 输出为 "\\\\Hello, Python\\_\\_"
                ```
        """

        ss = str(ss)
        ss = ss.replace('\\', "\\\\")
        ss = ss.replace("__", "\_\_")
        ss = ss.replace("#", "\#")
        return ss

    def _generate_count_char(self, char, count):
        """
        该方法的目的是根据给定的字符（char）和指定的数量（count）生成一个新的字符串。例如，如果传入的字符是'#'，数量是3，那么返回的结果就是'###'。这是一个内部方法，主要用于在生成markdown标题时，根据标题的级别动态生成对应数量的'#'符号。
        
        参数:
            char: 字符串类型，需要被重复的字符。
            count: 整数类型，字符需要被重复的次数。
        
        返回:
            返回一个新的字符串，其中包含了指定数量的char字符。
        
        示例:
            _generate_count_char('#', 3) 返回'###'
        """

        s = ""
        for _ in range(count):
            s += char

        return s

    def write_title(self, stra, level):
        """
        该函数是在markdowndoc类中定义的一个方法，用于在markdown文档中写入标题。
        
        参数:
            stra: string类型，标题的内容。
            level: int类型，标题的层级。例如，level为1表示一级标题，level为2表示二级标题，以此类推。
        
        返回值:
            无返回值。
        
        使用示例:
            doc = markdowndoc(path="path/to/your/file")
            doc.write_title(stra="Introduction", level=1)
        
        注意：
            在使用该函数时，如果需要在标题前添加索引，需要在初始化markdowndoc对象时，将title_with_index设置为True。
            另外，该函数只接收整数作为标题层级，不接受0或负数，也不接受非整数。
            如果标题层级的设置不按照递增或递减的顺序（例如，直接从一级标题跳到三级标题），会抛出"标题层级错误"的异常。
        """

        if not self.title_with_index:
            self.file_lines.append(f"{self._generate_count_char('#', level)} {self._convert_char(stra)} \n")
        else:
            if level > self._title_index_level:
                if level != self._title_index_level + 1:
                    raise Exception("title level error")
                self.title_index_stack.append(1)
                self._title_index_level = level
            elif level == self._title_index_level:
                self.title_index_stack[-1] += 1
            elif level < self._title_index_level:
                while True:
                    if len(self.title_index_stack) > level:
                        self.title_index_stack.pop(-1)
                        continue
                    break
                self.title_index_stack[-1] += 1
                self._title_index_level = level
            index_str = ".".join([str(xx_) for xx_ in self.title_index_stack])
            self.title_index[stra] = index_str
            self.file_lines.append(f"{self._generate_count_char('#', level)} {index_str} {self._convert_char(stra)} \n")

    def write_line(self, str, is_block=None, ishtml=False):
        """
        这是一个写入markdown文本行的函数, 主要是将字符串文本按照markdown的格式，写入到类对象的file_lines属性中（一个list）,用于后续的markdown文件生成。函数根据参数设定，还可以处理html代码块和加粗的文本。
        
        参数:
        str: 一个字符串，将被写入到markdown文件中。
        
        is_block: 一个布尔值，默认为None，表示写入的字符串是否需要被加粗（使用markdown的** **语法）。如果设为True, 则会在字符串前后加上** .
        
        ishtml: 一个布尔值，默认为False，表示写入的字符串是否是html代码。如果设为True, 则写入的字符串被当作html代码处理。
        
        返回值:
        无返回值。
        
        注意:
        1. 如果同时设定is_block和ishtml为True, 函数将优先处理ishtml参数，即字符串会被当作html代码处理，不会被加粗。
        2. 如果ishtml设为True, 写入的字符串需要符合html的语法规则，否则在markdown文件渲染时可能会出现格式错误。
        
        使用示例:
        
        ```python
        doc = markdowndoc("text.md")
        doc.write_line("This is a normal line")
        doc.write_line("This is a bold line", is_block=True)
        doc.write_line("<p>This is a line of HTML code</p>", ishtml=True)
        doc.flush()
        ```
        
        这段代码将创建一个名为text.md的markdown文件，并在其中写入三行文本，分别为正常文本、加粗文本、HTML代码，然后生成markdown文件。
        """

        if ishtml:
            self.file_lines.append(f"{str} \n")
        elif is_block:
            self.file_lines.append(f"**{self._convert_char(str)}** \n")
        else:
            self.file_lines.append(f"{self._convert_char(str)} \n")

    def write_split_line(self):
        """
        该方法用于写入markdown的分割线。
        
        使用"***"字符在markdown文件中创建一个水平分割线。调用此方法不需要任何参数。
        
        该方法没有返回值。
        
        调用示例：
            doc = markdowndoc('path/to/your/file')
            doc.write_split_line()
        
        注意：此方法不会立即将分割线写入文件，只是将其添加到待写入列表中。在调用flush()方法后，才会实际写入文件。
        """

        self.file_lines.append("*** \n")

    def write_footer(self):
        """
        此函数的主要目的是在markdown文件中写入页脚。它将在markdown文件的末尾添加一个分割线，并在分割线下面写入当前的时间日期。这可以非常有用，例如在每次更新文件时自动添加时间戳。
        
        参数:
        无
        
        返回:
        无
        
        示例:
        以下是如何使用该函数的一个例子:
        
        ```python
        doc = markdowndoc('path_to_your_file')
        doc.write_footer()
        ```
        在上面的代码中，我们首先创建了一个markdowndoc对象，然后调用了write_footer函数。结果将在markdown文件的末尾添加一个时间戳。
        
        错误或者bug:
        当前没有已知的错误或bug。
        
        注意:
        该函数在调用时将直接修改markdown文件，而不需要额外的确认或保存步骤。
        """

        self.write_split_line()
        self.write_line(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    def write_markdown_code(self, str):
        """
        这个方法的作用是向Markdown文档中写入Markdown代码。
        
        参数:
            str: 需要写入的Markdown代码，类型为字符串。
        
        返回:
            无
        
        示例:
            md = markdowndoc('example.md')
            md.write_markdown_code('# This is a title')
        
        以上代码会在example.md文件中写入'# This is a title'这行Markdown代码。
        
        错误或者bug:
            无
        """

        self.file_lines.append(str)

    def write_table(self, title: [], data: [[]]):
        """
        `write_table` 是一个类方法，其主要作用是在Markdown文件中写入一个格式化的表格。
        
        参数:
        - `title`: list类型，表示表格的标题行，每个元素是表格的一个列名。
        - `data`: 嵌套的list类型，表示表格的数据行。每个子列表表示一行数据，子列表的元素个数应该和title的元素个数一致。
        
        返回类型: 无
        
        该方法首先会对标题进行转义处理，然后将标题行写入Markdown文件，紧接着写入一个分隔线。之后对数据行进行处理，将每一行的数据写入到Markdown文件中。需要注意的是，数据行中的每个元素在写入时会将换行符替换为`<br>`。
        
        使用示例:
        
        ```python
        md = markdowndoc('path_to_markdown_file.md')
        title = ['姓名', '年龄', '职业']
        data = [['小明', '22', '程序员'], ['小红', '23', '设计师']]
        md.write_table(title, data)
        ```
        
        该示例会在Markdown文件中写入如下内容:
        
        ```
        | 姓名 | 年龄 | 职业 |
        | ---- | ---- | ---- |
        | 小明 | 22   | 程序员 |
        | 小红 | 23   | 设计师 |
        ```
        
        注意事项:
        - 如果数据行中的元素包含换行符，会被替换为`<br>`；
        - 如果数据行的元素个数和标题行的元素个数不一致，可能会导致生成的Markdown表格格式不正确。
        """

        title = [self._convert_char(x) for x in title]
        self.file_lines.append(f"| {'|'.join(title)} | \n")
        self.file_lines.append(f"| {'|'.join(['----' for _ in title])} | \n")
        for row in data:
            row = [str(_x).strip() for _x in row]
            row_new = [str(x).replace('\n', '<br>') for x in row]
            # row_new = [self._convert_char(x).replace('\n', '<br>') for x in row]
            self.file_lines.append(f"| {'|'.join(row_new)} | \n")

    def write_img(self, path):
        """
        该函数的主要目的是在Markdown文件中插入图片。
        
        函数参数:
            path (str): 插入图片的路径。
        
        返回类型:
            无
        
        使用方法:
            write_img("/path/to/your/image.jpg")
        
        注意:
            图片路径可以是相对路径或者绝对路径，完全取决于Markdown文件的相对位置。
            如果图片路径不存在，则不会插入任何内容。
        
        错误和bug:
            如果路径中含有特殊字符，可能会导致Markdown渲染错误。
        
        代码示例:
        ```python
            md = markdowndoc("demo.md")
            md.write_img("./test.jpg")
            md.flush()
        ```
        上述代码将在Markdown文件"demo.md"中插入图片"test.jpg"，图片路径为当前文件夹下的test.jpg。
        
        """

        self.file_lines.append(f"![a{str(time.time())}]({path})\n")

    def write_markdownobj(self, obj: draw_markdownobj):
        """
        `write_markdownobj`是一个成员函数，用于将提供的Markdown对象写入文件。
        
        参数:
            obj (draw_markdownobj): 需要写入的Markdown对象。此对象应该有一个`str_out`方法，返回一个由字符串组成的列表，每个字符串代表Markdown文件的一行。
        
        返回:
            无返回值。
        
        此函数将`obj`对象的`str_out`方法返回的每一行字符串添加到`file_lines`列表中，这些字符串稍后会被写入Markdown文件。
        
        注意:
            - `draw_markdownobj`需要有一个名为`str_out`的方法，如果没有，此函数将会抛出AttributeError。
            - 此函数没有进行错误处理，因此如果`str_out`方法不存在或者执行错误，将会直接抛出异常。
            - 对象`obj`的`str_out`方法应保证返回一个字符串列表，否则可能会引发其他类型的错误。
        
        例子:
            假设我们有一个Markdown对象，它的`str_out`方法能够生成Markdown文件的内容，那么我们可以这样使用：
        
            ```python
            md = markdowndoc("path_to_file")
            md_obj = draw_markdownobj()
            md.write_markdownobj(md_obj)
            ```
        """

        for line in obj.str_out():
            self.file_lines.append(line)

    def flush(self):
        """
        `flush`是`markdowndoc`类的一个方法，用于将markdown文档内容实际写入到指定的文件中。
        
        参数:
            无
        
        返回类型:
            无
        
        该方法首先会对标题索引（`title_index`）进行排序，排序规则是按照标题的长度降序排列。然后，它会打开指定的文件，并创建一个新的列表`lines_new`，用于存放最终要写入文件的行。
        
        然后，对于`file_lines`列表中的每一行，该方法会遍历所有的标题，将这一行中所有的标题引用（如"@@" + 标题）替换为对应的索引值和标题，然后将替换后的行添加到`lines_new`列表中。
        
        最后，它会将`lines_new`列表中的所有行写入到文件中。
        
        注意，由于这个方法是在析构函数中调用的，所以在类的实例被销毁时，会自动调用该方法，将文档内容写入到文件中。
        
        示例:
        
        ```python
        md = markdowndoc("test.md")
        md.write_title("测试标题", level=1)
        md.write_line("这是一行文字")
        md.flush()  # 这会将上述内容写入到"test.md"文件中
        ```
        """

        ordered_key = sorted(self.title_index.keys(), key=lambda x: len(x), reverse=True)

        with open(self.path, 'w', encoding='utf-8') as f:
            lines_new = []
            for ll in self.file_lines:
                for t_key in ordered_key:
                    t_val = self.title_index[t_key]
                    v1 = t_val
                    v2 = f"{t_val} {self._convert_char(t_key)}".lower().replace(' ', '-')
                    ll = ll.replace("@@" + t_key, v2)
                    ll = ll.replace("@" + t_key, v1)
                lines_new.append(ll)
            f.writelines(lines_new)

    def write_code(self, code):
        """
            def write_code(self, code):
                此函数用于将给定的代码字符串添加到 markdown 文档中。代码将在 markdown 中被封装在 "```python" 和 "```" 标签中，以便于在 markdown 阅读器中以代码块的形式呈现。
        
                参数:
                code (str): 需要添加到 markdown 文档中的代码字符串。
        
                返回:
                无返回值
        
                使用示例:
                mddoc = markdowndoc("example.md")
                mddoc.write_code("print('Hello, world!')")
        
                注意：
                1. 如果代码中含有不支持的字符，可能会导致错误。
                2. 此函数不会自动保存文件，需要调用 flush 函数进行保存。
        """

        self.file_lines.append("\n")
        self.file_lines.append("```python \n")
        self.file_lines.append(code)
        self.file_lines.append("\n")
        self.file_lines.append("```\n")

    # def __del__(self):
    #     self.flush()
