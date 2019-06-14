Azure Speech to Text
====================

This [MLHub](https://mlhub.ai) package provides a quick demonstration
of the pre-built Speech to Text model provided through Azure's
Cognitive Services. This service takes an audio signal and transcribes
it to return the text.

In addition to the demonstration this package provides a collection of
commands that turn the service into a useful command line tool to
transcribe from the microphone or from an audio file.

A free Azure subscription allowing up to 5,000 transactions per month
is available from https://azure.microsoft.com/free/. Once set up visit
https://ms.portal.azure.com and Create a resource under AI and Machine
Learning called Speech Services. Once created you can access the web
API subscription key from the portal. This will be prompted for in the
demo.

Please note that this is *closed source software* which limits your
freedoms and has no guarantee of ongoing availability.

Visit the github repository for more details:
<https://github.com/gjwgit/azspeech2txt>

The Python code is based on the [Azure Speech Services Quick Start for
Python](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstart-python).

Usage
-----

- To install mlhub 

```console
$ pip3 install mlhub
```

- To install and configure:

```console
$ ml install   azspeech2txt
$ ml configure azspeech2txt
```

Command Line Tools
------------------

In addition to the *demo* presented below, the *azspeech2txt* package
provides a number of useful command line tools.

The *listen* command will listen for an utterance from the microphone
for 15 seconds and then transcribe it to standard output.

```console
$ ml listen azspeech2txt
The machine learning hub is useful for demonstrating capability of 
models as well as providing command line tools.
```

The *transcribe* command takes an audio file and transcribes it to
standard output. For large audio files this can take some time.

```console
$ ml transcribe azspeech2txt recording.wav
The stale smell of old beer lingers it takes heat to bring out the odor.
A cold dip restore's health and Zest, a salt pickle taste fine with
Ham tacos, Al Pastore are my favorite a zestful food is the hot cross bun.
```

Demonstration
---------------

```console
$ ml demo azspeech2txt 
====================
Azure Speech to Text
====================

Welcome to a demo of the pre-built models for Speech to Text provided
through Azure's Cognitive Services. This cloud service accepts audio
and then converts that into text which it returns locally.

The following file has been found and is assumed to contain
an Azure Speech Services subscription key and region. We will load 
the file and use this information.

    /home/kt/.mlhub/azspeech2txt/private.py

Say something...

> Recognized: Welcome to a demo of the prebuilt models for speech to
> text provided through azure's cognitive services. This cloud service 
> accepts audio and then converts that into text, which it returns locally.

Thank you for exploring the 'azspeech2txt' model.
```

As you can see I read the first paragraph from the screen and the
Azure Speech to Text service was quite accurate in its
transcription. It is quite suitable, for example, to be used as a
dictation tool.
