import json
from pathlib import Path



import requests
import shutil
import os
import chevron


from nonebot_plugin_gocqhttpQQ.exceptions import BadConfigFormat
from nonebot_plugin_gocqhttpQQ.plugin_config import config

from ..plugin_config import AccountConfig, driver_config, onebot_config
from .device import DeviceInfo, random_device
from .download import ACCOUNTS_DATA_PATH


class AccountConfigHelper:
    CONFIG_TEMPLATE_PATH = (
        Path(config.CONFIG_TEMPLATE_PATH)
        if config.CONFIG_TEMPLATE_PATH
        else Path(__file__).parent / "config-template.yml"
    )

    TEMPLATE_FILE_NAME = "config-template.yml"
    CONFIG_FILE_NAME = "config.yml"          

    def __init__(self, account: AccountConfig):
        self.account = account                                       
        self.account_path = ACCOUNTS_DATA_PATH / str(account.uin)        
        self.account_path.mkdir(parents=True, exist_ok=True)     
              
        self.template_path = self.account_path / self.TEMPLATE_FILE_NAME    
        self.config_path = self.account_path / self.CONFIG_FILE_NAME    
        
        #在账号文件夹中直接创建 versions 方便直接读取协议而不是让账号登录在创建
        self.data_path = self.account_path / 'data'
        self.data_path.mkdir(exist_ok=True)
        self.versions_path = self.data_path / 'versions'
        self.versions_path.mkdir(exist_ok=True)     

        # 在机器人的目录 accounts 文件夹创建一个 xieyi 文件夹
        self.xieyi_path = ACCOUNTS_DATA_PATH / 'xieyi'

        # 创建一个名为'xieyi'的子目录，如果该目录已经存在，则不会抛出异常
        self.xieyi_path.mkdir(exist_ok=True)
        
        # 遍历 self.xieyi_path 目录下的所有文件和子目录
        for file in os.listdir(self.xieyi_path):

            # 从 xieyi 文件复制 versions 文件夹目录
            shutil.copy2(os.path.join(self.xieyi_path, file), self.versions_path)

           
    def download_files():  
        # 下载的文件夹路径 一般在机器人目录的accounts中
        xieyi_folder = "accounts/xieyi/" 
        # 下载的文件链接
        link1 = "https://download.fgit.cf/2027839379/ranran/releases/download/8.9.90/1.json"
        link6 = "https://download.fgit.cf/2027839379/ranran/releases/download/8.9.90/6.json" 

        # 检查文件夹是否存在或者文件夹中是否有文件，没有将会自动下载
        if not os.path.exists(xieyi_folder) or len(os.listdir(xieyi_folder)) == 0:
            print("gocq协议文件下载中...")

            try:
                response1 = requests.get(link1)                  # 发送请求获取第一个链接
                with open(xieyi_folder + '1.json', 'wb') as f:   # 打开文件进行写操作
                    f.write(response1.content)                   # 将响应内容写入文件

            except Exception as e:                               # 如果出现异常则捕获并打印错误信息
                print(f'Failed to download {link1}: {e}')

            else:
                try:
                    response2 = requests.get(link6)              # 发送请求获取第二个链接的内容
                    with open(xieyi_folder + '6.json', 'wb') as f:
                        f.write(response2.content)

                except Exception as e:
                    print(f'Failed to download {link6}: {e}')    
 
    
    download_files()     # 调用 download_files() 函数执行下载操作

             


    @property
    
    def exists(self):
        return self.config_path.is_file() and self.template_path.is_file()

    def read(self) -> str:
        return self.template_path.read_text(encoding="utf-8")

    def write(self, content: str) -> int:
        return self.template_path.write_text(content, encoding="utf-8")

    def generate(self):
        return self.template_path.write_text(
            self.CONFIG_TEMPLATE_PATH.read_text(encoding="utf-8"), encoding="utf-8"
        )
        
        
        
    def before_run(self):
        template_string = self.read()
        host = (
            "127.0.0.1"
            if driver_config.host.is_loopback or driver_config.host.is_unspecified
            else driver_config.host
        )
        rendered_string = chevron.render(
            template_string,
            data={
                "account": self.account,
                "server_address": f"ws://{host}:{driver_config.port}/onebot/v11/ws",
                "access_token": onebot_config.onebot_access_token or "",
            },
        )
        return self.config_path.write_text(rendered_string, encoding="utf-8")
        


 
class AccountDeviceHelper:
    DEVICE_FILE_NAME = "device.json"

    def __init__(self, account: AccountConfig):
        self.account = account
        self.account_path = ACCOUNTS_DATA_PATH / str(account.uin)
        self.account_path.mkdir(parents=True, exist_ok=True)

        self.device_path = self.account_path / self.DEVICE_FILE_NAME

    @property
    def exists(self):
        return self.device_path.is_file()

    def read(self) -> DeviceInfo:
        with self.device_path.open("rt", encoding="utf-8") as f:
            try:
                content = json.load(f)
            except json.JSONDecodeError as e:
                raise BadConfigFormat(BadConfigFormat.message + str(e)) from None
        return DeviceInfo.parse_obj(content)

    def write(self, content: DeviceInfo) -> int:
        return self.device_path.write_text(
            content.json(indent=4, ensure_ascii=False), encoding="utf-8"
        )

    def generate(self):
        generated_device = random_device(
            self.account.uin, self.account.protocol, **config.DEVICE_OVERRIDE
        )
        return self.write(generated_device)

    def before_run(self):
        device_content = self.read()
        device_content.protocol = self.account.protocol
        return self.write(device_content)



    
class SessionTokenHelper:
    SESSION_FILE_NAME = "session.token"
    
    def __init__(self, account: AccountConfig):
        self.account = account
        self.account_path = ACCOUNTS_DATA_PATH / str(account.uin)
        self.account_path.mkdir(parents=True, exist_ok=True)
        
        self.session_path = self.account_path / self.SESSION_FILE_NAME

    @property
    def exists(self):
        return self.session_path.is_file()

    def read(self) -> bytes:
        return self.session_path.read_bytes()

    def write(self, content: bytes) -> int:
        return self.session_path.write_bytes(content)

    def delete(self):
        return self.session_path.unlink()
    
    

     

    
    
        
        
