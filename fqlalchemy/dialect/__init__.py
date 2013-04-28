from sqlalchemy.engine.default import DefaultDialect
import dbapi


class FQLDialect(DefaultDialect):
    def _check_unicode_returns(self, connection):
        return u'test plain returns'

    def do_rollback(self, connection):
        pass

    @classmethod
    def dbapi(cls):
        return dbapi
