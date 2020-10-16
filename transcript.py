import ffmpeg
import os
import speech_recognition as sr

# Creating a file with a transcription report
report = open('report google recognition.txt', 'w')

for filename in os.listdir('OVIONT_audio_examples'):
    if filename.endswith(".mp3"):
        # Processed audio file
        report.write("\nAudio: " + 'OVIONT_audio_examples/' + filename + '\n')

        # Convert .mp3 to .wav
        stream = ffmpeg.input('OVIONT_audio_examples/' + filename)
        stream = ffmpeg.output(stream, 'audio.wav')
        ffmpeg.run(stream)

        # Creating a Recognizer instance
        r = sr.Recognizer()
        '''
        Each Recognizer instance has seven methods for recognizing speech from an audio source using various APIs.
        These are:
            recognize_bing(): Microsoft Bing Speech
            recognize_google(): Google Web Speech API
            recognize_google_cloud(): Google Cloud Speech - requires installation of the google-cloud-speech package
            recognize_houndify(): Houndify by SoundHound
            recognize_ibm(): IBM Speech to Text
            recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx
            recognize_wit(): Wit.ai
        '''

        # Records the data from the entire file into an AudioData instance
        harvard = sr.AudioFile('audio.wav')
        with harvard as source:
            audio = r.record(source)

        try:
            transcript = r.recognize_google(audio, language='ru-RU')
            # Successful speech recognition
            report.write("Transcript: " + transcript + '\n')
        except sr.RequestError:
            # API was unreachable or unresponsive
            report.write("ERROR: API unavailable\n")
        except sr.UnknownValueError:
            # Speech was unintelligible
            report.write("ERROR: Unable to recognize speech\n")

        os.remove('audio.wav')
