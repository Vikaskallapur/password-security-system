import hashlib
import requests

def check_breach(password: str):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        return False, 0

    hashes = response.text.splitlines()
    for line in hashes:
        h, count = line.split(":")
        if h == suffix:
            return True, int(count)

    return False, 0
