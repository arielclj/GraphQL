from flask import Flask
from pathlib import Path
import pandas
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy.orm import mapper, sessionmaker
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import os
from flask_graphql import GraphQLView
import sqlite3


conn = sqlite3.connect('demo.db')
c = conn.cursor()

# Verify DB creation and CSV insertion
# sqlite_select_query = """SELECT * from Labels"""
# c.execute(sqlite_select_query)
# result = c.fetchone()
# print(result)
# c.close()

# Create DB table - Entries
# c.execute('''CREATE TABLE Entries(
#    [CH1_EFFICIENCY]                 VARCHAR(10) 
#   ,[CH1_HLI_CHW_Control_SetPoint]   VARCHAR(5)
#   ,[CH1_KWH]                        VARCHAR(13)
#   ,[CH1_MCCB_TRIP]                  VARCHAR(12) 
#   ,[CH1_CHWP_VSD_CMD]               VARCHAR(7)
#   ,[Timestamp]                      VARCHAR(23) PRIMARY KEY
#   ,[CH1_CWRT]                       VARCHAR(6)
#   ,[CH1_SYS_ALARM]                  VARCHAR(26) 
#   ,[CH1_HLI_Leaving_CHW_Temp]       VARCHAR(6)
#   ,[CH1_HLI_Entering_CW_Temp]       VARCHAR(6)
#   ,[CH1_CHWP_DP_1]                  VARCHAR(8)
#   ,[CH1_HLI_Entering_CHW_Temp]      VARCHAR(6)
#   ,[CH1_CWST]                       VARCHAR(6)
#   ,[CH1_KW]                         VARCHAR(7)
#   ,[CH1_LOAD]                       VARCHAR(10)
#   ,[CH1_HLI_Percent_Line_Current]   VARCHAR(6)
#   ,[CH1_Run_Status_0_Ready_4On]     VARCHAR(6)
#   ,[CH1_HLI_Leaving_CW_Temp]        VARCHAR(6)
#   ,[CH1_HLI_Motor_RPM]              VARCHAR(9)
#   ,[CH1_CHWP_DP_Setpoint]           VARCHAR(8)
#   ,[CH1_TRIP]                       VARCHAR(26) 
#   ,[CH1_HLI_Line_KW]                VARCHAR(7)
#   ,[CH1_Active_Demand_Limit_]        VARCHAR(5)
#   ,[CH1_FLOWRATE]                   VARCHAR(6)
#   ,[CH2_FLOWRATE]                   VARCHAR(7)
#   ,[CH2_CHWP_VSD_CMD]               VARCHAR(7)
#   ,[CH2_CWRT]                       VARCHAR(6)
#   ,[CH2_Run_Status_0_Ready_4On]     VARCHAR(6)
#   ,[CH2_Active_Demand_Limit_]        VARCHAR(5)
#   ,[CH2_KWH]                        VARCHAR(12)
#   ,[CH2_HLI_Leaving_CHW_Temp]       VARCHAR(6)
#   ,[CH2_HLI_Motor_RPM]              VARCHAR(9)
#   ,[CH2_SYS_ALARM]                  VARCHAR(26) 
#   ,[CH2_HLI_CHW_Control_SetPoint]   VARCHAR(5)
#   ,[CH2_TRIP]                       VARCHAR(24) 
#   ,[CH2_LOAD]                       VARCHAR(11)
#   ,[CH2_CWST]                       VARCHAR(6)
#   ,[CH2_MCCB_TRIP]                  VARCHAR(12) 
#   ,[CH2_KW]                         VARCHAR(7)
#   ,[CH2_HLI_Entering_CHW_Temp]      VARCHAR(6)
#   ,[CH2_EFFICIENCY]                 VARCHAR(9)
#   ,[CH2_HLI_Percent_Line_Current]   VARCHAR(6)
#   ,[CH2_HLI_Entering_CW_Temp]       VARCHAR(6)
#   ,[CH2_HLI_Leaving_CW_Temp]        VARCHAR(6)
#   ,[CH2_CHWP_DP_Setpoint]           VARCHAR(6)
#   ,[CH2_HLI_Line_KW]                VARCHAR(7)
#   ,[CH2_CHWP_DP_1]                  VARCHAR(8)
#   ,[CH4_Run_Status_0_Ready_4On]     VARCHAR(6)
#   ,[CH4_CHWP_DP_1]                  VARCHAR(8)
#   ,[CH4_HLI_Motor_RPM]              VARCHAR(6)
#   ,[CH4_FLOWRATE]                   VARCHAR(7)
#   ,[CH4_HLI_CHW_Control_SetPoint]   VARCHAR(5)
#   ,[CH4_EFFICIENCY]                 VARCHAR(9)
#   ,[CH4_CWRT]                       VARCHAR(6)
#   ,[CH4_KWH]                        VARCHAR(12)
#   ,[CH4_MCCB_TRIP]                  VARCHAR(12) 
#   ,[CH4_HLI_Entering_CHW_Temp]      VARCHAR(6)
#   ,[CH4_HLI_Entering_CW_Temp]       VARCHAR(6)
#   ,[CH4_SYS_ALARM]                  VARCHAR(26)
#   ,[CH4_LOAD]                       VARCHAR(10)
#   ,[CH4_HLI_Line_KW]                VARCHAR(5)
#   ,[CH4_HLI_Leaving_CW_Temp]        VARCHAR(6)
#   ,[CH4_Active_Demand_Limit_]        VARCHAR(5)
#   ,[CH4_TRIP]                       VARCHAR(40) 
#   ,[CH4_HLI_Percent_Line_Current]   VARCHAR(5)
#   ,[CH4_CHWP_VSD_CMD]               VARCHAR(5)
#   ,[CH4_CWST]                       VARCHAR(6)
#   ,[CH4_CHWP_DP_Setpoint]           VARCHAR(6)
#   ,[CH4_HLI_Leaving_CHW_Temp]       VARCHAR(6)
#   ,[CH4_KW]                         VARCHAR(5)
#   ,[CH3_HLI_Entering_CW_Temp]       VARCHAR(5)
#   ,[CH3_CWRT]                       VARCHAR(6)
#   ,[CH3_TRIP]                       VARCHAR(12) 
#   ,[CH3_KWH]                        VARCHAR(12)
#   ,[CH3_Run_Status_0_Ready_4On]     VARCHAR(6)
#   ,[CH3_LOAD]                       VARCHAR(11)
#   ,[CH3_CHWP_DP_Setpoint]           VARCHAR(10)
#   ,[CH3_HLI_Line_KW]                VARCHAR(5)
#   ,[CH3_EFFICIENCY]                 VARCHAR(9)
#   ,[CH3_KW]                         VARCHAR(7)
#   ,[CH3_HLI_Leaving_CHW_Temp]       VARCHAR(5)
#   ,[CH3_FLOWRATE]                   VARCHAR(7)
#   ,[CH3_CWST]                       VARCHAR(6)
#   ,[CH3_HLI_Leaving_CW_Temp]        VARCHAR(5)
#   ,[CH3_Active_Demand_Limit_]        VARCHAR(5)
#   ,[CH3_HLI_CHW_Control_SetPoint]   VARCHAR(5)
#   ,[CH3_CHWP_VSD_CMD]               VARCHAR(7)
#   ,[CH3_HLI_Motor_RPM]              VARCHAR(6)
#   ,[CH3_HLI_Entering_CHW_Temp]      VARCHAR(5)
#   ,[CH3_CHWP_DP_1]                  VARCHAR(8)
#   ,[CH3_MCCB_TRIP]                  VARCHAR(12) 
#   ,[CH3_SYS_ALARM]                  VARCHAR(26) 
#   ,[CH3_HLI_Percent_Line_Current]   VARCHAR(5)
# )''')
                 
# conn.commit()

# Uploading CSV to db
# engine = create_engine('sqlite:///C:/Users/ariel/flask-graphql-project/demo.db', echo=False)
# read_entries = pandas.read_csv(r'C:/Users/ariel/Desktop/dashboard_demo/dashboard_demo/app/backend/model/data/CL_data_190116.csv')
# read_entries.columns = read_entries.columns.str.replace(' ', '_')
# read_entries.columns = read_entries.columns.str.replace('[^_A-Za-z0-9]+', '')
# read_entries = read_entries.drop_duplicates(subset="Timestamp")
# read_entries.to_sql('ENTRIES', con = engine, if_exists='append', index = False)

# Likewise for Labels Table
# c.execute('''CREATE TABLE Labels(
#    [Index]                 INTEGER(10) 
#   ,[Timestamp]   VARCHAR(23)
#   ,[Chiller_ID]   VARCHAR(5)
#   ,[Label_Type]   VARCHAR(5)
#   ,[Status]   VARCHAR(5)
# )''')
                 
# conn.commit()
# engine = create_engine('sqlite:///C:/Users/ariel/flask-graphql-project/demo.db', echo=False)
# read_entries = pandas.read_csv(r'C:/Users/ariel/Desktop/dashboard_demo/dashboard_demo/app/backend/model/data/Labels.csv')
# read_entries.to_sql('Labels', con = engine, if_exists='append', index = False)

