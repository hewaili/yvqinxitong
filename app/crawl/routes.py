from flask import render_template, request, jsonify
from flask_login import login_required
from app.crawl import bp
from app.spider.baidu import crawl_baidu_news

@bp.route('/api/search', methods=['POST'])
@login_required
def search_news():
    data = request.get_json()
    keyword = data.get('keyword')
    
    if not keyword:
        return jsonify({'code': 400, 'msg': '请输入关键词', 'data': []})
    
    try:
        results = crawl_baidu_news(keyword)
        return jsonify({
            'code': 0,
            'msg': 'success',
            'count': len(results),
            'data': results
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e), 'data': []})

@bp.route('/index')
@login_required
def index():
    return render_template('crawl/index.html')
