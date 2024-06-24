import pandas as pd
import pyodbc as p
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

datesys=datetime.now().strftime("%Y-%m-%d")
connStr = os.getenv("connStrW")
conn = p.connect(connStr)
mycursor = conn.cursor()
def checkColumnExist(TableName):
    mycursor.execute(f"""
                        SELECT Column_name
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME = N'{TableName}'
                     """)
    column= [i[0] for i in mycursor.fetchall()]
    return column
def CreateColumn(TableName,ColumnName):
    mycursor.execute(f"""
                        ALTER TABLE {TableName}
                        ADD {ColumnName} Varchar(MAX);
                     """)

def insertVessels(Vessels):
    VesselList=checkColumnExist("BlueT_API_Ships")
    for ship in Vessels:
        head=[i for i in ship]
        head.append("UpdatedDate")
        line=["'"+str(ship[i])+"'" for i in ship]
        date="'"+datesys+"'"
        print(line)
        line.append(date)
        for i in head:
            if i not in VesselList:
                CreateColumn("BlueT_API_Ships",i)
        Head=",".join(head)
        Line=",".join(line)
        #print(Head)
        #print(Line)
        mycursor.execute(f"""
                      INSERT INTO BlueT_API_Ships ({Head})
                      VALUES ({Line})
                     """)
    mycursor.close()
    conn.commit()
    conn.close()

def insertReport(header,lines,vessels):
    ReportList=checkColumnExist("BlueT_API_Report")
    header=header+",UpdatedDate"
    lines=lines+",'"+datesys+"'"
    Header=header.split(",")
    ReportList=[i.lower() for i in ReportList]
    for i in Header:
            if i.lower() not in ReportList:
                CreateColumn("BlueT_API_Report",i)
    mycursor.execute(f"""
                      INSERT INTO BlueT_API_Report (IMONum,{header})
                      VALUES ('{vessels}',{lines})
                     """)

    conn.commit()

def insertEngineReport(header, lines):
    ReportList=checkColumnExist("BlueT_API_ReportEngine")
    header=header+",UpdatedDate"
    Header=header.split(",")
    lines=lines+",'"+datesys+"'"
    ReportList=[i.lower() for i in ReportList]
    for i in Header:
            if i.lower() not in ReportList:
                CreateColumn("BlueT_API_ReportEngine",i)
    #print(header)
    #print(lines)
    mycursor.execute(f"""
            INSERT INTO BlueT_API_ReportEngine ({header})
            values ({lines})
            """
                         )
    conn.commit()


def insertEvent(Header,Line):
    Header=Header+",UpdatedDate"
    Line=Line+",'"+datesys+"'"
    mycursor.execute(
            f"""
            INSERT INTO BlueT_API_Events ({Header}) VALUES ({Line})
            """ )
    # mycursor.close()
    conn.commit()
    # conn.close()


def insertVoyage(Voyages,IMO):
    Count=0
    date=datesys
    for Voyage in Voyages:
    
        mycursor.execute("""
                      INSERT INTO BlueT_API_Voyages (id,name,imoNumber,UpdatedDate)
                      VALUES (?,?,?,?)
                     """,
                         Voyage["id"],Voyage["name"],IMO,date

                         )
        Count+=1
        
    # mycursor.close()
    conn.commit()
    return Count
def insertVoyageSummary(header,line):
    available=checkColumnExist("BlueT_API_VoyageSummary")
    header=header+",UpdatedDate"
    Header=header.split(",")
    line=line+",'"+datesys+"'"
    for i in Header:
            if i not in available:
                CreateColumn("BlueT_API_VoyageSummary",i)
    mycursor.execute(f"""
                      INSERT INTO BlueT_API_VoyageSummary ({header})
                      Values({line})
                     """
                         )

    # mycursor.close()
    conn.commit()
def get_Vessel():
    date=datesys
    mycursor.execute(f"""
                      select distinct imoNumber from BlueT_API_Ships
                      where UpdatedDate='{date}'
                     """
                         )
    tem=[i[0] for  i in mycursor.fetchall()]
    return (tem)
def get_VoyageID():
    date=datesys
    mycursor.execute(f"""
                          select distinct id from BlueT_API_Voyages
                          where UpdatedDate='{date}'
                         """
                     )
    tem = [i[0] for i in mycursor.fetchall()]
    return (tem)

def get_EventID():
    date=datesys
    mycursor.execute(f"""
                          select id from [dbo].[BlueT_API_Events] 
                            where eventType='Departure'
                            and UpdatedDate='{date}'
                         """
                     )
    tem = [i[0] for i in mycursor.fetchall()]
    return (tem)

def insertLegSummary(header,line):
    LegList=checkColumnExist("BlueT_API_LegSummary")
    LegList=[i.lower() for i in LegList]
    header=header+",UpdatedDate"
    Header=header.split(",")
    line=line+",'"+datesys+"'"
    for i in Header:
            if i.lower() not in LegList:
                #print(LegList)
                #print(i.lower())
                CreateColumn("BlueT_API_LegSummary",i)
    mycursor.execute(f"""
                      INSERT INTO BlueT_API_LegSummary ({header})
                      Values({line})
                     """
                         )

    # mycursor.close()
    conn.commit()
    # conn.close()
def TruncateFile(TableName):
    mycursor.execute(f"""
                          delete {TableName}
                         """
                     )
    
def GetDataList(TableName):
    mycursor.execute(f"""
                      select * from {TableName}
                     """
                         )
    data = mycursor.fetchall()
    head=[i[0] for i in mycursor.description]
    return [head,data]
def closeConnection():
    mycursor.close()
    conn.close()
def AddColumn(TableName, Column):
    mycursor.execute(f"""
                      ALTER TABLE {TableName}
                        ADD {Column} varchar(255)
                     """
                         )
    conn.commit()
