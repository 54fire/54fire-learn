import requests
from lxml import etree
from parse import parse_url
from tqdm import tqdm
import re

'''
@Author: 54fire
@Time: 2018-12-06 14:31
@Function: input 'title' and 'url', and output file.
'''
def Download_video(title,url):
    responses = requests.get(url, stream=True)
    with open(title + ".mp4","wb") as f:
        dl = 0
        total_size = int(responses.headers.get('content-length', 0))
        block_size = 1024
        for data in tqdm(responses.iter_content(block_size), total=(total_size/block_size), unit='KB', unit_scale=True):
            dl += len(data)
            if data:
                f.write(data)
        f.close()
        print("下载完成！")

class PronSpider:

    def __init__(self):
        self.main_url = "https://www.pornhub.com"
        self.url = "https://www.pornhub.com/video/search?search=" + input("input: ")

    def run(self):

        # 1. 设置url and headers
        main_url = self.main_url
        url = self.url
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"}

        # 2. 获取url的response
        r = parse_url(url)

        # 3. 提取页面的所有url
        html = etree.HTML(r.content.decode())
        elements = html.xpath('//div[@class="img fade fadeUp videoPreviewBg"]')

        # 提取网页的url，并且保存到datas中。
        datas = []
        for element in elements:
            video = {}      # 创建vedio字典，用于储存video的title和url。
            video["title"] = element.xpath('./a/@title')[0]
            video["url"] = main_url + element.xpath('./a/@href')[0]
            datas.append(video)

        # 3. 提取video数据
        for data in datas:
            responses = requests.get(data["url"],headers=headers)
            title = etree.HTML(responses.content.decode()).xpath("//h1[@class='title']/span/text()")[0]
            video_ul = re.findall('videoUrl":"(.*?)"',responses.content.decode())
            for i in video_ul:
                if i == '':
                    pass
                else:
                    video_url = i.replace("\/","/")
                    break
            print(title)

        # 4. 下载数据
            Download_video(title,video_url)


if __name__ == '__main__':
    spider = PronSpider()
    spider.run()
