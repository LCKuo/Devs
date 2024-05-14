import pyaudio
import wave
import os
from faster_whisper import WhisperModel
import keyboard
from openai import OpenAI
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

NEON_GREEN = '\033[1;32m'
RESET_COLOR = '\033[0m'
# Define a function to record a chunk of audio
# Define the main function for recording audio
def record_audio(file_path):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    # Record audio until SPACE key is pressed
    print("Recording start.")

    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if not keyboard.is_pressed("space"):
            break

    print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a WAV file
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Define the main function
def main2():
    print("Wait for Model loading ...")

    model_size = "large-v3"  # Choose your model settings
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    accumulated_transcription = ""  # Initialize an empty string to accumulate transcriptions
    print("STT Model loaded!")
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    history = [
        {"role": "system", "content": "Please respond in Chinese only,and keep as concisely as possible. Your name is LC."},
    ]

    try:
        print("Sys Initiate ... press Space to record")

        while True:
            if keyboard.is_pressed("space"):
                askPromp = ""
                returnAns = ""
                chunk_file = "temp_chunk.wav"
                record_audio(chunk_file) ##Record Audio from here
                segments, info = model.transcribe(chunk_file, beam_size=5)
                for segment in segments:
                    if segment.text != " Thank you.":
                        print(NEON_GREEN + segment.text + RESET_COLOR)
                        askPromp += segment.text ## get the Stt result,and add to LLM prompt
                        accumulated_transcription += segment.text ##For log
                ## Start ask LLM from Here ...##
                while True : 
                    history.append({"role": "user", "content": askPromp})
                    completion = client.chat.completions.create(
                        model="microsoft/Phi-3-mini-4k-instruct-gguf", ## using Models 
                        messages=history, ##聊天串
                        temperature=0.7,
                        stream=True,
                    )
                    new_message = {"role": "assistant", "content": ""}
    
                    for chunk in completion:
                        if chunk.choices[0].delta.content:
                            print(chunk.choices[0].delta.content, end="", flush=True)
                            returnAns += chunk.choices[0].delta.content
                            new_message["content"] += chunk.choices[0].delta.content

                    history.append(new_message)

                    break

                os.remove(chunk_file)
                print(returnAns, end="")
                ##Ask for TTS from here
                print("press Space to record...")

    except KeyboardInterrupt:
        print("Stopping.")
        # Write the accumulated transcription to the log file
        with open("log.txt", "w") as log_file:
            log_file.write(accumulated_transcription)
    finally:
        print("LOG:" + accumulated_transcription)
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main2()
