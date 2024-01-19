import os

from tketool.lmc.lmc_linked import lmc_linked_model
from tketool.lmc.llms import LLM_Plus
from tketool.files import *
from tketool.utils.progressbar import process_status_bar
from tketool.buffer.bufferbase import *
import ast, re
from tketool.lmc.prompts.prompt_controller import get_prompt
import typing
from tketool.lmc.tasks.task_init import get_init_llm
from tketool.markdowns.markdown import *


class comment_creator:
    # version 1.2
    """
    这个类名为`comment_creator`，主要用于为Python源码文件添加自动生成的注释。
    
    **目的**:
    
    为了提高代码的可读性和可维护性，该类可以自动分析Python源码文件，并根据代码结构和内容生成对应的注释。
    
    **使用例子**:
    
    ```python
    llm = LLM_Plus(...)
    path = "./src"
    cc = comment_creator(llm, path)
    cc.fill_comment()
    ```
    
    类方法：
    - `__init__(self, llm: LLM_Plus, path)`: 初始化，接收一个`LLM_Plus`对象和Python源码文件路径，准备用于后续代码分析生成注释。
    - `_parse_py_file(self, lines)`: 用于解析Python文件，通过`ast`模块获取代码的抽象语法树并进行分析。
    - `add_l1_coment(self, l1_list, l1_mark, l2_list, l2_mark, m_obj, m1, m2)`: 用于生成对应的注释，需要输入当前处理的行等信息。
    - `fill_comment(self)`: 对初始化时指定的路径下的所有Python文件进行遍历，自动添加注释。
    
    注意：该类依赖`LLM_Plus`对象生成注释，`LLM_Plus`需预先训练好。并且注释生成可能不完全准确，需要根据实际代码内容进行修改调整。
    
    **待修复的问题**：暂无已知bug。
    """

    def __init__(self, llm: LLM_Plus, path):
        # version 1.1
        """
        这个类的名称是comment_creator，其主要目的是对Python源代码文件进行解析，并自动添加注释。
        
        类的初始化函数需要两个参数：
        
        - llm (LLM_Plus)：一个LLM_Plus类型的对象，用于调用其相关功能对源代码进行解析。
        - path (str)：需要解析的Python源文件的路径。
        
        初始化函数主要进行以下几个操作：
        - 获取并保存输入参数
        - 枚举path路径下所有的文件，并存储到all_file_task属性中
        - 创建一个进度条对象p_bar，用于后续的任务进度显示
        - 获取注释生成模型的提示字符串（模型的语言设置为中文），并创建一个lmc_linked_model对象l1_parser，设置其模型提示模板以及重试次数。
        
        注意:
        - 在使用本类时，请确保提供的LLM_Plus对象和文件路径是有效的，不然可能会导致错误。
        - 本类尚未处理所有可能的错误情况和异常输入，因此在使用时请保证输入的参数正确性。
        """

        self.llm = llm
        self.path = path
        self.all_file_task = [(d_path, d_file) for d_path, d_file in
                              enum_files(path, True)]

        self.p_bar = process_status_bar()

        l1_parser_prompt_str = get_prompt("comments_level1", lang="chinese", )
        self.l1_parser = lmc_linked_model(llm).set_prompt_template(l1_parser_prompt_str).set_retry(3)
        summary_1_parser_prompt_str = get_prompt("doc_create_member_summary", lang="chinese", )
        self.summary_1_parser = lmc_linked_model(llm).set_prompt_template(summary_1_parser_prompt_str).set_retry(3)
        summary_2_parser_prompt_str = get_prompt("doc_create_module_summary", lang="chinese", )
        self.summary_2_parser = lmc_linked_model(llm).set_prompt_template(summary_2_parser_prompt_str).set_retry(3)

    def _parse_py_file(self, lines):

        """
        `_parse_py_file`是`comment_creator`类中的一个私有方法，这个方法的主要目的是解析Python文件，生成一个标记列表，标记列表中的每个元素表示原始代码行的类型。
        
        参数:
            lines (List[str]): 原始代码行的列表。
        
        返回:
            List[str]: 表示代码行类型的标记列表。可能的标记包括"class_start", "class", "func_start", "func", "comment"等等。如果某一行是类定义或函数定义的开始，该行的标记会在行号后加上"_start"。如果某一行是类定义或函数定义内部的一部分，该行的标记会是"class"或"func"。如果某一行是注释行，该行的标记会是"comment"。
        
        使用方法:
            该函数是内部使用的，通常不会直接调用。它被`fill_comment`方法调用，用于解析Python文件并生成标记列表，这些标记随后用于决定如何添加新的注释。
        
        注意:
            该函数使用Python的AST（Abstract Syntax Tree）模块进行源代码解析。因此，如果原始代码存在语法错误，该函数可能无法正确运行。
        
        示例代码:
            ```
            lines = read_file_lines("test.py")
            line_marks = self._parse_py_file(lines)
            ```
        
        可能的错误:
            如果输入的原始代码存在语法错误，AST的解析过程可能会失败，导致函数无法正确运行。
        """

        line_mark = ["" for _ in range(len(lines))]

        class python_visitor(ast.NodeVisitor):
            def visit_ClassDef(self, node):
                end_lineno = node.body[0].lineno
                for isdx in range(node.lineno, end_lineno):
                    if isdx == node.lineno:
                        line_mark[isdx - 1] = "class_start"
                    else:
                        line_mark[isdx - 1] = "class"

                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                    for isdx2 in range(node.body[0].lineno, node.body[0].end_lineno + 1):
                        line_mark[isdx2 - 1] = "comment"

                line_mark[node.lineno - 1] += f"_{node.end_lineno}"
                self.generic_visit(node)

            def visit_FunctionDef(self, node):
                end_lineno = node.body[0].lineno
                for isdx in range(node.lineno, end_lineno):
                    if isdx == node.lineno:
                        line_mark[isdx - 1] = "func_start"
                    else:
                        line_mark[isdx - 1] = "func"

                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                    for isdx2 in range(node.body[0].lineno, node.body[0].end_lineno + 1):
                        line_mark[isdx2 - 1] = "comment"

                line_mark[node.lineno - 1] += f"_{node.end_lineno}"
                # self.generic_visit(node)

        root = ast.parse("".join(lines), type_comments=True)
        visitor = python_visitor()
        visitor.visit(root)

        return line_mark

    def _add_memeber_summary(self, lines):
        """
        这是一个为类成员添加概要信息的方法。
        
        参数:
            lines: 类型为list，包含了要解析的源代码行。
        
        返回:
            字符串类型, 返回从源代码行解析得到的类成员概要信息。
        
        此函数的主要作用是分析源代码中的类成员，并为它们添加概要信息。它首先检查缓存中是否已存在此类成员的概要信息，如果存在，则直接从缓存中获取。如果不存在，则使用预定义的解析器从源代码行中提取信息，并将提取的信息添加到缓存中，最后从缓存中获取概要信息并返回。
        
        注意:
            使用此函数时，应确保传入的源代码行是有效的Python代码，否则可能会导致解析错误。
        """

        lines = [ll.strip() for ll in lines]
        key = "_".join(lines)
        if not has_item_key(key):
            res_ = self.summary_1_parser(content="\n".join(lines))
            rr = res_[0][0]

            buffer_item(key, rr)
            flush()
        rr = get_buffer_item(key)

        return rr

    def _add_module_summary(self, lines):
        """
            这是一个私有方法，其主要功能是为模块生成摘要。
        
            参数:
                lines: list, 需要生成摘要的模块的行列表。
        
            返回:
                str, 生成的模块摘要。
        
            该函数主要通过以下步骤实现其功能：
            1. 首先，对输入的模块行列表进行清洗，去除两端空白字符，并将其合并为一个字符串，作为键值。
            2. 然后，检查该键值是否已经存在于缓存中。如果存在，直接从缓存中获取摘要；如果不存在，就使用summary_2_parser进行解析，获取摘要，并将其缓存起来。
            3. 最后，返回生成的摘要。
        
            注意：该函数没有处理错误和异常的代码，因此调用者需要自行处理可能出现的错误和异常。
        
            示例代码:
        
            ```python
            lines = ['def func1():', '    pass', 'def func2():', '    pass']
            summary = _add_module_summary(lines)
            print(summary)
            ```
        """

        lines = [ll.strip() for ll in lines]
        key = "_".join(lines)
        if not has_item_key(key):
            res_ = self.summary_2_parser(content="\n".join(lines))
            rr = res_[0][0]
            buffer_item(key, rr)
            flush()
        rr = get_buffer_item(key)

        return rr

    def add_l1_coment(self, l1_list, l1_mark, l2_list, l2_mark, m_obj, m1, m2):
        """
        这个函数的主要目的是在给定的python代码块中添加一级注释。
        
        参数:
        l1_list: list, 一级代码块，通常为类定义
        l1_mark: list, 与l1_list长度相同，标记l1_list中的每一行代码
        l2_list: list, 二级代码块，通常为函数定义
        l2_mark: list, 与l2_list长度相同，标记l2_list中的每一行代码
        m_obj: list, 主要的python代码块
        m1: str, 主模块名
        m2: str, 子模块名
        
        返回值:
        str, 生成的一级注释
        
        这个函数首先判断l1_list和l2_list中哪一个是主要的代码块，然后根据主要的代码块生成一级注释的关键字key，
        并检查是否已经为这个key生成过注释。如果已经生成过，就直接从缓存中取出并返回；如果没有生成过，就先移除主要代码块中的注释，
        然后调用l1_parser生成一级注释，并添加到缓存中，最后返回生成的一级注释。
        
        注意:
        这个函数可能会抛出"list error."异常，当l1_list和l2_list都为空时会抛出这个异常，这是因为至少需要一个主要的代码块来生成注释。
        """

        log(f"invoke for {m_obj}")

        if len(l2_list) > 0:
            main_list = l2_list
            main_mark = l2_mark
        if len(l1_list) > 0:
            main_list = l1_list
            main_mark = l1_mark

        if len(main_list) == 0:
            raise Exception("list error.")

        key = f"m1_{m1}_m2_{m2}_{main_list[0]}_{m_obj[0]}"
        for ll in m_obj:
            striped = ll.strip()
            if striped.startswith("#version") or striped.startswith("# version"):
                key = key + "_" + striped
                break
        if not has_item_key(key):
            remove_comment_l1 = []
            for x, mark in zip(main_list, main_mark):
                if mark != "comment":
                    remove_comment_l1.append(x)
            remove_version_mobj = []
            for x in m_obj:
                if "# version" in x:
                    continue
                else:
                    remove_version_mobj.append(x)
            res_ = self.l1_parser(content="\n".join(remove_comment_l1), main_obj="\n".join(remove_version_mobj))
            rr = res_[0][0]
            start_sp = rr.find('"""') + 3
            end_sp = rr.rfind('"""')

            result = rr[start_sp:end_sp].replace('"""', "'''").replace(">>>", "")

            buffer_item(key, f'"""{result}"""\n')
            flush()
        rr = get_buffer_item(key)

        blank_count = len(m_obj[0]) - len(m_obj[0].lstrip(' '))

        return (rr, blank_count + 4)

    def fill_comment(self):
        """
            `fill_comment`方法用于给Python代码中的类和函数添加一级注释。
        
            这个方法首先创建了一个空的字典用于存储注释信息，然后遍历了所有的文件。对于每个Python文件，
            这个方法会读取文件的所有行，然后使用`_parse_py_file`方法解析这些行并标记它们。
        
            对于每个被标记为"class_start"或"func_start"的行，方法会创建一个缓冲区并尝试用`add_l1_coment`方法为其添加注释。
            然后，这个方法会将新的注释添加到新行列表中，并在完成文件遍历后，将这些新行写回到原文件中。
        
            参数：
            无
        
            返回：
            无
        
            注意：
            1. 这个方法不支持对嵌套的类和函数添加注释。
            2. 这个方法会直接修改原始文件，可能会导致原始代码丢失。在使用这个方法前，建议先备份原始文件。
        """

        doc_dict = {}
        for d_path, d_file in self.p_bar.iter_bar(self.all_file_task):
            if not d_file.endswith(".py"):
                continue

            lines_ori = read_file_lines(d_path)
            if len(lines_ori) < 2:
                continue
            if "pass_generate" in lines_ori[0]:
                continue
            # if "tool" in d_file or "setup" in d_file or "init" in d_file or "cmd_utils" in d_file:
            #     continue

            log(f"start {d_path}")
            m1_name = d_path.split("/")[-2]
            if m1_name not in doc_dict:
                doc_dict[m1_name] = {}
            m2_name = d_file.split(".")[0]
            if m2_name not in doc_dict[m1_name]:
                doc_dict[m1_name][m2_name] = {
                    'class': {},
                    'func': {}
                }

            lines_mark = self._parse_py_file(lines_ori)

            add_commit = {}
            l1_buffer = []
            l1_mark = []
            l1_line_end = -1

            l2_buffer = []
            l2_mark = []
            l2_line_end = -1

            for (mark_idx, mark), ll in self.p_bar.iter_bar(zip(enumerate(lines_mark), lines_ori), key=m2_name,
                                                            max=len(lines_ori)):
                if mark.startswith("class_start"):
                    l1_line_start = mark_idx
                    l1_line_end = int(mark.split('_')[-1])
                    l1_buffer = lines_ori[l1_line_start:l1_line_end]
                    l1_mark = lines_mark[l1_line_start:l1_line_end]

                if mark.startswith("func_start"):
                    l2_line_start = mark_idx
                    l2_line_end = int(mark.split('_')[-1])
                    l2_buffer = lines_ori[l2_line_start:l2_line_end]
                    l2_mark = lines_mark[l2_line_start:l2_line_end]

                if mark_idx > l1_line_end:
                    l1_buffer = []
                    l1_mark = []
                    l1_line_end = -1

                if mark_idx > l2_line_end:
                    l2_buffer = []
                    l2_mark = []
                    l2_line_end = -1

                if "_start" in mark:
                    l3_buffer = []
                    type = lines_mark[mark_idx].split("_")[0]
                    for l2idx in range(mark_idx, len(lines_ori)):
                        if type in lines_mark[l2idx]:
                            l3_buffer.append(lines_ori[l2idx])
                        else:
                            break

                    add_commit[mark_idx + len(l3_buffer) - 1] = self.add_l1_coment(l1_buffer, l1_mark,
                                                                                   l2_buffer, l2_mark,
                                                                                   l3_buffer, m1_name, m2_name)

            new_lines = []
            for (mark_idx, mark), ll in zip(enumerate(lines_mark), lines_ori):
                if mark == "comment":
                    continue
                else:
                    new_lines.append(ll)

                if mark_idx in add_commit:
                    blank_count = add_commit[mark_idx][1]
                    for sp_l in add_commit[mark_idx][0].split("\n"):
                        new_lines.append(' ' * blank_count + sp_l.rstrip())
                    # new_lines.append(add_commit[mark_idx])

            # debug_list = [l + k for l, k in zip(lines_mark, lines_ori)]
            # write_file_line(os.path.join("/Users/kejiang/Desktop", d_file + ".txt"), debug_list)

            write_file_line(d_path, new_lines)

            log(f"finished {d_path}")

    def extract_name(self, code: str) -> str:
        """
        该函数的主要目的是从给定的代码字符串中提取类名或函数名。
        
        参数:
            code (str): 需要用来提取名字的代码字符串。
        
        返回:
            str: 如果找到匹配的类名或函数名则返回该名字，否则返回None。
        
        使用示例:
            name = extract_name('class MyClass:')
            print(name)  # 输出: MyClass
        
        注意:
            - 只有当代码字符串以'class'或'def'开头时，才会尝试提取名字。
            - 如果代码字符串不符合预期格式，可能无法正确提取名字。
        
        异常:
            - 无特别异常处理，如果代码字符串格式错误，可能无法返回预期结果。
        
        该函数使用正则表达式匹配，可能对性能有一定影响，如果处理大量代码字符串，建议优化或者寻找其他方法。
        """

        match = re.search('(class|def) (\w+)(?=\(|:|$)', code)
        return match.group(2) if match else None

    def _add_style_comment_content(self, lines, mdoc):
        """
        此函数的主要目的是将指定的代码行添加到Markdown文档中以创建样式化的注释内容。
        
        参数:
        - lines (List[str]): 代表源代码的字符串列表，通常每个字符串代表源代码的一行。
        - mdoc (Object): Markdown文档对象，用于写入和格式化源代码行。
        
        该函数会遍历输入的源代码行，对每一行进行处理。如果行以三引号结束（即表示注释的结束），则移除三引号并执行以下操作：
        - 如果行为空，则忽略该行；
        - 如果行以冒号结束，则在Markdown文档中添加一行标记为粗体的文本；
        - 其他情况，直接在Markdown文档中添加该行。
        
        此函数不返回任何值，但会直接修改传入的Markdown文档对象。
        
        注意：此函数不会处理源代码行中的错误或bug，如果源代码行无法正确解析为Markdown格式，可能会引发错误。
        """

        mstr = mdoc.write(Mstring())
        for ll in lines:
            nll = ll.replace('"""', "").strip()
            if nll == "":
                continue
            else:
                if nll.endswith(":") or nll.endswith("："):
                    mstr.set("\n")
                    mstr.set_bold(nll)
                else:
                    mstr.set(nll)

    def export_document(self, doc_path):

        """
        该方法用于导出项目的文档，包括每个模块的介绍，类和函数成员的信息。
        
        参数:
            doc_path (str): 文档的导出路径。
        
        返回:
            None
        
        使用方法:
            创建一个 comment_creator 实例，然后调用该方法即可将文档导出到指定的路径，例如：
            cc = comment_creator(llm, path)
            cc.export_document("./doc.md")
        
        注意:
            本方法无法处理的异常情况包括：
            1. doc_path 的指定路径不合法或无写入权限。
            2. 类或函数的注释不规范，导致无法正确解析。
        """

        doc_dict = {}

        for d_path, d_file in self.p_bar.iter_bar(self.all_file_task):
            if not d_file.endswith(".py"):
                continue

            lines_ori = read_file_lines(d_path)
            if len(lines_ori) < 2:
                continue
            if "pass_doc" in lines_ori[0]:
                continue

            m1_name = d_path.split("/")[-2]
            m2_name = d_file.split(".")[0]

            if m1_name not in doc_dict:
                doc_dict[m1_name] = {}
            if m2_name not in doc_dict[m1_name]:
                doc_dict[m1_name][m2_name] = {}

            curr_dic = doc_dict[m1_name][m2_name]

            lines_mark = self._parse_py_file(lines_ori)

            l1_buffer = []
            l1_line_end = -1

            l2_buffer = []
            l2_line_end = -1

            for (mark_idx, mark), ll in zip(enumerate(lines_mark), lines_ori):
                if mark.startswith("class_start"):
                    l1_line_start = mark_idx
                    l1_line_end = int(mark.split('_')[-1])
                    l1_buffer = lines_ori[l1_line_start:l1_line_end]

                if mark.startswith("func_start"):
                    l2_line_start = mark_idx
                    l2_line_end = int(mark.split('_')[-1])
                    l2_buffer = lines_ori[l2_line_start:l2_line_end]

                if mark_idx > l1_line_end:
                    l1_buffer = []
                    l1_line_end = -1

                if mark_idx > l2_line_end:
                    l2_buffer = []
                    l2_line_end = -1

                if mark == "comment":
                    if len(l1_buffer) == 0 and len(l2_buffer) > 0:
                        type_name = self.extract_name(l2_buffer[0])
                        if type_name not in curr_dic:
                            curr_dic[type_name] = ([], [], "func")
                        curr_dic[type_name][1].append(ll.strip())
                    if len(l1_buffer) > 0 and len(l2_buffer) > 0:
                        base_name = self.extract_name(l1_buffer[0])
                        type_name = self.extract_name(l2_buffer[0])
                        if base_name not in curr_dic:
                            curr_dic[base_name] = ([], {})
                        if type_name not in curr_dic[base_name][1]:
                            curr_dic[base_name][1][type_name] = ([], [], "class_func")
                        curr_dic[base_name][1][type_name][1].append(ll.strip())
                    if len(l1_buffer) > 0 and len(l2_buffer) == 0:
                        base_name = self.extract_name(l1_buffer[0])
                        if base_name not in curr_dic:
                            curr_dic[base_name] = ([], {}, "class")
                        curr_dic[base_name][0].append(ll.strip())

        mdoc = markdowndoc(doc_path)

        for k in doc_dict.keys():
            mdoc.write(MTitle(k, 2))
            module_line = []
            module_text = mdoc.write(Mstring())
            # mdoc.write("模块介绍 ")
            mdoc.write("类成员: \n")
            class_table = mdoc.write(MTable(["name", "info"]))
            mdoc.write("函数成员: \n")
            func_table = mdoc.write(MTable(["name", "info"]))
            for k_file, vv in doc_dict[k].items():
                for l1_name, l1_vv in doc_dict[k][k_file].items():
                    if l1_name.strip().startswith("_"):
                        continue

                    if len(l1_vv) > 2:
                        if l1_vv[2] == "class":
                            mdoc.write(MTitle(l1_name, 3))
                            parser_line = [l1_name] + l1_vv[0]
                            self._add_style_comment_content(l1_vv[0], mdoc)
                            # for ll in l1_vv[0]:
                            #     strip_ll = ll.replace('"""', '').strip()
                            #     parser_line.append(strip_ll)
                            #     if strip_ll != "":
                            #         mdoc.write(strip_ll + "\n")
                            for sf_name, sfunc in l1_vv[1].items():
                                mdoc.write(MTitle(sf_name, 4))
                                self._add_style_comment_content(sfunc[1], mdoc)
                                # for ll in sfunc[1]:
                                #     strip_ll = ll.replace('"""', '').strip()
                                #     if strip_ll != "":
                                #         mdoc.write(strip_ll + "\n")
                                # pass

                            class_discribe = self._add_memeber_summary(parser_line)
                            class_table.add_row([l1_name, class_discribe])
                            module_line.append(f"{l1_name}:{class_discribe}\n")
                        else:
                            mdoc.write(MTitle(l1_name, 3))
                            parser_line = [l1_name] + l1_vv[1]
                            self._add_style_comment_content(l1_vv[1], mdoc)
                            # for ll in l1_vv[1]:
                            #     strip_ll = ll.replace('"""', '').strip()
                            #     parser_line.append(strip_ll)
                            #     if strip_ll != "":
                            #         mdoc.write(strip_ll + "\n")
                            class_discribe = self._add_memeber_summary(parser_line)
                            func_table.add_row([l1_name, class_discribe])
                            module_line.append(f"{l1_name}:{class_discribe}\n")

            module_discribe = self._add_module_summary(module_line)
            module_text.set(module_discribe)
            pass
        mdoc.flush()
        pass


def comment_creator_cmd(path):
    """
    此函数用于创建用于添加注释的命令行工具。
    
    参数:
        path (str): 需要添加注释的文件的路径。
    
    返回:
        此函数无返回值。
    
    函数执行步骤:
        1. 首先，函数会调用get_init_llm()函数获取一个初始的词法、语法和语义模型(llm)。
        2. 然后，使用此llm和文件路径作为参数创建一个CommentCreator实例。
        3. 最后，调用fill_comment()方法来对指定文件进行注释。
    
    注意:
        1. 需要确保指定的文件路径存在，否则可能会引发异常。
        2. 本函数不会检查指定的文件是否已经存在注释，如果已经存在注释，则可能会重复添加。
        3. 本函数不会保存添加注释后的文件，如果需要保存，请在调用此函数后调用相应的保存方法。
    
    示例:
        comment_creator_cmd('/path/to/your/file')
    """

    llm = get_init_llm()
    creator = comment_creator(llm, path)
    creator.fill_comment()
