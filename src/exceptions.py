class ServiceException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)


class JWTSecretNotExists(ServiceException):
    def __init__(self):
        self.code = 1
        self.message = "JWT secret not exists. Service required it to startup"
        super().__init__(self.code, self.message)


class LoginNotEnoughFields(ServiceException):
    def __init__(self):
        self.code = 403
        self.message = "Unauthorized. Not enough fields"
        super().__init__(self.code, self.message)


class UnauthorizedException(ServiceException):
    def __init__(self):
        self.code = 401
        self.message = "Unauthorized. User not found or incorrect credentials"
        super().__init__(self.code, self.message)


class IncorrectCurrentPassword(ServiceException):
    def __init__(self):
        self.code = 601
        self.message = "Incorrect current password"
        super().__init__(self.code, self.message)
