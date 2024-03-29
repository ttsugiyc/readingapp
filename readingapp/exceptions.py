class Message(Exception):
    pass


class LoginError(Message):
    def __init__(self, *args):
        super().__init__('ログインできませんでした', *args)


class PasswordError(Message):
    def __init__(self, *args):
        super().__init__('パスワードが違います', *args)


class UniquenessError(Message):
    def __init__(self, table, *args):
        message = f'その{table}は既に使用されています'
        super().__init__(message, *args)
