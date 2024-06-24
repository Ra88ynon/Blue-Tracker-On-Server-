import FromAPI as api
import ToSQL as sql
import logging
from datetime import date
from dotenv import load_dotenv, dotenv_values
import os

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    filename = os.getenv("logfile")+'RunGetEvent.log',
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
def getEvent(vessel):
    #file=open("BlueT_API_Events","w")
    count=0
    print("getting events")
    
    response=api.get_Events(vessel)
    print(str(response))
    if "Response" in str(response):
        logging.info(f"error={vessel}")
        return 0

    EventList = response["items"]

    print("flaternning data")

    
    for item in EventList:
        print(item["id"])
        # test=[flat(i) for i in item]
        [EventH, EventL]=flat(item)
        sql.insertEvent(",".join(EventH), ",".join(["'"+str(i)+"'"for i in EventL]))
        count+=1
    return count
    # for item in Event:
    #     value.append(list(Event[item]))
    # value=np.transpose(value)
    # sql.insertEvent(value)

#------------------get all Events

try:
    #sql.TruncateFile("BlueT_API_Events")
    logging.info(date.today())
    logging.info("Run api")
    Vessels=sql.get_Vessel()
    count=0
    for Vessel in Vessels:
        print(Vessel)
        count+=getEvent(str(Vessel))
    logging.info("End of getEvent")
except (Exception,TypeError,NameError)as Err:
    logging.exception(f"error on {Vessel}")
finally:
    print("done")
    logging.info(f"Number={count}")
    sql.closeConnection()
