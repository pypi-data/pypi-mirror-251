import pandas as pd

class RelatedIntents():
    def getYouMayAlsoLikeWeb():
        """
            Dialogflow's text template for "You may also like:"
            :return: JSON of text response of "you may also like"
        """
        return {
                "type": "0",
                "title": "",
                "textToSpeech": "",
                "lang": "en",
                "speech": [
                "👇🏼 You may also like:"  
                ],
                "condition": ""
        }
    
    def getRelatedIntentsWeb():
        """
        Dialogflow's chips template for related intents to be recommended to user
        :return: JSON of chips response consisting all related intents
        """
        return {
        "type": "4",
        "title": "",
        "payload": {
            "richContent": [
                [
                    {
                        "options": [ # top neighbour intent button payload here ["payload"]["richContent"][0][0]
                        ],
                        "type": "chips"
                    }
                ]
            ]
        },
        "textToSpeech": "",
        "lang": "en",
        "condition": ""
        }

    def getRelatedIntentName():
        """
            Dialogflow's text template as placeholder for related intent's name
            :return: JSON of text response consisting all related intent's Q1 as name
        """
        return {
        "text": ""  # Intent Q1 as text
        }
    
    def getRelatedIntentsTele(relatedArray):
        """
        Dialogflow's chips template for related intents to be recommended to user
        :return: JSON of chips response consisting all related intents
        """
        return {
          "type": "4",
          "platform": "telegram",
          "title": "",
          "payload": {
            "telegram": {
              "text": "👇🏼 You may also like:",
              "reply_markup": {
                "inline_keyboard": relatedArray
              }
            }
          }
        }
    
    def getTeleButtons(names):
        return [
            {
            "text": names,
            "callback_data": names
          }
        ]
    
    def createRelatedTextWeb():
        return RelatedIntents.getYouMayAlsoLikeWeb()  # Add in 'You may also like'
        
        
    def createRelatedPayload(relatedIntent, df2):
        relatedArray = []
        recResponseWeb = RelatedIntents.getRelatedIntentsWeb()
        # recResponseTele = RelatedIntents.getRelatedIntentsTele()

        for i in range(1, len(relatedIntent.columns)+1):
            recIntentNames = RelatedIntents.getRelatedIntentName()

            intent_key = "Related Intent {}".format(str(i)) # Search for related intent's columns
            pd.set_option("display.max_colwidth", None) # Settings to show full text for chips
            
            if(relatedIntent[intent_key].item()):
                related = df2[df2['S/N'] == relatedIntent[intent_key].item()]
                related_str = related['Q1'].to_string(index=False) #Get related intent's Q1 as display text for chips

                # Pull data into the text payload and append to list
                recIntentNames["text"] = related_str
                
                #recIntentNames_copy = recIntentNames.copy()
                recResponseWeb["payload"]["richContent"][0][0]["options"].append(recIntentNames)

                relatedArray.append(RelatedIntents.getTeleButtons(related_str))
    
        recResponseTele = RelatedIntents.getRelatedIntentsTele(relatedArray)
        
        return recResponseWeb, recResponseTele
    




