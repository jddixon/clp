# clp/clp/py.py

""" Functions and utilities for computer language processing."""

import hashlib
import os
import re
import sys
from tokenize import tokenize, untokenize, NAME, STRING
from io import BytesIO

from clp import CLPError
from xlattice import check_hashtype, HashTypes

if sys.version_info < (3, 6):
    import sha3         # monkey-patches hashlib
    assert sha3         # suppress warning

PY_NAME_PAT = r'^[a-zA-Z_][a-zA-Z_0-9]*$'
PY_NAME_RE = re.compile(PY_NAME_PAT)


def check_name(name):
    """ Verify that a string is an acceptable Python variable name. """

    if not name:
        raise CLPError("expected Python name, got an empty string")
    match = PY_NAME_RE.match(name)
    if not match:
        raise CLPError("'%s' is not a valid Python name" % name)


def check_string(tokval, name_pairs):
    """
    Where a string is a quoted variable name and the variable name
    is in the old-name/new-name map, do the replacement.

    The quote character must be either SQUOTE or DQUOTE.  If the comparison
    fails, return the value that was tested.
    """
    if len(tokval) > 2:
        qchar = tokval[0]
        if qchar in ['"', "'"]:
            end_char = tokval[-1]
            if qchar == end_char:
                text = tokval[1:-1]
                if text in name_pairs:
                    tokval = qchar + name_pairs[text] + qchar

    return tokval


def get_name_pairs(in_stream):
    """
    Read an input stream, expecting a series of old name/new name pairs.

    The main part of the file consists of old_name / new_name pairs
    separated by one or more tabs, one pair per line.  Blank lines are
    ignored.  Comments beginning with a sharp sign are ignored
    """

    assert in_stream is not None

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
                if ' ' not in line:
                    raise CLPError("ill-formed line: '%s'" % line)
                left, right = line.split(' ', maxsplit=1)
                left = left.rstrip()
                right = right.lstrip()
                if left and right:
                    # verify both names are good
                    check_name(left)            # possible CLPError
                    check_name(right)           # possible CLPError
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


def rename_in_file(path_to_file, name_pairs, hashtype, path_to_output=''):
    """
    Given a set of old-name/new-name pairs, edit a file to replace all
    Python names accordingly.

    Matches within strings are ignored, except where the entire text of
    the string is an old-name, in which case it is replaced with the
    corresponding new-name.

    If any changes are made, return the SHA of the original file, the
    output file, and a map from old-name to a count of any replacements
    made.  If path_to_output is not empty, write the transformed file
    to that location.

    If no change are made, return the SHA of the original file, None,
    and None.  In this case nothing is written to path_to_output.

    """
    old_hash = None
    new_hash = None
    counts = {}

    def hash_it(data, hashtype):
        """ Hash a block of data using the specified type of SHA. """

        sha = None
        if hashtype == HashTypes.SHA1:
            sha = hashlib.sha1()
        elif hashtype == HashTypes.SHA2:
            sha = hashlib.sha256()
        elif hashtype == HashTypes.SHA3:
            sha = hashlib.sha3_256()
        sha.update(data)
        return sha.hexdigest()

    if not os.path.exists(path_to_file):
        raise CLPError("%s does not exist" % path_to_file)
    else:
        check_hashtype(hashtype)      # may raise exception

    # CHECK: name_pairs must be a str->str map

    # ASSUMES the file is utf-8
    # SHOULD BE try/except
    with open(path_to_file, 'rb') as file:
        data = file.read()

    old_hash = hash_it(data, hashtype)

    # DEBUG
    # print("pathToFile: %s" % path_to_file)
    # print("old_hash:   %s" % old_hash)
    # END

    results = []
    tokens = tokenize(BytesIO(data).readline)
    for toknum, tokval, start, end, log_line in tokens:
        # start and end are 2-tuples (srow, scol; erow, ecol)
        if toknum == NAME:
            if tokval in name_pairs:
                tokval2 = name_pairs[tokval]
                if tokval in counts:
                    counts[tokval] += 1
                else:
                    counts[tokval] = 1
                tokval = tokval2
        elif toknum == STRING:
            tokval2 = check_string(tokval, name_pairs)
            if tokval2 != tokval:
                name = tokval[1:-1]
                if name in counts:
                    counts[name] += 1
                else:
                    counts[name] = 1
                tokval = tokval2

        results.append((toknum, tokval, start, end, log_line))

    data_out = untokenize(results)
    new_hash = hash_it(data_out, hashtype)
    with open(path_to_output, 'wb+') as file:
        file.write(data_out)

    # DEBUG
    # print("path_to_output %s" % path_to_output)
    # print("new_hash:   %s" % new_hash)
    # print("counts:")
    # for key in counts:
    #     print("  %-5s %d" % (key, counts[key]))
    # END

    return (data_out, counts, old_hash, new_hash)
