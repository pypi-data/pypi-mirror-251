# pass_generate
import httpx
from langchain.callbacks.manager import CallbackManagerForLLMRun
from typing import Optional, List, Dict, Mapping, Any
from tketool.lmc.models import LLM_Plus
import requests, os
from openai import AsyncClient, AsyncOpenAI, OpenAI


class ChatGLM(LLM_Plus):
    """
    这是一个名为`ChatGLM`的类，该类继承自基类`LLM_Plus`。该类主要用于实现和外部模型交互的API请求功能。
    
    主要包含三个方法：`__init__`，`_post` 和 `call_model`。
    
    `__init__`方法用于初始化ChatGLM类的实例。需要传入一个url字符串参数（用于API调用的url）和`**kwargs`参数（用于传入模型的其他参数）。
    
    `_post`方法用于向指定的url发送post请求。传入的参数包括一个url字符串和一个包含请求内容的字典。
    
    `call_model`方法用于调用模型。传入的参数包括一个prompt字符串（作为模型的输入）和其他可选的参数。该方法会对模型的返回结果进行处理，如果请求成功返回模型的预测结果，否则返回错误信息。
    
    类的使用示例：
    
    ```python
    chat_glm = ChatGLM("your_url")
    prompt = "你好，世界"
    result = chat_glm.call_model(prompt)
    # 返回模型的预测结果或错误信息
    print(result)
    ```
    
    注意：响应时间取决于模型的处理速度和网络状况，请在使用时确保网络通畅，以便及时获取请求结果。
    """

    gurl: str = ""

    def __init__(self, _url, **kwargs: Any):
        """
            这是ChatGLM类的初始化函数，用于初始化该类的实例。
        
            本方法首先通过调用父类的初始化方法，初始化LLM_Plus类，并设置模型的名称为"GLM6B"；
            然后，设置类变量gurl的值为参数_url，该变量将被用于后续的网络请求。
        
            Args:
                _url (str): 用于网络请求的URL地址
                **kwargs (Any): 可接收任何关键字参数，这些参数会被传递给父类LLM_Plus的初始化方法
        
            例子:
        
            ```
                chat_glm = ChatGLM(_url="http://example.com", token="my_token")
            ```
        
            在此例子中，我们创建了一个ChatGLM的实例，_url参数设置为"http://example.com"，
            并且通过kwargs传递了一个名为token的参数值为"my_token"到父类LLM_Plus的初始化方法中。
        """

        model_name = "GLM6B"
        super().__init__(model_name, **kwargs)
        self.gurl = _url

    def _post(self, url: str,
              query: Dict) -> Any:
        """
        这是一个私有的_post方法，用于向服务器发送POST请求。
        
        参数:
        url: str, 服务器的URL地址。
        query: Dict, 要发送的数据，以字典形式存在。
        
        返回:
        Any, 返回服务器的响应。
        
        使用方法:
        
        _post方法通常在类的内部使用，作为向服务器发送请求的工具函数。该函数使用了requests库的session对象进行网络请求，
        在请求过程中，设置了请求头为"Content_Type": "application/json"，并对请求进行了60秒的超时设置。
        在请求成功后，该函数返回服务器的响应。
        
        例如：
        假设我们有一个名为'query'的字典，包含我们要发送的数据。我们可以这样调用_post方法：
        
        response = self._post(url="http://example.com", query=query)
        
        注意：
        由于这是一个私有方法，所以通常只在类的内部使用。在类的外部调用可能会引发错误。
        """

        _headers = {"Content_Type": "application/json"}
        with requests.session() as sess:
            resp = sess.post(url,
                             json=query,
                             headers=_headers,
                             timeout=60)

        return resp

    def call_model(self, prompt, *args, **kwargs) -> Any:
        """
        这个方法是ChatGLM类的一部分，用于调用模型并获取预测结果。
        
        参数:
            prompt (str): 输入的提示，模型将根据该提示生成预测结果。
            *args: 变长参数，根据需要使用。
            **kwargs: 变长关键字参数，可以传递任意数量的关键字参数。
        
        返回:
            predictions (Any): 如果请求成功（HTTP状态码为200），则返回模型的预测结果；否则返回错误提示信息"请求模型Error"。
        
        使用示例:
        
        ```python
            glm = ChatGLM(_url='http://localhost:8000')
            prompt = "你好"
            print(glm.call_model(prompt))
        ```
        """

        query = {
            "prompt": prompt,
            "history": []
        }
        # post
        resp = self._post(url=self.gurl,
                          query=query)

        if resp.status_code == 200:
            resp_json = resp.json()
            predictions = resp_json["response"]

            return predictions
        else:
            return "请求模型Error"


class OpenAI_Complete_Model(LLM_Plus):
    """
    OpenAI_Complete_Model类是一个继承自LLM_Plus的类，用于实现与OpenAI对话模型的交互。在初始化时，它会根据提供的api token和模型名称初始化OpenAI客户端。这个类主要包含五个方法：`_construct_query`、`_invoke_model`、`_parse_invoke_result`、`call_model` 和`add_token_use`。
    
    类初始化方法`__init__`:
    - 参数:
        - `apitoken`(str): OpenAI的API认证令牌。
        - `model_name`(str): OpenAI模型的名称。
        - `price`(float): 调用模型的价格。
        - `**kwargs`(dict): 其他任意的关键字参数。
    - 返回: None
    
    方法`_construct_query`:
    - 功能: 构造一个查询请求，用于进一步向模型发送。
    - 参数:
        - `prompt`(str): 用户给模型的提示或问题。
    - 返回: 构造好的查询请求列表。
    
    方法`_invoke_model`:
    - 功能: 使用OpenAI客户端调用聊天模型，并返回响应。
    - 参数:
        - `prompt`(str): 用户给模型的提示或问题。
    - 返回: OpenAI聊天模型的响应。
    
    方法`_parse_invoke_result`:
    - 功能: 解析模型响应，获取并返回模型的回答，并记录消耗的token数。
    - 参数:
        - `response`(dict): OpenAI聊天模型的响应。
    - 返回: 模型的回答。
    
    方法`call_model`:
    - 功能: 调用上述三个方法，完成从构造请求到获取模型回答的整个过程。
    - 参数:
        - `prompt`(str): 用户给模型的提示或问题。
        - `*args`(tuple): 其他任意位置参数。
        - `**kwargs`(dict): 其他任意的关键字参数。
    - 返回: 模型的回答。
    
    使用例子：
    ```python
    model = OpenAI_Complete_Model(token, 'text-davinci-002', 0.06)
    prompt = 'Translate the following English text to French: {}'
    result = model.call_model(prompt.format('Hello, World!'))
    print(result)
    ```
    """

    api_token: Optional[str] = None
    client: Optional[OpenAI] = None

    def __init__(self, apitoken, model_name, price, **kwargs: Any):
        """
        这是一个初始化OpenAI_Complete_Model类的方法。该类继承自LLM_Plus类，用于与OpenAI API进行交互，获取模型预测的结果。
        
        初始化方法需要用户提供API的token，模型名称，以及模型的价格。
        
        如果用户希望使用代理，可以通过关键字参数proxy来设置。
        
        参数:
        
            apitoken: OpenAI平台的API token，类型为字符串，用于API调用的身份验证。
        
            model_name: OpenAI平台的模型名称，类型为字符串，指定调用哪个模型。
        
            price: 模型的价格，类型为数字，用于计算使用模型的费用。
        
            **kwargs: 任意额外的关键字参数，可能包括代理设置，传给父类LLM_Plus的初始化方法。
        
        返回：
        
            无返回值。
        
        示例:
        
            model = OpenAI_Complete_Model('API_TOKEN', 'gpt-3', 0.06, proxy='http://localhost:8080')
            result = model.call_model('Hello, World!')
        
        注意事项：
        
            在使用代理时，需要保证代理的可用性和安全性，否则可能会影响API的调用和结果。
        """

        super().__init__(model_name, price=price, **kwargs)  # (0.03, 0.06)

        self.api_token = apitoken

        http_client = None
        if self.proxy is not None:
            # os.environ['OPENAI_API_PROXY'] = ""
            http_client = httpx.Client(
                proxies=self.proxy
            )

        self.client = OpenAI(
            api_key=self.api_token,
            http_client=http_client
        )

    def _construct_query(self, prompt: str) -> List:
        """
        这个方法是用于构建查询的。在OpenAI Complete模型中，查询是以一个列表的形式存在的，列表中的元素是一个字典，键为'role'和'content'。'role'是一个字符串，表示发送消息的角色，这里是'user'，'content'是一个字符串，表示用户输入的提示。
        
        参数:
        prompt: str类型，表示用户输入的提示。
        
        返回:
        返回一个列表，列表中的元素是一个字典，键为'role'和'content'。
        
        示例:
        ```python
        def _construct_query(self, "你好"):
            # 返回: [{"role": "user", "content": "你好"}]
        ```
        """

        query = [
            {"role": "user", "content": prompt}
        ]
        return query

    def _invoke_model(self, prompt):
        """
        该函数用于调用模型并获取响应。
        
        参数:
            prompt: str类型，传入的用户提示信息。
        
        返回:
            返回从OpenAI接口获取的响应结果，通常是模型生成的文本结果。
        
        在此函数中，我们使用了OpenAI的chat.completions.create接口来调用我们的模型。我们将用户的提示信息（prompt）传入模型，并将模型的响应结果返回。返回的结果将在后续的_parse_invoke_result函数中进行解析。
        """

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=prompt,
            **self.call_dictionary_config
        )

        return response

    def _parse_invoke_result(self, response):
        """
            此函数的目的是解析模型调用的响应，并从响应中抽取所需的信息。
        
            该函数首先从响应中获取答案内容。接着，它获取输入（prompt）和补全所用的令牌（token）数量。最后，它会添加令牌的使用情况并返回答案。
        
            参数:
            response: OpenAI的模型调用响应。它是一个包含模型生成的文本、令牌的数量等信息的对象。
        
            返回:
            返回从响应中获取的答案内容，它是一个字符串。
        
            注意:
            这个函数没有错误处理机制，如果响应的结构与预期不符，可能会引发异常。例如，如果响应中没有"choices"键，将无法获取到答案内容。
        """

        answer = response.choices[0].message.content

        prompt_token_count = response.usage.prompt_tokens
        completion_token_count = response.usage.completion_tokens

        self.add_token_use((prompt_token_count, completion_token_count))

        return answer

    def call_model(self, prompt, *args, **kwargs) -> Any:
        """
        该函数是模型类OpenAI_Complete_Model的一个方法，用于调用模型并返回模型的输出结果。
        
        参数:
            prompt (str): 用户的输入提示，模型将基于此提示生成相应的回答或完成相应的任务。
            *args: 可变参数，根据具体需要传入。
            **kwargs: 关键字参数，根据具体需要传入。
        
        返回:
            Any: 返回模型生成的回答或完成任务的结果。
        
        用法示例:
            model = OpenAI_Complete_Model(apitoken="your_api_token", model_name="gpt-3", price=0.05)
            result = model.call_model(prompt="Translate the following English text to French: '{}'", *args, **kwargs)
        
        注意:
            在使用该函数时，需要确保已经正确设置了OpenAI的API密钥，并且已经选择了正确的模型。
        """

        query = self._construct_query(prompt)
        invoke_result = self._invoke_model(query)
        result = self._parse_invoke_result(invoke_result)

        return result


class ChatGPT4(OpenAI_Complete_Model):
    """
    ChatGPT4是一个继承自OpenAI_Complete_Model的类，用于创建并管理OpenAI的GPT-4聊天模型的实例。
    
    这个类的主要目的是使用OpenAI的API，利用提供的API令牌，实现与GPT-4聊天模型的交互。
    
    示例：
    
    ```python
    # 使用API令牌初始化ChatGPT4实例
    chatgpt = ChatGPT4(apitoken='your_openai_api_token')
    
    # 使用ChatGPT4实例进行一些操作，例如生成文本
    generated_text = chatgpt.generate_text(input_text='Hello, world!')
    ```
    
    参数:
    
    - `apitoken`: OpenAI的API令牌，是一个字符串，用于进行身份验证和API访问。
    - `kwargs`: 其他可选参数，可以传递给OpenAI_Complete_Model的初始化方法。
    
    注意：
    
    - 请确保你的OpenAI API令牌是有效的，否则将无法使用GPT-4模型。
    - 这个类没有明确的返回类型，它的主要作用是创建和管理GPT-4模型的实例。
    """

    def __init__(self, apitoken, **kwargs: Any):
        """
        初始化ChatGPT4类的实例。
        
        这个类是OpenAI_Complete_Model的子类，用于创建和管理GPT-4模型的实例。通过这个类，我们可以方便地调用和使用OpenAI的GPT-4模型进行各种任务。这个类在初始化时需要传入OpenAI的API令牌，这样才能正确地使用模型。
        
        参数：
            apitoken (str): OpenAI的API令牌，用于验证用户身份和调用模型。
            **kwargs: 任意关键字参数，这些参数将直接传递给OpenAI_Complete_Model的构造函数。
        
        例子：
            >>> model = ChatGPT4('YOUR_OPENAI_TOKEN')
            >>> output = model.generate_prompt('Hello, world')
        
        注意：
            请确保你的OpenAI API令牌是正确的，错误的令牌可能会导致无法调用模型。
            当前版本的类并不支持修改GPT-4模型的配置，模型的temperature和max tokens是固定的。
        
        """

        super().__init__(apitoken, "gpt-4", (0.03, 0.06), **kwargs)


class ChatGPT3(OpenAI_Complete_Model):
    """
    这是一个继承自OpenAI_Complete_Model的聊天模型类ChatGPT3。主要用于实现和Gpt-3.5的交互，包括生成文本等。
    
    参数:
    apitoken: API访问密钥。用于验证和建立与OpenAI模型的连接。
    **kwargs: 可以接受任意关键字参数。这些参数将传递给父类。
    
    使用示例:
    ```python
    apitoken = "你的API密钥"
    model = ChatGPT3(apitoken)
    generated_text = model.generate("你想说的话")
    ```
    
    注意：
      - 必须要有API访问密钥才能使用这个模型。
      - **kwargs 的参数将会传递给父类，具体取决于父类如何处理这些参数。
    """

    def __init__(self, apitoken, **kwargs: Any):
        """
        初始化ChatGPT3类。
        
        此类是OpenAI_Complete_Model的子类，用于创建ChatGPT3对象。
        
        ChatGPT3类实例化后，将创建一个与GPT-3.5-turbo模型的连接。
        
        参数：
            apitoken(str): OpenAI API的令牌。
            kwargs(dict, optional): 可选参数，用于控制模型的具体行为。可能包含例如temperature、max_tokens等参数。
        
        返回：
            None
        
        例子：
            >>> chatgpt = ChatGPT3(apitoken="your_api_token")
            >>> response = chatgpt.generate(prompt="Hello, world!")
        
        注意：
        此类需要有效的OpenAI API令牌才能使用。
        """

        super().__init__(apitoken, "gpt-3.5-turbo-0613", (0.0015, 0.002), **kwargs)


class FineTuned_Completion_Model(OpenAI_Complete_Model):
    """
    这是一个细调完成模型类，它继承自OpenAI_Complete_Model类。
    
    细调完成模型类主要用于自定义OpenAI的模型参数。它的构造函数需要两个参数：模型ID和API令牌。在初始化时，它将模型的ID和API令牌传递给超类，同时设置模型的温度范围为0.03到0.06。
    
    使用示例：
    ```
    model = FineTuned_Completion_Model('text-davinci-002', 'my-api-token')
    ```
    
    参数:
    - model_id: 一个字符串，表示OpenAI模型的ID
    - apitoken: 一个字符串，表示API的令牌
    - **kwargs: 任意数量的关键字参数
    
    注意：尽管这个类已经设置了模型的温度范围，但是你仍然可以通过传入关键字参数来自定义设置。
    
    注意：这个类没有明显的错误或bug，但是在使用时需要注意API的令牌安全。
    
    请确保你的API令牌是正确且安全的，否则可能会导致无法访问模型的错误。
    """

    def __init__(self, model_id, apitoken, **kwargs: Any):
        """
        这是FineTuned_Completion_Model类的构造函数, 这个类是OpenAI_Complete_Model的子类, 用于实现微调模型的功能。
        
        参数:
            model_id: 用于微调的模型的ID
            apitoken: 连接OpenAI API的令牌
            **kwargs: 任意数量的关键字参数, 这些参数将传递给父类的构造函数。
        
        返回:
            无返回值
        
        使用示例:
            model = FineTuned_Completion_Model(model_id="text-davinci-001", apitoken="my-token", temperature=0.5)
        
        注意:
            我们在这里假设OpenAI_Complete_Model类的构造函数接受模型ID、API令牌和一个浮点数元组作为参数，如果实际情况并非如此，请根据实际情况进行修改。
        """

        super().__init__(apitoken, model_id, (0.03, 0.06), **kwargs)
