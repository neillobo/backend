import requests
urls_to_test = [] # specify these
for url in x:
  response_status_code = requests.get(url).status_code
  if response_status_code != 200:
    print 'The url %s returned a status code of %d' % (url, response_status_code)

