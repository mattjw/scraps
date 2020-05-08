try:
    import urllib.parse as urlparse 
except ImportError:
    import urlparse
import collections
import re
import urllib
import publicsuffix  # pip install publicsuffix2


#
#
# Parsing URLs
#

def parse_url(url):
    """
    Parse a URL. Return OrderedDict of components.
    """
    out = collections.OrderedDict()
    parts = urlparse.urlparse(url)
    out['parsed_scheme'] = parts.scheme
    out['parsed_hostname'] = parts.hostname.lower()
    out['parsed_port'] = parts.port  # may be None
    out['parsed_path'] = parts.path
    out['parsed_params'] = parts.params
    out['parsed_query'] = parts.query
    out['parsed_fragment'] = parts.fragment
    
    # domain
    # note: differentiate between IP and hostname
    hostname = out['parsed_hostname']
    if (hostname.count('.') == 3) and (re.search('[a-zA-Z]', hostname) is None):
        # it's an IP. do not include IP addresses
        out['domain_full'] = None
        out['domain_simplified'] = None
        out['domain_public_suffix'] = None
    else:
        domain = hostname
        out['domain_full'] = domain
        out['domain_public_suffix'] = publicsuffix.get_public_suffix(domain)
        out['domain_simplified'] = re.sub('^(www[\d]?|m)\.', '', domain)  #www, www2, etc.

    return out


#
#
# Encoding / decoding / storing URLs
#

DELIM_URLS_LIST = ','
def urls_to_string(urls_list, delim=DELIM_URLS_LIST):
    """
    Encode a list of URLs as a string. Each individual URL is encoded using
    url.quote (thus replacing any commas and other symbols) and then joined
    into a comma-delimited list.
    """
    list_quoted = []
    for url in urls_list:
        try:
            quoted = urllib.quote(url)
        except KeyError as ex:
            # possibly unicode problem
            # URLs should not have native unicode bytes
            # they should use backslash escaping
            quoted = urllib.quote(url.encode('utf-8'))
        list_quoted.append(quoted)
    assert all(delim not in txt for txt in list_quoted), list_quoted
    txt = delim.join(list_quoted)
    return txt


def string_to_urls(txt, delim=DELIM_URLS_LIST):
    """
    Inverse of `urls_to_string`.
    """
    if len(txt.strip(' ')) == 0:
        return []
    quoted_urls = txt.split(delim)
    decoded = []
    for url in quote_urls:
        decoded.append(urllib.unquote(url))
    return decoded
