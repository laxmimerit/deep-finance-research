# Deep Research Environment Setup

Complete setup for LangGraph Deep Research.

## Prerequisites

Ubuntu/Linux, 8GB RAM, 10GB disk space

## 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
cd ~
```

## 2. Install Anaconda

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
bash Anaconda3-2024.10-1-Linux-x86_64.sh
source ~/.bashrc
conda config --set auto_activate_base false
```

## 3. Install Python Tools

### 3.1 Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

### 3.2 Install LangGraph CLI
```bash
pip install -U langgraph-cli langgraph-api
# Or with in-memory server
pip install -U "langgraph-cli[inmem]"
```

### 3.3 Upgrade typing_extensions
```bash
pip install --upgrade typing_extensions
```

## 4. Install Node.js

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 20
npm install -g yarn
```

## 5. Set Up API Keys

Get keys from:
- Anthropic: https://console.anthropic.com/
- Google: https://makersuite.google.com/app/apikey
- LangSmith: https://smith.langchain.com/

Create `.env` file in project root with your keys:

```bash
# LangSmith API Key (recommended for tracing)
# Get your key at: https://smith.langchain.com/
LANGSMITH_API_KEY="lsv2_your-key-here"
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_PROJECT="multi-agent-research"

# Google API Key (optional)
GOOGLE_API_KEY="your-google-key-here"

# Ollama API Key (optional, for local models)
OLLAMA_API_KEY="your-ollama-key-here"

# Weather API Key (optional)
WEATHER_API_KEY="your-weather-key-here"

# Qdrant API Key (optional)
QDRANT_API_KEY="your-qdrant-key-here"
```

## 6. Clone & Run Project

```bash
git clone https://github.com/laxmimerit/deep-finance-research.git
cd deep-finance-research
uv sync
langgraph dev
```

## 7. Set Up UI (New Terminal)

```bash
git clone https://github.com/langchain-ai/deep-agents-ui.git
cd deep-agents-ui
yarn install
yarn dev
```

Open http://localhost:3000

## Quick Start (After Setup)

Terminal 1:
```bash
cd ~/deep-finance-research
langgraph dev
```

Terminal 2:
```bash
cd ~/deep-agents-ui
yarn dev
```