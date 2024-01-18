import pkgutil
import buildABot
import os
from ..Intents.FallbackSocialTag import FallbackSocialTag

class Webhook_Learn:
    def __init__(self):
        pass

    def readFiles(keyFile):
        '''
        Read csv and template files
        :param slFile
        :return:
        '''
        accKeyFile = open(keyFile)

        package_dir = os.path.abspath(buildABot.__path__[0])
        src_dir = (package_dir.replace('\\','/')) + '/Data/Webhook/index_template_LEARN.js'
        template = open(src_dir, 'r', encoding="utf-8").read()
        #template = pkgutil.get_data("buildABot.Data.Webhook", 'Webhook/index_template_LEARN.js').decode("utf-8") 

        return accKeyFile, template

    def get_assignment():

        return 'var ASSIGNUM = snapshot.child("/ASSIGNMENTNAMEHERE/"+id).val(); '

    def get_check():

        return 'if(ASSIGNUM == 0){agent.add("💡 Reminder: Submit ASSIGNMENTNAMEHERE");} '  

    def getInfo(slData, accKeyFile, template):
        '''
        Get necessary data from csv files (service account key, firebase url, email)
        '''
        accKey = accKeyFile.read()
        dbURL = slData['Firebase URL'][0]
        slEmail = slData['Tutor Email'][0]
        gcpEmail = slData['GCP Account Email'][0]
        gcpAppKey = slData['GCP Account App Key'][0]

        '''
        Replace keywords with extracted values
        '''
        template = template.replace("SERVICEACCOUNTKEYHERE", accKey)
        template = template.replace("DBURLHERE", dbURL)
        template = template.replace("TUTOREMAILHERE", slEmail)

        template = template.replace('GCP_ACC_EMAIL', gcpEmail)
        template = template.replace('GCP_APP_KEY', gcpAppKey)

        return template
    
    def assignmentNudge(df, template):
        ## Assignment Check
        df.drop('Class', axis='columns', inplace=True)
        df.drop('Name', axis='columns', inplace=True)
        df.drop('Full Admin Number', axis='columns', inplace=True)
        df.drop('Telegram ID', axis='columns', inplace=True)
        
        assignments = list(df)
        noOfAssignments = len(assignments)
        assign_strings, checks = '', ''

        for i in range(1, noOfAssignments+1):
            assign_string = Webhook_Learn.get_assignment()
            check_assign = Webhook_Learn.get_check()
            
            assign_string = assign_string.replace('ASSIGNUM', 'assignment{}'.format(i))
            assign_string = assign_string.replace('ASSIGNMENTNAMEHERE', assignments[i-1])
            assign_string = assign_string.strip("'")
            assign_strings += assign_string

            check_assign = check_assign.replace('ASSIGNUM', 'assignment{}'.format(i))
            check_assign = check_assign.replace('ASSIGNMENTNAMEHERE', assignments[i-1])
            check_assign = check_assign.strip("'")
            checks += check_assign

        template = template.replace("ASSIGNMENTSTRINGHERE", assign_strings)  
        template = template.replace("CHECKASSIGNMENTHERE", checks)

        return template
    
    def getSocialTaggingStrings(template, dfStudents):
        socialTags = FallbackSocialTag.createSocialTagStrings(df=dfStudents)
        template = template.replace("#SocialTaggingStrings", str(socialTags))
        
        return template

    def createFulfillment(template):
        '''
        Write updated fulfillment code into destinated files and close files
        '''
        tutorFile = open(os.getenv('indexJSLearn'), 'w', encoding="utf-8")
        tutorFile.write(template)
        tutorFile.close()