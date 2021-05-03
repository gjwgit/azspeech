# -*- coding: utf-8 -*-
#
# Time-stamp: <Monday 2021-05-03 13:58:22 AEST Graham Williams>
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
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from mlhub.utils import get_cmd_cwd, get_private

# -----------------------------------------------------------------------
# Process the command line.
# -----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'sentence',
    nargs='*',
    help='sentence to speek')

option_parser.add_argument(
    '--input', '-i',
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

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

PRIVATE_FILE = "private.json"

path = os.path.join(os.getcwd(), PRIVATE_FILE)

private_dic = get_private(path, "azspeech")

key = private_dic["key"]

location = private_dic["location"]

# ----------------------------------------------------------------------
# Read the text to be translated.
# ----------------------------------------------------------------------

text = ""
if args.input:
    text = open(os.path.join(get_cmd_cwd(), args.input), "r").read()
elif args.sentence:
    text = " ".join(args.sentence)

# Split the text into a list of sentences. Each sentence is sent off
# for synthesis. This avoids a very long text going off to the
# synthesizer (which seems to have a limit of some 640 characters) and
# is a natural break point anyhow.

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
        if str(result.reason) == "ResultReason.Canceled":
            print("The Azure subscription key is not correct. Please run ml configure azspeech to update your key.",  file=sys.stderr)
            sys.exit(1)
else:
    if sys.stdin.isatty():
        try:
            for line in sys.stdin:
                if line == "\n":
                    break
                result = speech_synthesizer.speak_text_async(line).get()
                if str(result.reason) == "ResultReason.Canceled":
                    print("The Azure subscription key is not correct. Please run ml configure azspeech to update your key.",  file=sys.stderr)
                    sys.exit(1)
        except KeyboardInterrupt:
            pass
    else:
        for line in sys.stdin.readlines():
            result = speech_synthesizer.speak_text_async(line).get()
            if str(result.reason) == "ResultReason.Canceled":
                print("The Azure subscription key is not correct. Please run ml configure azspeech to update your key.",  file=sys.stderr)
                sys.exit(1)
