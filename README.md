# astrbot_plugin_blocklist

按 QQ 号拦截消息的 AstrBot 插件。名单内的用户发来的**私聊 / 群聊**消息会被直接拦下：既不进入上下文，也不会触发任何回复。

## 安装

把整个 `astrbot_plugin_blocklist` 目录丢进 AstrBot 的 `data/plugins/` 下，然后在面板里重载插件（AstrBot 没有文件监听，必须手动重载或重启容器）。

## 配置

在面板的插件配置里填：

| 字段 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `blocked_ids` | list | `[]` | 黑名单 QQ 号列表（字符串） |
| `log_blocked` | bool | `true` | 拦截时是否打日志 |

## 为什么要用 `sys.maxsize` 当优先级

AstrBot 内置星 `astrbot` 的 `handle_empty_mention` 用的是 `priority = maxsize - 1`。当一条消息**只有一个 @ 或只有唤醒前缀**时，它会直接发起一次 LLM 请求。

如果本插件用普通优先级（比如 `10000`），黑名单用户只 @ 一下就能绕过去拿到回复。

所以 `guard` 必须用 `sys.maxsize`，才能抢在内置星之前把事件 `stop_event()` 掉。

```python
@filter.event_message_type(filter.EventMessageType.ALL, priority=sys.maxsize)
```

> `star_handler` 按 `-priority` 降序排，数字大的先跑。

## 许可

MIT
