import jwt

class JWTGenerator:
    def __init__(self, secret:str, algorithm="HS256"):
        self.secret = secret
        self.algorithm = algorithm
        
    def generate_token(self, payload:dict):
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)
    
    def decode_token(self, token:dict):
        return jwt.decode(token, self.secret, algorithm=self.algorithm)
