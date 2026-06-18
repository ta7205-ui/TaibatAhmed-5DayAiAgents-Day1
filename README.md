# Mach Natural Resources Investor Intelligence Center

A premium, modern dark-themed web application that compiles and tracks investor intelligence, financial metrics, business structure, competitive advantages, risk factors, and news updates for **Mach Natural Resources (NYSE: MNR)**. 

This project was built using Python Flask, vanilla HTML5, CSS3, and JavaScript as part of Day 1 of the **5-Day AI Agents Challenge**.

## 🚀 Key Features

* **Financial Metrics**: Dynamic tracking of FY 2025 performance ($1.175B Revenue, $593M Adjusted EBITDA, +109% YoY Proved Reserves Growth) and Q1 2026 operational statistics.
* **Business Model Breakdown**: Detailed summary of MNR's Master Limited Partnership (MLP) structure, focus on Proved Developed Producing (PDP) low-decline assets, and capital distribution logic.
* **Strategic Strengths & Risks**: Transparent breakdown of competitive market dynamics vs. industry exposure (price volatility, depletion, dilution).
* **News & Activity Feed**: Real-time aggregation of updates related to Mach, upstream oil trends, insider trade activities (CEO Tom L. Ward), and major investors like Kayne Anderson and Bayou City Energy.
* **Interactive Refresh**: Dynamic async refresh action with CSS loaders and transition effects.

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Frontend**: HTML5, Vanilla CSS3 (Custom Grid Layouts & HSL styling), JavaScript (Fetch API)
* **Data Store**: Local structured JSON database (`mach_data.json`)

## 📦 Getting Started

### Prerequisites

* Python 3.8 or higher installed on your system.

### Installation & Run

1. Clone the repository:
   ```bash
   git clone https://github.com/ta7205-ui/TaibatAhmed-5DayAiAgents-Day1.git
   cd TaibatAhmed-5DayAiAgents-Day1
   ```

2. Install dependencies:
   ```bash
   pip install flask
   ```

3. Run the development server:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## 📂 Project Structure

```
├── app.py              # Flask server and UI layout
├── mach_data.json      # Structured investor intelligence data
├── .gitignore          # Git exclusion rules
└── README.md           # This document
```
