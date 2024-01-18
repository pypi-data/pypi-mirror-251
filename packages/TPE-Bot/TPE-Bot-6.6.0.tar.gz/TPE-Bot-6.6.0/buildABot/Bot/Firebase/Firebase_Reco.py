import pandas as pd
import hashlib
import os

class Firebase_Reco:
    def __init__(self):
        pass

    def sanitizeID(df):
        # Admin No
        adminNumber = df["Full Admin Number"]#Collect Admin No. into variable
        adminID = adminNumber.str[3:8] #Get last 4 digits of Admin no.
        df["Admin Number"] = adminID

        strings = []
        for index, row in df.iterrows():
            b = row["Admin Number"].encode('utf-8')
            hashed = hashlib.sha224(b).hexdigest()
            strings.append(hashed)
        return strings
    
    def createGreetingNames(df):
        # Name
        student_name = df["Name"]
        name = student_name.str.split() #Split full name by whitespace into fragments
        name.dropna()
        sanitized_name, initial = '', ''
        shortname = []
        initials = []
        for n in name:
            if(len(n) == 2):
                sanitized_name = n[0] + '.' + n[1][0]
                initial = n[0][0] +  n[1][0]
                
            elif(len(n) == 3):
                sanitized_name = n[0] + '.' + n[1][0] + '.' + n[2][0]
                initial = n[0][0] +  n[1][0] + n[2][0]
                
            elif(len(n) == 4):
                sanitized_name = n[0] + '.' + n[1][0] + '.' + n[2][0] + '.' + n[3][0]
                initial = n[0][0] +  n[1][0] + n[2][0] + n[3][0]
                
            elif(len(n) == 5):
                sanitized_name = n[0] + '.' + n[1][0] + '.' + n[2][0] + '.' + n[3][0] + '.' + n[4][0]
                initial = n[0][0] +  n[1][0] + n[2][0] + n[3][0] + n[4][0]
                
            elif(len(n) > 5):
                sanitized_name = n[0] + '.' + n[1][0] + '.' + n[2][0] + '.' + n[3][0] + '.' + n[4][0] + '.' + n[5][0]
                initial = n[0][0] +  n[1][0] + n[2][0] + n[3][0] + n[4][0] + n[5][0]

            shortname.append(sanitized_name)
            initials.append(initial)

        return shortname, initials
    
    def combineResult(studentData, strings, shortname, initials):
        xls = pd.ExcelFile(os.getenv('resultFile'))
        sheets = xls.sheet_names # list all sheets in the file
        sheets = sheets[1:] # exclude 1st sheet - rubrics
        data = pd.DataFrame()

        for sheet in sheets:
            #read each marking sheet
            df_assignment = pd.read_excel(os.getenv('resultFile'), sheet_name="{}".format(sheet))

            # Rename common column to prevent clash in db
            df_assignment['{} Grade'.format(sheet)] = df_assignment["Grade"]
            df_assignment['{} Total'.format(sheet)] = df_assignment["Total"]
            df_assignment['{} Feedback'.format(sheet)] = df_assignment["Feedback"]

            # Remove unwanted columns
            df_assignment.drop('Student', axis='columns', inplace=True)
            df_assignment.drop('Class', axis='columns', inplace=True)
            df_assignment.drop('Grade', axis='columns', inplace=True)
            df_assignment.drop('Total', axis='columns', inplace=True)
            df_assignment.drop('Feedback', axis='columns', inplace=True)
            
            #combine the different marking sheets into 1 
            data = pd.concat([data, df_assignment], axis=1) 

        # Add new columns for user details
        data["ID"] = strings
        data["NAME"] = shortname
        #data["PWD"] = shortname
        #data["VERIFY"] = initials

        studentData.drop(['Class', 'Name', 'Full Admin Number' , 'Admin Number'], axis='columns', inplace=True)
        dbdata = pd.concat([data, studentData], axis=1)
        #dbdata = pd.concat([data, df_sub], axis=1)

        return dbdata
        
    
    def createDBData(data): 
        data.to_csv(os.getenv('DBData'), index=False)
        data.to_json(os.getenv('DBDataJSON'))