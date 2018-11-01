#!/usr/bin/python
import os

ELF = '\x7fELF'
HEADR_SIZE = 128
SUID_PERM = 04000

PATH_DIRS = [i for i in os.environ['PATH'].split(':') if os.path.isdir(i)]
FILE_HEADERS = {}
SETUID_FILES = []
# UNIQUE_SUIDS = []


def is_elf(data):
    return data.startswith(ELF)

def get_header(path):
    with open(path, 'rb') as f:
        return f.read(HEADR_SIZE)

def is_suid(path):
    return os.stat(path).st_mode & SUID_PERM > 0

def is_suid_unique(suid_path):
    suid_header = FILE_HEADERS[suid_path]
    for h in FILE_HEADERS:
        if h == suid_path:
            continue
        if FILE_HEADERS[h] == FILE_HEADERS[suid_path]:
            print h
            return False
        return True

if __name__ == '__main__':
    # Iterate all binaries, extarct headers and suids
    for d in PATH_DIRS:
        for f_name in os.listdir(d):
            file_path = '%s/%s' % (d, f_name)
            if not os.path.isfile(file_path) or os.path.islink(file_path):
                continue
            header = get_header(file_path)
            if is_elf(header):
                FILE_HEADERS[file_path] = header
                if is_suid(file_path):
                    SETUID_FILES.append(file_path)

    # find all unique suid files
    for suid in SETUID_FILES:
        if is_suid_unique(suid):
            print suid
            # UNIQUE_SUIDS.append(suid)

