class MietrechtException(Exception):
    def __init__(self, message, http_code):
        self.message = message
        self.http_status_code = http_code
        super(Exception, self).__init__(self.message)
    
class BadRequestException(MietrechtException):
    def __init__(self, message):
        MietrechtException.__init__(self, message, 400)

class NonFoundException(MietrechtException):
    def __init__(self, message):
        MietrechtException.__init__(self, message, 404)

class NonFoundException(MietrechtException):
    def __init__(self, message):
        MietrechtException.__init__(self, message, 404)

class MethodNotAllowedException(MietrechtException):
    def __init__(self, message):
        MietrechtException.__init__(self, message, 405)

