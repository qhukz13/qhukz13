<div align="center">

# Hey, I'm qhukz 👋

**I build local-first AI developer tooling — agent orchestration, RAG, and the guardrails that keep autonomous agents honest.**

In parallel, I'm working through the ML underneath it all from first principles: math on paper, models from scratch, no skipped steps.

📍 Ukraine

</div>

---

## 🔭 What I'm building now

### [Asterim](https://github.com/qhukz13/Asterim) — an AI-native workspace for autonomous coding agents

A local-first control plane that brings multi-agent orchestration directly into your development environment — with humans firmly in the loop.

- Coordinate specialized coding agents (Claude Code, Antigravity, …) on complex engineering tasks through adapters and an internal event bus
- Local-first by design: code and data stay on your machine; external resources connect through a dedicated cloud relay
- Human approvals gate autonomous actions — nothing executes without your say-so
- Real-time dashboard to monitor agents, read logs, and intervene at any moment

`TypeScript` · `React` · `Fastify` · `pnpm + Turborepo monorepo` · `Docker` · `GitHub Actions`

### ORACLE — a local-first personal AI agent that never gets unsupervised root <sub>🔒 private while it grows</sub>

Not "a chatbot with shell access" — a small orchestrator that understands intent, routes work to the cheapest competent executor, and reports back, while every side effect passes through a policy layer that can refuse.

```
you ─▶ ORACLE ─▶ intent ─▶ route ─┬─▶ local tools        (fast, free, guarded)
                                  ├─▶ project knowledge  (hybrid RAG)
                                  └─▶ delegated agents   (deep code reasoning)
```

- A deliberately small local router model (0.8B via Ollama) — 93% intent accuracy on the eval set; heavy reasoning is delegated to agents that are good at it
- Three processes, three trust levels: the model emits tool *requests*, a policy engine decides, an isolated low-privilege tool host executes
- Hybrid RAG over code and docs: syntax-aware chunking with tree-sitter (18 grammars), ONNX embeddings on CPU, `sqlite-vec` search, watch-based incremental indexing, PDF extraction
- Event-sourced runtime — any session can be replayed, audited, and tested deterministically
- 370 Python + 77 TypeScript tests, `mypy --strict`, and a security suite that acts as a merge gate
- Built against real constraints: designed to run next to a 4 GB VRAM GPU

`Python 3.12` · `FastAPI` · `Tauri` · `SQLite` · `Ollama` · `ONNX Runtime` · `tree-sitter`

### [asterim-pipeline](https://github.com/qhukz13/asterim-pipeline) — CI/CD for coding agents

A zero-runtime-dependency Node.js pipeline runner that coordinates three agents — orchestrator → coder → tester — using repository files as the communication protocol.

- A state machine with human gates: phase completions, failures, and "done" claims without an actual commit all stop the loop for review
- Distributed mode: the PC orchestrates while a laptop executes over LAN — heartbeats, at-least-once delivery, idempotent dispatch, git as the sync layer
- Live dashboard streaming structured agent output (tool calls, turns, cost) in real time
- Safety first: never force-pushes, never runs destructive git commands, never executes anything found in repository markdown

`Node.js` · `zero dependencies` · `state machine` · `file-based protocol`

---

## 🧠 What I'm learning

I keep a structured AI/ML curriculum (an Obsidian vault + Jupyter notebooks) and move through it stage by stage — while the projects above let me build ahead of it.

- **Right now:** foundations done properly — linear algebra, NumPy, statistics — worked through in notebooks, not skimmed
- **Daily practice through building:** transformers & LLMs — attention, tokenization, embeddings, RAG & vector search, AI agents, prompt engineering, LLM evaluation, fine-tuning & RLHF
- **Next up:** PyTorch, from-scratch checkpoints (linear & logistic regression → a neural network → self-attention → a small GPT → a RAG app), then MLOps

## 🛠 Toolbox

**Languages & runtimes**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Node.js](https://img.shields.io/badge/Node.js-5FA04E?style=flat-square&logo=nodedotjs&logoColor=white)

**Building with**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Fastify](https://img.shields.io/badge/Fastify-000000?style=flat-square&logo=fastify&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Tauri](https://img.shields.io/badge/Tauri-24C8D8?style=flat-square&logo=tauri&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![pnpm](https://img.shields.io/badge/pnpm-F69220?style=flat-square&logo=pnpm&logoColor=white)
![Turborepo](https://img.shields.io/badge/Turborepo-EF4444?style=flat-square&logo=turborepo&logoColor=white)

**AI / ML**

![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white)
![ONNX](https://img.shields.io/badge/ONNX_Runtime-005CED?style=flat-square&logo=onnx&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-learning-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Obsidian](https://img.shields.io/badge/Obsidian-7C3AED?style=flat-square&logo=obsidian&logoColor=white)

## 📐 How I build

Design-first — architecture docs and ADRs lead the code · humans stay in the loop · untrusted content is data, never instructions · tests and security suites are merge gates, not suggestions

## 📊 GitHub

<div align="center">
  <img height="165" src="https://github-readme-stats.vercel.app/api?username=qhukz13&show_icons=true&hide_border=true&theme=transparent&rank_icon=github" alt="qhukz13's GitHub stats" />
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=qhukz13&layout=compact&hide_border=true&theme=transparent&langs_count=8&exclude_repo=SCRAPSHIFT" alt="Top languages" />
</div>

---

<div align="center">

📫 Reach me: [v.onashchuk@gmail.com](mailto:v.onashchuk@gmail.com)

</div>
