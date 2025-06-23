
<!-- README.md is generated from README.Rmd. Please edit that file -->

# EAISI - agentic-ai

<!-- badges: start -->

<!-- badges: end -->

## Resources

- [A Visual Guide to LLM
  Agents](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-llm-agents)
- [Why MCP really is a big deal \| Model Context Protocol with Tim
  Berglund](https://youtu.be/FLpS7OfD5-s?si=yEtR8H-eLfKPZ6YG)
- [MPC](https://modelcontextprotocol.io/introduction)

The goal of agentic-ai is to prepare for a small hackaton…

## Setup

This setup uses R & Python in the same Quarto document with virtual
environments. The virtual environments are setup with:

- R: renv
- Python: venv (using uv)

For sharing data between R and Python we use the `reticulate` package.

# Test your server directly

uv run mcp dev dev_assistant.py
