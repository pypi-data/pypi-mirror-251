import sqlparse.sql

from slicing.stmt.tokens.identifier import Identifier


class Function:
    def __init__(self, token):
        self._token = token

    @classmethod
    def match(cls, token):
        return type(token) == sqlparse.sql.Function

    def accept(self, statement):
        self._insert(statement)

    def _insert(self, statement):
        if statement.info.get("Type") == "INSERT" and statement.info.get("TableName") == "WaitFill":
            for t in self._token.tokens:
                for token_class in [Identifier]:
                    if token_class.match(t):
                        token_class(t).accept(statement)
            return True
        return False

