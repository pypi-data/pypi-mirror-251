class InfoCard():
  def infoCardPayload():
    return [
      {
        "type": "image",
        "rawUrl": ""
      },
      {
            "type": "info",
            "title": "Info item title",
            "subtitle": "Info item subtitle",
            "image": {
              "src": {
                "rawUrl": "https://firebasestorage.googleapis.com/v0/b/almgtbot.appspot.com/o/agenticon.png?alt=media&token=acfb8428-4e7e-4225-99dd-c4ec989530dc"
              }
            },
            "actionLink": ""
          }
    ]
  
  def redirChips(redirect):
    return {
      "type": "chips",
      "options": [
        {
          "text": "Click here!",
          "image": {
            "src": {
              "rawUrl": ""
            }
          },
          "link": redirect
        }
      ]
    }

  def createInfoCard(title, text, image, redirect):
    infoResponse = InfoCard.infoCardPayload()

    infoResponse[0]["rawUrl"] = image

    infoResponse[1]["title"] = title
    infoResponse[1]["subtitle"] = text
    
    if (redirect):
      infoResponse.append(InfoCard.redirChips(redirect))
    
    return infoResponse