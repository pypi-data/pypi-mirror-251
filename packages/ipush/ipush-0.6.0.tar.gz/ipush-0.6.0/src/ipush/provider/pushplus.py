import json

from ..utils.fetch import Fetch
from ._provider import Provider


class PushPlus(Provider):
    """
    PushPlus通知
    """

    def __init__(self, token=''):
        self.token = token
        self.template = 'html'

    def _signature(self):
        pass

    def _geturl(self):
        """
        生成请求的 URL
        """
        return 'https://www.pushplus.plus/send'

    def settemplate(self, template):
        self.template = (
            template if template in ['html', 'markdown', 'txt', 'json'] else 'html'
        )
        return self

    def send(self, message, title=''):
        """
        发送通知
        :param message: 消息内容
        """
        req_url = self._geturl()

        headers = {
            'content-type': 'application/json',
        }
        req = Fetch()
        req.update_headers(headers)

        data = {
            'token': self.token,
            'title': '新消息' if title == '' else title,
            'content': message,
            'template': self.template,
        }
        data = json.dumps(data, indent=4)
        req.post(req_url, data=data.encode('utf-8'))
        return req.response
