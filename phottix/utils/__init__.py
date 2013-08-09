import sys, random, string, tempfile, zipfile, logging, traceback
from uuid import uuid4
from functools import wraps
from datetime import datetime
from os import path, makedirs, walk
try: import simplejson as json
except ImportError: import json
from django.http import HttpResponse
from django.views.static import serve
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone



PAGE_SIZE = 10

#reload sys so we can set `ensure_ascii=False` when dump to JSON string
reload(sys)
sys.setdefaultencoding('utf8')

def render_response(request, template, dic):
    return render_to_response(template, dic, context_instance=RequestContext(request))

def auto_code():
    time = datetime.utcnow().strftime('%y%m%d%H%M%S%f')
    tail =  ''.join([ random.choice(string.ascii_letters) for i in range(4) ])
    return time + tail

def ensure_dir(f):
    d = path.dirname(f)
    if not path.isdir(d):
        makedirs(d)
        
def unique_id():
    """
    Generate random GUID
    """
    return uuid4().hex


def make_utc(d):
    return d.astimezone(timezone.utc)

def read_json(path, encoding='utf-8-sig'):
    """
    Read file contents as JSON
    """
    with open(path, 'r') as f:
        return load_json(f.read(), encoding)
    
def write_json(data, target):
    """
    Write JSON contents to file
    """
    with open(target, 'w+') as f:
        f.write(dump_json(data))

def load_json(s, encoding='utf-8-sig'):
    """
    Load JSON contents from string
    """
    try:
        return json.loads(s.decode(encoding))
    except:
        return json.loads(s.decode('utf-8'))

def dump_json(data):
    """
    Serialize ``data`` to a JSON formatted ``str``.
    """
    if isinstance(data, basestring):
        return data
    return json.dumps(data, indent=4, ensure_ascii=False)

def save_django_file(request, base_dir=None):
    """
    An utility function which saves django uploaded files to target directory and returns full file names
    """
    if base_dir is None:
        base_dir = settings.UPLOAD_FILE_DIR or tempfile.gettempdir()
    
    if not path.isdir(base_dir):
        makedirs(base_dir)
        
    file_names = []
    for up_file in request.FILES.values():
        bn = path.basename(up_file.name)
        fn = path.join(base_dir, '%s_%s' %(uuid4().hex, bn))
        with open(fn, 'wb') as f:
            for chunk in up_file.chunks():
                f.write(chunk)
        file_names.append((bn, path.relpath(fn, base_dir), fn))
    return file_names

def zip_folder(folder_path, output_path=None): 
    """
    Compress a folder as zip file
    """
    zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
    try:    
        for root, folders, files in walk(folder_path):
            for folder_name in folders:
                absolute_path = path.join(root, folder_name)
                relative_path = path.relpath(absolute_path, folder_path)
                zip_file.write(absolute_path, relative_path)
                
            for file_name in files:
                absolute_path = path.join(root, file_name)
                relative_path = path.relpath(absolute_path, folder_path)
                zip_file.write(absolute_path, relative_path)
        
        return output_path
    finally:
        zip_file.close()

def serve_static(request, file_path, attachment=False):
    """
    Serve static files below a given point in the directory structure.
    """
    filename = path.basename(file_path)
    resp = serve(request, filename, document_root=path.dirname(file_path))
    if attachment:
        attach_name = isinstance(attachment, basestring) and attachment or filename
        resp['Content-Disposition'] = 'attachment;filename=%s' %attach_name.encode('gb2312')
    return resp

def render_js_response(script):
    if not script.startswith('<script '):
        script = '<script type="text/javascript">%s</script>'% script
    return HttpResponse(script)

def suppress_exc(func, default=None):
    """
    Suppress exception
    """
    @wraps(func)
    def inner(*args, **kw):
        try:
            return func(*args, **kw)
        except:
            logging.exception(traceback.format_exc())
            return default
    return inner

def itersubclasses(cls, _seen=None):
    """
    Generator over all subclasses of a given class, in depth first order.
    """
    if _seen is None: _seen = set()
    try:
        subclses = cls.__subclasses__()
    except TypeError: # fails only when cls is type
        subclses = cls.__subclasses__(cls)
        
    for sub in subclses:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            
            for sub in itersubclasses(sub, _seen):
                yield sub
    
def encode_auth_token(cipher_token):
    key = settings.AUTH_RIJNDAEL_KEY
    if isinstance(key, list): key = ''.join(map(chr, key))
    iv = settings.AUTH_RIJNDAEL_IV
    if isinstance(iv, list): iv = ''.join(map(chr, iv))
 
    br = B64_Rijndael(key, iv)
    token = br.encrypt(cipher_token)
    return token 


def convert_time(utc_time):
    if not utc_time.tzinfo:
        import pytz
        utc_tz = pytz.timezone('Africa/Accra')
        utc_time = utc_tz.localize(utc_time)
    return timezone.localtime(utc_time)

def maybe_list(l):
    if l is None or isinstance(l, list):
        return l
    return [l]

class SettingProxy(object):
    """
    A proxy for getting configuration item 
    """
    def __getattr__(self, attr_name):
        return self.__dict__.get(attr_name) \
                or self._from_db(attr_name)  \
                or self._from_conf(attr_name)
    
    def _from_db(self, key):
        return None
    
    def _from_conf(self, key):
        from django.conf import settings
        return getattr(settings, key, None)

settings = SettingProxy()
