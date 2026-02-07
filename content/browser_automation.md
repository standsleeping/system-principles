---
id: BROWSER_AUTOMATION
title: "Claude Code Browser Automation."
essence: "MCP turns browser testing from writing scripts into an interactive conversation where results can be observed and adapted to."
---

Use Playwright MCP to give Claude Code direct control over a browser window. This enables interactive testing, responsive layout verification, and visual debugging without leaving the conversation.

**Setup**: Install with `claude mcp add playwright npx '@playwright/mcp@latest'`. Restart Claude Code after installation.

**Usage**: Direct Claude Code with natural language: "Use playwright mcp to open a browser to localhost:8000", "Resize the viewport to 600px wide", "Take a screenshot", "Click the Settings tab".

**Capabilities**: Navigation (open URLs, go back/forward, reload), viewport (resize, emulate devices), interaction (click, type, scroll, hover), inspection (screenshots, read content), forms (fill, select, submit), waiting (wait for elements, network idle).

**Responsive testing workflow**: Open the page, test wide layout (1200px), test narrow layout (400px), verify interactions, check navigation.

MCP turns browser testing from "write a script and run it" into an interactive conversation where Claude can observe results and adapt.