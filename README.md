# Azure Speech Capabilities

***Update 27 June 2020:*** The package *azspeech2txt* for the Azure Speech
to Text service has been renamed *azspeech*, to include text to speech
capabilities.

This [MLHub](https://mlhub.ai) package provides a quick introduction
to the pre-built Speech models provided through Azure's Cognitive
Services. This service can, for example, take an audio signal and
transcribes it to return the text. It also supports speech synthesis.

In addition to the demonstration this package provides a collection of
commands that turn the service into a useful command line tool for
transcribing from the microphone or from an audio file, and
synthesising speech.

A free Azure subscription allowing up to 5,000 transactions per month
is available from https://azure.microsoft.com/free/. After subscribing
visit https://ms.portal.azure.com and Create a resource under AI and
Machine Learning called Speech Services. Once created you can access
the web API subscription key and endpoint from the portal. This will
be prompted for in the demo.

This package is part of the Azure on MLHub suite. Please note that
these Azure models, unlike the MLHub models in general, use *closed
source services* which have no guarantee of ongoing availability and
do not come with the freedom to modify and share.

Visit the github repository for more details:
<https://github.com/gjwgit/azspeech>

## Quick Start

```console
$ wget https://github.com/realpython/python-speech-recognition/raw/master/audio_files/harvard.wav

$ ml transcribe azspeech
$ ml transcribe azspeech --file=harvard.wav

$ ml synthesize azspeech Welcome my friend, welcome to the machine.
$ ml synthesize azspeech --file=ai.txt
```

## Usage

- To install mlhub (Ubuntu)

		$ pip3 install mlhub

- To install and configure the demo:

		$ ml install   azspeech
		$ ml configure azspeech


## Command Line Tools

In addition to the *demo* command below, the package provides a number
of useful command line tools.

### *transcribe* from microphone

The *transcribe* command will listen for an utterance from the computer microphone
for up to 15 seconds and then transcribe it to standard output.

```console
$ ml transcribe azspeech
The machine learning hub is useful for demonstrating capability of 
models as well as providing command line tools.
```
We can pipe the output to other tools, such as to analyse the
sentiment of the spoken word. In the first instance you might say
*happy days* and in the second say *sad days*.

```console
$ ml transcribe azspeech | ml sentiment aztext
0.96

$ ml transcribe azspeech | ml sentiment aztext
0.07
```

### *transcribe* from --file

The *transcribe* command can take an audio (wav) file and transcribe
it to standard output. For large audio files this will take extra
time.

```console
$ wget https://github.com/realpython/python-speech-recognition/raw/master/audio_files/harvard.wav
$ ml transcribe azspeech --file=harvard.wav
The stale smell of old beer lingers it takes heat to bring out the odor.
A cold dip restore's health and Zest, a salt pickle taste fine with
Ham tacos, Al Pastore are my favorite a zestful food is the hot cross bun.
```

### *synthesize*

```console
$ ml synthesize azspeech Welcome my son, welcome to the machine.
$ ml synthesize azspeech --lang=fr-FR It's alright, we know where you've been.
$ ml synthesize azspeech --voice=en-AU-NatashaNeural You brought a guitar to punish your ma.

$ ml synthesize azspeech --file=short.txt
$ ml synthesize azspeech --lang=fr-FR --file=short.txt
$ ml synthesize azspeech --voice=en-AU-NatashaNeural --file=short.txt
$ ml synthesize azspeech --voice=fr-FR-DeniseNeural --file=short.txt
```

### Speaking French
```console
$ ml transcribe azspeech | ml translate aztranslate --to=fr | cut -d',' -f4- | ml synthesize azspeech --voice=fr-FR-HortenseRUS
```

## Demonstration

```console
$ ml demo azspeech 

=====================
Azure Speech Services
=====================

Welcome to a demo of the pre-built models for Speech provided
through Azure's Cognitive Services. This cloud service accepts audio
and then converts that into text which it returns locally.

The following file has been found and is assumed to contain
an Azure Speech Services subscription key and region. We will load 
the file and use this information.

    /home/kt/.mlhub/azspeech/private.txt

Say something...

> Recognized: Welcome to a demo of the prebuilt models for speech to
> text provided through azure's cognitive services. This cloud service 
> accepts audio and then converts that into text, which it returns locally.

Thank you for exploring the 'azspeech model.
```

As you can see I read the first paragraph from the screen and the
Azure Speech to Text service was quite accurate in its
transcription. If the accuracy for the particular accent is good then
it is quite suitable, for example, to be used as a dictation tool.

## Resources

* [Quick Start for
  Speech2Text](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/quickstart/python/from-microphone)
  
* [Try Out Text to
  Speech](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/#features)
  
* [Neural voice
  synthesis](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech)
  
* [Quick Start for
  Text2Speech](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstarts/text-to-speech-audio-file?tabs=ubuntu%2Cwindowsinstall&pivots=programming-language-python)
  
* [Quick Start Text2Speech Source
  Code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/quickstart/python/text-to-speech/quickstart.py)
  
* The Python code is based on the [Azure Speech Services Quick Start for
Python](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstart-python).

