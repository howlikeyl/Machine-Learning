"""
Picarx_robot Voice Assistant

Lets you type or speak a question; sends it to Google's Gemini model,
prints the answer, and speaks it aloud through the robot's speaker.
Type 'a' to ask by keyboard, 't' to talk, or 'q' to quit.

Requires: the GEMINI_API_KEY environment variable to be set.
Run with: python3 LLM_test.py
"""

import os
import google.generativeai as genai
from gtts import gTTS
import os
import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()
# read the key from the environment (not hardcoded)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# pick the model
model = genai.GenerativeModel("gemini-2.5-flash")

#. Listen for user Audio Input
def listen_for_audio():
  with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)  # adjust for ambient noise
    print("Please say something...")
    audio = recognizer.listen(source) # save the audio input from the microphone
  try:
    text = recognizer.recognize_google(audio)  # convert the audio to text using Google's speech recognition
    return text
  except sr.UnknownValueError:
    print("I'm sorry, I could not understand the audio. Please try again.")
    return None

if '__main__' == __name__:
  try:
    while True:
      text = None
      print ("press 't' to talk to Gemini, 'q' to quit, 'a' to ask a question")
      user_input = input("Enter your choice: ")
      if user_input.lower() == 'q':
        print("Thank you for using Gemini. Goodbye!")
        break
      elif user_input.lower() == 't':
        text = listen_for_audio()
        if text is not None:  #. to prevent crash if the audio is not understood
          print("You said: " + text)
      elif user_input.lower() == 'a':
        text = input("Please type your question: ")
      
      # Generate response from Gemini and convert to speech
      if text is not None:
        response = model.generate_content(text)
        print(response.text)
        answer = response.text
        answer = answer.replace("*", "")  # remove asterisks from the answer
        tts = gTTS(answer)              # convert text to speech
        tts.save("answer.mp3")         # save it as an audio file    
        os.system("mpg123 -a plughw:1,0 answer.mp3")
      else:
        print("No valid input received. Please try again.")
  finally:
    print("Exiting the program. Goodbye!")