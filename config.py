SECRET_KEY = 'secret_key'

CONFIG_DBMS = 'postgresql'
CONFIG_USER = 'postgres'
CONFIG_PASSWORD = 'postgres'
CONFIG_SERVER = 'localhost'
CONFIG_DATABASE = 'stardew'

# \ para quebrar linha
SQLALCHEMY_DATABASE_URI = \
  f'{CONFIG_DBMS}://{CONFIG_USER}:{CONFIG_PASSWORD}@{CONFIG_SERVER}/{CONFIG_DATABASE}'

# desativando aqui para melhora de desempenho
SQLALCHEMY_TRACK_MODIFICATIONS = False
