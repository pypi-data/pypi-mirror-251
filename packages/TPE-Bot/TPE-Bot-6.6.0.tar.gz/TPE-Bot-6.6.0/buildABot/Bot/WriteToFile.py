import os
import shutil
import json
from dotenv import load_dotenv
load_dotenv('./.env') # Load the environment variables from the .env file

import buildABot
package_dir = os.path.abspath(buildABot.__path__[0])

class WriteToFile():
    def __init__(self) -> None:
        pass

    def write_file_json(path, data):
      with open(path, "w", encoding="utf-8") as jsonfile:
          json.dump(data, jsonfile, indent=4)

    
    """
    Create respective zip files for option selected by user
    """
    def createLearnRestoreZip(self):
        '''
        combine intents into one folder
        '''
        
        src_dir = (package_dir.replace('\\','/')) + os.getenv('defaultLearn')
        
        intent_dir = os.getenv('learnIntents')
        worksheets_dir = os.getenv('wsIntents')
        entity_dir = os.getenv('entity')

        zip_name = os.getenv('restoreLearn')

        files = os.listdir(src_dir)

        '''
        put all intents together
        '''
        shutil.copytree(src_dir, intent_dir, dirs_exist_ok=True)
        shutil.copytree(worksheets_dir, intent_dir, dirs_exist_ok=True)


        '''
        put entities files together
        '''
        data_dir = (package_dir.replace('\\','/')) + os.getenv('defaultEntity')
        folder_name = os.getenv('entity')
        shutil.copytree(data_dir, folder_name, dirs_exist_ok=True)

        shutil.copytree(package_dir.replace('\\','/') + os.getenv('defaultWebhoook'), os.getenv('restoreLearn'), dirs_exist_ok=True)

        '''
        default package json for fulfillment
        '''
        shutil.copyfile(package_dir.replace('\\','/') + os.getenv('defaultWebhoook') + '/package.json', os.getenv('packageJSONLearn'))

        '''
        putting all necessary files to zip for importing to dialogflow
        '''
        shutil.copytree(intent_dir, zip_name+'/intents', dirs_exist_ok=True)
        shutil.copytree(entity_dir, zip_name+'/entities', dirs_exist_ok=True)
        shutil.copyfile(os.getenv('agent'), zip_name+'/agent.json')
        shutil.copyfile(os.getenv('package'), zip_name+'/package.json')

        shutil.make_archive(zip_name, 'zip',zip_name)
        shutil.rmtree(zip_name) 

    def createRecoRestoreZip(self):
        '''
        combine intents into one folder
        '''
        package_dir = os.path.abspath(buildABot.__path__[0])
        src_dir = (package_dir.replace('\\','/')) + os.getenv('defaultReco')
        
        reco_dir = os.getenv('recIntents')
        intent_dir = os.getenv('learnIntents')
        worksheets_dir = os.getenv('wsIntents')

        zip_name = os.getenv('restoreReco')

        files = os.listdir(src_dir)
        '''
        put all intents together
        '''
        shutil.copytree(src_dir, reco_dir, dirs_exist_ok=True)
        shutil.copytree(intent_dir, reco_dir, dirs_exist_ok=True)
        shutil.copytree(worksheets_dir, reco_dir, dirs_exist_ok=True)


        '''
        put entities files together
        '''
        data_dir = (package_dir.replace('\\','/')) + os.getenv('defaultEntity')
        entity_dir = os.getenv('entity')
        shutil.copytree(data_dir, entity_dir, dirs_exist_ok=True)

        '''
        default package json for fulfillment
        '''
        shutil.copyfile(package_dir.replace('\\','/') + os.getenv('defaultWebhoook') + '/package.json', os.getenv('packageJSONReco'))

        '''
        putting all necessary files to zip for importing to dialogflow
        '''
        shutil.copytree(reco_dir, zip_name+'/intents', dirs_exist_ok=True)
        shutil.copytree(entity_dir, zip_name+'/entities', dirs_exist_ok=True)
        shutil.copyfile(os.getenv('agent'), zip_name+'/agent.json')
        shutil.copyfile(os.getenv('package'), zip_name+'/package.json')

        shutil.make_archive(zip_name, 'zip',zip_name)
        shutil.rmtree(zip_name) 

    def createLearnWorksheetZip(self):
        '''
        combine intents into one folder
        '''
        package_dir = os.path.abspath(buildABot.__path__[0])

        dir_name = os.getenv('wsIntents')
        usersays = (package_dir.replace('\\','/')) + os.getenv('defaultWS')
        zip_name = os.getenv('importWS')

        '''
        putting all necessary files to zip for importing to dialogflow
        '''
        shutil.copytree(dir_name, zip_name+'/intents', dirs_exist_ok=True)
        shutil.copytree(usersays, zip_name+'/intents', dirs_exist_ok=True)

        shutil.copyfile(os.getenv('agent'), zip_name+'/agent.json')
        shutil.copyfile(os.getenv('package'), zip_name+'/package.json')

        shutil.make_archive(zip_name, 'zip',zip_name)
        shutil.rmtree(zip_name) 

    def createRecoWorksheetZip(self):
        '''
        combine intents into one folder
        '''
        package_dir = os.path.abspath(buildABot.__path__[0])

        dir_name = os.getenv('wsIntents')
        usersays = (package_dir.replace('\\','/')) + os.getenv('defaultWS')
        zip_name = os.getenv('importRecoWS')

        '''
        putting all necessary files to zip for importing to dialogflow
        '''
        shutil.copytree(dir_name, zip_name+'/intents', dirs_exist_ok=True)
        shutil.copytree(usersays, zip_name+'/intents', dirs_exist_ok=True)

        shutil.copyfile(os.getenv('agent'), zip_name+'/agent.json')
        shutil.copyfile(os.getenv('package'), zip_name+'/package.json')

        shutil.make_archive(zip_name, 'zip',zip_name)
        shutil.rmtree(zip_name) 

    def createIntentZip(self):
        '''
        combine intents into one folder
        '''
        folder_name = os.getenv('learnIntents')
        zip_name = os.getenv('importIntents')

        '''
        putting all necessary files to zip for importing to dialogflow
        '''
        shutil.copytree(folder_name, zip_name+'/intents')
        shutil.copyfile(os.getenv('agent'), zip_name+'/agent.json')
        shutil.copyfile(os.getenv('package'), zip_name+'/package.json')

        shutil.make_archive(zip_name, 'zip',zip_name)
        shutil.rmtree(zip_name) 

    def createEntZip(self):
        package_dir = os.path.abspath(buildABot.__path__[0])
        src_dir = (package_dir.replace('\\','/')) + os.getenv('defaultEntity')
        dir_name = os.getenv('entity')
        zip_name = os.getenv('importEntities')

        '''
        putting all necessary files to zip for importing to dialogflow
        '''
        shutil.copytree(src_dir, dir_name, dirs_exist_ok=True)
        shutil.copytree(dir_name, zip_name+'/entities')
        shutil.copyfile(os.getenv('agent'), zip_name+'/agent.json')
        shutil.copyfile(os.getenv('package'), zip_name+'/package.json')

        shutil.make_archive(zip_name, 'zip',zip_name)
        shutil.rmtree(zip_name) 

    def createRecoZip(self):
        package_dir = os.path.abspath(buildABot.__path__[0])
        '''
        combine intents into one folder
        '''
        folder_name = os.getenv('recIntents')
        reco_default = (package_dir.replace('\\','/')) + os.getenv('defaultReco')
        worksheets = os.getenv('wsIntents')
        worksheets_default = (package_dir.replace('\\','/')) + os.getenv('defaultWS')
        zip_name = os.getenv('importReco')

        '''
        putting all necessary files to zip for importing to dialogflow
        '''
        shutil.copytree(worksheets_default, zip_name+'/intents', dirs_exist_ok=True)
        shutil.copytree(worksheets, zip_name+'/intents', dirs_exist_ok=True)
        shutil.copytree(reco_default, zip_name+'/intents', dirs_exist_ok=True)
        shutil.copytree(folder_name, zip_name+'/intents', dirs_exist_ok=True)
        shutil.copyfile(os.getenv('agent'), zip_name+'/agent.json')
        shutil.copyfile(os.getenv('package'), zip_name+'/package.json')

        shutil.make_archive(zip_name, 'zip',zip_name)
        shutil.rmtree(zip_name) 
        