import os
import dotenv

dotenv.load_dotenv()

ConectorConfig = {
    'host' : os.getenv('host'),
    'port' : int(os.getenv('port')),
    'username' : os.getenv('username'),
    'password' : os.getenv('password'),
    'database' : os.getenv('database'),
    'ssl_ca' : os.getenv('ssl_ca')
}

PUBLIC_KEY = os.getenv('PUBLIC_KEY')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')