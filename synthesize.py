# -*- coding: utf-8 -*-
#
# Time-stamp: <Tuesday 2021-04-20 09:16:19 AEST Graham Williams>
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
import re
import sys
import argparse

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from mlhub.pkg import azkey
from mlhub.utils import get_cmd_cwd

# -----------------------------------------------------------------------
# Process the command line.
# -----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'sentence',
    nargs='*',
    help='sentence to speek')

option_parser.add_argument(
    '--file', '-f',
    help='path to a text file to speek')

option_parser.add_argument(
    '--lang', "-l",
    help='spoken language')

option_parser.add_argument(
    '--voice', "-v",
    help='spoken voice')

option_parser.add_argument(
    '--output', "-o",
    help='path to an audio file to save. The file type should be wav')

args = option_parser.parse_args()

text = " ".join(args.sentence)

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

SERVICE = "Speech"
KEY_FILE = os.path.join(os.getcwd(), "private.txt")

key, location = azkey(KEY_FILE, SERVICE, connect="location", verbose=False)

# ----------------------------------------------------------------------
# Read the text to be translated.
# ----------------------------------------------------------------------

text = ""
if args.file:
    text = open(os.path.join(get_cmd_cwd(), args.file), "r").read()
elif args.sentence:
    text = " ".join(args.sentence)

# Split the text into a list of sentences. Each sentence is sent off
# for synthesis. This avoids a very long text going off to the
# synthesizer (which seems to have a limit of some 640 characters) and
# is a natural break point anyhow.

text = " ".join(text.splitlines())
text = " ".join(text.splitlines())
text = text.replace(". ", "\n")
text = text.splitlines()

# -----------------------------------------------------------------------
# Set up a speech synthesizer using the default speaker as audio output.
#
# https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support
#
# -----------------------------------------------------------------------

speech_conf = speechsdk.SpeechConfig(subscription=key, region=location)


if args.lang:
    speech_conf.speech_synthesis_language = args.lang
if args.voice:
    speech_conf.speech_synthesis_voice_name = args.voice

if args.output:
    audio_conf = AudioOutputConfig(filename=args.output)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_conf,
                                                     audio_config=audio_conf)
else:
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_conf)

# ----------------------------------------------------------------------
# Synthesize the text to speech. When the following line is run expect
# to hear the synthesized speech.
# ----------------------------------------------------------------------

if len(text):
    for sentence in text:
        result = speech_synthesizer.speak_text_async(sentence).get()
else:
    if sys.stdin.isatty():
        try:
            for line in sys.stdin:
                if line == "\n":
                    break
                result = speech_synthesizer.speak_text_async(line).get()
        except KeyboardInterrupt:
            pass
    else:
        for line in sys.stdin.readlines():
            result = speech_synthesizer.speak_text_async(line).get()
