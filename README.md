Azure Speech to Text
====================

This [MLHub](https://mlhub.ai) package provides a quick demonstration
of the pre-built Speech to Text model provided through Azure's
Cognitive Services. This service takes an audio signal and transcribes
it to return the text.

An Azure subscription is required and a free Azure subscription
allowing up to 5,000 transactions per month is available from
https://azure.microsoft.com/free/. Once set up visit
https://ms.portal.azure.com and Create a resource under AI and Machine
Learning called Speech Services. Once created you can access the web
API subscription key from the portal. This will be prompted for in the
demo.

Please note that this is *closed source software* which limits your
freedoms and has no guarantee of ongoing availability.

Visit the github repository for more details:
<https://github.com/gjwgit/azspeech2txt>

The Python code is based on the [Azure Speech Services Quick Start for
Python](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstart-python)

Usage
-----

To install and run the pre-built model:

    $ pip3 install mlhub
    $ ml install   azspeech2txt
    $ ml configure azspeech2txt
    $ ml demo      azspeech2txt

