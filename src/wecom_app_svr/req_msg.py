# 参考文档: https://developer.work.weixin.qq.com/document/path/96466
class UserInfo(object):
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id


class ReqMsg(object):
    def __init__(self, xml_tree):
        self.to_user = xml_tree.find('ToUserName').text
        self.from_user = xml_tree.find('FromUserName').text
        self.create_time = int(xml_tree.find('CreateTime').text)
        self.msg_type = xml_tree.find('MsgType').text
        self.msg_id = xml_tree.find('MsgId').text
        self.agent_id = xml_tree.find('AgentID').text

    @staticmethod
    def create_msg(xml_tree):
        msg_type = xml_tree.find('MsgType').text
        if msg_type == 'text':
            return TextReqMsg(xml_tree)
        elif msg_type == 'event':
            return EventReqMsg(xml_tree)
        elif msg_type == 'image':
            return ImageReqMsg(xml_tree)
        elif msg_type == 'voice':
            return VoiceReqMsg(xml_tree)
        elif msg_type == 'video':
            return VideoReqMsg(xml_tree)
        else:
            return None


class TextReqMsg(ReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.msg_type = 'text'
        self.content = xml_tree.find('Content').text


class EventReqMsg(ReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.msg_type = 'event'
        self.event_type = xml_tree.find('Event').find('EventType').text
        # self.event_key = None


class ImageReqMsg(ReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.msg_type = 'image'
        self.image_url = xml_tree.find('PicUrl').text
        self.media_id = xml_tree.find('MediaId').text


class VoiceReqMsg(ReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.msg_type = 'voice'
        self.media_id = xml_tree.find('MediaId').text
        self.format = xml_tree.find('Format').text


class VideoReqMsg(ReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.msg_type = 'video'
        self.media_id = xml_tree.find('MediaId').text
        self.thumb_media_id = xml_tree.find('ThumbMediaId').text
