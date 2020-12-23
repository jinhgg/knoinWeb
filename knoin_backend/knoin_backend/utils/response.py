class ResponseData:
    def __init__(self, code=0, msg='', data={}):
        self.code = code
        self.msg = msg
        self.data = data


rs = ResponseData(1, 'haha', {'isok': True})

print(rs.code)