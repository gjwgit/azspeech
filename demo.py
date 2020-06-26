# -*- coding: utf-8 -*-
#
# Time-stamp: <Friday 2020-06-26 21:27:44 AEST Graham Williams>
#
# Copyright (c) Togaware Pty Ltd. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# This demo is based on the Azure Cognitive Services Speech to Text Quick Start

from mlhub.pkg import azkey, mlask, mlcat

mlcat("Speech Services", """\
Welcome to a demo of the pre-built models for Speech provided
through Azure's Cognitive Services. The Speech cloud service 
supports speech to text and text to speech capabilities.
""")

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import os
import sys

import azure.cognitiveservices.speech as speechsdk

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

SERVICE   = "Speech"
KEY_FILE  = os.path.join(os.getcwd(), "private.txt")

key, location = azkey(KEY_FILE, SERVICE, connect="location")

#-----------------------------------------------------------------------
# Set up a speech recognizer and synthesizer.
#-----------------------------------------------------------------------

# Following is the code that does the actual work, creating an
# instance of a speech config with the specified subscription key and
# service region, then creating a recognizer with the given settings,
# and then performing recognition. recognize_once() returns when the
# first utterance has been recognized, so it is suitable only for
# single shot recognition like command or query. For long-running
# recognition, use start_continuous_recognition() instead, or if you
# want to run recognition in a non-blocking manner, use
# recognize_once_async().

speech_config     = speechsdk.SpeechConfig(subscription=key, region=location)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

#-----------------------------------------------------------------------
# Trasnscribne some spoken words.
#-----------------------------------------------------------------------

mlask(prompt="Press Enter and then say something", end="\n")

result = speech_recognizer.recognize_once()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))

mlask(begin="\n", end="\n")

#-----------------------------------------------------------------------
# Request text from console input.
#-----------------------------------------------------------------------

print("Now type text to be spoken. When Enter is pressed you will hear the result.\n")
text = input()

# Synthesize the text to speech. When the following line is run expect
# to hear the synthesized speech.

result = speech_synthesizer.speak_text_async(text).get()

print()
