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


class S3CannotUploadFile(ServiceException):
    def __init__(self, log: str = ""):
        self.code = 602
        self.message = f"Can't upload file to S3. {log}"
        super().__init__(self.code, self.message)


class S3ImageNotFound(ServiceException):
    def __init__(self, log: str = ""):
        self.code = 603
        self.message = f"Image not found in S3. {log}"
        super().__init__(self.code, self.message)


class S3FileNotFound(ServiceException):
    def __init__(self):
        self.code = 404
        self.message = "Can't find file in S3 storage"
        super().__init__(self.code, self.message)


class S3FileIsNotImage(ServiceException):
    def __init__(self):
        self.code = 604
        self.message = "Chosen file is not image"
        super().__init__(self.code, self.message)


class S3FileNotCreated(ServiceException):
    def __init__(self):
        self.code = 605
        self.message = "File not created at S3 storage"
        super().__init__(self.code, self.message)


class PostBodyIsEmpty(ServiceException):
    def __init__(self):
        self.code = 605
        self.message = "Post body is empty"
        super().__init__(self.code, self.message)


class DivisionNotFound(ServiceException):
    def __init__(self, division: str):
        self.code = 404
        self.message = f"{division} not found"
        super().__init__(self.code, self.message)
