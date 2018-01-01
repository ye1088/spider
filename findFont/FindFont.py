#!usr/bin/python
# ! _*_coding:utf-8_*_


def findLittleSizeFont():
    '''
    查找字体大小小于某个数值的字体
    :return:
    '''
    import requests,time
    from lxml import etree
    maxPage = 50
    page = 0
    firstHalfUrl = "http://www.zhaozi.cn/e/action/fontList.php?page="
    secondHalfUrl = "&classid=35&ph=1&andor=and&softsq=%E5%85%B1%E4%BA%AB%E5%AD%97%E4%BD%93&orderby=&myorder=0&totalnum=2670"
    while page < maxPage:
        print("正在爬取第%d页" % (page+1))
        url = firstHalfUrl + str(page) + secondHalfUrl
        response = requests.get(url,timeout=20)
        xparse = etree.HTML(response.text)
        font_url = xparse.xpath('//div[@class="fontlist"]/ul[@class="img"]/li[1]/a/@href')
        font_name = xparse.xpath('//div[@class="fontlist"]/ul[@class="img"]/li/a/text()')
        font_size = xparse.xpath('//div[@class="fontlist"]/ul[@class="img"]/li/text()')
        # print(font_url)
        # print(font_size)
        # print(font_name)
        font_url_index = 0
        while font_url_index < len(font_url):
            font_size_txt = font_size[font_url_index*2]
            fontSizeNum = str(font_size_txt.split(" / 人气:")[0].split("/ 大小:")[-1].split("MB")[0]).strip()
            font_url_txt = font_url[font_url_index]
            try:
                if float(fontSizeNum) < 1.1:
                    print("\nfont name : "+font_name[font_url_index*4]+"\nfont url : "+font_url_txt+"\nfont size : "+ font_size_txt)
            except:
                print("\nfont name : " + font_name[
                    font_url_index * 4] + "\nfont url : " + font_url_txt + "\nfont size : " + font_size_txt)

            font_url_index+=1
        page += 1
        time.sleep(1)


if __name__=='__main__':
    findLittleSizeFont()
    pass