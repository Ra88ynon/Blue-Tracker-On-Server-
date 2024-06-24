import FromAPI as api
import ToSQL as sql
import pandas as pd
import numpy as np
import logging
from datetime import date
from dotenv import load_dotenv, dotenv_values
import os

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    filename = os.getenv("logfile")+'RunGetVessels.log',
    datefmt='%Y-%m-%d %H:%M:%S')
today=date.today()

try:
    #sql.TruncateFile("BlueT_API_Ships")
    logging.info(date.today())
    logging.info("Run api")
    Vessels=api.get_Vessels()["items"]
    sql.insertVessels(Vessels)
    print(len(Vessels))
    logging.info("End of Vessels")

finally:
    print("Program ended")
    logging.info(f"Num of Vessels{len(Vessels)}")
    
