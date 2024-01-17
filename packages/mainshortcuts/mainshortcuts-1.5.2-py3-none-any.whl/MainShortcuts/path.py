import MainShortcuts.addon as _a
import os as _os
import shutil as _shutil
sep=_os.sep # Разделитель в пути файла
separator=sep
def exists(path): # Объект существует?
  return _os.path.exists(path)
def merge(array): # Собрать путь к объекту из массива
  return sep.join(array)
def split(path): # Разложить путь к объекту на массив
  return path.split(sep)
def info(path=_os.getcwd(),listdir=False,listlinks=False): # Информация о пути
  info={
    "dir":None, # Папка, в которой находится объект
    "dirs":None, # Рекурсивный список папок (если аргумент listdir=True)
    "exists":None, # Существует ли объект? | True/False
    "ext":None, # Расширение файла, даже если это папка
    "files":None, # Рекурсивный список файлов (если аргумент listdir=True)
    "fullname":None, # Полное название объекта (включая расширение)
    "fullpath":None, # Полный путь к объекту
    "link":None, # Это ссылка или оригинал? | True/False
    "name":None, # Название файла без расширения, даже если это папка
    "path":None, # Полученный путь к объекту
    "realpath":None, # Путь к оригиналу, если указана ссылка
    "size":None, # Размер. Для получения размера папки укажите аргумент listdir=True
    "split":[], # Путь, разделённый на массив
    "type":None # Тип объекта | "file"/"dir"
    }
  info["path"]=path
  info["split"]=split(path)
  info["dir"]=merge(info["split"][:-1])
  info["fullname"]=info["split"][-1]
  if "." in info["fullname"]:
    info["ext"]=info["fullname"].split(".")[-1]
    info["name"]=".".join(info["fullname"].split(".")[:-1])
  else:
    info["ext"]=None
    info["name"]=info["fullname"]
  info["exists"]=exists(path)
  if info["exists"]:
    info["fullpath"]=_os.path.abspath(path)
    info["link"]=_os.path.islink(path)
    if info["link"]:
      info["realpath"]=_os.path.realpath(path)
    if _os.path.isfile(path):
      info["size"]=_os.path.getsize(path)
      info["type"]="file"
    elif _os.path.isdir(path):
      info["type"]="dir"
      if listdir:
        tmp=_a.listdir(path,listlinks)
        info["dirs"]=tmp["d"]
        info["files"]=tmp["f"]
        info["size"]=tmp["s"]
    else:
      info["type"]="unknown"
  return info
def delete(path): # Удалить
  info=info(path)
  if info["exists"]:
    if info["type"]=="file":
      _os.remove(path)
    elif info["type"]=="dir":
      _os.rmdir(path)
    else:
      raise Exception("Unknown type: "+info["type"])
rm=delete
# del=delete
def copy(fr,to): # Копировать
  type=info(fr)["type"]
  if type=="file":
    _shutil.copy(fr,to)
  elif type=="dir":
    _shutil.copytree(fr,to)
  else:
    raise Exception("Unknown type: "+type)
cp=copy
def move(fr,to): # Переместить
  _shutil.move(fr,to)
mv=move
def rename(fr,to): # Переименовать
  _os.rename(fr,to)
rn=rename
def link(fr,to,force=False): # Сделать символическую ссылку
  if exists(to) and force:
    delete(to)
  _os.symlink(fr,to)
ln=link
def format(path,replace_to="_",replace_errors=True): # Форматировать путь к файлу (изменить разделитель, удалить недопустимые символы)
  for i in ["/","\\"]:
    path=path.replace(i,sep)
  if replace_errors:
    for i in ["\n",":","*","?","\"","<",">","|","+","%","!","@"]:
      path=path.replace(i,replace_to)
  return path