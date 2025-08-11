from chatbox_modelscope_sync_mcp import ModelScopeMCPSync

syncer = ModelScopeMCPSync()
success = syncer.export_mcp_json_to_file('./mcp.json')
# syncer.sync()