# Example: Using gemini to generate a conversation text and by using bark creating a audio version from the text
So in this example were going to create a conversation between a woman and a man on the Big-Bang.

To generate the conversation text we will use gemini and to create the conversation audio we will use <a href="https://github.com/suno-ai/bark">bark transformer-based text-to-audio model</a>.

The part in the code realted to bark come's from there long audio examples which you can find if you <a href="https://github.com/suno-ai/bark/blob/main/notebooks/long_form_generation.ipynb">click here.</a>

Dependencies:
```console
pip install -q -U google-generativeai
pip install git+https://github.com/suno-ai/bark.git
```


```python
import google.generativeai as genai
import numpy as np
import scipy
from bark import SAMPLE_RATE, generate_audio, preload_models
from IPython.display import Audio

from bark.generation import (
    generate_text_semantic,
    preload_models,
)
from bark.api import semantic_to_waveform
from bark import generate_audio, SAMPLE_RATE

preload_models()

# Generate text with gemini
genai.configure(api_key="YOUR-API-KEY")
model = genai.GenerativeModel('gemini-1.5-flash')
prompt = """Write a conversation between a man and a woman about the big bang, the women is an expert cosmologist and the man do not know anything about that subject.
include scientific explanation and also pre-big bang theories. for the conversation format make sure to use the next format=> WOMAN: something, MAN:something.
"""
response = model.generate_content(prompt)
script = response.text

# Define speakers voices 
speaker_lookup = {"WOMAN": "v2/en_speaker_9", "MAN": "v2/en_speaker_2"}
# Format the text
script = script.strip().split("\n")
script = [s.strip() for s in script if s]

# Generate audio with bark by creating audio for each speaker
pieces = []
# Create silence to add for each line
silence = np.zeros(int(0.5*SAMPLE_RATE))
for line in script:
    # Seprate speaker and what he say
    speaker, text = line.split(": ")
    # Genrate audio for the current speaker
    audio_array = generate_audio(text, history_prompt=speaker_lookup[speaker], )
    # Append generated audio with slience
    pieces += [audio_array, silence.copy()]
# listen to the audio in a notebook
#Audio(np.concatenate(pieces), rate=SAMPLE_RATE) 
# save the audio as a wav file
scipy.io.wavfile.write("conversation", rate=SAMPLE_RATE, data=np.concatenate(pieces))


```
[conversation.webm](https://github.com/ip-repo/guides/assets/123945379/a16a994b-9553-4ad7-bb3a-da2f51b8a338)
