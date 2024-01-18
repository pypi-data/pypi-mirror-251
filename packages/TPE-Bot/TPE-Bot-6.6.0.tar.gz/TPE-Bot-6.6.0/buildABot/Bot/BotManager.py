import pandas as pd
import os
import datetime
import buildABot
from buildABot.Bot.BotController import BotController
from .WriteToFile import WriteToFile

class BotManager(BotController):
    def __init__(self, inputFile, resultFile, keyFile):
        # self.qaFile = qaFile
        # self.slFile = slFile
        # self.studentFile = studentFile
        self.inputFile = inputFile
        self.resultFile = resultFile
        self.keyFile = keyFile

    """
    Respective function handler for different purpose
    """
    def createLearnChatbot(self):
        print("Execution started @ ", datetime.datetime.now())
        # Clear files before execution
        dir = os.getenv('learnIntents')
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
            
        BotController.createParaphrases(self)
        BotController.createCustomIntents(self)
        BotController.createLearnMenu(self)
        BotController.createSocialTag(self)
        BotController.createLearnWorksheets(self)
        BotController.createEntities(self)
        BotController.createLearnWebhook(self)
        print()
        print("Dialogflow files done... Next up: Firebase\n")

        BotController.createLearnFirebase(self)
        print("Firebase files done... Next up: WebApp\n")

        BotController.createLearnWebapp(self)
        print("WebApp files done... Next up: Prepare all files for deployment\n")

        WriteToFile.createLearnRestoreZip(self)
        print("Chatbot ready for deployment!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())

    def createLearnAndRecoChatbot(self):
        print("Execution started @ ", datetime.datetime.now())
         # Clear files before execution
        dir = os.getenv('recIntents')
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
            
        BotController.createParaphrases(self)
        BotController.createCustomIntents(self)
        BotController.createLearnMenu(self)
        BotController.createRecoMenu(self)
        BotController.createSocialTag(self)
        #BotController.createPwIntent(self)
        BotController.createRecoWorksheets(self)
        BotController.createEntities(self)
        BotController.createRecoWebhook(self)
        print("Dialogflow files done... Next up: Firebase\n")

        BotController.createRecoFirebase(self)
        print("Firebase files done... Next up: WebApp\n")

        BotController.createRecoWebApp(self)
        print("WebApp files done... Next up: Prepare all files for deployment\n")

        WriteToFile.createRecoRestoreZip(self)
        print("Chatbot ready for deployment!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())


    def updateLearnIntents(self):
        print("Execution started @ \n", datetime.datetime.now())

        # Clear files before execution
        dir = os.getenv('learnIntents')
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        BotController.createParaphrases(self)
        BotController.createCustomIntents(self)
        BotController.createLearnMenu(self)
        BotController.createLearnWorksheets(self)
        print("New Intents Created...\n")

        WriteToFile.createIntentZip(self)
        print("Chatbot ready for update!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())
    
    def updateRecoIntents(self):
        print("Execution started @ \n", datetime.datetime.now())

        # Clear files before execution
        dir = os.getenv('learnIntents')
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        BotController.createParaphrases(self)
        BotController.createCustomIntents(self)
        BotController.createLearnMenu(self)
        BotController.createRecoMenu(self)
        BotController.createRecoWorksheets(self)
        print("New Intents Created...\n")

        WriteToFile.createIntentZip(self)
        print("Chatbot ready for update!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())


    def updateLearnLatestWorksheets(self):
        print("Execution started @ \n", datetime.datetime.now())
        BotController.createLearnWorksheets(self)
        print("Latest Worksheets Added...\n")

        WriteToFile.createLearnWorksheetZip(self)
        print("Chatbot ready for update!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())

    def updateRecoLatestWorksheets(self):
        print("Execution started @ \n", datetime.datetime.now())
        BotController.createRecoWorksheets(self)
        print("Latest Worksheets Added...\n")

        WriteToFile.createRecoWorksheetZip(self)
        print("Chatbot ready for update!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())


    def addNewResults(self):
        print("Execution started @ \n", datetime.datetime.now())
        # Clear files before execution
        dir = os.getenv('recIntents')
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        BotController.createRecoMenu(self)
        BotController.createRecoWorksheets(self)
        BotController.createSocialTag(self)
        BotController.createRecoWebhook(self)
        BotController.createRecoFirebase(self)
        BotController.createRecoWebApp(self)
        print("Latest Results Added...\n")

        WriteToFile.createRecoZip(self)
        print("Chatbot ready for update!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())


    def updateLearnEntities(self):
        print("Execution started @ \n", datetime.datetime.now())
        BotController.createSocialTag(self)
        BotController.createEntities(self)
        BotController.createLearnFirebase(self)
        print("New Entities Created...\n")

        WriteToFile.createEntZip(self)
        print("Chatbot ready for update!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())

    def updateRecoEntities(self):
        print("Execution started @ \n", datetime.datetime.now())
        BotController.createSocialTag(self)
        BotController.createEntities(self)
        BotController.createRecoFirebase(self)
        print("New Entities Created...\n")

        WriteToFile.createEntZip(self)
        print("Chatbot ready for update!\n")
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())


    def createAnalytics(self):
        print("Execution started @ \n", datetime.datetime.now())
        print("Please make sure the downloaded logs files are in the Analytics/Data folder, named as 'Logs.csv'.\n")
        input("If you have done so, press enter to continue...\n")

        BotController.createTeleLogs(self)
        print("Telebot Logs created!\n")
        print("Creating dashboard data now, please wait...\n")
        BotController.createDashboard(self)
        print("Dashboard Data created!\n")
        
        print("Execution done, exiting...\n")
        print("Execution Ended @ ", datetime.datetime.now())
    