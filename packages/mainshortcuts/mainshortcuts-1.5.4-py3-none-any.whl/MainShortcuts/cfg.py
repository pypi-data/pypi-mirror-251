noimport={}
import MainShortcuts.path as m_path
try:
  import MainShortcuts.json as json
except Exception as e:
  noimport["json"]=e
try:
  import pickle
except Exception as e:
  noimport["pickle"]=e
try:
  import cPickle
except Exception as e:
  noimport["cPickle"]=e
try:
  import toml
except Exception as e:
  noimport["toml"]=e
types=["auto","json","pickle","cPickle","toml"]
def _checkType(path,type):
  ext=m_path.info(path)["ext"].lower()
  for i in types:
    if type.lower()==i.lower():
      type=i
      break
  if not type in types:
    raise TypeError('Type "{0}" not supported'.format(type))
  elif type!="auto":
    return type
  elif ext in ["json"]:
    return "json"
  elif ext in ["pickle","pkl"]:
    return "pickle"
  elif ext in ["cpickle","dpb"]:
    return "cPickle"
  elif ext in ["toml"]:
    return "toml"
def _checkImport(type):
  if type in noimport:
    raise ImportError(noimport[type])
    return False
  else:
    return True
class cfg:
  # Код
  def __init__(self,path,
    data=None,
    type="auto", # "auto" - определение по расширению файла
    json_args={},
    pickle_args={},
    cPickle_args={},
    toml_args={}
    ):
    # Код
    json_dargs={
      "mode":"c",
      "indent":2,
      "sort":True,
      "encoding":"utf-8"
      }
    pickle_dargs={
      "protocol":None,
      "fix_imports":True,
      "buffer_callback":None,
      "encoding":"ASCII",
      "errors":"strict",
      "buffers":None
      }
    cPickle_dargs={}
    toml_dargs={
      "encoding":"utf-8"
      }
    self.path=path
    self.data=data
    self.type=_checkType(path,type)
    _checkImport(self.type)
    json_dargs.update(json_args)
    pickle_dargs.update(pickle_args)
    cPickle_dargs.update(cPickle_args)
    toml_dargs.update(toml_args)
    self.json_args=json_dargs
    self.pickle_args=pickle_dargs
    self.cPickle_args=cPickle_dargs
    self.toml_args=toml_dargs
  def load(self,path=None,type=None,pickle_args={},toml_args={}):
    # Загрузка из файла
    if path==None:
      path=self.path
    if type==None:
      type=self.type
    else:
      type=_checkType(path,type)
    _checkImport(type)
    if type=="json":
      self.data=m_json.read(path)
    elif type=="pickle":
      args=self.pickle_args
      args.update(pickle_args)
      with open(path,"rb") as f:
        self.data=pickle.load(f,
          fix_imports=args["fix_imports"],
          encoding=args["encoding"],
          errors=args["errors"],
          buffers=args["buffers"]
          )
    elif type=="cPickle":
      with open(path,"rb") as f:
        self.data=cPickle.load(f)
    elif type=="toml":
      args=self.toml_args
      args.update(toml_args)
      with open(path,"r",encoding=args["encoding"]) as f:
        self.data=toml.load(f)
    return self.data
  def save(self,path=None,type=None,json_args={},pickle_args={},cPickle_args={},toml_args={}):
    if path==None:
      path=self.path
    if type==None:
      type=self.type
    else:
      type=_checkType(path,type)
    _checkImport(type)
    if type=="json":
      args=self.json_args
      args.update(json_args)
      m_json.write(path,self.data,mode=args["mode"],indent=args["indent"],sort=args["sort"],encoding=args["encoding"])
    elif type=="pickle":
      args=self.pickle_args
      args.update(pickle_args)
      with open(path,"wb") as f:
        pickle.dump(self.data,f,
          protocol=args["protocol"],
          fix_imports=args["fix_imports"],
          buffer_callback=args["buffer_callback"]
          )
    elif type=="cPickle":
      args=self.cPickle_args
      args.update(cPickle_args)
      with open(path,"wb") as f:
        cPickle.dump(self.data,f)
    elif type=="toml":
      args=self.toml_args
      args.update(toml_args)
      with open(path,"w",encoding=args["encoding"]) as f:
        toml.dump(self.data,f)
