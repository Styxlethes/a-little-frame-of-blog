import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'caonima'

    # flask-sqlalchemy
    # 此处utf-8是无效的，只有utf8才有效
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:081791@localhost:3376/flask_blog?charset=utf8'
    # SQLALCHEMY_DATABASE_URI='sqlite///'+os.path.join(basedir,'flaskblog.db')
    SQLALCHEMY_TRACK_MODEFICATION = False
    SQLALCHEMY_ECHO = False

    BLOG_ADMIN = 'woshiyibaichi@126.com'

    # flask-mail
    MAIL_DEBUG = False
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '642698748@qq.com'
    MAIL_PASSWORD = 'khsdmeyhivmibbcg'
    MAIL_SENDER = '642698748@qq.com'

    DEBUG = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # 将错误通过电子邮件发送给管理员
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = True
            mail_handler = SMTPHandler(
                mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
                fromaddr=cls.MAIL_SENDER,
                toaddrs=[cls.BLOG_ADMIN],
                subject='服务器出错',
                credentials=credentials,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
