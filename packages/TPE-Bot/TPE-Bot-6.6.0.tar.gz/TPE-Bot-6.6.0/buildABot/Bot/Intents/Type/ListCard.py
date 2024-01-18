import re

class ListCard():
  def listPayload():
    return [{
      "type": "image",
      "rawUrl": ""
    }]
          #lists  
        

  def list():
    return {
      "type": "list",
      "title": "List item 1 title",
      "subtitle": "List item 1 subtitle",
      "event": {
        "name": "",
        "languageCode": "",
        "parameters": {}
      },
      "link": ""
    }
      
  def listDivider():
    return {
      "type": "divider"
    }
  
  def chips():
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
          "link": "" #reach here
        }
      ]
    }

  def createList(title, text, image, redirect):
    listResponse = ListCard.listPayload()
    listResponse[0]["rawUrl"] = image
    #placeholder = listResponse[1]

    sentences = text.splitlines()
    sentences = [i for i in sentences if i]
    link = redirect.splitlines()
    link = [i for i in link if i]

    for i in range(len(sentences)):
      if(i != ''):
        lists = ListCard.list()
        lists["title"] = sentences[i]
        lists["subtitle"] = title
        if(redirect != ''):
          #lists["link"] = link[i]
          lists["link"] = re.search("(?P<url>https?://[^\s]+)", link[i]).group("url")
        listResponse.append(lists)
        listResponse.append(ListCard.listDivider())
    
    # chipsPayload = ListCard.chips()
    # chipsPayload["options"][0]["link"] = redirect
    # placeholder.append(ListCard.chips())

    return listResponse

    





