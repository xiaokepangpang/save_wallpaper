# -*- coding: utf-8 -*-
#
# @Time : 2020/4/12 10:26
#
# @Author : Zheng Hengbing
#
# @File : save_wallpaper.py

import cv2
import json
import hashlib
import os
import winreg

class SaveWallpaper(object):

  def __init__(self, source_folder, target_folder):
    self.__source = os.path.realpath(source_folder)
    self.__target = os.path.realpath(target_folder)
    self.__config_file = "exists.json"
    print(f"source path: {self.__source}")
    print(f"target path: {self.__target}")
    config_path = os.path.join(target_path, self.__config_file)
    if os.path.exists(config_path):
      with open(os.path.join(target_path, self.__config_file)) as f:
        self.__exists_set = set(json.loads(f.read()))
    else:
      print(f"no {self.__config_file} detected, start init...")
      self.init_exist_set(target_path)
      print("init success")

  def get_file_hash(self, file_content):
    if not file_content:
      return None
    value = hashlib.sha256(file_content)
    return value.hexdigest()

  def get_img_resolution(self, img_path):
    image = cv2.imread(img_path)
    return image.shape[:2]

  def does_file_exist(self, file_content):
    file_hash = self.get_file_hash(file_content)
    return file_hash in self.__exists_set

  def init_exist_set(self, folder):
    self.__exists_set = set([])
    all_file = self.get_all_file(folder)
    for img_file in [x for x in all_file if x.endswith(".jpg")]:
      content = self.get_binary_content(img_file)
      file_hash = self.get_file_hash(content)
      set_len = len(self.__exists_set)
      self.__exists_set.add(file_hash)
      if len(self.__exists_set) > set_len:
        target_path = os.path.join(self.get_target_folder(img_file), f"{file_hash}.jpg")
        self.write_binary_content(target_path, content)

  def get_all_file(self, path):
    result = []
    if os.path.isfile(path):
      result.append(os.path.realpath(path))
    else:
      for sub_path in os.listdir(path):
        result.extend(self.get_all_file(os.path.join(path, sub_path)))
    return result

  def get_target_folder(self, path):
    image = cv2.imread(path)
    height, width = image.shape[:2]
    target_folder = f"{width}x{height}"
    target_path = os.path.join(self.__target, target_folder)
    if os.path.exists(target_path) and os.path.isdir(target_path):
      return target_path
    os.mkdir(target_path)
    return target_path

  def save_exists_set(self):
    print(f"start write {self.__config_file}")
    content = json.dumps(list(self.__exists_set), ensure_ascii=False)
    with open(os.path.join(self.__target, self.__config_file), "w") as f:
      f.write(content)
    print(f"write {self.__config_file} done")

  def get_binary_content(self, path):
    with open(path, "rb") as f:
      content = f.read()
    return content

  def write_binary_content(self, path, content):
    print(f"write {path}")
    with open(path, "wb") as f:
      f.write(content)

  def main(self):
    if not os.path.exists(self.__source):
      print("source path not exists, exit")
      return
    if not os.path.exists(self.__target):
      os.mkdir(self.__target)
    for file_name in os.listdir(self.__source):
      file_path = os.path.join(self.__source, file_name)
      if os.path.isdir(file_path):
        continue
      content = self.get_binary_content(file_path)
      file_hash = self.get_file_hash(content)
      if file_hash in self.__exists_set:
        continue
      else:
        target_path = os.path.join(self.get_target_folder(file_path), f"{file_hash}.jpg")
        self.write_binary_content(target_path, content)
        self.__exists_set.add(file_hash)
    print("save finish")
    self.save_exists_set()

if __name__ == "__main__":
  source_path = os.path.realpath(os.environ["LOCALAPPDATA"] + r"\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets")
  keys = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders')
  user_pic = winreg.QueryValueEx(keys,'My Pictures')[0]
  target_path = os.path.join(user_pic, "wallpaper")
  SaveWallpaper(source_path, target_path).main()
  print("all finish")
