import os
directory = os.getcwd()
parent = os.path.dirname(directory).replace('\\','/')
import pkgutil

class WebApp_Learn:
    def __init__(self):
        import pandas as pd

    def readFiles():
        template = pkgutil.get_data("buildABot.Data", 'WebApp/index_template_Learn.html').decode("utf-8") 
        # tempFile = open('./Data/index_template.html', "r")
        # data = tempFile.read()
        return str(template)
    
    def getInfo(df, data):
        subject = df['Subject'][0]
        agentID = df['Agent ID'][0]

        data = data.replace("SUBJECTNAME", subject)
        data = data.replace("#AGENT-ID", agentID)

        return data

    def dfMessengerfontSizeCustomisation(df, data):
        persona = df['Persona'][0]
        data = data.replace("BOTNAME", persona)

        fontSize = df['Font Size'][0]
        if(fontSize == '1'):
            fontSz = '12px'
        elif(fontSize == '2'):
            fontSz = '14px'
        elif(fontSize == '3'):
            fontSz = '16px'
        else:
            fontSz = '14px'

        data = data.replace('#FONTSIZE' , fontSz)
        
        return data
    
    def dfMessengerFontCustomisation(df, data):
        font = df['Font'][0]
        if(font == '1'):
            fontFamily = 'Roboto'
        elif(font == '2'):
            fontFamily = 'Roboto Slab'
        elif(font == '3'):
            fontFamily = 'Montserrat'
        elif(font == '4'):
            fontFamily = 'Serif'
        else:
            fontFamily = ''
        
        data = data.replace('#FONTFAMILY' , fontFamily)

        return data

    def dfMessengerSchemeCustomisation(df, data):
        scheme = df['Scheme'][0]
        customisation = {
                'buttonColour': '',
                'buttonHover': '',
                'titlebarColour': '',
                'chatBackgroundColour': '',
                'fontColour': '',
                'userMessageColour': '',
                'botMessageColour': '',
                'chipColour': ''
            }
        
        if(scheme == '1'):
            customisation['buttonColour'] = '#c79a96'
            customisation['buttonHover'] = '#dfc1b8'
            customisation['titlebarColour'] = '#808274'
            customisation['chatBackgroundColour'] = 'white'
            customisation['fontColour'] = 'white'
            customisation['userMessageColour'] = '#c79a96'
            customisation['botMessageColour'] = '#808274'
            customisation['chipColour'] = '#b7b4a2'
            
        elif(scheme == '2'):
            customisation['buttonColour'] = '#b8c9c3'
            customisation['buttonHover'] = '#668991'
            customisation['titlebarColour'] = '#668991'
            customisation['chatBackgroundColour'] = '#668991'
            customisation['fontColour'] = 'black'
            customisation['userMessageColour'] = '#88a6c1'
            customisation['botMessageColour'] = 'white'
            customisation['chipColour'] = '#bdd1d2'

        elif(scheme == '3'):
            customisation['buttonColour'] = '#ca7d48'
            customisation['buttonHover'] = '#ca9964'
            customisation['titlebarColour'] = '#b7a27f'
            customisation['chatBackgroundColour'] = 'white'
            customisation['fontColour'] = 'white'
            customisation['userMessageColor'] = '#ca9964'
            customisation['botMessageColour'] = '#678a9e'
            customisation['chipColor'] = '#949c97'

        elif(scheme == '4'):
            customisation['buttonColor'] = '#94b5b8'
            customisation['buttonHover'] = '#286e83'
            customisation['titlebarColour'] = '#7f886c'
            customisation['chatBackgroundColour'] = 'white'
            customisation['fontColour'] = 'white'
            customisation['userMessageColour'] = '#d8cfb1'
            customisation['botMessageColour'] = '#286e83'
            customisation['chipColour'] = '#94b5b8'

        elif(scheme == '5'):
            customisation['buttonColour'] = '#94b5b8'
            customisation['buttonHover'] = '#286e83'
            customisation['titlebarColour'] = '#7f886c'
            customisation['chatBackgroundColour'] = '#7f886c'
            customisation['fontColour'] = 'black'
            customisation['userMessageColour'] = '#94b5b8'
            customisation['botMessageColour'] = 'white'
            customisation['chipColour'] = '#d8cfb1'
        
        else:
            customisation['titlebarColour'] = '#607D86'
            customisation['chatBackgroundColour'] = 'white'
            customisation['fontColour'] = 'white'
            customisation['userMessageColour'] = '#607D86'
            customisation['botMessageColour'] = '#696969'
            customisation['chipColour'] = 'lightgray'
        
        data = data.replace('titlebarColour' , customisation['titlebarColour'])
        data = data.replace('chatBackgroundColour' , customisation['chatBackgroundColour'])
        data = data.replace('fontColour' , customisation['fontColour'])
        data = data.replace('userMessageColour' , customisation['userMessageColour'])
        data = data.replace('botMessageColour' , customisation['botMessageColour'])
        data = data.replace('chipColour' , customisation['chipColour'])

        return data

    def createHTML(data):
        htmlFile = open(os.getenv('indexHTML'), 'w')
        htmlFile.write(data)
        htmlFile.close()