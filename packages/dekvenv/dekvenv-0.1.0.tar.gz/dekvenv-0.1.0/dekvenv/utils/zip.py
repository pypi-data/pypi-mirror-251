import os
import zipfile
from .file import remove_path, sure_dir


def compress_files(src, zip_file, combine=False):
    src = os.path.normpath(os.path.abspath(src))
    zip_file = os.path.normpath(os.path.abspath(zip_file))
    sure_dir(os.path.dirname(zip_file))
    if not combine:
        remove_path(zip_file)
    with zipfile.ZipFile(zip_file, mode='w', compression=zipfile.ZIP_BZIP2, allowZip64=True, compresslevel=9) as zf:
        for base, _, files in os.walk(src):
            for file in files:
                p = os.path.join(base, file)
                zf.write(
                    p,
                    p[len(src):]
                )


def decompress_files(zip_file, dest_dir, combine=False):
    dest_dir = os.path.normpath(os.path.abspath(dest_dir))
    if not combine:
        remove_path(dest_dir)
    sure_dir(dest_dir)

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(dest_dir)
