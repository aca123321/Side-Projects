import mysql.connector
from easygui import *
import pandas as pd
import sqlalchemy

db = mysql.connector.connect(host = "localhost" , user = "aca123321" , passwd = "aca123321")
cur = db.cursor() 
engine = sqlalchemy.create_engine('mysql+pymysql://aca123321:aca123321@localhost:3306/warehouse')
df = pd.read_sql_table("grocer",engine)

def justname(x):
    st = str(x)
    st = st.replace("(","")
    st = st.replace(")","")
    st = st.replace("'","")
    st = st.replace(",","")
    return st;
    

un = enterbox("Enter your mysql username" , "MySQL Sign in")
if(un != "aca123321"):
    msgbox("Username incorrect", "Error")
    exit()
else:
    pw = passwordbox("Enter your mysql password" , "MySQL Sign in")
    if(pw != "aca123321"):
        msgbox("Password incorrect", "Error")
        exit()        
    else:
        cur.execute("use warehouse")

        # main window
        choice = ["Sorting" , "Classification" , "Product type"] 
        response = buttonbox("Choose:" , "Functions" , choice)

        #sorting window
        if(response == "Sorting"):
            sortchoice = ["Id", "price", "ExpiryDate" , "qty" ]
            response = buttonbox("Sort by" , "Sorting" , sortchoice)

            if(sortchoice != "Back"):
                st = "select * from grocer order by " + str(response)
                
                #cur.execute(st)
                #a = disp(cur)
                df = pd.read_sql_query(st,engine)
                st = str(df.iloc[0:])
                codebox("Items sorted by " + str(response) + " are:\n\nId) Name -- Retailer -- quantity -- Expiry Date -- Item price", "item list" , st)
                exit()
                
                

        #Classification window
        elif(response == "Classification"):
            classchoice = ["ExpiryDate", "Retailer"]
            response = buttonbox("Classification on the basis of" , "Classification" , classchoice)

            #ExpiryDate classification
            if(response == "ExpiryDate"):
                months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
                response = choicebox("Choose a month", "Expiry month", months)
                ind  = months.index(response)
                st = "0"
                if((ind + 1)>=10):
                    st = str(ind+1)
                else:
                    st += str(ind+1)
                s = "select * from grocer where expirydate like '%-" + st + "-%'"
                df = pd.read_sql_query(s,con = db)
                st = str(df.iloc[0:])
                codebox("Items expiring in " + str(response) + " are:\n\nId) Name -- Retailer -- quantity -- Expiry Date -- Item price", "item list" , st)
                exit()
    
            #Retailer Classification                
            else:
                ret = []
                st = ""
                cur.execute("select Retailer from grocer group by Retailer")
                for x in cur:
                    st = justname(x)
                    ret.append(st)
                response = choicebox("Choose a retailer", "Retailer", ret)
                st = "select * from grocer where Retailer = '" + response + "'"
                df = pd.read_sql_query(st,engine)
                st = str(df.iloc[0:])
                codebox("Items sold by " + str(response) + " are:\n\nId) Name -- Retailer -- quantity -- Expiry Date -- Item price", "item list" , st)
                exit()

        #Product Type
        else:
            response = enterbox("Enter a product type", "Product type")
            st = "select * from grocer where name like '%" + str(response) + "%'"
            df = pd.read_sql_query(st, con = db )
            s = str(df.iloc[0:])
            codebox(str(response) + " type products are:\n\nId) Name -- Retailer -- quantity -- Expiry Date -- Item price", "item list" , s)
            exit()
