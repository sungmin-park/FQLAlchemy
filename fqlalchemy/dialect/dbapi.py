import re
from urllib import urlencode
from urllib2 import urlopen
from simplejson import loads


class Error(StandardError):
    pass


class Warning(StandardError):
    pass


class InterfaceError(Error):
    pass


class DatabaseError(Error):
    pass


class InternalError(DatabaseError):
    pass


class OperationalError(DatabaseError):
    pass


class ProgrammingError(DatabaseError):
    pass


class IntegrityError(DatabaseError):
    pass


class DataError(DatabaseError):
    pass


class NotSupportedError(DatabaseError):
    pass

paramstyle = 'format'

TABLE_RE = re.compile('FROM ([^\s]+)')
VERSBOSE_FIELDS_RE = re.compile(' AS [^\s,]+')
ESCAPE_QUOTE_RE = re.compile("'")


def esapce_params(params):
    result = []
    for param in params:
        if isinstance(param, basestring):
            param = "'%s'" % ESCAPE_QUOTE_RE.sub("\\'", param)
        result.append(param)
    return tuple(result)


class Cursor(object):
    def __init__(self, access_token):
        self.access_token = access_token

    @property
    def description(self):
        desc = []
        for field, name in self._selected_fields:
            desc.append((name, 'String'))
        return desc

    def execute(self, sql, params=None):
        table = TABLE_RE.search(sql).group(1)
        # remove versbose field description
        sql = re.sub(table + '\.([^\s]+)', '\\1', sql)
        self._selected_fields = re.findall('([^\s]+) AS ([^\s,]+)', sql)
        sql = VERSBOSE_FIELDS_RE.sub('', sql)
        query = sql % esapce_params(params)
        params = dict(q=query)
        if self.access_token:
            params['access_token'] = self.access_token
        url = 'https://graph.facebook.com/fql?' + urlencode(params)
        print query
        result = loads(urlopen(url).read(), 'utf-8')
        self._rows = tuple(result['data'])

    def fetchall(self):
        if not self._rows:
            return tuple()
        result = []
        for row in self._rows:
            row_result = []
            for field, name in self._selected_fields:
                row_result.append(unicode(row[field]))
            result.append(row_result)
        self._rows = None
        return tuple(result)


class Connection(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def cursor(self):
        return Cursor(self.access_token)


def connect(access_token=None):
    return Connection(access_token)
