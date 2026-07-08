from fastmcp import FastMCP
import httpx

mcp = FastMCP("天气查询")

@mcp.tool()
async def get_weather(city: str) -> str:
    """
    查询指定城市的实时天气
    
    参数:
        city: 城市名称，比如 "北京"、"上海"
    """
    try:
        url = f"https://wttr.in/{city}?format=%C|%t|%h|%w&lang=zh"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            parts = resp.text.split("|")
            return f"""
🌍 {city} 实时天气
━━━━━━━━━━━━━
☁️  天气：{parts[0] if len(parts)>0 else "未知"}
🌡️  温度：{parts[1] if len(parts)>1 else "未知"}
💧  湿度：{parts[2] if len(parts)>2 else "未知"}%
🌬️  风速：{parts[3] if len(parts)>3 else "未知"}
━━━━━━━━━━━━━"""
    except Exception as e:
        return f"❌ 查询失败：{e}"

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
