import logging
import sys

from wecom_app_svr import WecomAppServer, RspTextMsg, RspImageMsg, RspVideoMsg


def msg_handler(req_msg):
    if req_msg.msg_type == 'text' and req_msg.content.strip() == 'help':
        ret = RspTextMsg()
        ret.content = f'msg_type: {req_msg.msg_type}, content: {req_msg.content}'
        return ret
    if req_msg.msg_type == 'image':
        ret = RspImageMsg(req_msg.to_user, req_msg.from_user, req_msg.media_id)
        return ret
    if req_msg.msg_type == 'video':
        ret = RspVideoMsg(req_msg.to_user, req_msg.from_user, req_msg.media_id, "视频标题", "视频描述")
        return ret

    # 返回消息类型
    ret = RspTextMsg()
    ret.content = f'msg_type: {req_msg.msg_type}, content: {req_msg.content}'

    return ret


def event_handler(req_msg):
    # TODO
    ret = RspTextMsg()
    if req_msg.event_type == 'add_to_chat':  # 入群事件处理
        ret.content = f'msg_type: {req_msg.msg_type}\n群会话ID: {req_msg.chat_id}\n查询用法请回复: help'
    return ret


def main():
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger().setLevel(logging.INFO)

    token = 'xxx'  # 3个x
    aes_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # 43个x
    corp_id = 'YOUR_CORP_ID'
    host = '0.0.0.0'
    port = 5001
    server = WecomAppServer("wecom-app-svr", host, port, path='/wecom_app_cb', token=token, aes_key=aes_key,
                            corp_id=corp_id)

    server.set_message_handler(msg_handler)
    server.set_event_handler(event_handler)
    server.run()


if __name__ == '__main__':
    main()
