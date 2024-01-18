"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"
import pandas as pd
import os
import datetime

from buildABot.QA.DataBank import DataBank
from buildABot.QA.Responses import Responses
from buildABot.QA.Para import Para

class QAManager(DataBank, Responses):
    def __init__(self, qaFile, apiKey):
        self.qaFile = qaFile
        self.apiKey = apiKey

    def getData(file):
        """
        Read QAfile and clean the file before using
        :param file: QA_data.xlsx, SL Inputs.xlsx
        :return: [Dataframe] Cleaned file as dataframe
        """
        # Get QAfile and read as dataframe
        df = pd.read_excel(file, dtype=str)
        df.fillna(value='', inplace=True)
        return df
    
    def genPara(self):
        df = QAManager.getData(self.qaFile)
        result = Para.genPara(df=df, api_key=self.apiKey)
        result.to_excel(os.getenv('qaFile'), index=False)

    def genQA(self):
        df = QAManager.getData(self.qaFile)
        mainTopics, subTopics, intentNames, q1s, responses = DataBank.getContent(api_key=self.apiKey)
        qa = DataBank.extractNLoad(qaFile=df,
                        mainTopics=mainTopics, subTopics=subTopics, 
                        intentNames=intentNames, 
                        q1s=q1s, responses=responses)
        qa.to_excel(os.getenv('qaFile'), index=False)
        
    def genResp(self):
        df = QAManager.getData(self.qaFile)
        resp = Responses.createResp(df=df, api_Key=self.apiKey)
        resp.to_excel(os.getenv('qaFile'), index=False)


    def createQA(self):
        print("Execution started @ ", datetime.datetime.now())

        QAManager.genQA(self)
        print("Generating Training Phrases...\n")
        QAManager.genPara(self)

        print("QA and Training Phrases Generated!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())
    
    def createResponse(self):
        print("Execution started @ ", datetime.datetime.now())

        QAManager.genResp(self)
        QAManager.genPara(self)

        print("Responses and Training Phrases Generated!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())
    
