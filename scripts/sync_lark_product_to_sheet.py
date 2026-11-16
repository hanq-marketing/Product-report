import csv
import json
import os
import re
import sys
from collections import defaultdict
import requests
import gspread
from google.oauth2.service_account import Credentials

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "google_service_account.json")
RAW_JSON_FILE = os.path.join(BASE_DIR, "data", "lark_tong_hop_san_pham.json")
PANCAKE_CSV_FILE = os.path.join(BASE_DIR, "data", "bao_cao_cac_tai_khoan_10_2026.csv")
CLEAN_CSV_FILE = os.path.join(BASE_DIR, "data", "lark_product_cleaned.csv")
CLEAN_JSON_FILE = os.path.join(BASE_DIR, "data", "lark_product_cleaned.json")

LARK_HOST = "https://open.larksuite.com"
LARK_APP_TOKEN = "CAtMbm9A0a57cHsBZP6ljKYCgxb"
LARK_TABLE_ID = "tblEr3vySvt58EkK"
TARGET_SHEET_URL = "https://docs.google.com/spreadsheets/d/1V9z5T7BQABDSvsytY0P1kKV5b4lMfpzcFZWghJwUitw/edit"

# Định mức CPL Kế Hoạch theo từng đầu sản phẩm (VNĐ)
CPL_PLAN_MAP = {
    "Data Analyst": 170000,
    "Data Engineer": 200000,
    "Embedded": 180000,
    "BrSE": 250000,
    "AI Engineer": 200000,
    "Cyber Security": 250000,
    "Network Security": 250000,
    "Xueba": 160000,
}


def load_env():
    env = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s and not s.startswith("#") and "=" in s:
                    k, v = s.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def load_pancake_fallback():
    """Đọc số SĐT từ bao_cao_cac_tai_khoan_10_2026.csv làm fallback khi SL DATA TỔNG & SL DATA ADS trên Lark = 0"""
    fallback = defaultdict(int)
    if not os.path.exists(PANCAKE_CSV_FILE):
        return fallback
    with open(PANCAKE_CSV_FILE, "r", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            ym = str(r.get("Ngày") or "")[:7]
            p = str(r.get("Sản phẩm") or "").strip()
            if p == "Embeded":
                p = "Embedded"
            elif p == "AI engineer":
                p = "AI Engineer"
            elif p == "XueBa":
                p = "Xueba"
            fallback[(ym, p)] += int(float(r.get("Sđt theo campain") or 0))
    return fallback


def fetch_lark_records():
    env = load_env()
    app_id = env.get("LARK_APP_ID")
    app_secret = env.get("LARK_APP_SECRET")
    if not app_id or not app_secret:
        with open(RAW_JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    try:
        print(f"[1] Đang kết nối Lark Base ({LARK_APP_TOKEN} / {LARK_TABLE_ID})...")
        auth_url = f"{LARK_HOST}/open-apis/auth/v3/tenant_access_token/internal"
        resp = requests.post(auth_url, json={"app_id": app_id, "app_secret": app_secret}, timeout=20).json()
        if resp.get("code") != 0:
            raise RuntimeError(f"Lỗi xác thực Lark: {resp}")
        token = resp["tenant_access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        records = []
        page_token = None
        while True:
            url = f"{LARK_HOST}/open-apis/bitable/v1/apps/{LARK_APP_TOKEN}/tables/{LARK_TABLE_ID}/records"
            params = {"page_size": 500}
            if page_token:
                params["page_token"] = page_token
            r = requests.get(url, headers=headers, params=params, timeout=30).json()
            if r.get("code") != 0:
                raise RuntimeError(f"Lỗi đọc bảng {LARK_TABLE_ID}: {r}")
            data = r.get("data") or {}
            items = data.get("items") or []
            records.extend(items)
            if not data.get("has_more"):
                break
            page_token = data.get("page_token")

        print(f"-> Đã tải {len(records)} bản ghi trực tiếp từ Lark Base.")
        with open(RAW_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        return records
    except Exception as e:
        print(f"⚠️ Không thể gọi trực tiếp Lark API ({e}), sử dụng bản lưu {RAW_JSON_FILE}...")
        with open(RAW_JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)


def parse_month_str(thang_raw):
    s = str(thang_raw or "").strip()
    m = re.search(r"(\d{1,2})\s*/\s*(\d{4})", s)
    if m:
        month_num = int(m.group(1))
        year_num = int(m.group(2))
        ym = f"{year_num}-{month_num:02d}"
        label = f"Tháng {month_num:02d}/{year_num}"
        return year_num, month_num, ym, label
    return 0, 0, s, s


def map_product_tag(raw_prod):
    p = str(raw_prod or "").strip()
    tag_map = {
        "Data Analyst": ("Data Analyst", "Data & Analytics"),
        "PTDL - Power BI": ("PTDL - Power BI", "Data & Analytics"),
        "Data Engineer": ("Data Engineer", "Data & Analytics"),
        "Embedded": ("Embedded", "Kỹ thuật & Nhúng"),
        "BA": ("BA", "Business Analyst"),
        "BrSE": ("BrSE", "Nhật Bản & BrSE"),
        "IT Tsubasa": ("IT Tsubasa", "Nhật Bản & BrSE"),
        "IT Tsubasa Plus": ("IT Tsubasa Plus", "Nhật Bản & BrSE"),
        "Gambaru": ("Gambaru", "Nhật Bản & BrSE"),
        "Du học Kỹ sư CNTT": ("Du học Kỹ sư CNTT", "Nhật Bản & BrSE"),
        "AI Engineer": ("AI Engineer", "AI & Công nghệ mới"),
        "AI Driven": ("AI Driven", "AI & Công nghệ mới"),
        "AI": ("AI", "AI & Công nghệ mới"),
        "IT Java Backend": ("IT Java Backend", "Lập trình & Phần mềm"),
        "Fullstack IT New": ("Fullstack IT New", "Lập trình & Phần mềm"),
        "Tester": ("Tester", "Lập trình & Phần mềm"),
        "Network Security": ("Cyber Security", "An toàn thông tin"),
        "Cyber Security": ("Cyber Security", "An toàn thông tin"),
        "Xueba": ("Xueba", "Ngoại ngữ & Khác"),
        "PTIT": ("PTIT", "Đại học & Liên kết"),
        "IOC": ("IOC", "Khác"),
    }
    return tag_map.get(p, (p, "Khác"))


def num_val(v):
    if v is None or v == "":
        return 0.0
    if isinstance(v, list):
        v = v[0] if v else 0.0
    try:
        return float(v)
    except Exception:
        return 0.0


def clean_and_tag_records(raw_records):
    print("\n[2] Làm sạch dữ liệu, gắn tag sản phẩm & đối chiếu CPL Kế hoạch...")
    pancake_fallback = load_pancake_fallback()
    cleaned = []
    removed_multi = 0
    removed_empty = 0

    for r in raw_records:
        flds = r.get("fields") or {}
        thang_raw = flds.get("Tháng")
        sp_raw = flds.get("Sản Phẩm")

        if isinstance(sp_raw, list):
            sp_list = [str(x).strip() for x in sp_raw if x]
        elif isinstance(sp_raw, str) and sp_raw.strip():
            sp_list = [sp_raw.strip()]
        else:
            sp_list = []

        if len(sp_list) > 1:
            removed_multi += 1
            continue
        if len(sp_list) == 0 or not thang_raw:
            removed_empty += 1
            continue

        prod_origin = sp_list[0]
        year_num, month_num, ym_code, month_label = parse_month_str(thang_raw)
        if year_num == 0:
            removed_empty += 1
            continue

        tong_cp_sau_thue = round(num_val(flds.get("TỔNG CHI PHÍ ADS SAU THUẾ")))
        cp_fb_mess = round(num_val(flds.get("CHI PHÍ Fb Mess Ads")))
        cp_fb_mess_sau_thue = round(num_val(flds.get("CHI PHÍ FB Mess SAU THUẾ")))
        cp_fb_ldp = round(num_val(flds.get("Chi phí Fb Landing")))
        cp_fb_ldp_sau_thue = round(num_val(flds.get("CHI PHÍ FB Landing SAU THUẾ")))
        cp_tiktok = round(num_val(flds.get("CHI PHÍ Tiktok Ads")))
        cp_tiktok_sau_thue = round(num_val(flds.get("CHI PHÍ TIKTOK ADS SAU THUẾ")))

        sl_mess = int(round(num_val(flds.get("SL MESS"))))
        sl_data_raw_tong = int(round(num_val(flds.get("SL DATA TỔNG"))))
        sl_data_ads = int(round(num_val(flds.get("SL DATA ADS"))))
        sl_data_fb_mess = int(round(num_val(flds.get("SL DATA FB Mess"))))
        sl_data_fb_ldp = int(round(num_val(flds.get("SL DATA FB Landing"))))
        sl_data_tiktok = int(round(num_val(flds.get("SL DATA RAW TIKTOK"))))

        # Ưu tiên SL DATA TỔNG -> SL DATA ADS -> Pancake SĐT để tính CPL chính xác cho cả Embedded, Xueba, Cyber Security
        sl_data_tong = sl_data_raw_tong if sl_data_raw_tong > 0 else (sl_data_ads if sl_data_ads > 0 else pancake_fallback.get((ym_code, prod_origin), 0))

        hd_trong_thang = int(round(num_val(flds.get("HĐ ký trong tháng"))))
        tong_hd = int(round(num_val(flds.get("Tổng HĐ"))))
        hd_het_vong = int(round(num_val(flds.get("HĐ Hết Vòng"))))

        ds_trong_thang = round(num_val(flds.get("DS PHÁT SINH TRONG THÁNG")))
        ds_tong = round(num_val(flds.get("DOANH SỐ TỔNG")))

        if (
            tong_cp_sau_thue == 0
            and cp_fb_mess == 0
            and cp_fb_ldp == 0
            and cp_tiktok == 0
            and sl_data_tong == 0
            and sl_mess == 0
            and tong_hd == 0
            and ds_tong == 0
        ):
            removed_empty += 1
            continue

        tag_sp, nhom_sp = map_product_tag(prod_origin)

        cpl_tong = round(tong_cp_sau_thue / sl_data_tong) if sl_data_tong > 0 else round(num_val(flds.get("CPL TỔNG")))
        cpl_plan = CPL_PLAN_MAP.get(tag_sp) or CPL_PLAN_MAP.get(prod_origin) or 0
        cpl_diff = (cpl_tong - cpl_plan) if (cpl_tong > 0 and cpl_plan > 0) else 0
        cpl_diff_pct = round((cpl_tong - cpl_plan) / cpl_plan * 100, 1) if (cpl_tong > 0 and cpl_plan > 0) else 0.0

        if cpl_plan > 0 and cpl_tong > 0:
            if cpl_tong > cpl_plan:
                cpl_alert = f"🚨 VƯỢT KH (+{cpl_diff_pct}%)"
            else:
                cpl_alert = f"✅ ĐẠT KH ({cpl_diff_pct}%)"
        elif cpl_plan > 0 and tong_cp_sau_thue > 0 and sl_data_tong == 0:
            cpl_alert = "⚠️ Có chi phí - Chưa ghi Data"
        else:
            cpl_alert = "--"

        cp_per_mess = round(cp_fb_mess_sau_thue / sl_mess) if sl_mess > 0 else round(num_val(flds.get("CP/MESS")))
        cp_per_hd = round(tong_cp_sau_thue / hd_het_vong) if hd_het_vong > 0 else round(num_val(flds.get("CP/HĐ - hết vòng")))
        cp_ds_pct = round((tong_cp_sau_thue / ds_tong) * 100, 2) if ds_tong > 0 else round(num_val(flds.get("CP/DS TỔNG")) * 100, 2)

        cleaned.append({
            "Mã Tháng": ym_code,
            "Năm": year_num,
            "Tháng Số": month_num,
            "Tháng": month_label,
            "Tag Sản Phẩm": tag_sp,
            "Nhóm Sản Phẩm": nhom_sp,
            "Sản Phẩm Gốc": prod_origin,
            "Tổng Chi Phí Ads (Sau Thuế)": tong_cp_sau_thue,
            "Chi Phí FB Mess (Sau Thuế)": cp_fb_mess_sau_thue,
            "Chi Phí FB Landing (Sau Thuế)": cp_fb_ldp_sau_thue,
            "Chi Phí TikTok (Sau Thuế)": cp_tiktok_sau_thue,
            "Chi Phí FB Mess (Trước Thuế)": cp_fb_mess,
            "Chi Phí FB Landing (Trước Thuế)": cp_fb_ldp,
            "Chi Phí TikTok (Trước Thuế)": cp_tiktok,
            "SL Mess": sl_mess,
            "SL Data Tổng": sl_data_tong,
            "SL Data FB Mess": sl_data_fb_mess,
            "SL Data FB Landing": sl_data_fb_ldp,
            "SL Data TikTok": sl_data_tiktok,
            "CPL Tổng": cpl_tong,
            "CPL Kế Hoạch": cpl_plan,
            "Chênh Lệch CPL": cpl_diff,
            "% Vượt/Đạt CPL KH": cpl_diff_pct,
            "Cảnh Báo CPL": cpl_alert,
            "CP/Mess": cp_per_mess,
            "HĐ Ký Trong Tháng": hd_trong_thang,
            "Tổng HĐ": tong_hd,
            "HĐ Hết Vòng": hd_het_vong,
            "CP/HĐ Hết Vòng": cp_per_hd,
            "Doanh Số Trong Tháng": ds_trong_thang,
            "Doanh Số Tổng": ds_tong,
            "CP/DS Tổng (%)": cp_ds_pct,
            "Record ID": r.get("record_id") or r.get("id") or "",
        })

    cleaned.sort(key=lambda x: (x["Mã Tháng"], -x["Tổng Chi Phí Ads (Sau Thuế)"]))

    fieldnames = list(cleaned[0].keys()) if cleaned else []
    with open(CLEAN_CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned)

    with open(CLEAN_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"-> Đã lưu {len(cleaned)} bản ghi kèm CPL Kế hoạch & Cảnh báo tại: {CLEAN_CSV_FILE}")
    return cleaned


def push_to_google_sheet(cleaned_rows):
    print(f"\n[3] Đang đẩy dữ liệu sạch & Bảng So Sánh CPL lên Google Sheets: {TARGET_SHEET_URL} ...")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    sh = client.open_by_url(TARGET_SHEET_URL)
    print(f"-> Đã mở thành công file Google Sheet: '{sh.title}'")

    headers = list(cleaned_rows[0].keys())
    matrix = [headers]
    for r in cleaned_rows:
        matrix.append([r[h] for h in headers])

    # 1. Tab 1: Data_San_Pham_Cleaned
    ws_first = sh.get_worksheet(0)
    if ws_first.title != "Data_San_Pham_Cleaned":
        try:
            ws_first.update_title("Data_San_Pham_Cleaned")
        except Exception:
            pass

    ws_first.clear()
    ws_first.update(matrix, "A1", value_input_option="USER_ENTERED")
    ws_first.format("A1:AG1", {"textFormat": {"bold": True}})
    print(f"  ✓ Đã ghi {len(cleaned_rows)} dòng (kèm CPL Thực tế, CPL Kế hoạch, Cảnh báo CPL) vào tab '{ws_first.title}'.")

    # 2. Tab 2: So_Sanh_CPL_2026 (Bảng đối chiếu CPL Thực tế trung bình các tháng vs CPL Kế hoạch)
    rows_2026 = [r for r in cleaned_rows if int(r["Năm"]) == 2026]
    months_2026 = sorted(set(r["Mã Tháng"] for r in rows_2026))

    prod_stats = {}
    for r in rows_2026:
        p = r["Tag Sản Phẩm"]
        st = prod_stats.setdefault(p, {
            "plan": r["CPL Kế Hoạch"],
            "spend_all": 0,
            "spend_with_data": 0,
            "data_all": 0,
            "months_cpl": {},
            "months_over": 0,
            "months_active": 0
        })
        sp = r["Tổng Chi Phí Ads (Sau Thuế)"]
        dt = r["SL Data Tổng"]
        cpl_m = r["CPL Tổng"]
        st["spend_all"] += sp
        if dt > 0:
            st["spend_with_data"] += sp
            st["data_all"] += dt
        if cpl_m > 0:
            st["months_cpl"][r["Mã Tháng"]] = cpl_m
            st["months_active"] += 1
            if st["plan"] > 0 and cpl_m > st["plan"]:
                st["months_over"] += 1

    cpl_headers = [
        "Tag Sản Phẩm",
        "CPL Kế Hoạch (VNĐ)",
        "CPL TB Năm 2026 (Tính trên tháng có Data)",
        "CPL TB Cộng Trung Bình Các Tháng",
        "Chênh Lệch vs KH (VNĐ)",
        "% Vượt / Đạt KH",
        "Số Tháng Vượt KH",
        "Cảnh Báo CPL Năm 2026",
        "Tổng Chi Tiêu 2026",
        "Tổng Data 2026"
    ] + [f"CPL T{m.split('-')[1]}/2026" for m in months_2026]

    cpl_rows = [cpl_headers]
    for p, st in sorted(prod_stats.items(), key=lambda x: (x[1]["plan"] == 0, -x[1]["spend_all"])):
        plan = st["plan"]
        cpl_weighted = round(st["spend_with_data"] / st["data_all"]) if st["data_all"] > 0 else 0
        cpl_vals = list(st["months_cpl"].values())
        cpl_avg_months = round(sum(cpl_vals) / len(cpl_vals)) if cpl_vals else 0
        cpl_ref = cpl_weighted if cpl_weighted > 0 else cpl_avg_months

        diff = (cpl_ref - plan) if (plan > 0 and cpl_ref > 0) else 0
        diff_pct = round((cpl_ref - plan) / plan * 100, 1) if (plan > 0 and cpl_ref > 0) else 0.0

        if plan > 0 and cpl_ref > 0:
            alert_str = f"🚨 VƯỢT KẾ HOẠCH (+{diff_pct}%)" if cpl_ref > plan else f"✅ ĐẠT KẾ HOẠCH ({diff_pct}%)"
        elif plan > 0:
            alert_str = "⚠️ Chưa đủ Data tính CPL"
        else:
            alert_str = "Chưa đặt KH"

        m_cells = []
        for m in months_2026:
            v = st["months_cpl"].get(m, 0)
            if v > 0 and plan > 0:
                flag = " 🚨" if v > plan else " ✅"
                m_cells.append(f"{v:,}{flag}")
            elif v > 0:
                m_cells.append(f"{v:,}")
            else:
                m_cells.append("--")

        cpl_rows.append([
            p,
            plan if plan > 0 else "--",
            cpl_weighted if cpl_weighted > 0 else "--",
            cpl_avg_months if cpl_avg_months > 0 else "--",
            diff if (plan > 0 and cpl_ref > 0) else "--",
            f"{diff_pct:+.1f}%" if (plan > 0 and cpl_ref > 0) else "--",
            f"{st['months_over']}/{st['months_active']} tháng" if plan > 0 else "--",
            alert_str,
            st["spend_all"],
            st["data_all"],
            *m_cells
        ])

    try:
        ws_cpl = sh.worksheet("So_Sanh_CPL_2026")
    except gspread.exceptions.WorksheetNotFound:
        ws_cpl = sh.add_worksheet(title="So_Sanh_CPL_2026", rows="100", cols="25")

    ws_cpl.clear()
    ws_cpl.update(cpl_rows, "A1", value_input_option="USER_ENTERED")
    ws_cpl.format("A1:U1", {"textFormat": {"bold": True}})
    print(f"  ✓ Đã cập nhật tab 'So_Sanh_CPL_2026' đối chiếu CPL Kế hoạch vs CPL Thực tế các tháng.")

    # 3. Tab 3: Pivot_Chi_Tieu_2026
    prods_2026 = {}
    for r in rows_2026:
        p = r["Tag Sản Phẩm"]
        prods_2026.setdefault(p, {})[r["Mã Tháng"]] = r["Tổng Chi Phí Ads (Sau Thuế)"]

    pivot_headers = ["Tag Sản Phẩm", "CPL Kế Hoạch", "CPL TB 2026", "Cảnh Báo CPL", "Tổng Chi Tiêu 2026", "% Tỷ Trọng 2026"] + [f"Tháng {m.split('-')[1]}/2026" for m in months_2026]
    total_2026_all = sum(sum(m_map.values()) for m_map in prods_2026.values()) or 1

    pivot_rows = [pivot_headers]
    for p, m_map in sorted(prods_2026.items(), key=lambda x: sum(x[1].values()), reverse=True):
        tot_p = sum(m_map.values())
        share_p = round(tot_p / total_2026_all * 100, 2)
        st = prod_stats[p]
        plan = st["plan"]
        cpl_w = round(st["spend_with_data"] / st["data_all"]) if st["data_all"] > 0 else 0
        alert_p = ("🚨 VƯỢT KH" if cpl_w > plan else "✅ ĐẠT KH") if (plan > 0 and cpl_w > 0) else "--"
        row_vals = [p, plan or "--", cpl_w or "--", alert_p, tot_p, f"{share_p}%"] + [m_map.get(m, 0) for m in months_2026]
        pivot_rows.append(row_vals)

    tot_row = ["TỔNG CỘNG NĂM 2026", "--", "--", "--", total_2026_all, "100%"] + [
        sum(prods_2026[p].get(m, 0) for p in prods_2026) for m in months_2026
    ]
    pivot_rows.append(tot_row)

    try:
        ws_pivot = sh.worksheet("Pivot_Chi_Tieu_2026")
    except gspread.exceptions.WorksheetNotFound:
        ws_pivot = sh.add_worksheet(title="Pivot_Chi_Tieu_2026", rows="100", cols="25")

    ws_pivot.clear()
    ws_pivot.update(pivot_rows, "A1", value_input_option="USER_ENTERED")
    ws_pivot.format("A1:S1", {"textFormat": {"bold": True}})
    print(f"  ✓ Đã cập nhật bảng 'Pivot_Chi_Tieu_2026' kèm CPL Kế hoạch & Cảnh báo.")


if __name__ == "__main__":
    raw = fetch_lark_records()
    cleaned = clean_and_tag_records(raw)
    push_to_google_sheet(cleaned)
    print("\n✅ HOÀN TẤT CẬP NHẬT CPL KẾ HOẠCH & CẢNH BÁO LÊN GOOGLE SHEETS!")
