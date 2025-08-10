#!/bin/bash
# 设置环境变量
export MODELSCOPE_API_KEY="your_api_key_here"
export CHATBOX_CONFIG="$HOME/.config/chatbox/config.json"

# 执行同步
echo "开始同步MCP服务器..."
chatbox-modelscope-sync

if [ $? -eq 0 ]; then
    echo "同步成功，重启Chatbox应用"
    # 这里可以添加重启Chatbox的命令
else
    echo "同步失败，请检查错误信息"
fi