# -*- coding: utf-8 -*-
#
# MLHub toolket for Azure Speech - Transcribe
#
# Time-stamp: <Sunday 2022-03-13 21:26:59 +1100 Graham Williams>
#
# Author: Graham.Williams@togaware.com
# Licensed under GPLv3.
# Copyright (c) Togaware Pty Ltd. All rights reserved.
#
# ml transcribe azspeech

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import os
import sys
import time
import wave
import click
import textwrap

import azure.cognitiveservices.speech as speechsdk

from azure.cognitiveservices.speech import SpeechRecognizer
from azure.cognitiveservices.speech.audio import AudioConfig

from mlhub.pkg import get_cmd_cwd, get_private

done = False


# -----------------------------------------------------------------------
# Command line argument and options
# -----------------------------------------------------------------------

@click.command()
@click.argument("filename",
                default=None,
                required=False,
                type=click.STRING)
@click.option("-l", "--lang",
              default=None,
              type=click.STRING,
              help="The language of the source audio.")
def cli(filename, lang):
    """Transcribe an audio WAV file or audio from the microphone.

Currently only WAV audio is supported for the FILENAME. If no FILENAME
is suppled then the audio is captured from the microphone.

The audio is sent off to the Auzue Cognitive Services to perform an
AI based transcription. The result is returned as text.

    """
    # ----------------------------------------------------------------------
    # Request subscription key and location from user.
    # ----------------------------------------------------------------------

    key, location = get_private()

    # -----------------------------------------------------------------------
    # Set up a speech configuration.
    # -----------------------------------------------------------------------

    speech_config = speechsdk.SpeechConfig(subscription=key, region=location)

    if lang:
        speech_config.speech_recognition_language = lang

    # -----------------------------------------------------------------------
    # Transcribe file or from microphone.
    # -----------------------------------------------------------------------

    if filename:
        path = os.path.join(get_cmd_cwd(), filename)
        if not os.path.exists(path):
            sys.exit(f"azspeech transcribe: File not found: {path}")

        # Test that we have a suitable WAV file.

        try:
            wave.open(path)
        except Exception:
            sys.exit(f"azspeech transcribe: File is not wav audio: {path}")

        # Create a callback to terminate the transcription once the full
        # audio has been transcribed.

        def stop_cb(evt):
            """Callback stop continuous recognition on receiving event (evt)"""
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

        audio_config = AudioConfig(use_default_microphone=False,
                                   filename=path)

        speech_recognizer = SpeechRecognizer(speech_config=speech_config,
                                             audio_config=audio_config)

        # Connect callbacks to the events fired by the speech
        # recognizer. Most are commented out as examples here to allow
        # tracing if you are interested in exploring the interactions with
        # the server.
        #
        # speech_recognizer.recognizing.connect(lambda evt:
        #                                 print('RECOGNIZING: {}'.format(evt)))
        # speech_recognizer.session_started.connect(lambda evt:
        #                                 print('STARTED: {}'.format(evt)))
        # speech_recognizer.session_stopped.connect(lambda evt:
        #                                 print('STOPPED {}'.format(evt)))
        # speech_recognizer.canceled.connect(lambda evt:
        #                                  print('CANCELED {}'.format(evt)))

        # This callback provides the actual transcription.

        def respond(evt):
            print(f'{textwrap.fill(evt.result.text)}\n')

        speech_recognizer.recognized.connect(respond)

        # Stop continuous recognition on either session stopped or canceled
        # events.

        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition, and then perform
        # recognition. For long-running recognition we use
        # start_continuous_recognition().

        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

    else:

        speech_recognizer = SpeechRecognizer(speech_config=speech_config)

        # -----------------------------------------------------------------------
        # Trasnscribe spoken words from the system microphone.
        # -----------------------------------------------------------------------

        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("{}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print(f"No speech could be recognized: {result.no_match_details}")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: f{cancellation_details.error_details}")
                print("Update your key with 'ml configure azspeech'.",
                      file=sys.stderr)
                sys.exit(1)


if __name__ == "__main__":
    cli(prog_name="transcribe")
