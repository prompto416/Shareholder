import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="shareholderNamedb"
)
# mycursor = mydb.cursor()
# mycursor.execute("SELECT * FROM `other` WHERE `Table1` LIKE '%NVDR%' AND `awswer` LIKE 'Y';")
# myresult = mycursor.fetchall()

def checkName(name,queryType):
    if queryType == "fund":
        queryType = "other"
    elif queryType == "investor":
        queryType = "person"
    else:
        raise Exception("Invalid dbConnect.checkname parameter: queryType")
        quit()

    res = []
    cursor = mydb.cursor()
    # try:
        
    cursor.execute(f'SELECT * FROM `{queryType}` WHERE `Table1` LIKE "%{str(name)}%" AND `awswer` LIKE "Y";')
    checkNameTempList = cursor.fetchall()
    cursor.execute(f'SELECT * FROM `{queryType}` WHERE `Table2` LIKE "%{str(name)}%" AND `awswer` LIKE "Y";')
    checkNameTempList += cursor.fetchall()
    # except:
    #     print("SQL ERROR NAME: ",name)
    #     # quit()
    for i in checkNameTempList:
        if i[1] not in res:
            res.append(i[1])
        if i[2] not in res:
            res.append(i[2])
    if len(res) > 0:
        return res
    return None

# matched = checkName("THAILAND SECURITIES DEPOSITORY COMPANY LIMITED","fund")





# (87028595, 'MUANG THAI INSURANCE PUBLIC COMPANY LIMITED', 'BANGKOK THANATHON FINANCE PUBLIC COMPANY LIMITED', '-', 'Y')
# (87034984, 'THAI NVDR COMPANY LIMITED', 'THAI ALLIANCE COMPANY LIMITED', 'SIS', 'Y')
# (38765909, 'SRIMITR FINANCE AND SECURITIES PUBLIC COMPANY LIMITED', 'EKTHANAKIJ FINANCE PUBLIC COMPANY LIMITED', 'DCC', 'Y')
# (38770883, 'SCF FINANCE AND SECURITIES PUBLIC COMPANY LIMITED', 'KIATNAKIN FINANCE AND SECURITIES PUBLIC COMPANY LIMITED', '-', 'Y')