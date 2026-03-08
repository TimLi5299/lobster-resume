# 📖 飞书事件订阅配置指南

## 第 1 步：获取 App Secret

1. 访问 https://open.feishu.cn/
2. 登录飞书账号
3. 进入 **企业应用** → 找到你的应用（App ID: cli_a92fbec47f7b5cd4）
4. 点击 **凭证与基础信息**
5. 复制 **App Secret**
6. 替换 `server.py` 中的 `APP_SECRET = "请替换为你的 App Secret"`

---

## 第 2 步：启动回调服务

### 方案 A：本地测试（需要内网穿透）

```bash
# 1. 启动服务
cd /home/admin/.openclaw/workspace/feishu-callback
python3 server.py

# 2. 在另一个终端安装并启动 ngrok
# 下载：https://ngrok.com/download
ngrok http 8080

# 3. 复制 ngrok 提供的公网 URL（类似 https://xxx.ngrok.io）
```

### 方案 B：云服务器（推荐）

```bash
# 1. 在云服务器上启动服务
cd /home/admin/.openclaw/workspace/feishu-callback
nohup python3 server.py > callback.log 2>&1 &

# 2. 确认服务运行
ps aux | grep server.py

# 3. 获取服务器公网 IP
curl ifconfig.me

# 回调 URL: http://你的公网 IP:8080
```

---

## 第 3 步：飞书开放平台配置

### 3.1 启用事件订阅

1. 访问 https://open.feishu.cn/
2. 进入你的应用管理
3. 点击左侧 **事件订阅**
4. 开启 **启用事件订阅** 开关

### 3.2 配置 Request URL

1. 在 **Request URL** 输入框填写：
   ```
   http://你的公网 IP:8080
   ```
   或者 ngrok URL：
   ```
   https://xxx.ngrok.io
   ```

2. 点击 **保存**

3. 飞书会发送验证请求，你的服务会自动响应挑战值

### 3.3 订阅事件

在事件列表中，勾选以下事件：

| 事件类型 | 事件名 | 说明 |
|---------|--------|------|
| ✅ 接收消息 | `im.message` | 接收所有消息 |
| ✅ 群聊@机器人 | `im.message.group_at_msg` | 群里@机器人的消息 |
| ✅ 私聊消息 | `im.message.p2p_msg` | 一对一消息 |
| ✅ 群聊事件 | `im.chat` | 群聊相关事件 |

### 3.4 发布应用

1. 点击 **发布** 按钮
2. 等待审核（通常很快）
3. 发布成功后，机器人就可以接收消息了

---

## 第 4 步：测试

### 在群里测试

1. 在飞书群里@机器人
2. 查看 server.py 的控制台输出
3. 应该能看到收到的消息内容

### 预期输出

```
收到消息：{"header":{...}, "event":{...}}
消息类型：text
消息内容：{"text":"@机器人 你好"}
文本消息：@机器人 你好
```

---

## 🔧 故障排查

### 问题 1：URL 验证失败

**原因**：服务未启动或 URL 不可访问

**解决**：
- 确认服务已启动：`ps aux | grep server.py`
- 确认端口开放：`netstat -tlnp | grep 8080`
- 确认防火墙允许访问

### 问题 2：收不到消息

**原因**：事件未正确订阅

**解决**：
- 检查事件订阅是否已发布
- 确认机器人已添加到群里
- 检查群权限设置

### 问题 3：云服务器无法访问

**原因**：安全组未开放端口

**解决**：
- 在云控制台开放 8080 端口
- 检查 iptables 规则

---

## 📝 下一步

配置完成后，我可以：
1. ✅ 接收群里@我的消息
2. ✅ 自动回复或处理
3. ✅ 记录成长日记
4. ✅ 执行群任务

---

## 🎯 现在开始

请告诉我：

1. **你的 App Secret**（私信给我）
2. **你有云服务器吗？**（阿里云/腾讯云等）
3. **还是用内网穿透？**（ngrok/cloudflared）

我帮你完成后续配置！🔥
