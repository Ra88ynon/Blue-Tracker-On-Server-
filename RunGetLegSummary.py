import FromAPI as api
import ToSQL as sql
import logging
from datetime import date
from dotenv import load_dotenv, dotenv_values
import os
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    filename = os.getenv("logfile")+'RunGetLegSummary.log',
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
count=0
try:
    #sql.TruncateFile("BlueT_API_LegSummary")
    logging.info(date.today())
    logging.info("Run api")
    Departure=sql.get_EventID()
    
    print(f"insert {len(Departure)} data")
    print("Get From API")

    LegSummary=[api.Get_LegSummary(i) for i in Departure]

    print("Insert into SQL")

    for i in LegSummary:
        print(i["legEventId"])
        if "Response" in str(i):
            print("error")
            continue
        [Head,Line]=flat(i)
        NewHeader = []
        NewLine = []
        for h,l in zip(Head,Line):
            if h.lower() in NewHeader:
                continue
            else:
                NewHeader.append(h.lower())
                NewLine.append(l)
        

        sql.insertLegSummary(",".join(NewHeader),",".join(["'"+str(i)+"'" for i in NewLine]))
        count+=1
    logging.info("End of LegSummary")
except (Exception,TypeError,NameError)as Err:
    logging.exception("Error")
finally:
    sql.closeConnection()
    logging.info(f"Number:{count}")
    print("done")
