import subprocess
import os
import time # 导入 time 模块

def open_chrome_debug(user_data_dir,profile_name, port=9222, start_url=None): # 添加 start_url 参数
    """
    用指定的Google账户目录以调试模式打开Chrome浏览器。

    Args:
        user_data_dir (str): Chrome用户数据目录的路径。
                              这是Chrome存储用户配置文件、缓存等的地方。
        port (int): 调试协议的端口（默认为9222）。
        start_url (str, optional): Chrome启动时要打开的初始URL。默认为None。
    """
    if not os.path.isdir(user_data_dir):
        print(f"错误：未找到用户数据目录：{user_data_dir}")
        print("请确保路径正确且目录存在。")
        return

    # 根据操作系统确定Chrome可执行文件路径
    if os.name == 'nt':  # Windows
        chrome_path = os.path.join(os.environ.get('PROGRAMFILES'), 'Google', 'Chrome', 'Application', 'chrome.exe')
        if not os.path.exists(chrome_path):
            chrome_path = os.path.join(os.environ.get('PROGRAMFILES(X86)'), 'Google', 'Chrome', 'Application', 'chrome.exe')
    elif os.uname().sysname == 'Darwin':  # macOS
        chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    else:  # Linux (常见路径)
        chrome_path = '/usr/bin/google-chrome'
        if not os.path.exists(chrome_path):
            chrome_path = '/usr/bin/google-chrome-stable'

    if not os.path.exists(chrome_path):
        print(f"错误：在您操作系统的常见路径中未找到Chrome可执行文件。尝试了：{chrome_path}")
        print("请指定正确的Chrome可执行文件路径。")
        return

    command = [
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        f"--profile-directory={profile_name}"
    ]

    if start_url:
        command.append(start_url) # 如果指定了URL，则添加到命令中

    print(f"正在使用命令打开Chrome：{' '.join(command)}")
    try:
        # 使用subprocess.Popen避免阻塞脚本
        subprocess.Popen(command)
        print(f"Chrome已在调试模式下打开，端口为 {port}，使用用户数据目录：{user_data_dir}")
        if start_url:
            print(f"并尝试打开URL：{start_url}")
        print("您现在可以连接到调试端口（例如，通过浏览器开发工具或客户端库）。")

        # 尝试添加一个短暂的延迟，让Chrome有时间完全加载配置文件和会话
        print("等待5秒，让Chrome完全加载配置文件和会话...")
        time.sleep(5) # 暂停5秒
        print("等待结束。请检查Chrome是否已登录。")

    except FileNotFoundError:
        print(f"错误：未找到Chrome可执行文件。请检查路径：{chrome_path}")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    # IMPORTANT: Replace this with the actual path to your desired Chrome user data directory.
    # To find your user data directory:
    # 1. Open Chrome.
    # 2. Type chrome://version in the address bar and press Enter.
    # 3. Look for the "Profile Path" entry. The user data directory is the parent folder of the "Default" profile.
    #    For example, if "Profile Path" is C:\Users\YourUser\AppData\Local\Google\Chrome\User Data\Default
    #    then your user_data_dir would be C:\Users\YourUser\AppData\Local\Google\Chrome\User Data
    
    # Example for Windows:
    # To avoid "SyntaxWarning: invalid escape sequence '\w'", use a raw string (prefix with 'r')
    # or double the backslashes (e.g., "C:\\Users\\YourUser\\AppData\\Local\\Google\\Chrome\\User Data").
    # The warning you saw for '\w' happens because '\w' is not a standard escape sequence in Python.
    chrome_user_data_path = r"D:\web3\Chrome" # Corrected example using a raw string
    chrome_profile_name = "Profile 9"

    # Example for macOS:
    # chrome_user_data_path = "/Users/YourUser/Library/Application Support/Google/Chrome"

    # Example for Linux:
    # chrome_user_data_path = "/home/youruser/.config/google-chrome"
    
    # You can specify a different port if 9222 is in use, e.g., 9223
    debug_port = 9222

    # 可以尝试指定一个Google服务的URL，例如：
    # start_url_to_open = "https://accounts.google.com"
    # start_url_to_open = "https://mail.google.com"
    # start_url_to_open = "https://www.google.com"
    start_url_to_open = None # 默认不打开特定URL，您可以取消注释上面一行来尝试

    open_chrome_debug(chrome_user_data_path,chrome_profile_name, debug_port, start_url_to_open)
