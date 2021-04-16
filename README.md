# Azure Speech Capabilities

This [MLHub](https://mlhub.ai) package provides a demonstration and
command line tools built from the pre-built Speech models provided
through Azure's Cognitive Services. This service can support speech 
to text, text to speech, speech translation and Speaker Recognition 
capabilities.

An Azure subscription is required, allowing up to 5,000 free
transactions per month (https://azure.microsoft.com/free/). Through
the [Azure Portal](https://ms.portal.azure.com) create a Speech
resource and use the resulting key and endpoint from the portal for
the *demo*. 

**Note**: we highly recommend choosing westus in Location because Speaker Recognition
can only work under this area. 

**Warning** Unlike the MLHub models in general these Azure models use
*closed source services* which have no guarantee of ongoing
availability and do not come with the freedom to modify and share.

**Warning** This cloud based service sends all of your text (for
synthesis) and audio (for transcription) to the cloud.

The azspeech source code is available from
<https://github.com/gjwgit/azspeech>.

## Quick Start

```console
$ wget https://github.com/realpython/python-speech-recognition/raw/master/audio_files/harvard.wav

$ ml synthesize azspeech Welcome my friend, welcome to the machine.
$ ml synthesize azspeech --file=ai.txt
$ ml synthesize azspeech --output=spoken.wav

$ ml transcribe azspeech
$ ml transcribe azspeech --file=harvard.wav

$ ml translate azspeech --target=fr
$ ml translate azspeech --original=zh-CN --target=fr --ouput=spoken.wav

$ ml recognise azspeech --file=sample.wav --file=sample2.wav --file=sample3.wav --verify=verify.wav
```

## Usage

- To install mlhub (Ubuntu):

		$ pip3 install mlhub
		$ ml configure

- To install, configure, and run the demo:

		$ ml install   azspeech
		$ ml configure azspeech
		$ ml readme    azspeech
		$ ml commands  azspeech
		$ ml demo      azspeech
		
- Command line tools:

		$ ml synthesize azspeech [(--file|-f) <txt file>] [(--lang|-l) <lang>] [(--voice|-v) <voice>] [sentence] [(--output|-o) <wav file>]
		$ ml transcribe azspeech [(--file|-f) <wav file>]
		$ ml translate azspeech [(--original) <from language code>] [(--target) <to language code>] [(--output) <wav file>]
		$ ml recognise azspeech [(--file) <sample wav file>] [(--file) <sample2 wav file>] [(--file) <sample3 wav file>] [(--verify) <verify wav file>]

## Command Line Tools

In addition to the *demo* command below, the package provides a number
of useful command line tools.

### *synthesize* to speaker

The *synthesize* command will generate spoken word audio from supplied
text and play the audio on the system's default audio output. It has the option 
to save an audio (wav) file. 

```console
$ ml synthesize azspeech Welcome my son, welcome to the machine.
$ ml synthesize azspeech --lang=fr-FR It's alright, we know where you've been.
$ ml synthesize azspeech --voice=en-AU-NatashaNeural You brought a guitar to punish your ma.

$ echo It's alright, we told you what to dream | ml synthesize azspeech

$ ml synthesize azspeech --file=short.txt
$ ml synthesize azspeech --output=spoken.wav
$ ml synthesize azspeech --lang=de-DE --file=short.txt
$ ml synthesize azspeech --voice=fr-FR-DeniseNeural --file=short.txt
```

### *transcribe* from microphone

The *transcribe* command will listen for an utterance from the computer microphone
for up to 15 seconds and then transcribe it to standard output. After
issuing the command it waits for you to type input and after hitting
the Engter key it sends that text off to be transcribed.

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
time. Currently only wav files are supported through the command line
(though the service also supports mp3, ogg, and flac).

```console
$ wget https://github.com/realpython/python-speech-recognition/raw/master/audio_files/harvard.wav
$ ml transcribe azspeech --file=harvard.wav
The stale smell of old beer lingers it takes heat to bring out the odor.
A cold dip restore's health and Zest, a salt pickle taste fine with
Ham tacos, Al Pastore are my favorite a zestful food is the hot cross bun.
```

### A Pipeline for Speaking French
```console
$ ml transcribe azspeech | ml translate aztranslate --to=fr | cut -d',' -f4- | ml synthesize azspeech --voice=fr-FR-HortenseRUS
```
### Speech Translation

The *translate* command can listen for  an utterance from the computer microphone
for up to 15 seconds and then translate it to other language. It has the option to save
the output audio (wav) file. The default input language is English, users can choose a different language 
as they prefer. 

```console
$ ml translate azspeech --target fr
$ ml translate azspeech --original zh-CN --target fr
$ ml translate azspeech --original zh-CN --target fr --output out.wav
```

**Note**: The language code in *--original* should choose from Locale in Speech-to-text table:
<https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#speech-to-text>,
while *--target* should choose from Language Code in Text languages table:
<https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#speech-translation>

### Speaker Recognise

The *recognise* command can verify if a speaker matches a enrolled voice. Four audios are required. The users should
choose the same passphrase in these audios. See the [reference doc](https://docs.microsoft.com/en-us/rest/api/speakerrecognition/#text-dependent-speaker-verification) 
for a list of supported passphrases.

The first three are the sample audios, and the fourth one will be the audio that needs to verify. 
*result* and *score* are the two components in the output. *result* is "Accept" or "Reject" 
and *score* is the similarity with range 0-1. The "Accept" or "Reject" response is a result combining 
both the speaker verification result and speech recognition result, while the similarity score only 
measures the voice similarity. 

```console
$ ml recognise azspeech --file sample1.wav --file sample2.wav --file sample3.wav --verify verify.wav
```



## Demonstration

```console
$ ml demo azspeech 

===============
Speech Services
===============

Welcome to a demo of the pre-built models for Speech provided through
Azure's Cognitive Services. The Speech cloud service  supports speech
to text and text to speech capabilities.

The following file has been found and is assumed to contain an Azure 
subscription key and location for Speech. We will load 
the file and use this information.

    /home/gjw/.mlhub/azspeech/private.txt

Press Enter and then say something: 

> Recognized: Welcome to a demo of the prebuilt models speech provided 
> through Azure as cognitive services. The speech cloud service provides
> speech to text and text to speech capabilities.

Press Enter to continue: 

Now type text to be spoken. When Enter is pressed you will hear the result.

> Welcome to a demo of the prebuilt models for speech.

==================
Speech Translation
==================

This part is to translate English to other language. Now please speak
English. This speech service will translate it to French.

Press Enter to continue: 

Say something...
Recognized: "Hello."
Translated into "fr": Bonjour.

Press Enter to continue: 

===================
Speaker Recognition
===================

This part is the act of confirming that a speaker matches a enrolled
voice. Now you will hear four audios. The first three will be the
sample audios, and the fourth one will be the audio that needs to
compare against them.

Press Enter to continue: 

 The first sample audio...

Press Enter to continue: 

 The second sample audio...

Press Enter to continue: 

 The third sample audio...

Press Enter to continue: 

 The fourth audio that needs to verify...

Press Enter to continue: 

==============
Get the result
==============

Now, we will insert the first three examples into our recognition
system, and use these samples to verify the fourth audio by its
unique voice characteristics.

Press Enter to continue: 

Result: Accept
Score: 0.8664135336875916

```

The first paragraph from the screen was read and the Azure Speech to
Text service was mostly accurate in its transcription. 

For synthesis
the same text was used and could be heard through the system speakers.

For speak translation, it will show both language's transcribed words
and play the audio for the target language. 

For Speaker Recognition, four audios will be played orderly, and the 
results will be shown after that. 

## Resources

* [MLHub](https://mlhub.ai)

* [Speech Services
  Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)

* [Supported
  Languages](https://docs.microsoft.com/en-gb/azure/cognitive-services/speech-service/language-support)

* [Python code for Speech Recognizer:
  Speech2Text](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/quickstart/python/from-microphone)
  
* [Python code for Speech Synthesizer:
  Text2Speech](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/quickstart/python/text-to-speech)
  
 
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)  
[This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/)
