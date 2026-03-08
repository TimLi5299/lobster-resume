# Long-Term Memory

## Preferences

### Search
- **Default search tool:** searxng skill (privacy-respecting local metasearch)
- When any web search is needed, prioritize the searxng skill over web_search (Brave API)
- SearXNG instance: configured via `SEARXNG_URL` env var (default: `http://localhost:8080`)

## Notes

- Memory file created: 2026-02-28
- User prefers privacy-focused search tools

## Feishu Integration

- **No webhook needed** - OpenClaw has built-in Feishu integration via `message` tool
- Use `message send --channel feishu` for direct messaging
- Don't create webhook configs or curl-based sending
