# clp/clp/py.py

import os
import hashlib
from tokenize import tokenize, untokenize, NAME, STRING
from io import BytesIO

import sha3         # monkey-patches hashlib
from clp import CLPError

from xlattice import check_using_sha, Q


def get_name_pairs(in_stream):
    """
    Read an input stream, expecting a series of old name/new name pairs.

    The main part of the file consists of old_name / new_name pairs
    separated by one or more tabs, one pair per line.  Blank lines are
    ignored.  Comments beginning with a sharp sign are ignored
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


def check_string(tokval, name_pairs):
    """
    Where a string is a quoted variable name and the variable name
    is in the old-name/new-name map, do the replacement.

    The quote character must either SQUOTE or DQUOTE.  If the comparison
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


def rename_in_file(path_to_file, name_pairs, using_sha, path_to_output=''):
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

    def hash_it(data, using_sha):
        sha = None
        if using_sha == Q.USING_SHA1:
            sha = hashlib.sha1()
        elif using_sha == Q.USING_SHA2:
            sha = hashlib.sha256()
        elif using_sha == Q.USING_SHA3:
            sha = hashlib.sha3_256()
        sha.update(data)
        return sha.hexdigest()

    if not os.path.exists(path_to_file):
        raise CLPError("%s does not exist" % path_to_file)
    else:
        check_using_sha(using_sha)      # may raise exception

    # XXX CHECK: name_pairs must be a str->str map

    # XXX this assumes the file is utf-8
    # XXX Should be try/except
    with open(path_to_file, 'rb') as file:
        data = file.read()

    old_hash = hash_it(data, using_sha)

    # DEBUG
    print("pathToFile: %s" % path_to_file)
    print("old_hash:   %s" % old_hash)
    # END

    results = []
    g = tokenize(BytesIO(data).readline)
    for toknum, tokval, start, end, log_line in g:
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
    new_hash = hash_it(data_out, using_sha)
    with open(path_to_output, 'wb+') as file:
        file.write(data_out)

    # DEBUG
    print("path_to_output %s" % path_to_output)
    print("new_hash:   %s" % new_hash)
    print("counts:")
    for key in counts:
        print("  %-5s %d" % (key, counts[key]))
    # END

    return (data_out, counts, old_hash, new_hash)