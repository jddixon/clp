# clp/clp/py.py

import os
import hashlib
from tokenize import tokenize, untokenize, NAME
from io import BytesIO

import sha3         # monkey-patches hashlib
from clp import CLPError

from xlattice import check_using_sha, Q


def get_name_pairs(in_stream):
    """
    Read an input stream, expecting a series of old name/new name pairs.

    The main part of the file consists of old_name / new_name pairs
    separated by one or more tabs, one pair per line.  Blank lines are
    ignored.  Comments beginning with a sharp sign are ignored.
    """

    # XXX test for null in_stream

    pairs = {}
    line = in_stream.readline()
    while line:
        # DEBUG
        # print("LINE: '%s'" % line)
        # END
        line, _, _ = line.partition('#')
        if line:
            line = line.strip()
            if line:
                if not '\t' in line:
                    raise CLPError("ill-formed line: '%s'" % line)
                left, right = line.split('\t', maxsplit=1)
                left = left.rstrip()
                right = right.lstrip()
                # XXX could check for pathelogical cases ...
                if left and right:
                    if left in pairs:
                        raise CLPError("duplicate left value: %s" % left)
                    pairs[left] = right
                    # DEBUG
                    # print("    %-20s -> %s" % (left, right))
                    # END
        line = in_stream.readline()
    if not pairs:
        raise CLPError("empty name-pairs file")
    return pairs


def rename_in_file(path_to_file, name_pairs, using_sha, write_tmpfile=False):
    """

    """
    old_hash = None
    new_hash = None

    def make_sha(using_sha):
        sha = None
        if using_sha == Q.USING_SHA1:
            sha = hashlib.sha1()
        elif using_sha == Q.USING_SHA2:
            sha = hashlib.sha256()
        elif using_sha == Q.USING_SHA3:
            sha = hashlib.sha3_256()

    if not os.path.exists(path_to_file):
        raise CLPError("%s does not exist" % path_to_file)
    else:
        check_using_sha(using_sha)      # may raise exception

    # XXX CHECK: name_pairs must be a str->str map

    # XXX this assumes the file is utf-8
    # XXX Should be try/except
    with open(path_to_file, 'rb') as file:
        data = file.read()

    sha = make_sha(using_sha)
    sha.update(data)
    old_hash = sha.hexdigest()

    # DEBUG
    print("pathToFile: %s" % path_to_file)
    print("old_hash:   %s" % old_hash)
    # END
    # END

    results = []
    g = tokenize(BytesIO(data).readline)
    for toknum, tokval, _, _, _ in g:
        if toknum == NAME:
            # HACKING IN PROGRESS
            print(tokval)

    return (old_hash, new_hash)
