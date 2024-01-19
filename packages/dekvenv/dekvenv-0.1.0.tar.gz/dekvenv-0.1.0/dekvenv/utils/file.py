import os
import tempfile
import shutil
import codecs
import filecmp

DEFAULT_VALUE = object()


def write_file(filepath, s=None, b=None, sb=None, m=None, mi=None, c=None, ci=None, t=None, encoding='utf-8'):
    if filepath and t is None:
        if os.path.exists(filepath):
            remove_path(filepath)
        sure_dir(os.path.dirname(filepath))
    if s is not None:
        write_text(filepath, s, encoding)
    elif b is not None:
        with open(filepath, 'wb') as f:
            f.write(b)
    elif sb is not None:
        if isinstance(sb, str):
            write_file(filepath, s=sb)
        else:
            write_file(filepath, b=sb)
    elif c is not None:
        filepath_temp = filepath + '.__tempfile__'
        if os.path.exists(filepath_temp):
            os.remove(filepath_temp)
        if os.path.isdir(c):
            shutil.copytree(c, filepath_temp)
        else:
            shutil.copyfile(c, filepath_temp)
        shutil.move(filepath_temp, filepath)
    elif ci is not None:
        if os.path.exists(ci):
            write_file(filepath, c=ci)
    elif t is not None:
        fp = os.path.join(tempfile.mkdtemp(), filepath or '__tempfile__')
        write_file(fp, sb=t)
        return fp
    elif m is not None:
        shutil.move(m, filepath)
    elif mi is not None:
        if os.path.exists(mi):
            write_file(filepath, m=mi)
    else:
        raise Exception('s, b, c, m is all empty')


def read_file(filepath, default=DEFAULT_VALUE):
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            return f.read()
    else:
        if default is not DEFAULT_VALUE:
            return default
        else:
            raise


def read_text(filepath, default=DEFAULT_VALUE, encoding='utf-8'):
    if os.path.isfile(filepath):
        with codecs.open(filepath, encoding=encoding) as f:
            return f.read()
    else:
        if default is not DEFAULT_VALUE:
            return default
        else:
            raise


def write_text(filepath, content, encoding='utf-8'):
    with codecs.open(filepath, 'w', encoding=encoding) as f:
        return f.write(content)


def remove_path(path, ignore=False):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        return True
    except PermissionError as e:
        if not ignore:
            raise e from e
        return False


def clear_dir(path, ignore=False):
    for file in os.listdir(path):
        remove_path(os.path.join(path, file), ignore)


def merge_dir(dest, src):
    for fn in os.listdir(src):
        write_file(os.path.join(dest, fn), ci=os.path.join(src, fn))


def copy_path(src, dest):
    remove_path(dest)
    if os.path.isdir(src):
        shutil.copytree(src, dest)
    elif os.path.isfile(src):
        shutil.copyfile(src, dest)


def sure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def content_cmp(a, b):
    return filecmp.cmp(a, b, False)
