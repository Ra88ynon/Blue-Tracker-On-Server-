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
    filename = os.getenv("logfile")+'RunGetReport.log',
    datefmt='%Y-%m-%d %H:%M:%S')
today=date.today()

def flat(json_data, parent_key=''):
    flattened = {}
    for key, value in json_data.items():
        new_key = f"{parent_key}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(flat(value, new_key))
        else:
            flattened[new_key] = value
    return flattened



    return[column,line]
def reportsummaries(Vessel):
    report1 = api.get_Report(Vessel)["items"]
    EngineReportCount=0
    ReportCount=0
    for item in report1:
        id=item["id"]
        print(id)
        Data = flat(item)
        Head=Data.keys()
        Line=Data.values()
        MainReport = []
        Mainheader = []
        
        for i, j in zip(Head,Line):
            # id=item["id"]

            if "ship" in i:
                continue
            elif "aggregationDetails" in i:
                
                for item in j:
                    
                    EngHeader=[]
                    EngLine=[]
                    EngHeader.append("Engine")
                    EngHeader.append("IMONumber")
                    EngHeader.append("id")
                    EngLine.append(i.replace("aggregationDetails",""))
                    EngLine.append(Vessel)
                    EngLine.append(id)
                    for element in item:
                        if type(item[element])==list:
                            EngHeader.append(element)
                            EngLine.append(",".join([str(j).replace("'","''") for j in item[element]]))
                        elif type(item[element])==dict:
                            for head,line in zip(item[element].keys(),item[element].values()):
                                EngHeader.append(element+head)
                                EngLine.append(str(line).replace("'","''"))
                        else:
                            EngHeader.append(element)
                            EngLine.append(str(item[element]).replace("'","''"))
                    # print(EngHeader,len(EngHeader))
                    # print(EngLine,len(EngLine))
                    sql.insertEngineReport(",".join(EngHeader), ",".join(["'"+str(i)+"'" for i in EngLine]))
                    EngineReportCount+=1
                # continue
            else:
                Mainheader.append(i)
                MainReport.append(j)
        sql.insertReport(",".join(Mainheader), ",".join(["'"+str(i)+"'" for i in MainReport]), Vessel)
        ReportCount+=1
    return [ReportCount,EngineReportCount]
TotalRC=0
TotalERC=0
try:
    #sql.TruncateFile("BlueT_API_Report")
    #sql.TruncateFile("BlueT_API_ReportEngine")
    logging.info(date.today())
    logging.info("Run api")
    
    Vessels=api.get_Vessels()["items"]
    for Vessel in Vessels:
        print("Vessel:",Vessel["imoNumber"])
        [RC,ERC]=reportsummaries(str(Vessel["imoNumber"]))
        TotalRC+=RC
        TotalERC+=ERC
    logging.info("End of reportsummaries")
    
finally:
    print("complete")
    logging.info(f"ReportCount :{TotalRC}")
    logging.info(f"EngReportCount : {TotalERC}")
    sql.closeConnection()

        
