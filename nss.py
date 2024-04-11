import speech_recognition as sr
from dotenv import load_dotenv
import os
import pyttsx3
from config import apikey
from datetime import datetime
import time
import wikipedia
import streamlit as st
import google.generativeai as genai
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown
import PyPDF2
import requests



model = genai.GenerativeModel('gemini-pro')
load_dotenv()
genai.configure(api_key=apikey)
chat = model.start_chat(enable_automatic_function_calling=True)
inse="'You are a chatbot for NSS College of Engineering, Palakkad, Kerala. Your purpose is to assist students, faculty, and anyone interested in the college with relevant information. You can answer questions aboutAcademics: Programs offered, admission procedures, fees, scholarships, faculty, etc. Campus life: Facilities, hostels, clubs, events, sports, etc. Placements: Companies visiting, average salary packages, placement process,etc.General information: College history, location, contact details, etc.Please note:Do not answer any questions outside the scope of the provided information about NSSCE. If you encounter such questions, politely inform the user that you are not equipped to answer them. Always be friendly and helpful i'n your responses.Maintain a formal yet approachable tone.If you are unsure about something, offer to direct the user to the relevant resources or personnel.Here is the information you can use to answer questions:(Insert the full text of the provided PDF document about NSSCE here) make answer short and use full"
def get_ai(text):

  response = chat.send_message(text)
  text=response.text
  text = text.replace('*',' ')
  print(text)
  return text

def speak(text):
    engine = pyttsx3.init()
    print(text)
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Sorry  some thing gone rong "
if __name__ == '__main__':
    with open('NSS College of Engineering - Wikipedia.pdf', 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        pdf_text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            pdf_text += page_text

    api_url = "https://api.gemini.com/green/v1/analyze"  # Replace with the actual API endpoint
    api_key = apikey  # Replace with your API key

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "pdf_text": pdf_text
    }

    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code == 200:
        # Successful request
        analysis_results = response.json()
        # Process the analysis results
    else:
        # Handle error
        print(f"Error: {response.status_code}")
    response = get_ai(inse)
    print(response)
    speak(" Hey there! I'm Safari, your online campus tour guide. Ready to explore together?")
    speak("Hey homie! If you need anything at all, just call hay safari.")
    while True:
        print("Listening...")
        query=takeCommand()
        if "safari exit".lower() in query.lower():
            exit()
        elif "hey safari".lower() in query.lower():
            speak("how can i help")
            query = takeCommand()
            response = get_ai(query)
            speak(response)