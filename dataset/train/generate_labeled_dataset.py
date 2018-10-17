# -*- coding: utf-8 -*-

import traceback
from util.urlutil import UrlUtil
from database.labels import Labels
from dataset.train.transform import Transform

LABEL_T = '__label__t'
LABEL_F = '__label__f'


urlUtil = UrlUtil()
transform = Transform()
labels = Labels()

def make_text(data):
  text, p, l = transform.clean(data)
  # print('domain = ', text)
  # print('path = ', p)
  d = ''
  pa = ''
  for i in text:
    d = d  + i
  for i in p:
    pa = pa + i

  txt = l + ' ' + d + pa

  return txt

def generate():
  try:
    offset = 0
    limit = 100
    with open('labled_dataset.txt', 'w') as f:
      while True:
        data = labels.get_labels(offset=offset, limit=limit)

        if len(data) == 0:
          break

        for d in data:
          t = make_text(d)
          print(t)
          f.write(t + '\n')

        offset = offset + limit

  except Exception as ex:
    traceback.print_exc()
    print(ex)

  f.close()

if __name__ == '__main__':
  generate()
