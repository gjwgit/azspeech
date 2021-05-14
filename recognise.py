from mlhub.utils import get_cmd_cwd, get_private
import argparse
import os
import requests
import sys
import wave


def recognise(file, verify, single_line, key):
    # -----------------------------------------------------------------------
    # Create verification voice profile
    # -----------------------------------------------------------------------

    create_headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }

    endpoint = 'https://westus.api.cognitive.microsoft.com/'
    path = 'speaker/verification/v2.0/text-dependent/profiles'
    create_profile_url = endpoint + path
    result = requests.post(create_profile_url, data="{\"locale\":\"en-US\"}", headers=create_headers)

    # -----------------------------------------------------------------------
    # Enroll the voice profile (3 samples)
    # -----------------------------------------------------------------------

    # If the location is not westus, profileId will not be found.
    try:
        profile_id = result.json()['profileId']
    except:
        if result.json()['error']['code']=='401':
            print("The Azure subscription key is not correct, please run ml configure azspeech to update your key. ",  file=sys.stderr)
        else:
            error = result.json()['error']['message']
            print(f"Error: {error}",  file=sys.stderr)
        sys.exit(1)

    enroll_url = create_profile_url + "/" + profile_id + "/enrollments"
    enroll_header = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000'
    }

    # Add three sample audios
    for i in range(0, 3):
        path = os.path.join(get_cmd_cwd(), file[i])

        try:
            w = wave.open(path, "rb")
        except FileNotFoundError:
            print(f"Error: wrong sample file location. \n{file[i]}", file=sys.stderr)
            sys.exit(1)

        # Convert audio file into binary format
        binary_data = w.readframes(w.getnframes())
        w.close()
        result = requests.post(enroll_url, data=binary_data, headers=enroll_header)

        # Catch the invalid audios
        try:
            if result.json()['error']['message']:
                error = result.json()['error']['message']
                print(f"The sample audio file {file[i]} error: {error}", file=sys.stderr)
        except:
            pass
        else:
            sys.exit(0)

    # -----------------------------------------------------------------------
    # Verify the audio
    # -----------------------------------------------------------------------

    verify_url = create_profile_url + "/" + profile_id + "/verify"
    verify_header = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000'
    }

    path = os.path.join(get_cmd_cwd(), verify)

    try:
        w = wave.open(path, "rb")
    except FileNotFoundError:
        print(f"Error: wrong verification file location.\n{verify}", file=sys.stderr)
        sys.exit(1)

    # Convert audio file into binary format
    binary_data = w.readframes(w.getnframes())
    w.close()
    result = requests.post(verify_url, data=binary_data, headers=verify_header)

    try:
        if not single_line:
            print("Result: " + result.json()['recognitionResult'])
            print("Score: " + str(result.json()['score']))
        else:
            print(result.json()['recognitionResult'] + ", " + str(result.json()['score']))
    except:
        error = result.json()['error']['message']
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    # -----------------------------------------------------------------------
    # Delete the voice profile
    # -----------------------------------------------------------------------

    delete_url = create_profile_url + "/" + profile_id
    delete_header = {
        'Ocp-Apim-Subscription-Key': key,
    }
    requests.delete(delete_url, headers=delete_header)


if __name__ == "__main__":

    # -----------------------------------------------------------------------
    # Process the command line.
    # -----------------------------------------------------------------------

    option_parser = argparse.ArgumentParser(add_help=False)

    option_parser.add_argument(
        '--file',
        "-f",
        action='append',
        help='wav input file')

    option_parser.add_argument(
        '--verify',
        "-v",
        help='the wav file which wants to verify')

    args = option_parser.parse_args()

    # ----------------------------------------------------------------------
    # Request subscription key and location from user.
    # ----------------------------------------------------------------------

    PRIVATE_FILE = "private.json"

    path = os.path.join(os.getcwd(), PRIVATE_FILE)

    private_dic = get_private(path, "azspeech")

    key = private_dic["Azure subscription"]["key"]
    location = private_dic["Azure subscription"]["location"]

    RECOGNISE_FLAG = True

    if location != "westus":
        RECOGNISE_FLAG = False

    sample = args.file
    target = args.verify

    # ----------------------------------------------------------------------
    # Run RECOGNISE
    # ----------------------------------------------------------------------

    if RECOGNISE_FLAG:
        recognise(sample, target, True, key)
    else:
        print("This service currently only supported in Azure Speech resources "
              "created in the westus region. \nIf you want to use this service, please "
              "create another resource under westus region.\n",
              "To update the key and location, please run ml configure azspeech.",
              file=sys.stderr)
