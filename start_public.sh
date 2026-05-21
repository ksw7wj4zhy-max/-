#!/bin/bash
# 合成大网鱼 - 公网访问启动脚本

echo "🚀 启动合成大网鱼公网访问..."

# 1. 确保HTTP服务器运行
pkill -f "http.server 8000" 2>/dev/null
sleep 1
cd /Users/black/WorkBuddy/20260507222124
nohup python3 -m http.server 8000 --bind 0.0.0.0 > /tmp/game_http.log 2>&1 &
echo "✅ HTTP服务器已启动 (端口8000)"

sleep 2

# 2. 启动localtunnel
export PATH=/Users/black/.workbuddy/binaries/node/versions/22.12.0/bin:$PATH
cd /Users/black/.workbuddy/binaries/node/workspace
nohup node node_modules/.bin/lt --port 8000 > /tmp/game_tunnel.log 2>&1 &
echo "✅ 内网穿透已启动"

sleep 3

# 3. 显示公网链接
echo ""
echo "🌐 公网访问链接："
tail -1 /tmp/game_tunnel.log
echo ""
echo "📱 手机访问：复制上面的https链接，在手机浏览器打开"
echo "💻 电脑访问：http://localhost:8000"
echo ""
echo "📝 日志位置："
echo "   HTTP服务器: /tmp/game_http.log"
echo "   内网穿透: /tmp/game_tunnel.log"
