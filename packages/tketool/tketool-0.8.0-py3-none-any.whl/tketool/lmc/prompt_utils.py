# pass_generate
from tketool.files import *
from tketool.lmc.prompts.prompt_controller import *
from tketool.lmc.tasks.translate import translate
from tketool.lmc.tasks.task_init import get_init_llm
from tketool.utils.progressbar import process_status_bar


def update_prompt_folder(root_folder, llm=None):
    """
    这个函数的主要功能是更新指定根文件夹下的文档。它首先读取所有内容，并将其存储在名为all_content的字典中。然后，该函数通过遍历语言和内容来更新内容，找到最新的版本，并根据需要创建更新任务。
    
    在更新完成后，该函数使用进度条显示更新的状态，并执行更新任务。如果在执行过程中发生错误，程序将抛出异常。
    
    参数:
    root_folder: str，需要更新的文件夹路径
    llm: 一个可选参数，默认为None。如果没有提供，那么函数将使用get_init_llm()来初始化。
    
    返回:
    无返回值
    
    错误:
    如果翻译失败，函数将抛出异常。
    
    使用示例:
    假设我们有一个名为"prompts"的文件夹，我们希望更新其中的内容，我们可以按照以下方式使用此函数：
    ```python
    update_prompt_folder("prompts")
    ```
    """

    if llm is None:
        llm = get_init_llm()

    # read all content
    all_content = {name: {} for _, name in enum_directories(root_folder)}
    all_langs = [k for k in all_content.keys()]

    for lang in all_langs:
        for fpath, fname in enum_files(os.path.join(root_folder, lang)):
            prompt_key = fname.split('.')[0]
            all_content[lang][prompt_key] = read_prompt_file(fpath)

    # update
    finished_prompt = set()
    worklist = []
    for lang in all_langs:
        for kk, vv in all_content[lang].items():
            if kk in finished_prompt:
                continue
            standard_ver = vv['version']
            stardard_item = vv
            # find last version
            for lang2 in all_langs:
                if kk in all_content[lang2]:
                    if float(all_content[lang2][kk]['version']) > float(standard_ver):
                        standard_ver = all_content[lang2][kk]['version']
                        stardard_item = all_content[lang2][kk]

            # create task
            for lang2 in all_langs:
                if kk not in all_content[lang2] or float(standard_ver) > float(all_content[lang2][kk]['version']):
                    worklist.append((kk, lang2, stardard_item))

            finished_prompt.add(kk)

    pb = process_status_bar()
    # do task
    for key, tolang, item in pb.iter_bar(worklist, key="translate task"):
        translate_str = translate(tolang, item['templatestr'], tllm=llm)
        path = os.path.join(root_folder, tolang, f"{key}.txt")
        if translate_str is None:
            raise Exception("translate failed.")
        write_prompt_file(path, item['version'], item['description'], item['params'], translate_str)
        pb.print_log(f"translate {key} to {tolang} in version {item['version']} \n")
