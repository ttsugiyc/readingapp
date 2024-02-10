class MyException(Exception):
    pass


class LoginError(MyException):
    def __init__(self, *args):
        super().__init__('ログインできませんでした', *args)


class PasswordError(MyException):
    def __init__(self, *args):
        super().__init__('パスワードが違います', *args)


class UniquenessError(MyException):
    def __init__(self, table, *args):
        message = f'その{table}は既に使用されています'
        super().__init__(message, *args)
