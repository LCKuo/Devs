import pyaudio
import wave
import keyboard
import os

# Define the main function for recording audio
def record_audio(file_path, duration):
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

    print("Recording... Press SPACE to stop.")

    # Record audio until SPACE key is pressed
    while not keyboard.is_pressed("space"):
        data = stream.read(CHUNK)
        frames.append(data)

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

if __name__ == "__main__":
    file_path = "recorded_audio.wav"  # File path to save the recorded audio
    duration = 5  # Duration of recording in seconds
    record_audio(file_path, duration)
