import json
import os

class Usersays():
    def write_file_json(QA_Data, data):
      with open(QA_Data, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=4)
 
    def getTrainingPhrases():
      return {
        "id": "",
        "data": [
        {
            "text": "", #Q{} Training phrase
            "userDefined": False
        }
        ],
        "isTemplate": False,
        "count": 0,
        "updated": 0
    }
 
    def createUserSays(df):
        '''
        Training Phrases for each intent
        '''
        for index, rows in df.iterrows():
            trainingPhrase = Usersays.getTrainingPhrases()
            trainingPhrases = []

            intentName = str(rows['Main Label']) + '.' + str(rows['Intent Label']) + ' ' + rows['Main Topic'] + ' - ' + rows['Name']
            intentName = intentName.strip()
            if(len(intentName) > 100):
                intentName = intentName[:100]

            # Base case - intent name
            trainingPhrase["data"][0]["text"] = rows['Name']
            trainingPhrases.append(trainingPhrase)

            questions = (rows.filter(like="Q")).to_frame().transpose()
            
            # Get all Questions from QAfile as training phrases and put it into placeholder
            for i in range(1, len(questions.columns)+1):
                trainingPhrase = Usersays.getTrainingPhrases()
                trainingPhrase.pop("id", None)
                question_key = "Q{}".format(str(i)) # Seach for Questions columns

                if str(rows[question_key]).strip() != "":
                    trainingPhrase["data"][0]["text"] = str(rows[question_key])
                    trainingPhrases.append(trainingPhrase)  
                    
            Usersays.write_file_json(os.getenv('intentsUsersays').format(intentName[:80]), trainingPhrases)
    
    '''
    Learn & Explore
    '''
    def createMenuUserSays():
       defaultPhrases = ['See Topics', 'Learn', 'Learn Menu', 'Back to Learn Menu', "↩ Back to Learn Menu", "Learn & Explore", 'Go to Learn Menu']
       trainingIntent = []
       for phrase in defaultPhrases:
        
        trainingPayload = Usersays.getTrainingPhrases()
        trainingPayload["data"][0]["text"] = phrase
        trainingIntent.append(trainingPayload)

        Usersays.write_file_json(os.getenv('learnMenuUsersays'), trainingIntent)

    def createSubMenuUserSays(mainTopic):
        defaultPhrases =[mainTopic, 'Back to {}'.format(mainTopic)]
        trainingIntent = []

        for phrase in defaultPhrases:
            trainingPayload = Usersays.getTrainingPhrases()
            trainingPayload["data"][0]["text"] = phrase
            trainingIntent.append(trainingPayload)

        Usersays.write_file_json(os.getenv('intentsUsersays').format(mainTopic), trainingIntent)

    def createIntentsUserSays(mainTopic, SubTopic):
        if(SubTopic == ''):
            defaultPhrases =[mainTopic, 'Back to {}'.format(mainTopic)]
            trainingIntent = []

            for phrase in defaultPhrases:
                trainingPayload = Usersays.getTrainingPhrases()
                trainingPayload["data"][0]["text"] = phrase
                trainingIntent.append(trainingPayload)

            Usersays.write_file_json(os.getenv('intentsUsersays').format(mainTopic), trainingIntent)

        else:
            defaultPhrases =[SubTopic, 'Back to {}'.format(SubTopic)]
            trainingIntent = []

            for phrase in defaultPhrases:
                trainingPayload = Usersays.getTrainingPhrases()
                trainingPayload["data"][0]["text"] = phrase
                trainingIntent.append(trainingPayload)

            Usersays.write_file_json(os.getenv('intentsTopicUsersays').format(mainTopic, SubTopic), trainingIntent)


    def createCustomUserSays(string, fileName):
       trainingPayload = Usersays.getTrainingPhrases()
       trainingIntent = []
       trainingPayload["data"][0]["text"] = string
       trainingIntent.append(trainingPayload)
       Usersays.write_file_json(fileName, trainingIntent)


    '''
    Results & Recommendations
    '''
    def createRecoUserSays(assignmentNum, criteria, name):
        defaultPhrases =['[Rubrics] {} '.format(criteria)]
        trainingIntent = []

        for phrase in defaultPhrases:
            trainingPayload = Usersays.getTrainingPhrases()
            trainingPayload["data"][0]["text"] = phrase
            trainingIntent.append(trainingPayload)

        Usersays.write_file_json(os.getenv('intentsRecommendedUsersays').format(name), trainingIntent)

    def createRecoMenuUserSays():
       defaultPhrases = ['Recommended Menu', 'back to recommended menu']
       trainingIntent = []
       for phrase in defaultPhrases:
        
        trainingPayload = Usersays.getTrainingPhrases()
        trainingPayload["data"][0]["text"] = phrase
        trainingIntent.append(trainingPayload)

        Usersays.write_file_json(os.getenv('intentsRecoUsersays'), trainingIntent)

    def createResultsMenuUserSays():
       defaultPhrases = ['Results & Recommendations', 'results', ' recommendations', 'report card']
       trainingIntent = []
       for phrase in defaultPhrases:
        
        trainingPayload = Usersays.getTrainingPhrases()
        trainingPayload["data"][0]["text"] = phrase
        trainingIntent.append(trainingPayload)

        Usersays.write_file_json(os.getenv('intentsLoginResultsUsersays'), trainingIntent)
