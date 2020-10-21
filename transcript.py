import ffmpeg
import os
import speech_recognition as sr

# Creating a file with a transcription report
report = open('report google set 2 - 30sec.txt', 'w')

LINE_WIDTH = 100
# Formatting the transcribed text for the report
def recognition_report():
    length = 0
    for word in transcript.split():
        if (len(word) + length < LINE_WIDTH):
            report.write(word + ' ')
            length+=len(word) + 1
        else:
            report.write('\n')
            length = 0
    report.write('\n')

for filename in os.listdir('audio_examples_set_2'):
    if filename.endswith('.mp3'):
        # Processed audio file
        report.write('\naudio_examples_set_2/' + filename + '\n')

        # Convert .mp3 to .wav
        stream = ffmpeg.input('audio_examples_set_2/' + filename)
        stream = ffmpeg.output(stream, 'audio.wav')
        ffmpeg.run(stream)

        report.write("Size: {}\n".format(int(os.path.getsize('audio.wav')) / 1024))

        # Splitting records into parts of 60 seconds
        os.system('ffmpeg -i audio.wav -f segment -segment_time 30 -c copy audio%03d.wav')
        os.remove('audio.wav')

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

        for audio_chunk in os.listdir('.'):
            if audio_chunk.endswith(".wav"):

                # Records the data from the entire file into an AudioData instance
                harvard = sr.AudioFile(audio_chunk)
                with harvard as source:
                    audio = r.record(source)

                try:
                    transcript = r.recognize_google(audio, language='ru-RU')
                    # Successful speech recognition
                    recognition_report()
                except sr.RequestError:
                    # API was unreachable or unresponsive
                    report.write("ERROR: API unavailable\n")
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    report.write("ERROR: Unable to recognize speech\n")

                os.remove(audio_chunk)
  