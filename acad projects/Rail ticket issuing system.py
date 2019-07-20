import mysql.connector
import sqlalchemy as sa
import pandas as pd
from easygui import *


db = mysql.connector.connect(host = "localhost" , user = "aca123321" , passwd = "aca123321")
cur = db.cursor()
engine = sa.create_engine("mysql+pymysql://aca123321:aca123321@localhost:3306/raildb")
df = pd.read_sql_table("railinfo",engine)

def justname(x):
    st = str(x)
    st = st.replace("(","")
    st = st.replace(")","")
    st = st.replace("'","")
    st = st.replace(",","")
    return st;

choice = ["Username", "Password"]
un,pw = multenterbox("Sign in" , "Enter details:" , choice)
	
if(un == 'asd'):
	if(pw == 'asd'):

		# SUCCESSFUL Login
		cur.execute("use raildb")
		
		#source selection
		cur.execute("select Source_Station_Name from railinfo group by Source_Station_Name")
		ret = []
		for x in cur:
			ret.append(justname(x))
		source = choicebox("Choose a source:" , "Source selection" , ret)	

		#destination selection
		cur.execute("select Destination_Station_Name from railinfo group by Source_Station_Name")
		ret = []
		for x in cur:
			ret.append(justname(x))
		destination = choicebox("Choose a destination:" , "Source selection" , ret)

		st = "select * from railinfo where Source_Station_Name = '" + str(source) + "' and Destination_Station_Name = '" + str(destination) + "'"
		df = pd.read_sql_query(st,engine)
		st = str(df.iloc[0:])
		codebox("Available trains from " + str(source) + " to " + str(destination) + " are:" , "Trains display" , st)
		exit()
	


	else:
		msgbox("Incorrect password:\nusername entered: " + un + "\npassword entered: " + pw , "Sign in result")
            
else:
	msgbox("Incorrect username:\nusername entered: " + un + "\npassword entered: " + pw , "Sign in result")

