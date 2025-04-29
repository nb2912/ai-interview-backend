# speech_to_text/stream_handler.py

from .realtime_transcribe import transcribe_audio_stream
import threading
from typing import Callable

class AudioStreamHandler:
    def __init__(self, text_callback: Callable[[str], None]):
        """
        Initializes the audio stream handler.

        Args:
            text_callback: A function to be called with each transcribed text chunk.
        """
        self.text_callback = text_callback
        self.transcription_thread = None
        self._is_running = False

    def start_streaming(self):
        """
        Starts the audio stream and transcription in a separate thread.
        """
        if not self._is_running:
            self._is_running = True
            self.transcription_thread = threading.Thread(target=self._run_transcription)
            self.transcription_thread.daemon = True  # Thread will exit when the main program exits
            self.transcription_thread.start()
            print("Audio streaming started.")
        else:
            print("Audio streaming is already running.")

    def stop_streaming(self):
        """
        Stops the audio stream and the transcription thread.
        """
        if self._is_running and self.transcription_thread and self.transcription_thread.is_alive():
            self._is_running = False
            # There's no direct way to stop the generator gracefully from another thread
            # This relies on the KeyboardInterrupt in the transcribe_audio_stream
            print("Requesting to stop audio streaming...")
        elif not self._is_running:
            print("Audio streaming is not running.")
        else:
            print("Transcription thread not active.")

    def _run_transcription(self):
        """
        Internal method to run the transcription and call the callback.
        """
        for text in transcribe_audio_stream():
            if self._is_running:
                self.text_callback(text)
            else:
                break
        print("Transcription finished.")
        self._is_running = False

if __name__ == "__main__":
    def handle_transcribed_text(text):
        print("Callback received:", text)

    audio_handler = AudioStreamHandler(handle_transcribed_text)
    audio_handler.start_streaming()

    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        audio_handler.stop_streaming()
        if audio_handler.transcription_thread and audio_handler.transcription_thread.is_alive():
            audio_handler.transcription_thread.join()  # Wait for the thread to finish
        print("Program stopped.")