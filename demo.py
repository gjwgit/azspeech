# -*- coding: utf-8 -*-
#
# Time-stamp: <Monday 2021-05-03 14:14:52 AEST Graham Williams>
#
# Copyright (c) Togaware Pty Ltd. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# This demo is based on the Azure Cognitive Services Speech to Text Quick Start

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.
from mlhub.pkg import mlask, mlcat, get_private
from recognise import recognise
from translate import translate_speech_to_text
import azure.cognitiveservices.speech as speechsdk
import os
import sys

mlcat("Speech Services", """\
Welcome to a demo of the pre-built models for Speech provided
through Azure's Cognitive Services. The Speech cloud service
supports speech to text, text to speech, speech translation and
Speaker Recognition capabilities.
""")

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------
key, location = get_private()

# Recognition is experimental and is only available at present
# 20210428 from the westus data centre.

RECOGNISE_FLAG = (location == "westus")

# -----------------------------------------------------------------------
# Set up a speech recognizer and synthesizer.
# -----------------------------------------------------------------------

# Following is the code that does the actual work, creating an
# instance of a speech config with the specified subscription key and
# service region, then creating a recognizer with the given settings,
# and then performing recognition. recognize_once() returns when the
# first utterance has been recognized, so it is suitable only for
# single shot recognition like command or query. For long-running
# recognition, use start_continuous_recognition() instead, or if you
# want to run recognition in a non-blocking manner, use
# recognize_once_async().

speech_config = speechsdk.SpeechConfig(subscription=key, region=location)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# -----------------------------------------------------------------------
# Transcribe some spoken words.
# -----------------------------------------------------------------------

mlask(end="\n")

mlcat("Speech to Text", """\
The TRANSCRIBE command can take spoken audio, from the microphone
for example, and transcribe it into text.
""")

mlask(end=True, prompt="Press Enter and then say something")

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
        print("To update your key, please run ml configure azspeech.", file=sys.stderr)
        sys.exit(1)

mlask(begin="\n", end="\n")

# -----------------------------------------------------------------------
# Request text from console input.
# -----------------------------------------------------------------------

mlcat("Text to Speech", """\
Now we will convert that same text back to speech.
""")

text = result.text

mlask(end="\n")

# Synthesize the text to speech. When the following line is run expect
# to hear the synthesized speech.

result = speech_synthesizer.speak_text_async(text).get()
if str(result.reason) == "ResultReason.Canceled":
    print("The Azure Speech key is not correct. Please run ml configure azspeech to update your key.",  file=sys.stderr)
    sys.exit(1)

# -----------------------------------------------------------------------
# Translate language to other language
# -----------------------------------------------------------------------

mlcat("Speech Translation", """\
We can also translate English to other languages. Please speak some
English and we'll use the speech service to translate it to French.
""")

mlask(end="\n", prompt="Wait 1 second to speak after pressing Enter")
translate_speech_to_text("en-US", "fr", False, False, key, location)

# -----------------------------------------------------------------------
# Confirming that the speaker matches a known, or enrolled voice
# -----------------------------------------------------------------------

if RECOGNISE_FLAG:

    mlask(begin="\n", end="\n")
    mlcat("Speaker Recognition", """\
A speaker recognition system will build a model of a speaker based on samples
of the speaker. The system can then confirm the speaker matches an enrolled
voice.

For our demo we will hear three samples that enroll the speaker. A fourth
audio is then tested against the enrolled speaker.
""")

    first = os.path.join(os.getcwd(), "data/sample1.wav")
    second = os.path.join(os.getcwd(), "data/sample2.wav")
    third = os.path.join(os.getcwd(), "data/sample3.wav")
    fourth = os.path.join(os.getcwd(), "data/verify.wav")

    # Play the first audio.

    mlask(end="\n")
    mlcat("", """The first sample audio...
""")
    os.system(f'aplay {first} >/dev/null 2>&1')
    mlask(end="\n")

    # Play the second audio.
    
    mlcat("", """The second sample audio...
""")
    os.system(f'aplay {second} >/dev/null 2>&1')
    mlask(end="\n")

    # Play the third audio
    mlcat("", """The third sample audio...
""")
    os.system(f'aplay {third} >/dev/null 2>&1')

    mlcat("Verify the Speaker", """\
Now, we will insert the first three examples into the recognition system, and
use these samples to verify the fourth audio by its unique voice
characteristics.
""")
    mlask(end="\n")

    # Play the fourth audio.

    mlcat("", """The fourth audio to be verified...
""")
    os.system(f'aplay {fourth} >/dev/null 2>&1')
    recognise([first, second, third, fourth],  False, key)
    print("")
else:

    mlask(begin="\n", end="\n")
    mlcat("Speaker Recognition", f"""\
This service is currently (April 2021) only supported by the
'westus' region. Your current region is '{location}'.

You can create an Azure Speech resource for 'westus' if you want to use this
service and to utilise the RECOGNISE command.

Once the appropriate resource has been created replace the key
by running ml configure azspeech.
""")
