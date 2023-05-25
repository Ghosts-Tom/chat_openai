import openai
import os
import pyttsx3
import config

openai.api_key = config.api_key

def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

with open("transcription.txt", "r") as f:
    prompt = f.read()
    response = chat_with_gpt(prompt)
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()
