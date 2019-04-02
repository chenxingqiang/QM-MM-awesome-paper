# -*- coding: utf-8 -*-
# @Create Time    : 2019-04-02 16:20
# @Author  : Xingqiang Chen
# !/usr/bin/python
__author__ = 'Administrator'


if __name__ == "__main__":
    import os
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait

    root_dir = "/Users/xingqiangchen/PycharmProjects/QM-MM-awesome-paper/"

    chromedriver = os.path.join(root_dir,"chromedriver","chromedriver")
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.get('https://gfsoso.99lb.net')
    inputElement = driver.find_element_by_name("q")
    searchWord = "QM/MM"
    inputElement.send_keys(searchWord)
    inputElement.submit()

    currentURL = driver.current_url
    print(currentURL)

    urlList = []
    localDir = os.path.join(root_dir,'down_pdf')
    fileOut = os.path.join(localDir,searchWord.replace('/','-') + ".txt")

    import urllib, re, codecs, sys

    fileOp = codecs.open(fileOut, 'a', sys.getdefaultencoding())
    for i in range(0, 50):  # 需要抓取的页数
        print(i)
        pdf_url = driver.find_elements_by_css_selector("a")
        for k in pdf_url:
            try:
                z = k.get_attribute("href")
                if '.pdf' in z and z not in urlList:
                    urlList.append(z)
                    print(z)
            except:
                import time

                time.sleep(1)
                continue
        contents = driver.find_elements_by_css_selector('h3')
        for ct in contents:
            print(ct.text)
            fileOp.write('%s\n' %(ct.text)) # 把页面上所有的文章名称存到txt，有时会报错
        driver.get(currentURL + "&start=" + str(i * 10) + "&as_sdt=0,5&as_ylo=2008")

        import time

        time.sleep(3)

    for everyURL in urlList:  # 遍历列表的每一项，即每一个PDF的url
        wordItems = everyURL.split('/')  # 将url以/为界进行划分，为了提取该PDF文件名
        for item in wordItems:  # 遍历每个字符串
            if re.match('.*\.pdf$', item):  # 查找PDF的文件名
                PDFName = item  # 查找到PDF文件名
        localPDF = os.path.join(localDir, searchWord.replace('/','-') + "_" + PDFName)
        try:
            urllib.urlretrieve(everyURL, localPDF)  # 按照url进行下载，并以其文件名存储到本地目录
        except Exception as e:
            continue
