import json
import os

from .Type.AccordionCard import AccordionCard
from .Type.InfoCard import InfoCard
from .Type.ListCard import ListCard
from .Type.DescriptionCard import DescriptionCard
from .Type.ImageCard import ImageCard

class CustomResponse(AccordionCard, InfoCard, ListCard, DescriptionCard, ImageCard):

    def __init__(self):
        pass
    
    def getResponse():
        return {
            "type": "4",
            "title": "",
            "payload": {
                "richContent": [
                    
                        #payloads
                ]
            }
        }
    
    def createResponseType(dfTitle, dfImage, dfResponse, dfRedirect, dfLength):
        # Short Response
        # if (dfLength < 30):
        #     if (dfImage != ''):
        #         intentResponse = InfoCard.createInfoCard(dfTitle, dfResponse, dfImage, dfRedirect)
            
        #     else:
        #         intentResponse = DescriptionCard.createDescriptionCard(dfTitle, dfResponse, dfImage, dfRedirect)

        # # Long Responses
        # else: 
        #     # List Handler 
        #     if(dfResponse[0] == '-' or dfResponse[0] == '1'):
        #         intentResponse = ListCard.createList(dfTitle, dfResponse, dfImage, dfRedirect)
                
        #     else:
        #         intentResponse = AccordionCard.createAccordionCard(dfTitle, dfResponse, dfImage, dfRedirect)

        # response = CustomResponse.getResponse()
        # response["payload"]["richContent"].append(intentResponse)
        
        # return response
        if ((dfResponse.find('- ')!= -1) or (dfResponse.find('1.') != -1) or (dfResponse.find('1)') != -1)):
            #intentResponse = ListCard.createList(dfTitle, dfResponse, dfImage, dfRedirect)
            intentResponse = AccordionCard.createAccordionCard(dfTitle, dfResponse, dfImage, dfRedirect)

        else:
            # if(dfResponse.find('<br>')!= -1):
            #     intentResponse = DescriptionCard.createDescriptionCard(dfTitle, dfResponse, dfImage, dfRedirect)
            
            #else:
            intentResponse = InfoCard.createInfoCard(dfTitle, dfResponse, dfImage, dfRedirect)
                #intentResponse = AccordionCard.createAccordionCard(dfTitle, dfResponse, dfImage, dfRedirect)

        response = CustomResponse.getResponse()
        response["payload"]["richContent"].append(intentResponse)
        
        return response
    
    
    def getFeedbackChips():
        return {
            "type": "4",
            "title": "",
            "payload": {
                "richContent": [
                    [
                        {
                            "options": [
                                {
                                    "text": "👍🏼"
                                },
                                {
                                    "text": "👎🏼"
                                }
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

            