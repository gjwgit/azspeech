# -*- coding: utf-8 -*-
#
# Time-stamp: <Saturday 2020-06-27 07:32:22 AEST Graham Williams>
#
# Copyright (c) Togaware Pty Ltd. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# ml synthesize azspeech <myspeech.txt>

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import os
import sys
import argparse

import azure.cognitiveservices.speech as speechsdk

from mlhub.pkg import azkey
from mlhub.utils import get_cmd_cwd

#-----------------------------------------------------------------------
# Process the command line.
#-----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'path',
    help='path to text file to synthesize')

args = option_parser.parse_args()

path = os.path.join(get_cmd_cwd(), args.path)

text = open(path, "r").read()

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
