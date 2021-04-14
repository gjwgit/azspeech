import os
import argparse
import requests

from mlhub.pkg import azkey
from mlhub.utils import get_cmd_cwd

import wave

# -----------------------------------------------------------------------
# Process the command line.
# -----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    '--file',
    "-f",
    action='append',
    required=True,
    help='wav input file')

option_parser.add_argument(
    '--verify',
    "-v",
    required=True,
    help='the wav file which wants to verify')

args = option_parser.parse_args()

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

SERVICE   = "Speech"
KEY_FILE  = os.path.join(os.getcwd(), "private.txt")

key, location = azkey(KEY_FILE, SERVICE, connect="location", verbose=False)

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

profile_id = result.json()['profileId']
enroll_url = create_profile_url + "/" + profile_id + "/enrollments"
enroll_header = {
    'Ocp-Apim-Subscription-Key': key,
    'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000'
}

# Add three sample audios
for i in range(0, 3):
    path = os.path.join(get_cmd_cwd(), args.file[i])
    w = wave.open(path, "rb")
    # Convert audio file into binary format
    binary_data = w.readframes(w.getnframes())
    w.close()
    result = requests.post(enroll_url, data=binary_data, headers=enroll_header)

# -----------------------------------------------------------------------
# Verify the audio
# -----------------------------------------------------------------------

verify_url = create_profile_url + "/" + profile_id + "/verify"
verify_header = {
    'Ocp-Apim-Subscription-Key': key,
    'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000'
}

path = os.path.join(get_cmd_cwd(), args.verify)
w = wave.open(path, "rb")
# Convert audio file into binary format
binary_data = w.readframes(w.getnframes())
w.close()
result = requests.post(verify_url, data=binary_data, headers=verify_header)
print("Result: " + result.json()['recognitionResult'])
print("Score: " + str(result.json()['score']))

# -----------------------------------------------------------------------
# Delete the voice profile
# -----------------------------------------------------------------------

delete_url = create_profile_url + "/" + profile_id
delete_header = {
    'Ocp-Apim-Subscription-Key': key,
}
result = requests.delete(delete_url, headers=delete_header)

