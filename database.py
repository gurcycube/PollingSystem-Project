from databases import Database
from config import Config

config = Config()
database = Database(config.DATABASE_URL)
