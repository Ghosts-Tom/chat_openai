
import pyaudio
import wave
# import openai
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