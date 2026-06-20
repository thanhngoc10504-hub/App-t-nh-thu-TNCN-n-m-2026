```python
import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="App Tính Thuế TNCN Việt Nam 2026",
    page_icon="💰",
    layout="centered"
)

# =========================
# LOGO
# =========================
try:
    st.image("logo.jpg", width=250)
except:
    st.warning("Không tìm thấy file logo.jpg")

# =========================
# TIÊU ĐỀ
# =========================
st.markdown("### 📝 TS. VŨ ĐỨC BÌNH")

st.title("💰 Ứng Dụng Tính Thuế Thu Nhập Cá Nhân")

st.write(
    "Cập nhật đầy đủ Lương, Thưởng, Tăng ca, Phụ cấp "
    "theo quy định thuế TNCN năm 2026"
)

st.divider()

# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📋 Nhập thông tin thu nhập tháng này")

gross_salary = st.number_input(
    "1. Lương đóng BHXH (VND)",
    min_value=0,
    value=30000000,
    step=500000,
    format="%d"
)

gross_bonus_pay = st.number_input(
    "2. Tiền thưởng / Bonus (VND)",
    min_value=0,
    value=0,
    step=500000,
    format="%d"
)

overtime_pay = st.number_input(
    "3. Tiền tăng ca / làm thêm giờ (VND)",
    min_value=0,
    value=0,
    step=500000,
    format="%d"
)

st.markdown("### 4. Các khoản phụ cấp")

col1, col2 = st.columns(2)

with col1:
    lunch_allowance = st.number_input(
        "Phụ cấp ăn trưa (VND)",
        min_value=0,
        value=0,
        step=50000
    )

with col2:
    other_allowance = st.number_input(
        "Phụ cấp điện thoại, xăng xe (VND)",
        min_value=0,
        value=0,
        step=50000
    )

dependents = st.number_input(
    "5. Số người phụ thuộc",
    min_value=0,
    value=1,
    step=1
)

st.divider()

# =========================
# HÀM TÍNH THUẾ
# =========================
def tinh_thue_tncn(
    gross,
    bonus,
    overtime,
    lunch,
    other,
    deps
):
    # Tổng thu nhập
    total_income = gross + bonus + overtime + lunch + other

    # Bảo hiểm
    bhxh = gross * 0.08
    bhyt = gross * 0.015
    bhtn = gross * 0.01

    total_insurance = bhxh + bhyt + bhtn

    # Giảm trừ gia cảnh
    self_reduction = 15_500_000
    dependent_reduction = deps * 6_200_000

    total_reduction = (
        self_reduction +
        dependent_reduction
    )

    # Khoản miễn thuế
    exempt_lunch = min(lunch, 730_000)

    exempt_allowance = other

    total_exempt_income = (
        overtime +
        exempt_lunch +
        exempt_allowance
    )

    # Thu nhập tính thuế
    assessable_income = max(
        0,
        total_income
        - total_exempt_income
        - total_insurance
        - total_reduction
    )

    # Biểu thuế
    brackets = [
        {
            "limit": 10_000_000,
            "rate": 0.05,
            "desc": "Bậc 1 (5%)"
        },
        {
            "limit": 30_000_000,
            "rate": 0.10,
            "desc": "Bậc 2 (10%)"
        },
        {
            "limit": 60_000_000,
            "rate": 0.20,
            "desc": "Bậc 3 (20%)"
        },
        {
            "limit": 100_000_000,
            "rate": 0.30,
            "desc": "Bậc 4 (30%)"
        },
        {
            "limit": float("inf"),
            "rate": 0.35,
            "desc": "Bậc 5 (35%)"
        }
    ]

    tax = 0
    tax_breakdown = []

    remaining_income = assessable_income
    previous_limit = 0

    for b in brackets:

        if remaining_income <= 0:
            break

        range_size = b["limit"] - previous_limit

        taxable_amount = min(
            remaining_income,
            range_size
        )

        tax_amount = taxable_amount * b["rate"]

        tax += tax_amount

        tax_breakdown.append({
            "Bậc thuế": b["desc"],
            "Thu nhập tính thuế":
                f"{taxable_amount:,.0f} VND",
            "Thuế phải nộp":
                f"{tax_amount:,.0f} VND"
        })

        remaining_income -= taxable_amount
        previous_limit = b["limit"]

    # Lương thực nhận
    net_salary = (
        total_income
        - total_insurance
        - tax
    )

    return {
        "total_income": total_income,
        "bhxh": bhxh,
        "bhyt": bhyt,
        "bhtn": bhtn,
        "total_insurance": total_insurance,
        "dependent_reduction": dependent_reduction,
        "exempt_lunch": exempt_lunch,
        "exempt_allowance": exempt_allowance,
        "assessable_income": assessable_income,
        "tax": tax,
        "net_salary": net_salary,
        "tax_breakdown": tax_breakdown
    }

# =========================
# NÚT TÍNH THUẾ
# =========================
if st.button(
    "🧮 Tính Thuế & Nhận Kết Quả",
    type="primary"
):

    res = tinh_thue_tncn(
        gross_salary,
        gross_bonus_pay,
        overtime_pay,
        lunch_allowance,
        other_allowance,
        dependents
    )

    st.divider()

    st.subheader("🎯 Kết Quả Tóm Tắt")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tổng thu nhập",
            f"{res['total_income']:,.0f} VND"
        )

        st.metric(
            "Tổng bảo hiểm",
            f"{res['total_insurance']:,.0f} VND"
        )

    with col2:
        st.metric(
            "Thuế TNCN",
            f"{res['tax']:,.0f} VND"
        )

        st.metric(
            "Thực nhận (NET)",
            f"{res['net_salary']:,.0f} VND"
        )

    st.divider()

    st.subheader("📜 Giải trình chi tiết")

    st.markdown(f"""
- **Tổng thu nhập:** `{res['total_income']:,.0f} VND`

- **Miễn thuế tăng ca:** `{overtime_pay:,.0f} VND`

- **Miễn thuế ăn trưa:** `{res['exempt_lunch']:,.0f} VND`

- **Miễn thuế phụ cấp:** `{res['exempt_allowance']:,.0f} VND`

- **BHXH:** `{res['bhxh']:,.0f} VND`

- **BHYT:** `{res['bhyt']:,.0f} VND`

- **BHTN:** `{res['bhtn']:,.0f} VND`

- **Giảm trừ bản thân:** `15,500,000 VND`

- **Giảm trừ người phụ thuộc:** `{res['dependent_reduction']:,.0f} VND`

- **Thu nhập tính thuế:** `{res['assessable_income']:,.0f} VND`
""")

    if res["tax"] > 0:
        st.subheader("📊 Chi tiết thuế theo từng bậc")
        st.table(res["tax_breakdown"])
    else:
        st.success(
            "Sau khi giảm trừ gia cảnh và các khoản miễn thuế, "
            "thu nhập tính thuế bằng 0 nên không phát sinh thuế TNCN."
        )
```
