# pass_generate
from tketool.lmc.lmc_linked import lmc_linked_model
from tketool.lmc.tasks.task_init import get_init_llm
from tketool.logs import log


def translate(lang: str, ori_text: str, tllm=None):
    """
    此函数是一个翻译函数，通过调用lmc_linked_model模型进行语言翻译。
    
    参数:
        lang (str): 目标语言名称，以字符串形式。
        ori_text (str): 需要被翻译的原文本，以字符串形式。
        tllm (model, 可选): 用于翻译的模型。如果没有提供，函数将会使用get_init_llm()函数来获取初始模型。默认值为None。
    
    返回:
        str: 翻译后的文本。如果无法进行翻译，将返回None。
    
    错误或bug:
        如果提供的原始文本为空，或者目标语言无法识别，函数可能无法正常工作。此外，如果lmc_linked_model模型无法正常工作，也可能导致函数错误。
    
    使用示例:
        translate("zh", "Hello, world!")  # 返回 "你好，世界！"
        translate("fr", "Hello, world!")  # 返回 "Bonjour, monde !"
    """

    if tllm is None:
        tllm = get_init_llm()
    link_model = lmc_linked_model(tllm).set_prompt_template("You are an excellent translator. \n"
                                                            "Please translate this paragraph into {lang} \n"
                                                            "Please keep the format of the paragraph (line breaks) \n"
                                                            "The original text is:"
                                                            "‘{content}’")

    results, _ = link_model(lang=lang, content=ori_text)

    if len(results) == 0:
        log("can't translate the paragraph.")
    else:
        # log(f"{ori_text} => {lang}")
        # print_dash_line()
        # log(results[0])

        return results[0]
