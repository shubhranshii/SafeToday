# import base64
# from senti_model import extract_features
# from fastapi import FastAPI,File,UploadFile
# from fastapi import Form
# from pydantic import BaseModel
# from typing import List
# import re
# import speech_recognition as sr
# from pydub import AudioSegment
# app = FastAPI()

# r = sr.Recognizer()


# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# @app.post("/check")
# async def isInDanger(myfile: bytes = File(...), keywords: List[str] = Form(...)):
#     # Decode the file and convert to wav
#     data = base64.b64encode(myfile)
#     mp3_file = open("temp.mp3", "wb")
#     decode_string = base64.b64decode(data)
#     mp3_file.write(decode_string)
#     sound = AudioSegment.from_file("temp.mp3")
#     sound.export("temp.wav", format="wav")
    
#     voice = sr.AudioFile("temp.wav")
#     with voice as source:
#         r.adjust_for_ambient_noise(source, duration=0.3)
#         audio = r.record(source, offset=0.3)

#     try:     
#         speech = r.recognize_google(audio, show_all=True, language='en-GB')
#         wordSpoken = ''
#         for sentence in speech['alternative']:
#             wordSpoken += " " + sentence['transcript']

#         print(f"Full Transcription: {wordSpoken}")

#         # Check if any of the keywords are present
#         isKeywordPresent = re.compile('|'.join(keywords), re.IGNORECASE).search(wordSpoken) is not None
#         print(f"Is Keyword Present: {isKeywordPresent}")

#         # Extract features for danger detection
#         isFearful = extract_features('temp.wav', mfcc=True, chroma=True, mel=True)
#         print(f"Is Fearful: {isFearful}")

#         if isFearful or isKeywordPresent:
#             return {"result": "True", "transcription": wordSpoken}
#         else:
#             return {"result": "False", "transcription": wordSpoken}

#     except r.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#         return {"result": "False", "transcription": "Error in speech recognition"}

# import base64
# from senti_model import extract_features
# from fastapi import FastAPI,File,UploadFile
# from fastapi import Form
# from pydantic import BaseModel
# from typing import List
# import re
# import speech_recognition as sr
# from pydub import AudioSegment
# app = FastAPI()

# r = sr.Recognizer()


# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}


# @app.post("/check")
# async def isInDanger(myfile: bytes = File(...),keywords: List[str] = Form(...)):
#     data = base64.b64encode(myfile)
#     mp3_file = open("temp.mp3", "wb")
#     decode_string = base64.b64decode(data)
#     mp3_file.write(decode_string)
#     sound = AudioSegment.from_file("temp.mp3")
#     sound.export("temp.wav", format="wav")
#     voice = sr.AudioFile("temp.wav")
#     with voice as source:
#          r.adjust_for_ambient_noise(source, duration=0.3)
#          audio = r.record(source,offset=0.3)
#     try:     
#         speech = r.recognize_google(audio,show_all=True,language='en-GB')
    
#         wordSpoken = ''
#         try:
#             for sentence in speech['alternative']:
#                  wordSpoken = ''.join([wordSpoken," ", sentence['transcript']])
#             return wordSpoken
#         except TypeError:
#              isKeywordPresent = False
        
#         if re.compile('|'.join(keywords),re.IGNORECASE).search(wordSpoken): #re.IGNORECASE is used to ignore case
#              # Do Something if word is present
#              isKeywordPresent = True
#         else:
#             # Do Something else if word is not present
#              isKeywordPresent = False
    
#     except r.UnknownValueError:
#          print("Google Speech Recognition could not understand audio")
#          isKeywordPresent = False

#     isFearful = extract_features('temp.wav',mfcc= True, chroma= True, mel= True)
#     if isFearful and isKeywordPresent :
#         return "True"
#     else:
#         return "False"         

import base64
from senti_model import extract_features
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import List
import re
import speech_recognition as sr
from pydub import AudioSegment

app = FastAPI()

r = sr.Recognizer()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/check")
async def isInDanger(myfile: bytes = File(...), keywords: List[str] = Form(...)):
    data = base64.b64encode(myfile)
    mp3_file = open("temp.mp3", "wb")
    decode_string = base64.b64decode(data)
    mp3_file.write(decode_string)
    sound = AudioSegment.from_file("temp.mp3")
    sound.export("temp.wav", format="wav")
    voice = sr.AudioFile("temp.wav")

    transcription = ""
    isKeywordPresent = False

    with voice as source:
        r.adjust_for_ambient_noise(source, duration=0.3)
        audio = r.record(source, offset=0.3)

    try:
        speech = r.recognize_google(audio, show_all=True, language='en-GB')
        if speech:
            for sentence in speech['alternative']:
                transcription += sentence['transcript'] + " "

            # Check if any of the keywords are present in the transcription
            if re.compile('|'.join(keywords), re.IGNORECASE).search(transcription):
                isKeywordPresent = True
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        transcription = ""

    # Use the sentiment model to detect fear in the audio
    isFearful = extract_features('temp.wav', mfcc=True, chroma=True, mel=True)

    # Determine the final result
    result = isFearful or isKeywordPresent
    return {
        "result": str(result),
        "transcription": transcription.strip()
    }
