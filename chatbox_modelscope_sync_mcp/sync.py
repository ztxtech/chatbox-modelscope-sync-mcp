import os
import sys
import json
import uuid
import shutil
from pathlib import Path
import requests


class ModelScopeMCPSync:
    """ModelScope MCP同步工具类"""

    def __init__(self, api_key=None, config_path=None, api_url=None):
        self.api_key = api_key
        self.config_path = config_path
        self.api_url = api_url or "https://www.modelscope.cn/api/v1/mcp/services/operational"

    def _get_config_path(self):
        """获取配置文件路径"""
        if self.config_path:
            return self.config_path

        # 自动检测Chatbox配置路径
        if os.name == 'nt':  # Windows
            return os.path.expanduser('~/AppData/Roaming/xyz.chatboxapp.app/config.json')
        elif os.name == 'posix':
            if sys.platform == 'darwin':  # macOS
                return os.path.expanduser('~/Library/Application Support/xyz.chatboxapp.app/config.json')
            else:  # Linux
                return os.path.expanduser('~/.config/xyz.chatboxapp.app/config.json')

        return 'config.json'

    def _get_api_key(self):
        """获取API密钥"""
        return self.api_key or os.getenv('MODELSCOPE_API_KEY')

    def call_modelscope_api(self):
        """调用ModelScope API"""
        api_key = self._get_api_key()
        if not api_key:
            raise ValueError("未提供API密钥，请使用--token参数或设置MODELSCOPE_API_KEY环境变量")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(self.api_url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API调用失败: {e}")

    def load_config(self, config_path):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 如果文件不存在，创建默认配置
            return {
                "settings": {
                    "mcp": {
                        "servers": []
                    }
                }
            }
        except json.JSONDecodeError as e:
            raise ValueError(f"配置文件格式错误: {e}")
        except Exception as e:
            raise RuntimeError(f"加载配置文件失败: {e}")

    def backup_config(self, config_path):
        """备份配置文件"""
        backup_path = f"{config_path}.bak"
        try:
            shutil.copy2(config_path, backup_path)
            print(f"已备份配置文件到: {backup_path}")
            return True
        except Exception as e:
            print(f"备份配置文件失败: {e}")
            return False

    def save_config(self, config, config_path):
        """保存配置文件"""
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"已更新配置文件: {config_path}")
            return True
        except Exception as e:
            raise RuntimeError(f"保存配置文件失败: {e}")

    def get_server_name(self, service):
        """智能获取服务器名称"""
        name = service.get('chinese_name', '').strip()
        if name:
            return name

        locales = service.get('locales', {})
        for lang in ['zh', 'en']:
            if lang in locales:
                name = locales[lang].get('name', '').strip()
                if name:
                    return name

        name = service.get('name', '').strip()
        if name:
            return name

        server_id = service.get('id', '').strip()
        if server_id:
            return server_id.replace('@', '').replace('/', '-')

        return None

    def filter_valid_servers(self, api_response):
        """过滤有效服务器"""
        if not api_response or 'Data' not in api_response or 'Result' not in api_response['Data']:
            return []

        valid_servers = []
        for service in api_response['Data']['Result']:
            name = self.get_server_name(service)
            if not name:
                continue

            urls = service.get('operational_urls', [])
            if not urls:
                continue

            url = urls[0].get('url')
            if not url:
                continue

            valid_servers.append({
                'name': name,
                'url': url,
                'id': service.get('id', 'unknown')
            })

        return valid_servers

    def sync(self, backup=True):
        """执行同步"""
        config_path = self._get_config_path()

        print("正在调用ModelScope API...")
        api_response = self.call_modelscope_api()

        print("正在加载配置文件...")
        config = self.load_config(config_path)

        valid_servers = self.filter_valid_servers(api_response)
        if not valid_servers:
            print("没有找到有效的MCP服务器")
            return False

        # 获取现有服务器
        servers = config['settings']['mcp']['servers']
        existing_urls = {s['transport']['url']: s for s in servers
                         if s.get('transport', {}).get('type') == 'http'}

        updated_count = 0
        added_count = 0

        for server_info in valid_servers:
            url = server_info['url']
            name = server_info['name']

            if url in existing_urls:
                old_server = existing_urls[url]
                if old_server['name'] != name:
                    old_name = old_server['name']
                    old_server['name'] = name
                    updated_count += 1
                    print(f"更新: {old_name} -> {name}")
            else:
                new_server = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "enabled": True,
                    "transport": {
                        "type": "http",
                        "url": url
                    }
                }
                servers.append(new_server)
                added_count += 1
                print(f"新增: {name}")

        if updated_count == 0 and added_count == 0:
            print("配置已是最新，无需更新")
            return True

        # 备份并更新配置
        if backup and os.path.exists(config_path):
            self.backup_config(config_path)

        self.save_config(config, config_path)
        print(f"同步完成: 更新{updated_count}个, 新增{added_count}个")
        return True