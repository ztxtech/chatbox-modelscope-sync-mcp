@echo off
set MODELSCOPE_API_KEY=your_api_key_here
set CHATBOX_CONFIG=%USERPROFILE%\.config\chatbox\config.json

echo 开始同步MCP服务器...
chatbox-modelscope-sync

if %errorlevel% equ 0 (
    echo 同步成功，重启Chatbox应用
) else (
    echo 同步失败，请检查错误信息
)