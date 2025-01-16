from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongoarrow.api import write
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Get list of database names
for db_name in client.list_database_names():
    print(db_name)

train = pd.read_csv('./database/TRAIN.csv')
test = pd.read_csv('./database/TEST.csv')

# write data to MongoDB
write(client.sales_forecasting.train, train)
write(client.sales_forecasting.test, test)

# Always close the client after completing the operation
client.close()