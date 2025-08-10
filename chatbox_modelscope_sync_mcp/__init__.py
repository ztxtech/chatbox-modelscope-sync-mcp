"""
Chatbox ModelScope MCP Sync Tool
一键同步ModelScope MCP服务器到Chatbox配置
"""

__version__ = "1.0.0"
__author__ = "ModelScope"
__email__ = "support@modelscope.cn"

from .sync import ModelScopeMCPSync

__all__ = ['ModelScopeMCPSync']