import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv(override=True)


DATA_DIR = Path(os.environ.get(
    'DOCKETANALYZER_DATA_DIR',
    Path.home().resolve() / 'data' / 'docketanalyzer',
))

COURTLISTENER_TOKEN = os.environ.get('COURTLISTENER_TOKEN')

ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
ELASTIC_PORT = os.environ.get('ELASTIC_PORT')
ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD')
ELASTIC_USERNAME = os.environ.get('ELASTIC_USERNAME')
