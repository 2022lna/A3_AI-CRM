# 自定义空值异常类
class EmptyValueError(Exception):
    """当某个值为空（如 None 或空字符串、空列表等）时抛出"""
    def __init__(self, message="值不能为空"):
        self.message = message
        super().__init__(self.message)