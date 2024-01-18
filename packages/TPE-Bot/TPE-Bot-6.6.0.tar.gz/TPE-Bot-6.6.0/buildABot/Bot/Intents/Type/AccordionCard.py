class AccordionCard():
    def accordionPayload():
      return {
          "type": "accordion",
          "title": "Accordion title",
          "subtitle": "",
          "image": {
            "src": {
              "rawUrl": ""
            }
          },
          "text": "Accordion text"
        }
      
    
    def redirectChips(redirect):
      return  {
        "type": "chips",
        "options": [
            {
              "text": "Click here!",
              "link": redirect
            }
          ]
      }
    
    def image():
      return  {
        "type": "image",
        "rawUrl": ""
      }

    def createAccordionCard(title, text, image, redirect):
      accordions = []
    
      # Separate text into lines by number or symbol
      # Create multiple accordion
      lines = text.split('\n\n' or '\n' or '-' or ')')
      for line in lines:
        accordionResponse = AccordionCard.accordionPayload()
        accordionResponse["title"] = title
        accordionResponse["text"] = line
        accordions.append(accordionResponse)

      if(image):
        imagePayload = AccordionCard.image()
        imagePayload['rawUrl'] = image
        accordions.append(imagePayload)

      if(redirect != ''):
        accordions.append(AccordionCard.redirectChips(redirect))

      return accordions