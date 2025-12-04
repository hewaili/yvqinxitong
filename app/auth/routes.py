from flask import render_template, redirect, url_for, flash, request, session, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import User
from app.auth import bp
from captcha.image import ImageCaptcha
import io
import random
import string

@bp.route('/captcha')
def get_captcha():
    image = ImageCaptcha(width=120, height=38, font_sizes=(24, 28, 32))
    # 生成随机字符
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    session['captcha'] = captcha_text.lower()
    
    data = image.generate(captcha_text)
    return send_file(data, mimetype='image/png')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        captcha = request.form.get('captcha')
        
        # 验证码校验
        if not captcha or captcha.lower() != session.get('captcha'):
            flash('验证码错误', 'danger')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            
            # 登录成功后，如果是管理员跳转到后台，普通用户跳转到首页
            if user.is_admin:
                return redirect(url_for('admin.index'))
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功退出', 'info')
    return redirect(url_for('auth.login'))
