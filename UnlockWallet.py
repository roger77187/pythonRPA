from pywinauto import Desktop, Application
import time

PLUGIN_URL = f"chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html"
PASSWORD = "520zzh@hzh"


def unlockWallet(plugin_url):
    time.sleep(1) 
    # 找到第一个Chrome窗口（假设只有一个）
    chrome_windows = [w for w in Desktop(backend="uia").windows() if "Chrome" in w.window_text()]
    if not chrome_windows:
        print("未找到打开的Chrome窗口")
        exit()

    chrome_win = chrome_windows[0]
    chrome_win.set_focus()
    time.sleep(1)

    # 发送 Ctrl+T 新建标签页
    from pywinauto.keyboard import send_keys
    send_keys('^t')
    time.sleep(1)

    # 输入插件URL，发送回车
    send_keys(plugin_url)
    time.sleep(0.5)
    send_keys('{ENTER}')
    time.sleep(3)  # 等待页面加载

    # 连接到Chrome窗口
    app = Application(backend="uia").connect(handle=chrome_win.handle)
    dlg = app.window(handle=chrome_win.handle)
    dlg.set_focus()
    time.sleep(1)

    try:
        # 定位密码输入框，ID是password
        password_box = dlg.child_window(auto_id="password", control_type="Edit")
        password_box.click_input()
        password_box.type_keys(PASSWORD, with_spaces=True)
        time.sleep(0.5)

        # 查找 Unlock 按钮，点击
        buttons = dlg.descendants(control_type="Button")
        unlock_button = None
        for b in buttons:
            if "unlock" in b.window_text().lower():
                unlock_button = b
                break

        if unlock_button:
            unlock_button.click_input()
            print("MetaMask 已解锁")
        else:
            print("未找到 Unlock 按钮")

    except Exception as e:
        print(f"自动解锁失败: {e}")

if __name__ == "__main__":
    unlockWallet(PLUGIN_URL)        
