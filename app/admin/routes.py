from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import User, SystemSetting
from . import bp
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@bp.before_request
@login_required
def before_request():
    if not current_user.is_admin:
        # 如果不是管理员，且访问 admin 路由，则重定向或报错
        # 但这里为了安全，最好是在每个视图加 admin_required，或者在这里统一拦截
        pass

@bp.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@bp.route('/users')
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    if request.method == 'POST':
        app_name = request.form.get('app_name')
        # 保存设置
        setting = SystemSetting.query.filter_by(key='app_name').first()
        if not setting:
            setting = SystemSetting(key='app_name', value=app_name)
            db.session.add(setting)
        else:
            setting.value = app_name
        db.session.commit()
        flash('设置已更新', 'success')
        return redirect(url_for('admin.settings'))
    
    app_name = SystemSetting.get_value('app_name', '政企智能舆情分析报告生成智能体应用系统')
    return render_template('admin/settings.html', app_name=app_name)
