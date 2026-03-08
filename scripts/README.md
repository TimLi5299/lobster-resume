# 每日早报系统

## 📋 功能
每天早晨 8:00 自动推送早报到飞书，包含：
- 昨日完成的重要事项
- 今日待办任务（延续 + 新增）

## 🔧 配置说明

### ✅ 已配置（OpenClaw 飞书集成）

本系统使用 OpenClaw 内置的飞书 API 集成，**无需额外配置 Webhook**。

早报会通过你当前使用的飞书对话直接发送给你。

### 定时任务
```bash
# 已配置 cron（每天 8:00 生成）
crontab -l
# 输出：0 8 * * * /home/admin/.openclaw/workspace/scripts/daily-briefing.sh > /tmp/daily-briefing-$(date +\%Y\%m\%d).txt 2>&1
```

## 📁 文件说明
- `daily-briefing.sh` - 早报生成脚本
- `send-feishu-briefing.sh` - 飞书发送脚本（备用，使用 Webhook 方式）
- `.feishu_webhook` - 飞书 Webhook 配置（已弃用，保留兼容）

## 🧪 测试
```bash
# 手动测试生成
/home/admin/.openclaw/workspace/scripts/daily-briefing.sh
```

## 📝 记忆格式
为了让早报系统正常工作，请确保每天的记忆文件包含：

```markdown
## 重要事件
- 事件 1 描述
- 事件 2 描述

## 待办事项
- [x] 已完成任务
- [ ] 未完成任务
```

系统会自动提取这些内容生成早报。
