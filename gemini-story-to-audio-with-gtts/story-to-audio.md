# Quick example of using Gemini to generate a story and converting it to audio with gtts
In this example were using the quick start code from gemini docs to generate a story about a turtle discoverting physics.

The first step will be to install the necessary libraries.
```console
pip install -q -U google-generativeai
pip install gTTS
````
Then we can use the  <a href= "https://ai.google.dev/gemini-api/docs/quickstart?lang=python"> Gemini quick start code </a> and pass the response to a text to speech engine and save the output.

```python
from gtts import gTTS
import google.generativeai as genai

# Set api key
genai.configure(api_key="YOUR-API-KEY-GOES-HERE")
# Choose model
model = genai.GenerativeModel('gemini-1.5-flash')

# Usr generate_content method to generate text
response = model.generate_content("Write a story about a turtle called Dave discovering physics laws.")

# Pass to gtts engine the respone text
tts = gTTS(text=response.text, lang='en')

# Save the generated speech to an MP3 file
tts.save("Dave-the-turtle.mp3")
````
The story : 

[Dave-the-turtle.webm](https://github.com/ip-repo/guides/assets/123945379/7efe9913-c09e-49c8-98b4-029d3339b1bc)

