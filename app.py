import os
import json
import time
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mach_data.json')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mach Natural Resources (MNR) Investor Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --border-color: #30363d;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --accent-color: #58a6ff;
            --accent-gradient: linear-gradient(135deg, #58a6ff 0%, #bc8cff 100%);
            --accent-success: #3fb950;
            --accent-error: #f85149;
            --accent-warn: #d29922;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
            line-height: 1.6;
            padding: 2rem 1rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 2.5rem;
        }

        .header-title h1 {
            font-size: 2.2rem;
            font-weight: 700;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-title p {
            color: var(--text-secondary);
            margin-top: 0.2rem;
            font-size: 0.95rem;
        }

        .btn-refresh {
            background: rgba(88, 166, 255, 0.1);
            border: 1px solid var(--accent-color);
            color: var(--accent-color);
            padding: 0.6rem 1.2rem;
            border-radius: 50px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
        }

        .btn-refresh:hover {
            background: var(--accent-color);
            color: var(--bg-color);
            box-shadow: 0 0 15px rgba(88, 166, 255, 0.4);
            transform: translateY(-2px);
        }

        .spinner {
            width: 16px;
            height: 16px;
            border: 2px solid currentColor;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            display: none;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.8rem;
        }

        @media (min-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 2fr 1fr;
            }
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            border-color: #484f58;
        }

        .card-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            border-bottom: 1px solid rgba(240, 246, 250, 0.08);
            padding-bottom: 0.6rem;
            color: #ffffff;
        }

        .metrics-subgrid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .metric-item {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }

        .metric-label {
            color: var(--text-secondary);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.3rem;
        }

        .metric-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: #ffffff;
        }

        .metric-value.highlight {
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .section-subtitle {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 1.2rem;
            margin-bottom: 0.6rem;
        }

        ul, ol {
            padding-left: 1.2rem;
        }

        li {
            margin-bottom: 0.8rem;
            color: var(--text-primary);
        }

        .list-item-title {
            font-weight: 600;
            color: #ffffff;
        }

        .badge {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            font-size: 0.75rem;
            font-weight: 600;
            border-radius: 50px;
            margin-right: 0.5rem;
        }

        .badge-info { background: rgba(88, 166, 255, 0.15); color: var(--accent-color); border: 1px solid rgba(88, 166, 255, 0.3); }
        .badge-success { background: rgba(63, 185, 80, 0.15); color: var(--accent-success); border: 1px solid rgba(63, 185, 80, 0.3); }
        .badge-error { background: rgba(248, 81, 73, 0.15); color: var(--accent-error); border: 1px solid rgba(248, 81, 73, 0.3); }
        .badge-warn { background: rgba(210, 153, 34, 0.15); color: var(--accent-warn); border: 1px solid rgba(210, 153, 34, 0.3); }

        .news-feed {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .news-item {
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 8px;
            padding: 1rem;
            transition: background 0.2s ease;
        }

        .news-item:hover {
            background: rgba(255, 255, 255, 0.03);
        }

        .news-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .news-title {
            font-weight: 600;
            color: #ffffff;
            margin-top: 0.3rem;
            margin-bottom: 0.3rem;
            font-size: 1rem;
        }

        .news-summary {
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .news-date {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        .ref-links {
            margin-top: 2rem;
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-align: center;
            border-top: 1px solid var(--border-color);
            padding-top: 1.5rem;
        }

        .ref-links a {
            color: var(--accent-color);
            text-decoration: none;
            margin: 0 0.5rem;
        }

        .ref-links a:hover {
            text-decoration: underline;
        }
        .btn-export {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.75rem;
            padding: 0.3rem 0.7rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: inherit;
        }

        .btn-export:hover {
            background: rgba(88, 166, 255, 0.15);
            border-color: var(--accent-color);
            color: var(--accent-color);
        }

        .card-header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(240, 246, 250, 0.08);
            padding-bottom: 0.6rem;
            margin-bottom: 1.2rem;
        }

        .card-header-container .card-title {
            margin-bottom: 0;
            border-bottom: none;
            padding-bottom: 0;
        }
    </style>
</head>
<body>
    <header>
        <div class="header-title">
            <h1>Mach Natural Resources</h1>
            <p>Investor Presentation & 10-K Intelligence Center</p>
        </div>
        <button class="btn-refresh" id="refreshBtn" onclick="refreshDashboard()">
            <span class="spinner" id="spinner"></span>
            <span id="btnText">Refresh Data</span>
        </button>
    </header>

    <div class="dashboard-grid">
        <!-- Main Content Column -->
        <div style="display: flex; flex-direction: column; gap: 1.8rem;">
            <!-- Financial Metrics -->
            <div class="card" id="card-financials">
                <div class="card-header-container">
                    <h2 class="card-title">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                        Key Financial & Operational Metrics
                    </h2>
                </div>
                
                <h3 class="section-subtitle">Fiscal Year 2025 (10-K Annual Report)</h3>
                <div class="metrics-subgrid">
                    <div class="metric-item">
                        <div class="metric-label">Total Revenue</div>
                        <div class="metric-value">{{ data.financial_metrics.fiscal_year_2025.total_revenue }}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Adjusted EBITDA</div>
                        <div class="metric-value">{{ data.financial_metrics.fiscal_year_2025.adjusted_ebitda }}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Net Income</div>
                        <div class="metric-value">{{ data.financial_metrics.fiscal_year_2025.net_income }}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Reserves Growth</div>
                        <div class="metric-value highlight">{{ data.financial_metrics.fiscal_year_2025.proved_reserves_growth }}</div>
                    </div>
                </div>

                <h3 class="section-subtitle">Q1 2026 Financial Results</h3>
                <div class="metrics-subgrid">
                    <div class="metric-item">
                        <div class="metric-label">Q1 Revenue</div>
                        <div class="metric-value">{{ data.financial_metrics.first_quarter_2026.total_revenue }}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Adjusted EBITDA</div>
                        <div class="metric-value">{{ data.financial_metrics.first_quarter_2026.adjusted_ebitda }}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Avg Production</div>
                        <div class="metric-value" style="font-size: 1.1rem; padding-top: 0.3rem;">{{ data.financial_metrics.first_quarter_2026.average_production.split(' (')[0] }}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">LOE per Boe</div>
                        <div class="metric-value">{{ data.financial_metrics.first_quarter_2026.lease_operating_expense }}</div>
                    </div>
                </div>
            </div>

            <!-- Business Structure & Model -->
            <div class="card" id="card-structure">
                <div class="card-header-container">
                    <h2 class="card-title">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
                        Business Structure & Value Creation
                    </h2>
                </div>
                <p style="color: var(--text-secondary); margin-bottom: 1rem;">{{ data.business_structure.description }}</p>
                <h3 class="section-subtitle">How MNR Generates Revenue & Distributions:</h3>
                <ol>
                    {% for item in data.business_structure.how_they_make_money %}
                    <li>
                        <span class="list-item-title">{{ item.split(':')[0] }}:</span>
                        {{ item.split(':')[1] }}
                    </li>
                    {% endfor %}
                </ol>
            </div>

            <!-- Competitive Advantages -->
            <div class="card" id="card-advantages">
                <div class="card-header-container">
                    <h2 class="card-title">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                        Strategic & Competitive Advantages
                    </h2>
                </div>
                <ul>
                    {% for adv in data.advantages %}
                    <li>
                        <span class="list-item-title">{{ adv.split(':')[0] }}:</span>
                        {{ adv.split(':')[1] }}
                    </li>
                    {% endfor %}
                </ul>
            </div>

            <!-- Risk Factors -->
            <div class="card" id="card-risks">
                <div class="card-header-container">
                    <h2 class="card-title" style="color: #ff7b72;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                        Current Risk Factors
                    </h2>
                </div>
                <ul>
                    {% for risk in data.risks %}
                    <li>
                        <span class="list-item-title" style="color: #ff7b72;">{{ risk.split(':')[0] }}:</span>
                        {{ risk.split(':')[1] }}
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>

        <!-- Sidebar / News & Investor Updates -->
        <div>
            <div class="card" id="card-news" style="height: 100%;">
                <div class="card-header-container">
                    <h2 class="card-title">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v11"></path><path d="M12 12H5"></path><path d="M16 6v12"></path><path d="M12 8H5"></path></svg>
                        News & Activity Feed
                    </h2>
                </div>
                <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.9rem;">
                    Tracking Mach updates, upstream oil sector, and investor activity.
                </p>

                <div class="news-feed" id="newsFeed">
                    {% for news in data.news_and_activity %}
                    <div class="news-item">
                        <div class="news-header">
                            {% if news.category == 'Mach Natural Resources' %}
                            <span class="badge badge-info">{{ news.category }}</span>
                            {% elif news.category == 'Major Investors' or news.category == 'Insider Activity' %}
                            <span class="badge badge-success">{{ news.category }}</span>
                            {% else %}
                            <span class="badge badge-warn">{{ news.category }}</span>
                            {% endif %}
                            <span class="news-date">{{ news.date }}</span>
                        </div>
                        <h4 class="news-title">{{ news.title }}</h4>
                        <p class="news-summary">{{ news.summary }}</p>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <footer class="ref-links">
        <p>Source Materials & Reference Documents:</p>
        <div style="margin-top: 0.5rem;">
            <a href="https://d1io3yog0oux5.cloudfront.net/_4d209f0ad0d74e314edc8373d6535e3a/machresources/db/2407/23328/pdf/060126+-+MNR+June+2026+Investor+Presentation.pdf" target="_blank">June 2026 Investor Presentation (PDF)</a> |
            <a href="https://www.sec.gov/edgar/searchedgar/companysearch" target="_blank">SEC EDGAR (10-K Filings)</a>
        </div>
    </footer>

    <script>
        function refreshDashboard() {
            const spinner = document.getElementById('spinner');
            const btnText = document.getElementById('btnText');
            const refreshBtn = document.getElementById('refreshBtn');

            // Show spinner and disable button
            spinner.style.display = 'inline-block';
            btnText.textContent = 'Updating...';
            refreshBtn.disabled = true;

            // Simple api fetch simulation to refresh content or trigger python reload
            fetch('/api/refresh')
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        // Reload window to show freshly-loaded templates/data
                        window.location.reload();
                    }, 1200); // 1.2s delay for delightful spinner interaction
                })
                .catch(error => {
                    console.error('Error refreshing:', error);
                    spinner.style.display = 'none';
                    btnText.textContent = 'Refresh Data';
                    refreshBtn.disabled = false;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    data = load_data()
    return render_template_string(HTML_TEMPLATE, data=data)

@app.route('/api/refresh')
def refresh():
    # Simulate data fetching and reload from file (or you can perform live requests here)
    time.sleep(0.5)
    return jsonify({"status": "success", "message": "Data reloaded successfully"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
