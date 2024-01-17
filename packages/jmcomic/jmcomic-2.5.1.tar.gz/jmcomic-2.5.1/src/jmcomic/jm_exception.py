# 该文件存放jmcomic的异常机制设计和实现
from .jm_entity import *


class JmcomicException(Exception):
    """
    jmcomic 模块异常
    """

    def __init__(self, msg: str, context: dict):
        self.msg = msg
        self.context = context

    def from_context(self, key):
        return self.context[key]


class ResponseUnexpectedException(JmcomicException):
    """
    响应不符合预期异常
    """

    @property
    def resp(self):
        return self.from_context(ExceptionTool.CONTEXT_KEY_RESP)


class RegularNotMatchException(ResponseUnexpectedException):
    """
    正则表达式不匹配异常
    """

    @property
    def error_text(self):
        return self.from_context(ExceptionTool.CONTEXT_KEY_HTML)

    @property
    def pattern(self):
        return self.from_context(ExceptionTool.CONTEXT_KEY_RE_PATTERN)


class JsonResolveFailException(ResponseUnexpectedException):
    pass


class MissingAlbumPhotoException(ResponseUnexpectedException):
    """
    缺少本子/章节异常
    """

    @property
    def error_jmid(self) -> str:
        return self.from_context(ExceptionTool.CONTEXT_KEY_MISSING_JM_ID)


class ExceptionTool:
    """
    抛异常的工具
    1: 能简化 if-raise 语句的编写
    2: 有更好的上下文信息传递方式
    """

    CONTEXT_KEY_RESP = 'resp'
    CONTEXT_KEY_HTML = 'html'
    CONTEXT_KEY_RE_PATTERN = 'pattern'
    CONTEXT_KEY_MISSING_JM_ID = 'missing_jm_id'

    @classmethod
    def raises(cls,
               msg: str,
               context: dict = None,
               etype: Optional[Type[Exception]] = None,
               ):
        """
        抛出异常

        :param msg: 异常消息
        :param context: 异常上下文数据
        :param etype: 异常类型，默认使用 JmcomicException
        """
        if context is None:
            context = {}

        if etype is None:
            etype = JmcomicException

        # 异常对象
        e = etype(msg, context)

        # 异常处理建议
        advice = JmModuleConfig.REGISTRY_EXCEPTION_ADVICE.get(etype, None)

        if advice is not None:
            advice(e)

        raise e

    @classmethod
    def raises_regex(cls,
                     msg: str,
                     html: str,
                     pattern: Pattern,
                     ):
        cls.raises(
            msg,
            {
                cls.CONTEXT_KEY_HTML: html,
                cls.CONTEXT_KEY_RE_PATTERN: pattern,
            },
            RegularNotMatchException,
        )

    @classmethod
    def raises_resp(cls,
                    msg: str,
                    resp,
                    etype=ResponseUnexpectedException
                    ):
        cls.raises(
            msg, {
                cls.CONTEXT_KEY_RESP: resp
            },
            etype,
        )

    @classmethod
    def raise_missing(cls,
                      resp,
                      jmid: str,
                      ):
        """
        抛出本子/章节的异常
        :param resp: 响应对象
        :param jmid: 禁漫本子/章节id
        """
        url = resp.url

        req_type = "本子" if "album" in url else "章节"
        cls.raises(
            (
                f'请求的{req_type}不存在！({url})\n'
                '原因可能为:\n'
                f'1. id有误，检查你的{req_type}id\n'
                '2. 该漫画只对登录用户可见，请配置你的cookies，或者使用移动端Client（api）\n'
            ),
            {
                cls.CONTEXT_KEY_RESP: resp,
                cls.CONTEXT_KEY_MISSING_JM_ID: jmid,
            },
            MissingAlbumPhotoException,
        )

    @classmethod
    def require_true(cls, case: bool, msg: str):
        if case:
            return

        cls.raises(msg)
