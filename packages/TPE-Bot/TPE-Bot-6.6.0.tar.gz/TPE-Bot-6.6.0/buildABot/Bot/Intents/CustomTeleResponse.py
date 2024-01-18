import os

class CustomTeleResponse():
    def __init__(self) -> None:
        pass
    
    def getTeleResponse():
        return {
            "type": "1",
            "platform": "telegram",
            "imageUrl": "", #image
            "subtitle": "", #repsonse
            "title": "", #name
            "buttons": [],
            "textToSpeech": "",
            "lang": "en",
            "condition": ""
        }
    
    def getButton(redirect):
        return {
            "postback": redirect, #redirect
            "text": "Click here!"
        }
    
    def getTeleMenuKeyboard():
        return {
            "type": "4",
            "platform": "telegram",
            "title": "",
            "payload": {
                "telegram": {
                    "reply_markup": {
                        "keyboard": [
                            # texts
                        ]
                    },
                    "text": "Pick a topic:"
                }
            },
            "textToSpeech": "",
            "lang": "en",
            "condition": ""
        }
    
    def getTexts(text):
        return [
            {
                "text": "{}".format(text),
                "callback_data": "{}".format(text)
            }
        ]
    
    def getFeedback():
        return {
            "type": "1",
            "platform": "telegram",
            "title": "Did you find our answers helpful?",
            "buttons": [
                {
                    "text": "👍",
                    "callback_data": "👍"
                },
                {
                    "text": "👎",
                    "callback_data": "👎"
                }
            ],
            "textToSpeech": "",
            "lang": "en",
            "condition": ""
        }
    
    def getTeleKeyboard():
        return {
            "type": "4",
            "platform": "telegram",
            "title": "",
            "payload": {
                "telegram": {
                    "reply_markup": {
                        "keyboard": [
                            [
                            {
                                "text": "Back to {} Menu", #Back to Topic Menu
                                "callback_data": "Back to {} Menu"
                            }
                            ],
                            [
                            {
                                "callback_data": "Back to Main Menu",
                                "text": "Back to Main Menu"
                            }
                            ]
                        ]
                    },
                    "text": ""
                }
            },
            "textToSpeech": "",
            "lang": "en",
            "condition": ""
        }

    def createTeleRepsonse(dfTitle, dfImage, dfResponse, dfRedirect):
        telePayload = CustomTeleResponse.getTeleResponse()
        telePayload["title"] = dfTitle
        telePayload["subtitle"] = dfResponse
        telePayload["imageUrl"] = dfImage
        if(dfRedirect):
            telePayload["buttons"].append(CustomTeleResponse.getButton(dfRedirect))

        return telePayload

    def createFeedbackQuickReplies():
        return CustomTeleResponse.getFeedback()
    
    def createTeleKeyboard(dfMainTopic):
        teleKeyboard = CustomTeleResponse.getTeleKeyboard()
        teleKeyboard["payload"]["telegram"]["reply_markup"]["keyboard"][0][0]["text"] = "Back to {} Menu".format(dfMainTopic)
        teleKeyboard["payload"]["telegram"]["reply_markup"]["keyboard"][0][0]["callback_data"] = "Back to {} Menu".format(dfMainTopic)

        return teleKeyboard
