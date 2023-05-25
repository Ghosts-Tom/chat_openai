import sys
import tkinter as tk
import pyaudio
import wave
import openai
import pyttsx3
from io import StringIO

# Set your API key
openai.api_key = "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"

# Create a Tkinter window and Text widget to display output
root = tk.Tk()
text_widget = tk.Text(root)
text_widget.pack()

# Create a StringIO object to redirect standard output to
output = StringIO()

# Redirect standard output to the StringIO object
sys.stdout = output


def audio():
    # 通过本地话筒将语音录入到output.mp3文件中
    # set the format of audio
    FORMAT = pyaudio.paInt16
    # set the number of channels
    CHANNELS = 1
    # set the sample rate
    RATE = 44100
    # set the chunk size
    CHUNK = 1024
    # set the duration of recording
    RECORD_SECONDS = 8
    # set the name of the output file
    WAVE_OUTPUT_FILENAME = "output.mp3"

    # create an instance of PyAudio
    audio = pyaudio.PyAudio()

    # open the microphone and start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    # create a list to store the recorded data
    frames = []

    # record for the specified duration
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # stop recording and close the microphone
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # write the recorded data to a WAV file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


# 将语音转换成文本

def transcribe():
    # Open the audio file
    audio_file = open("output.mp3", "rb")

    # Transcribe the audio file
    transcript = openai.Audio.transcribe("whisper-1", audio_file, language="zh")

    # Get the transcribed text
    transcribed_text = transcript["text"]

    # Print and save the transcribed text
    print(transcribed_text)

    with open("transcription.txt", "w", encoding="gbk") as file:
        file.write(transcribed_text)


# 将本地的txt文件中的内容读取出来，作为prompt，然后调用chat_with_gpt函数，返回response，最后打印出来
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



# 将response转换成语音
# Convert text to speech
def transcription():
    with open("transcription.txt", "r") as f:
        prompt = f.read()
        response = chat_with_gpt(prompt)
        print(response)
        engine = pyttsx3.init()
        engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-HK_TRACY_11.0")


# 是否结束运行？
stop = False

while not stop:
    audio()
    transcribe()
    transcription()
    # Set the value of the Text widget to the value of the StringIO object
    text_widget.insert(tk.END, output.getvalue())