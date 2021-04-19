# Import the required libraries.

import os
import azure.cognitiveservices.speech as speechsdk
import argparse
from mlhub.pkg import azkey
import pandas
import sys

# -----------------------------------------------------------------------
# Process the command line
# -----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

# Currently only wav supported here. For mp3 some extra configuration
# required. See

option_parser.add_argument(
    '--original', "-f",
    help='original language')

option_parser.add_argument(
    '--target', "-t",
    help='target language')

option_parser.add_argument(
    '--output', "-o",
    help='path to an audio file to save. The file type should be wav')

args = option_parser.parse_args()

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

if args.original:
    pass
else:
    args.original = "en-US"

SERVICE = "Speech"
KEY_FILE = os.path.join(os.getcwd(), "private.txt")

speech_key, service_region = azkey(KEY_FILE, SERVICE, connect="location", verbose=False)

# ----------------------------------------------------------------------
# Get language code. "Original": is from Loale in Speech-to-text table.
# (https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#speech-to-text)
# "target": is from Language Code in Text languages table.
# (https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#speech-translation)
# Make sure the text language in Text Language table exists in Neural voices
# table.
# ----------------------------------------------------------------------

language_to_voice_map = {}
dataframe_speech = pandas.read_csv("text-to-speech.txt",delimiter="\t")

for index, row in dataframe_speech.iterrows():
    if row[1] == "zh-HK":
        language_code = "yue"
    elif row[1] == "zh-CN":
        language_code = "zh-Hant"

    else:
        language_code = row[1][0:2]

    language_to_voice_map[language_code] = row[3]

# ----------------------------------------------------------------------
# Translate the speech to another language speech
# ----------------------------------------------------------------------


def translate_speech_to_text(from_language, to_language, single_line):
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key, region=service_region)

    translation_config.speech_recognition_language = from_language
    translation_config.add_target_language(to_language)

    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config)

    result = recognizer.recognize_once()
    synthesize_translations(to_language, single_line, result=result)


def synthesize_translations(to_language, single_line, result):
    if not single_line:
        print(f'Recognized: "{result.text}"')
        try:
            translation = result.translations[to_language]
        except Exception as e:
            print(f"Error:{e}.")
            print("Error: wrong original or target language code. For original language code, please choose one from "
                  "Loale in Speech-to-text table"
                  "(https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#speech-to-text).\n"
                  "For target language code, please choose one from Language Code in Text languages table"
                  "(https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#speech-translation)")
            sys.exit(1)
        print(f'Translated into "{to_language}": {translation}')
    else:
        try:
            translation = result.translations[to_language]
        except Exception as e:
            print(f"Error:{e}.")
            print("Error: wrong original or target language code. For original language code, please choose one from "
                  "Loale in Speech-to-text table"
                  "(https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#speech-to-text).\n"
                  "For target language code, please choose one from Language Code in Text languages table"
                  "(https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#speech-translation)")
            sys.exit(1)
        print(f'Recognized: "{result.text}". Translated into "{to_language}": {translation}')

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    try:
        speech_config.speech_synthesis_voice_name = language_to_voice_map.get(to_language)
    except:
        print("Error: This target language doesn't have speech.")
        sys.exit(1)


    if args.output:
        audio_config = speechsdk.audio.AudioOutputConfig(filename=args.output)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    else:
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    speech_synthesizer.speak_text_async(translation).get()


from_language = args.original
to_language = args.target

if __name__ == "__main__":
    from_language = args.original
    to_language = args.target
    translate_speech_to_text(from_language, to_language, True)
