# -*- coding: utf-8 -*-
#
# Time-stamp: <Saturday 2020-06-27 06:46:35 AEST Graham Williams>
#
# Copyright (c) Togaware Pty Ltd. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# ml listen azspeech

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import os
import sys

import azure.cognitiveservices.speech as speechsdk

from mlhub.pkg import azkey

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

SERVICE   = "Speech"
KEY_FILE  = os.path.join(os.getcwd(), "private.txt")

key, location = azkey(KEY_FILE, SERVICE, connect="location", verbose=False)

#-----------------------------------------------------------------------
# Set up a speech recognizer.
#-----------------------------------------------------------------------

speech_config     = speechsdk.SpeechConfig(subscription=key, region=location)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

#-----------------------------------------------------------------------
# Trasnscribe some spoken words.
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
