import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
manager = Manager(app)
moment = Moment(app)
class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(64),unique=True,primary_key=True)

class NameForm(FlaskForm):
    name = StringField('你的名字呢0.0',validators=[Required()])
    submit = SubmitField('提交')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))
'''
from是上面继承wtf的表单，只有名字和提交按钮
一开始用户没有登录的情况下，渲染的模板中没有名字保存，所以字典get的返回值是None，session【‘know’】默认是flase，显示stranger
之后当我们提交表单了，首先会在数据库中查询是否有这个用户的名字，如果没有的话则会在数据库中新添加这个user名并提交保存
如果我们检查到有这个用户，就不需要重复提交保存到数据库了。之后把session中name建的值指向form.name.data。（这里是所填写表单中name的数据）
session是为了保存请求之间所需要的数据，因为http是一种无状态协议，所以在每次请求结束后都会清空数据。对我们来说是不方便的。
'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()