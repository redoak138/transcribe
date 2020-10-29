import ffmpeg
import json
import os
import shutil
import time
from vosk import Model, KaldiRecognizer
import wave

PROJECT_PATH = os.getcwd()
AUDIO_RECORDINGS = PROJECT_PATH + "/audio_examples/"
REPORT_PATH      = PROJECT_PATH + "/VOSK Speech Recognition"
# https://alphacephei.com/vosk/models
MODEL = Model("vosk-model-ru-0.10")
REPORT_LINE_WIDTH = 100

# Variables for the resulting report
number_audio = 0
total_time = 0
total_recognized_words = 0

# Creating a folder with the final transcription report
shutil.rmtree(REPORT_PATH, ignore_errors=True)
os.makedirs(REPORT_PATH)

# Formatting the transcribed text for the report
def recognition_report():
    count_word = 0
    for word in transcript.split():
        count_word += 1
        if (len(word) + recognition_report.length > REPORT_LINE_WIDTH):
            audio_report.write('\n')
            recognition_report.length = 0
        audio_report.write(word + ' ')
        recognition_report.length += len(word) + 1
    return count_word

for audio_name in os.listdir(AUDIO_RECORDINGS):
    if audio_name.endswith('.mp3'):
        start_time = time.time()
        number_audio+=1

        # Report for the current audio file
        audio_report = open(REPORT_PATH + '/' + audio_name.rsplit(".", 1)[0] + '.txt', 'w')

        # Convert .mp3 to .wav
        stream = ffmpeg.input(AUDIO_RECORDINGS + audio_name)
        stream = ffmpeg.output(stream, 'audio.wav')
        ffmpeg.run(stream)

        audio_report.write("Size of the converted .wav file : {} KB\n".format(os.path.getsize('audio.wav') // 1024))

        wf = wave.open('audio.wav', "rb")
        rec = KaldiRecognizer(MODEL, wf.getframerate())

        recognized_words = 0
        recognition_report.length = 0
        audio_report.write("\nTranscription:\n")

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                json_dict = json.loads(rec.Result())
                transcript = json_dict['text']
                count_word = recognition_report()
                recognized_words += count_word
            else:
                rec.PartialResult()

        total_recognized_words += recognized_words
        current_audio_time = time.time() - start_time
        total_time += current_audio_time

        audio_report.write("\n\nThe processing time of the audio file: ")
        audio_report.write("{}\n".format(time.strftime("%M:%S", time.gmtime(current_audio_time))))
        audio_report.write("Number of recognized words: {}".format(recognized_words))

        os.remove('audio.wav')

average_audio = total_time // number_audio

# Creating the final report
main_report = open(REPORT_PATH + '.txt', 'w')

main_report.write("Total time: {}\n".format(time.strftime("%H:%M:%S", time.gmtime(total_time))))

main_report.write("\nTotal audio recordings: {}\n".format(number_audio))
main_report.write("Average processing time per audio recording: ")
main_report.write("{}\n".format(time.strftime("%M:%S", time.gmtime(average_audio))))
main_report.write("Total number of recognized words: {}\n".format(total_recognized_words))
