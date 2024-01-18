class DescriptionCard():
  def descriptionPayload():
    return [
          {
            "type": "image",
            "rawUrl": ""
          },
          {
            "type": "description",
            "title": "Description title",
            "text": [
              "This is text line 1.",
              "This is text line 2."
            ]
          },
          {
            "type": "chips",
            "options": [
              {
                "text": "Click here!",
                "image": {
                  "src": {
                    "rawUrl": ""
                  }
                },
                "link": "" #reach here
              }
            ]
          }
        ]

  def createDescriptionCard(title, text, image, redirect):
    descriptionResponse = DescriptionCard.descriptionPayload()

    descriptionResponse[0]["rawUrl"] = image
    
    descriptionResponse[1]["title"] = title
    sentences = text.split('<br>')
    descriptionResponse[1]["text"] = sentences

    descriptionResponse[2]["options"][0]["link"] = redirect

    return descriptionResponse
  
