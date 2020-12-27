import requests
import hashlib
import sys

def request(query):
  url = 'https://api.pwnedpasswords.com/range/' + query
  res = requests.get(url)
  if res.status_code != 200:
    raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
  return res

def count(hashes, hash_to_check):
  hashes = (line.split(':') for line in hashes.text.splitlines())
  for h, count in hashes:
    if h == hash_to_check:
      return count
  return 0

def apicheck(password):
  sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
  first5_char, tail = sha1password[:5], sha1password[5:]
  response = request(first5_char)
  return count(response, tail)

def main(args):
  for password in args:
    count = apicheck(password)
    if count:
      print(f'{password} was hacked {count} times... ')
    else:
      print(f'{password} was NOT found. ')
  return 'done!'

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))

