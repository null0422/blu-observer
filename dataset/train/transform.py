# -*- coding: utf-8 -*-
import re
from util.urlutil import UrlUtil

class Transform(object):
  def __init__(self):
    super(Transform,self).__init__()
    self.urlUtil = UrlUtil()
    with open("./dataset/train/except_words.dat") as f1:
      self.words = [line.strip() for line in f1]
    with open("./dataset/train/except_keywords.dat") as f2:
      self.keywords = [line.strip() for line in f2]

  def clean(self, data):
    sentence = []

    label = data.get('label')
    sub_domain = data.get('sub_domain', None)
    sub_domain_name = self.urlUtil.remove_tld(sub_domain)
    sub_domain_name = self.split_in_string(sub_domain_name)
    # print(sub_domain_name)
    sentence.extend(sub_domain_name)
    path = data.get('path', None)


    label = data.get('label')

    path = path.lower()
    # self.normalize(path)
    # sentence.extend(path.split('/'))
    if self.is_normal_content(path) is False:
      path = self.remove_digits(path)
      paths = self.split_path(path)
      paths = self.remove_value(paths)
      paths = self.split_in_list(paths)
      # print(paths)

    sentence = list(filter(None, sentence))
    sentence = list(set(sentence))
    self.remove_except_words(sentence)
    self.remove_except_keywords(sentence)
    self.remove_symbol(sentence)
    sentence = self.remove_single_char(sentence)
    sentence.insert(0,label)
    # print(sentence)
    return sentence

  def remove_single_char(self, data):
    data = [i for i in data if len(i) > 1]
    return data

  def remove_symbol(self, data):
    ss = []
    for s in data:
      ss.extend(self.remove_special_chars(s))

  def remove_except_words(self, data):
    for word in self.words:
      for s in data:
        if word in data:
          data.remove(word)

  def remove_except_keywords(self, data):
    for word in self.keywords:
      for d in data:
        if d.find(word) > -1:
          data.remove(d)

  def remove_digits(self, s):
    return ''.join([i for i in s if not i.isdigit()])

  def remove_value(self, paths):
    p = []
    for s in paths:
      s = s.split('=')[0]
      p.append(self.replace_percent(s))
    return p

  def split_in_list(self, paths):
    p = []
    for s in paths:
      s = s.replace('-', ' ').replace('_', ' ').replace('.', ' ').split()
      p.extend(s)
    return p

  def split_in_string(self, s):
    return s.replace('-', ' ').replace('_', ' ').replace('.', ' ').split()

  def split_path(self, s):
    return s.split('/')

  def is_normal_content(self, s):
    s = s.lower()
    ext = [".jpg", ".jpg_s", ".jpeg", ".css", ".html", ".gif", ".gif_s", \
           ".png", ".png_s", ".swf", ".svg", ".wmv", ".ttf", ".woff", ".woff2"]
    return s.endswith(tuple(ext))

  def replace_percent(self, s):
    return s.replace('%', ' ')

  def remove_special_chars(self, s):
    return s.replace(';', ' ').replace(':', ' ').replace('&', 'at')

  def normalize(self, s):
    s = s.lower()
    # Replace ips
    s = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ' _ip_ ', s)
    # Isolate punctuation
    s = re.sub(r'([\'\"\.\(\)\!\?\-\\\/\,])', r' \1 ', s)
    # Remove some special characters
    s = re.sub(r'([\;\:\|•«\n])', ' ', s)
    # Replace numbers and symbols with language
    s = s.replace('&', ' and ')
    s = s.replace('@', ' at ')
    return s
