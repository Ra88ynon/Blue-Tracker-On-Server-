import FromAPI as api
import ToSQL as sql
import logging
from datetime import date
from dotenv import load_dotenv, dotenv_values
import os
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    filename = os.getenv("logfile")+'RunGetVoyage.log',
    datefmt='%Y-%m-%d %H:%M:%S')

today=date.today()

def getVoyage(vessel):
    Event=api.get_Voyage(vessel)["items"]
    return sql.insertVoyage(Event,vessel)
count=0
Vessels=api.get_Vessels()["items"]
try:
    #sql.TruncateFile("BlueT_API_Voyages")
    logging.info(date.today())
    logging.info("Run api")
    
    for Vessel in Vessels:
        print(f"""working on {Vessel["imoNumber"]}""")
        count+=getVoyage(str(Vessel["imoNumber"]))
    logging.info("End of get_Voyage")
except (Exception,TypeError,NameError)as Err:
    logging.exception(f"error Vessel['imoNumber']")
finally:
    print("complete")
    logging.info(f"Count Voyage: {count}")
    sql.closeConnection()
