# 💰 AccountantAgent

A personal finance optimization tool powered by AI that helps individuals track, analyze, and improve their financial habits through intelligent insights and actionable recommendations.

Built with [Strands Agents SDK](https://github.com/strands-agents/sdk-python) and a local [Ollama](https://ollama.com/) LLM.

---

## ✨ Features

- **Expense & Income Tracking** — Log transactions via natural language in English or Spanish
- **Automatic Categorization** — AI-powered categorizer determines category and type (Income/Outcome)
- **Persistent Storage** — All transactions stored in PostgreSQL
- **Conversational Interface** — Interactive CLI chat with an AI agent
- **Two-Step Workflow** — Every transaction is categorized then inserted automatically

## 🏗️ Architecture

```
AccountantAgent/
├── main.py                  # Entry point — agent setup & interactive loop
├── AGENT.md                 # Agent system prompt & personality
├── instructions/
│   ├── instructions.input.md    # Input parsing & workflow rules
│   └── instructions.output.md   # Response formatting rules
├── tools/
│   ├── categorizer.py       # Transaction categorization tool
│   └── db.py                # Database insert/query tools
├── db/
│   ├── db.py                # PostgreSQL connection manager
│   ├── tables/              # Table definitions (Transaction, User)
│   └── queries/             # SQL query builders
├── docker-compose.yml       # PostgreSQL + pgAdmin services
├── pgadmin/
│   └── servers.json         # Auto-register DB in pgAdmin
├── .env                     # Environment variables (git-ignored)
├── .env.example             # Template for environment variables
└── pyproject.toml           # Project metadata & dependencies
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Framework | [Strands Agents SDK](https://github.com/strands-agents/sdk-python) |
| LLM | [Ollama](https://ollama.com/) — LLaMA 3.1 (local) |
| Database | PostgreSQL 17 |
| DB Manager | pgAdmin 4 |
| Language | Python 3.14+ |
| Containers | Docker Compose |

## 🚀 Getting Started

### Prerequisites

- [Python 3.14+](https://www.python.org/)
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Ollama](https://ollama.com/) with `llama3.1:latest` pulled

### 1. Clone & Setup

```bash
git clone https://github.com/your-username/AccountantAgent.git
cd AccountantAgent
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your preferred credentials
```

### 3. Start Database Services

```bash
docker compose up -d
```

This starts:
- **PostgreSQL** on `localhost:5432`
- **pgAdmin** on [http://localhost:5050](http://localhost:5050)

### 4. Install Dependencies

```bash
pip install strands-agents strands-agents-tools psycopg2-binary python-dotenv
```

### 5. Start Ollama

```bash
ollama pull llama3.1:latest
ollama serve
```

### 6. Run the Agent

```bash
python main.py
```

### Usage

```
you: gasté 300 dólares en comida hoy
Tool #1: categorizer
Tool #2: insert_outcome
✅ Transaction saved — Food, $300.00, 2026-02-13

you: recibí mi salario de 50000 pesos el 1 de febrero
Tool #1: categorizer
Tool #2: insert_income
✅ Transaction saved — Salary, $50000.00, 2026-02-01

you: exit
```

## 🔮 Future Roadmap

### Short-Term
- [ ] **Monthly Reports** — Generate summaries of income vs expenses by category
- [ ] **Budget Alerts** — Notify when spending exceeds defined thresholds per category
- [ ] **Multi-User Support** — Authenticate users and scope data per account
- [ ] **Query Tools** — Ask questions like "how much did I spend on food this month?"

### Mid-Term
- [ ] **Recurring Transactions** — Automatically log subscriptions, rent, and salary
- [ ] **Financial Goals** — Set savings targets and track progress
- [ ] **Data Visualization** — Charts and graphs for spending trends (web UI)
- [ ] **CSV/Bank Import** — Bulk import transactions from bank exports

### Long-Term
- [ ] **Predictive Analytics** — Forecast future spending based on historical patterns
- [ ] **Smart Recommendations** — Personalized cost-cutting suggestions
- [ ] **Multi-Currency Support** — Handle transactions in different currencies with conversion
- [ ] **Web/Mobile Interface** — Move beyond CLI to a full web or mobile app
- [ ] **Cloud LLM Support** — Option to use cloud-hosted models (OpenAI, Anthropic, Bedrock)

## 📄 License

This project is for personal use and learning purposes.

---

> Built with ❤️ by [@njmercado](https://github.com/njmercado)