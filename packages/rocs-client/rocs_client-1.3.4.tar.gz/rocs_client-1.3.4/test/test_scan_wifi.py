import subprocess
import re
import time

# 开始扫描二维码
proc = subprocess.Popen(["zbarcam", "/dev/video0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
                        universal_newlines=True)


# 定义连接WiFi的函数
def connect_to_wifi(ssid, password):
    subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "password", password])


# 循环监测zbarcam输出
while True:
    output = proc.stdout.readline().rstrip()
    if output:
        # 通过正则表达式匹配WiFi信息
        match = re.match(r"WIFI:S:([^;]+);T:([^;]+);P:([^;]+);", output.decode('utf-8'))
        if match:
            ssid = match.group(1)  # 获取SSID
            password = match.group(3)  # 获取密码
            print(f"Detected WiFi QR Code. SSID: {ssid}, Password: {password}")
            # 连接WiFi
            connect_to_wifi(ssid, password)
            break  # 连接成功后退出循环

    time.sleep(1)

# 结束zbarcam进程
proc.terminate()
