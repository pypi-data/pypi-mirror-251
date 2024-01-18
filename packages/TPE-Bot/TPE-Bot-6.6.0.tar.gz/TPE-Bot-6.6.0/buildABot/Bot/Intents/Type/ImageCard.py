class ImageCard():
    def imageCardPayload():
      return {
        "type": "image",
        "rawUrl": ""
      }

    def createImageCard(imageURL):
      imageResponse = ImageCard.imageCardPayload()
      imageResponse['rawUrl'] = imageURL

      return imageResponse
  

