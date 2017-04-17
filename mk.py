#!/usr/bin/python
#encoding: utf-8

import json
import codecs
import os

def get_files(root_path):
    for dir in os.walk(root_path):
        if dir[2]:
            for nf in dir[2]:
                yield os.path.join(dir[0], nf)

def exclude_filter(exclude, nfile):
    files_path = exclude.get('file_path')
    files_name = exclude.get('file_name')
    base_name = os.path.basename(nfile)
    exts_name = exclude.get('ext_name')
    base_ext_name = base_name.rsplit(".", 1)[1]
    if files_path:
        for npath in files_path:
            if npath==nfile:
                return True
    elif files_name:
        for name in files_name:
            print name, base_name
            if name==base_name:
                return True
    elif exts_name:
        for name in exts_name:
            print name, base_ext_name
            if name==base_ext_name:
                return True

def include_filter(include, nfile):
    files_path = include.get('file_path')
    files_name = include.get('file_name')
    base_name = os.path.basename(nfile)
    if files_path:
        for npath in files_path:
            if npath==nfile:
                return True
    elif files_name:
        for name in files_name:
            if name==base_name:
                return True

def main():
    # read config
    config = {}
    with codecs.open("config.json","rb","UTF-8") as f:
        config = json.loads(f.read())
    if not config:
        return

    template = config.get("template")
    if template and template.get('path'):
        root_path = template.get('path')
        if not os.path.exists(root_path):
            print "source path not exist"
            return
        root_path = os.path.abspath(root_path)
        old_path = os.path.dirname(root_path)
    else:
        return
    exclude = template.get('exclude')
    include = template.get('include')

    store = config.get("store")
    if not store or not os.path.exists(store.get('dir_path', '')):
        return

    data = config.get("data")
    if not data:
        return

    if not os.path.exists(root_path):
        print 'root path not exists'
        return

    if os.path.isfile(root_path):
        files = [root_path]
    else:
        base_name = os.path.basename(root_path)
        store_root_path = os.path.join(store.get('dir_path'), base_name)
        if not os.path.exists(store_root_path):
            os.mkdir(store_root_path)
        files = get_files(root_path)

    for nfile in files:
        print nfile
        try:
            with codecs.open(nfile, "rb", "UTF-8") as f:
                s = f.read()

            if not exclude_filter(exclude, nfile) or include_filter(include, nfile):
                s = s % data
        except:
            with codecs.open(nfile, "rb") as f:
                s = f.read()

        # save to file
        fn = nfile.replace(old_path, store.get('dir_path'))
        fn_dir = os.path.dirname(fn)
        if not os.path.exists(fn_dir):
            os.makedirs(fn_dir)
        try:
            with codecs.open(fn, "wb", "UTF-8") as f:
                f.write(s)
                f.flush()
        except:
            with codecs.open(fn, "wb") as f:
                f.write(s)
                f.flush()

if __name__ == '__main__':
    main()
