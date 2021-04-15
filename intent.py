from mlhub.pkg import azkey
import os
import azure.cognitiveservices.speech as speechsdk

print("Say something...")

"""performs one-shot intent recognition from input from the default microphone"""

# ----------------------------------------------------------------------
# Request subscription key and location from user for the intent recognizer
# This uses the Language Understading key, not the Speech Services Key
# ----------------------------------------------------------------------

SERVICE = "Language Understanding (LUIS) "
KEY_FILE = os.path.join(os.getcwd(), "private_luis.txt")

key, location = azkey(KEY_FILE, SERVICE, connect="location")

intent_config = speechsdk.SpeechConfig(subscription=key, region=location)

# ----------------------------------------------------------------------
# Set up the intent recognizer
# ----------------------------------------------------------------------

intent_recognizer = speechsdk.intent.IntentRecognizer(speech_config=intent_config)
print("please provide your Language Understanding App id: ")

id = input()

# ----------------------------------------------------------------------
# set up the intents that are to be recognized. These can be a mix of simple
# phrases and intents specified through a LanguageUnderstanding Model.
# Here, we include all the intents.
# ----------------------------------------------------------------------

model = speechsdk.intent.LanguageUnderstandingModel(app_id=id)

intent_recognizer.add_all_intents(model)

# ----------------------------------------------------------------------
# Starts intent recognition, and returns after a single utterance is recognized.
# The end of a single utterance is determined by listening for silence at
# the end or until a maximum of 15 seconds of audio is processed. It returns
# the recognition text as result.
# Note: Since recognize_once() returns only a single utterance, it is suitable
# only for single shot recognition like command or query.
# ----------------------------------------------------------------------

intent_result = intent_recognizer.recognize_once()

if intent_result.reason == speechsdk.ResultReason.RecognizedIntent:
    print("Recognized: \"{}\" with intent id `{}`".format(intent_result.text, intent_result.intent_id))
elif intent_result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(intent_result.text))
elif intent_result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(intent_result.no_match_details))
elif intent_result.reason == speechsdk.ResultReason.Canceled:
    print("Intent recognition canceled: {}".format(intent_result.cancellation_details.reason))
    if intent_result.cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(intent_result.cancellation_details.error_details))

