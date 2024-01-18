# pass_generate
import io
import paramiko
from paramiko import SFTPClient, SSHClient
from tketool.mlsample.LocalSampleSource import LocalDisk_NLSampleSource
from tketool.JConfig import get_config_instance
from tketool.files import create_folder_if_not_exists
from tketool.utils.progressbar import process_status_bar
from tketool.logs import log
import os


class SSHSampleSource(LocalDisk_NLSampleSource):
    """
    SSHSampleSource类是一个用于处理SSH源文件的类，继承自LocalDisk_NLSampleSource类。这个类实现了各种对SSH源文件的操作，包括下载、更新、创建新的数据集、检查数据集是否存在、添加行、获取元数据键、迭代数据、获取远程目录列表等等。
    
    注意：此类需要先安装paramiko库才能使用。
    
    类的初始化函数参数介绍：
    - folder_path: 本地文件夹路径
    - endpoint: SSH服务器的IP地址或者主机名
    - access_user: SSH登录的用户名
    - secret_pwd: SSH登录的密码
    - target_path: SSH服务器上的目标文件夹路径
    - port: SSH服务器的端口，默认为22
    
    使用示例:
    ```python
    ssh_source = SSHSampleSource('/local/path', 'ssh.server.com', 'user', 'password', '/remote/path')
    ssh_source.download('dataset_name')
    ```
    
    此类可能存在的问题:
    - 对于大文件的同步可能会有性能问题
    - 当SSH服务器连接问题时，可能会出现异常
    - 使用的SSH连接库paramiko没有对并发做优化，可能会有并发问题
    """

    @staticmethod
    def instance_default():
        """
        这是一个staticmethod，命名为instance_default的类方法。这个方法主要用于获取配置信息，并依据这些配置信息创建一个SSHSampleSource实例。
        
        这个方法的工作流程是：
        1. 通过调用get_config_instance().get_config("ssh_samplesource_xxx")函数，获取必要的SSH连接参数，包括folder_path, endpoint, access_user, access_pwd和access_target_path等。
        2. 使用上述获取的参数创建并返回一个SSHSampleSource实例。
        
        返回类型：
        该方法返回一个SSHSampleSource类的实例。
        
        使用示例：
        sample_source = SSHSampleSource.instance_default()
        
        注意事项：
        在使用这个方法的过程中需要注意，所有的配置信息都需要在应用的配置文件中进行预设，并且这个方法在读取配置信息的时候不会进行任何的错误处理，所以如果配置信息不存在或者格式错误，都会导致程序运行错误。
        """

        folder_path = get_config_instance().get_config("ssh_samplesource_folderpath")
        endpoint = get_config_instance().get_config("ssh_samplesource_endpoint")
        access_user = get_config_instance().get_config("ssh_samplesource_user")
        access_pwd = get_config_instance().get_config("ssh_samplesource_pwd")
        access_target_path = get_config_instance().get_config("ssh_samplesource_target_apth")

        return SSHSampleSource(folder_path, endpoint, access_user, access_pwd, access_target_path)

    def __init__(self, folder_path, endpoint, access_user, secret_pwd, target_path, port=22):
        """"""
