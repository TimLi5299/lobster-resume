#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书事件订阅回调服务
接收飞书群消息和@机器人消息
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import hashlib
import base64
import time

# 配置（需要替换）
APP_ID = "cli_a92fbec47f7b5cd4"
APP_SECRET = "9obOSZkki67hshXsKI1qAfnvCM4jvwnS"
PORT = 8082

class FeishuEventHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            print(f"收到消息：{json.dumps(data, ensure_ascii=False)}")
            
            # 处理挑战验证
            if 'challenge' in data:
                self.send_challenge_response(data['challenge'])
                return
            
            # 处理消息
            if 'header' in data and 'event' in data:
                self.handle_message(data)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
            
        except Exception as e:
            print(f"处理错误：{e}")
            self.send_response(500)
            self.end_headers()
    
    def send_challenge_response(self, challenge):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'challenge': challenge}).encode())
    
    def handle_message(self, data):
        """处理飞书消息"""
        event = data.get('event', {})
        message = event.get('message', {})
        
        # 提取消息内容
        msg_type = message.get('message_type')
        content = message.get('content')
        
        print(f"消息类型：{msg_type}")
        print(f"消息内容：{content}")
        
        # 如果是文本消息
        if msg_type == 'text':
            try:
                content_json = json.loads(content)
                text = content_json.get('text', '')
                print(f"文本消息：{text}")
                
                # 在这里处理你的业务逻辑
                # 比如调用 AI 接口回复
                
            except Exception as e:
                print(f"解析消息内容失败：{e}")
    
    def log_message(self, format, *args):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")

def main():
    print(f"🚀 飞书事件订阅服务启动中...")
    print(f"监听端口：{PORT}")
    print(f"回调 URL: http://你的服务器 IP:{PORT}")
    print(f"\n请在飞书开放平台配置此 URL 为事件订阅地址")
    
    server = HTTPServer(('0.0.0.0', PORT), FeishuEventHandler)
    print(f"\n✅ 服务已启动，等待飞书消息...")
    server.serve_forever()

if __name__ == '__main__':
    main()
