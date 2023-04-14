import pyaudio
import numpy as np
import math
import time
from pydub import AudioSegment
from pydub.playback import play

# Define parameters for audio stream
chunk_size = 1024
sample_rate = 44100

# Initialize PyAudio and open audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

# Define function to convert frequency to note
def freq_to_note(freq):
    if freq <= 0:
        return "Invalid"
    # Define frequency ranges for each note
    note_ranges = {
        'C': (16.35, 34.65),
        'C#': (34.65, 69.3),
        'D': (69.3, 138.59),
        'D#': (138.59, 277.18),
        'E': (277.18, 554.37),
        'F': (554.37, 1108.73),
        'F#': (1108.73, 2217.46),
        'G': (2217.46, 4434.92),
        'G#': (4434.92, 8869.84),
        'A': (8869.84, 17739.68),
        'A#': (17739.68, 35279.36),
        'B': (35279.36, 7902.13e8)
    }
    # Find the note whose frequency range includes the given frequency
    for note, (min_freq, max_freq) in note_ranges.items():
        if freq >= min_freq and freq < max_freq:
            return note
    # If no matching note is found, return "Invalid"
    return "Invalid"

# Define the amplitude threshold
threshold = 1000

# Loop to continuously read audio data from stream and calculate FFT
while True:
    # Read audio data from stream
    audio_data = stream.read(chunk_size)

    # Convert audio data to NumPy array and calculate FFT
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    fft_data = np.fft.fft(audio_array)

    # Extract positive frequency components and corresponding frequencies
    positive_freq = np.abs(fft_data[:len(fft_data)//2])
    freqs = np.fft.fftfreq(len(fft_data), 1/sample_rate)[:len(fft_data)//2]

    # Find the dominant frequency
    idx = np.argmax(positive_freq)
    dominant_freq = freqs[idx]

    # Check if the dominant frequency amplitude is above the threshold
    if np.max(positive_freq) >= threshold:
        # Print the dominant frequency and corresponding note
        pitch = freq_to_note(dominant_freq)
        print(pitch)

        # Pfad zur Audio-Datei angeben
        if pitch != "Invalid":
            print(pitch)
            audio_file = "tones/"+ pitch+"4.wav"
            # Audio-Datei abspielen
            time.sleep(0.6)
            sound = AudioSegment.from_wav(audio_file)
            time.sleep(0.6)
            play(sound)
        
    time.sleep(0.5)
