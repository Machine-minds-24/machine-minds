# dream_app/views.py
import speech_recognition as sr
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import requests

from .models import DreamApp
from summarizer import Summarizer

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Tokenize text
    

    resp = requests.post('https://api.smrzr.io/v1/summarize?num_sentences=5&algorithm=kmeans&min_length=40&max_length=500', data=text)
    summary = resp.json()['summary']
    summary = summary.split(',')

    # for i in summary:
    #     print("->",i)
    tokens = word_tokenize(text.lower())

    # Remove punctuation and stopwords
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords.words('english')]

    # Lemmatize tokens
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return summary

@csrf_exempt
def dream_app_input(request):
    if request.method == 'POST':
        if 'audio_data' in request.FILES:
            
            audio_file = request.FILES['audio_data']
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
            try:
                description = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                description = "Sorry, could not understand the audio."
            except sr.RequestError:
                description = "Sorry, could not process the request. Please try again later."
        else:
            
            description = request.POST.get('description', '')

        
        tokens = preprocess_text(description)
        feature_list = list(set(tokens))

        
        DreamApp.objects.create(description=description, feature_list=feature_list)

        return render(request, 'dreamapp/result.html', {'description': description, 'feature_list': feature_list})
    return render(request, 'dreamapp/input.html')
