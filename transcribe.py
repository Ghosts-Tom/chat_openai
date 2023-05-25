# import pyaudio
# import wave
import openai

audio_file = open("output.mp3", "rb")

# Transcribe the audio file
transcript = openai.Audio.transcribe("whisper-1", audio_file, language="zh")

# Get the transcribed text
transcribed_text = transcript["text"]

# Print and save the transcribed text
print(transcribed_text)

with open("transcription.txt", "w", encoding="gbk") as file:
    file.write(transcribed_text)

#将本地的txt文件中的内容读取出来，作为prompt，然后调用chat_with_gpt函数，返回response，最后打印出来
def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message