# speech_to_text/realtime_transcribe.py

import speech_recognition as sr
from typing import Generator

def transcribe_audio_stream() -> Generator[str, None, None]:
    """
    Continuously listens to the microphone and yields transcribed text chunks.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Say something!")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise

        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)  # Using Google Speech Recognition
                yield text
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from speech recognition service; {e}")
                break
            except KeyboardInterrupt:
                print("\nStopping transcription.")
                break

if __name__ == "__main__":
    for transcription in transcribe_audio_stream():
        print("Transcription:", transcription)