from tld import get_tld, get_fld
from urllib.parse import urlparse
from capture.har import Har
from database.observer import Observer
from database.site import Site
import json
from os.path import splitext

# COUNTRIES = ['KR', 'US', 'VN', 'ID']
COUNTRIES = ['VN']

har = Har()
observer = Observer()
site = Site()
# f = open("label_f_t2.txt", "w")

d = []


def capture(url):
    origin = get_fld('http://%s' % url, fail_silently=True)
    if origin is None:
        print("error: TldDomainNotFount")
        pass
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
        req_origin = get_fld(url, fail_silently=True)

        if req_origin is None:
            print("error: TldDomainNotFount")
            pass

        print(url)
        # print(req_origin)

        u = urlparse(url)
        info['sub_domain'] = u.netloc
        info['path'] = u.path
        info['query_string'] = req.get('queryString', {})

        e_path = u.path
        ext = splitext(e_path)[1]
        # print(ext)

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

    label['label_t'] = label_t
    label['label_f'] = label_f

    d.append(label)

    # f.write(json.dumps(label, indent=2))

    # f.write(url)

    # har.clear("facebook.com")


def main():
    # with open('dataset.json', 'r', encoding="utf-8") as data_file:
    #   old_data = json.load(data_file)

    for c in COUNTRIES:
        offset = 0  # 872 #start #891
        limit = 100

        # offset = offset + limit
        while True:
            sites = site.get_sites(country=c, offset=offset, limit=limit)

            if len(sites) == 0:
                break
                # breakcapture(s['domain'])

            offset = offset + limit
            print(offset)
            cnt = 0
            for s in sites:
                print(cnt)
                capture(s['domain'])
                with open('dataset2.json', 'w', encoding="utf-8") as make_file:
                    json.dump(d, make_file, ensure_ascii=False, indent='\t')
                # with open('dataset.json', 'w', encoding="utf-8") as make_file:
                #   json.dump(old_data+d, make_file, ensure_ascii=False, indent='\t')
                cnt += 1


if __name__ == '__main__':
    main()
