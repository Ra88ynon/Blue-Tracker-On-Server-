import FromAPI as api
import ToSQL as sql
import logging
from datetime import date
from dotenv import load_dotenv, dotenv_values
import os
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    filename = os.getenv("logfile")+'RunGetVoyageSummary.log',
    datefmt='%Y-%m-%d %H:%M:%S')
today=date.today()

def flat(data,header=""):
    column=[]
    line=[]
    for i in data:
        if type(data[i])==dict:
            [col,li]=flat(data[i],i)
            for j, i in zip(col,li):
                column.append(j)
                line.append(i)
        else:
            tem=header+i
            column.append(tem)
            line.append(data[i])


    return[column,line]
try:
    count=0
    #sql.TruncateFile("BlueT_API_VoyageSummary")

    logging.info(date.today())
    logging.info("Run api")
    print("get Voyage Id")
    voyage=sql.get_VoyageID()
    print("get all Voyage Summary")
    voyageSummary= [api.Get_VoyageSummary(i)for i in voyage]
    
    for item in voyageSummary:
        if "Response" in str(item):
            logging.info(f"{item}")
            continue
        print(item["id"])
        [header, line] = flat(item)
        header=",".join(header)
        line=",".join(["'"+str(i)+"'" for i in line])
        count+=1
        sql.insertVoyageSummary(header, line)
    logging.info("End of voyageSummary")
except (Exception,TypeError,NameError)as Err:
    logging.exception("error")
finally:
    logging.info(f"Number{count}")
    sql.closeConnection()
    print("done")
