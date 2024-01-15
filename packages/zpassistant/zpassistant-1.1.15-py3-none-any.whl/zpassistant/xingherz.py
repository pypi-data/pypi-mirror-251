# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
from zpassistant import SsoLoginUtil
import argparse
import json
from selenium.webdriver.common.by import By

class Xingherz():
    def __init__(self) -> None:
        self.loginUtil = SsoLoginUtil("https://zpsso.zhaopin.com/login",keep_browser_alive=True,force_browser = True)
        self.session = self.loginUtil.login("https://xinghe.zhaopin.com/user/info")

    def checkSsoLogin(self,browser):
        if browser.title == '我的信息':
            print("login success ,closing browser")
            return True
        return False
    
    def listUploadFiles(self,page = 1,size = 20):
        # 查询已上传的文件列表
        browser = self.loginUtil.get_installed_browser()
        browser.get("https://xinghe.zhaopin.com/user/folder")
        titles = None
        while True:
            try:
                titles = browser.find_elements(by=By.XPATH,value="/html/body/div[2]/div[2]/table/thead/tr/th")
                break
            except Exception as e:
                time.sleep(0.1)
                pass
        for index in range(1,len(titles)):
            title = titles[index]
            print(str(title.text) + "\t\t\t",end="")
        print("\n------------------------------------------------------------")
        trs = browser.find_elements(by=By.XPATH,value="/html/body/div[2]/div[2]/table/tbody/tr")
        # 需要跳过第一个tr
        for tri in range(1,len(trs)):
            tr = trs[tri]
            tds = tr.find_elements(by=By.TAG_NAME,value="td")
            for tdi in range(1):
                td = tds[tdi]
                print(str(td.text) + "\t\t\t",end="")
            print("\n")
        pass

    def uploadFile(self,filePath):
        url = 'https://xinghe.zhaopin.com/user/upload/file'
        data = {
            'pid': '0',
            'secret_type': '',
            'secret_size': '0',
            'secret_code': '0',
            'remark': '',
        }
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Origin': 'https://xinghe.zhaopin.com',
            'Referer': 'https://xinghe.zhaopin.com/user/folder',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.17',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        # 读取文件名
        fileName = os.path.basename(filePath)
        files = {'file': (fileName, open(filePath, 'rb'))}
        response = self.session.post(url, headers=headers, data=data, files=files)
        if response.status_code == 200:
            try:
                result = json.loads(response.text)
                if str(result["code"]) == "200":
                    # 打印绿色
                    print("\033[32m upload file success,fileId: "+ str(result["data"]["id"]) + " ,fileName: " + str(result["data"]["filename"]))
                else:
                    # 打印红色
                    print("\033[31m upload file failed : " + response.text)
            except Exception as e:
                print("\033[31m upload file failed " + response.text + ",exception: "+ str(e))

    def downloadFile(self,fileName):
        link = f"https://xinghe.zhaopin.com/user/folder/{fileName}?action=download"
        # browser设置文件默认下载路径
        browser = self.loginUtil.get_installed_browser()
        
        browser.get(link)

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='''
example
    xingherz --delete \$(xingherz -ls) # delete 20 uploaded files
    xingherz tmp.json  # upload file
    xingherz -d "16af6563-a022-4c4f-89a4-88efd3ce7adb" -n fileName # download file by id
                                       
    ''', add_help=True, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--file', type=str, help="upload file path")
    parser.add_argument('-d', '--download', type=str, help="download file name")
    parser.add_argument('-n', '--name', type=str, help="download file name")
    parser.add_argument('-l', '--list', nargs='*', type=int, help="list uploaded files")
    args = parser.parse_args(["-d","issues.ics"])
    if args.list is not None:
        # 如果参数长度<2则忽略
        if len(args.list) < 2:
            args.list = [1, 20]
        Xingherz().listUploadFiles(args.list[0], args.list[1])
    
    if args.file is not None:
        Xingherz().uploadFile(args.file)
    
    if args.download is not None:
        Xingherz().downloadFile(args.download)
    
    
    
