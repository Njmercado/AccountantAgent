# Input Instructions

These rules govern how the agent processes and interprets user input.

## Transaction Detection
- When a user describes a financial transaction (income or expense), trigger the **two-step transaction workflow**.
- A transaction message typically contains:
  - A **description** of what happened (e.g., "compré zapatos", "received my salary")
  - An **amount** (e.g., "5000 dólares", "$300")
  - A **date** (e.g., "hoy", "ayer", "2026-02-10") — this may be implicit or explicit

## Two-Step Transaction Workflow

### Step 1 — Categorize
- Call the `categorizer` tool with the full transaction description.
- The categorizer determines the **category** (e.g., Food, Shopping, Salary) and **type** (Income or Outcome).

### Step 2 — Insert
- Immediately after categorization, call the appropriate insert tool:
  - If type is **Income** → call `insert_income`
  - If type is **Outcome** → call `insert_outcome`
- Pass all required fields: `category`, `amount`, `date`.

### Critical Rules
- **NEVER stop after Step 1.** Both steps must always be completed for every transaction.
- If the user has **not provided all required fields** (amount or date), ask the user for the missing information **before** calling the insert tool.
- Do not guess or invent missing data — always ask the user.

## Input Parsing
- Extract the **amount** from the user's message, removing currency symbols and words (e.g., "5000 dólares" → `5000.00`).
- Extract the **date** from the user's message and convert it to `YYYY-MM-DD` format.
  - `"hoy"` / `"today"` → current date
  - `"ayer"` / `"yesterday"` → current date minus one day
  - Explicit dates should be parsed as provided
- Extract the **description** as the full context of what the user said about the transaction.

## Non-Transaction Queries
- If the user is asking a general question (e.g., "how much did I spend this month?"), do **not** trigger the transaction workflow.
- Use the appropriate query tools or provide guidance based on available data.
- If no relevant tool exists for the query, respond with helpful financial advice based on the context.
