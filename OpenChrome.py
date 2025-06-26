import subprocess
import os
import time
import psutil

def kill_all_chrome():
    """关闭所有Chrome进程"""
    for proc in psutil.process_iter(['name']):
        if proc.name().lower() in ('chrome.exe', 'google chrome'):
            try:
                proc.kill()
                time.sleep(2)  # 等待进程完全退出
            except:
                pass

def is_port_in_use(port):
    """检查端口是否被占用"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_by_port(port):
    """终止占用指定端口的进程"""
    for proc in psutil.process_iter():
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    proc.kill()
                    time.sleep(2)
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def open_chrome_with_debug(profile_name="Default", debug_port=9222):
    """启动带调试模式的Chrome（确保使用已登录的配置文件）"""
    kill_all_chrome()  # 关键步骤！

    # 自动查找Chrome路径
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome"
    ]
    chrome_exe = next((p for p in chrome_paths if os.path.exists(p)), None)
    if not chrome_exe:
        raise FileNotFoundError("Chrome未安装或路径错误")

    # 用户数据目录（确保路径正确！）
    user_data_dir = os.path.join(os.path.expanduser('~'), 
                                'AppData', 'Local', 'Google', 'Chrome', 'User Data')
    print(f"使用的配置文件路径: {user_data_dir}\\{profile_name}")

    # 终止占用端口的进程
    if is_port_in_use(debug_port):
        kill_process_by_port(debug_port)

    # 启动命令（添加--no-sandbox和--disable-web-security仅限测试环境！）
    cmd = [
        chrome_exe,
        f"--remote-debugging-port={debug_port}",
        f"--user-data-dir={user_data_dir}",
        f"--profile-directory={profile_name}",
        "--no-first-run",
        "--no-default-browser-check",
        "--no-sandbox",              # 关闭沙盒（解决部分权限问题）
        "--disable-web-security",    # 禁用同源策略（测试用）
        "about:blank"
    ]

    try:
        process = subprocess.Popen(cmd)
        print(f"Chrome已启动 | 调试地址: http://localhost:{debug_port}")
        print(f"使用的配置文件: {profile_name}")
        return process
    except Exception as e:
        print(f"启动失败: {e}")
        return None

if __name__ == "__main__":
    # 手动指定已登录的配置文件（如"Default"或"Profile 1"）
    chrome_process = open_chrome_with_debug(profile_name="Profile 22")
    if chrome_process:
        input("按回车键退出...")
        chrome_process.terminate()
