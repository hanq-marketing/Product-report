import csv
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, "data", "bao_cao_cac_tai_khoan_10_2026.csv")
html_path = os.path.join(base_dir, "dashboard_tru_cot_1_ngan_sach.html")

print("Đọc dữ liệu từ CSV cho Dashboard Ngân Sách 2026...")
rows = []
with open(csv_path, mode="r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for r in reader:
        row_dict = dict(r)
        for num_field in ["Chi tiêu", "CTR (%)", "CPC", "CPM", "CPA"]:
            try:
                row_dict[num_field] = float(row_dict.get(num_field, 0))
            except Exception:
                row_dict[num_field] = 0.0
        for int_field in ["Hiển thị", "Click link", "Tin nhắn", "Lead", "Đăng ký", "Sđt theo campain"]:
            try:
                row_dict[int_field] = int(float(row_dict.get(int_field, 0)))
            except Exception:
                row_dict[int_field] = 0
        rows.append(row_dict)

print(f"-> Đã đọc {len(rows)} dòng dữ liệu.")
json_data_str = json.dumps(rows, ensure_ascii=False)

html_content = """<!DOCTYPE html>
<html lang="vi" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Quản Trị Chi Tiêu Quảng Cáo Năm 2026 Theo Đầu Sản Phẩm</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
    <style>
        :root {
            --bg-base: #070b14;
            --bg-surface: rgba(15, 23, 42, 0.85);
            --bg-surface-solid: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.65);
            --border-color: rgba(255, 255, 255, 0.09);
            --border-hover: rgba(99, 102, 241, 0.45);

            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;

            --primary: #6366f1;
            --primary-light: rgba(99, 102, 241, 0.16);
            --success: #10b981;
            --success-light: rgba(16, 185, 129, 0.16);
            --warning: #f59e0b;
            --warning-light: rgba(245, 158, 11, 0.16);
            --danger: #ef4444;
            --danger-light: rgba(239, 68, 68, 0.16);
            --cyan: #06b6d4;
            --purple: #a855f7;

            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-full: 9999px;
            --shadow-card: 0 8px 28px -4px rgba(0, 0, 0, 0.45);
        }

        [data-theme="light"] {
            --bg-base: #f1f5f9;
            --bg-surface: rgba(255, 255, 255, 0.94);
            --bg-surface-solid: #ffffff;
            --bg-card: #f8fafc;
            --border-color: rgba(15, 23, 42, 0.1);
            --border-hover: rgba(79, 70, 229, 0.45);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --primary: #4f46e5;
            --shadow-card: 0 4px 16px rgba(0, 0, 0, 0.06);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-base);
            background-image:
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.14) 0px, transparent 45%),
                radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.10) 0px, transparent 45%);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.5;
            padding-bottom: 3rem;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 1.25rem 1.5rem;
        }

        /* ─── HEADER ─── */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            padding: 1.1rem 1.4rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-card);
            margin-bottom: 1.35rem;
        }

        .brand-box {
            display: flex;
            align-items: center;
            gap: 0.95rem;
        }

        .brand-icon {
            width: 46px;
            height: 46px;
            border-radius: 13px;
            background: linear-gradient(135deg, #6366f1 0%, #10b981 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.45rem;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
        }

        .brand-title h1 {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .brand-title p {
            font-size: 0.82rem;
            color: var(--text-secondary);
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            flex-wrap: wrap;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.5rem 0.95rem;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-color);
            background: var(--bg-card);
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.82rem;
            font-weight: 700;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s;
        }

        .btn:hover {
            border-color: var(--primary);
            transform: translateY(-1px);
        }

        .btn-primary {
            background: var(--primary);
            border-color: var(--primary);
            color: #fff;
        }

        /* ─── SECTION BLOCK ─── */
        .section-block {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.35rem 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow-card);
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 1rem;
            padding-bottom: 1rem;
            margin-bottom: 1.15rem;
            border-bottom: 1px solid var(--border-color);
        }

        .section-tag {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.2rem 0.65rem;
            border-radius: var(--radius-full);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background: var(--primary-light);
            color: #818cf8;
            border: 1px solid rgba(99, 102, 241, 0.35);
            margin-bottom: 0.35rem;
        }

        .section-title {
            font-size: 1.18rem;
            font-weight: 800;
            color: var(--text-primary);
        }

        .section-desc {
            font-size: 0.82rem;
            color: var(--text-secondary);
            margin-top: 0.15rem;
        }

        /* ─── FILTER ROW IN SECTION 1 ─── */
        .filter-panel {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1rem 1.15rem;
            margin-bottom: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.9rem;
        }

        .filter-controls-grid {
            display: flex;
            align-items: flex-end;
            gap: 0.9rem;
            flex-wrap: wrap;
        }

        .filter-item {
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            flex: 1;
            min-width: 190px;
        }

        .filter-label {
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: var(--text-secondary);
        }

        .select-input {
            width: 100%;
            height: 40px;
            padding: 0 0.75rem;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-color);
            background: var(--bg-surface-solid);
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.84rem;
            font-weight: 600;
        }

        /* Product Quick Pills */
        .product-pills-wrap {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            flex-wrap: wrap;
            padding-top: 0.65rem;
            border-top: 1px solid var(--border-color);
        }

        .prod-pill {
            padding: 0.34rem 0.78rem;
            border-radius: var(--radius-full);
            border: 1px solid var(--border-color);
            background: var(--bg-surface-solid);
            color: var(--text-secondary);
            font-size: 0.76rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.18s;
        }

        .prod-pill:hover {
            border-color: var(--primary);
            color: var(--text-primary);
        }

        .prod-pill.active {
            background: var(--primary);
            border-color: var(--primary);
            color: #fff;
            box-shadow: 0 2px 10px rgba(99, 102, 241, 0.35);
        }

        /* ─── KPI CARDS (SECTION 1) ─── */
        .kpi-grid-4 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1rem;
            margin-bottom: 1.35rem;
        }

        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-top: 4px solid var(--accent, var(--primary));
            border-radius: var(--radius-md);
            padding: 1.1rem 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        .kpi-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-secondary);
        }

        .kpi-main-val {
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }

        .kpi-meta {
            font-size: 0.78rem;
            color: var(--text-secondary);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.35rem;
            padding-top: 0.35rem;
            border-top: 1px solid var(--border-color);
        }

        /* ─── TABLE STYLING ─── */
        .table-wrap {
            overflow-x: auto;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.83rem;
            text-align: left;
            white-space: nowrap;
        }

        th {
            background: var(--bg-surface-solid);
            padding: 0.82rem 0.95rem;
            font-weight: 700;
            color: var(--text-secondary);
            border-bottom: 2px solid var(--border-color);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        td {
            padding: 0.78rem 0.95rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
            vertical-align: middle;
        }

        tr:hover td {
            background: rgba(99, 102, 241, 0.05);
        }

        tr.selected-row td {
            background: rgba(99, 102, 241, 0.14);
        }

        tr.total-row td {
            background: rgba(99, 102, 241, 0.12);
            font-weight: 800;
            border-top: 2px solid var(--primary);
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            padding: 0.2rem 0.58rem;
            border-radius: var(--radius-full);
            font-size: 0.73rem;
            font-weight: 800;
        }

        .badge-up { background: rgba(16, 185, 129, 0.16); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }
        .badge-down { background: rgba(239, 68, 68, 0.16); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.35); }
        .badge-warn { background: rgba(245, 158, 11, 0.16); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.35); }
        .badge-info { background: rgba(6, 182, 212, 0.16); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.35); }
        .badge-neutral { background: rgba(148, 163, 184, 0.14); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.28); }

        .bar-mini {
            width: 60px;
            height: 6px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 99px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-right: 6px;
        }

        .bar-mini-fill {
            height: 100%;
            border-radius: 99px;
        }

        /* ─── SECTION 2: CHARTS LAYOUT ─── */
        .charts-main-grid {
            display: grid;
            grid-template-columns: 1.55fr 1fr;
            gap: 1.25rem;
            margin-bottom: 1.25rem;
        }

        @media (max-width: 1024px) {
            .charts-main-grid {
                grid-template-columns: 1fr;
            }
        }

        .chart-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1.15rem 1.25rem;
        }

        .chart-card-head {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 0.9rem;
        }

        .chart-card-title {
            font-size: 0.98rem;
            font-weight: 800;
            color: var(--text-primary);
        }

        .chart-card-sub {
            font-size: 0.76rem;
            color: var(--text-secondary);
            margin-top: 0.15rem;
        }

        .chart-canvas-box {
            position: relative;
            height: 350px;
            width: 100%;
        }

        .mode-switch-group {
            display: inline-flex;
            background: var(--bg-surface-solid);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-sm);
            padding: 3px;
            gap: 3px;
        }

        .mode-switch-btn {
            padding: 0.3rem 0.7rem;
            border-radius: 6px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            font-family: inherit;
            font-size: 0.75rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
        }

        .mode-switch-btn.active {
            background: var(--primary);
            color: #fff;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- ─── HEADER ─── -->
        <header>
            <div class="brand-box">
                <div class="brand-icon">📊</div>
                <div class="brand-title">
                    <h1>DASHBOARD QUẢN TRỊ CHI TIÊU QUẢNG CÁO NĂM 2026 THEO ĐẦU SẢN PHẨM</h1>
                    <p>Thống kê tổng chi tiêu năm 2026 theo đầu sản phẩm, chu kỳ theo tháng & đối sánh biến thiên Tháng trước vs. Tháng hiện tại</p>
                </div>
            </div>
            <div class="header-actions">
                <span id="syncBadge" class="badge badge-up">🟢 Dữ liệu Năm 2026</span>
                <button class="btn btn-primary" onclick="syncGoogleSheet()">🔄 Đồng bộ Google Sheet</button>
                <a class="btn" href="https://hanq-marketing.github.io/daily-report/" target="_blank">📊 Mở Báo Cáo Tổng Quan (Daily Report)</a>
                <button class="btn" onclick="toggleTheme()">🌓 Giao diện</button>
            </div>
        </header>

        <!-- ═══════════════════════════════════════════════════════════════════════════
             SECTION 1: TỔNG CHI TIÊU TRONG NĂM 2026 LỌC THEO ĐẦU SẢN PHẨM, CHU KỲ THEO THÁNG
                        SO SÁNH THÁNG TRƯỚC VÀ THÁNG HIỆN TẠI
             ═══════════════════════════════════════════════════════════════════════════ -->
        <section class="section-block" id="section1">
            <div class="section-header">
                <div>
                    <span class="section-tag">📌 SECTION 1</span>
                    <div class="section-title">Tổng Chi Tiêu Trong Năm 2026 Theo Đầu Sản Phẩm & So Sánh Tháng Trước vs. Tháng Hiện Tại</div>
                    <div class="section-desc">Lọc chi tiết theo từng đầu sản phẩm, chu kỳ theo tháng trong năm 2026 và đo lường tốc độ biến thiên ngân sách giữa Tháng trước và Tháng hiện tại</div>
                </div>
                <div>
                    <button class="btn" onclick="exportSection1CSV()">📥 Xuất CSV Section 1</button>
                </div>
            </div>

            <!-- Bộ lọc Section 1 -->
            <div class="filter-panel">
                <div class="filter-controls-grid">
                    <!-- Lọc Đầu Sản Phẩm -->
                    <div class="filter-item" style="flex: 1.4;">
                        <label class="filter-label">📦 Lọc Theo Đầu Sản Phẩm</label>
                        <select id="productSelect" class="select-input" onchange="onProductSelectChange()">
                            <option value="ALL">👉 Tất cả đầu sản phẩm (Toàn hệ thống 2026)</option>
                        </select>
                    </div>

                    <!-- Chế độ nhóm Đầu Sản Phẩm -->
                    <div class="filter-item" style="flex: 1.1;">
                        <label class="filter-label">🗂️ Cách Phân Nhóm Sản Phẩm</label>
                        <select id="groupBySelect" class="select-input" onchange="initProductOptions(); renderDashboard();">
                            <option value="product" selected>Theo Đầu Sản Phẩm (Data Analyst, Embedded, AI Engineer...)</option>
                            <option value="account">Theo Tài Khoản Ads (RA10 - DABK, Ra1 - EMBEDDED...)</option>
                        </select>
                    </div>

                    <!-- Năm -->
                    <div class="filter-item" style="flex: 0.7; min-width: 130px;">
                        <label class="filter-label">📅 Năm Quản Trị</label>
                        <select id="yearSelect" class="select-input" onchange="initMonthSelectors(); renderDashboard();">
                            <option value="2026" selected>Năm 2026</option>
                        </select>
                    </div>

                    <!-- Tháng Trước -->
                    <div class="filter-item" style="flex: 1;">
                        <label class="filter-label">⏪ Chu Kỳ: Tháng Trước</label>
                        <select id="prevMonthSelect" class="select-input" onchange="renderDashboard()"></select>
                    </div>

                    <!-- Tháng Hiện Tại -->
                    <div class="filter-item" style="flex: 1;">
                        <label class="filter-label">⏩ Chu Kỳ: Tháng Hiện Tại</label>
                        <select id="currMonthSelect" class="select-input" onchange="renderDashboard()"></select>
                    </div>

                    <!-- Hình thức chạy -->
                    <div class="filter-item" style="flex: 0.9; min-width: 155px;">
                        <label class="filter-label">🎯 Hình Thức Chạy</label>
                        <select id="formatSelect" class="select-input" onchange="renderDashboard()">
                            <option value="ALL">Tất cả hình thức</option>
                            <option value="Mess">💬 Mess</option>
                            <option value="CĐ">🎯 Chuyển đổi (CĐ)</option>
                            <option value="Phễu Học Thử">🎪 Phễu Học Thử</option>
                            <option value="Branding">📢 Branding</option>
                        </select>
                    </div>
                </div>

                <!-- Thanh bấm chọn nhanh Đầu Sản Phẩm -->
                <div class="product-pills-wrap" id="productPillsBar"></div>
            </div>

            <!-- 4 Thẻ KPI Tổng Chi Tiêu 2026 & So Sánh Tháng Trước vs Tháng Hiện Tại -->
            <div class="kpi-grid-4" id="section1KpiGrid"></div>

            <!-- Bảng Tổng Chi Tiêu Năm 2026 & So Sánh Tháng Trước vs. Tháng Hiện Tại Theo Đầu Sản Phẩm -->
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Đầu Sản Phẩm</th>
                            <th>Tổng Chi Tiêu Năm 2026</th>
                            <th>Tỷ Trọng Năm 2026</th>
                            <th id="thPrevMonth">Tháng Trước (T10/2026)</th>
                            <th id="thCurrMonth">Tháng Hiện Tại (T11/2026)</th>
                            <th>Chênh Lệch (Tháng Này - Trước)</th>
                            <th>Δ% Biến Thiên Tháng</th>
                            <th>Chi Tiêu TB/Ngày (Trước ➔ Này)</th>
                            <th>Δ% Tốc Độ Chi/Ngày</th>
                            <th>SĐT Pancake (Trước ➔ Này)</th>
                            <th>CPL Giá/SĐT (Trước ➔ Này)</th>
                            <th>Đánh Giá Biến Thiên</th>
                        </tr>
                    </thead>
                    <tbody id="section1TableBody"></tbody>
                </table>
            </div>
        </section>

        <!-- ═══════════════════════════════════════════════════════════════════════════
             SECTION 2: BIỂU ĐỒ CHI TIÊU CÁC SẢN PHẨM
             ═══════════════════════════════════════════════════════════════════════════ -->
        <section class="section-block" id="section2">
            <div class="section-header">
                <div>
                    <span class="section-tag">📈 SECTION 2</span>
                    <div class="section-title">Biểu Đồ Chi Tiêu Các Sản Phẩm (Năm 2026 & So Sánh Giữa Các Tháng)</div>
                    <div class="section-desc">Trực quan hóa quy mô ngân sách, đối sánh trực diện Chi tiêu Tháng trước vs. Tháng hiện tại và cơ cấu tỷ trọng ngân sách của từng đầu sản phẩm</div>
                </div>
                <div class="mode-switch-group">
                    <button class="mode-switch-btn active" id="btnMetricSpend" onclick="setSection2Metric('spend')">💰 Xem Chi Tiêu (VNĐ)</button>
                    <button class="mode-switch-btn" id="btnMetricDaily" onclick="setSection2Metric('daily')">⚡ Xem Chi Tiêu TB/Ngày</button>
                    <button class="mode-switch-btn" id="btnMetricPhones" onclick="setSection2Metric('phones')">📱 Xem Chi Tiêu kèm SĐT</button>
                </div>
            </div>

            <!-- Hàng 1 của Section 2: Biểu đồ Cột So sánh Tháng trước vs Tháng hiện tại + Biểu đồ Tỷ trọng Năm 2026 -->
            <div class="charts-main-grid">
                <div class="chart-card">
                    <div class="chart-card-head">
                        <div>
                            <div class="chart-card-title" id="chartCompareTitle">1️⃣ Biểu Đồ So Sánh Chi Tiêu Các Sản Phẩm: Tháng Trước vs. Tháng Hiện Tại</div>
                            <div class="chart-card-sub">Bấm vào bất kỳ cột sản phẩm nào trên biểu đồ để lọc riêng sản phẩm đó</div>
                        </div>
                    </div>
                    <div class="chart-canvas-box">
                        <canvas id="chartProductMonthCompare"></canvas>
                    </div>
                </div>

                <div class="chart-card">
                    <div class="chart-card-head">
                        <div>
                            <div class="chart-card-title">2️⃣ Cơ Cấu Tỷ Trọng Chi Tiêu Năm 2026 Theo Đầu Sản Phẩm (% Share)</div>
                            <div class="chart-card-sub">Phân bổ tổng ngân sách lũy kế năm 2026 giữa các đầu sản phẩm</div>
                        </div>
                    </div>
                    <div class="chart-canvas-box">
                        <canvas id="chartProductShare2026"></canvas>
                    </div>
                </div>
            </div>

            <!-- Hàng 2 của Section 2: Biểu đồ Xu hướng Chi tiêu các sản phẩm theo Chu kỳ (Tháng / Tuần / Ngày) -->
            <div class="chart-card">
                <div class="chart-card-head">
                    <div>
                        <div class="chart-card-title" id="chartTimelineTitle">3️⃣ Biểu Đồ Diễn Biến Chi Tiêu Các Đầu Sản Phẩm Theo Thời Gian Trong Năm 2026</div>
                        <div class="chart-card-sub">Theo dõi sự tăng/giảm ngân sách của từng đầu sản phẩm qua các Tháng hoặc các Tuần trong năm 2026</div>
                    </div>
                    <div class="mode-switch-group">
                        <button class="mode-switch-btn active" id="btnTimeMonth" onclick="setTimelineGranularity('month')">🗓️ Theo Tháng</button>
                        <button class="mode-switch-btn" id="btnTimeWeek" onclick="setTimelineGranularity('week')">📅 Theo Tuần (W40➔W47)</button>
                        <button class="mode-switch-btn" id="btnTimeDay" onclick="setTimelineGranularity('day')">📆 Theo Ngày</button>
                    </div>
                </div>
                <div class="chart-canvas-box" style="height: 340px;">
                    <canvas id="chartProductTimeline"></canvas>
                </div>
            </div>
        </section>
    </div>

    <script>
        const GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1PD3zhqZ2rTZlMi7X3lsCh6fkvNcR-B2kGv0m9L0Fl_4/gviz/tq?tqx=out:csv&sheet=Master%20Data";
        let RAW_DATA = """ + json_data_str + """;

        let chartCompareInstance = null;
        let chartShareInstance = null;
        let chartTimelineInstance = null;

        let currentSec2Metric = "spend"; // 'spend' | 'daily' | 'phones'
        let currentTimelineGranularity = "month"; // 'month' | 'week' | 'day'
        let lastSection1Rows = [];

        const formatMoney = (v) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(Math.round(v || 0));
        const formatShortMoney = (v) => {
            if (!v || v === 0) return '0 ₫';
            if (Math.abs(v) >= 1e6) return (v / 1e6).toFixed(2) + ' tr';
            if (Math.abs(v) >= 1e3) return Math.round(v / 1e3) + 'k';
            return String(Math.round(v)) + ' ₫';
        };
        const formatNum = (v) => new Intl.NumberFormat('vi-VN').format(v || 0);

        const PRODUCT_PALETTE = [
            '#6366f1', '#10b981', '#06b6d4', '#f59e0b', '#ec4899',
            '#a855f7', '#3b82f6', '#84cc16', '#f43f5e', '#14b8a6'
        ];

        function normalizeProductName(row) {
            let p = String(row["Sản phẩm"] || "").trim();
            if (["BrSE", "Tsu", "Tsubasa"].includes(p)) return "BrSE";
            if (["Embeded", "Nhúng"].includes(p)) return "Embedded";
            if (["AI engineer", "AI Enginner", "AI"].includes(p)) return "AI Engineer";
            if (["Data Analyst", "DA"].includes(p)) return "Data Analyst";
            if (["Data Engineer", "DE"].includes(p)) return "Data Engineer";
            if (["Network Security", "Cyber"].includes(p)) return "Network Security";
            if (!p) {
                const acc = String(row["Tài khoản"] || "");
                if (acc.includes("DABK")) return "Data Analyst";
                if (acc.includes("EMBEDDED")) return "Embedded";
                if (acc.includes("AI")) return "AI Engineer";
                if (acc.includes("BA")) return "BA";
                if (acc.includes("DE")) return "Data Engineer";
                if (acc.includes("PTIT")) return "PTIT";
                if (acc.includes("NHẬT")) return "BrSE";
                return acc || "Khác";
            }
            return p;
        }

        function getEntityName(row) {
            const groupBy = document.getElementById('groupBySelect')?.value || 'product';
            if (groupBy === 'account') {
                return String(row["Tài khoản"] || "Khác").trim();
            }
            return normalizeProductName(row);
        }

        function getIsoWeekKey(dateStr) {
            if (!dateStr) return "Unknown";
            const parts = String(dateStr).trim().split('-');
            if (parts.length < 3) return dateStr.slice(0, 7);
            const d = new Date(Date.UTC(+parts[0], +parts[1] - 1, +parts[2]));
            const dayNum = d.getUTCDay() || 7;
            d.setUTCDate(d.getUTCDate() + 4 - dayNum);
            const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
            const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
            return `W${String(weekNo).padStart(2, '0')}`;
        }

        function formatMonthLabel(ym) {
            if (!ym || !ym.includes('-')) return ym;
            const [y, m] = ym.split('-');
            return `Tháng ${m}/${y}`;
        }

        function initMonthSelectors() {
            const year = document.getElementById('yearSelect')?.value || '2026';
            const prevSel = document.getElementById('prevMonthSelect');
            const currSel = document.getElementById('currMonthSelect');

            const monthMap = {};
            RAW_DATA.forEach(r => {
                const d = String(r["Ngày"] || "").trim();
                if (!d.startsWith(year)) return;
                const ym = d.slice(0, 7);
                if (!monthMap[ym]) monthMap[ym] = new Set();
                monthMap[ym].add(d);
            });

            const months = Object.keys(monthMap).sort();
            prevSel.innerHTML = '';
            currSel.innerHTML = '';

            months.forEach(ym => {
                const daysCount = monthMap[ym].size;
                const text = `${formatMonthLabel(ym)} (${daysCount} ngày có dữ liệu)`;
                const o1 = document.createElement('option');
                o1.value = ym; o1.textContent = text;
                prevSel.appendChild(o1);

                const o2 = document.createElement('option');
                o2.value = ym; o2.textContent = text;
                currSel.appendChild(o2);
            });

            if (months.length >= 2) {
                prevSel.value = months[months.length - 2];
                currSel.value = months[months.length - 1];
            } else if (months.length === 1) {
                prevSel.value = months[0];
                currSel.value = months[0];
            }
        }

        function initProductOptions() {
            const sel = document.getElementById('productSelect');
            const pillsBar = document.getElementById('productPillsBar');
            const year = document.getElementById('yearSelect')?.value || '2026';

            const spendByEntity = {};
            RAW_DATA.forEach(r => {
                const d = String(r["Ngày"] || "").trim();
                if (!d.startsWith(year)) return;
                const ent = getEntityName(r);
                spendByEntity[ent] = (spendByEntity[ent] || 0) + (r["Chi tiêu"] || 0);
            });

            const sortedEntities = Object.keys(spendByEntity).sort((a, b) => spendByEntity[b] - spendByEntity[a]);

            sel.innerHTML = '<option value="ALL">👉 Tất cả đầu sản phẩm (Toàn hệ thống 2026)</option>';
            sortedEntities.forEach(ent => {
                const o = document.createElement('option');
                o.value = ent;
                o.textContent = `📦 ${ent} (${formatShortMoney(spendByEntity[ent])})`;
                sel.appendChild(o);
            });

            pillsBar.innerHTML = `<span style="font-size:0.76rem; font-weight:700; color:var(--text-muted); margin-right:0.2rem;">Chọn nhanh SP:</span>`;
            const allBtn = document.createElement('button');
            allBtn.className = 'prod-pill active';
            allBtn.setAttribute('data-prod', 'ALL');
            allBtn.textContent = 'Tất cả SP';
            allBtn.onclick = () => selectProductPill('ALL');
            pillsBar.appendChild(allBtn);

            sortedEntities.forEach(ent => {
                const btn = document.createElement('button');
                btn.className = 'prod-pill';
                btn.setAttribute('data-prod', ent);
                btn.textContent = ent;
                btn.onclick = () => selectProductPill(ent);
                pillsBar.appendChild(btn);
            });
        }

        function selectProductPill(prodVal) {
            const sel = document.getElementById('productSelect');
            sel.value = prodVal;
            syncProductPillsUI();
            renderDashboard();
        }

        function onProductSelectChange() {
            syncProductPillsUI();
            renderDashboard();
        }

        function syncProductPillsUI() {
            const cur = document.getElementById('productSelect').value;
            document.querySelectorAll('.prod-pill').forEach(btn => {
                btn.classList.toggle('active', btn.getAttribute('data-prod') === cur);
            });
        }

        function setSection2Metric(metric) {
            currentSec2Metric = metric;
            document.getElementById('btnMetricSpend').classList.toggle('active', metric === 'spend');
            document.getElementById('btnMetricDaily').classList.toggle('active', metric === 'daily');
            document.getElementById('btnMetricPhones').classList.toggle('active', metric === 'phones');
            renderDashboard();
        }

        function setTimelineGranularity(gran) {
            currentTimelineGranularity = gran;
            document.getElementById('btnTimeMonth').classList.toggle('active', gran === 'month');
            document.getElementById('btnTimeWeek').classList.toggle('active', gran === 'week');
            document.getElementById('btnTimeDay').classList.toggle('active', gran === 'day');
            renderDashboard();
        }

        function renderDashboard() {
            const year = document.getElementById('yearSelect')?.value || '2026';
            const selectedProd = document.getElementById('productSelect')?.value || 'ALL';
            const prevMonth = document.getElementById('prevMonthSelect')?.value || '2026-10';
            const currMonth = document.getElementById('currMonthSelect')?.value || '2026-11';
            const fmtFilter = document.getElementById('formatSelect')?.value || 'ALL';

            // Lọc dữ liệu trong năm 2026 (theo Hình thức chạy)
            const yearRows = RAW_DATA.filter(r => {
                const d = String(r["Ngày"] || "").trim();
                if (!d.startsWith(year)) return false;
                if (fmtFilter !== 'ALL' && String(r["Hình thức chạy"] || "").trim() !== fmtFilter) return false;
                return true;
            });

            // Gom theo Đầu sản phẩm -> Tháng
            const entityMap = {};
            const monthDaysSystem = {}; // ym -> Set(dates)
            let systemTotal2026Spend = 0;
            let systemTotal2026Phones = 0;

            yearRows.forEach(r => {
                const d = String(r["Ngày"] || "").trim();
                const ym = d.slice(0, 7);
                const ent = getEntityName(r);
                const sp = r["Chi tiêu"] || 0;
                const ph = r["Sđt theo campain"] || 0;
                const ms = r["Tin nhắn"] || 0;

                if (!monthDaysSystem[ym]) monthDaysSystem[ym] = new Set();
                monthDaysSystem[ym].add(d);

                if (!entityMap[ent]) {
                    entityMap[ent] = {
                        name: ent,
                        yearSpend: 0,
                        yearPhones: 0,
                        yearMsgs: 0,
                        yearDays: new Set(),
                        months: {}
                    };
                }
                const eObj = entityMap[ent];
                eObj.yearSpend += sp;
                eObj.yearPhones += ph;
                eObj.yearMsgs += ms;
                eObj.yearDays.add(d);

                if (!eObj.months[ym]) {
                    eObj.months[ym] = { spend: 0, phones: 0, msgs: 0, days: new Set() };
                }
                eObj.months[ym].spend += sp;
                eObj.months[ym].phones += ph;
                eObj.months[ym].msgs += ms;
                eObj.months[ym].days.add(d);

                systemTotal2026Spend += sp;
                systemTotal2026Phones += ph;
            });

            const prevDaysSys = (monthDaysSystem[prevMonth] && monthDaysSystem[prevMonth].size) || 1;
            const currDaysSys = (monthDaysSystem[currMonth] && monthDaysSystem[currMonth].size) || 1;

            // Tính toán bảng Section 1
            const allEntityRows = Object.values(entityMap).map(e => {
                const mPrev = e.months[prevMonth] || { spend: 0, phones: 0, msgs: 0, days: new Set() };
                const mCurr = e.months[currMonth] || { spend: 0, phones: 0, msgs: 0, days: new Set() };

                const shareYear = systemTotal2026Spend > 0 ? (e.yearSpend / systemTotal2026Spend * 100) : 0;
                const diffSpend = mCurr.spend - mPrev.spend;
                const deltaMonthPct = mPrev.spend > 0 ? ((mCurr.spend - mPrev.spend) / mPrev.spend * 100) : (mCurr.spend > 0 ? 100 : 0);

                // Tốc độ chi tiêu TB/ngày của tháng (chia cho số ngày thực tế của tháng có chạy hoặc số ngày hệ thống)
                const dailyPrev = mPrev.spend / prevDaysSys;
                const dailyCurr = mCurr.spend / currDaysSys;
                const deltaDailyPct = dailyPrev > 0 ? ((dailyCurr - dailyPrev) / dailyPrev * 100) : (dailyCurr > 0 ? 100 : 0);

                const deltaPhonesPct = mPrev.phones > 0 ? ((mCurr.phones - mPrev.phones) / mPrev.phones * 100) : (mCurr.phones > 0 ? 100 : 0);
                const cplPrev = mPrev.phones > 0 ? (mPrev.spend / mPrev.phones) : 0;
                const cplCurr = mCurr.phones > 0 ? (mCurr.spend / mCurr.phones) : 0;
                const deltaCplPct = (cplPrev > 0 && cplCurr > 0) ? ((cplCurr - cplPrev) / cplPrev * 100) : 0;

                // Đánh giá biến thiên
                let statusHtml = `<span class="badge badge-neutral">Ổn định</span>`;
                if (mCurr.spend >= 1000000 && mCurr.phones === 0) {
                    statusHtml = `<span class="badge badge-down">🛑 Đốt tiền (0 SĐT)</span>`;
                } else if (deltaDailyPct > 15 && cplCurr > 0 && (cplPrev === 0 || cplCurr <= cplPrev * 1.15)) {
                    statusHtml = `<span class="badge badge-up">🚀 Mở rộng hiệu quả (+${deltaDailyPct.toFixed(0)}%/ngày)</span>`;
                } else if (deltaDailyPct > 10 && cplPrev > 0 && cplCurr > cplPrev * 1.20) {
                    statusHtml = `<span class="badge badge-warn">⚠️ Tăng chi nhưng CPL đắt (+${deltaCplPct.toFixed(0)}%)</span>`;
                } else if (mCurr.phones > 0 && cplCurr <= 280000) {
                    statusHtml = `<span class="badge badge-info">💎 CPL tối ưu (${formatShortMoney(cplCurr)})</span>`;
                } else if (deltaDailyPct < -20) {
                    statusHtml = `<span class="badge badge-neutral">🔽 Thu hẹp ngân sách (${deltaDailyPct.toFixed(0)}%/ngày)</span>`;
                }

                return {
                    name: e.name,
                    yearSpend: e.yearSpend,
                    yearPhones: e.yearPhones,
                    shareYear,
                    mPrev,
                    mCurr,
                    diffSpend,
                    deltaMonthPct,
                    dailyPrev,
                    dailyCurr,
                    deltaDailyPct,
                    deltaPhonesPct,
                    cplPrev,
                    cplCurr,
                    deltaCplPct,
                    statusHtml
                };
            }).sort((a, b) => b.yearSpend - a.yearSpend);

            lastSection1Rows = allEntityRows;

            // Dữ liệu hiển thị cho KPI (Nếu đang chọn 1 sản phẩm thì tính riêng sản phẩm đó, nếu ALL thì tính toàn hệ thống)
            const kpiTargetRows = selectedProd === 'ALL'
                ? allEntityRows
                : allEntityRows.filter(r => r.name === selectedProd);

            renderSection1KPIs(kpiTargetRows, selectedProd, year, prevMonth, currMonth, prevDaysSys, currDaysSys, systemTotal2026Spend);
            renderSection1Table(allEntityRows, selectedProd, prevMonth, currMonth, prevDaysSys, currDaysSys);
            renderSection2Charts(allEntityRows, yearRows, selectedProd, prevMonth, currMonth, prevDaysSys, currDaysSys);
        }

        // ─── RENDER SECTION 1 KPIs ───
        function renderSection1KPIs(rows, selectedProd, year, prevMonth, currMonth, prevDaysSys, currDaysSys, systemTotal2026Spend) {
            const totalYearSpend = rows.reduce((s, r) => s + r.yearSpend, 0);
            const totalYearPhones = rows.reduce((s, r) => s + r.yearPhones, 0);
            const yearCpl = totalYearPhones > 0 ? (totalYearSpend / totalYearPhones) : 0;
            const shareOfSystem = systemTotal2026Spend > 0 ? (totalYearSpend / systemTotal2026Spend * 100) : 0;

            const prevSpend = rows.reduce((s, r) => s + r.mPrev.spend, 0);
            const prevPhones = rows.reduce((s, r) => s + r.mPrev.phones, 0);
            const prevCpl = prevPhones > 0 ? (prevSpend / prevPhones) : 0;
            const prevDaily = prevSpend / prevDaysSys;

            const currSpend = rows.reduce((s, r) => s + r.mCurr.spend, 0);
            const currPhones = rows.reduce((s, r) => s + r.mCurr.phones, 0);
            const currCpl = currPhones > 0 ? (currSpend / currPhones) : 0;
            const currDaily = currSpend / currDaysSys;

            const diffMonthSpend = currSpend - prevSpend;
            const deltaMonthPct = prevSpend > 0 ? ((currSpend - prevSpend) / prevSpend * 100) : (currSpend > 0 ? 100 : 0);
            const deltaDailyPct = prevDaily > 0 ? ((currDaily - prevDaily) / prevDaily * 100) : (currDaily > 0 ? 100 : 0);
            const deltaPhonesPct = prevPhones > 0 ? ((currPhones - prevPhones) / prevPhones * 100) : 0;

            const scopeTitle = selectedProd === 'ALL' ? 'TOÀN BỘ ĐẦU SẢN PHẨM' : `ĐẦU SP: ${selectedProd.toUpperCase()}`;

            document.getElementById('section1KpiGrid').innerHTML = `
                <!-- KPI 1: Tổng Chi Tiêu Năm 2026 -->
                <div class="kpi-card" style="--accent: #6366f1;">
                    <div class="kpi-head">
                        <span>💰 TỔNG CHI TIÊU NĂM ${year} (${scopeTitle})</span>
                    </div>
                    <div class="kpi-main-val">${formatMoney(totalYearSpend)}</div>
                    <div class="kpi-meta">
                        <span>Tỷ trọng năm: <b>${shareOfSystem.toFixed(1)}%</b></span>
                        <span>Tổng SĐT 2026: <b style="color:#34d399;">${formatNum(totalYearPhones)} SĐT</b> (${yearCpl > 0 ? formatShortMoney(yearCpl) : '--'}/SĐT)</span>
                    </div>
                </div>

                <!-- KPI 2: Chi Tiêu Tháng Trước -->
                <div class="kpi-card" style="--accent: #3b82f6;">
                    <div class="kpi-head">
                        <span>⏪ THÁNG TRƯỚC: ${formatMonthLabel(prevMonth)} (${prevDaysSys} ngày)</span>
                    </div>
                    <div class="kpi-main-val">${formatMoney(prevSpend)}</div>
                    <div class="kpi-meta">
                        <span>TB/ngày: <b>${formatShortMoney(prevDaily)}/ngày</b></span>
                        <span>SĐT: <b style="color:#34d399;">${formatNum(prevPhones)}</b> (CPL: <b>${prevCpl > 0 ? formatShortMoney(prevCpl) : '--'}</b>)</span>
                    </div>
                </div>

                <!-- KPI 3: Chi Tiêu Tháng Hiện Tại -->
                <div class="kpi-card" style="--accent: #10b981;">
                    <div class="kpi-head">
                        <span>⏩ THÁNG HIỆN TẠI: ${formatMonthLabel(currMonth)} (${currDaysSys} ngày)</span>
                    </div>
                    <div class="kpi-main-val" style="color:#34d399;">${formatMoney(currSpend)}</div>
                    <div class="kpi-meta">
                        <span>TB/ngày: <b>${formatShortMoney(currDaily)}/ngày</b></span>
                        <span>SĐT: <b style="color:#34d399;">${formatNum(currPhones)}</b> (CPL: <b>${currCpl > 0 ? formatShortMoney(currCpl) : '--'}</b>)</span>
                    </div>
                </div>

                <!-- KPI 4: So Sánh Tháng Trước vs Tháng Hiện Tại -->
                <div class="kpi-card" style="--accent: #f59e0b;">
                    <div class="kpi-head">
                        <span>⚖️ SO SÁNH ${currMonth} VS ${prevMonth}</span>
                    </div>
                    <div class="kpi-main-val" style="color:${deltaMonthPct >= 0 ? '#fbbf24' : '#38bdf8'};">
                        ${deltaMonthPct >= 0 ? '+' : ''}${deltaMonthPct.toFixed(1)}% <small style="font-size:0.85rem; font-weight:700;">(${diffMonthSpend >= 0 ? '+' : ''}${formatShortMoney(diffMonthSpend)})</small>
                    </div>
                    <div class="kpi-meta">
                        <span>Tốc độ chi/ngày: <b style="color:${deltaDailyPct >= 0 ? '#fbbf24' : '#34d399'};">${deltaDailyPct >= 0 ? '+' : ''}${deltaDailyPct.toFixed(1)}%</b></span>
                        <span>Biến thiên SĐT: <b style="color:${deltaPhonesPct >= 0 ? '#34d399' : '#f87171'};">${deltaPhonesPct >= 0 ? '+' : ''}${deltaPhonesPct.toFixed(1)}%</b></span>
                    </div>
                </div>
            `;
        }

        // ─── RENDER SECTION 1 TABLE ───
        function renderSection1Table(rows, selectedProd, prevMonth, currMonth, prevDaysSys, currDaysSys) {
            document.getElementById('thPrevMonth').textContent = `Tháng Trước (${prevMonth})`;
            document.getElementById('thCurrMonth').textContent = `Tháng Hiện Tại (${currMonth})`;

            const tbody = document.getElementById('section1TableBody');
            const displayRows = selectedProd === 'ALL' ? rows : rows.filter(r => r.name === selectedProd);

            const html = displayRows.map(r => {
                const isSelected = selectedProd === r.name;
                const monthBadge = r.deltaMonthPct >= 0 ? 'badge-warn' : 'badge-info';
                const dailyBadge = r.deltaDailyPct > 10 ? 'badge-warn' : r.deltaDailyPct < -10 ? 'badge-neutral' : 'badge-up';
                const cplPrevStr = r.mPrev.phones > 0 ? formatShortMoney(r.cplPrev) : '--';
                const cplCurrStr = r.mCurr.phones > 0 ? formatShortMoney(r.cplCurr) : (r.mCurr.spend > 0 ? '0 SĐT' : '--');

                return `
                    <tr class="${isSelected ? 'selected-row' : ''}" onclick="selectProductPill('${r.name === selectedProd ? 'ALL' : r.name.replace(/'/g, "\\'")}')" style="cursor:pointer;" title="Bấm để lọc riêng sản phẩm ${r.name}">
                        <td><b>📦 ${r.name}</b></td>
                        <td><b>${formatMoney(r.yearSpend)}</b></td>
                        <td>
                            <div class="bar-mini"><div class="bar-mini-fill" style="width:${Math.min(100, r.shareYear)}%; background:#6366f1;"></div></div>
                            <b>${r.shareYear.toFixed(1)}%</b>
                        </td>
                        <td>${formatMoney(r.mPrev.spend)}</td>
                        <td><b style="color:#34d399;">${formatMoney(r.mCurr.spend)}</b></td>
                        <td style="color:${r.diffSpend >= 0 ? '#fbbf24' : '#94a3b8'}; font-weight:700;">
                            ${r.diffSpend >= 0 ? '+' : ''}${formatMoney(r.diffSpend)}
                        </td>
                        <td><span class="badge ${monthBadge}">${r.deltaMonthPct >= 0 ? '+' : ''}${r.deltaMonthPct.toFixed(1)}%</span></td>
                        <td>${formatShortMoney(r.dailyPrev)} ➔ <b>${formatShortMoney(r.dailyCurr)}</b></td>
                        <td><span class="badge ${dailyBadge}">${r.deltaDailyPct >= 0 ? '+' : ''}${r.deltaDailyPct.toFixed(1)}%/ngày</span></td>
                        <td><b>${r.mPrev.phones}</b> ➔ <b style="color:#34d399;">${r.mCurr.phones} SĐT</b></td>
                        <td>${cplPrevStr} ➔ <b>${cplCurrStr}</b></td>
                        <td>${r.statusHtml}</td>
                    </tr>
                `;
            }).join('');

            // Dòng tổng cộng
            const totYear = displayRows.reduce((s, r) => s + r.yearSpend, 0);
            const totPrev = displayRows.reduce((s, r) => s + r.mPrev.spend, 0);
            const totCurr = displayRows.reduce((s, r) => s + r.mCurr.spend, 0);
            const totDiff = totCurr - totPrev;
            const totDeltaMonth = totPrev > 0 ? ((totCurr - totPrev) / totPrev * 100) : 0;
            const totDailyPrev = totPrev / prevDaysSys;
            const totDailyCurr = totCurr / currDaysSys;
            const totDeltaDaily = totDailyPrev > 0 ? ((totDailyCurr - totDailyPrev) / totDailyPrev * 100) : 0;
            const totPhonesPrev = displayRows.reduce((s, r) => s + r.mPrev.phones, 0);
            const totPhonesCurr = displayRows.reduce((s, r) => s + r.mCurr.phones, 0);
            const totCplPrev = totPhonesPrev > 0 ? formatShortMoney(totPrev / totPhonesPrev) : '--';
            const totCplCurr = totPhonesCurr > 0 ? formatShortMoney(totCurr / totPhonesCurr) : '--';

            const totalRow = `
                <tr class="total-row">
                    <td>TỔNG CỘNG (${selectedProd === 'ALL' ? 'TOÀN HỆ THỐNG' : selectedProd})</td>
                    <td>${formatMoney(totYear)}</td>
                    <td>${selectedProd === 'ALL' ? '100.0%' : displayRows[0]?.shareYear.toFixed(1) + '%'}</td>
                    <td>${formatMoney(totPrev)}</td>
                    <td>${formatMoney(totCurr)}</td>
                    <td>${totDiff >= 0 ? '+' : ''}${formatMoney(totDiff)}</td>
                    <td>${totDeltaMonth >= 0 ? '+' : ''}${totDeltaMonth.toFixed(1)}%</td>
                    <td>${formatShortMoney(totDailyPrev)} ➔ ${formatShortMoney(totDailyCurr)}</td>
                    <td>${totDeltaDaily >= 0 ? '+' : ''}${totDeltaDaily.toFixed(1)}%/ngày</td>
                    <td>${totPhonesPrev} ➔ ${totPhonesCurr} SĐT</td>
                    <td>${totCplPrev} ➔ ${totCplCurr}</td>
                    <td>Tổng SĐT Năm 2026: ${displayRows.reduce((s, r) => s + r.yearPhones, 0)} SĐT</td>
                </tr>
            `;

            tbody.innerHTML = html + totalRow;
        }

        // ─── RENDER SECTION 2: BIỂU ĐỒ CHI TIÊU CÁC SẢN PHẨM ───
        function getThemeColors() {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            return {
                text: isDark ? '#94a3b8' : '#475569',
                grid: isDark ? 'rgba(255, 255, 255, 0.07)' : 'rgba(15, 23, 42, 0.07)'
            };
        }

        function renderSection2Charts(allEntityRows, yearRows, selectedProd, prevMonth, currMonth, prevDaysSys, currDaysSys) {
            const colors = getThemeColors();

            // 1. Biểu đồ 2.1: So sánh Chi tiêu các sản phẩm Tháng trước vs Tháng hiện tại
            const ctxCompare = document.getElementById('chartProductMonthCompare').getContext('2d');
            const chartRows = allEntityRows.filter(r => r.yearSpend > 0);
            const labels = chartRows.map(r => r.name);

            let datasetsCompare = [];
            if (currentSec2Metric === 'daily') {
                document.getElementById('chartCompareTitle').textContent = `1️⃣ So Sánh Chi Tiêu TB/Ngày Các Sản Phẩm: ${prevMonth} vs. ${currMonth}`;
                datasetsCompare = [
                    {
                        label: `TB/Ngày ${prevMonth}`,
                        data: chartRows.map(r => Math.round(r.dailyPrev)),
                        backgroundColor: 'rgba(59, 130, 246, 0.75)',
                        borderRadius: 6
                    },
                    {
                        label: `TB/Ngày ${currMonth}`,
                        data: chartRows.map(r => Math.round(r.dailyCurr)),
                        backgroundColor: 'rgba(16, 185, 129, 0.85)',
                        borderRadius: 6
                    }
                ];
            } else if (currentSec2Metric === 'phones') {
                document.getElementById('chartCompareTitle').textContent = `1️⃣ So Sánh Tổng Chi Tiêu & SĐT Các Sản Phẩm: ${prevMonth} vs. ${currMonth}`;
                datasetsCompare = [
                    {
                        label: `Chi tiêu ${prevMonth}`,
                        data: chartRows.map(r => Math.round(r.mPrev.spend)),
                        backgroundColor: 'rgba(59, 130, 246, 0.65)',
                        borderRadius: 6,
                        yAxisID: 'ySpend'
                    },
                    {
                        label: `Chi tiêu ${currMonth}`,
                        data: chartRows.map(r => Math.round(r.mCurr.spend)),
                        backgroundColor: 'rgba(16, 185, 129, 0.78)',
                        borderRadius: 6,
                        yAxisID: 'ySpend'
                    },
                    {
                        label: `SĐT ${currMonth}`,
                        data: chartRows.map(r => r.mCurr.phones),
                        type: 'line',
                        borderColor: '#f59e0b',
                        backgroundColor: '#f59e0b',
                        borderWidth: 2.5,
                        pointRadius: 5,
                        yAxisID: 'yPhones'
                    }
                ];
            } else {
                document.getElementById('chartCompareTitle').textContent = `1️⃣ Biểu Đồ So Sánh Chi Tiêu Các Sản Phẩm: Tháng Trước (${prevMonth}) vs. Tháng Hiện Tại (${currMonth})`;
                datasetsCompare = [
                    {
                        label: `Tháng Trước (${prevMonth})`,
                        data: chartRows.map(r => Math.round(r.mPrev.spend)),
                        backgroundColor: chartRows.map(r => (selectedProd === 'ALL' || selectedProd === r.name) ? 'rgba(99, 102, 241, 0.78)' : 'rgba(99, 102, 241, 0.22)'),
                        borderRadius: 6
                    },
                    {
                        label: `Tháng Hiện Tại (${currMonth})`,
                        data: chartRows.map(r => Math.round(r.mCurr.spend)),
                        backgroundColor: chartRows.map(r => (selectedProd === 'ALL' || selectedProd === r.name) ? 'rgba(16, 185, 129, 0.85)' : 'rgba(16, 185, 129, 0.22)'),
                        borderRadius: 6
                    }
                ];
            }

            if (chartCompareInstance) chartCompareInstance.destroy();
            chartCompareInstance = new Chart(ctxCompare, {
                type: 'bar',
                data: { labels, datasets: datasetsCompare },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    onClick: (evt, els) => {
                        if (els.length > 0) {
                            const clickedProd = labels[els[0].index];
                            selectProductPill(selectedProd === clickedProd ? 'ALL' : clickedProd);
                        }
                    },
                    plugins: {
                        legend: { position: 'top', labels: { color: colors.text, font: { weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => {
                                    if (ctx.dataset.yAxisID === 'yPhones') return `${ctx.dataset.label}: ${ctx.raw} SĐT`;
                                    return `${ctx.dataset.label}: ${formatMoney(ctx.raw)}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: { grid: { color: colors.grid }, ticks: { color: colors.text, font: { weight: 600 } } },
                        ySpend: {
                            type: 'linear',
                            position: 'left',
                            grid: { color: colors.grid },
                            ticks: { color: colors.text, callback: v => formatShortMoney(v) }
                        },
                        ...(currentSec2Metric === 'phones' ? {
                            yPhones: {
                                type: 'linear',
                                position: 'right',
                                grid: { drawOnChartArea: false },
                                ticks: { color: '#f59e0b', precision: 0 }
                            }
                        } : {})
                    }
                }
            });

            // 2. Biểu đồ 2.2: Cơ cấu Tỷ trọng Chi tiêu Năm 2026 giữa các Đầu sản phẩm
            const ctxShare = document.getElementById('chartProductShare2026').getContext('2d');
            if (chartShareInstance) chartShareInstance.destroy();
            chartShareInstance = new Chart(ctxShare, {
                type: 'doughnut',
                data: {
                    labels: chartRows.map(r => `${r.name} (${r.shareYear.toFixed(1)}%)`),
                    datasets: [{
                        data: chartRows.map(r => Math.round(r.yearSpend)),
                        backgroundColor: PRODUCT_PALETTE,
                        borderWidth: 2,
                        borderColor: 'transparent'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '62%',
                    onClick: (evt, els) => {
                        if (els.length > 0) {
                            const clickedProd = chartRows[els[0].index].name;
                            selectProductPill(selectedProd === clickedProd ? 'ALL' : clickedProd);
                        }
                    },
                    plugins: {
                        legend: { position: 'right', labels: { color: colors.text, font: { size: 11, weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => {
                                    const r = chartRows[ctx.dataIndex];
                                    return `${r.name}: ${formatMoney(r.yearSpend)} (${r.shareYear.toFixed(1)}% | ${r.yearPhones} SĐT)`;
                                }
                            }
                        }
                    }
                }
            });

            // 3. Biểu đồ 2.3: Diễn biến Chi tiêu các sản phẩm theo Thời gian (Tháng / Tuần / Ngày)
            const ctxTime = document.getElementById('chartProductTimeline').getContext('2d');
            const filteredTimeRows = selectedProd === 'ALL'
                ? yearRows
                : yearRows.filter(r => getEntityName(r) === selectedProd);

            const bucketSet = new Set();
            const entTimeMap = {}; // ent -> bucket -> {spend, phones}
            const bucketPhones = {};

            filteredTimeRows.forEach(r => {
                const d = String(r["Ngày"] || "").trim();
                const bKey = currentTimelineGranularity === 'month'
                    ? d.slice(0, 7)
                    : (currentTimelineGranularity === 'week' ? getIsoWeekKey(d) : d.slice(5));
                bucketSet.add(bKey);
                const ent = getEntityName(r);
                if (!entTimeMap[ent]) entTimeMap[ent] = {};
                if (!entTimeMap[ent][bKey]) entTimeMap[ent][bKey] = 0;
                entTimeMap[ent][bKey] += (r["Chi tiêu"] || 0);
                bucketPhones[bKey] = (bucketPhones[bKey] || 0) + (r["Sđt theo campain"] || 0);
            });

            const sortedBuckets = Array.from(bucketSet).sort();
            const activeEntities = (selectedProd === 'ALL' ? chartRows.slice(0, 8).map(r => r.name) : [selectedProd]);

            const timeDatasets = activeEntities.map((ent, idx) => ({
                label: ent,
                data: sortedBuckets.map(b => Math.round((entTimeMap[ent] && entTimeMap[ent][b]) || 0)),
                backgroundColor: PRODUCT_PALETTE[idx % PRODUCT_PALETTE.length],
                borderRadius: 4,
                yAxisID: 'ySpend',
                order: 2
            }));

            // Thêm đường Tổng SĐT lên trên cột chồng
            timeDatasets.push({
                label: 'Tổng SĐT Pancake',
                data: sortedBuckets.map(b => bucketPhones[b] || 0),
                type: 'line',
                borderColor: '#34d399',
                backgroundColor: '#34d399',
                borderWidth: 2.5,
                pointRadius: 4,
                tension: 0.25,
                yAxisID: 'yPhones',
                order: 1
            });

            if (chartTimelineInstance) chartTimelineInstance.destroy();
            chartTimelineInstance = new Chart(ctxTime, {
                type: 'bar',
                data: { labels: sortedBuckets, datasets: timeDatasets },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: { position: 'top', labels: { color: colors.text, boxWidth: 12, font: { size: 11, weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => {
                                    if (ctx.dataset.yAxisID === 'yPhones') return `SĐT Pancake: ${ctx.raw} SĐT`;
                                    return `${ctx.dataset.label}: ${formatMoney(ctx.raw)}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: { stacked: true, grid: { color: colors.grid }, ticks: { color: colors.text } },
                        ySpend: {
                            stacked: true,
                            position: 'left',
                            grid: { color: colors.grid },
                            ticks: { color: colors.text, callback: v => formatShortMoney(v) }
                        },
                        yPhones: {
                            position: 'right',
                            grid: { drawOnChartArea: false },
                            ticks: { color: '#34d399', precision: 0 }
                        }
                    }
                }
            });
        }

        // ─── Đồng bộ Google Sheets ───
        async function syncGoogleSheet() {
            const badge = document.getElementById('syncBadge');
            badge.textContent = '⏳ Đang đồng bộ...';
            try {
                const resp = await fetch(GOOGLE_SHEET_CSV_URL, { cache: 'no-cache' });
                if (!resp.ok) throw new Error('HTTP ' + resp.status);
                const text = await resp.text();
                Papa.parse(text, {
                    header: true,
                    dynamicTyping: true,
                    skipEmptyLines: true,
                    complete: (res) => {
                        if (res.data && res.data.length > 0) {
                            RAW_DATA = res.data.map(r => ({
                                "Tài khoản": r["Account Name"] || r["Tài khoản"] || "",
                                "ID tài khoản": r["Account ID"] || r["ID tài khoản"] || "",
                                "Ngày": String(r["Ngày"] || "").trim(),
                                "Campaign ID": String(r["Campaign ID"] || ""),
                                "Tên chiến dịch": r["Tên chiến dịch"] || "",
                                "Sản phẩm": r["Sản phẩm"] || "",
                                "Hình thức chạy": r["Hình thức chạy"] || "",
                                "Trạng thái": r["Trạng thái"] || "UNKNOWN",
                                "Chi tiêu": parseFloat(r["Chi tiêu"] || 0),
                                "Hiển thị": parseInt(r["Hiển thị"] || 0),
                                "Click link": parseInt(r["Click link"] || 0),
                                "Tin nhắn": parseInt(r["Tin nhắn"] || 0),
                                "Lead": parseInt(r["Lead"] || 0),
                                "Đăng ký": parseInt(r["Đăng ký"] || 0),
                                "Sđt theo campain": parseInt(r["Sđt theo campain"] || 0)
                            }));
                            badge.textContent = '🟢 Đã đồng bộ Google Sheet';
                            initMonthSelectors();
                            initProductOptions();
                            renderDashboard();
                        }
                    }
                });
            } catch (e) {
                badge.textContent = '🟡 Dữ liệu Cục bộ 2026';
            }
        }

        function exportSection1CSV() {
            if (!lastSection1Rows.length) return;
            const prevMonth = document.getElementById('prevMonthSelect').value;
            const currMonth = document.getElementById('currMonthSelect').value;
            const data = lastSection1Rows.map(r => ({
                "Đầu sản phẩm": r.name,
                "Tổng chi tiêu năm 2026": Math.round(r.yearSpend),
                "Tỷ trọng năm 2026 (%)": +r.shareYear.toFixed(2),
                [`Chi tiêu ${prevMonth}`]: Math.round(r.mPrev.spend),
                [`Chi tiêu ${currMonth}`]: Math.round(r.mCurr.spend),
                "Chênh lệch (VNĐ)": Math.round(r.diffSpend),
                "Δ% Biến thiên tháng (%)": +r.deltaMonthPct.toFixed(2),
                [`TB/Ngày ${prevMonth}`]: Math.round(r.dailyPrev),
                [`TB/Ngày ${currMonth}`]: Math.round(r.dailyCurr),
                "Δ% Tốc độ chi/ngày (%)": +r.deltaDailyPct.toFixed(2),
                [`SĐT ${prevMonth}`]: r.mPrev.phones,
                [`SĐT ${currMonth}`]: r.mCurr.phones,
                [`CPL ${prevMonth}`]: Math.round(r.cplPrev),
                [`CPL ${currMonth}`]: Math.round(r.cplCurr)
            }));
            const csv = Papa.unparse(data);
            const blob = new Blob(["\\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `Chi_Tieu_San_Pham_2026_${prevMonth}_vs_${currMonth}.csv`;
            a.click();
        }

        function toggleTheme() {
            const cur = document.documentElement.getAttribute('data-theme');
            document.documentElement.setAttribute('data-theme', cur === 'dark' ? 'light' : 'dark');
            renderDashboard();
        }

        document.addEventListener('DOMContentLoaded', () => {
            initMonthSelectors();
            initProductOptions();
            renderDashboard();
        });
    </script>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Đã cập nhật Dashboard theo thiết kế Section 1 & Section 2 tại: {html_path}")
print(f"Dung lượng file: {os.path.getsize(html_path) / 1024:.1f} KB")
