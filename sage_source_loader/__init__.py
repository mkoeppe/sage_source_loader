import os
import sys
from importlib import invalidate_caches
from importlib.abc import SourceLoader
from importlib.machinery import FileFinder

# Adapted from https://stackoverflow.com/questions/43571737/how-to-implement-an-import-hook-that-can-modify-the-source-code-on-the-fly-using

class SageSourceLoader(SourceLoader):
    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path

    def get_filename(self, fullname):
        return self.path

    def get_data(self, filename):
        """exec_module is already defined for us, we just have to provide a way
        of getting the source code of the module"""
        filename = os.path.abspath(filename)
        with open(filename) as f:
            contents = f.read()

        from sage.repl.preparse import handle_encoding_declaration, preparse_file
        #contents = handle_encoding_declaration(contents, out)
        parsed = preparse_file(contents)
        print(f'🐰 Importing {filename} via Sage preparser')
        header = '''from sage.all import *
'''
        return header + parsed


loader_details = SageSourceLoader, [".sage"]

def install():
    # insert the path hook ahead of other path hooks
    sys.path_hooks.insert(0, FileFinder.path_hook(loader_details))
    # clear any loaders that might already be in use by the FileFinder
    sys.path_importer_cache.clear()
    invalidate_caches()

install()
