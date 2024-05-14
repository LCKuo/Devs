import pyaudio
import wave
import os
from faster_whisper import WhisperModel
import keyboard
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

NEON_GREEN = '\033[1;32m'
RESET_COLOR = '\033[0m'
# Define a function to record a chunk of audio
def record_chunk(p, stream, file_path, chunk_length=3):
    frames = []
    for _ in range(0, int(16000 / 1024 * chunk_length)):
        data = stream.read(1024)
        frames.append(data)

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()

# Define the main function
def main2():
    model_size = "large-v3"  # Choose your model settings
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    accumulated_transcription = ""  # Initialize an empty string to accumulate transcriptions
    try:
        while True:
            chunk_file = "temp_chunk.wav"
            record_chunk(p, stream, chunk_file)
            segments, info = model.transcribe(chunk_file, beam_size=5)
            for segment in segments:
                if segment.text != " Thank you.":
                    print(NEON_GREEN + segment.text + RESET_COLOR)
                    accumulated_transcription += segment.text
            os.remove(chunk_file)
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
