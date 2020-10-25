import ffmpeg
import os
import shutil
import speech_recognition as sr
import time

PROJECT_PATH = os.getcwd()
AUDIO_RECORDINGS = PROJECT_PATH + "/audio_examples/"
REPORT_PATH      = PROJECT_PATH + "/Google Web Speech API with 30 sec split/"
REPORT_LINE_WIDTH = 100

# Variables for the resulting report
total_audio = 0
total_chunks = 0
error_chunks = 0
chunks_time = 0

# Creating a folder with the final transcription report
shutil.rmtree(REPORT_PATH, ignore_errors=True)
os.makedirs(REPORT_PATH)

# Formatting the transcribed text for the report
def recognition_report():
    length = 0
    for word in transcript.split():
        if (len(word) + length < REPORT_LINE_WIDTH):
            audio_report.write(word + ' ')
            length+=len(word) + 1
        else:
            audio_report.write('\n')
            length = 0
    audio_report.write('\n')

total_time = time.time()
for audio_name in os.listdir(AUDIO_RECORDINGS):
    if audio_name.endswith('.mp3'):
        total_audio+=1

        # Processed audio file
        audio_report = open(REPORT_PATH + audio_name.rsplit(".", 1)[0] + '.txt', 'w')

        # Convert .mp3 to .wav
        stream = ffmpeg.input(AUDIO_RECORDINGS + audio_name)
        stream = ffmpeg.output(stream, 'audio.wav')
        ffmpeg.run(stream)

        audio_report.write("Size of the converted .wav file : {}\n".format(int(os.path.getsize('audio.wav')) / 1024))

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

        audio_report.write("\nTranscription:\n")

        for audio_chunk in os.listdir(PROJECT_PATH):
            if audio_chunk.endswith(".wav"):
                total_chunks+=1
                chunk_time = time.time()

                # Records the data from the entire file into an AudioData instance
                harvard = sr.AudioFile(audio_chunk)
                with harvard as source:
                    audio = r.record(source)
                try:
                    transcript = r.recognize_google(audio, language='ru-RU')
                    # Successful speech recognition
                    recognition_report()
                except sr.RequestError:
                    error_chunks+=1
                    # API was unreachable or unresponsive
                    audio_report.write("ERROR: API unavailable\n")
                except sr.UnknownValueError:
                    error_chunks+=1
                    # Speech was unintelligible
                    audio_report.write("ERROR: Unable to recognize speech\n")

                os.remove(audio_chunk)
                chunks_time += time.time() - chunk_time

total_time = time.time() - total_time
average_audio = int(total_time / total_audio)
average_chunk = int(chunks_time / total_chunks)

# Creating the final report
main_report = open(REPORT_PATH + 'report.txt', 'w')

main_report.write("Total time: {}\n".format(time.strftime("%H:%M:%S", time.gmtime(total_time))))

main_report.write("\nTotal audio recordings: {}\n".format(total_audio))
main_report.write("Average processing time per audio recording: ")
main_report.write("{}\n".format(time.strftime("%M:%S", time.gmtime(average_audio))))

main_report.write("\nTotal chunks (30 sec) of audio recordings: {}\n".format(total_chunks))
main_report.write("Average processing time per chunk (30 sec) of audio recording: ")
main_report.write("{}\n".format(time.strftime("%M:%S", time.gmtime(average_chunk))))
main_report.write("Chunks with errors: {}%\n".format(error_chunks / total_chunks * 100))
