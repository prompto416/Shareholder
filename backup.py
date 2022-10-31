import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import math
import dbConnect 
from deep_translator import GoogleTranslator
import threading

#sample of multiple cell update
# cell_list = fundSheet.range('A25:B289')
# cell_values = [1,2,3,4,5,6,7]
# for i, val in enumerate(cell_values):  #gives us a tuple of an index and value
#     cell_list[i].value = val    #use the index on cell_list and the val from cell_values
# fundSheet.update_cells(cell_list)



def myFormatDecimal(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

def num2col(n):
    """Number to Excel-style column name, e.g., 1 = A, 26 = Z, 27 = AA, 703 = AAA."""
    name = ''
    while n > 0:
        n, r = divmod (n - 1, 26)
        name = chr(r + ord('A')) + name
    return name

def col2num(name):
    """Excel-style column name to number, e.g., A = 1, Z = 26, AA = 27, AAA = 703."""
    n = 0
    for c in name:
        n = n * 26 + 1 + ord(c) - ord('A')
    return n

#ใช้เเยกระหว่างกองทุนกับคนเบื้องต้น 
def getFundOrInvestor(userInput):
    #0 = Fund
    #1 = Investory
    #3 = Full List
    # bug เอาเม้นออกถ้าบัค
    summaryColumnB = globalVar1

    fundAndInvestor =  []
    titleMatcher = ['บริษัท','ห้างหุ่นส่วน','กองทุน','จำกัด','มหาชน','limited','company','listed','publicly','partnership','fund'
            ,'incorporation','corporation','ltd','inc.','pte']
    capTitle = [x.upper() for x in titleMatcher]
    titleMatcher += capTitle
    
    
    for i in summaryColumnB:
        for j in i:
            fundAndInvestor.append(j)
    fundAndInvestor = list(dict.fromkeys(fundAndInvestor))
    if userInput == 3:
        return fundAndInvestor
    fundAndInvestor = [ele.upper() for ele in fundAndInvestor]

    investor = fundAndInvestor
    fund = [ele for ele in fundAndInvestor if any(funds in ele for funds in titleMatcher)]
    for ele in fund:
        if ele in investor:
            investor.remove(ele)

    if userInput == 0:
        return list(dict.fromkeys(fund))
    elif userInput == 1:
        return list(dict.fromkeys(investor))
    else:
        print("ValueError: INVALID INPUT!!!")
        raise ValueError
        return ValueError

# fund = getFundOrInvestor(0)
# investor = getFundOrInvestor(1)
# fundAndInvestor = fund+investor

#เป็นฟังก์ชั่นคัดกรองข้อมูลก่อนไปคัดอีกที ลอง Print ค่าดูคับ
#post-requisite data for appendPerformanceToList function
def getInterestedPerformance(interestedData,month):
    
    profitList = []
    lossList = []
    lossCount = 0
    profitCount = 0

    if month == 1:
        monthIndex = 3
    elif month == 3:
        monthIndex = 4
    elif month == 6:
        monthIndex = 5
    elif month == 12:
        monthIndex = 6
    else:
        print('Invalid Month input')
        quit()
    for i in range(len(interestedData)):
        if float(interestedData[i][1]) < 0:
            buyOrSell = 'sell'
        elif float(interestedData[i][1]) >= 0:
            buyOrSell = 'buy'
        priceAction = float(interestedData[i][2])
        priceMonth = interestedData[i][monthIndex]
        if priceMonth == '-':
            return ['-']
        priceMonth = float(priceMonth)
        #First time was buy
        # if (buyOrSell == 'buy'):
        #     if priceAction < priceMonth:
        #         lossCount += 1
        #         lossList.append(priceMonth - priceAction)
        #     elif priceAction > priceMonth:
        #         profitCount += 1
        #         profitList.append(priceAction - priceMonth)
        # #Was sell
        # elif buyOrSell == 'sell':
        #     if priceAction > priceMonth:
        #         profitCount += 1
        #         profitList.append(priceAction - priceMonth)
        #     elif priceAction < priceMonth:
        #         lossCount += 1
        #         lossList.append(priceMonth - priceAction)
        # else:
        #     print('invalid buy or sell input')
        #     quit()
            
           #First time was buy
        if (buyOrSell == 'buy'):
            if priceAction < priceMonth:
                profitCount += 1
                profitList.append(priceMonth - priceAction)
            elif priceAction > priceMonth:
                lossCount += 1
                lossList.append(priceAction - priceMonth)
        #Was sell
        elif buyOrSell == 'sell':
            if priceAction < priceMonth:
                lossCount += 1
                lossList.append(priceMonth - priceAction)
            elif priceAction > priceMonth:
                profitCount += 1
                profitList.append(priceAction - priceMonth)
        else:
            print('invalid buy or sell input')
            quit()

    interestedCount = len(interestedData)
    
        
    performanceMonth = (profitCount / interestedCount)
    
        

    # try:
    #     maxProfit = max(profitList)
    # except:
    #     maxProfit = 0
    # try:
    #     avgProfit = sum(profitList)/profitCount
    # except ZeroDivisionError:
    #     avgProfit = '-'
    # try:
    #     maxLoss = max(lossList)
    # except:
    #     maxLoss = 0
    # try:
    #     avgLoss = sum(lossList)/lossCount
    # except:
    #     avgLoss = '-'
    if len(profitList) > 0:
        maxProfit = max(profitList)
    else:
        maxProfit = 0
    if len(lossList) > 0:
        maxLoss = max(lossList)
    else:
        maxLoss = 0
    if profitCount > 0:
        avgProfit = sum(profitList)/profitCount
    else:
        avgProfit = 0
    # avgProfit = '-'
    if lossCount > 0:
        avgLoss = sum(lossList)/lossCount
    else:
        avgLoss = 0
    # avgLoss = '-'
        
    interestedStats =  [performanceMonth,maxProfit,avgProfit,maxLoss,avgLoss]
    #format decimal 
    for i in range(1,len(interestedStats)):
        if type(interestedStats[i]) != type(str()):
            # interestedStats[i] = myFormatDecimal(interestedStats[i],2)
            interestedStats[i] = f"{interestedStats[i]:.2f}"
        
            
    if interestedStats[0] != '-':
        # interestedStats[0] = f"{float(interestedStats[i])}%"
        percentageBuffer = myFormatDecimal(interestedStats[0]*100,2)
        
        
        interestedStats[0] = str(percentageBuffer)+"%"
        
    
    return interestedStats

#ใช้ข้อมูลจากฟังก์ชันก่อนหน้ามาใส่ใน List เเล้วค่อยเอา List ไปใช้เขียนตามเเต่ละ index
def appendPerformanceToList(interested):
    if type(interested) != list:   
        originInterested = interested
    elif type(interested) == list:
        originInterested = interested[0]
    
    
    
    interestedPerformance = [interested]
    oldMax = -9999999999999
    listOfOccurence = []
    colBtoI = globalVar2
    #buy or sell will be determined by negative and positive number instead
    # buyOrSell = summary.get('Z2:Z999')
    for i in range(len(colBtoI)):
        #using the database in this block เอาชื่อมา mark ว่าเป็นคนเดียวกันในนี้
        
        if (type(interested) != list):
            interested = interested.upper()
            if ((colBtoI[i][0].upper() == interested)):
            # print(colBtoI[i][0].upper(),interested)
                listOfOccurence.append(colBtoI[i])
        elif (type(interested)) == list:
            if (colBtoI[i][0].upper() in interested):
                # if (GoogleTranslator(source='auto', target='en').translate(colBtoI[i][0].upper())).upper() in interested:
                listOfOccurence.append(colBtoI[i])
                    # print(colBtoI[i][0].upper())


    
    interested1month = getInterestedPerformance(listOfOccurence,1)
    interested3month = getInterestedPerformance(listOfOccurence,3)
    interested6month = getInterestedPerformance(listOfOccurence,6)
    interested12month = getInterestedPerformance(listOfOccurence,12)
    interestColumn = interested1month+interested3month+interested6month+interested12month
    interestColumn.insert(0,originInterested)
    interestColumn.insert(1,len(listOfOccurence))
    
    return interestColumn

def labelColumn():
    # fundSheet.update("B1","hello world")
    labelColAB = ["Name","#Trade"]
    labelColC = ["Performance","Max Profit","Avg Profit ( Sum Profit / # Profit )","Max Loss","Avg Loss ( Sum Loss / # Loss)"]
    labelColC = labelColC * 4
    timeFrame = [1,3,6,12]
    performanceIndex = 0
    for i in range(4):
        labelColC[performanceIndex] = f"{labelColC[performanceIndex]} {str(timeFrame[i])}"
        performanceIndex += 5
    fundSheet.update("A1",labelColAB[0])
    fundSheet.update("B1",labelColAB[1])
    labelCellList = fundSheet.range("C1:V1")
    for i,val in enumerate(labelColC):
        labelCellList[i].value = val
    fundSheet.update_cells(labelCellList)
    fundSheet.format("A1:V1", {"textFormat": {"bold": True}})
    
    investorSheet.update("A1",labelColAB[0])
    investorSheet.update("B1",labelColAB[1])
    labelCellList = investorSheet.range("C1:V1")
    for i,val in enumerate(labelColC):
        labelCellList[i].value = val
    investorSheet.update_cells(labelCellList)
    investorSheet.format("A1:V1", {"textFormat": {"bold": True}})
    
    fundSheet.format("C2:V999", {"horizontalAlignment": "RIGHT"})
    investorSheet.format("C2:V999", {"horizontalAlignment": "RIGHT"})
    
    fundSheet.format("C2:G999", {"backgroundColor": {
      "red": 0.97,
      "green": 0.79,
      "blue": 0.61}},
      )
    fundSheet.format("H2:L999", {"backgroundColor": {
      "red": (217)/255,
      "green": (234)/255,
      "blue": (211)/255}})
    fundSheet.format("M2:Q999", {"backgroundColor": {
      "red": (255)/255,
      "green": (242)/255,
      "blue": (204)/255}})
    fundSheet.format("R2:V999", {"backgroundColor": {
      "red": (208)/255,
      "green": (224)/255,
      "blue": (227)/255}})
    
    investorSheet.format("C2:G999", {"backgroundColor": {
      "red": 0.97,
      "green": 0.79,
      "blue": 0.61}})
    investorSheet.format("H2:L999", {"backgroundColor": {
      "red": (217)/255,
      "green": (234)/255,
      "blue": (211)/255}})
    investorSheet.format("M2:Q999", {"backgroundColor": {
      "red": (255)/255,
      "green": (242)/255,
      "blue": (204)/255}})
    investorSheet.format("R2:V999", {"backgroundColor": {
      "red": (208)/255,
      "green": (224)/255,
      "blue": (227)/255}})


def finalWritingFunction():
    fundRes = []
    fund = getFundOrInvestor(0)
    investor = getFundOrInvestor(1)
    investorRes = []
    #changing name with multiple name into the a list instead of a string 
    for i in range(len(fund)):
        tempTrans = GoogleTranslator(source='auto', target='en').translate(fund[i])
        dbDataF = dbConnect.checkName(tempTrans,"fund")
        if dbDataF == None:
            continue
        elif dbDataF != None:
            originalFund = fund[i]
            dbDataF.insert(0,originalFund)
            fund[i] = dbDataF
            
    for i in range(len(investor)):
        tempTrans = GoogleTranslator(source='auto', target='en').translate(investor[i])
        dbDataI = dbConnect.checkName(tempTrans,"investor")
        if dbDataI == None:
            continue
        elif dbDataI != None:
            originalInvestor = investor[i]
            dbDataI.insert(0,originalInvestor)
            investor[i] = dbDataI
            
     #Adding more translated matching names into the same list 
    matchedIndex_fund = []
    # toBeRemoved_fund = []
    for i in range(len(fund)):
        if type(fund[i]) == list:
            matchedIndex_fund.append(i)
            
    for i in matchedIndex_fund:
        for j in matchedIndex_fund:
            if (fund[i][0] != fund[j][0]) and (fund[i][1] == fund[j][1]):
                fund[i].append(fund[j][0]) 
                # toBeRemoved_fund.append(fund[j])
    
    # for i in toBeRemoved_fund:
    #     fund.remove(i)
    
    #Adding translated matching names into the same list 
    matchedIndex_investor = []
    for i in range(len(investor)):
        if type(investor[i]) == list:
            matchedIndex_investor.append(i)
            
    for i in matchedIndex_investor:
        for j in matchedIndex_investor:
            if (investor[i][0] != investor[j][0]) and (investor[i][1] == investor[j][1]):
                investor[i].append(investor[j][0]) 
        
    
        
                

    #Evalute Data and save into list with previous functions
    for i in fund:
        
        fund_dataToWrite = appendPerformanceToList(i)
        fundRes.append(fund_dataToWrite)
    
    # for i in fundRes:
    #     for j in fundRes:
    #         if (i[1:] == j[1:]) and (i[0] != j[0]):
    #             print(i)
    #             print(j)
    #             print()
    
    for i in range(len(fundRes)):
        try:
            for j in range(len(fundRes)):
                if (fundRes[i][1:] == fundRes[j][1:]) and (fundRes[i][0] != fundRes[j][0]):
                    tempTrans1 = (GoogleTranslator(source='auto', target='en').translate(fundRes[i][0].upper())).upper()
                    tempTrans2 = (GoogleTranslator(source='auto', target='en').translate(fundRes[j][0].upper())).upper()
                    tempTransCheck_list = dbConnect.checkName(tempTrans1,"fund")
                    if (tempTrans1 in tempTransCheck_list) and (tempTrans2 in tempTransCheck_list):
                        fundRes[i][0] = f"{fundRes[i][0]}/{fundRes[j][0]}"
                        fundRes.remove(fundRes[j])
        except:
            continue
    
                
                
    fundSheet.batch_update([{
    'range': 'A2:V999',
    'values': fundRes,
    }, ])

    for i in investor:
        investor_dataToWrite = appendPerformanceToList(i)
        investorRes.append(investor_dataToWrite)

    for i in range(len(investorRes)):
        try:
            for j in range(len(investorRes)):
                if (investorRes[i][1:] == investorRes[j][1:]) and (investorRes[i][0] != investorRes[j][0]):
                    tempTrans1 = (GoogleTranslator(source='auto', target='en').translate(investorRes[i][0].upper())).upper()
                    tempTrans2 = (GoogleTranslator(source='auto', target='en').translate(investorRes[j][0].upper())).upper()
                    tempTransCheck_list = dbConnect.checkName(tempTrans1,"investor")
                    if (tempTrans1 in tempTransCheck_list) and (tempTrans2 in tempTransCheck_list):
                        investorRes[i][0] = f"{investorRes[i][0]}/{investorRes[j][0]}"
                        investorRes.remove(investorRes[j])
        except:
            continue
    
    investorSheet.batch_update([{
    'range': 'A2:V999',
    'values': investorRes,
    }, ])
    
#Start of the script
scope =['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('testSheetAPI_Key.json', scope)
client = gspread.authorize(creds)

summary_Name = client.open_by_key("1i40P3kmMFiAnfaIRo70AL22iGBbvJaR_WoccHJb0RvU").worksheet("Name")
symbolNames_raw = summary_Name.get("A2:A99999")
symbolKeys_raw = summary_Name.get("B2:B99999")
symbolNames = [item for sublist in symbolNames_raw for item in sublist]
symbolKeys = [item for sublist in symbolKeys_raw for item in sublist]


#change userInput into list of stock symbols
usin = ["shareholderSummary_testSheet","speedtest1","speedtest2","speedtest3"]

# core(36,195)
# for targetIteration in range(startingIndex,len(symbolKeys)-1):
for targetIteration in range(83,780-1):
    # targetSheet = "shareholderSummary_testSheet"
    targetSheet_Name = symbolNames[targetIteration]
    targetSheet = symbolKeys[targetIteration]
    f = open("summaryLog.txt","a")
    # folderID = "1hSJLJfkPfgKdOW7sQAovRq3fUntZzkEa"
    folderID = None
    #potential bug because except with no specific error
    #potential bug2 global variable summarycolumnb and colbtoI


# opened = client.open(targetSheet,folderID)
    opened = client.open_by_key(targetSheet)
    summary = opened.worksheet('Summary')

    try:
        investorSheet = opened.worksheet('Investor')
        
    except gspread.exceptions.WorksheetNotFound:
        investorSheet = opened.add_worksheet(title="Investor",rows=0,cols=0)

    try:
        fundSheet = opened.worksheet('Fund')
    except gspread.exceptions.WorksheetNotFound:
        fundSheet = opened.add_worksheet(title="Fund",rows=0,cols=0)
        

    #global variable scope 
    globalVar1 = summary.get('B2:B9999')
    globalVar2 = summary.get('B2:I999')
    # summaryB2 = summary.get('B2:B9999')
    summaryB2 = globalVar1
    summaryB2 = [item for sublist in summaryB2 for item in sublist]
    print(targetSheet_Name,"Start!",datetime.datetime.now().strftime("%H:%M:%S"))
    f.write(f"{targetSheet_Name} Start!{datetime.datetime.now()}")
    labelColumn()
    finalWritingFunction()
    print(targetSheet_Name,"Done!",datetime.datetime.now().strftime("%H:%M:%S"))
    f.write(f"{targetSheet_Name} Done!{datetime.datetime.now()}\n")
    # f.write(f"{targetSheet_Name} Done!\n")
    f.close()
    if targetIteration == len(symbolKeys):
        print("Finished",targetIteration,len(symbolKeys))
        quit()

# thread1 = threading.Thread(target=core,args=(0,195))
# thread1.start()
# thread2 = threading.Thread(target=core,args=(196,390))
# thread2.start()
# thread3 = threading.Thread(target=core,args=(391,585))
# thread3.start()
# thread4 = threading.Thread(target=core,args=(586,780-1))
# thread4.start()

#11 writing requests per sheets








#old writing loop
# for i in fund:
#     if count % 30 == 0 :
#         print('sleeping for a minute')
#         time.sleep(60)
#     dataToWrite = appendPerformanceToList(i)
#     fundCellList = fundSheet.range(f"A{count}:V{count}")
#     print(dataToWrite)
#     for j in range(len(fundCellList)):
#         try:
#             fundCellList[j].value = dataToWrite[j]
#         except IndexError:
#             pass
#     fundSheet.update_cells(fundCellList)
 
#     count+=1
# print("Finished writing, Sleeping for a minute")
# count = 2
# time.sleep(60)

# investor = getFundOrInvestor(1)
# for i in investor:
#     if count % 30 == 0 :
#         print('sleeping for a minute')
#         time.sleep(60)
#     dataToWrite = appendPerformanceToList(i)
#     investorCellList = investorSheet.range(f"A{count}:V{count}")
#     for j in range(len(investorCellList)):
#         try:
#             investorCellList[j].value = dataToWrite[j]
#         except IndexError:
#             pass
#     investorSheet.update_cells(investorCellList)
#     count+=1










