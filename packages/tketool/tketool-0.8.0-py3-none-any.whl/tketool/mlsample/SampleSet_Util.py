# pass_generate
import time, os, csv
from tketool.mlsample.LocalSampleSource import LocalDisk_NLSampleSource
from tketool.JConfig import get_config_instance
from tketool.mlsample.NLSampleSource import NLSampleSourceBase
from tketool.mlsample.MemorySampleSource import Memory_NLSampleSource
from tketool.mlsample.SampleSet import SampleSet
from prettytable import PrettyTable, ALL
from tketool.utils.progressbar import process_status_bar
from PyPDF2 import PdfReader
from tketool.mlsample.MinioSampleSource import MinioSampleSource
from tketool.mlsample.SSHSampleSource import SSHSampleSource
import fnmatch
from tketool.files import read_file
from tketool.logs import convert_print_color, log_color_enum


def _truncate_content(content, max_length):
    """
    这是一个函数，其作用是截断过长的内容并在尾部添加省略号。
    
    参数:
        content (str): 需被截断的字符串内容。
        max_length (int): 字符串的最大长度。
    
    返回:
        str: 如果原始内容长度超过最大长度，则返回截断后并在尾部添加'..'的字符串；否则返回原始字符串。
    
    注意：
        如果max_length设置为负数，则截取功能将无效，会原样返回字符串。
    
    使用示例:
        >>> _truncate_content('Hello World!', 5)
        'Hello..'
    
        >>> _truncate_content('Hello World!', 20)
        'Hello World!'
    
        >>> _truncate_content('Hello World!', -5)
        'Hello World!'
    """

    return (content[:max_length] + '..') if len(content) > max_length else content


def set_list(tsource="local", path=None, match=None):
    """
    此函数的目的是从不同的源(本地、Minio或SSH)获取并设置数据集列表。它首先根据源类型验证路径或配置，然后从源获取数据集列表信息，最后以表格形式打印出数据集的关键信息。
    
    参数:
        tsource (str)：数据源类型，默认为"local"。可选值有"local"（本地），"minio"（Minio对象存储），"ssh"（SSH服务器）。
        path (str)：数据集的路径。如果未提供，将从配置实例中获取数据集路径。
        match (str)：匹配数据集名称的模式字符串。如果提供了该参数，函数只会返回匹配该模式的数据集。
    
    返回:
        此函数没有返回值。
    
    可能的错误:
        如果指定的路径不存在，或者配置信息不完整，函数会引发异常。
        如果从源获取的数据集信息为空，函数也会引发异常。
    
    示例:
        set_list("local", "/path/to/dataset")
        set_list("minio", "/path/to/dataset", "train*")
    
    注意:
        在使用"minio"或"ssh"作为数据源类型时，你需要提供完整的配置信息，如endpoint, access_key, secret_key等。
        匹配字符串中可以使用通配符，例如"train*"匹配所有以"train"开头的数据集。
    """

    if tsource is None:
        tsource = "local"

    path = path if path else get_config_instance().get_config("sample_source_path")

    info_dict = None

    print(f"source type: {tsource}")

    if tsource == "local":
        if not os.path.exists(path):
            raise Exception(f"can not find the path : {path}")
        source = LocalDisk_NLSampleSource(path)
        info_dict = source.get_dir_list()
        info_dict = dict(sorted(info_dict.items(), key=lambda item: item[1]['create_date']))

    if tsource == "minio":
        endpoint = get_config_instance().get_config("minio_endpoint", "")
        access_key = get_config_instance().get_config("minio_access_key", "")
        secret_key = get_config_instance().get_config("minio_secret_key", "")
        bucket_name = get_config_instance().get_config("minio_bucket_name", "")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = MinioSampleSource(path, endpoint, access_key, secret_key, bucket_name)
        info_dict = source.get_remote_dir_list()

    if tsource == "ssh":
        # endpoint, access_user, secret_pwd, target_path, port=22
        endpoint = get_config_instance().get_config("ssh_endpoint", "")
        access_key = get_config_instance().get_config("ssh_access_user", "")
        secret_key = get_config_instance().get_config("ssh_secret_pwd", "")
        bucket_name = get_config_instance().get_config("ssh_target_path", "")
        port = get_config_instance().get_config("ssh_port", "22")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = SSHSampleSource(path, endpoint, access_key, secret_key, bucket_name, int(port))
        info_dict = source.get_remote_dir_list()

        pass

    if info_dict is None:
        raise Exception("Source is error.")

    xtable = PrettyTable()
    # 设置表头
    xtable.field_names = ["Set name", "Count", "Columns", "description", "base_set"]

    all_keys = list(info_dict.keys())

    if match is not None:
        all_keys = [s for s in all_keys if fnmatch.fnmatchcase(s, match)]

    for k in all_keys:
        v = info_dict[k]
        xtable.add_row([k, v['count'],
                        _truncate_content(str(v['meta']['label_keys']), 30),
                        _truncate_content(v['meta']['des'], 20),
                        _truncate_content(v['meta']['base_set'], 20)
                        ])

    print(xtable)


def download(tsource, set_name, path=None):
    """
    这个函数的主要目的是用来下载数据集的. 它主要根据`tsource`这个参数来决定数据源是哪个类型, 例如 "minio" 或者 "ssh". 如果`tsource`是"minio",那么会从minio的endpoint, 使用access key和secret key，从指定bucket中下载数据到预设的路径. 如果`tsource`是"ssh",那么会通过ssh从远程服务器的目标路径下载数据到预设的路径. 在两种情况中,如果没有给出预设的路径,那么会使用配置文件中的`sample_source_path`作为默认路径.
    
    参数:
        tsource (str): 数据源的类型, 可选的类型有 "minio" 和 "ssh".
        set_name (str): 要下载的数据集的名称.
        path (str, optional): 数据下载的预设路径. 如果没有给出, 那么会使用配置文件中的`sample_source_path`作为默认路径.
    
    返回类型:
        这个函数没有返回.
    
    异常:
        如果数据源的类型不支持, 那么会抛出一个Exception.
        如果在配置文件中找不到对应的配置信息, 那么也会抛出一个Exception.
    
    使用例子:
    ```python
        download('minio', 'dataset1', '/path/to/dataset1')
        download('ssh', 'dataset2')
    ```
    注意事项:
        这个函数在运行时会检查配置文件中对应的数据源的配置信息是否都存在，如果不存在，那么会抛出异常。
        对于ssh数据源，如果配置文件中没有提供ssh的端口信息，那么会默认使用22端口。
    """

    path = path if path else get_config_instance().get_config("sample_source_path")

    source = None

    if tsource == "minio":
        endpoint = get_config_instance().get_config("minio_endpoint", "")
        access_key = get_config_instance().get_config("minio_access_key", "")
        secret_key = get_config_instance().get_config("minio_secret_key", "")
        bucket_name = get_config_instance().get_config("minio_bucket_name", "")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = MinioSampleSource(path, endpoint, access_key, secret_key, bucket_name)

    if tsource == "ssh":
        # endpoint, access_user, secret_pwd, target_path, port=22
        endpoint = get_config_instance().get_config("ssh_endpoint", "")
        access_key = get_config_instance().get_config("ssh_access_user", "")
        secret_key = get_config_instance().get_config("ssh_secret_pwd", "")
        bucket_name = get_config_instance().get_config("ssh_target_path", "")
        port = get_config_instance().get_config("ssh_port", "22")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = SSHSampleSource(path, endpoint, access_key, secret_key, bucket_name, int(port))

        pass

    if source is None:
        raise Exception("Source Error.")

    source.download(set_name)


def upload(tsource, set_name=None, path=None):
    """
    此函数用于上传源文件到指定路径，通过读取配置文件，支持两种上传方式：minio和ssh。
    
    参数:
        tsource (str): 上传文件的类型，可以是"minio"或者"ssh"。
        set_name (str, 可选): 集合名称。默认为None。
        path (str, 可选): 文件路径。如果没有指定，则会从配置文件中读取。
    
    返回:
        无
    
    错误:
        Exception: 如果tsource不是"minio"和"ssh"之一，或者必要的配置信息不存在，将抛出异常。
    
    例子:
        upload("minio", "myset", "/path/to/myfile")
        upload("ssh", "myset", "/path/to/myfile")
    
    注意:
        此函数依赖get_config_instance函数和MinioSampleSource、SSHSampleSource类，需要先定义这些依赖才能正常使用。
        并且此函数没有进行参数合法性检查，调用者需要保证参数的正确性。
    """

    path = path if path else get_config_instance().get_config("sample_source_path")

    source = None

    if tsource == "minio":
        endpoint = get_config_instance().get_config("minio_endpoint", "")
        access_key = get_config_instance().get_config("minio_access_key", "")
        secret_key = get_config_instance().get_config("minio_secret_key", "")
        bucket_name = get_config_instance().get_config("minio_bucket_name", "")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = MinioSampleSource(path, endpoint, access_key, secret_key, bucket_name)

    if tsource == "ssh":
        # endpoint, access_user, secret_pwd, target_path, port=22
        endpoint = get_config_instance().get_config("ssh_endpoint", "")
        access_key = get_config_instance().get_config("ssh_access_user", "")
        secret_key = get_config_instance().get_config("ssh_secret_pwd", "")
        bucket_name = get_config_instance().get_config("ssh_target_path", "")
        port = get_config_instance().get_config("ssh_port", "22")

        if endpoint == "" or access_key == "" or secret_key == "" or bucket_name == "":
            raise Exception("config is None.")

        source = SSHSampleSource(path, endpoint, access_key, secret_key, bucket_name, int(port))

        pass

    if source is None:
        raise Exception("Source Error.")

    source.update(set_name)


def set_info(setname, count=5, max_len=100, path=None):
    """
    这个函数是用来打印一组特定样本的基础信息和详细信息的。基础信息包括其名称、数量、基础集、键、标签和描述等，详细信息则包括每一行数据的各个属性值以及属性的名称。
    
    参数:
        setname (str): 需要打印信息的样本集的名称。
        count (int, 可选): 想要打印的样本行数，默认为5。
        max_len (int, 可选): 每一个样本值打印的最大长度，如果超过这个长度则会被截断，截断的部分以...表示，默认为100。
        path (str, 可选): 样本文件的存储路径。如果不提供，则会从config实例中获取"sample_source_path"的值。
    
    返回值:
        无
    
    用法示例:
        set_info('train', count=10, max_len=50, path='/path/to/data')
    
    注意：
        如果providing的路径不存在，将会引发异常。此外，如果setname没有在指定路径下找到，也会引发异常。
    """

    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")
    source = LocalDisk_NLSampleSource(path)

    meta_data = source.get_metadata_keys(setname)

    print("basic info: \n")
    table = PrettyTable(header=False)
    table.hrules = ALL
    # 定义表格的列名
    table.field_names = ["Attribute", "Value"]
    # 添加数据
    table.add_row(["Name", setname])
    table.add_row(["Count", source.get_set_count(setname)])
    table.add_row(["base set", meta_data['base_set']])
    table.add_row(["keys", meta_data['label_keys']])
    table.add_row(["tags", meta_data['tags']])
    table.add_row(["des", meta_data['des']])
    print(table)
    print("Set file info:")
    source.print_set_info(setname)
    print(f"Set Data (first {str(count)} row):")
    for item in SampleSet(source, setname).take(count):
        print("---" * 3)
        for k, v in item.items():
            vv = str(v)
            v_data = f" {vv[:max_len]}"
            if len(vv) > max_len:
                print(convert_print_color((k + "\t:", log_color_enum.GREEN), v_data, ("...", log_color_enum.YELLOW)))
            else:
                print(convert_print_color((k + "\t:", log_color_enum.GREEN), v_data))


def set_data_info(setname, label_key, path=None):
    """
    此函数用于设置数据信息，并以表格形式显示每个标签键的计数。
    
    参数:
        setname (str): 需要分析的数据集名称。
        label_key (str): 数据集中的标签键。
        path (str, optional): 数据集的路径。若未提供，则从配置中获取默认路径。
    
    返回:
        无返回值。但会打印出每个标签键的计数信息。
    
    异常:
        当提供的路径不存在时，会抛出异常。
    
    示例:
        >>> set_data_info('train', 'label', '/path/to/dataset')
        可以显示训练集中每个标签的计数信息。
    
    注意:
        这个函数没有处理数据集中可能存在的空标签的情况，如果数据集中存在空标签，可能会导致错误。
    
    """

    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")
    source = LocalDisk_NLSampleSource(path)

    content_key = {}
    for item in SampleSet(source, setname):
        label_value = item[label_key]
        if label_value not in content_key:
            content_key[label_value] = 0
        content_key[label_value] += 1

    print("Data info (count of per label key): \n")
    table = PrettyTable(header=False)
    table.hrules = ALL
    # 定义表格的列名
    table.field_names = ["Attribute", "Value"]

    for k, v in content_key.items():
        table.add_row([k, v])

    print(table)


def delete_set(setname, path=None):
    """
    删除指定的数据集。
    
    这个函数会在指定的路径下查找并删除给定的数据集。如果没有提供路径，那么它会从配置文件中获取默认路径。
    
    参数:
        setname (str): 要删除的数据集的名称。
        path (str, 可选): 数据集所在的文件路径。默认为None，此时会从配置文件中获取默认路径。
    
    返回:
        无返回
    
    异常:
        如果指定的路径不存在，将会引发异常。
    
    示例:
        >>> delete_set('my_dataset', '/path/to/datasets')
        >>> "my_dataset deleted."
    
    注意:
        这个函数会永久性地从磁盘上删除数据集，所以在调用之前一定要确保备份重要数据。
    
    """

    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")
    source = LocalDisk_NLSampleSource(path)
    source.delete_set(setname)
    print(f"{setname} deleted.")


def capture_str(setname, folderpath, path=None):
    """
    `capture_str` 是一个函数，用于从给定文件夹中提取文本数据，并将结果保存到特定路径的本地磁盘或内存中。
    
    该函数将在给定的文件夹中查找所有.txt和.pdf文件，然后读取他们的内容。对于pdf文件，它将提取每一页的文本。如果遇到错误，它将记录错误信息，然后继续处理其他文件。最后，它将所有收集的数据保存到指定路径的本地磁盘或内存中。
    
    参数:
        setname (str): 创建的数据集的名称。
        folderpath (str): 包含要提取数据的文件的文件夹路径。
        path (str, 可选): 保存数据的路径。如果未提供，将使用配置实例的 "sample_source_path"。
    
    返回:
        None
    
    使用示例:
    
        capture_str("dataset1", "./data_folder", "./output_folder")
    
    注意:
        - 该函数只处理.txt和.pdf文件，遇到其他类型的文件将引发异常并记录日志。
        - 当给定的路径不存在时，该函数将引发异常。
        - 如果在处理文件时遇到错误，该函数将记录错误信息，然后继续处理其他文件。
    
    可能的错误或bug:
        - 如果文件夹中的文件数量过多，可能会导致内存问题。
        - 如果pdf文件的页数过多，可能会导致处理速度慢。
        - 如果文件内容包含无法正确解析的字符，可能会引发异常。
    """

    path = path if path else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(path):
        raise Exception(f"can not find the path : {path}")

    source = LocalDisk_NLSampleSource(path)
    # source = Memory_NLSampleSource()
    source.create_new_set(setname, "capture from folder", ['capture'], ['filename', 'text'])

    pb = process_status_bar()
    allfiles = os.listdir(folderpath)

    for filename in pb.iter_bar(allfiles):
        try:
            name, ext = os.path.splitext(filename)
            if ext == ".txt":
                content = read_file(os.path.join(folderpath, filename))
                source.add_row(setname, [filename, content])
                continue

            if ext == '.pdf':
                pdf_file_obj = open(os.path.join(folderpath, filename), 'rb')
                pdf_reader = PdfReader(pdf_file_obj)

                text = ''
                for page in pdf_reader.pages:
                    # page_obj = pdf_reader.pages[page_num]  # getPage(page_num)
                    text += page.extract_text()
                pdf_file_obj.close()
                source.add_row(setname, [filename, text])
                continue

            raise Exception(f"Can't capture the file {filename}")


        except Exception as ex:
            pb.print_log(f"file {filename} error. {ex}")

    source.flush()


def output_csv(setname, tpath=None, path="a.csv", count=100):
    """
    这个函数的目的是从给定的源路径读取一定数量的样本数据，并将其输出保存到CSV文件中。
    
    参数:
        setname (str): 具有样本数据的集合名称。
        tpath (str, 可选): 源路径。如果未提供，将使用配置文件中的"sample_source_path"。默认值为None。
        path (str, 可选): 保存CSV文件的路径。默认值为"a.csv"。
        count (int, 可选): 从setname中读取的样本数量。默认值为100。
    
    返回类型:
        此函数无返回值。执行完毕后，将在指定的路径保存CSV文件。
    
    使用示例：
        output_csv("mySet", tpath="/my/path", path="/my/path/a.csv", count=200)
    
    注意:
        如果提供的tpath不存在，或者在配置文件中没有定义"sample_source_path"，则会引发异常。
        source使用的是LocalDisk_NLSampleSource，此类专门用于从本地磁盘读取样本数据。
        使用csv.writer将数据写入csv文件，可以保证有效的数据存储和读取。
    """

    spath = tpath if tpath else get_config_instance().get_config("sample_source_path")
    if not os.path.exists(spath):
        raise Exception(f"can not find the path : {spath}")

    source = LocalDisk_NLSampleSource(spath)

    meta_data = source.get_metadata_keys(setname)

    keyslist = meta_data['label_keys']
    data = [keyslist]

    for item in SampleSet(source, setname).take(count):
        data.append([item[k] for k in keyslist])

    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


# def Info_of_set(sample_set: SampleSet, key_func):
#     key_dict = {}
#     for item in sample_set:
#         lable = key_func(item)
#         if lable not in key_dict:
#             key_dict[lable] = 0
#         key_dict[lable] += 1
#
#     # PRINT
#     print("\n 统计结果:")
#     for k, v in key_dict.items():
#         print(f"{k} : {v} \n")


def SplitSet(samplesource: NLSampleSourceBase, ori_set_name: str, key_func,
             name_to_key_dict: dict, need_shuffle=True):
    """
    该函数用于根据给定的名称-键字典对样本源进行分割。每个键值对应的样本都会生成一个新的独立样本集，新生成的样本集将会以"原样本集_键名"的形式命名。
    
    参数:
        samplesource(NLSampleSourceBase): 用于操作的样本来源。
        ori_set_name(str): 需要被分割的原始样本集的名称。
        key_func: 用于从样本中提取键的函数。
        name_to_key_dict(dict): 用于划分新样本集的名称-键字典。字典的键将作为新样本集的名称，字典的值用于匹配样本。
        need_shuffle(bool, optional): 是否需要对原始样本集进行乱序处理。默认为True。
    
    返回值:
        无返回值。
    
    注意事项:
        新生成的样本集将会包含原始样本集的所有元数据。
    
    举例:
        假设我们有一个名为"total"的样本集，我们想根据样本的标签将其分割成两个子集"positive"和"negative"。那么我们可以这样使用该函数：
        ```
        def get_label(sample):
            return sample['label']
    
        name_to_key_dict = {
            "positive": {1: 10000},
            "negative": {0: 10000}
        }
        SplitSet(sample_source, "total", get_label, name_to_key_dict)
        ```
        这样，"total"样本集就被分割成了"total_positive"和"total_negative"两个样本集，每个样本集包含了10000个样本。
    """

    meta_data = samplesource.get_metadata_keys(ori_set_name)
    new_set_name_gen_list = []

    # Create new sample sets based on the provided name-to-key dictionary
    for n_setname in name_to_key_dict.keys():
        n_name = f"{ori_set_name}_{n_setname}"
        samplesource.create_new_set(n_name, f"split from {ori_set_name}", ["split"],
                                    meta_data['label_keys'], ori_set_name)
        new_set_name_gen_list.append(n_name)

    sample_set = SampleSet(samplesource, ori_set_name)
    if need_shuffle:
        sample_set = sample_set.shuffle()

    # Initialize a list of counters, each element is a dictionary to track the label count for a subset
    count_list = [{} for _ in name_to_key_dict.values()]

    for item in sample_set:
        cur_label = key_func(item)
        list_formattor = [item[key] for key in meta_data['label_keys']]
        # Find the appropriate subset
        for idx, subset_name in enumerate(name_to_key_dict.keys()):
            subset_dict = name_to_key_dict[subset_name]
            if cur_label in subset_dict and subset_dict[cur_label] > count_list[idx].get(cur_label, 0):
                samplesource.add_row(new_set_name_gen_list[idx], list_formattor)
                count_list[idx][cur_label] = count_list[idx].get(cur_label, 0) + 1
                break

    samplesource.flush()
