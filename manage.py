from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# from app.auth.models import User
# from app.main.models import Post

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)


# def make_shell_context():
# return dict(app=app, db=db, User=User, Post=Post)


# manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    '''部署命令'''
    from flask_migrate import upgrade
    from app.models import Role, User

    # 将数据库迁移到最新的版本
    upgrade()

    # 创建用户角色
    Role.insert_roles()

    # 让所有的用户都关注次用户
    # User.add_self_follows()


if __name__ == '__main__':
    manager.run()
