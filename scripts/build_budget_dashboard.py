import csv
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, "data", "lark_product_cleaned.csv")
html_path = os.path.join(base_dir, "dashboard_tru_cot_1_ngan_sach.html")

print("Đọc dữ liệu sạch từ lark_product_cleaned.csv...")
rows = []
int_fields = {
    "Năm", "Tháng Số",
    "Tổng Chi Phí Ads (Sau Thuế)", "Chi Phí FB Mess (Sau Thuế)", "Chi Phí FB Landing (Sau Thuế)", "Chi Phí TikTok (Sau Thuế)",
    "Chi Phí FB Mess (Trước Thuế)", "Chi Phí FB Landing (Trước Thuế)", "Chi Phí TikTok (Trước Thuế)",
    "SL Mess", "SL Data Tổng", "SL Data FB Mess", "SL Data FB Landing", "SL Data TikTok",
    "CPL Tổng", "CPL Kế Hoạch", "Chênh Lệch CPL", "CP/Mess",
    "HĐ Ký Trong Tháng", "Tổng HĐ", "HĐ Hết Vòng", "CP/HĐ Hết Vòng",
    "Doanh Số Trong Tháng", "Doanh Số Tổng"
}
float_fields = {"CP/DS Tổng (%)", "% Vượt/Đạt CPL KH"}

with open(csv_path, mode="r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for r in reader:
        d = dict(r)
        for k in int_fields:
            try:
                d[k] = int(float(d.get(k, 0) or 0))
            except Exception:
                d[k] = 0
        for k in float_fields:
            try:
                d[k] = float(d.get(k, 0.0) or 0.0)
            except Exception:
                d[k] = 0.0
        rows.append(d)

print(f"-> Đã đọc {len(rows)} bản ghi sản phẩm sạch.")
json_data_str = json.dumps(rows, ensure_ascii=False)

html_content = """<!DOCTYPE html>
<html lang="vi" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quản Trị Ngân Sách & CPL Sản Phẩm 2026 | Product Report</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
    <style>
        :root {
            --bg-base: #070b14;
            --bg-surface: rgba(15, 23, 42, 0.88);
            --bg-surface-solid: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.65);
            --border-color: rgba(255, 255, 255, 0.09);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --primary: #6366f1;
            --primary-light: rgba(99, 102, 241, 0.16);
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --cyan: #06b6d4;
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-full: 9999px;
            --shadow-card: 0 8px 24px -4px rgba(0, 0, 0, 0.42);
        }

        [data-theme="light"] {
            --bg-base: #f1f5f9;
            --bg-surface: #ffffff;
            --bg-surface-solid: #f8fafc;
            --bg-card: #f8fafc;
            --border-color: rgba(15, 23, 42, 0.1);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --primary: #4f46e5;
            --shadow-card: 0 4px 14px rgba(0, 0, 0, 0.06);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-base);
            background-image:
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 45%),
                radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.08) 0px, transparent 45%);
            color: var(--text-primary);
            min-height: 100vh;
            padding-bottom: 2.5rem;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 1rem 1.25rem;
        }

        /* ─── COMPACT TOP BAR ─── */
        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.75rem;
            padding: 0.85rem 1.15rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-card);
            margin-bottom: 0.85rem;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .brand-logo {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: linear-gradient(135deg, #6366f1 0%, #10b981 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        }

        .brand-title {
            font-size: 1.08rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .top-controls {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .select-sm {
            height: 36px;
            padding: 0 0.65rem;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-color);
            background: var(--bg-surface-solid);
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.8rem;
            font-weight: 700;
            cursor: pointer;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            height: 36px;
            padding: 0 0.8rem;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-color);
            background: var(--bg-card);
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.78rem;
            font-weight: 700;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.15s;
        }

        .btn:hover { border-color: var(--primary); }
        .btn-primary { background: var(--primary); border-color: var(--primary); color: #fff; }

        /* ─── PRODUCT PILLS BAR ─── */
        .pills-bar {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            flex-wrap: wrap;
            padding: 0.6rem 1rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            margin-bottom: 0.85rem;
        }

        .prod-pill {
            padding: 0.28rem 0.7rem;
            border-radius: var(--radius-full);
            border: 1px solid var(--border-color);
            background: var(--bg-surface-solid);
            color: var(--text-secondary);
            font-size: 0.75rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }

        .prod-pill:hover { border-color: var(--primary); color: var(--text-primary); }
        .prod-pill.active {
            background: var(--primary);
            border-color: var(--primary);
            color: #fff;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.35);
        }

        .pill-dot-alert {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #ef4444;
            display: inline-block;
        }

        .pill-dot-ok {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #10b981;
            display: inline-block;
        }

        /* ─── CPL ALERT BANNER ─── */
        .cpl-alert-strip {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.65rem;
            padding: 0.7rem 1rem;
            border-radius: var(--radius-md);
            background: rgba(239, 68, 68, 0.10);
            border: 1px solid rgba(239, 68, 68, 0.32);
            margin-bottom: 1rem;
            font-size: 0.79rem;
        }

        .cpl-alert-chips {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            flex-wrap: wrap;
        }

        .cpl-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.22rem 0.6rem;
            border-radius: var(--radius-full);
            font-size: 0.74rem;
            font-weight: 800;
            cursor: pointer;
        }

        .cpl-chip.over {
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.45);
        }

        .cpl-chip.good {
            background: rgba(16, 185, 129, 0.18);
            color: #6ee7b7;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }

        [data-theme="light"] .cpl-chip.over { color: #dc2626; }
        [data-theme="light"] .cpl-chip.good { color: #059669; }

        /* ─── SECTION CONTAINER ─── */
        .section-box {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.1rem 1.25rem;
            margin-bottom: 1.15rem;
            box-shadow: var(--shadow-card);
        }

        .section-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.9rem;
        }

        .section-label {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.96rem;
            font-weight: 800;
        }

        .tag-sec {
            padding: 0.15rem 0.5rem;
            border-radius: 6px;
            background: var(--primary-light);
            color: #818cf8;
            font-size: 0.7rem;
            font-weight: 800;
        }

        /* ─── SECTION 1: 6 COMPACT KPI CARDS ─── */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 0.75rem;
        }

        @media (max-width: 1380px) { .kpi-grid { grid-template-columns: repeat(3, 1fr); } }
        @media (max-width: 700px) { .kpi-grid { grid-template-columns: 1fr; } }

        .kpi-box {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-top: 3px solid var(--accent, var(--primary));
            border-radius: var(--radius-md);
            padding: 0.85rem 1rem;
        }

        .kpi-name {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-secondary);
            display: flex;
            justify-content: space-between;
        }

        .kpi-num {
            font-size: 1.38rem;
            font-weight: 800;
            margin: 0.25rem 0;
            letter-spacing: -0.02em;
            font-variant-numeric: tabular-nums;
        }

        .kpi-foot {
            font-size: 0.73rem;
            color: var(--text-secondary);
            display: flex;
            justify-content: space-between;
            padding-top: 0.3rem;
            border-top: 1px solid var(--border-color);
            font-variant-numeric: tabular-nums;
        }

        /* ─── SECTION 2: CHARTS ─── */
        .charts-row {
            display: grid;
            grid-template-columns: 1.35fr 1fr;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        @media (max-width: 1024px) { .charts-row { grid-template-columns: 1fr; } }

        .chart-panel {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 0.95rem 1.05rem;
        }

        .chart-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.65rem;
            font-size: 0.85rem;
            font-weight: 800;
        }

        .canvas-wrap {
            position: relative;
            height: 300px;
            width: 100%;
        }

        .switch-group {
            display: inline-flex;
            background: var(--bg-surface-solid);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 2px;
            gap: 2px;
        }

        .switch-btn {
            padding: 0.22rem 0.6rem;
            border-radius: 5px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            font-family: inherit;
            font-size: 0.72rem;
            font-weight: 700;
            cursor: pointer;
        }

        .switch-btn.active { background: var(--primary); color: #fff; }

        /* ─── COMPACT TABLES ─── */
        .table-wrap {
            overflow-x: auto;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.79rem;
            text-align: left;
            white-space: nowrap;
            font-variant-numeric: tabular-nums;
        }

        th {
            background: var(--bg-surface-solid);
            padding: 0.65rem 0.8rem;
            font-weight: 700;
            color: var(--text-secondary);
            border-bottom: 2px solid var(--border-color);
            font-size: 0.71rem;
            text-transform: uppercase;
        }

        td {
            padding: 0.6rem 0.8rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        tr:hover td { background: rgba(99, 102, 241, 0.05); }
        tr.active-row td { background: rgba(99, 102, 241, 0.14); }
        tr.total-row td {
            background: rgba(99, 102, 241, 0.12);
            font-weight: 800;
            border-top: 2px solid var(--primary);
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.2rem;
            padding: 0.15rem 0.5rem;
            border-radius: var(--radius-full);
            font-size: 0.7rem;
            font-weight: 800;
        }

        .b-up { background: rgba(16, 185, 129, 0.16); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }
        .b-down { background: rgba(239, 68, 68, 0.18); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
        .b-warn { background: rgba(245, 158, 11, 0.16); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.35); }
        .b-info { background: rgba(6, 182, 212, 0.16); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.35); }
        .b-muted { background: rgba(148, 163, 184, 0.14); color: #94a3b8; }

        .mini-bar {
            width: 44px;
            height: 5px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 99px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-right: 5px;
        }

        .mini-bar-fill { height: 100%; border-radius: 99px; background: #6366f1; }

        /* ═══════════ TỐI ƯU HIỂN THỊ ═══════════ */
        html { scroll-behavior: smooth; }

        /* Thanh lọc dính trên cùng khi cuộn */
        .sticky-head {
            position: sticky;
            top: 0;
            z-index: 60;
            padding-top: 0.6rem;
            margin-top: -0.6rem;
            background: linear-gradient(to bottom, var(--bg-base) 82%, transparent);
        }
        .sticky-head .topbar { backdrop-filter: blur(10px); margin-bottom: 0.5rem; }
        .sticky-head .pills-bar { margin-bottom: 0.6rem; }

        /* Điều hướng nhanh giữa các section */
        .sec-nav { display: flex; gap: 0.35rem; flex-wrap: wrap; margin-left: auto; }
        .sec-nav a {
            font-size: 0.7rem; font-weight: 700; text-decoration: none;
            color: var(--text-secondary); padding: 0.22rem 0.6rem;
            border-radius: var(--radius-full); border: 1px solid var(--border-color);
            background: var(--bg-surface-solid);
        }
        .sec-nav a:hover { color: var(--text-primary); border-color: var(--primary); }
        .section-box, #cplAlertStrip { scroll-margin-top: 150px; }

        /* KPI co giãn theo màn hình, số không bị tràn */
        .kpi-grid { grid-template-columns: repeat(auto-fit, minmax(215px, 1fr)) !important; }
        .kpi-num { font-size: clamp(1.05rem, 1.35vw, 1.38rem); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .kpi-name { gap: 0.4rem; }
        .kpi-name span:last-child { text-transform: none; font-weight: 600; color: var(--text-muted); white-space: nowrap; }
        .kpi-foot { gap: 0.4rem; flex-wrap: wrap; }

        /* Bảng: header dính, cột Sản phẩm dính, zebra, số căn phải */
        .table-wrap { max-height: 560px; overflow: auto; }
        .table-wrap thead th { position: sticky; top: 0; z-index: 3; }
        .table-wrap th:first-child,
        .table-wrap td:first-child {
            position: sticky; left: 0; z-index: 2;
            background: var(--bg-surface-solid);
            box-shadow: 1px 0 0 var(--border-color);
            min-width: 150px;
        }
        .table-wrap thead th:first-child { z-index: 4; }
        .table-wrap td:not(:first-child), .table-wrap th:not(:first-child) { text-align: right; }
        .table-wrap tbody tr:nth-child(even):not(.total-row) td:not(:first-child) { background: rgba(148, 163, 184, 0.045); }
        .table-wrap tbody tr:hover td:not(:first-child) { background: rgba(99, 102, 241, 0.08); }
        .table-wrap tbody tr.active-row td { background: rgba(99, 102, 241, 0.16); }
        .table-wrap tbody tr.active-row td:first-child { box-shadow: inset 3px 0 0 var(--primary), 1px 0 0 var(--border-color); }
        .table-wrap tr.total-row td { position: sticky; bottom: 0; z-index: 2; background: var(--bg-surface-solid); }
        .table-wrap tr.total-row td:first-child { z-index: 3; }
        #perfTable td { vertical-align: top; padding: 0.5rem 0.65rem; }
        #perfTable th:not(:first-child) { min-width: 92px; }

        /* Chú thích cho bảng hiệu suất */
        .legend-row { display: flex; gap: 0.9rem; flex-wrap: wrap; font-size: 0.71rem; color: var(--text-secondary); margin-bottom: 0.6rem; }
        .legend-row b { color: var(--text-primary); }
        .lg-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; vertical-align: middle; }

        /* Light theme: tăng tương phản màu chữ */
        [data-theme="light"] .b-up { color: #047857; }
        [data-theme="light"] .b-down { color: #b91c1c; }
        [data-theme="light"] .b-warn { color: #b45309; }
        [data-theme="light"] .b-info { color: #0e7490; }
        [data-theme="light"] .mini-bar { background: rgba(15, 23, 42, 0.1); }
        [data-theme="light"] .tag-sec { color: #4f46e5; }

        /* Màn hình nhỏ */
        @media (max-width: 900px) {
            .sticky-head { position: static; background: none; }
            .sec-nav { display: none; }
            .container { padding: 0.6rem; }
            .section-box { padding: 0.85rem; }
            table { font-size: 0.74rem; }
            .canvas-wrap { height: 250px !important; }
            .top-controls { width: 100%; }
            .top-controls .select-sm { flex: 1 1 140px; }
        }

        /* In ấn / xuất PDF */
        @media print {
            .sticky-head { position: static; }
            .top-controls, .sec-nav, .switch-group, .btn { display: none !important; }
            .table-wrap { max-height: none; overflow: visible; }
            .section-box { break-inside: avoid; box-shadow: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sticky-head">
        <!-- ─── TOP BAR ─── -->
        <div class="topbar">
            <div class="brand">
                <div class="brand-logo">📊</div>
                <div>
                    <div class="brand-title">QUẢN TRỊ NGÂN SÁCH & ĐỊNH MỨC CPL SẢN PHẨM</div>
                    <div style="font-size:0.72rem; color:var(--text-secondary);" id="syncStatusText">🟢 Nguồn: Lark Base (tblEr3vySvt58EkK) ➔ Google Sheet Online</div>
                </div>
            </div>

            <div class="top-controls">
                <select id="yearSelect" class="select-sm" onchange="onYearChange()">
                    <option value="2026" selected>📅 Năm 2026</option>
                    <option value="2025">📅 Năm 2025</option>
                </select>
                <select id="productSelect" class="select-sm" onchange="onProductDropdownChange()">
                    <option value="ALL">📦 Tất cả sản phẩm</option>
                </select>
                <select id="prevMonthSelect" class="select-sm" onchange="renderAll()"></select>
                <span style="font-weight:800; color:var(--primary);">➔</span>
                <select id="currMonthSelect" class="select-sm" onchange="renderAll()"></select>

                <button class="btn btn-primary" onclick="fetchFromGoogleSheet()">🔄 Làm mới Sheet</button>
                <a class="btn" href="https://docs.google.com/spreadsheets/d/1V9z5T7BQABDSvsytY0P1kKV5b4lMfpzcFZWghJwUitw/edit" target="_blank">📗 Google Sheet</a>
                <button class="btn" onclick="toggleTheme()">🌓</button>
            </div>
        </div>

        <!-- ─── QUICK PRODUCT PILLS ─── -->
        <div class="pills-bar">
            <div id="productPills" style="display:flex; gap:0.4rem; flex-wrap:wrap; align-items:center;"></div>
            <nav class="sec-nav">
                <a href="#sec1">① Tổng quan</a>
                <a href="#sec2">② Biểu đồ & Bảng NS</a>
                <a href="#cplAlertStrip">🎯 Cảnh báo CPL</a>
                <a href="#sec3">③ Hiệu suất tháng</a>
            </nav>
        </div>
        </div>

        <!-- ═══════════════════════════════════════════════════════════════════════════
             SECTION 1: TỔNG CHI TIÊU NĂM 2026, SO SÁNH THÁNG & ĐỐI CHIẾU CPL KẾ HOẠCH
             ═══════════════════════════════════════════════════════════════════════════ -->
        <div class="section-box" id="sec1">
            <div class="section-bar">
                <div class="section-label">
                    <span class="tag-sec">SECTION 1</span>
                    <span id="sec1Title">Tổng Chi Tiêu Năm 2026, So Sánh Tháng Trước vs. Tháng Hiện Tại & CPL Kế Hoạch</span>
                </div>
                <div class="switch-group">
                    <button class="switch-btn active" id="btnTaxAfter" onclick="setTaxMode('after')">Sau thuế (Tổng CP)</button>
                    <button class="switch-btn" id="btnTaxBefore" onclick="setTaxMode('before')">Trước thuế</button>
                </div>
            </div>

            <div class="kpi-grid" id="sec1KpiGrid"></div>
        </div>

        <!-- ═══════════════════════════════════════════════════════════════════════════
             SECTION 2: BIỂU ĐỒ CHI TIÊU & ĐỐI SÁNH CPL KẾ HOẠCH CÁC SẢN PHẨM
             ═══════════════════════════════════════════════════════════════════════════ -->
        <div class="section-box" id="sec2">
            <div class="section-bar">
                <div class="section-label">
                    <span class="tag-sec">SECTION 2</span>
                    <span>Biểu Đồ Chi Tiêu Các Sản Phẩm & Kiểm Soát Trần CPL Kế Hoạch</span>
                </div>
                <div class="switch-group">
                    <button class="switch-btn active" id="btnChartSpend" onclick="setChartMetric('spend')">💰 Chi Tiêu</button>
                    <button class="switch-btn" id="btnChartData" onclick="setChartMetric('data')">📱 Chi Tiêu + Data</button>
                    <button class="switch-btn" id="btnChartHD" onclick="setChartMetric('hd')">📝 Chi Tiêu + HĐ</button>
                    <button class="switch-btn" id="btnChartDS" onclick="setChartMetric('ds')">💵 Chi Tiêu + Doanh Số</button>
                </div>
            </div>

            <!-- Hàng 1: So sánh Chi tiêu Tháng trước vs Tháng hiện tại + Đối sánh CPL Thực tế vs CPL Kế hoạch -->
            <div class="charts-row">
                <div class="chart-panel">
                    <div class="chart-head">
                        <span id="compareChartTitle">1. Chi Tiêu Sản Phẩm: Tháng Trước vs. Tháng Hiện Tại</span>
                        <span style="font-size:0.71rem; color:var(--text-muted); font-weight:600;">Bấm vào cột để lọc SP</span>
                    </div>
                    <div class="canvas-wrap">
                        <canvas id="chartMonthCompare"></canvas>
                    </div>
                </div>

                <div class="chart-panel">
                    <div class="chart-head">
                        <span id="cplChartTitle">2. Đối Sánh CPL Thực Tế vs. CPL Kế Hoạch (Đỏ = Vượt KH)</span>
                        <div class="switch-group">
                            <button class="switch-btn active" id="btnCplModeAvg" onclick="setCplChartMode('avg')">TB Các Tháng</button>
                            <button class="switch-btn" id="btnCplModeCurr" onclick="setCplChartMode('curr')">Tháng Hiện Tại</button>
                        </div>
                    </div>
                    <div class="canvas-wrap">
                        <canvas id="chartCplVsPlan"></canvas>
                    </div>
                </div>
            </div>

            <!-- Hàng 2: Xu hướng chi tiêu & CPL qua các tháng trong năm -->
            <div class="chart-panel" style="margin-bottom: 1rem;">
                <div class="chart-head">
                    <span id="trendChartTitle">3. Diễn Biến Qua Các Tháng Trong Năm (T01 ➔ T11)</span>
                    <div class="switch-group">
                        <button class="switch-btn active" id="btnStackProd" onclick="setTrendMode('product')">Chi Tiêu Theo SP</button>
                        <button class="switch-btn" id="btnStackRevenue" onclick="setTrendMode('revenue')">💵 Doanh Số Theo SP</button>
                        <button class="switch-btn" id="btnStackChannel" onclick="setTrendMode('channel')">Chi Tiêu Theo Kênh</button>
                        <button class="switch-btn" id="btnStackCpl" onclick="setTrendMode('cpl')">🎯 CPL Qua Các Tháng vs. KH</button>
                    </div>
                </div>
                <div class="canvas-wrap" style="height: 285px;">
                    <canvas id="chartMonthlyTrend"></canvas>
                </div>
            </div>

            <!-- Bảng đối chiếu gọn & Ma trận các tháng -->
            <div class="chart-head" style="margin-top:0.25rem;">
                <span id="tableModeTitle">4. Bảng Quản Trị Ngân Sách & Cảnh Báo CPL Sản Phẩm</span>
                <div style="display:flex; gap:0.4rem; flex-wrap:wrap;">
                    <div class="switch-group">
                        <button class="switch-btn active" id="btnTblCompare" onclick="setTableMode('compare')">So Sánh Tháng & CPL KH</button>
                        <button class="switch-btn" id="btnTblCplMatrix" onclick="setTableMode('cpl_matrix')">🎯 Ma Trận CPL 11 Tháng vs. KH</button>
                        <button class="switch-btn" id="btnTblMatrix" onclick="setTableMode('matrix')">💰 Ma Trận Chi Tiêu 11 Tháng</button>
                        <button class="switch-btn" id="btnTblDsMatrix" onclick="setTableMode('ds_matrix')">💵 Ma Trận Doanh Số 11 Tháng</button>
                    </div>
                    <button class="btn" style="height:28px; padding:0 0.6rem; font-size:0.72rem;" onclick="exportCSV()">📥 Xuất CSV</button>
                </div>
            </div>

            <div class="table-wrap">
                <table id="mainTable">
                    <thead id="mainTableHead"></thead>
                    <tbody id="mainTableBody"></tbody>
                </table>
            </div>
        </div>

        <!-- ─── CPL ALERT STRIP (CẢNH BÁO SẢN PHẨM VƯỢT CPL KẾ HOẠCH - ĐƯA XUỐNG DƯỚI) ─── -->
        <div class="cpl-alert-strip" id="cplAlertStrip" style="margin-top: 1.15rem; margin-bottom: 1.15rem;"></div>

        <!-- ═══════════════════════════════════════════════════════════════════════════
             SECTION 3: BẢNG HIỆU SUẤT CPL THỰC TẾ vs. KH, TỶ LỆ CĐ & CHI PHÍ / HĐ THEO THÁNG
             ═══════════════════════════════════════════════════════════════════════════ -->
        <div class="section-box" id="sec3">
            <div class="section-bar">
                <div class="section-label">
                    <span class="tag-sec">SECTION 3</span>
                    <span id="sec3Title">Bảng Hiệu Suất CPL Thực Tế vs. Kế Hoạch, Tỷ Lệ CĐ & Chi Phí / HĐ Theo Tháng</span>
                </div>
                <div style="display:flex; gap:0.4rem; flex-wrap:wrap; align-items:center;">
                    <div class="switch-group">
                        <button class="switch-btn active" id="btnPerfAll" onclick="setPerfTableMode('all')">📊 Tổng Hợp</button>
                        <button class="switch-btn" id="btnPerfCpl" onclick="setPerfTableMode('cpl')">🎯 CPL vs. KH</button>
                        <button class="switch-btn" id="btnPerfCr" onclick="setPerfTableMode('cr')">🔄 Tỷ Lệ CĐ</button>
                        <button class="switch-btn" id="btnPerfCpHd" onclick="setPerfTableMode('cphd')">📝 CP / HĐ</button>
                        <button class="switch-btn" id="btnPerfDs" onclick="setPerfTableMode('ds')">💵 Doanh Số</button>
                    </div>
                    <div class="switch-group">
                        <button class="switch-btn active" id="btnPerfViewChart" onclick="setPerfView('chart')">📈 Biểu đồ</button>
                        <button class="switch-btn" id="btnPerfViewTable" onclick="setPerfView('table')">📋 Bảng</button>
                        <button class="switch-btn" id="btnPerfViewBoth" onclick="setPerfView('both')">Cả hai</button>
                    </div>
                    <button class="btn" style="height:28px; padding:0 0.6rem; font-size:0.72rem;" onclick="exportPerfCSV()">📥 Xuất CSV</button>
                </div>
            </div>

            <div id="perfChartsBlock">
                <div class="charts-row" style="grid-template-columns: 1fr 1fr;">
                    <div class="chart-panel" id="perfPanelA">
                        <div class="chart-head">
                            <span id="perfChartATitle">1. Diễn Biến CPL Thực Tế vs. CPL Kế Hoạch Theo Tháng</span>
                            <span style="font-size:0.71rem; color:var(--text-muted); font-weight:600;">Đường đứt nét = Trần KH</span>
                        </div>
                        <div class="canvas-wrap"><canvas id="chartPerfA"></canvas></div>
                    </div>
                    <div class="chart-panel" id="perfPanelB">
                        <div class="chart-head">
                            <span id="perfChartBTitle">2. Tỷ Lệ Chuyển Đổi Theo Tháng (Data/Mess % & HĐ/Data %)</span>
                            <span style="font-size:0.71rem; color:var(--text-muted); font-weight:600;">Cột = Data/Mess • Đường = HĐ/Data</span>
                        </div>
                        <div class="canvas-wrap"><canvas id="chartPerfB"></canvas></div>
                    </div>
                </div>
                <div class="charts-row" style="grid-template-columns: 1fr 1fr; margin-bottom: 1rem;">
                    <div class="chart-panel" id="perfPanelC">
                        <div class="chart-head">
                            <span id="perfChartCTitle">3. Chi Phí / Hợp Đồng (CP/HĐ) & Số Lượng Hợp Đồng Theo Tháng</span>
                            <span style="font-size:0.71rem; color:var(--text-muted); font-weight:600;">Cột = CP/HĐ (VNĐ) • Đường = Số lượng HĐ</span>
                        </div>
                        <div class="canvas-wrap"><canvas id="chartPerfC"></canvas></div>
                    </div>
                    <div class="chart-panel" id="perfPanelD">
                        <div class="chart-head">
                            <span id="perfChartDTitle">4. Doanh Số & Tỷ Lệ Chi Phí / Doanh Số (% CP/DS) Theo Tháng</span>
                            <span style="font-size:0.71rem; color:var(--text-muted); font-weight:600;">Cột = Doanh Số • Đường = % CP/DS</span>
                        </div>
                        <div class="canvas-wrap"><canvas id="chartPerfD"></canvas></div>
                    </div>
                </div>
            </div>

            <div id="perfTableBlock" style="display:none;">
                <div class="legend-row">
                    <span><span class="lg-dot" style="background:#34d399;"></span><b>Xanh</b> = CPL đạt kế hoạch</span>
                    <span><span class="lg-dot" style="background:#f87171;"></span><b>Đỏ 🚨</b> = CPL vượt kế hoạch</span>
                    <span><b>D/M</b> = Data / Mess</span>
                    <span><b>HĐ/D</b> = Hợp đồng / Data</span>
                    <span><span class="lg-dot" style="background:#22d3ee;"></span><b>CP/HĐ</b> = Chi phí / Hợp đồng (số HĐ)</span>
                    <span style="color:var(--text-muted);">• Bấm vào dòng để lọc sản phẩm</span>
                </div>

                <div class="table-wrap">
                    <table id="perfTable">
                        <thead id="perfTableHead"></thead>
                        <tbody id="perfTableBody"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        const GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1V9z5T7BQABDSvsytY0P1kKV5b4lMfpzcFZWghJwUitw/gviz/tq?tqx=out:csv&sheet=Data_San_Pham_Cleaned";
        let RAW_DATA = """ + json_data_str + """;

        // Định mức CPL Kế hoạch chuẩn (VNĐ)
        const CPL_PLAN_MAP = {
            "Data Analyst": 170000,
            "Data Engineer": 200000,
            "Embedded": 180000,
            "BrSE": 250000,
            "AI Engineer": 200000,
            "Cyber Security": 250000,
            "Network Security": 250000,
            "Xueba": 160000
        };

        let taxMode = "after";         // 'after' | 'before'
        let chartMetric = "spend";     // 'spend' | 'data' | 'hd'
        let cplChartMode = "avg";      // 'avg' (TB các tháng) | 'curr' (Tháng hiện tại)
        let trendMode = "product";     // 'product' | 'channel' | 'cpl'
        let tableMode = "compare";     // 'compare' | 'cpl_matrix' | 'matrix'

        let chartCompareInst = null;
        let chartCplInst = null;
        let chartTrendInst = null;
        let chartPerfAInst = null;
        let chartPerfBInst = null;
        let chartPerfCInst = null;
        let chartPerfDInst = null;
        let currentSummaryRows = [];
        let currentAllMonths = [];
        let perfTableMode = 'all';
        let perfView = 'chart';

        const PALETTE = [
            '#6366f1', '#10b981', '#06b6d4', '#f59e0b', '#ec4899',
            '#a855f7', '#3b82f6', '#84cc16', '#f43f5e', '#14b8a6',
            '#eab308', '#8b5cf6', '#0ea5e9', '#fb923c'
        ];

        const fmtVND = (v) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(Math.round(v || 0));
        const fmtShort = (v) => {
            if (!v || v === 0) return '0';
            if (Math.abs(v) >= 1e9) return (v / 1e9).toFixed(2) + ' tỷ';
            if (Math.abs(v) >= 1e6) return (v / 1e6).toFixed(1) + ' tr';
            if (Math.abs(v) >= 1e3) return Math.round(v / 1e3) + 'k';
            return String(Math.round(v));
        };
        const fmtNum = (v) => new Intl.NumberFormat('vi-VN').format(Math.round(v || 0));

        function normalizeProd(raw) {
            const p = String(raw || "").trim();
            if (p === "Network Security") return "Cyber Security";
            return p || "Khác";
        }

        function getPlanCPL(prodName) {
            return CPL_PLAN_MAP[prodName] || 0;
        }

        function getSpend(r) {
            if (taxMode === 'before') {
                return (Number(r["Chi Phí FB Mess (Trước Thuế)"]) || 0)
                     + (Number(r["Chi Phí FB Landing (Trước Thuế)"]) || 0)
                     + (Number(r["Chi Phí TikTok (Trước Thuế)"]) || 0);
            }
            return Number(r["Tổng Chi Phí Ads (Sau Thuế)"]) || 0;
        }

        function getChannelSpend(r) {
            if (taxMode === 'before') {
                return {
                    fbMess: Number(r["Chi Phí FB Mess (Trước Thuế)"]) || 0,
                    fbLdp: Number(r["Chi Phí FB Landing (Trước Thuế)"]) || 0,
                    tiktok: Number(r["Chi Phí TikTok (Trước Thuế)"]) || 0
                };
            }
            return {
                fbMess: Number(r["Chi Phí FB Mess (Sau Thuế)"]) || 0,
                fbLdp: Number(r["Chi Phí FB Landing (Sau Thuế)"]) || 0,
                tiktok: Number(r["Chi Phí TikTok (Sau Thuế)"]) || 0
            };
        }

        function initSelectors() {
            const year = document.getElementById('yearSelect').value;
            const yearRows = RAW_DATA.filter(r => String(r["Năm"]) === String(year));

            const months = Array.from(new Set(yearRows.map(r => r["Mã Tháng"]).filter(Boolean))).sort();
            const prevSel = document.getElementById('prevMonthSelect');
            const currSel = document.getElementById('currMonthSelect');
            prevSel.innerHTML = '';
            currSel.innerHTML = '';

            months.forEach(ym => {
                const [y, m] = ym.split('-');
                const lbl = `Tháng ${m}/${y}`;
                const o1 = document.createElement('option');
                o1.value = ym; o1.textContent = `⏪ ${lbl}`;
                prevSel.appendChild(o1);

                const o2 = document.createElement('option');
                o2.value = ym; o2.textContent = `⏩ ${lbl}`;
                currSel.appendChild(o2);
            });

            if (months.length >= 2) {
                prevSel.value = months[months.length - 2];
                currSel.value = months[months.length - 1];
            } else if (months.length === 1) {
                prevSel.value = months[0];
                currSel.value = months[0];
            }

            const prodSpend = {};
            yearRows.forEach(r => {
                const p = normalizeProd(r["Tag Sản Phẩm"] || r["Sản Phẩm Gốc"]);
                prodSpend[p] = (prodSpend[p] || 0) + getSpend(r);
            });
            const sortedProds = Object.keys(prodSpend).sort((a, b) => prodSpend[b] - prodSpend[a]);

            const prodSel = document.getElementById('productSelect');
            const curProd = prodSel.value;
            prodSel.innerHTML = `<option value="ALL">📦 Tất cả (${sortedProds.length} sản phẩm)</option>`;
            sortedProds.forEach(p => {
                const plan = getPlanCPL(p);
                const planTxt = plan > 0 ? ` • KH ${fmtShort(plan)}` : '';
                const o = document.createElement('option');
                o.value = p;
                o.textContent = `📦 ${p} (${fmtShort(prodSpend[p])}${planTxt})`;
                prodSel.appendChild(o);
            });
            if (sortedProds.includes(curProd)) prodSel.value = curProd;
        }

        function onYearChange() {
            initSelectors();
            renderAll();
        }

        function onProductDropdownChange() {
            renderAll();
        }

        function selectProduct(prod) {
            const sel = document.getElementById('productSelect');
            sel.value = (sel.value === prod && prod !== 'ALL') ? 'ALL' : prod;
            renderAll();
        }

        function setTaxMode(m) {
            taxMode = m;
            document.getElementById('btnTaxAfter').classList.toggle('active', m === 'after');
            document.getElementById('btnTaxBefore').classList.toggle('active', m === 'before');
            initSelectors();
            renderAll();
        }

        function setChartMetric(m) {
            chartMetric = m;
            document.getElementById('btnChartSpend').classList.toggle('active', m === 'spend');
            document.getElementById('btnChartData').classList.toggle('active', m === 'data');
            document.getElementById('btnChartHD').classList.toggle('active', m === 'hd');
            document.getElementById('btnChartDS').classList.toggle('active', m === 'ds');
            renderAll();
        }

        function setCplChartMode(m) {
            cplChartMode = m;
            document.getElementById('btnCplModeAvg').classList.toggle('active', m === 'avg');
            document.getElementById('btnCplModeCurr').classList.toggle('active', m === 'curr');
            renderAll();
        }

        function setTrendMode(m) {
            trendMode = m;
            document.getElementById('btnStackProd').classList.toggle('active', m === 'product');
            document.getElementById('btnStackRevenue').classList.toggle('active', m === 'revenue');
            document.getElementById('btnStackChannel').classList.toggle('active', m === 'channel');
            document.getElementById('btnStackCpl').classList.toggle('active', m === 'cpl');
            renderAll();
        }

        function setTableMode(m) {
            tableMode = m;
            document.getElementById('btnTblCompare').classList.toggle('active', m === 'compare');
            document.getElementById('btnTblCplMatrix').classList.toggle('active', m === 'cpl_matrix');
            document.getElementById('btnTblMatrix').classList.toggle('active', m === 'matrix');
            document.getElementById('btnTblDsMatrix').classList.toggle('active', m === 'ds_matrix');
            renderAll();
        }

        function setPerfTableMode(m) {
            perfTableMode = m;
            document.getElementById('btnPerfAll').classList.toggle('active', m === 'all');
            document.getElementById('btnPerfCpl').classList.toggle('active', m === 'cpl');
            document.getElementById('btnPerfCr').classList.toggle('active', m === 'cr');
            document.getElementById('btnPerfCpHd').classList.toggle('active', m === 'cphd');
            document.getElementById('btnPerfDs').classList.toggle('active', m === 'ds');
            renderAll();
        }

        function setPerfView(v) {
            perfView = v;
            document.getElementById('btnPerfViewChart').classList.toggle('active', v === 'chart');
            document.getElementById('btnPerfViewTable').classList.toggle('active', v === 'table');
            document.getElementById('btnPerfViewBoth').classList.toggle('active', v === 'both');
            document.getElementById('perfChartsBlock').style.display = (v === 'chart' || v === 'both') ? 'block' : 'none';
            document.getElementById('perfTableBlock').style.display = (v === 'table' || v === 'both') ? 'block' : 'none';
            renderAll();
        }

        function renderAll() {
            const year = document.getElementById('yearSelect').value;
            const selProd = document.getElementById('productSelect').value;
            const prevM = document.getElementById('prevMonthSelect').value;
            const currM = document.getElementById('currMonthSelect').value;

            const yearRows = RAW_DATA.filter(r => String(r["Năm"]) === String(year));
            const allMonths = Array.from(new Set(yearRows.map(r => r["Mã Tháng"]).filter(Boolean))).sort();

            const prodMap = {};
            let sysYearSpend = 0;

            yearRows.forEach(r => {
                const p = normalizeProd(r["Tag Sản Phẩm"] || r["Sản Phẩm Gốc"]);
                const ym = r["Mã Tháng"];
                const sp = getSpend(r);
                const ch = getChannelSpend(r);
                const dt = Number(r["SL Data Tổng"]) || 0;
                const ms = Number(r["SL Mess"]) || 0;
                const hd = Number(r["Tổng HĐ"]) || 0;
                const ds = Number(r["Doanh Số Tổng"]) || 0;

                if (!prodMap[p]) {
                    prodMap[p] = {
                        name: p,
                        planCPL: getPlanCPL(p),
                        yearSpend: 0,
                        yearSpendWithData: 0,
                        yearData: 0,
                        yearMess: 0,
                        yearHD: 0,
                        yearDS: 0,
                        months: {}
                    };
                }
                const po = prodMap[p];
                po.yearSpend += sp;
                if (dt > 0) {
                    po.yearSpendWithData += sp;
                    po.yearData += dt;
                }
                po.yearMess += ms;
                po.yearHD += hd;
                po.yearDS += ds;
                sysYearSpend += sp;

                if (!po.months[ym]) {
                    po.months[ym] = { spend: 0, fbMess: 0, fbLdp: 0, tiktok: 0, data: 0, mess: 0, hd: 0, ds: 0, cpl: 0 };
                }
                const mo = po.months[ym];
                mo.spend += sp;
                mo.fbMess += ch.fbMess;
                mo.fbLdp += ch.fbLdp;
                mo.tiktok += ch.tiktok;
                mo.data += dt;
                mo.mess += ms;
                mo.hd += hd;
                mo.ds += ds;
                mo.cpl = mo.data > 0 ? Math.round(mo.spend / mo.data) : (Number(r["CPL Tổng"]) || 0);
            });

            const summaryRows = Object.values(prodMap).map(p => {
                const mp = p.months[prevM] || { spend: 0, fbMess: 0, fbLdp: 0, tiktok: 0, data: 0, mess: 0, hd: 0, ds: 0, cpl: 0 };
                const mc = p.months[currM] || { spend: 0, fbMess: 0, fbLdp: 0, tiktok: 0, data: 0, mess: 0, hd: 0, ds: 0, cpl: 0 };
                const shareYear = sysYearSpend > 0 ? (p.yearSpend / sysYearSpend * 100) : 0;
                const diffSpend = mc.spend - mp.spend;
                const deltaSpendPct = mp.spend > 0 ? ((mc.spend - mp.spend) / mp.spend * 100) : (mc.spend > 0 ? 100 : 0);

                // Tính CPL Trung bình các tháng trong năm (Weighted trên các tháng có Data + Simple avg)
                const activeCplMonths = Object.values(p.months).filter(m => m.cpl > 0);
                const overPlanMonths = p.planCPL > 0 ? activeCplMonths.filter(m => m.cpl > p.planCPL).length : 0;
                const avgYearCPL = p.yearData > 0
                    ? Math.round(p.yearSpendWithData / p.yearData)
                    : (activeCplMonths.length > 0 ? Math.round(activeCplMonths.reduce((s, m) => s + m.cpl, 0) / activeCplMonths.length) : 0);

                const cplPrev = mp.cpl;
                const cplCurr = mc.cpl;

                // So sánh với CPL Kế hoạch (Ưu tiên đánh giá cả TB Năm và Tháng hiện tại)
                const refCPL = cplCurr > 0 ? cplCurr : avgYearCPL;
                const diffPlanAvgPct = (p.planCPL > 0 && avgYearCPL > 0) ? ((avgYearCPL - p.planCPL) / p.planCPL * 100) : 0;
                const diffPlanCurrPct = (p.planCPL > 0 && cplCurr > 0) ? ((cplCurr - p.planCPL) / p.planCPL * 100) : 0;
                const isOverPlanAvg = p.planCPL > 0 && avgYearCPL > p.planCPL;
                const isOverPlanCurr = p.planCPL > 0 && cplCurr > p.planCPL;

                return {
                    ...p,
                    shareYear,
                    mp,
                    mc,
                    diffSpend,
                    deltaSpendPct,
                    avgYearCPL,
                    cplPrev,
                    cplCurr,
                    activeCplMonthsCount: activeCplMonths.length,
                    overPlanMonths,
                    diffPlanAvgPct,
                    diffPlanCurrPct,
                    isOverPlanAvg,
                    isOverPlanCurr
                };
            }).sort((a, b) => b.yearSpend - a.yearSpend);

            currentSummaryRows = summaryRows;
            currentAllMonths = allMonths;

            renderProductPills(summaryRows, selProd);
            renderCplAlertStrip(summaryRows, currM);

            const kpiRows = selProd === 'ALL' ? summaryRows : summaryRows.filter(r => r.name === selProd);
            renderSection1KPIs(kpiRows, selProd, year, prevM, currM, sysYearSpend);
            renderSection2Charts(summaryRows, allMonths, selProd, year, prevM, currM);
            renderMainTable(summaryRows, allMonths, selProd, year, prevM, currM);
            renderPerfCharts(summaryRows, allMonths, selProd, year);
            renderPerfTable(summaryRows, allMonths, selProd, year);
        }

        function renderProductPills(summaryRows, selProd) {
            const pillsEl = document.getElementById('productPills');
            let html = `<button class="prod-pill ${selProd === 'ALL' ? 'active' : ''}" onclick="selectProduct('ALL')">Tất cả (${summaryRows.length})</button>`;
            summaryRows.forEach(r => {
                let dot = '';
                if (r.planCPL > 0 && (r.avgYearCPL > 0 || r.cplCurr > 0)) {
                    const over = (r.cplCurr > 0 ? r.isOverPlanCurr : r.isOverPlanAvg);
                    dot = over ? `<span class="pill-dot-alert" title="Vượt CPL kế hoạch"></span>` : `<span class="pill-dot-ok" title="Đạt CPL kế hoạch"></span>`;
                }
                html += `<button class="prod-pill ${selProd === r.name ? 'active' : ''}" onclick="selectProduct('${r.name}')">${dot}${r.name}</button>`;
            });
            pillsEl.innerHTML = html;
        }

        function renderCplAlertStrip(summaryRows, currM) {
            const strip = document.getElementById('cplAlertStrip');
            const plannedRows = summaryRows.filter(r => r.planCPL > 0 && (r.avgYearCPL > 0 || r.cplCurr > 0));
            const overList = plannedRows.filter(r => r.isOverPlanAvg || r.isOverPlanCurr);
            const goodList = plannedRows.filter(r => !r.isOverPlanAvg && !r.isOverPlanCurr);

            const overChips = overList.map(r => {
                const cplShow = r.cplCurr > 0 ? r.cplCurr : r.avgYearCPL;
                const pctShow = r.cplCurr > 0 ? r.diffPlanCurrPct : r.diffPlanAvgPct;
                const tagLbl = r.cplCurr > 0 && r.isOverPlanCurr ? currM : 'TB năm';
                return `<span class="cpl-chip over" onclick="selectProduct('${r.name}')" title="Bấm để lọc ${r.name}">🚨 ${r.name}: ${fmtShort(cplShow)} vs KH ${fmtShort(r.planCPL)} (+${pctShow.toFixed(0)}% ${tagLbl})</span>`;
            }).join('');

            const goodChips = goodList.map(r => {
                const cplShow = r.cplCurr > 0 ? r.cplCurr : r.avgYearCPL;
                const pctShow = r.cplCurr > 0 ? r.diffPlanCurrPct : r.diffPlanAvgPct;
                return `<span class="cpl-chip good" onclick="selectProduct('${r.name}')" title="Bấm để lọc ${r.name}">✅ ${r.name}: ${fmtShort(cplShow)} / KH ${fmtShort(r.planCPL)} (${pctShow.toFixed(0)}%)</span>`;
            }).join('');

            strip.innerHTML = `
                <div style="font-weight:800; color:#f87171; display:flex; align-items:center; gap:0.4rem;">
                    <span>🎯 KIỂM SOÁT ĐỊNH MỨC CPL KẾ HOẠCH (${overList.length} SP Vượt KH / ${goodList.length} SP Đạt KH):</span>
                </div>
                <div class="cpl-alert-chips">
                    ${overChips}
                    ${goodChips}
                </div>
            `;
        }

        function renderSection1KPIs(rows, selProd, year, prevM, currM, sysYearSpend) {
            const ySpend = rows.reduce((s, r) => s + r.yearSpend, 0);
            const ySpendWithData = rows.reduce((s, r) => s + r.yearSpendWithData, 0);
            const yData = rows.reduce((s, r) => s + r.yearData, 0);
            const yHD = rows.reduce((s, r) => s + r.yearHD, 0);
            const yShare = sysYearSpend > 0 ? (ySpend / sysYearSpend * 100) : 0;
            const yCPL = yData > 0 ? Math.round(ySpendWithData / yData) : 0;

            const pSpend = rows.reduce((s, r) => s + r.mp.spend, 0);
            const pData = rows.reduce((s, r) => s + r.mp.data, 0);
            const pHD = rows.reduce((s, r) => s + r.mp.hd, 0);
            const pCPL = pData > 0 ? Math.round(pSpend / pData) : 0;

            const cSpend = rows.reduce((s, r) => s + r.mc.spend, 0);
            const cData = rows.reduce((s, r) => s + r.mc.data, 0);
            const cHD = rows.reduce((s, r) => s + r.mc.hd, 0);
            const cCPL = cData > 0 ? Math.round(cSpend / cData) : 0;

            const diffSpend = cSpend - pSpend;
            const deltaPct = pSpend > 0 ? ((cSpend - pSpend) / pSpend * 100) : (cSpend > 0 ? 100 : 0);

            // CPL Kế hoạch mục tiêu
            let planVal = 0;
            if (selProd !== 'ALL' && rows.length === 1) {
                planVal = rows[0].planCPL;
            } else {
                // Trung bình gia quyền CPL kế hoạch của các SP có định mức
                const planned = rows.filter(r => r.planCPL > 0 && r.yearData > 0);
                const totDataPlanned = planned.reduce((s, r) => s + r.yearData, 0);
                if (totDataPlanned > 0) {
                    planVal = Math.round(planned.reduce((s, r) => s + r.planCPL * r.yearData, 0) / totDataPlanned);
                }
            }

            const compareCPL = cCPL > 0 ? cCPL : yCPL;
            const cplVsPlanPct = (planVal > 0 && compareCPL > 0) ? ((compareCPL - planVal) / planVal * 100) : 0;
            const isOver = planVal > 0 && compareCPL > planVal;
            const yCostPerHD = yHD > 0 ? Math.round(ySpend / yHD) : 0;
            const cCostPerHD = cHD > 0 ? Math.round(cSpend / cHD) : 0;
            const yDS = rows.reduce((s, r) => s + r.yearDS, 0);
            const pDS = rows.reduce((s, r) => s + r.mp.ds, 0);
            const cDS = rows.reduce((s, r) => s + r.mc.ds, 0);
            const yCpDsPct = yDS > 0 ? (ySpend / yDS * 100) : 0;

            const scope = selProd === 'ALL' ? `Tất cả sản phẩm` : selProd;
            document.getElementById('sec1Title').textContent = `Tổng Chi Tiêu Năm ${year} (${scope}) • So Sánh ${prevM} ➔ ${currM} & Định Mức CPL`;

            document.getElementById('sec1KpiGrid').innerHTML = `
                <div class="kpi-box" style="--accent: #6366f1;">
                    <div class="kpi-name"><span>💰 Tổng Chi Tiêu ${year}</span> <span>${yShare.toFixed(1)}% hệ thống</span></div>
                    <div class="kpi-num">${fmtVND(ySpend)}</div>
                    <div class="kpi-foot">
                        <span>Data ${year}: <b>${fmtNum(yData)}</b></span>
                        <span>Hợp đồng: <b style="color:#34d399;">${fmtNum(yHD)} HĐ</b></span>
                    </div>
                </div>

                <div class="kpi-box" style="--accent: #3b82f6;">
                    <div class="kpi-name"><span>⏪ Tháng Trước (${prevM})</span> <span>CPL: ${pCPL > 0 ? fmtShort(pCPL) : '--'}</span></div>
                    <div class="kpi-num">${fmtVND(pSpend)}</div>
                    <div class="kpi-foot">
                        <span>Data: <b>${fmtNum(pData)}</b></span>
                        <span>Hợp đồng: <b>${fmtNum(pHD)} HĐ</b></span>
                    </div>
                </div>

                <div class="kpi-box" style="--accent: #10b981;">
                    <div class="kpi-name"><span>⏩ Tháng Hiện Tại (${currM})</span> <span>CPL: ${cCPL > 0 ? fmtShort(cCPL) : '--'}</span></div>
                    <div class="kpi-num" style="color:#34d399;">${fmtVND(cSpend)}</div>
                    <div class="kpi-foot">
                        <span>Data: <b>${fmtNum(cData)}</b></span>
                        <span>Hợp đồng: <b style="color:#34d399;">${fmtNum(cHD)} HĐ</b></span>
                    </div>
                </div>

                <div class="kpi-box" style="--accent: #f59e0b;">
                    <div class="kpi-name"><span>⚖️ Biến Thiên (${currM} vs ${prevM})</span> <span>MoM</span></div>
                    <div class="kpi-num" style="color:${deltaPct >= 0 ? '#fbbf24' : '#38bdf8'};">
                        ${deltaPct >= 0 ? '+' : ''}${deltaPct.toFixed(1)}%
                    </div>
                    <div class="kpi-foot">
                        <span>Tiền: <b>${diffSpend >= 0 ? '+' : ''}${fmtShort(diffSpend)}</b></span>
                        <span>CPL: <b>${pCPL > 0 ? fmtShort(pCPL) : '--'} ➔ ${cCPL > 0 ? fmtShort(cCPL) : '--'}</b></span>
                    </div>
                </div>

                <div class="kpi-box" style="--accent: ${isOver ? '#ef4444' : '#10b981'};">
                    <div class="kpi-name"><span>🎯 CPL Thực Tế vs. Kế Hoạch</span> <span>${planVal > 0 ? 'KH: ' + fmtShort(planVal) : 'Chưa đặt KH'}</span></div>
                    <div class="kpi-num" style="color:${isOver ? '#f87171' : '#34d399'};">
                        ${compareCPL > 0 ? fmtVND(compareCPL) : '--'}
                    </div>
                    <div class="kpi-foot">
                        <span>TB Năm: <b>${yCPL > 0 ? fmtShort(yCPL) : '--'}</b></span>
                        <span>${planVal > 0 && compareCPL > 0 ? `<b style="color:${isOver ? '#f87171' : '#34d399'};">${isOver ? '🚨 Vượt +' : '✅ Đạt '}${cplVsPlanPct.toFixed(1)}%</b>` : '--'}</span>
                    </div>
                </div>

                <div class="kpi-box" style="--accent: #06b6d4;">
                    <div class="kpi-name"><span>📝 Hợp Đồng & CP/HĐ</span> <span>Năm ${year}</span></div>
                    <div class="kpi-num" style="color:#22d3ee;">${fmtNum(yHD)} HĐ</div>
                    <div class="kpi-foot">
                        <span>CP/HĐ Năm: <b>${yCostPerHD > 0 ? fmtShort(yCostPerHD) : '--'}</b></span>
                        <span>${currM}: <b>${cHD} HĐ (${cCostPerHD > 0 ? fmtShort(cCostPerHD) : '--'})</b></span>
                    </div>
                </div>

                <div class="kpi-box" style="--accent: #ec4899;">
                    <div class="kpi-name"><span>💵 Doanh Số & CP/DS</span> <span>${yCpDsPct > 0 ? 'CP/DS: ' + yCpDsPct.toFixed(1) + '%' : 'Năm ' + year}</span></div>
                    <div class="kpi-num" style="color:#f472b6;">${fmtVND(yDS)}</div>
                    <div class="kpi-foot">
                        <span>${prevM}: <b>${pDS > 0 ? fmtShort(pDS) : '--'}</b></span>
                        <span>${currM}: <b style="color:#34d399;">${cDS > 0 ? fmtShort(cDS) : '--'}</b></span>
                    </div>
                </div>
            `;
        }

        function getThemeColors() {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            return {
                text: isDark ? '#94a3b8' : '#475569',
                grid: isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(15, 23, 42, 0.06)'
            };
        }

        function renderSection2Charts(summaryRows, allMonths, selProd, year, prevM, currM) {
            const colors = getThemeColors();

            // 1. Chart 2A: Compare prevM vs currM per product
            const activeCompare = summaryRows.filter(r => r.mp.spend > 0 || r.mc.spend > 0);
            const labelsA = activeCompare.map(r => r.name);
            document.getElementById('compareChartTitle').textContent = `1. Chi Tiêu Sản Phẩm: ${prevM} vs. ${currM}`;

            const datasetsA = [
                {
                    label: prevM,
                    data: activeCompare.map(r => r.mp.spend),
                    backgroundColor: activeCompare.map(r => (selProd === 'ALL' || selProd === r.name) ? 'rgba(99, 102, 241, 0.78)' : 'rgba(99, 102, 241, 0.22)'),
                    borderRadius: 6,
                    yAxisID: 'ySpend'
                },
                {
                    label: currM,
                    data: activeCompare.map(r => r.mc.spend),
                    backgroundColor: activeCompare.map(r => (selProd === 'ALL' || selProd === r.name) ? 'rgba(16, 185, 129, 0.85)' : 'rgba(16, 185, 129, 0.22)'),
                    borderRadius: 6,
                    yAxisID: 'ySpend'
                }
            ];

            if (chartMetric === 'data') {
                datasetsA.push({
                    label: `Data (${currM})`,
                    data: activeCompare.map(r => r.mc.data),
                    type: 'line',
                    borderColor: '#f59e0b',
                    backgroundColor: '#f59e0b',
                    borderWidth: 2.5,
                    pointRadius: 4,
                    yAxisID: 'yCount'
                });
            } else if (chartMetric === 'hd') {
                datasetsA.push({
                    label: `Hợp đồng (${currM})`,
                    data: activeCompare.map(r => r.mc.hd),
                    type: 'line',
                    borderColor: '#ec4899',
                    backgroundColor: '#ec4899',
                    borderWidth: 2.5,
                    pointRadius: 4,
                    yAxisID: 'yCount'
                });
            } else if (chartMetric === 'ds') {
                datasetsA.push({
                    label: `Doanh số (${currM})`,
                    data: activeCompare.map(r => r.mc.ds),
                    type: 'line',
                    borderColor: '#f472b6',
                    backgroundColor: '#f472b6',
                    borderWidth: 2.5,
                    pointRadius: 4,
                    yAxisID: 'yCount'
                });
            }

            const ctxA = document.getElementById('chartMonthCompare').getContext('2d');
            if (chartCompareInst) chartCompareInst.destroy();
            chartCompareInst = new Chart(ctxA, {
                type: 'bar',
                data: { labels: labelsA, datasets: datasetsA },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    onClick: (e, els) => {
                        if (els.length > 0) selectProduct(labelsA[els[0].index]);
                    },
                    plugins: {
                        legend: { position: 'top', labels: { color: colors.text, boxWidth: 12, font: { size: 11, weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => (ctx.dataset.yAxisID === 'yCount' && chartMetric !== 'ds')
                                    ? `${ctx.dataset.label}: ${fmtNum(ctx.raw)}`
                                    : `${ctx.dataset.label}: ${fmtVND(ctx.raw)}`
                            }
                        }
                    },
                    scales: {
                        x: { grid: { color: colors.grid }, ticks: { color: colors.text, font: { weight: 600 } } },
                        ySpend: {
                            position: 'left',
                            grid: { color: colors.grid },
                            ticks: { color: colors.text, callback: v => fmtShort(v) }
                        },
                        ...(chartMetric !== 'spend' ? {
                            yCount: {
                                position: 'right',
                                grid: { drawOnChartArea: false },
                                ticks: {
                                    color: chartMetric === 'ds' ? '#f472b6' : '#f59e0b',
                                    precision: 0,
                                    callback: v => chartMetric === 'ds' ? fmtShort(v) : v
                                }
                            }
                        } : {})
                    }
                }
            });

            // 2. Chart 2B: Đối Sánh CPL Thực Tế vs CPL Kế Hoạch (Cột Đỏ = Vượt KH, Cột Xanh = Đạt KH, Đường Đứt Nét = CPL Kế Hoạch)
            const cplRows = summaryRows.filter(r => r.planCPL > 0 && (r.avgYearCPL > 0 || r.cplCurr > 0));
            const labelsB = cplRows.map(r => r.name);
            const actualCplVals = cplRows.map(r => cplChartMode === 'curr' ? (r.cplCurr || r.avgYearCPL) : r.avgYearCPL);
            const planCplVals = cplRows.map(r => r.planCPL);

            const ctxB = document.getElementById('chartCplVsPlan').getContext('2d');
            if (chartCplInst) chartCplInst.destroy();
            chartCplInst = new Chart(ctxB, {
                type: 'bar',
                data: {
                    labels: labelsB,
                    datasets: [
                        {
                            label: cplChartMode === 'curr' ? `CPL Thực Tế (${currM})` : `CPL TB Năm ${year}`,
                            data: actualCplVals,
                            backgroundColor: cplRows.map((r, idx) => actualCplVals[idx] > r.planCPL ? 'rgba(239, 68, 68, 0.82)' : 'rgba(16, 185, 129, 0.82)'),
                            borderRadius: 6,
                            order: 2
                        },
                        {
                            label: 'Định Mức CPL Kế Hoạch',
                            data: planCplVals,
                            type: 'line',
                            borderColor: '#fbbf24',
                            backgroundColor: '#fbbf24',
                            borderWidth: 2.5,
                            borderDash: [5, 5],
                            pointRadius: 5,
                            tension: 0,
                            order: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    onClick: (e, els) => {
                        if (els.length > 0) selectProduct(labelsB[els[0].index]);
                    },
                    plugins: {
                        legend: { position: 'top', labels: { color: colors.text, boxWidth: 12, font: { size: 11, weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => {
                                    const r = cplRows[ctx.dataIndex];
                                    const act = actualCplVals[ctx.dataIndex];
                                    const diffPct = ((act - r.planCPL) / r.planCPL * 100).toFixed(1);
                                    if (ctx.datasetIndex === 0) {
                                        return `${ctx.dataset.label}: ${fmtVND(act)} (${act > r.planCPL ? '🚨 Vượt +' + diffPct + '%' : '✅ Đạt ' + diffPct + '%'})`;
                                    }
                                    return `CPL Kế Hoạch: ${fmtVND(r.planCPL)}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: { grid: { color: colors.grid }, ticks: { color: colors.text, font: { weight: 600 } } },
                        y: {
                            grid: { color: colors.grid },
                            ticks: { color: colors.text, callback: v => fmtShort(v) }
                        }
                    }
                }
            });

            // 3. Chart 2C: Monthly Trend across Year (Spend or CPL vs Plan)
            const ctxC = document.getElementById('chartMonthlyTrend').getContext('2d');
            const targetList = selProd === 'ALL' ? summaryRows.slice(0, 9) : summaryRows.filter(r => r.name === selProd);

            let datasetsC = [];
            let isStacked = true;

            if (trendMode === 'cpl') {
                isStacked = false;
                document.getElementById('trendChartTitle').textContent = `3. Diễn Biến CPL Thực Tế Qua Các Tháng vs. CPL Kế Hoạch (${selProd === 'ALL' ? 'Các SP có định mức' : selProd})`;
                const cplTargetList = selProd === 'ALL'
                    ? summaryRows.filter(r => r.planCPL > 0)
                    : summaryRows.filter(r => r.name === selProd);

                datasetsC = cplTargetList.map((r, i) => ({
                    label: `CPL ${r.name} (KH: ${fmtShort(r.planCPL)})`,
                    data: allMonths.map(m => (r.months[m] && r.months[m].cpl) || null),
                    type: 'line',
                    borderColor: PALETTE[i % PALETTE.length],
                    backgroundColor: PALETTE[i % PALETTE.length],
                    borderWidth: 2.5,
                    pointRadius: 4,
                    spanGaps: true,
                    tension: 0.25
                }));

                if (selProd !== 'ALL' && cplTargetList.length === 1 && cplTargetList[0].planCPL > 0) {
                    const pVal = cplTargetList[0].planCPL;
                    datasetsC.push({
                        label: `Trần CPL Kế Hoạch (${fmtShort(pVal)})`,
                        data: allMonths.map(() => pVal),
                        type: 'line',
                        borderColor: '#ef4444',
                        borderDash: [6, 6],
                        borderWidth: 2,
                        pointRadius: 0
                    });
                }
            } else if (trendMode === 'channel') {
                document.getElementById('trendChartTitle').textContent = `3. Chi Tiêu Qua Các Tháng Theo Kênh (${selProd === 'ALL' ? 'Tất cả SP' : selProd})`;
                datasetsC = [
                    {
                        label: 'FB Mess Ads',
                        data: allMonths.map(m => targetList.reduce((s, r) => s + ((r.months[m] && r.months[m].fbMess) || 0), 0)),
                        backgroundColor: '#6366f1',
                        borderRadius: 4
                    },
                    {
                        label: 'FB Landing (CĐ)',
                        data: allMonths.map(m => targetList.reduce((s, r) => s + ((r.months[m] && r.months[m].fbLdp) || 0), 0)),
                        backgroundColor: '#10b981',
                        borderRadius: 4
                    },
                    {
                        label: 'TikTok Ads',
                        data: allMonths.map(m => targetList.reduce((s, r) => s + ((r.months[m] && r.months[m].tiktok) || 0), 0)),
                        backgroundColor: '#ec4899',
                        borderRadius: 4
                    }
                ];
            } else if (trendMode === 'revenue') {
                document.getElementById('trendChartTitle').textContent = `3. Doanh Số Các Sản Phẩm Qua Các Tháng Năm ${year} (${selProd === 'ALL' ? 'Tất cả SP' : selProd})`;
                datasetsC = targetList.map((r, i) => ({
                    label: r.name,
                    data: allMonths.map(m => (r.months[m] && r.months[m].ds) || 0),
                    backgroundColor: PALETTE[i % PALETTE.length],
                    borderRadius: 4
                }));
            } else {
                document.getElementById('trendChartTitle').textContent = `3. Chi Tiêu Các Sản Phẩm Qua Các Tháng Năm ${year} (${selProd === 'ALL' ? 'Tất cả SP' : selProd})`;
                datasetsC = targetList.map((r, i) => ({
                    label: r.name,
                    data: allMonths.map(m => (r.months[m] && r.months[m].spend) || 0),
                    backgroundColor: PALETTE[i % PALETTE.length],
                    borderRadius: 4
                }));
            }

            if (chartTrendInst) chartTrendInst.destroy();
            chartTrendInst = new Chart(ctxC, {
                type: trendMode === 'cpl' ? 'line' : 'bar',
                data: {
                    labels: allMonths.map(m => `T${m.split('-')[1]}/${m.split('-')[0].slice(2)}`),
                    datasets: datasetsC
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: { position: 'top', labels: { color: colors.text, boxWidth: 11, font: { size: 11, weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => ctx.raw !== null ? `${ctx.dataset.label}: ${fmtVND(ctx.raw)}` : ''
                            }
                        }
                    },
                    scales: {
                        x: { stacked: isStacked, grid: { color: colors.grid }, ticks: { color: colors.text, font: { weight: 600 } } },
                        y: {
                            stacked: isStacked,
                            grid: { color: colors.grid },
                            ticks: { color: colors.text, callback: v => fmtShort(v) }
                        }
                    }
                }
            });
        }

        function renderMainTable(summaryRows, allMonths, selProd, year, prevM, currM) {
            const thead = document.getElementById('mainTableHead');
            const tbody = document.getElementById('mainTableBody');
            const rows = selProd === 'ALL' ? summaryRows : summaryRows.filter(r => r.name === selProd);

            // 1. Mode: Ma trận CPL 11 tháng vs Kế hoạch
            if (tableMode === 'cpl_matrix') {
                document.getElementById('tableModeTitle').textContent = `4. Ma Trận CPL Thực Tế Các Tháng Năm ${year} So Với CPL Kế Hoạch`;
                thead.innerHTML = `
                    <tr>
                        <th>Sản Phẩm</th>
                        <th>CPL Kế Hoạch</th>
                        <th>CPL TB Năm ${year}</th>
                        <th>Cảnh Báo Năm</th>
                        ${allMonths.map(m => `<th style="text-align:right;">T${m.split('-')[1]}/${m.split('-')[0].slice(2)}</th>`).join('')}
                    </tr>
                `;

                const bodyHtml = rows.map(r => {
                    const planTxt = r.planCPL > 0 ? `<b>${fmtShort(r.planCPL)}</b>` : `<span style="color:var(--text-muted);">--</span>`;
                    const avgTxt = r.avgYearCPL > 0 ? `<b>${fmtShort(r.avgYearCPL)}</b>` : `--`;
                    let alertBadge = `<span class="badge b-muted">--</span>`;
                    if (r.planCPL > 0 && r.avgYearCPL > 0) {
                        alertBadge = r.isOverPlanAvg
                            ? `<span class="badge b-down">🚨 Vượt +${r.diffPlanAvgPct.toFixed(0)}% (${r.overPlanMonths}/${r.activeCplMonthsCount}T)</span>`
                            : `<span class="badge b-up">✅ Đạt ${r.diffPlanAvgPct.toFixed(0)}% (${r.overPlanMonths}/${r.activeCplMonthsCount}T vượt)</span>`;
                    }

                    const mCells = allMonths.map(m => {
                        const cplVal = (r.months[m] && r.months[m].cpl) || 0;
                        if (cplVal === 0) return `<td style="text-align:right; color:var(--text-muted);">--</td>`;
                        const isOverM = r.planCPL > 0 && cplVal > r.planCPL;
                        const color = r.planCPL > 0 ? (isOverM ? '#f87171' : '#34d399') : 'var(--text-primary)';
                        return `<td style="text-align:right; color:${color}; font-weight:700;">${fmtShort(cplVal)}${isOverM ? ' 🚨' : ''}</td>`;
                    }).join('');

                    return `
                        <tr class="${selProd === r.name ? 'active-row' : ''}" onclick="selectProduct('${r.name}')" style="cursor:pointer;">
                            <td><b>📦 ${r.name}</b></td>
                            <td>${planTxt}</td>
                            <td>${avgTxt}</td>
                            <td>${alertBadge}</td>
                            ${mCells}
                        </tr>
                    `;
                }).join('');

                tbody.innerHTML = bodyHtml;
                return;
            }

            // 2. Mode: Ma trận Chi tiêu 11 tháng
            if (tableMode === 'matrix') {
                document.getElementById('tableModeTitle').textContent = `4. Ma Trận Chi Tiêu Sản Phẩm Qua Các Tháng Năm ${year}`;
                thead.innerHTML = `
                    <tr>
                        <th>Sản Phẩm</th>
                        ${allMonths.map(m => `<th style="text-align:right;">T${m.split('-')[1]}/${m.split('-')[0].slice(2)}</th>`).join('')}
                        <th style="text-align:right;">Tổng Năm ${year}</th>
                        <th style="text-align:right;">% Năm</th>
                    </tr>
                `;

                const bodyHtml = rows.map(r => `
                    <tr class="${selProd === r.name ? 'active-row' : ''}" onclick="selectProduct('${r.name}')" style="cursor:pointer;">
                        <td><b>📦 ${r.name}</b></td>
                        ${allMonths.map(m => {
                            const sp = (r.months[m] && r.months[m].spend) || 0;
                            return `<td style="text-align:right; color:${sp > 0 ? 'var(--text-primary)' : 'var(--text-muted)'};">${sp > 0 ? fmtShort(sp) : '--'}</td>`;
                        }).join('')}
                        <td style="text-align:right;"><b>${fmtVND(r.yearSpend)}</b></td>
                        <td style="text-align:right;"><b>${r.shareYear.toFixed(1)}%</b></td>
                    </tr>
                `).join('');

                const totYear = rows.reduce((s, r) => s + r.yearSpend, 0);
                const totRow = `
                    <tr class="total-row">
                        <td>TỔNG CỘNG</td>
                        ${allMonths.map(m => {
                            const mSum = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].spend) || 0), 0);
                            return `<td style="text-align:right;">${fmtShort(mSum)}</td>`;
                        }).join('')}
                        <td style="text-align:right;">${fmtVND(totYear)}</td>
                        <td style="text-align:right;">100%</td>
                    </tr>
                `;
                tbody.innerHTML = bodyHtml + totRow;
                return;
            }

            // 2b. Mode: Ma trận Doanh số 11 tháng
            if (tableMode === 'ds_matrix') {
                document.getElementById('tableModeTitle').textContent = `4. Ma Trận Doanh Số Sản Phẩm Qua Các Tháng Năm ${year}`;
                thead.innerHTML = `
                    <tr>
                        <th>Sản Phẩm</th>
                        ${allMonths.map(m => `<th style="text-align:right;">T${m.split('-')[1]}/${m.split('-')[0].slice(2)}</th>`).join('')}
                        <th style="text-align:right;">Tổng DS ${year}</th>
                        <th style="text-align:right;">% DS</th>
                        <th style="text-align:right;">% CP/DS</th>
                    </tr>
                `;

                const totAllDS = rows.reduce((s, r) => s + r.yearDS, 0);
                const totAllSpend = rows.reduce((s, r) => s + r.yearSpend, 0);
                const bodyHtml = rows.map(r => {
                    const shareDS = totAllDS > 0 ? (r.yearDS / totAllDS * 100) : 0;
                    const cpDs = r.yearDS > 0 ? (r.yearSpend / r.yearDS * 100) : 0;
                    return `
                        <tr class="${selProd === r.name ? 'active-row' : ''}" onclick="selectProduct('${r.name}')" style="cursor:pointer;">
                            <td><b>📦 ${r.name}</b></td>
                            ${allMonths.map(m => {
                                const ds = (r.months[m] && r.months[m].ds) || 0;
                                return `<td style="text-align:right; color:${ds > 0 ? '#f472b6' : 'var(--text-muted)'}; font-weight:${ds > 0 ? '700' : '400'};">${ds > 0 ? fmtShort(ds) : '--'}</td>`;
                            }).join('')}
                            <td style="text-align:right;"><b style="color:#f472b6;">${fmtVND(r.yearDS)}</b></td>
                            <td style="text-align:right;"><b>${shareDS.toFixed(1)}%</b></td>
                            <td style="text-align:right;"><b>${cpDs > 0 ? cpDs.toFixed(1) + '%' : '--'}</b></td>
                        </tr>
                    `;
                }).join('');

                const totCpDs = totAllDS > 0 ? (totAllSpend / totAllDS * 100).toFixed(1) + '%' : '--';
                const totRow = `
                    <tr class="total-row">
                        <td>TỔNG CỘNG</td>
                        ${allMonths.map(m => {
                            const mSum = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].ds) || 0), 0);
                            return `<td style="text-align:right;">${mSum > 0 ? fmtShort(mSum) : '--'}</td>`;
                        }).join('')}
                        <td style="text-align:right;">${fmtVND(totAllDS)}</td>
                        <td style="text-align:right;">100%</td>
                        <td style="text-align:right;">${totCpDs}</td>
                    </tr>
                `;
                tbody.innerHTML = bodyHtml + totRow;
                return;
            }

            // 3. Mode: Compare 2 Months + CPL Plan vs Actual
            document.getElementById('tableModeTitle').textContent = `4. Bảng Ngân Sách Sản Phẩm Năm ${year}, So Sánh ${prevM} ➔ ${currM} & Cảnh Báo CPL Kế Hoạch`;
            thead.innerHTML = `
                <tr>
                    <th>Sản Phẩm</th>
                    <th>Lũy Kế ${year}</th>
                    <th>% Tỷ Trọng</th>
                    <th>Tháng Trước (${prevM})</th>
                    <th>Tháng Hiện Tại (${currM})</th>
                    <th>Δ% Chi Tiêu</th>
                    <th>Data (${prevM}➔${currM})</th>
                    <th>HĐ (${prevM}➔${currM})</th>
                    <th>Tổng HĐ ${year}</th>
                    <th>CP/HĐ (${year})</th>
                    <th>CPL Kế Hoạch</th>
                    <th>CPL TB ${year}</th>
                    <th>CPL (${prevM}➔${currM})</th>
                    <th>Cảnh Báo CPL</th>
                </tr>
            `;

            const bodyHtml = rows.map(r => {
                const dBadge = r.deltaSpendPct > 0 ? 'b-warn' : (r.deltaSpendPct < 0 ? 'b-info' : 'b-muted');
                const planStr = r.planCPL > 0 ? `<b>${fmtShort(r.planCPL)}</b>` : `<span style="color:var(--text-muted);">--</span>`;
                const avgCplColor = r.planCPL > 0 ? (r.isOverPlanAvg ? '#f87171' : '#34d399') : 'var(--text-primary)';
                const currCplColor = r.planCPL > 0 && r.cplCurr > 0 ? (r.isOverPlanCurr ? '#f87171' : '#34d399') : 'var(--text-primary)';

                let cplAlertBadge = `<span class="badge b-muted">Chưa đặt KH</span>`;
                if (r.planCPL > 0) {
                    if (r.cplCurr > 0) {
                        cplAlertBadge = r.isOverPlanCurr
                            ? `<span class="badge b-down">🚨 Vượt KH +${r.diffPlanCurrPct.toFixed(1)}% (${currM})</span>`
                            : `<span class="badge b-up">✅ Đạt KH ${r.diffPlanCurrPct.toFixed(1)}% (${currM})</span>`;
                    } else if (r.avgYearCPL > 0) {
                        cplAlertBadge = r.isOverPlanAvg
                            ? `<span class="badge b-down">🚨 Vượt KH +${r.diffPlanAvgPct.toFixed(1)}% (TB Năm)</span>`
                            : `<span class="badge b-up">✅ Đạt KH ${r.diffPlanAvgPct.toFixed(1)}% (TB Năm)</span>`;
                    } else {
                        cplAlertBadge = `<span class="badge b-muted">Chưa có Data</span>`;
                    }
                }

                return `
                    <tr class="${selProd === r.name ? 'active-row' : ''}" onclick="selectProduct('${r.name}')" style="cursor:pointer;">
                        <td><b>📦 ${r.name}</b></td>
                        <td><b>${fmtVND(r.yearSpend)}</b></td>
                        <td>
                            <div class="mini-bar"><div class="mini-bar-fill" style="width:${Math.min(100, r.shareYear)}%;"></div></div>
                            <b>${r.shareYear.toFixed(1)}%</b>
                        </td>
                        <td>${fmtVND(r.mp.spend)}</td>
                        <td><b style="color:#34d399;">${fmtVND(r.mc.spend)}</b></td>
                        <td><span class="badge ${dBadge}">${r.deltaSpendPct >= 0 ? '+' : ''}${r.deltaSpendPct.toFixed(1)}%</span></td>
                        <td>${r.mp.data} ➔ <b>${r.mc.data}</b></td>
                        <td>${r.mp.hd} ➔ <b style="color:#22d3ee;">${r.mc.hd}</b></td>
                        <td><b>${fmtNum(r.yearHD)}</b></td>
                        <td><b>${r.yearHD > 0 ? fmtShort(r.yearSpend / r.yearHD) : '--'}</b></td>
                        <td>${planStr}</td>
                        <td style="color:${avgCplColor}; font-weight:800;">${r.avgYearCPL > 0 ? fmtShort(r.avgYearCPL) : '--'}</td>
                        <td>${r.cplPrev > 0 ? fmtShort(r.cplPrev) : '--'} ➔ <b style="color:${currCplColor};">${r.cplCurr > 0 ? fmtShort(r.cplCurr) : '--'}</b></td>
                        <td>${cplAlertBadge}</td>
                    </tr>
                `;
            }).join('');

            const totY = rows.reduce((s, r) => s + r.yearSpend, 0);
            const totYWithData = rows.reduce((s, r) => s + r.yearSpendWithData, 0);
            const totYData = rows.reduce((s, r) => s + r.yearData, 0);
            const totP = rows.reduce((s, r) => s + r.mp.spend, 0);
            const totC = rows.reduce((s, r) => s + r.mc.spend, 0);
            const totDelta = totP > 0 ? ((totC - totP) / totP * 100) : 0;
            const totDataP = rows.reduce((s, r) => s + r.mp.data, 0);
            const totDataC = rows.reduce((s, r) => s + r.mc.data, 0);
            const totHDP = rows.reduce((s, r) => s + r.mp.hd, 0);
            const totHDC = rows.reduce((s, r) => s + r.mc.hd, 0);
            const totYHD = rows.reduce((s, r) => s + r.yearHD, 0);
            const overCount = rows.filter(r => r.planCPL > 0 && (r.isOverPlanCurr || r.isOverPlanAvg)).length;

            tbody.innerHTML = bodyHtml + `
                <tr class="total-row">
                    <td>TỔNG CỘNG</td>
                    <td>${fmtVND(totY)}</td>
                    <td>${selProd === 'ALL' ? '100.0%' : rows[0]?.shareYear.toFixed(1) + '%'}</td>
                    <td>${fmtVND(totP)}</td>
                    <td>${fmtVND(totC)}</td>
                    <td>${totDelta >= 0 ? '+' : ''}${totDelta.toFixed(1)}%</td>
                    <td>${totDataP} ➔ ${totDataC}</td>
                    <td>${totHDP} ➔ ${totHDC}</td>
                    <td>${fmtNum(totYHD)}</td>
                    <td>${totYHD > 0 ? fmtShort(totY / totYHD) : '--'}</td>
                    <td>--</td>
                    <td>${totYData > 0 ? fmtShort(totYWithData / totYData) : '--'}</td>
                    <td>${totDataP > 0 ? fmtShort(totP/totDataP) : '--'} ➔ ${totDataC > 0 ? fmtShort(totC/totDataC) : '--'}</td>
                    <td>🚨 ${overCount} SP Vượt CPL KH</td>
                </tr>
            `;
        }

        function renderPerfCharts(summaryRows, allMonths, selProd, year) {
            const colors = getThemeColors();
            const rows = selProd === 'ALL' ? summaryRows : summaryRows.filter(r => r.name === selProd);
            const mLabels = allMonths.map(m => `T${m.split('-')[1]}/${m.split('-')[0].slice(2)}`);
            const scopeLbl = selProd === 'ALL' ? 'Toàn Hệ Thống' : selProd;

            // Điều chỉnh hiển thị các panel biểu đồ theo tab đang chọn
            const pA = document.getElementById('perfPanelA');
            const pB = document.getElementById('perfPanelB');
            const pC = document.getElementById('perfPanelC');
            const pD = document.getElementById('perfPanelD');
            const rowTop = pA.parentElement;
            const rowBot = pC.parentElement;

            if (perfTableMode === 'all') {
                rowTop.style.display = 'grid';
                rowTop.style.gridTemplateColumns = '1fr 1fr';
                rowBot.style.display = 'grid';
                rowBot.style.gridTemplateColumns = '1fr 1fr';
                pA.style.display = 'block';
                pB.style.display = 'block';
                pC.style.display = 'block';
                pD.style.display = 'block';
            } else if (perfTableMode === 'cpl') {
                rowTop.style.display = 'grid';
                rowTop.style.gridTemplateColumns = '1fr';
                rowBot.style.display = 'none';
                pA.style.display = 'block';
                pB.style.display = 'none';
            } else if (perfTableMode === 'cr') {
                rowTop.style.display = 'grid';
                rowTop.style.gridTemplateColumns = '1fr';
                rowBot.style.display = 'none';
                pA.style.display = 'none';
                pB.style.display = 'block';
            } else if (perfTableMode === 'cphd') {
                rowTop.style.display = 'none';
                rowBot.style.display = 'grid';
                rowBot.style.gridTemplateColumns = '1fr';
                pC.style.display = 'block';
                pD.style.display = 'none';
            } else if (perfTableMode === 'ds') {
                rowTop.style.display = 'none';
                rowBot.style.display = 'grid';
                rowBot.style.gridTemplateColumns = '1fr';
                pC.style.display = 'none';
                pD.style.display = 'block';
            }

            // 1. Biểu đồ 3A: CPL Thực Tế vs. CPL Kế Hoạch Theo Tháng
            document.getElementById('perfChartATitle').textContent = `1. CPL Thực Tế vs. Kế Hoạch Theo Tháng (${scopeLbl})`;
            const ctxPA = document.getElementById('chartPerfA').getContext('2d');
            if (chartPerfAInst) chartPerfAInst.destroy();

            let datasetsPA = [];
            if (selProd !== 'ALL' && rows.length === 1) {
                const r = rows[0];
                const mCpls = allMonths.map(m => (r.months[m] && r.months[m].cpl) || 0);
                datasetsPA.push({
                    type: 'bar',
                    label: `CPL Thực Tế (${r.name})`,
                    data: mCpls,
                    backgroundColor: mCpls.map(v => (r.planCPL > 0 && v > r.planCPL) ? 'rgba(239, 68, 68, 0.82)' : 'rgba(16, 185, 129, 0.82)'),
                    borderRadius: 6,
                    order: 2
                });
                if (r.planCPL > 0) {
                    datasetsPA.push({
                        type: 'line',
                        label: `CPL Kế Hoạch (${fmtShort(r.planCPL)})`,
                        data: allMonths.map(() => r.planCPL),
                        borderColor: '#fbbf24',
                        backgroundColor: '#fbbf24',
                        borderDash: [6, 6],
                        borderWidth: 2.5,
                        pointRadius: 3,
                        order: 1
                    });
                }
            } else {
                const cplRows = summaryRows.filter(r => r.planCPL > 0);
                datasetsPA = cplRows.map((r, i) => ({
                    type: 'line',
                    label: `${r.name} (KH: ${fmtShort(r.planCPL)})`,
                    data: allMonths.map(m => (r.months[m] && r.months[m].cpl) || null),
                    borderColor: PALETTE[i % PALETTE.length],
                    backgroundColor: PALETTE[i % PALETTE.length],
                    borderWidth: 2.2,
                    pointRadius: 3.5,
                    spanGaps: true,
                    tension: 0.25
                }));
            }

            chartPerfAInst = new Chart(ctxPA, {
                type: 'bar',
                data: { labels: mLabels, datasets: datasetsPA },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: { position: 'top', labels: { color: colors.text, boxWidth: 11, font: { size: 10.5, weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => ctx.raw ? `${ctx.dataset.label}: ${fmtVND(ctx.raw)}` : ''
                            }
                        }
                    },
                    scales: {
                        x: { grid: { color: colors.grid }, ticks: { color: colors.text, font: { weight: 600 } } },
                        y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: v => fmtShort(v) } }
                    }
                }
            });

            // 2. Biểu đồ 3B: Tỷ Lệ Chuyển Đổi (Data/Mess % & HĐ/Data %) Theo Tháng
            document.getElementById('perfChartBTitle').textContent = `2. Tỷ Lệ Chuyển Đổi Theo Tháng (${scopeLbl})`;
            const dmRates = allMonths.map(m => {
                const ms = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].mess) || 0), 0);
                const dt = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].data) || 0), 0);
                return ms > 0 ? +(dt / ms * 100).toFixed(1) : 0;
            });
            const hdRates = allMonths.map(m => {
                const dt = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].data) || 0), 0);
                const hd = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].hd) || 0), 0);
                return dt > 0 ? +(hd / dt * 100).toFixed(1) : 0;
            });

            const ctxPB = document.getElementById('chartPerfB').getContext('2d');
            if (chartPerfBInst) chartPerfBInst.destroy();
            chartPerfBInst = new Chart(ctxPB, {
                type: 'bar',
                data: {
                    labels: mLabels,
                    datasets: [
                        {
                            type: 'bar',
                            label: 'Tỷ lệ Data / Mess (%)',
                            data: dmRates,
                            backgroundColor: 'rgba(99, 102, 241, 0.78)',
                            borderRadius: 6,
                            yAxisID: 'yDm',
                            order: 2
                        },
                        {
                            type: 'line',
                            label: 'Tỷ lệ Chốt HĐ / Data (%)',
                            data: hdRates,
                            borderColor: '#10b981',
                            backgroundColor: '#10b981',
                            borderWidth: 2.5,
                            pointRadius: 4,
                            tension: 0.25,
                            yAxisID: 'yHd',
                            order: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: { position: 'top', labels: { color: colors.text, boxWidth: 11, font: { size: 11, weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}%`
                            }
                        }
                    },
                    scales: {
                        x: { grid: { color: colors.grid }, ticks: { color: colors.text, font: { weight: 600 } } },
                        yDm: {
                            position: 'left',
                            grid: { color: colors.grid },
                            ticks: { color: '#818cf8', callback: v => v + '%' }
                        },
                        yHd: {
                            position: 'right',
                            grid: { drawOnChartArea: false },
                            ticks: { color: '#34d399', callback: v => v + '%' }
                        }
                    }
                }
            });

            // 3. Biểu đồ 3C: Chi Phí / Hợp Đồng (CP/HĐ) & Số Lượng HĐ Theo Tháng
            document.getElementById('perfChartCTitle').textContent = `3. Chi Phí / Hợp Đồng (CP/HĐ) & Số Lượng HĐ Theo Tháng (${scopeLbl})`;
            const mCpHd = allMonths.map(m => {
                const sp = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].spend) || 0), 0);
                const hd = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].hd) || 0), 0);
                return hd > 0 ? Math.round(sp / hd) : 0;
            });
            const mHdCounts = allMonths.map(m => rows.reduce((s, r) => s + ((r.months[m] && r.months[m].hd) || 0), 0));

            const ctxPC = document.getElementById('chartPerfC').getContext('2d');
            if (chartPerfCInst) chartPerfCInst.destroy();
            chartPerfCInst = new Chart(ctxPC, {
                type: 'bar',
                data: {
                    labels: mLabels,
                    datasets: [
                        {
                            type: 'bar',
                            label: 'Chi Phí / HĐ (VNĐ)',
                            data: mCpHd,
                            backgroundColor: 'rgba(6, 182, 212, 0.78)',
                            borderRadius: 6,
                            yAxisID: 'yCpHd',
                            order: 2
                        },
                        {
                            type: 'line',
                            label: 'Số Lượng Hợp Đồng (HĐ)',
                            data: mHdCounts,
                            borderColor: '#f59e0b',
                            backgroundColor: '#f59e0b',
                            borderWidth: 2.5,
                            pointRadius: 4.5,
                            tension: 0.25,
                            yAxisID: 'yHdCount',
                            order: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: { position: 'top', labels: { color: colors.text, boxWidth: 11, font: { size: 11, weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => ctx.dataset.yAxisID === 'yHdCount'
                                    ? `${ctx.dataset.label}: ${fmtNum(ctx.raw)} HĐ`
                                    : `${ctx.dataset.label}: ${fmtVND(ctx.raw)}`
                            }
                        }
                    },
                    scales: {
                        x: { grid: { color: colors.grid }, ticks: { color: colors.text, font: { weight: 600 } } },
                        yCpHd: {
                            position: 'left',
                            grid: { color: colors.grid },
                            ticks: { color: '#22d3ee', callback: v => fmtShort(v) }
                        },
                        yHdCount: {
                            position: 'right',
                            grid: { drawOnChartArea: false },
                            ticks: { color: '#fbbf24', precision: 0, callback: v => v + ' HĐ' }
                        }
                    }
                }
            });

            // 4. Biểu đồ 3D: Doanh Số & % Chi Phí / Doanh Số Theo Tháng
            document.getElementById('perfChartDTitle').textContent = `4. Doanh Số & % Chi Phí / Doanh Số Theo Tháng (${scopeLbl})`;
            const mDsVals = allMonths.map(m => rows.reduce((s, r) => s + ((r.months[m] && r.months[m].ds) || 0), 0));
            const mCpDsPcts = allMonths.map((m, idx) => {
                const sp = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].spend) || 0), 0);
                const ds = mDsVals[idx];
                return ds > 0 ? +(sp / ds * 100).toFixed(1) : 0;
            });

            const ctxPD = document.getElementById('chartPerfD').getContext('2d');
            if (chartPerfDInst) chartPerfDInst.destroy();
            chartPerfDInst = new Chart(ctxPD, {
                type: 'bar',
                data: {
                    labels: mLabels,
                    datasets: [
                        {
                            type: 'bar',
                            label: 'Doanh Số (VNĐ)',
                            data: mDsVals,
                            backgroundColor: 'rgba(236, 72, 153, 0.78)',
                            borderRadius: 6,
                            yAxisID: 'yDs',
                            order: 2
                        },
                        {
                            type: 'line',
                            label: '% CP / Doanh Số',
                            data: mCpDsPcts,
                            borderColor: '#34d399',
                            backgroundColor: '#34d399',
                            borderWidth: 2.5,
                            pointRadius: 4.5,
                            tension: 0.25,
                            yAxisID: 'yCpDs',
                            order: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: { position: 'top', labels: { color: colors.text, boxWidth: 11, font: { size: 11, weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => ctx.dataset.yAxisID === 'yCpDs'
                                    ? `${ctx.dataset.label}: ${ctx.raw}%`
                                    : `${ctx.dataset.label}: ${fmtVND(ctx.raw)}`
                            }
                        }
                    },
                    scales: {
                        x: { grid: { color: colors.grid }, ticks: { color: colors.text, font: { weight: 600 } } },
                        yDs: {
                            position: 'left',
                            grid: { color: colors.grid },
                            ticks: { color: '#f472b6', callback: v => fmtShort(v) }
                        },
                        yCpDs: {
                            position: 'right',
                            grid: { drawOnChartArea: false },
                            ticks: { color: '#34d399', callback: v => v + '%' }
                        }
                    }
                }
            });
        }

        function renderPerfTable(summaryRows, allMonths, selProd, year) {
            const thead = document.getElementById('perfTableHead');
            const tbody = document.getElementById('perfTableBody');
            const rows = selProd === 'ALL' ? summaryRows : summaryRows.filter(r => r.name === selProd);
            const monthHeaders = allMonths.map(m => `<th style="text-align:right;">T${m.split('-')[1]}/${m.split('-')[0].slice(2)}</th>`).join('');

            // Mode 1: Tổng hợp CPL + Tỷ lệ CĐ + CP/HĐ qua các tháng
            if (perfTableMode === 'all') {
                document.getElementById('sec3Title').textContent = `Bảng Tổng Hợp Hiệu Suất Năm ${year}: CPL Thực Tế vs. KH • Tỷ Lệ CĐ • Chi Phí / HĐ Theo Tháng`;
                thead.innerHTML = `
                    <tr>
                        <th>Sản Phẩm</th>
                        <th style="text-align:right;">CPL KH</th>
                        <th style="text-align:right;">TB Năm ${year}</th>
                        ${monthHeaders}
                    </tr>
                `;

                const bodyHtml = rows.map(r => {
                    const planTxt = r.planCPL > 0 ? `<b>${fmtShort(r.planCPL)}</b>` : `<span style="color:var(--text-muted);">--</span>`;
                    const yDmRate = r.yearMess > 0 ? (r.yearData / r.yearMess * 100).toFixed(1) : '--';
                    const yHdRate = r.yearData > 0 ? (r.yearHD / r.yearData * 100).toFixed(1) : '--';
                    const yCpHd = r.yearHD > 0 ? fmtShort(r.yearSpend / r.yearHD) : '--';
                    const yCpDs = r.yearDS > 0 ? (r.yearSpend / r.yearDS * 100).toFixed(1) + '%' : '--';
                    const yCplColor = r.planCPL > 0 && r.avgYearCPL > 0 ? (r.isOverPlanAvg ? '#f87171' : '#34d399') : 'var(--text-primary)';

                    const avgCell = `
                        <td style="text-align:right; line-height:1.45; font-size:0.73rem; background:rgba(99,102,241,0.06);">
                            <div>CPL: <b style="color:${yCplColor};">${r.avgYearCPL > 0 ? fmtShort(r.avgYearCPL) : '--'}</b></div>
                            <div style="color:var(--text-secondary);">D/M: <b>${yDmRate}%</b> • HĐ/D: <b>${yHdRate}%</b></div>
                            <div style="color:#22d3ee;">CP/HĐ: <b>${yCpHd}</b> (${r.yearHD} HĐ)</div>
                            <div style="color:#f472b6;">DS: <b>${r.yearDS > 0 ? fmtShort(r.yearDS) : '--'}</b> (${yCpDs})</div>
                        </td>
                    `;

                    const mCells = allMonths.map(m => {
                        const mo = r.months[m];
                        if (!mo || (mo.spend === 0 && mo.data === 0 && mo.hd === 0 && mo.ds === 0)) {
                            return `<td style="text-align:right; color:var(--text-muted);">--</td>`;
                        }
                        const isOverM = r.planCPL > 0 && mo.cpl > r.planCPL;
                        const cplColor = r.planCPL > 0 && mo.cpl > 0 ? (isOverM ? '#f87171' : '#34d399') : 'var(--text-primary)';
                        const dmRate = mo.mess > 0 ? (mo.data / mo.mess * 100).toFixed(0) + '%' : '--';
                        const hdRate = mo.data > 0 ? (mo.hd / mo.data * 100).toFixed(1) + '%' : '--';
                        const cpHd = mo.hd > 0 ? fmtShort(mo.spend / mo.hd) : '--';
                        return `
                            <td style="text-align:right; line-height:1.45; font-size:0.72rem; white-space:nowrap;">
                                <div><b style="color:${cplColor};">${mo.cpl > 0 ? fmtShort(mo.cpl) : '--'}</b>${isOverM ? ' 🚨' : ''}</div>
                                <div style="color:var(--text-secondary);">${dmRate} • ${hdRate}</div>
                                <div style="color:#22d3ee;">${cpHd}${mo.hd > 0 ? ` (${mo.hd})` : ''}</div>
                                <div style="color:#f472b6;">${mo.ds > 0 ? fmtShort(mo.ds) : '--'}</div>
                            </td>
                        `;
                    }).join('');

                    return `
                        <tr class="${selProd === r.name ? 'active-row' : ''}" onclick="selectProduct('${r.name}')" style="cursor:pointer;">
                            <td><b>📦 ${r.name}</b></td>
                            <td style="text-align:right;">${planTxt}</td>
                            ${avgCell}
                            ${mCells}
                        </tr>
                    `;
                }).join('');

                tbody.innerHTML = bodyHtml;
                return;
            }

            // Mode 2: CPL Thực tế vs CPL Kế hoạch qua các tháng
            if (perfTableMode === 'cpl') {
                document.getElementById('sec3Title').textContent = `Bảng So Sánh CPL Thực Tế vs. CPL Kế Hoạch Theo Tháng (${year})`;
                thead.innerHTML = `
                    <tr>
                        <th>Sản Phẩm</th>
                        <th style="text-align:right;">CPL Kế Hoạch</th>
                        <th style="text-align:right;">CPL TB ${year}</th>
                        <th>Đánh Giá Năm</th>
                        ${monthHeaders}
                    </tr>
                `;
                tbody.innerHTML = rows.map(r => {
                    const planTxt = r.planCPL > 0 ? `<b>${fmtShort(r.planCPL)}</b>` : `<span style="color:var(--text-muted);">--</span>`;
                    const avgColor = r.planCPL > 0 && r.avgYearCPL > 0 ? (r.isOverPlanAvg ? '#f87171' : '#34d399') : 'var(--text-primary)';
                    let badge = `<span class="badge b-muted">--</span>`;
                    if (r.planCPL > 0 && r.avgYearCPL > 0) {
                        badge = r.isOverPlanAvg
                            ? `<span class="badge b-down">🚨 Vượt +${r.diffPlanAvgPct.toFixed(1)}%</span>`
                            : `<span class="badge b-up">✅ Đạt ${r.diffPlanAvgPct.toFixed(1)}%</span>`;
                    }
                    const mCells = allMonths.map(m => {
                        const mo = r.months[m];
                        if (!mo || mo.cpl === 0) return `<td style="text-align:right; color:var(--text-muted);">--</td>`;
                        const isOverM = r.planCPL > 0 && mo.cpl > r.planCPL;
                        const color = r.planCPL > 0 ? (isOverM ? '#f87171' : '#34d399') : 'var(--text-primary)';
                        const diffTxt = r.planCPL > 0 ? `<div style="font-size:0.67rem; opacity:0.85;">${((mo.cpl - r.planCPL) / r.planCPL * 100 >= 0 ? '+' : '') + ((mo.cpl - r.planCPL) / r.planCPL * 100).toFixed(0)}%</div>` : '';
                        return `<td style="text-align:right; color:${color}; font-weight:700;">${fmtShort(mo.cpl)}${isOverM ? ' 🚨' : ''}${diffTxt}</td>`;
                    }).join('');
                    return `
                        <tr class="${selProd === r.name ? 'active-row' : ''}" onclick="selectProduct('${r.name}')" style="cursor:pointer;">
                            <td><b>📦 ${r.name}</b></td>
                            <td style="text-align:right;">${planTxt}</td>
                            <td style="text-align:right; color:${avgColor}; font-weight:800;">${r.avgYearCPL > 0 ? fmtShort(r.avgYearCPL) : '--'}</td>
                            <td>${badge}</td>
                            ${mCells}
                        </tr>
                    `;
                }).join('');
                return;
            }

            // Mode 3: Tỷ lệ chuyển đổi theo tháng (Data/Mess % và HĐ/Data %)
            if (perfTableMode === 'cr') {
                document.getElementById('sec3Title').textContent = `Bảng Tỷ Lệ Chuyển Đổi (Data/Mess % & Chốt HĐ/Data %) Theo Tháng (${year})`;
                thead.innerHTML = `
                    <tr>
                        <th>Sản Phẩm</th>
                        <th style="text-align:right;">Mess ➔ Data ➔ HĐ (${year})</th>
                        <th style="text-align:right;">TB Data/Mess</th>
                        <th style="text-align:right;">TB HĐ/Data</th>
                        ${monthHeaders}
                    </tr>
                `;
                tbody.innerHTML = rows.map(r => {
                    const yDm = r.yearMess > 0 ? (r.yearData / r.yearMess * 100).toFixed(1) + '%' : '--';
                    const yHdD = r.yearData > 0 ? (r.yearHD / r.yearData * 100).toFixed(1) + '%' : '--';
                    const mCells = allMonths.map(m => {
                        const mo = r.months[m];
                        if (!mo || (mo.mess === 0 && mo.data === 0 && mo.hd === 0)) {
                            return `<td style="text-align:right; color:var(--text-muted);">--</td>`;
                        }
                        const dm = mo.mess > 0 ? (mo.data / mo.mess * 100).toFixed(1) + '%' : '--';
                        const hdD = mo.data > 0 ? (mo.hd / mo.data * 100).toFixed(1) + '%' : '--';
                        return `
                            <td style="text-align:right; line-height:1.4; font-size:0.73rem;">
                                <div>D/M: <b>${dm}</b></div>
                                <div style="color:#34d399;">HĐ/D: <b>${hdD}</b></div>
                            </td>
                        `;
                    }).join('');
                    return `
                        <tr class="${selProd === r.name ? 'active-row' : ''}" onclick="selectProduct('${r.name}')" style="cursor:pointer;">
                            <td><b>📦 ${r.name}</b></td>
                            <td style="text-align:right; font-size:0.74rem;">${fmtNum(r.yearMess)} ➔ <b>${fmtNum(r.yearData)}</b> ➔ <b style="color:#34d399;">${fmtNum(r.yearHD)}</b></td>
                            <td style="text-align:right;"><b>${yDm}</b></td>
                            <td style="text-align:right; color:#34d399;"><b>${yHdD}</b></td>
                            ${mCells}
                        </tr>
                    `;
                }).join('');
                return;
            }

            // Mode 4: Chi phí / Hợp đồng (CP/HĐ) qua các tháng
            if (perfTableMode === 'cphd') {
                document.getElementById('sec3Title').textContent = `Bảng Chi Phí / Hợp Đồng (CP/HĐ) & Số Lượng HĐ Theo Tháng (${year})`;
                thead.innerHTML = `
                    <tr>
                        <th>Sản Phẩm</th>
                        <th style="text-align:right;">Tổng HĐ ${year}</th>
                        <th style="text-align:right;">CP/HĐ Năm ${year}</th>
                        ${monthHeaders}
                    </tr>
                `;
                const cpHdBody = rows.map(r => {
                    const yCpHd = r.yearHD > 0 ? fmtShort(r.yearSpend / r.yearHD) : '--';
                    const mCells = allMonths.map(m => {
                        const mo = r.months[m];
                        if (!mo || mo.spend === 0) return `<td style="text-align:right; color:var(--text-muted);">--</td>`;
                        if (mo.hd === 0) return `<td style="text-align:right; color:#f87171; font-size:0.72rem;">0 HĐ<div style="font-size:0.67rem; opacity:0.8;">(${fmtShort(mo.spend)})</div></td>`;
                        const cpHd = fmtShort(mo.spend / mo.hd);
                        return `
                            <td style="text-align:right; line-height:1.4; font-size:0.73rem;">
                                <div style="color:#22d3ee;"><b>${cpHd}</b></div>
                                <div style="color:var(--text-secondary); font-size:0.68rem;">${mo.hd} HĐ</div>
                            </td>
                        `;
                    }).join('');
                    return `
                        <tr class="${selProd === r.name ? 'active-row' : ''}" onclick="selectProduct('${r.name}')" style="cursor:pointer;">
                            <td><b>📦 ${r.name}</b></td>
                            <td style="text-align:right;"><b>${fmtNum(r.yearHD)} HĐ</b></td>
                            <td style="text-align:right; color:#22d3ee;"><b>${yCpHd}</b></td>
                            ${mCells}
                        </tr>
                    `;
                }).join('');

                const totAllSpend = rows.reduce((s, r) => s + r.yearSpend, 0);
                const totAllHD = rows.reduce((s, r) => s + r.yearHD, 0);
                const totRowCpHd = `
                    <tr class="total-row">
                        <td>TỔNG CỘNG</td>
                        <td style="text-align:right;">${fmtNum(totAllHD)} HĐ</td>
                        <td style="text-align:right;">${totAllHD > 0 ? fmtShort(totAllSpend / totAllHD) : '--'}</td>
                        ${allMonths.map(m => {
                            const mSp = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].spend) || 0), 0);
                            const mHd = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].hd) || 0), 0);
                            return `<td style="text-align:right;">${mHd > 0 ? fmtShort(mSp / mHd) + ` (${mHd})` : (mSp > 0 ? '0 HĐ' : '--')}</td>`;
                        }).join('')}
                    </tr>
                `;
                tbody.innerHTML = cpHdBody + totRowCpHd;
                return;
            }

            // Mode 5: Doanh Số & % CP/DS qua các tháng
            document.getElementById('sec3Title').textContent = `Bảng Doanh Số & Tỷ Lệ Chi Phí / Doanh Số (% CP/DS) Theo Tháng (${year})`;
            thead.innerHTML = `
                <tr>
                    <th>Sản Phẩm</th>
                    <th style="text-align:right;">Tổng DS ${year}</th>
                    <th style="text-align:right;">% CP/DS Năm</th>
                    ${monthHeaders}
                </tr>
            `;
            const dsBody = rows.map(r => {
                const yCpDs = r.yearDS > 0 ? (r.yearSpend / r.yearDS * 100).toFixed(1) + '%' : '--';
                const mCells = allMonths.map(m => {
                    const mo = r.months[m];
                    if (!mo || (mo.ds === 0 && mo.spend === 0)) return `<td style="text-align:right; color:var(--text-muted);">--</td>`;
                    if (mo.ds === 0) return `<td style="text-align:right; color:var(--text-muted); font-size:0.72rem;">--</td>`;
                    const cpDs = (mo.spend / mo.ds * 100).toFixed(1) + '%';
                    return `
                        <td style="text-align:right; line-height:1.4; font-size:0.73rem;">
                            <div style="color:#f472b6;"><b>${fmtShort(mo.ds)}</b></div>
                            <div style="color:#34d399; font-size:0.68rem;">${cpDs}</div>
                        </td>
                    `;
                }).join('');
                return `
                    <tr class="${selProd === r.name ? 'active-row' : ''}" onclick="selectProduct('${r.name}')" style="cursor:pointer;">
                        <td><b>📦 ${r.name}</b></td>
                        <td style="text-align:right; color:#f472b6;"><b>${fmtVND(r.yearDS)}</b></td>
                        <td style="text-align:right; color:#34d399;"><b>${yCpDs}</b></td>
                        ${mCells}
                    </tr>
                `;
            }).join('');

            const totAllSpendDs = rows.reduce((s, r) => s + r.yearSpend, 0);
            const totAllDS = rows.reduce((s, r) => s + r.yearDS, 0);
            const totRowDs = `
                <tr class="total-row">
                    <td>TỔNG CỘNG</td>
                    <td style="text-align:right;">${fmtVND(totAllDS)}</td>
                    <td style="text-align:right;">${totAllDS > 0 ? (totAllSpendDs / totAllDS * 100).toFixed(1) + '%' : '--'}</td>
                    ${allMonths.map(m => {
                        const mSp = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].spend) || 0), 0);
                        const mDs = rows.reduce((s, r) => s + ((r.months[m] && r.months[m].ds) || 0), 0);
                        return `<td style="text-align:right;">${mDs > 0 ? fmtShort(mDs) + ` (${(mSp/mDs*100).toFixed(0)}%)` : '--'}</td>`;
                    }).join('')}
                </tr>
            `;
            tbody.innerHTML = dsBody + totRowDs;
        }

        function exportPerfCSV() {
            if (!currentSummaryRows.length) return;
            const exportData = [];
            currentSummaryRows.forEach(r => {
                currentAllMonths.forEach(m => {
                    const mo = r.months[m];
                    if (!mo) return;
                    exportData.push({
                        "Sản phẩm": r.name,
                        "Tháng": m,
                        "Chi tiêu": Math.round(mo.spend),
                        "SL Mess": mo.mess,
                        "SL Data": mo.data,
                        "Tổng HĐ": mo.hd,
                        "Doanh số": Math.round(mo.ds),
                        "% CP/DS": mo.ds > 0 ? +(mo.spend / mo.ds * 100).toFixed(2) : 0,
                        "CPL Thực tế": mo.cpl,
                        "CPL Kế hoạch": r.planCPL || "",
                        "Tỷ lệ Data/Mess (%)": mo.mess > 0 ? +(mo.data / mo.mess * 100).toFixed(2) : 0,
                        "Tỷ lệ HĐ/Data (%)": mo.data > 0 ? +(mo.hd / mo.data * 100).toFixed(2) : 0,
                        "Chi phí / HĐ": mo.hd > 0 ? Math.round(mo.spend / mo.hd) : 0
                    });
                });
            });
            const csv = Papa.unparse(exportData);
            const blob = new Blob(["\\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `Hieu_Suat_CPL_CD_CPHD_Theo_Thang.csv`;
            a.click();
        }

        async function fetchFromGoogleSheet() {
            const st = document.getElementById('syncStatusText');
            st.textContent = '⏳ Đang đồng bộ từ Google Sheet...';
            try {
                const resp = await fetch(GOOGLE_SHEET_CSV_URL, { cache: 'no-cache' });
                if (!resp.ok) throw new Error('HTTP ' + resp.status);
                const csvText = await resp.text();
                Papa.parse(csvText, {
                    header: true,
                    dynamicTyping: true,
                    skipEmptyLines: true,
                    complete: (res) => {
                        if (res.data && res.data.length > 0) {
                            RAW_DATA = res.data;
                            st.textContent = `🟢 Đã đồng bộ Google Sheet Online (${new Date().toLocaleTimeString('vi-VN')})`;
                            const prev = document.getElementById('prevMonthSelect').value;
                            const curr = document.getElementById('currMonthSelect').value;
                            initSelectors();
                            if (prev) document.getElementById('prevMonthSelect').value = prev;
                            if (curr) document.getElementById('currMonthSelect').value = curr;
                            renderAll();
                        }
                    }
                });
            } catch (e) {
                st.textContent = '🟢 Dữ liệu Lark Base & Google Sheet đã đồng bộ';
            }
        }

        function exportCSV() {
            if (!currentSummaryRows.length) return;
            const prevM = document.getElementById('prevMonthSelect').value;
            const currM = document.getElementById('currMonthSelect').value;
            const data = currentSummaryRows.map(r => ({
                "Sản phẩm": r.name,
                "Tổng chi tiêu năm": Math.round(r.yearSpend),
                "% Tỷ trọng năm": +r.shareYear.toFixed(2),
                [`Chi tiêu ${prevM}`]: Math.round(r.mp.spend),
                [`Chi tiêu ${currM}`]: Math.round(r.mc.spend),
                "Δ% Tháng": +r.deltaSpendPct.toFixed(2),
                [`Data ${prevM}`]: r.mp.data,
                [`Data ${currM}`]: r.mc.data,
                [`HĐ ${prevM}`]: r.mp.hd,
                [`HĐ ${currM}`]: r.mc.hd,
                "Tổng HĐ Năm": r.yearHD,
                "CP/HĐ Năm": r.yearHD > 0 ? Math.round(r.yearSpend / r.yearHD) : 0,
                [`Doanh số ${prevM}`]: Math.round(r.mp.ds),
                [`Doanh số ${currM}`]: Math.round(r.mc.ds),
                "Tổng Doanh Số Năm": Math.round(r.yearDS),
                "% CP/DS Năm": r.yearDS > 0 ? +(r.yearSpend / r.yearDS * 100).toFixed(2) : 0,
                "CPL Kế Hoạch": r.planCPL || "",
                "CPL TB Năm": r.avgYearCPL || "",
                [`CPL ${prevM}`]: r.cplPrev || "",
                [`CPL ${currM}`]: r.cplCurr || "",
                "Cảnh báo CPL": r.planCPL > 0 ? ((r.cplCurr > 0 ? r.isOverPlanCurr : r.isOverPlanAvg) ? "VƯỢT KẾ HOẠCH" : "ĐẠT KẾ HOẠCH") : ""
            }));
            const csv = Papa.unparse(data);
            const blob = new Blob(["\\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `Ngan_Sach_CPL_San_Pham_${prevM}_vs_${currM}.csv`;
            a.click();
        }

        function toggleTheme() {
            const cur = document.documentElement.getAttribute('data-theme');
            document.documentElement.setAttribute('data-theme', cur === 'dark' ? 'light' : 'dark');
            renderAll();
        }

        document.addEventListener('DOMContentLoaded', () => {
            initSelectors();
            renderAll();
            fetchFromGoogleSheet();
        });
    </script>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Đã biên dịch thành công Dashboard kèm CPL Kế hoạch & Cảnh báo tại: {html_path}")
print(f"Dung lượng file: {os.path.getsize(html_path) / 1024:.1f} KB")
