class BaseResponse:
    def __init__(self, success=True, data=None, message=None):
        self.success = success
        self.data = data
        self.message = message

    # 返回JSON格式数据
    def __dict__(self):
        return {
            'success': self.success,
            'data': self.data,
            'message': self.message
        }
