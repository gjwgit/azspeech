# -*- coding: utf-8 -*-
#
# Time-stamp: <Monday 2021-05-03 13:59:17 AEST Graham Williams>
#
# Copyright (c) Togaware Pty Ltd. All rights reserved.
# Licensed under GPLv3.
# Author: Graham.Williams@togaware.com
#
# ml transcribe azspeech

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

from mlhub.utils import get_cmd_cwd, get_private
import argparse
import azure.cognitiveservices.speech as speechsdk
import os
import sys
import textwrap
import time

#-----------------------------------------------------------------------
# Process the command line
#-----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

# Currently only wav supported here. For mp3 some extra configuration
# required. See 

option_parser.add_argument(
    '--input', "-i",
    help='wav input file')

args = option_parser.parse_args()

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

PRIVATE_FILE = "private.json"

path = os.path.join(os.getcwd(), PRIVATE_FILE)

private_dic = get_private(path, "azspeech")

key = private_dic["Azure subscription"]["key"]

location = private_dic["Azure subscription"]["location"]

#-----------------------------------------------------------------------
# Set up a speech configuration.
#-----------------------------------------------------------------------

speech_config     = speechsdk.SpeechConfig(subscription=key, region=location)

#-----------------------------------------------------------------------
# Transcribe file or from microphone.
#-----------------------------------------------------------------------

if args.input:
    path = os.path.join(get_cmd_cwd(), args.input)
    
    # Create a callback to terminate the transcription once the full
    # audio has been transcribed.

    done = False
    def stop_cb(evt):
        """Callback to stop continuous recognition upon receiving an event (evt)"""
        speech_recognizer.stop_continuous_recognition()
        global done
        done = True

    # Create an audio configuration to load the audio from file rather
    # than from microphone. A sample audio file is available as
    # harvard.wav from:
    #
    # https://github.com/realpython/python-speech-recognition/raw/master/
    # audio_files/harvard.wav
    #
    # A recognizer is then created with the given settings.

    audio_config  = speechsdk.audio.AudioConfig(use_default_microphone=False, filename=path)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                                   audio_config=audio_config)

    # Connect callbacks to the events fired by the speech
    # recognizer. Most are commented out as examples here to allow
    # tracing if you are interested in exploring the interactions with
    # the server.
    #
    # speech_recognizer.recognizing.connect(lambda evt:
    #                                       print('RECOGNIZING: {}'.format(evt)))
    # speech_recognizer.session_started.connect(lambda evt:
    #                                           print('STARTED: {}'.format(evt)))
    # speech_recognizer.session_stopped.connect(lambda evt:
    #                                           print('STOPPED {}'.format(evt)))
    # speech_recognizer.canceled.connect(lambda evt:
    #                                    print('CANCELED {}'.format(evt)))
    
    # This callback provides the actual transcription.

    speech_recognizer.recognized.connect(lambda evt:
                                         print(f'{textwrap.fill(evt.result.text)}\n'))

    # Stop continuous recognition on either session stopped or canceled
    # events.

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition, and then perform
    # recognition. For long-running recognition we use
    # start_continuous_recognition().

    speech_recognizer.start_continuous_recognition()
    while not done: time.sleep(.5)
    
else:

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    #-----------------------------------------------------------------------
    # Trasnscribe spoken words from the system microphone.
    #-----------------------------------------------------------------------

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("{}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("To update your key, please run ml configure azspeech.", file=sys.stderr)
            sys.exit(1)



