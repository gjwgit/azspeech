# -*- coding: utf-8 -*-
#
# Time-stamp: <Saturday 2020-06-27 07:30:39 AEST Graham Williams>
#
# Copyright (c) Togaware Pty Ltd. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# ml speek azspeech This is a smaple text

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import os
import sys
import argparse

import azure.cognitiveservices.speech as speechsdk

from mlhub.pkg import azkey

#-----------------------------------------------------------------------
# Process the command line.
#-----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'word',
    nargs='+',
    help='word(s) to say')

args = option_parser.parse_args()

text = " ".join(args.word)

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

SERVICE   = "Speech"
KEY_FILE  = os.path.join(os.getcwd(), "private.txt")

key, location = azkey(KEY_FILE, SERVICE, connect="location", verbose=False)

#-----------------------------------------------------------------------
# Set up a speech synthesizer using the default speaker as audio output.
#-----------------------------------------------------------------------

speech_config      = speechsdk.SpeechConfig(subscription=key, region=location)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Synthesize the text to speech. When the following line is run expect
# to hear the synthesized speech.

result = speech_synthesizer.speak_text_async(text).get()
