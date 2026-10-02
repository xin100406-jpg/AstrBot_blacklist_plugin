import sys

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star


class BlockList(Star):
    """黑名单:拦截指定 QQ 号发来的私聊/群聊消息。"""

    def __init__(self, context: Context, config: dict | None = None):
        super().__init__(context)
        cfg = config or {}
        self.blocked = {
            str(x).strip() for x in (cfg.get("blocked_ids") or []) if str(x).strip()
        }
        self.log_blocked = bool(cfg.get("log_blocked", True))

    # priority 必须是 sys.maxsize。内置星 astrbot 的 handle_empty_mention 用的是
    # maxsize - 1,它在“只有一个 @ / 只有唤醒前缀”的消息上会直接发起一次 LLM 请求,
    # 排在普通插件(如本插件原先的 10000)前面 —— 于是黑名单用户只 @ 一下照样能拿到回复。
    # 取 maxsize 才能抢在它之前拦下来。
    @filter.event_message_type(filter.EventMessageType.ALL, priority=sys.maxsize)
    async def guard(self, event: AstrMessageEvent):
        sender = str(event.get_sender_id())
        if sender in self.blocked:
            if self.log_blocked:
                logger.info(
                    f"[blocklist] 已拦截 {sender} 的消息({event.get_message_type()})"
                )
            event.stop_event()
