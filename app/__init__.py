from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# 导入上级目录中的文件
import sys
sys.path.append('..')
# 导入配制信息
from config import Config
# from livereload import Server #livereload模块实现自动刷新
# from functools import reduce
app = Flask(__name__)
# 添加配制信息
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)
# 加入登录限制功能
login.login_view = 'login'
from app import route, models
# 绑定app与数据库，以便进行操作
migrate = Migrate(app, db)


# 自定义jinja2的过滤器
# @app.template_filter('md')
# def markdown_to_txt(txt):
# 	from markdown import markdown
# 	return markdown(txt)

# 自定义jinja2函数
# def read_md(filename):
# 	with open(filename) as md_file:
# 		content=reduce(lambda x,y:x+y,md_file.readlines())
# 	return content.encode('GBK').decode('utf-8')

# @app.context_processor
# def inject_methods():
# 	return dict(read_md=read_md)


# if __name__ == '__main__':
# 	# live_server=Server(app.wsgi_app)
# 	# live_server.watch('**/**')	#检测app.py目录下所有文件的变更
# 	# live_server.serve(open_url=True)
# 	app.run(debug=True)
