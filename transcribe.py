# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# AIM:
# ml transcribe azspeech2txt sample.wav

# Defaults.

KEY_FILE = "private.py"
DEFAULT_REGION = "southeastasia"

subscription_key = None
region = DEFAULT_REGION

# Import the required libraries.

import os
import sys
import azure.cognitiveservices.speech as speechsdk

#from textwrap import fill

# Prompt the user for the key and region and save into private.py for
# future runs of the model. The contents of that file is:
#
# subscription_key = "a14d...ef24"
# region = "southeastasia"

if os.path.isfile(KEY_FILE) and os.path.getsize(KEY_FILE) != 0:
    exec(open(KEY_FILE).read())
else:
    sys.stdout.write("Please enter your Speech Services subscription key []: ")
    subscription_key = input()

    sys.stdout.write("Please enter your region [southeastasia]: ")
    region = input()
    if len(region) == 0: region = DEFAULT_REGION

    if len(subscription_key) > 0:
        assert subscription_key
        ofname = open(KEY_FILE, "w")
        ofname.write("""subscription_key = "{}"
region = "{}"
    """.format(subscription_key, region))
        ofname.close()

        print("""
I've saved that information into the file:

        """ + os.getcwd() + "/" + KEY_FILE)

########################################################################
#
# Following is the code that does the actual work, creating an
# instance of a speech config with the specified subscription key and
# service region, then creating a recognizer with the given settings,
# and then performing recognition. recognize_once() returns when the
# first utterance has been recognized, so it is suitable only for
# single shot recognition like command or query. For long-running
# recognition, use start_continuous_recognition() instead, or if you
# want to run recognition in a non-blocking manner, use
# recognize_once_async().

# harvard.wav comes from
# https://github.com/realpython/python-speech-recognition/raw/master/audio_files/harvard.wav

speech_config     = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
#audio_config      = speechsdk.audio.AudioConfig(use_default_microphone=False, filename='harvard.wav')
audio_config      = speechsdk.audio.AudioConfig(use_default_microphone=False, filename='sample.wav')
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
#result            = speech_recognizer.recognize_once()
#result            = speech_recognizer.start_continuous_recognition()

#es = speechsdk.EventSignal(sr.recognized, sr.recognized)

#result = sr.recognize_once()

import time
speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speech_recognizer.session_stopped.connect(lambda evt: print('\nSESSION STOPPED {}'.format(evt)))
speech_recognizer.recognized.connect(lambda evt: print('\n{}'.format(evt.result.text)))

speech_recognizer.start_continuous_recognition()
time.sleep(1000)
speech_recognizer.stop_continuous_recognition()

speech_recognizer.session_started.disconnect_all()
speech_recognizer.recognized.disconnect_all()
speech_recognizer.session_stopped.disconnect_all()

# Should be: the stale smell of old beer lingers it takes heat to
# bring out the odor a cold dip restores health and zest a salt pickle
# taste fine with ham tacos al Pastore are my favorite a zestful food
# is the hot cross bun

#
########################################################################

# Checks result.

# if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#     print("Recognized: {}".format(result.text))
# elif result.reason == speechsdk.ResultReason.NoMatch:
#     print("No speech could be recognized: {}".format(result.no_match_details))
# elif result.reason == speechsdk.ResultReason.Canceled:
#     cancellation_details = result.cancellation_details
#     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#     if cancellation_details.reason == speechsdk.CancellationReason.Error:
#         print("Error details: {}".format(cancellation_details.error_details))
