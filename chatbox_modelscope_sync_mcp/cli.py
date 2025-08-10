import argparse
import sys
from .sync import ModelScopeMCPSync


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        description='Chatbox ModelScope MCP Sync Tool',
        prog='chatbox-modelscope-sync'
    )

    parser.add_argument(
        '--token', '-t',
        help='ModelScope API Token (也可以使用 MODELSCOPE_API_KEY 环境变量)'
    )

    parser.add_argument(
        '--path', '-p',
        help='Chatbox配置文件路径 (也可以使用 CHATBOX_CONFIG 环境变量)'
    )

    parser.add_argument(
        '--url',
        help='ModelScope MCP API URL (默认: https://www.modelscope.cn/api/v1/mcp/services/operational)'
    )

    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='不创建配置文件备份'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    try:
        syncer = ModelScopeMCPSync(
            api_key=args.token,
            config_path=args.path,
            api_url=args.url
        )

        success = syncer.sync(backup=not args.no_backup)

        if success:
            print("\n✅ MCP服务器同步成功!")
            print("重启Chatbox应用以应用新配置")
        else:
            print("\n❌ MCP服务器同步失败")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()