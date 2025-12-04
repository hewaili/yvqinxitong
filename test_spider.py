import requests
import json

def test_crawl():
    # 1. 登录获取 session
    session = requests.Session()
    login_url = "http://127.0.0.1:5000/auth/login"
    
    # 先获取登录页面的 CSRF token (虽然我们还没加 CSRF 保护，但这是好习惯)
    # 主要是为了建立 session
    response = session.get(login_url)
    
    # 模拟登录 - 这里假设你知道一个有效的用户名密码
    # 注意：因为有验证码，直接自动化登录比较困难。
    # 所以我们这里使用一种 trick：
    # 我们在 app/auth/routes.py 中暂时禁用了验证码校验或者直接在这里通过后门方式登录？
    # 不，更简单的方法是，我们直接调用爬虫函数测试，绕过 web 层
    pass

def test_spider_direct():
    from app.spider.baidu import crawl_baidu_news
    print("正在测试爬取关键词: 宜宾")
    try:
        results = crawl_baidu_news("宜宾")
        print(f"成功抓取 {len(results)} 条数据:")
        for item in results:
            print("-" * 50)
            print(f"标题: {item['title']}")
            print(f"来源: {item['source']}")
            print(f"链接: {item['url']}")
            print(f"封面: {item['cover']}")
            print(f"摘要: {item['summary'][:50]}...")
    except Exception as e:
        print(f"爬取失败: {e}")

if __name__ == "__main__":
    test_spider_direct()
