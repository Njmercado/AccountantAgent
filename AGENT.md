# AccountantAgent

## Overview
AccountantAgent is a personal finance optimization tool designed to help individuals track, analyze, and improve their financial habits through intelligent insights and actionable recommendations.

## Features

### 📊 Expense Tracking
- Monitor monthly income and expenses
- Categorize spending by topics (food, transportation, entertainment, etc.)
- Real-time financial data analysis

### 🎯 Financial Optimization
- Identify spending patterns and trends
- Suggest budget optimizations
- Highlight areas for potential savings

### 📈 Smart Insights
- Generate detailed financial reports
- Provide personalized recommendations
- Track progress toward financial goals

### ⚡ Actionable Intelligence
- Automated expense categorization
- Budget alerts and notifications
- Responsible financial action plans

## Use Cases
- **Budget Management**: Track where your money goes each month
- **Expense Analysis**: Understand spending patterns across categories
- **Financial Planning**: Set and achieve savings goals
- **Cost Reduction**: Identify opportunities to cut unnecessary expenses
- **Financial Health**: Build better money management habits

## Getting Started
1. Connect your financial accounts
2. Set up expense categories
3. Define your financial goals
4. Review monthly reports and recommendations
5. Take action on suggested improvements

## Goals
Help users take control of their finances through data-driven insights and practical recommendations for improved financial well-being.

## Instructions:
When a user describes a financial transaction (income or expense), you MUST follow this exact two-step workflow:

1. **Step 1 — Categorize**: Call the `categorizer` tool with the transaction description to determine the category and type (Income or Outcome).
2. **Step 2 — Insert**: Immediately after categorization, call `insert_income` (if type is Income) or `insert_outcome` (if type is Outcome) with all the required data (description, amount, date). If the user has not provided all required fields (amount, date), ask the user for the missing information before calling the insert tool.

NEVER stop after Step 1. You must ALWAYS complete both steps for every transaction.