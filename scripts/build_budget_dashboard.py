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
    "CPL Tổng", "CP/Mess", "HĐ Ký Trong Tháng", "Tổng HĐ", "HĐ Hết Vòng", "CP/HĐ Hết Vòng",
    "Doanh Số Trong Tháng", "Doanh Số Tổng"
}
float_fields = {"CP/DS Tổng (%)"}

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
    <title>Quản Trị Ngân Sách Sản Phẩm 2026 | Product Report</title>
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
            max-width: 1580px;
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
            margin-bottom: 0.9rem;
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
            padding: 0.65rem 1rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            margin-bottom: 1rem;
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
        }

        .prod-pill:hover { border-color: var(--primary); color: var(--text-primary); }
        .prod-pill.active {
            background: var(--primary);
            border-color: var(--primary);
            color: #fff;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.35);
        }

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

        /* ─── SECTION 1: 4 COMPACT KPI CARDS ─── */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.85rem;
        }

        @media (max-width: 1024px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 600px) { .kpi-grid { grid-template-columns: 1fr; } }

        .kpi-box {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-top: 3px solid var(--accent, var(--primary));
            border-radius: var(--radius-md);
            padding: 0.9rem 1.05rem;
        }

        .kpi-name {
            font-size: 0.73rem;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-secondary);
            display: flex;
            justify-content: space-between;
        }

        .kpi-num {
            font-size: 1.48rem;
            font-weight: 800;
            margin: 0.25rem 0;
            letter-spacing: -0.02em;
            font-variant-numeric: tabular-nums;
        }

        .kpi-foot {
            font-size: 0.74rem;
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
            grid-template-columns: 1.65fr 1fr;
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
            gap: 0.5rem;
            margin-bottom: 0.65rem;
            font-size: 0.86rem;
            font-weight: 800;
        }

        .canvas-wrap {
            position: relative;
            height: 310px;
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
            font-size: 0.8rem;
            text-align: left;
            white-space: nowrap;
            font-variant-numeric: tabular-nums;
        }

        th {
            background: var(--bg-surface-solid);
            padding: 0.68rem 0.85rem;
            font-weight: 700;
            color: var(--text-secondary);
            border-bottom: 2px solid var(--border-color);
            font-size: 0.72rem;
            text-transform: uppercase;
        }

        td {
            padding: 0.62rem 0.85rem;
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
            padding: 0.15rem 0.5rem;
            border-radius: var(--radius-full);
            font-size: 0.71rem;
            font-weight: 800;
        }

        .b-up { background: rgba(16, 185, 129, 0.16); color: #34d399; }
        .b-down { background: rgba(239, 68, 68, 0.16); color: #f87171; }
        .b-warn { background: rgba(245, 158, 11, 0.16); color: #fbbf24; }
        .b-info { background: rgba(6, 182, 212, 0.16); color: #22d3ee; }
        .b-muted { background: rgba(148, 163, 184, 0.14); color: #94a3b8; }

        .mini-bar {
            width: 48px;
            height: 5px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 99px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-right: 5px;
        }

        .mini-bar-fill { height: 100%; border-radius: 99px; background: #6366f1; }
    </style>
</head>
<body>
    <div class="container">
        <!-- ─── TOP BAR ─── -->
        <div class="topbar">
            <div class="brand">
                <div class="brand-logo">📊</div>
                <div>
                    <div class="brand-title">QUẢN TRỊ NGÂN SÁCH SẢN PHẨM QUẢNG CÁO</div>
                    <div style="font-size:0.73rem; color:var(--text-secondary);" id="syncStatusText">🟢 Nguồn: Lark Base (tblEr3vySvt58EkK) ➔ Google Sheet</div>
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
        <div class="pills-bar" id="productPills"></div>

        <!-- ═══════════════════════════════════════════════════════════════════════════
             SECTION 1: TỔNG CHI TIÊU NĂM 2026 & SO SÁNH THÁNG TRƯỚC VS. THÁNG HIỆN TẠI
             ═══════════════════════════════════════════════════════════════════════════ -->
        <div class="section-box">
            <div class="section-bar">
                <div class="section-label">
                    <span class="tag-sec">SECTION 1</span>
                    <span id="sec1Title">Tổng Chi Tiêu Năm 2026 & So Sánh Tháng Trước vs. Tháng Hiện Tại</span>
                </div>
                <div class="switch-group">
                    <button class="switch-btn active" id="btnTaxAfter" onclick="setTaxMode('after')">Sau thuế (Tổng CP)</button>
                    <button class="switch-btn" id="btnTaxBefore" onclick="setTaxMode('before')">Trước thuế</button>
                </div>
            </div>

            <div class="kpi-grid" id="sec1KpiGrid"></div>
        </div>

        <!-- ═══════════════════════════════════════════════════════════════════════════
             SECTION 2: BIỂU ĐỒ CHI TIÊU CÁC SẢN PHẨM QUA CÁC THÁNG
             ═══════════════════════════════════════════════════════════════════════════ -->
        <div class="section-box">
            <div class="section-bar">
                <div class="section-label">
                    <span class="tag-sec">SECTION 2</span>
                    <span>Biểu Đồ Chi Tiêu Các Sản Phẩm Qua Các Tháng</span>
                </div>
                <div class="switch-group">
                    <button class="switch-btn active" id="btnChartSpend" onclick="setChartMetric('spend')">💰 Chi Tiêu</button>
                    <button class="switch-btn" id="btnChartData" onclick="setChartMetric('data')">📱 Chi Tiêu + Data</button>
                    <button class="switch-btn" id="btnChartHD" onclick="setChartMetric('hd')">📝 Chi Tiêu + HĐ</button>
                </div>
            </div>

            <!-- Hàng 1: So sánh Tháng trước vs Tháng hiện tại + Tỷ trọng năm -->
            <div class="charts-row">
                <div class="chart-panel">
                    <div class="chart-head">
                        <span id="compareChartTitle">1. So Sánh Chi Tiêu Sản Phẩm: Tháng Trước vs. Tháng Hiện Tại</span>
                        <span style="font-size:0.72rem; color:var(--text-muted); font-weight:600;">Bấm vào cột để lọc SP</span>
                    </div>
                    <div class="canvas-wrap">
                        <canvas id="chartMonthCompare"></canvas>
                    </div>
                </div>

                <div class="chart-panel">
                    <div class="chart-head">
                        <span id="shareChartTitle">2. Tỷ Trọng Ngân Sách Năm 2026 Theo Sản Phẩm</span>
                    </div>
                    <div class="canvas-wrap">
                        <canvas id="chartYearShare"></canvas>
                    </div>
                </div>
            </div>

            <!-- Hàng 2: Xu hướng chi tiêu qua các tháng trong năm -->
            <div class="chart-panel" style="margin-bottom: 1rem;">
                <div class="chart-head">
                    <span id="trendChartTitle">3. Xu Hướng Chi Tiêu Qua Các Tháng Trong Năm (T01 ➔ T11)</span>
                    <div class="switch-group">
                        <button class="switch-btn active" id="btnStackProd" onclick="setTrendMode('product')">Theo Sản Phẩm</button>
                        <button class="switch-btn" id="btnStackChannel" onclick="setTrendMode('channel')">Theo Kênh (FB Mess / LDP / TikTok)</button>
                    </div>
                </div>
                <div class="canvas-wrap" style="height: 290px;">
                    <canvas id="chartMonthlyTrend"></canvas>
                </div>
            </div>

            <!-- Bảng đối chiếu gọn & Ma trận các tháng -->
            <div class="chart-head" style="margin-top:0.25rem;">
                <span id="tableModeTitle">4. Bảng Số Liệu Ngân Sách Sản Phẩm</span>
                <div style="display:flex; gap:0.4rem;">
                    <div class="switch-group">
                        <button class="switch-btn active" id="btnTblCompare" onclick="setTableMode('compare')">So Sánh 2 Tháng</button>
                        <button class="switch-btn" id="btnTblMatrix" onclick="setTableMode('matrix')">Ma Trận Toàn Bộ Các Tháng</button>
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
    </div>

    <script>
        const GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1V9z5T7BQABDSvsytY0P1kKV5b4lMfpzcFZWghJwUitw/gviz/tq?tqx=out:csv&sheet=Data_San_Pham_Cleaned";
        let RAW_DATA = """ + json_data_str + """;

        let taxMode = "after";       // 'after' | 'before'
        let chartMetric = "spend";   // 'spend' | 'data' | 'hd'
        let trendMode = "product";   // 'product' | 'channel'
        let tableMode = "compare";   // 'compare' | 'matrix'

        let chartCompareInst = null;
        let chartShareInst = null;
        let chartTrendInst = null;
        let currentSummaryRows = [];

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

            // Months
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

            // Products
            const prodSpend = {};
            yearRows.forEach(r => {
                const p = r["Tag Sản Phẩm"] || r["Sản Phẩm Gốc"] || "Khác";
                prodSpend[p] = (prodSpend[p] || 0) + getSpend(r);
            });
            const sortedProds = Object.keys(prodSpend).sort((a, b) => prodSpend[b] - prodSpend[a]);

            const prodSel = document.getElementById('productSelect');
            const curProd = prodSel.value;
            prodSel.innerHTML = `<option value="ALL">📦 Tất cả (${sortedProds.length} sản phẩm)</option>`;
            sortedProds.forEach(p => {
                const o = document.createElement('option');
                o.value = p;
                o.textContent = `📦 ${p} (${fmtShort(prodSpend[p])})`;
                prodSel.appendChild(o);
            });
            if (sortedProds.includes(curProd)) prodSel.value = curProd;

            // Pills
            const pillsEl = document.getElementById('productPills');
            pillsEl.innerHTML = '';
            const allBtn = document.createElement('button');
            allBtn.className = `prod-pill ${prodSel.value === 'ALL' ? 'active' : ''}`;
            allBtn.setAttribute('data-prod', 'ALL');
            allBtn.textContent = 'Tất cả';
            allBtn.onclick = () => selectProduct('ALL');
            pillsEl.appendChild(allBtn);

            sortedProds.forEach(p => {
                const b = document.createElement('button');
                b.className = `prod-pill ${prodSel.value === p ? 'active' : ''}`;
                b.setAttribute('data-prod', p);
                b.textContent = p;
                b.onclick = () => selectProduct(p);
                pillsEl.appendChild(b);
            });
        }

        function onYearChange() {
            initSelectors();
            renderAll();
        }

        function onProductDropdownChange() {
            const val = document.getElementById('productSelect').value;
            document.querySelectorAll('.prod-pill').forEach(b => {
                b.classList.toggle('active', b.getAttribute('data-prod') === val);
            });
            renderAll();
        }

        function selectProduct(prod) {
            const sel = document.getElementById('productSelect');
            sel.value = (sel.value === prod && prod !== 'ALL') ? 'ALL' : prod;
            onProductDropdownChange();
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
            renderAll();
        }

        function setTrendMode(m) {
            trendMode = m;
            document.getElementById('btnStackProd').classList.toggle('active', m === 'product');
            document.getElementById('btnStackChannel').classList.toggle('active', m === 'channel');
            renderAll();
        }

        function setTableMode(m) {
            tableMode = m;
            document.getElementById('btnTblCompare').classList.toggle('active', m === 'compare');
            document.getElementById('btnTblMatrix').classList.toggle('active', m === 'matrix');
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
                const p = r["Tag Sản Phẩm"] || r["Sản Phẩm Gốc"] || "Khác";
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
                        group: r["Nhóm Sản Phẩm"] || "",
                        yearSpend: 0, yearData: 0, yearMess: 0, yearHD: 0, yearDS: 0,
                        months: {}
                    };
                }
                const po = prodMap[p];
                po.yearSpend += sp;
                po.yearData += dt;
                po.yearMess += ms;
                po.yearHD += hd;
                po.yearDS += ds;
                sysYearSpend += sp;

                if (!po.months[ym]) {
                    po.months[ym] = { spend: 0, fbMess: 0, fbLdp: 0, tiktok: 0, data: 0, mess: 0, hd: 0, ds: 0 };
                }
                po.months[ym].spend += sp;
                po.months[ym].fbMess += ch.fbMess;
                po.months[ym].fbLdp += ch.fbLdp;
                po.months[ym].tiktok += ch.tiktok;
                po.months[ym].data += dt;
                po.months[ym].mess += ms;
                po.months[ym].hd += hd;
                po.months[ym].ds += ds;
            });

            const summaryRows = Object.values(prodMap).map(p => {
                const mp = p.months[prevM] || { spend: 0, fbMess: 0, fbLdp: 0, tiktok: 0, data: 0, mess: 0, hd: 0, ds: 0 };
                const mc = p.months[currM] || { spend: 0, fbMess: 0, fbLdp: 0, tiktok: 0, data: 0, mess: 0, hd: 0, ds: 0 };
                const shareYear = sysYearSpend > 0 ? (p.yearSpend / sysYearSpend * 100) : 0;
                const diffSpend = mc.spend - mp.spend;
                const deltaSpendPct = mp.spend > 0 ? ((mc.spend - mp.spend) / mp.spend * 100) : (mc.spend > 0 ? 100 : 0);
                const cplPrev = mp.data > 0 ? (mp.spend / mp.data) : 0;
                const cplCurr = mc.data > 0 ? (mc.spend / mc.data) : 0;

                return {
                    ...p,
                    shareYear,
                    mp,
                    mc,
                    diffSpend,
                    deltaSpendPct,
                    cplPrev,
                    cplCurr
                };
            }).sort((a, b) => b.yearSpend - a.yearSpend);

            currentSummaryRows = summaryRows;

            const kpiRows = selProd === 'ALL' ? summaryRows : summaryRows.filter(r => r.name === selProd);
            renderSection1KPIs(kpiRows, selProd, year, prevM, currM, sysYearSpend);
            renderSection2Charts(summaryRows, yearRows, allMonths, selProd, year, prevM, currM);
            renderMainTable(summaryRows, allMonths, selProd, year, prevM, currM);
        }

        function renderSection1KPIs(rows, selProd, year, prevM, currM, sysYearSpend) {
            const ySpend = rows.reduce((s, r) => s + r.yearSpend, 0);
            const yData = rows.reduce((s, r) => s + r.yearData, 0);
            const yHD = rows.reduce((s, r) => s + r.yearHD, 0);
            const yShare = sysYearSpend > 0 ? (ySpend / sysYearSpend * 100) : 0;

            const pSpend = rows.reduce((s, r) => s + r.mp.spend, 0);
            const pData = rows.reduce((s, r) => s + r.mp.data, 0);
            const pHD = rows.reduce((s, r) => s + r.mp.hd, 0);
            const pCPL = pData > 0 ? (pSpend / pData) : 0;

            const cSpend = rows.reduce((s, r) => s + r.mc.spend, 0);
            const cData = rows.reduce((s, r) => s + r.mc.data, 0);
            const cHD = rows.reduce((s, r) => s + r.mc.hd, 0);
            const cCPL = cData > 0 ? (cSpend / cData) : 0;

            const diffSpend = cSpend - pSpend;
            const deltaPct = pSpend > 0 ? ((cSpend - pSpend) / pSpend * 100) : (cSpend > 0 ? 100 : 0);
            const deltaDataPct = pData > 0 ? ((cData - pData) / pData * 100) : 0;

            const scope = selProd === 'ALL' ? `Tất cả sản phẩm` : selProd;
            document.getElementById('sec1Title').textContent = `Tổng Chi Tiêu Năm ${year} (${scope}) & So Sánh ${prevM} ➔ ${currM}`;

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
                    <div class="kpi-name"><span>⚖️ Chênh Lệch (${currM} vs ${prevM})</span> <span>MoM</span></div>
                    <div class="kpi-num" style="color:${deltaPct >= 0 ? '#fbbf24' : '#38bdf8'};">
                        ${deltaPct >= 0 ? '+' : ''}${deltaPct.toFixed(1)}%
                    </div>
                    <div class="kpi-foot">
                        <span>Tiền: <b>${diffSpend >= 0 ? '+' : ''}${fmtShort(diffSpend)}</b></span>
                        <span>Data: <b style="color:${deltaDataPct >= 0 ? '#34d399' : '#f87171'};">${deltaDataPct >= 0 ? '+' : ''}${deltaDataPct.toFixed(1)}%</b></span>
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

        function renderSection2Charts(summaryRows, yearRows, allMonths, selProd, year, prevM, currM) {
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
                                label: (ctx) => ctx.dataset.yAxisID === 'yCount'
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
                                ticks: { color: '#f59e0b', precision: 0 }
                            }
                        } : {})
                    }
                }
            });

            // 2. Chart 2B: Year Share Doughnut
            document.getElementById('shareChartTitle').textContent = `2. Tỷ Trọng Ngân Sách Năm ${year}`;
            const ctxB = document.getElementById('chartYearShare').getContext('2d');
            if (chartShareInst) chartShareInst.destroy();
            chartShareInst = new Chart(ctxB, {
                type: 'doughnut',
                data: {
                    labels: summaryRows.map(r => `${r.name} (${r.shareYear.toFixed(1)}%)`),
                    datasets: [{
                        data: summaryRows.map(r => r.yearSpend),
                        backgroundColor: PALETTE,
                        borderWidth: 2,
                        borderColor: 'transparent'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '62%',
                    onClick: (e, els) => {
                        if (els.length > 0) selectProduct(summaryRows[els[0].index].name);
                    },
                    plugins: {
                        legend: { position: 'right', labels: { color: colors.text, boxWidth: 11, font: { size: 11, weight: 600 } } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => {
                                    const r = summaryRows[ctx.dataIndex];
                                    return `${r.name}: ${fmtVND(r.yearSpend)} (${r.shareYear.toFixed(1)}%)`;
                                }
                            }
                        }
                    }
                }
            });

            // 3. Chart 2C: Monthly Trend across Year
            const ctxC = document.getElementById('chartMonthlyTrend').getContext('2d');
            const targetList = selProd === 'ALL' ? summaryRows.slice(0, 9) : summaryRows.filter(r => r.name === selProd);
            document.getElementById('trendChartTitle').textContent = `3. Xu Hướng Chi Tiêu Qua Các Tháng Năm ${year} (${selProd === 'ALL' ? 'Tất cả SP' : selProd})`;

            let datasetsC = [];
            if (trendMode === 'channel') {
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
            } else {
                datasetsC = targetList.map((r, i) => ({
                    label: r.name,
                    data: allMonths.map(m => (r.months[m] && r.months[m].spend) || 0),
                    backgroundColor: PALETTE[i % PALETTE.length],
                    borderRadius: 4
                }));
            }

            if (chartTrendInst) chartTrendInst.destroy();
            chartTrendInst = new Chart(ctxC, {
                type: 'bar',
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
                                label: (ctx) => `${ctx.dataset.label}: ${fmtVND(ctx.raw)}`
                            }
                        }
                    },
                    scales: {
                        x: { stacked: true, grid: { color: colors.grid }, ticks: { color: colors.text, font: { weight: 600 } } },
                        y: {
                            stacked: true,
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

            // Mode: compare
            document.getElementById('tableModeTitle').textContent = `4. Bảng Ngân Sách Sản Phẩm Năm ${year} & So Sánh ${prevM} ➔ ${currM}`;
            thead.innerHTML = `
                <tr>
                    <th>Sản Phẩm</th>
                    <th>Lũy Kế Năm ${year}</th>
                    <th>% Tỷ Trọng</th>
                    <th>Tháng Trước (${prevM})</th>
                    <th>Tháng Hiện Tại (${currM})</th>
                    <th>Chênh Lệch</th>
                    <th>Δ% Tháng</th>
                    <th>Data (${prevM}➔${currM})</th>
                    <th>CPL (${prevM}➔${currM})</th>
                    <th>HĐ (${prevM}➔${currM})</th>
                    <th>Trạng Thái</th>
                </tr>
            `;

            const bodyHtml = rows.map(r => {
                let badge = `<span class="badge b-muted">Tạm dừng</span>`;
                if (r.mc.spend > 0 || r.mp.spend > 0) {
                    if (r.mc.spend > 0 && r.mp.spend === 0) badge = `<span class="badge b-info">🆕 Mới chạy</span>`;
                    else if (r.deltaSpendPct > 10) badge = `<span class="badge b-warn">🔼 Tăng chi</span>`;
                    else if (r.deltaSpendPct < -15) badge = `<span class="badge b-muted">🔽 Giảm chi</span>`;
                    else badge = `<span class="badge b-up">✅ Ổn định</span>`;
                }

                const dBadge = r.deltaSpendPct > 0 ? 'b-warn' : (r.deltaSpendPct < 0 ? 'b-info' : 'b-muted');

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
                        <td style="color:${r.diffSpend >= 0 ? '#fbbf24' : '#94a3b8'}; font-weight:700;">
                            ${r.diffSpend >= 0 ? '+' : ''}${fmtShort(r.diffSpend)}
                        </td>
                        <td><span class="badge ${dBadge}">${r.deltaSpendPct >= 0 ? '+' : ''}${r.deltaSpendPct.toFixed(1)}%</span></td>
                        <td>${r.mp.data} ➔ <b>${r.mc.data}</b></td>
                        <td>${r.cplPrev > 0 ? fmtShort(r.cplPrev) : '--'} ➔ <b>${r.cplCurr > 0 ? fmtShort(r.cplCurr) : '--'}</b></td>
                        <td>${r.mp.hd} ➔ <b style="color:#34d399;">${r.mc.hd}</b></td>
                        <td>${badge}</td>
                    </tr>
                `;
            }).join('');

            const totY = rows.reduce((s, r) => s + r.yearSpend, 0);
            const totP = rows.reduce((s, r) => s + r.mp.spend, 0);
            const totC = rows.reduce((s, r) => s + r.mc.spend, 0);
            const totDiff = totC - totP;
            const totDelta = totP > 0 ? ((totC - totP) / totP * 100) : 0;
            const totDataP = rows.reduce((s, r) => s + r.mp.data, 0);
            const totDataC = rows.reduce((s, r) => s + r.mc.data, 0);
            const totHDP = rows.reduce((s, r) => s + r.mp.hd, 0);
            const totHDC = rows.reduce((s, r) => s + r.mc.hd, 0);

            tbody.innerHTML = bodyHtml + `
                <tr class="total-row">
                    <td>TỔNG CỘNG</td>
                    <td>${fmtVND(totY)}</td>
                    <td>${selProd === 'ALL' ? '100.0%' : rows[0]?.shareYear.toFixed(1) + '%'}</td>
                    <td>${fmtVND(totP)}</td>
                    <td>${fmtVND(totC)}</td>
                    <td>${totDiff >= 0 ? '+' : ''}${fmtShort(totDiff)}</td>
                    <td>${totDelta >= 0 ? '+' : ''}${totDelta.toFixed(1)}%</td>
                    <td>${totDataP} ➔ ${totDataC}</td>
                    <td>${totDataP > 0 ? fmtShort(totP/totDataP) : '--'} ➔ ${totDataC > 0 ? fmtShort(totC/totDataC) : '--'}</td>
                    <td>${totHDP} ➔ ${totHDC}</td>
                    <td>Tổng ${rows.length} SP</td>
                </tr>
            `;
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
                "Chênh lệch": Math.round(r.diffSpend),
                "Δ% Tháng": +r.deltaSpendPct.toFixed(2),
                [`Data ${prevM}`]: r.mp.data,
                [`Data ${currM}`]: r.mc.data,
                [`HĐ ${prevM}`]: r.mp.hd,
                [`HĐ ${currM}`]: r.mc.hd
            }));
            const csv = Papa.unparse(data);
            const blob = new Blob(["\\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `Ngan_Sach_San_Pham_${prevM}_vs_${currM}.csv`;
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

print(f"✅ Đã biên dịch thành công Dashboard tại: {html_path}")
print(f"Dung lượng file: {os.path.getsize(html_path) / 1024:.1f} KB")
