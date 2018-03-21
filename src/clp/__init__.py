# clp/cp/__init__.py
""" Tools for computer language processing. """

__version__ = '0.1.14'
__version_date__ = '2018-03-21'

__all__ = ['CLPError',
           'serialize_str_list']


class CLPError(RuntimeError):
    """ Errors encountered in processing computer language. """
    pass


def serialize_str_list(name, indent, elements, line_len=78):
    """
    Given a list of strings, serialize it with the specified
    initial indent, with list members SQUOTEd and separated by
    COMMA SPACE.  Return the serialized list as a list of one or more lines,
    each of length not exceeding line_len.  Newlines are not appended to
    the output.
    """

    output = []
    name_len = len(name)
    out = ' ' * indent + name + '=['
    out_len = len(out)

    if elements:
        for element in elements:
            elm_len = len(element) + 4  # tswo SQUOTEs, comma, space
            if out_len + elm_len > line_len:
                output.append(out[0:-1])
                out = (' ' * (indent + name_len + 2)) + "'" + element + "', "
                out_len = len(out)
            else:
                out += "'" + element + "', "
                out_len += elm_len

    if out.endswith(', '):
        out = out[0:-2]
    out += ']'
    output.append(out)
    return output
