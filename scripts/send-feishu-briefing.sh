#!/bin/bash

# 飞书早报发送脚本
# 使用 OpenClaw message 工具直接发送，无需 webhook

set -e

# 生成早报内容
BRIEFING=$(/home/admin/.openclaw/workspace/scripts/daily-briefing.sh)

# 使用 OpenClaw message 工具发送（通过 stdin 传递消息）
echo "$BRIEFING" | openclaw message send --channel feishu --stdin

echo "✅ 早报已发送到飞书"
