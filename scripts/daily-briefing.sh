#!/bin/bash

# Daily Briefing - 每日早报生成脚本
# 用途：汇总昨天的活动和今天的待办
# 调用：./daily-briefing.sh [日期 YYYY-MM-DD]

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"

# 获取日期（默认昨天）
if [ -n "$1" ]; then
    TARGET_DATE="$1"
    YESTERDAY="$1"
    TODAY=$(date -d "$TARGET_DATE + 1 day" +%Y-%m-%d)
else
    YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
    TODAY=$(date +%Y-%m-%d)
fi

YESTERDAY_FILE="$MEMORY_DIR/${YESTERDAY}.md"
TODAY_FILE="$MEMORY_DIR/${TODAY}.md"

echo "📅 早报生成中..."
echo "日期：$TODAY"
echo "汇总昨日：$YESTERDAY"
echo ""

# 检查昨天的记忆文件是否存在
if [ ! -f "$YESTERDAY_FILE" ]; then
    echo "⚠️ 未找到昨天的记忆文件：$YESTERDAY_FILE"
    echo "可能昨天没有记录活动"
    exit 0
fi

# 提取昨天的重要事件
echo "━━━━━━━━━━━━━━━━━━━━"
echo "🌅 昨日回顾 ($YESTERDAY)"
echo "━━━━━━━━━━━━━━━━━━━━"
echo ""

# 提取"重要事件"部分
if grep -q "## 重要事件" "$YESTERDAY_FILE"; then
    sed -n '/## 重要事件/,/## 待办事项/p' "$YESTERDAY_FILE" | grep -v "## 重要事件" | grep -v "## 待办事项" | grep -v "^$"
else
    echo "📝 昨日无重要事件记录"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━"
echo "📋 今日待办 ($TODAY)"
echo "━━━━━━━━━━━━━━━━━━━━"
echo ""

# 提取昨天的未完成待办
if grep -q "## 待办事项" "$YESTERDAY_FILE"; then
    UNDONE=$(sed -n '/## 待办事项/,$p' "$YESTERDAY_FILE" | grep -E "^\- \[ \]" || echo "")
    if [ -n "$UNDONE" ]; then
        echo "⏳ 延续任务（从昨日）:"
        echo "$UNDONE"
        echo ""
    fi
fi

# 检查今天的记忆文件是否有新增待办
if [ -f "$TODAY_FILE" ] && grep -q "## 待办事项" "$TODAY_FILE"; then
    echo "🎯 今日新增任务:"
    sed -n '/## 待办事项/,$p' "$TODAY_FILE" | grep -v "## 待办事项" | grep -v "^$"
    echo ""
else
    echo "💡 暂无今日新增任务"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━"
echo "✨ 祝你今天高效！"
echo "━━━━━━━━━━━━━━━━━━━━"
