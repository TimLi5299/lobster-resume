# 🧪 老铁的 AI 实验室 - 网站部署指南

## 📦 网站文件说明

```
website-laotie/
├── index.html      # 主页面（不用改）
├── works.js        # 作品数据（在这里添加作品！）
├── images/         # 放作品图片的文件夹（自己创建）
└── README.md       # 这个文件
```

---

## ✏️ 如何添加作品

打开 `works.js`，按照这个格式添加：

```javascript
{
    id: 4,  // 编号递增
    title: "作品标题",
    date: "2026-03-05",
    type: "AI 绘画",  // 可选：AI 绘画/AI 写作/AI 视频/AI 音乐/数据分析/其他
    cover: "images/work4.jpg",  // 封面图路径
    description: "作品描述...",
    aiTools: ["Midjourney", "GPT-4"],  // 用的 AI 工具
    tags: ["标签 1", "标签 2"]
},
```

---

## 🚀 部署到服务器（3 步搞定）

### 第 1 步：买服务器

**推荐：** 阿里云 或 腾讯云  
**配置：** 最便宜的就行（1 核 2G，约 ¥100/月）  
**系统：** 选 Ubuntu 22.04

### 第 2 步：上传文件

**方法 A：用 FTP 工具（推荐新手）**
1. 下载 FileZilla（免费）
2. 连接服务器（IP、用户名、密码）
3. 把这 3 个文件拖到服务器的 `/var/www/html` 目录

**方法 B：用命令（如果你会用 SSH）**
```bash
# 登录服务器
ssh root@你的服务器 IP

# 创建网站目录
mkdir -p /var/www/laotie.ai

# 上传文件（在你的 Mac 上执行）
scp -r website-laotie/* root@你的服务器 IP:/var/www/laotie.ai/
```

### 第 3 步：安装 Nginx（网站服务器）

在服务器上执行：
```bash
# 安装 Nginx
apt update
apt install nginx -y

# 创建网站配置
cat > /etc/nginx/sites-available/laotie.ai << 'EOF'
server {
    listen 80;
    server_name laotie.ai www.laotie.ai;
    root /var/www/laotie.ai;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/laotie.ai /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# 重启 Nginx
systemctl restart nginx
```

---

## 🔗 绑定域名 laotie.ai

### 1. 域名解析

在你的域名注册商那里（阿里云/腾讯云/GoDaddy 等）：

**添加两条 A 记录：**
| 主机记录 | 记录类型 | 记录值 |
|----------|----------|--------|
| @ | A | 你的服务器 IP |
| www | A | 你的服务器 IP |

### 2. 等待生效

DNS 生效需要 10 分钟到 24 小时不等。

### 3. 测试

在浏览器输入 `http://laotie.ai`，应该能看到你的网站了！

---

## 🔒 加 HTTPS（可选但推荐）

在服务器上执行：
```bash
# 安装 Certbot
apt install certbot python3-certbot-nginx -y

# 自动申请证书
certbot --nginx -d laotie.ai -d www.laotie.ai
```

按提示输入邮箱，同意条款，就搞定了！

---

## 📝 日常更新作品

**方法 1：直接改服务器上的文件**
```bash
ssh root@你的服务器 IP
nano /var/www/laotie.ai/works.js
# 修改后保存，刷新网页即可
```

**方法 2：在 Mac 上改好再上传**
```bash
# 在 Mac 上编辑 works.js
# 然后上传
scp works.js root@你的服务器 IP:/var/www/laotie.ai/
```

---

## ❓ 遇到问题？

1. **网页打不开** → 检查服务器防火墙，确保 80 端口开放
2. **图片不显示** → 检查图片路径是否正确
3. **域名解析失败** → 等 DNS 生效，或检查 DNS 设置

随时问我！🚀
