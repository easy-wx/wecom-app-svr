# 参考文档: https://developer.work.weixin.qq.com/document/path/96469
import time
import xml.etree.cElementTree as ET


class RspMsg(object):
    def __init__(self, msg_type, to_user_name, from_user_name):
        self.msg_type = msg_type
        self.to_user_name = to_user_name
        self.from_user_name = from_user_name
        self.create_time = int(time.time())
        self.xml_tree = ET.Element('xml')

    def insert_elem(self, name, value):
        curr_node = self.xml_tree

        for n in name.split('/'):
            if curr_node.find(n) is None:
                e = ET.Element(n)
                curr_node.append(e)
            curr_node = curr_node.find(n)
        curr_node.text = value

    def dump_xml(self):
        self.update_xml()
        return ET.tostring(self.xml_tree, encoding='ascii', method='html')

    def update_xml(self):
        self.insert_elem("MsgType", self.msg_type)
        self.insert_elem("ToUserName", self.to_user_name)
        self.insert_elem("FromUserName", self.from_user_name)


class RspTextMsg(RspMsg):
    def __init__(self, from_user_name=None, to_user_name=None, content=None):
        super().__init__('text', from_user_name, to_user_name)
        self.content = content

    def update_xml(self):
        super().update_xml()
        self.insert_elem('Content', self.content)


class RspImageMsg(RspMsg):
    def __init__(self, from_user_name=None, to_user_name=None, media_id=None):
        super().__init__('image', from_user_name, to_user_name)
        self.media_id = media_id

    def update_xml(self):
        super().update_xml()
        self.insert_elem('Image/MediaId', self.media_id)


class RspVoiceMsg(RspMsg):
    def __init__(self, from_user_name=None, to_user_name=None, media_id=None):
        super().__init__('voice', from_user_name, to_user_name)
        self.media_id = media_id

    def update_xml(self):
        super().update_xml()
        self.insert_elem('Voice/MediaId', self.media_id)


class RspVideoMsg(RspMsg):
    def __init__(self, from_user_name=None, to_user_name=None, media_id=None, title=None, description=None):
        super().__init__('video', from_user_name, to_user_name)
        self.media_id = media_id
        self.title = title
        self.description = description

    def update_xml(self):
        super().update_xml()
        self.insert_elem('Video/MediaId', self.media_id)
        self.insert_elem('Video/Title', self.title)
        self.insert_elem('Video/Description', self.description)
