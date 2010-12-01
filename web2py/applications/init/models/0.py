from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Amazing Quiz'
settings.subtitle = 'powered by web2py'
settings.author = 'Zhe'
settings.author_email = 'linuxcity.jn@gmail.com'
settings.keywords = 'facebook quiz fun'
settings.description = ''
settings.layout_theme = 'GreenandPlain'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = 'b75e3312-2f47-4d37-8645-f245e973adb5'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = 'linuxcity.jn@gmail.com'
settings.login_method = 'local'
settings.login_config = ''
