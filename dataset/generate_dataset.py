from tld import get_tld, get_fld
from urllib.parse import urlparse
from capture.har import Har
from database.observer import Observer
from database.site import Site


f = open('list.txt', 'w')

COUNTRIES = ['KR', 'US', 'VN', 'ID']

har = Har()
observer = Observer()
site = Site()


def capture(url):
  origin = get_fld('http://%s' % url)
  # print(origin)

  label = {
    'domain': url,
    'label_f': None,
    'label_t': None
  }

  label_t = []
  label_f = []

  data = har.capture(url)

  entries = data['log']['entries']

  for entry in entries:
    info = {
      'sub_domain': None,
      'path': None,
      'query_string': None
    }

    req = entry['request']
    url = req['url']
    req_origin = get_fld(url)

    u = urlparse(url)
    info['sub_domain'] = u.netloc
    info['path'] = u.path
    info['query_string'] = req.get('queryString', {})

    if origin != req_origin:
      # print('req_origin', req_origin)
      # print('sub_comain', sub_domain)
      black = observer.get_black(req_origin)

      if black == None:
        b = observer.get_black(info['sub_domain'], src='blu')
        if b != None:
          whites = b.get('whites', [])
          if origin in whites:
            # print('white 1')
            label_t.append(info)
          else:
            label_f.append(info)
      else:
        whites = black.get('whites', [])
        if origin in whites:
          # print('white 2')
          label_t.append(info)
        else:
          label_f.append(info)
    else:
      label_t.append(info)
          
  f.close()
      

  label['label_t'] = label_t
  label['label_f'] = label_f
  print(label)
  f.write(label)
  # har.clear("facebook.com")

def main():
  for c in COUNTRIES:
    offset = 0
    limit = 100
    while True:
      sites = site.get_sites(country=c, src='blu', offset=offset, limit=limit)

      if len(sites) == 0:
        break

      for s in sites:
        capture(s['domain'])


if __name__ == '__main__':
  main()
