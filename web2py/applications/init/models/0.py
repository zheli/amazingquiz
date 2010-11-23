from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Installer Test'
settings.subtitle = 'powered by web2py'
settings.author = 'Zhe'
settings.author_email = 'zhe.li@lavasoft.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'ConcreteV2'
settings.database_uri = 'postgres://web2py:web2py@10.0.1.34/installation'
settings.security_key = '59a693d5-3890-4874-bac8-3cd24d397819'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
