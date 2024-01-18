class ButtonCard():
  def buttonPayload():
    return {
      "type": "button",
      "icon": {
        "type": "chevron_right"
      },
      "text": "Button text",
      "link": "https://example.com",
      "event": {
        "name": "",
        "languageCode": "en",
        "parameters": {}
      }
    }
  
        

  def createButtonCard(text, event, redirect):
    buttonResponse = ButtonCard.buttonPayload()
    buttonResponse["text"] = text
    buttonResponse["link"] = redirect
    buttonResponse["event"]["name"] = event
    
    return buttonResponse