import os
import pandas as pd
import pkgutil

class Webhook_Reco:
    def __init__(self):
        pass

    def get_snapshot_template():
        return ' var CRITERIA = snapshot.child("/TOPICNAME/"+id).val();'

    def get_highlight_template():
        return ' var highlight = "";'

    def get_null_template():
        return ' && criteria{} == null'

    def get_if_template():
        return " if (criteria1 <= THRESHOLD) { flaw +=1; highlight1 = '❗';}"

    def get_results_template():
        return "+ 'CRITERIANAME :' + criteria1 + '\\n' "

    def get_assignment():

        return 'var ASSIGNUM = snapshot.child("/ASSIGNMENTGRADEHERE/"+id).val(); '

    def get_check():

        return 'if(ASSIGNUM == null){agent.add("💡 Reminder: Submit ASSIGNMENTNAMEHERE");} '  

    def get_assignMenu():
        return {'text': 'ASSIGNMENT'}

    def get_assignMenuTele():
        return {'text': 'ASSIGNMENT', 'callback_data': 'ASSIGNMENT'}


    def getFromSLInputs(df, keyFile):
        acc_key = open(keyFile)
        acckey = acc_key.read()

        dbUrl = df['Firebase URL'][0]
        email = df['Tutor Email'][0]
        gcpEmail = df['GCP Account Email'][0]
        gcpAppKey = df['GCP Account App Key'][0]

        return acckey, dbUrl, email, gcpEmail, gcpAppKey
    

    def getAssignments(df):
        assignments = df.Assessment.unique() # Get list of assignments available
        #numOfAssignments = len(assignments) # Get no. of assignments available

        functions = ''
        intentMaps = ''
        
        for a in (assignments):
            assigmmentData = df[df['Assessment'] == a]
            criterias = list(assigmmentData['Criteria'])
            subtopics = list(assigmmentData['Sub Topic'])
            #weightages = list(assigmmentData['Weightage'])
            thresholds = list(assigmmentData['Threshold'])

            menu, intentMap = Webhook_Reco.webhookMenuFunction(a, criterias, subtopics, thresholds)
            
            intentMaps += intentMap
            functions += "\n"
            functions += menu

        return functions, intentMaps
    
    def webhookMenuFunction(a, listOfCriteria, listOfSubtopics, listOfThresholds): 
        assignmentVarName = a.replace(" ", "")
        menu = pkgutil.get_data("buildABot.Data", '/Webhook/ReportCard_Template_RECO.js').decode("utf-8") 

        # PAYLOAD FUNCTIONS
        
        snapshots = ''
        criterias = ''

        ## Function name
        menu = menu.replace('recommendedMenu', '{}Menu'.format(assignmentVarName))
       
        numOfCriteria = len(listOfCriteria)
        for i in range (1, numOfCriteria+1):

            snapshot = Webhook_Reco.get_snapshot_template()

            snapshot = snapshot.replace('CRITERIA', 'criteria{}'.format(i))
            
            snapshot = snapshot.replace('TOPICNAME', listOfCriteria[i-1])

            snapshot = snapshot.strip("'")

            snapshots += snapshot

            criterias+= 'criteria{}, '.format(i)
        
        criterias = criterias[:-2]
        
        menu = menu.replace('CRITERIASHERE', criterias)

        menu = menu.replace("SNAPSHOTHERE", snapshots)
        menu = menu.replace('// TELE SNAPSHOT HERE //', snapshots.replace('id', 'teleID'))

        ## Grade variable
        grade = 'var grade = snapshot.child("/Assignment 1 Grade/"+id).val();'
        grade_tele = 'var grade = snapshot.child("/Assignment 1 Grade/"+teleID).val();'
        menu = menu.replace('// ASSIGNMENT GRADE HERE //', grade.replace('Assignment 1', '{}'.format(a)))
        menu = menu.replace('// TELEASSIGNMENT GRADE HERE //', grade_tele.replace('Assignment 1', '{}'.format(a)))
        
        ## Highlights
        highlights = ''
        for i in range (1, numOfCriteria+1):

            highlight = Webhook_Reco.get_highlight_template()

            highlight = highlight.replace('highlight', 'highlight{}'.format(i))

            highlight = highlight.strip("'")

            highlights += highlight

        menu = menu.replace("HIGHLIGHTHERE", highlights)


        ## Null condition
        nullStrings = ''

        for i in range (2, numOfCriteria+1):

            nullString = Webhook_Reco.get_null_template()

            nullString = nullString.replace('criteria{}', 'criteria{}'.format(i))

            nullStrings += nullString

        menu = menu.replace("NULLHERE", nullStrings)

        
        ## Threshold loop
        ifloops = ''
        for i in range (1, numOfCriteria+1):
            ifloop = Webhook_Reco.get_if_template()

            ifloop = ifloop.replace('criteria1', 'criteria{}'.format(i))

            ifloop = ifloop.replace('THRESHOLD', listOfThresholds[i-1])

            ifloop = ifloop.replace('highlight1', 'highlight{}'.format(i))

            ifloop.strip("'")

            ifloops += ifloop

        menu = menu.replace("IFLOOPHERE", ifloops)

        
        ## Report Card
        menu = menu.replace('ASSIGNMENTGRADEHERE', ' {} Report Card --'.format(a))
        menu = menu.replace('#ASSIGNMENTREPORTCARD', '{}ReportCard'.format(assignmentVarName))
        menu = menu.replace('#AssignmentFeedback', '{} Feedback'.format(a))
        
        ## Recommended Menu - Chips Payload
        payloads = ''
        for i in range (1, numOfCriteria+1):
            payload = "{'text': highlight + 'CRITERIANAME'}, "
            payload = payload.replace('CRITERIANAME', str('[Rubrics] ' + listOfCriteria[i-1]))
            
            highlights = ('highlight' + str(i))
            highlights = highlights.replace(' " ', "")
            
            payload = payload.replace('highlight', highlights)
            payloads += payload
        payloads = payloads[:-2]
        payload_text = '[' + payloads + ']'
        menu = menu.replace('CHIPSPAYLOADHERE', payload_text)

        ## Recommended Menu - Tele Payload
        teleloads = ''
        for i in range(1, numOfCriteria+1):
            teleload = "[{'text': highlight + 'CRITERIANAME', 'callback_data': highlight + 'CRITERIANAME'}],"
            teleload = teleload.replace('CRITERIANAME', str('[Rubrics] ' + listOfCriteria[i-1]))

            highlights = ('highlight' + str(i))
            highlights = highlights.replace(' " ', "")

            teleload = teleload.replace('highlight', highlights)
            teleloads += teleload
            
        teleloads = teleloads[:-1]
        menu = menu.replace('TELEPAYLOADHERE', teleloads)

        ## IntentMap
        intentMap = "intentMap.set('Menu - Recommended - {}', {}Menu);".format(a, assignmentVarName)

        return menu, intentMap
 

    def createWebhookCode(acckey, dbUrl, email, gcpEmail, gcpAppKey, functions, intentMaps, assign_strings, checks, textAssignments, teleAssignments):
        data = pkgutil.get_data("buildABot.Data", '/Webhook/index_template_RECO.js').decode("utf-8") 
        data = data.replace("SERVICEACCOUNTKEYHERE", acckey)
        data = data.replace("DBURLHERE", dbUrl)
        data = data.replace("TUTOREMAILHERE", email)
        data = data.replace('GCP_ACC_EMAIL', gcpEmail)
        data = data.replace('GCP_APP_KEY', gcpAppKey)

        data = data.replace('ASSIGNMENTSFUNCTIONSHERE', functions)
        data = data.replace('INTENTMAPSHERE', intentMaps)

        data = data.replace("ASSIGNMENTSTRINGHERE", assign_strings)  
        data = data.replace("CHECKASSIGNMENTHERE", checks)

        data = data.replace("ASSIGNMENTSCHIPSHERE", str(textAssignments))
        data = data.replace("ASSIGNMENTSTELEHERE", str(teleAssignments))

        return data

    
    def submissionNudge(df):
        assignments = df.Assessment.unique()
        assign_strings, checks = '', ''

        for i in assignments:
            assign_string = Webhook_Reco.get_assignment()
            check_assign = Webhook_Reco.get_check()
            
            assignmentName = i.replace(" ", "")
            assign_string = assign_string.replace('ASSIGNUM', '{}'.format(assignmentName))
            assign_string = assign_string.replace('ASSIGNMENTNAMEHERE', '{}'.format(i))
            assign_string = assign_string.replace('ASSIGNMENTGRADEHERE', '{} Grade'.format(i))
            assign_string = assign_string.strip("'")
            assign_strings += assign_string

            check_assign = check_assign.replace('ASSIGNUM', '{}'.format(assignmentName))
            check_assign = check_assign.replace('ASSIGNMENTNAMEHERE', '{}'.format(i))
            check_assign = check_assign.strip("'")
            checks += check_assign

        ## Assignment Menu
        textAssignments = []
        teleAssignments = []

        for assignment in assignments:
            payload = Webhook_Reco.get_assignMenu()
            payload["text"] = assignment
            textAssignments.append(payload)

            payload_tele = Webhook_Reco.get_assignMenuTele()
            payload_tele["text"] = assignment
            payload_tele["callback_data"] = assignment
            teleAssignments.append(payload_tele)

        return assign_strings, checks, textAssignments, teleAssignments
       

    def createFallback(df, data):
        msg = []
        for index, row in df.iterrows():
            msg.append("@" + row["Telegram ID"] + " do you know the answer?")

       # data = pkgutil.get_data("buildABot.Data", '/Webhook/index_template_RECO.js').decode("utf-8") 
        data = data.replace("#SocialTaggingStrings", str(msg))

        return data


    def writeFile(data):
        final = open(os.getenv('indexJSReco'), 'w', encoding='utf8')
        final.write(data)
        final.close()