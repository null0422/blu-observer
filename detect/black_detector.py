from dataset.train.transform import Transform
from urllib.parse import urlparse
import fasttext

transform = Transform()

def get_data(url):

    # Need to implement retrieve sub_domain & path from the url

    if url.startswith('http') != True:
      url = 'http://' + url
    u = urlparse(url)
    sub_domain = u.netloc
    path = u.path

    return sub_domain, path

def inferrence(url):

    sub_domain, path = get_data(url)

    data ={
        "sub_domain": sub_domain,
        "path": path
    }
    text = transform.clean(data)
    temp = []
    txt = []

    for i in range(1,len(text)):
        txt.append(text[i])

    temp.append(' '.join(txt))
    print(temp)
    return model(temp)

def model(text):

    classifier = fasttext.load_model('./detect/random_model2.bin', label_prefix='__label__')

    labels = classifier.predict_proba(text, k=1)
    print(labels)

    if labels[0][0][0] is 't':
        return True
    else:
        return False

if __name__ == '__main__':
  url = 'www.naver.com/abd/dskfias'
  # sub_domain = 'www.naver.com'
  # path = '/adb/dskfjas'
  result = inferrence(url)
  print(result)