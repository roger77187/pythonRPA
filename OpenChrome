import subprocess
import os
import time

def open_chrome_with_account(profile_name):
    """
    使用指定Chrome用户配置文件启动Chrome并打开空白页
    
    :param profile_name: Chrome配置文件夹名称（如"Default"、"Profile 1"或自定义名称）
    """

    # Chrome常见安装路径
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]

    # 查找Chrome安装位置
    chrome_exe = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_exe = path
            break
    
    if not chrome_exe:
        raise FileNotFoundError("未找到Chrome安装路径，请确保已安装Chrome浏览器")
    
    # 构建启动命令
    subprocess.Popen([
        chrome_exe,
        f"--profile-directory={profile_name}",
        "about:blank"
    ])


def list_available_profiles():
    """列出所有可用的Chrome用户配置文件"""
    user_data_dir = os.path.join(os.path.expanduser('~'), 
                                'AppData', 'Local', 'Google', 'Chrome', 'User Data')
    
    if os.path.exists(user_data_dir):
        print("\n可用配置文件:")
        for item in os.listdir(user_data_dir):
            if item.startswith("Profile") or item == "Default":
                print(f"- {item}")
        print("\n提示: 配置文件通常对应不同的Google账户")
    else:
        print("未找到Chrome用户数据目录")

if __name__ == "__main__":
    # 显示可用账户
    list_available_profiles()
    
    # 设置要使用的账户配置文件
    target_profile = "Profile 22"  # 修改为您需要的配置文件名
    
    # 启动Chrome
    open_chrome_with_account(target_profile)
