# pass_generate
import time
from tketool.lmc.prompts.prompt_controller import get_prompt
from tketool.lmc.lmc_linked import lmc_linked_model
from tketool.lmc.tasks.task_init import get_init_llm
from tketool.logs import log
import glob, os
from tketool.files import read_file, write_file_line
from tketool.utils.progressbar import process_status_bar
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def codereview(path, filter="*", addition_mark='.report'):
    """
    这是一个通过路径、过滤器和附加标记来进行代码审查的函数。
    
    函数首先检查过滤器和附加标记，如果没有设置或为空，则将其设置为默认值。然后，它会获取指定路径下所有的文件，并通过使用递归文本拆分器，将每个文件的内容拆分为大小为1000的块。
    
    对于每个文件，如果文件内容为空，则跳过该文件并继续处理下一个文件。否则，函数会将文件路径和文件长度打印到日志中。
    
    然后，该函数会逐个处理拆分后的文本块，对其进行语言模型链接，生成结果和日志。如果结果为空，则在日志中打印错误信息。否则，根据索引值将结果写入到文件中。
    
    注意，对于每个文件，第一个放入结果的文件名将附加给定的附加标记，而其他的文件名将添加索引号和附加标记。
    
    参数:
        path: str. 文件路径。处理该路径下所有的文件。
        filter: str,默认为'*'. 文件名过滤器，用于选择需要处理的文件。默认处理所有文件。
        addition_mark: str, 默认为'.report'. 用于标记处理完成的文件的附加标记。
    
    无返回值，但会生成表示处理结果的文件，文件名格式为“原始文件名+附加标记”。
    
    错误或异常:
        如果文件路径不存在或无法访问，该函数可能会抛出异常。
        如果在处理文件时遇到错误，如读取文件失败或者写入文件失败，该函数可能会抛出异常。
    
    示例:
        codereview('/path/to/files', '*.txt', '.report')
    """

    if filter is None or filter == "":
        filter = "*"
    if addition_mark is None or addition_mark == "":
        addition_mark = ".report"
    path = os.path.join(path, filter)
    llm = get_init_llm()

    link_model = lmc_linked_model(llm).set_prompt_template(get_prompt("codereviews"))

    link_model.log_state()

    allfiles = [filepath for filepath in glob.iglob(path, recursive=False)]
    pb = process_status_bar()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    for filepath in pb.iter_bar(allfiles, key="file"):
        pb.process_print(filepath)
        documents = read_file(filepath)
        documents = documents.replace("    ", " ")

        if len(documents) == 0:
            continue

        pb.print_log(f"Code File {filepath} Length:{len(documents)}")
        split_document = text_splitter.split_text(documents)
        for idx, doc_split in pb.iter_bar(enumerate(split_document), key="split", max=len(split_document)):
            results, logs = link_model(lang="chinese", content=doc_split)
            if len(results) == 0:
                pb.print_log(f"file {filepath} error.")
            else:
                if idx == 0:
                    write_file_line(filepath + addition_mark, [results[0]])
                else:
                    write_file_line(f"{filepath}_{idx}_{addition_mark}", [results[0]])
