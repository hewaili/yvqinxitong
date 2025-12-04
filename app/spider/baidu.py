import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def crawl_baidu_news(keyword):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    encoded_keyword = quote(keyword)
    url = f"https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word={encoded_keyword}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # 百度新闻通常包含在 class 为 result-op c-container xpath-log new-pmd 的 div 中
        # 但具体 class 可能会变，这里尝试使用比较宽泛的选择器
        news_items = soup.select('.result-op.c-container')
        
        if not news_items:
             # 尝试更宽泛的选择器，适应不同的页面结构
            news_items = soup.select('div[class*="result-op"]')

        for item in news_items:
            news_data = {
                "title": "",
                "summary": "",
                "cover": "",
                "url": "",
                "source": ""
            }
            
            # 标题和链接
            # 尝试多种选择器
            title_element = item.select_one('.news-title_1YtI1 a')
            if not title_element:
                title_element = item.select_one('h3 a')
            if not title_element:
                 title_element = item.select_one('a[aria-label*="标题"]')

            if title_element:
                news_data['title'] = title_element.get_text(strip=True)
                news_data['url'] = title_element.get('href')
            
            # 来源
            source_element = item.select_one('.c-color-gray.c-font-normal')
            if not source_element:
                source_element = item.select_one('.news-source')
            if not source_element:
                source_element = item.select_one('.source-text_383Fj') # 新样式
                
            if source_element:
                news_data['source'] = source_element.get_text(strip=True)
            else:
                 # 尝试从文本中提取，或者查找aria-label
                 pass

            # 概要
            summary_element = item.select_one('.c-font-normal.c-color-text')
            if not summary_element:
                 summary_element = item.select_one('.news-content_10jX_') # 新样式
            
            if summary_element:
                news_data['summary'] = summary_element.get_text(strip=True)
                
            # 封面图片
            img_element = item.select_one('.c-img')
            if not img_element:
                 img_element = item.select_one('.news-img_3Nn5Q') # 新样式

            if img_element:
                news_data['cover'] = img_element.get('src')
            
            if news_data['title'] and news_data['url']:
                results.append(news_data)
                
        return results

    except Exception as e:
        print(f"Error crawling baidu news: {e}")
        return []

if __name__ == "__main__":
    # 测试代码
    keyword = "西昌"
    news_list = crawl_baidu_news(keyword)
    for news in news_list:
        print(news)
