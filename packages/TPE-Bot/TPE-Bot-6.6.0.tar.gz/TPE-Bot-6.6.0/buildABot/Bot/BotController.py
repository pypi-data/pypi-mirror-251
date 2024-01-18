import pandas as pd
import os
import buildABot

from .Intents.Paraphraser import Paraphraser

from .Intents.CustomIntents import CustomIntents
from .Intents.CustomMenu import CustomMenu
from .Intents.CustomRecommendedMenu import CustomRecommendedMenu
from .Intents.DefaultIntent import DefaultIntent
from .Intents.Usersays import Usersays

from .Intents.FallbackSocialTag import FallbackSocialTag
from .Intents.Worksheets_Learn import Worksheets_Learn
from .Intents.Worksheets_Reco import Worksheets_Reco

from .Firebase.Entities import Entities

from .Firebase.Webhook_Learn import Webhook_Learn
from .Firebase.Webhook_Reco import Webhook_Reco

from .Firebase.Firebase_Learn import Firebase_Learn
from .Firebase.Firebase_Reco import Firebase_Reco

from .Webapp.WebApp_Learn import WebApp_Learn
from .Webapp.WebApp_Reco import WebApp_Reco

from .Dashboard.TelegramLogs import TelegramLogs
from .Dashboard.Analytics import Analytics

from .WriteToFile import WriteToFile

package_dir = os.path.abspath(buildABot.__path__[0])

class BotController(Paraphraser,
                    FallbackSocialTag, Worksheets_Learn, Worksheets_Reco, 
                    Entities, Webhook_Learn, Webhook_Reco, Firebase_Learn, Firebase_Reco, 
                    WebApp_Learn, WebApp_Reco, 
                    TelegramLogs, Analytics):
    
    def __init__(self, inputFile, resultFile, keyFile):
        # self.qaFile = qaFile
        # self.slFile = slFile
        # self.studentFile = studentFile
        self.inputFile = inputFile
        self.resultFile = resultFile
        self.keyFile = keyFile

    def getData(file, sheetName):
        """
        Read QAfile and clean the file before using
        :param file: QA_data.xlsx, SL Inputs.xlsx
        :return: [Dataframe] Cleaned file as dataframe
        """
        # Get QAfile and read as dataframe
        df = pd.read_excel(file, dtype=str, sheet_name=sheetName)
        df.fillna(value='', inplace=True)
        return df
    
    def formatQA(self, df):
        """
            To create labels for Main Topics, Sub Topics & Intents for Analytics, FAQ and Intent Naming purposes
            :return: [dataframe] Updated QA file with different labels columns
        """
        #df = BotController.getData(file, 'QA')
        listOfMainTopics = df['Main Topic'].unique().tolist()  # Get list of topics
        mainTopicsLabels, subTopicsLabels, intentsLabels, numOfMTIntents = [], [], [], []  # Initialise empty arrays
        count = 1  # Set counter to 1

        '''
        Grouping Intents by Main & Sub Topics
        Set labels for MainTopics, SubTopics and Intents (To be used in Analytics)
        '''
        for i in range(len(listOfMainTopics)):  # Loop for no. of MainTopics
            subTopicsCount = 1  # set counter for subtopic
            mainTopics = df.loc[df['Main Topic'] == listOfMainTopics[i]]  # Filter to each Main Topics
            subTopics = mainTopics['Sub Topic'].unique().tolist()  # Get Sub Topics from each Main Topics

            if (subTopics != ['']):  # For intents that has subtopics
                for i in range(len(subTopics)):
                    subTopic = mainTopics.loc[mainTopics['Sub Topic'] == subTopics[i]]  # Filter to each Sub Topics
                    numOfSTIntents = len(subTopic.index) * [subTopicsCount]  # Get number of intents for each sub topics
                    subTopicsLabels.extend(numOfSTIntents)  # Put labels from count of each subtopics into list
                    subTopicsCount += 1
            else:  # For intent that has no sub topic
                numOfSTIntents = len(mainTopics.index) * ['']
                subTopicsLabels.extend(numOfSTIntents)  # Add blank to list to indicate no sub topics

            numOfMTIntents.append(len(mainTopics.index))  # Get number of intents for each main topics

        for num in numOfMTIntents:
            for i in range(num):
                mainTopicsLabels.append(count)  # Make Main Topics Labelling
                intentsLabels.append(i + 1)
            count += 1

        responses = []
        for index, row in df.iterrows():
            responses.append(row['Response'].replace('<br>', '\n\n'))
        '''
        Create new columns for each labels
        Store updated QA with labels (for Analytics & FAQ)
        '''
        df['Main Label'] = mainTopicsLabels
        df['Sub Label'] = subTopicsLabels
        df['Intent Label'] = intentsLabels
        
        ''' Ensure Name is accepted '''
        df['Name'] = df['Name'].replace('/', ' or ')
        df['Name'] = df['Name'].replace('?', '')
        df['Name'] = df['Name'].replace('"', "'")
        df['Name'] = df['Name'].replace('.', '')
        df['Name'] = df['Name'].replace('[', '')
        df['Name'] = df['Name'].replace(']', '')
        df['Name'] = df['Name'].replace('#', '')
        df['Name'] = df['Name'].replace('$', '')

        df['Response'] = responses
        
        # Intent Number, Small Name, Full Name
        intentNum, fullName, smallName, idxNum = [], [], [] , []
        for index, row in df.iterrows():
            intent_name = str(row['Main Label']) + '.' + str(row['Intent Label']) + ' ' + row['Main Topic'] + ' - ' + row['Name']
            intentNum.append(str(row['Main Label']) + '.' + str(row['Intent Label']))
            fullName.append(intent_name) #for dashboard
            smallName.append(row['Main Topic'] + ' - ' + row['Name']) #for dashboard
            idxNum.append(str(index+1))

        df['Intent Number'] = intentNum
        df['Small Name'] = smallName
        df['Full Name'] = fullName
        df['Events'] = df['Name'].str.replace(" ", "")

        return df
    
    def createParaphrases(self):
        df = BotController.getData(self.inputFile, "QA")
        qa = df.applymap(lambda x: x.strip())
        dfFormatted = BotController.formatQA(self, qa)
        dfFormatted.to_excel(os.getenv('paraFile'), index=False)
        Paraphraser.random_state(1234)
        qaData = BotController.getData(file=os.getenv('paraFile'), sheetName='Sheet1')
        df, df_qn, dfString = Paraphraser.extractData(df=qaData)
        numTrainPara, paraphrases = Paraphraser.paraphrase(dfString=dfString)
        Paraphraser.createNewQAFile(numTrainPara=numTrainPara, paraphrases=paraphrases, df=df, df_qn=df_qn)
        
    def createCustomIntents(self):    
        """
        Executing the different functions to obtain JSON files of all intents
        :return: Display message after successful excution
        """
        df = BotController.getData(os.getenv('paraFile'), 'Sheet1')
        CustomIntents.createIntentResponse(df)
        Usersays.createUserSays(df)

    def createLearnMenu(self):
        df = BotController.getData(os.getenv('paraFile'), 'Sheet1')
        CustomMenu.createLearnMenu(df["Main Topic"].unique())
        CustomMenu.createSubMenu(df[['Main Topic', 'Sub Topic', 'Name']])
        CustomMenu.createIntentsMenu(df)

    def createRecoMenu(self):
        df = BotController.getData(os.getenv('resultFile'), 'Rubrics')
        assignments, criteria, subTopic, counts = CustomRecommendedMenu.getInfo(os.getenv('resultFile'), df)
        
        CustomRecommendedMenu.createRecommendedMainMenu(assignments)
        CustomRecommendedMenu.createRecommendedAssignmentMenu(assignments)
        CustomRecommendedMenu.createRecommendedCriteriaMenu(df)

    def createSocialTag(self):
        dfStudents = BotController.getData(self.inputFile, 'Student List')
        intent = FallbackSocialTag.createSocialTagFallbackNo(df=dfStudents)
        WriteToFile.write_file_json(os.getenv('socialTagFallbackNo'),intent)

    def createLearnWorksheets(self):
        df = BotController.getData(self.inputFile, 'Worksheets-Hot Topics')

        intent_payload, worksheetArray = Worksheets_Learn.createWsIntent(self, df)
        intent_payload, hotTopicsArray = Worksheets_Learn.createHotTopics(self, df, intent_payload=intent_payload)
        Worksheets_Learn.createSentimentIntents(self, intent_payload=intent_payload)

        '''
        Default Intents
        '''
        DefaultIntent.createWelcomeIntent(worksheetArray, hotTopicsArray)
        DefaultIntent.createFallbackIntent(worksheetArray, hotTopicsArray)

    def createRecoWorksheets(self):
        df = BotController.getData(self.inputFile, 'Worksheets-Hot Topics')
        
        intent_payload, worksheetArray = Worksheets_Reco.createWsIntent(df)
        intent_payload, hotTopicsArray = Worksheets_Reco.createHotTopics(df, intent_payload=intent_payload)
        Worksheets_Reco.createSentimentIntents(self, intent_payload=intent_payload)

        '''
        Default Intents
        '''
        DefaultIntent.createRecoWelcomeIntent(worksheetArray, hotTopicsArray)
        DefaultIntent.createRecoFallbackIntent(worksheetArray, hotTopicsArray)

    def createEntities(self):
        studentData = BotController.getData(file=self.inputFile, sheetName='Student List')
        slData = BotController.getData(file=self.inputFile, sheetName='Info')

        cleanedStudentData = Entities.cleanStudentID(studentData)
        Entities.createEntity(cleanedStudentData)

    def createLearnWebhook(self):
        slData = BotController.getData(file=self.inputFile, sheetName='Info')
        accKeyFile, template = Webhook_Learn.readFiles(keyFile=self.keyFile)
        template = Webhook_Learn.getInfo(slData=slData, accKeyFile=accKeyFile, template=template)
        
        data = Webhook_Learn.assignmentNudge(df=BotController.getData(self.inputFile, 'Student List'), template=template)
        final = Webhook_Learn.getSocialTaggingStrings(data, BotController.getData(self.inputFile, 'Student List'))
        Webhook_Learn.createFulfillment(template=final)

    def createRecoWebhook(self):
        df = BotController.getData(self.inputFile, 'Info')
        acckey, dbUrl, email, gcpEmail, gcpAppKey = Webhook_Reco.getFromSLInputs(df=df, keyFile=self.keyFile)
       

        df = BotController.getData(self.resultFile, 'Rubrics')
        functions, intentMaps = Webhook_Reco.getAssignments(df=df)
        assign_strings, checks, textAssignments, teleAssignments = Webhook_Reco.submissionNudge(df=df)#BotController.getData(self.inputFile, 'Student List'))

        data = Webhook_Reco.createWebhookCode(acckey, dbUrl, email, gcpEmail, gcpAppKey, functions, intentMaps, assign_strings, checks, textAssignments, teleAssignments)
        
        dfStudents = BotController.getData(self.inputFile, 'Student List')
        indexJS = Webhook_Reco.createFallback(df=dfStudents, data=data)

        Webhook_Reco.writeFile(indexJS)

        '''
        functions, intentMaps = Webhook_Reco.webhookMenuFunction(numOfTopics, topics, numOfAssignments, threshold)
        assign_strings, checks, textAssignments, teleAssignments = Webhook_Reco.submissionNudge(df=BotController.getData(self.inputFile, 'Student List'))
        data = Webhook_Reco.webhookCode(acckey, dbUrl, email, gcpEmail, gcpAppKey, functions, intentMaps, assign_strings, checks, textAssignments, teleAssignments)
       
        dfStudents = BotController.getData(self.inputFile, 'Student List')
        indexJS = Webhook_Reco.createFallback(df=dfStudents, data=data)

        Webhook_Reco.writeFile(indexJS)
        '''
    def createLearnFirebase(self):
        studentData = BotController.getData(file=self.inputFile, sheetName='Student List')
        slData = BotController.getData(file=self.inputFile, sheetName='Info')

        data, slLogins = Firebase_Learn.getID(data=studentData, slData=slData)
        strings = Firebase_Learn.dataEncryption(data=data, slLogins=slLogins)
        names = Firebase_Learn.sanitiseName(data=studentData)
        Firebase_Learn.createDBData(strings=strings, names=names, df=studentData)

    def createRecoFirebase(self):
        df = BotController.getData(self.inputFile, 'Student List')

        strings = Firebase_Reco.sanitizeID(df=df)
        shortname, initials = Firebase_Reco.createGreetingNames(df=df)
        dbdata = Firebase_Reco.combineResult(studentData=df, strings=strings, shortname=shortname, initials=initials)
        Firebase_Reco.createDBData(data=dbdata)

    def createLearnWebapp(self):
        df = BotController.getData(file=self.inputFile, sheetName='Info')
        template = WebApp_Learn.readFiles()
        data = WebApp_Learn.getInfo(df=df, data=template)

        customDF = BotController.getData(file=self.inputFile, sheetName='Customisation')
        data1 = WebApp_Learn.dfMessengerfontSizeCustomisation(customDF, data)
        data2 = WebApp_Learn.dfMessengerFontCustomisation(customDF, data1)
        data3 = WebApp_Learn.dfMessengerSchemeCustomisation(customDF, data2)

        WebApp_Learn.createHTML(data=data3)

    def createRecoWebApp(self):
        df = BotController.getData(self.inputFile, 'Info')
        index_temp, index_file, index_data = WebApp_Reco.getFiles()
        WebApp_Reco.customisationHTML(df=df, index_file=index_file, index_data=index_data)
        #config = WebApp_Reco.getFirebaseConfig()
        #WebApp_Reco.resetJS(reset_data=reset_data, reset_file=reset_file, config=config)
        WebApp_Reco.closeFiles(index_temp=index_temp, index_file=index_file)

    def createTeleLogs(self):
        teleLogs = pd.read_csv(os.getenv('logsFile'))
        df = BotController.getData(self.inputFile, 'Student List')

        TelegramLogs.createTeleParticipation(teleLogs=teleLogs, df=df)

    def createDashboard(self):
        logs, qna_data, students_data, dummy = Analytics.retrieveData()
        logs_main = Analytics.cleanData(logs_raw=logs, dummy=dummy)
        logs_main = Analytics.match_unmatchFiles(logs_main=logs_main)
        logs_main = Analytics.saveCleanedLogs(logs_main=logs_main)
        logs_main, helpful_df = Analytics.voteFiles(logs_main=logs_main)
        logs_helpful = Analytics.durationFile(logs_main=logs_main, helpful_df=helpful_df)
        logs_helpful = Analytics.corrFile(qna_data=qna_data, logs_helpful=logs_helpful)
        Analytics.pathFile(logs_helpful=logs_helpful)

