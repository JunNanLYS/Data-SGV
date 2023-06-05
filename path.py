import os

"""
CN
该文件里面用于存放一些文件的路径

EN
...
"""

root_path = os.path.abspath(__file__)  # 根目录
while (name := root_path.split("\\"))[-1] != "Data-SGV":
    root_path = os.path.dirname(root_path)
setting_json_path = root_path + "\setting.json"  # setting配置文件
qss_path = root_path + "\qss"  # qss文件
