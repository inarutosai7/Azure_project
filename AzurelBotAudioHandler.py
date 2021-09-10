import azure.cognitiveservices.speech as speechsdk
import configparser
from random import random
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
import os

# Init Speech Key & Area
config = configparser.ConfigParser()
config.read('config.ini')
speech_key, service_region = config.get('AzureKeyData', 'SpeechKey'), config.get('AzureKeyData', 'ServiceArea')
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

#Initial
global BotResponses

# ffMPEG reference command
# ffmpeg -i 111.mp3 -acodec pcm_s16le -ac 1 -ar 16000 out.wav
# ffmpeg -i 111.mp3 -acodec pcm_s16le  -ac 1 -ar 16000 out.wav
# ffmpeg -i input.wav -ar 16000 output.wav
# ffmpeg -i sample.mp3 -ac 1 sample.wav

def LineBotAudioDirect2Wav(AudioFilePath):
    # Convert Audio file  from mp3/m4a to WAV
    if('mp3' in AudioFilePath ):
        print(' mp3 to wav\n')
        AzureWavFilePath = AudioFilePath.replace('mp3', 'wav')
        os.system('ffmpeg -y -i ' + AudioFilePath + '  -ac 1 -ar 16000  ' +AzureWavFilePath+ ' -loglevel quiet')
        print('\n ffmpeg -y -i ' + AudioFilePath + '  -ac 1 -ar 16000  ' + AzureWavFilePath+ ' -loglevel quiet \n')

    elif('m4a' in AudioFilePath ):
        print(' m4a to wav\n')
        AzureWavFilePath =AudioFilePath.replace('m4a', 'wav')
        os.system('ffmpeg -y -i ' + AudioFilePath + '   -ac 1  -ar 16000  ' + AzureWavFilePath + ' -loglevel quiet')
        print('\n ffmpeg -y -i ' + AudioFilePath + ' -ac 1  -ar 16000  '  + AzureWavFilePath + ' -loglevel quiet \n')
    else:
        print(' [ Error ] InCorrect File Name  or File not found !!')

    # Start Azure Process
    print('Azure input file \n')
    audio_input = speechsdk.audio.AudioConfig(filename=AzureWavFilePath)
    # Creates a recognizer with the given settings
    print('Azure doing job \n')
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                                                                        language="zh-TW",
                                                                                        audio_config=audio_input)
    print("Recognizing first result...")
    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.  The task returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        usrInput = result.text
        return usrInput
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
        return False
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            return False
        return False

def LineBotAudioConvert2AzureAudio(FilePath):
    # Assign FFPMG bin address
    print('Assign ffpmg location')
    # If you don't set the system variables, please assgin ffmpeg file allocation
    # AudioSegment.converter = 'C:\\ffmpg\\bin\\ffmpeg.exe'
    print('read audio message')
    usraudio  = AudioSegment.from_file_using_temporary_files(FilePath)
    # Convert Audio file  from mp3/m4a to WAV
    # wav path for Azure

    usraudio.export(FilePath, format="wav")
    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_filename = FilePath
    # Change the File Name from m4a to wav
    print('Azure wav file path == ',audio_filename.replace('m4a','wav'))
    # Start Azure Process
    print('Azure input file \n')
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)
    # Creates a recognizer with the given settings
    print('Azure Start doing job ')
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,language="zh-TW", audio_config=audio_input)
    print("Recognizing first result...")
    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.  The task returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        usrInput = result.text
        return usrInput
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
        return False
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            return False
        return False
