import os


class DevelopmentConfig:
    # Flask
    DEBUG = True
    SECRET_KEY = os.urandom(24)

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8mb4'.format(**{
        'user': os.getenv('DB_USER', 'admin'),
        'password': os.getenv('DB_PASSWORD', 'simpway1'),
        'host': os.getenv('DB_HOST', 'simpway-test.crhuck6lqdki.ap-northeast-1.rds.amazonaws.com'),
        'port': os.getenv('DB_PORT', '3306'),
        'dbname': os.getenv('DB_NAME', 'simpway'),
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


Config = DevelopmentConfig
