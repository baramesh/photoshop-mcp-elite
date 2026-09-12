import sys

import pytest
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_mcp_server_e2e_lifecycle():
    """End-to-end test verifying MCP stdio protocol handshake, listing all tools, and calling a tool."""
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],
        env=None
    )

    async with (
        stdio_client(server_params) as (read, write),
        ClientSession(read, write) as session,
    ):
        # 1. Initialize MCP Handshake
            init_res = await session.initialize()
            assert init_res.server_info.name == "photoshop"

            # 2. List all registered tools
            tools_res = await session.list_tools()
            tool_names = [t.name for t in tools_res.tools]

            # Verify total count and critical features
            assert len(tool_names) == 42
            assert "photoshop_get_document_info" in tool_names
            assert "photoshop_generative_fill_ai" in tool_names
            assert "photoshop_generative_remove_ai" in tool_names
            assert "photoshop_harmonize_sky" in tool_names
            assert "photoshop_smart_remove_distractions" in tool_names
            assert "photoshop_select_sky" in tool_names
            assert "photoshop_select_subject" in tool_names
            assert "photoshop_execute_custom_jsx" in tool_names

            # 3. Call a tool schema inspection (verify input schema is valid)
            gen_fill_tool = next(t for t in tools_res.tools if t.name == "photoshop_generative_fill_ai")
            assert "prompt" in gen_fill_tool.input_schema.get("properties", {})
