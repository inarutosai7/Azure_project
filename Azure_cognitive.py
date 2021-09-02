from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

#  Initial Azure configure
speech_key = config.get('azure_cognitive', 'speech_key')
service_region = config.get('azure_cognitive', 'service_region')
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

def Azure_cognictive(path, event):
    usraudio = AudioSegment.from_file_using_temporary_files(path)
    path = './static/{}.wav'.format(event.message.id)
    usraudio.export(path, format="wav")
    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_filename = path
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)
    # Creates a recognizer with the given settings

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
        return "Recognized: {}".format(result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized: {}".format(result.no_match_details)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return "Speech Recognition canceled: {}".format(cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
