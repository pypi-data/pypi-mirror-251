class Chips():
  def chipsPayload():
    return [
      {
        "type": "chips",
        "options": [ #chips option
        ]
      }
    ]

  def chipsOption():
    return{
      "text": "Chip 1",
      "image": {
        "src": {
          "rawUrl": ""
        }
      },
      "link": "https://example.com"
    }

  def createOptions(text, redirect):
    options = Chips.chipsOption()
    options["text"] = text
    options["link"] = redirect

    return options
  
  def createChips(options):
    chipsResponse = Chips.chipsPayload()

    chipsResponse["richContent"][0][0]["options"] = options

    return chipsResponse



  def getReturnChipsPayload():
    return {
            "type": "4",
            "title": "",
            "payload": {
                "richContent": [[
                    {
                        "options": [
                            #ReturnChips
                        ],
                        "type": "chips"
                    }
                ]]
            },
            "textToSpeech": "",
            "lang": "en",
            "condition": ""
        }
    
  def getReturnSubChips(subTopic):
      return {
          "text": "Back to " + subTopic, #Back to ['Sub Topic']
          "image": {
              "src": {
                  "rawUrl": "https://firebasestorage.googleapis.com/v0/b/almgtbot.appspot.com/o/left-arrow-curved-black-symbol.png?alt=media&token=f0225665-02e7-459f-b8e9-1c19618a7234"
              }
          }
      }
  
  def getReturnMainChips():
      return {
          "text": "Back to Main Menu",
          "image": {
              "src": 
              {
                  "rawUrl": "https://firebasestorage.googleapis.com/v0/b/almgtbot.appspot.com/o/home%20(1).png?alt=media&token=c8b0db13-9aeb-48ab-ad44-6134a55049e2"
              }
          }
      }

  def getReturnRecommendedChips():
    return {
        "text": "Back to Recommended Menu",
        "image": {
            "src": {
                "rawUrl": "https://firebasestorage.googleapis.com/v0/b/almgtbot.appspot.com/o/left-arrow-curved-black-symbol.png?alt=media&token=f0225665-02e7-459f-b8e9-1c19618a7234"
            }
        }
    }