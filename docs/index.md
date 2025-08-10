# Chatbox ModelScope MCP Sync

[![PyPI version](https://badge.fury.io/py/chatbox-modelscope-sync-mcp.svg)](https://badge.fury.io/py/chatbox-modelscope-sync-mcp)
[![Python](https://img.shields.io/pypi/pyversions/chatbox-modelscope-sync-mcp.svg)](https://pypi.org/project/chatbox-modelscope-sync-mcp/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

一键同步ModelScope MCP服务器到Chatbox配置，支持智能名称选择和跨平台配置路径检测。

## 🚀 功能特性

- **一键同步** 自动备份原配置文件并更新MCP服务器列表
- **智能命名** 优先使用中文名称，支持多语言回退策略
- **跨平台** 自动检测Windows/macOS/Linux的Chatbox配置路径
- **灵活配置** 支持命令行参数、环境变量和配置文件
- **安全备份** 每次更新前自动创建配置文件备份
- **增量更新** 智能识别新增和更新的服务器，避免重复

## 📦 安装

### 通过pip安装（推荐）

```bash
pip install chatbox-modelscope-sync-mcp
```

### 从源码安装

```bash
git clone https://github.com/ztxtech/chatbox-modelscope-sync-mcp.git
cd chatbox-modelscope-sync-mcp
pip install -e .
```

## 🎯 快速开始

### 1. 获取ModelScope API Token

1. 访问 [ModelScope官网](https://www.modelscope.cn)
2. 登录后进入个人中心 → API令牌
3. 创建并复制你的API令牌

### 2. 运行同步

#### 命令行方式

```bash
# 使用命令行参数
chatbox-modelscope-sync --token YOUR_API_TOKEN

# 简写命令
chatbox-mcp-sync -t YOUR_TOKEN

# 指定配置文件路径
chatbox-modelscope-sync --token YOUR_TOKEN --path /path/to/config.json
```

#### 环境变量方式

```bash
# 设置环境变量
export MODELSCOPE_API_KEY=your_api_token_here
export CHATBOX_CONFIG=/path/to/config.json  # 可选

# 运行同步
chatbox-modelscope-sync
```

#### Python代码方式

```python
from chatbox_modelscope_sync_mcp import ModelScopeMCPSync

# 基本用法
syncer = ModelScopeMCPSync(api_key="your_token")
syncer.sync()

# 高级用法
syncer = ModelScopeMCPSync(
    api_key="your_token",
    config_path="/path/to/config.json",
    api_url="https://custom-api.com/mcp"
)
syncer.sync(backup=True)
```

## ⚙️ 配置优先级

配置项按以下优先级加载：

1. **命令行参数**（最高优先级）
   - `--token`, `--path`, `--url`

2. **环境变量**
   - `MODELSCOPE_API_KEY`
   - `CHATBOX_CONFIG`

3. **自动检测**（最低优先级）
   - 自动检测Chatbox默认配置路径

## 🖥️ 支持的平台

| 操作系统 | 默认配置路径 |
|----------|--------------|
| **Windows** | `~/AppData/Roaming/xyz.chatboxapp.app/config.json` |
| **macOS** | `~/Library/Application Support/xyz.chatboxapp.app/config.json` |
| **Linux** | `~/.config/xyz.chatboxapp.app/config.json` |

## 📋 命令行选项

```bash
chatbox-modelscope-sync --help

# 输出：
usage: chatbox-modelscope-sync [-h] [--token TOKEN] [--path PATH] [--url URL] [--no-backup] [--version]

Chatbox ModelScope MCP Sync Tool

options:
  -h, --help            显示帮助信息
  -t, --token TOKEN     ModelScope API Token (也可以使用 MODELSCOPE_API_KEY 环境变量)
  -p, --path PATH       Chatbox配置文件路径 (也可以使用 CHATBOX_CONFIG 环境变量)
  --url URL             ModelScope MCP API URL
  --no-backup           不创建配置文件备份
  -v, --version         显示版本信息
```

## 🔧 高级用法

### 自定义API端点

如果你的ModelScope服务部署在自定义地址：

```bash
chatbox-modelscope-sync \
  --token YOUR_TOKEN \
  --url https://your-domain.com/api/v1/mcp/services/operational
```

### 批量操作脚本

创建批量更新脚本：

```bash
#!/bin/bash
# sync-mcp.sh

TOKENS=("token1" "token2" "token3")
for token in "${TOKENS[@]}"; do
    echo "正在同步 token: ${token:0:8}..."
    chatbox-modelscope-sync --token "$token" --no-backup
    sleep 2
done
```

### 定时同步

使用cron定时同步（Linux/macOS）：

```bash
# 每小时同步一次
0 * * * * /usr/local/bin/chatbox-modelscope-sync --token YOUR_TOKEN

# 每天凌晨3点同步
0 3 * * * /usr/local/bin/chatbox-modelscope-sync --token YOUR_TOKEN
```

## 📝 配置示例

### 更新前配置

```json
{
  "settings": {
    "mcp": {
      "servers": [
        {
          "id": "existing-server",
          "name": "现有服务器",
          "enabled": true,
          "transport": {
            "type": "http",
            "url": "http://localhost:8080"
          }
        }
      ]
    }
  }
}
```

### 更新后配置

```json
{
  "settings": {
    "mcp": {
      "servers": [
        {
          "id": "existing-server",
          "name": "现有服务器",
          "enabled": true,
          "transport": {
            "type": "http",
            "url": "http://localhost:8080"
          }
        },
        {
          "id": "a1b2c3d4-e5f6-7890-abcd-1234567890ef",
          "name": "ModelScope中文模型",
          "enabled": true,
          "transport": {
            "type": "http",
            "url": "https://modelscope.cn/api/mcp/server1"
          }
        },
        {
          "id": "b2c3d4e5-f6g7-8901-bcde-2345678901fa",
          "name": "ModelScope English Model",
          "enabled": true,
          "transport": {
            "type": "http",
            "url": "https://modelscope.cn/api/mcp/server2"
          }
        }
      ]
    }
  }
}
```

## 🛠️ 故障排除

### 常见问题

#### 1. API Token无效

**错误信息**: `API调用失败: 401 Unauthorized`

**解决方案**:
- 检查API Token是否正确
- 确保Token有访问MCP服务的权限
- 重新生成Token并重试

#### 2. 配置文件路径错误

**错误信息**: `加载配置文件失败: [Errno 2] No such file or directory`

**解决方案**:
- 确认Chatbox已安装并运行过一次
- 手动指定配置文件路径: `--path /path/to/config.json`
- 检查文件权限

#### 3. 权限不足

**错误信息**: `保存配置文件失败: [Errno 13] Permission denied`

**解决方案**:
- 以管理员身份运行命令
- 检查文件和目录权限
- 使用sudo（Linux/macOS）

#### 4. 网络连接问题

**错误信息**: `API调用失败: Connection timeout`

**解决方案**:
- 检查网络连接
- 确认防火墙设置
- 尝试使用代理

### 调试模式

```bash
# 查看详细日志
chatbox-modelscope-sync --token YOUR_TOKEN --verbose

# 测试API连接
python -c "
from chatbox_modelscope_sync_mcp import ModelScopeMCPSync
syncer = ModelScopeMCPSync(api_key='your_token')
result = syncer.call_modelscope_api()
print('API连接成功' if result else 'API连接失败')
"
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

### 开发环境设置

```bash
git clone https://github.com/ztxtech/chatbox-modelscope-sync-mcp.git
cd chatbox-modelscope-sync-mcp
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/

# 代码格式化
black chatbox_modelscope_sync_mcp/
isort chatbox_modelscope_sync_mcp/
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙋‍♂️ 支持

- 📧 邮箱: ztxtechfoxmail.com
- 🐛 Issue: [GitHub Issues](https://github.com/ztxtech/chatbox-modelscope-sync-mcp/issues)
- 💬 讨论: [GitHub Discussions](https://github.com/ztxtech/chatbox-modelscope-sync-mcp/discussions)

## 🔄 更新日志

### v0.0.1 (2025-8-10)
- ✨ 初始版本发布
- 🎯 支持一键同步ModelScope MCP服务器
- 🌍 跨平台配置路径自动检测
- 🧠 智能服务器名称选择
- 🛡️ 配置文件自动备份
- 📦 PyPI包发布

---

**Made with ❤️ by ztxtech**