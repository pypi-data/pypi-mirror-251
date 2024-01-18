# pass_generate
from tketool.JConfig import get_config_instance
from tketool.lmc.models import *
from tketool.ServiceShelve import Service_Shelve
# from langchain.chat_models import ChatOpenAI
import os


def get_init_llm():
    """
    这个函数的主要功能是初始化llm模型。它首先从Service_Shelve类实例中获取配置，提取出llm模型的类型，然后根据llm模型的类型分别初始化对应的模型。目前支持的模型类型有"gpt4"和"glm"。
    
    参数:
    无
    
    返回:
    返回初始化后的llm模型实例。
    
    错误处理:
    如果配置中的llm模型类型不在支持的类型列表中（"gpt4", "glm"），则会抛出异常。
    
    示例:
    
    ```python
    llm = get_init_llm()
    ```
    
    注意：
    在使用这个函数之前，需要确保已经正确配置了llm模型的类型。
    
    """

    service_shelve = Service_Shelve("")
    llm_type = service_shelve.get_config().get_config("llm_type", "chatgpt")

    if llm_type == "gpt4":
        return service_shelve.get_llm_GPT4()
        # return OpenAI(temperature=float(temperature), model_name=model_name)

    if llm_type == "glm":
        return service_shelve.get_llm_GLM6B()

    raise Exception("Notset")
