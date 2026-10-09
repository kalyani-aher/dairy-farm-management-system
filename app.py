import streamlit as st
import sqlite3
import pandas as pd

# ============================================================
# PROFESSIONAL UI STYLING
# ============================================================

st.markdown("""
<style>

    /* Streamlit top header */
header[data-testid="stHeader"] {
    background-color: #ffffff !important;
}

    /* Main application background */
    .stApp {
        background-color: #F5FFFA !important;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Dashboard title */
    .dashboard-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    /* Custom metric cards */
        .metric-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        min-height: 120px;
        transition: all 0.2s ease;
    }

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    border-color: #c8ddc8;
}

.quick-nav-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    min-height: 145px;
    transition: all 0.2s ease;
}

.quick-nav-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 7px 20px rgba(0,0,0,0.09);
    border-color: #9fc49f;
}

    .metric-icon {
        font-size: 25px;
        margin-bottom: 8px;
    }

    .metric-label {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 5px;
    }

    .metric-value {
        font-size: 25px;
        font-weight: 700;
        color: #111827;
    }

    /* Section headings */
    .section-title {
        font-size: 21px;
        font-weight: 650;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

/* Fix text visibility on light background */

    .stApp,
    .stApp p,
    .stApp span,
    .stApp div {
        color: #111827;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    [data-testid="stSidebar"] * {
        color: #111827 !important;
    }

    /* Radio navigation */
    [data-testid="stSidebar"] label {
        color: #111827 !important;
    }

    /* Captions */
    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: #6b7280 !important;
    }

    /* Soft gray input labels */
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] span {
        color: #6b7280 !important;
        font-weight: 500 !important;
    }

    /* Light green input controls */
    [data-testid="stTextInput"] > div,
    [data-testid="stTextInput"] > div > div,
    [data-testid="stNumberInput"] > div,
    [data-testid="stNumberInput"] > div > div,
    [data-testid="stDateInput"] > div,
    [data-testid="stDateInput"] > div > div,
    [data-testid="stDateInput"] [data-baseweb="input"],
    [data-baseweb="select"],
    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div {
        background-color: #f1f8f1 !important;
        border-color: #c8ddc8 !important;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input {
        background-color: #f1f8f1 !important;
        color: #111827 !important;
    }

    /* Number input +/- buttons */
    [data-testid="stNumberInput"] button {
        background-color: #e8f3e8 !important;
        color: #4f6f52 !important;
        border-color: #c8ddc8 !important;
    }

    [data-testid="stNumberInput"] button:hover {
        background-color: #d9ead9 !important;
        color: #355e3b !important;
    }

    /* Cow Management options as button boxes */

    [data-testid="stRadio"] [role="radiogroup"] {
        display: flex !important;
        gap: 12px !important;
        flex-wrap: wrap !important;
    }

    [data-testid="stRadio"] [role="radiogroup"] label {
        background-color: #ffffff !important;
        border: 1px solid #c8ddc8 !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
        min-height: 42px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stRadio"] [role="radiogroup"] label:hover {
        background-color: #f1f8f1 !important;
        border-color: #8fb88f !important;
    }

    [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
        background-color: #e3f1e3 !important;
        border: 2px solid #6f9f6f !important;
    }

    [data-testid="stRadio"] [role="radiogroup"] label p {
        color: #111827 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Dairy Farm Management",
    page_icon="🐄",
    layout="wide"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    conn = sqlite3.connect("dairy_farm.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # COWS TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cow_id TEXT UNIQUE NOT NULL,
            breed TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    # --------------------------------------------------------
    # MILK RECORDS TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS milk_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cow_id TEXT NOT NULL,
            date TEXT NOT NULL,
            morning_milk REAL DEFAULT 0,
            evening_milk REAL DEFAULT 0,
            total_milk REAL DEFAULT 0
        )
    """)

    # --------------------------------------------------------
    # HEALTH RECORDS TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cow_id TEXT NOT NULL,
            record_type TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            next_due_date TEXT
        )
    """)

    # --------------------------------------------------------
    # FINANCE RECORDS TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


# Create tables when application starts
create_tables()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🐄 Dairy Farm")
st.sidebar.caption("Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🐄 Cow Management",
        "🥛 Milk Management",
        "💉 Health & Vaccination",
        "💰 Income & Expenses",
        "📊 Reports"
    ]
)
# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    from datetime import date, timedelta

    today = date.today()
    today_str = str(today)

    # ========================================================
    # PROFESSIONAL DASHBOARD HEADER
    # ========================================================

    st.markdown(
        f"""
        <div class="dashboard-title">
            🐄 Dairy Farm Dashboard
        </div>

        <div class="dashboard-subtitle">
            Monitor your cows, milk production, health and finances
            from one place.
        </div>

        <div style="
            color:#6b7280;
            font-size:14px;
            margin-top:-12px;
            margin-bottom:20px;
        ">
            📅 {today.strftime("%A, %d %B %Y")}
        </div>
        """,
        unsafe_allow_html=True
    )

    conn = get_connection()

    # ========================================================
    # BASIC COUNTS
    # ========================================================

    total_cows = conn.execute(
        """
        SELECT COUNT(*)
        FROM cows
        """
    ).fetchone()[0]

    # ========================================================
    # TODAY'S MILK
    # ========================================================

    today_milk = conn.execute(
        """
        SELECT COALESCE(SUM(total_milk), 0)
        FROM milk_records
        WHERE date = ?
        """,
        (today_str,)
    ).fetchone()[0]

    # ========================================================
    # TODAY'S INCOME
    # ========================================================

    today_income = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM finance_records
        WHERE record_type = 'Income'
        AND date = ?
        """,
        (today_str,)
    ).fetchone()[0]

    # ========================================================
    # TODAY'S EXPENSES
    # ========================================================

    today_expenses = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM finance_records
        WHERE record_type = 'Expense'
        AND date = ?
        """,
        (today_str,)
    ).fetchone()[0]

    today_profit = today_income - today_expenses

    # ========================================================
    # HEALTH / VACCINATION ALERTS
    # ========================================================

    upcoming_date = str(
    today + timedelta(days=30)
    )

    # --------------------------------------------------------
    # OVERDUE RECORDS
    # --------------------------------------------------------

    overdue_records = conn.execute(
        """
        SELECT
            cow_id,
            record_type,
            next_due_date
        FROM health_records
        WHERE next_due_date IS NOT NULL
        AND next_due_date < ?
        ORDER BY next_due_date
        """,
        (today_str,)
    ).fetchall()

    # --------------------------------------------------------
    # UPCOMING RECORDS
    # --------------------------------------------------------

    upcoming_records = conn.execute(
        """
        SELECT
            cow_id,
            record_type,
            next_due_date
        FROM health_records
        WHERE next_due_date IS NOT NULL
        AND next_due_date >= ?
        AND next_due_date <= ?
        ORDER BY next_due_date
        """,
        (
            today_str,
            upcoming_date
        )
    ).fetchall()

    # ========================================================
    # LAST 30 DAYS MILK
    # ========================================================

    thirty_days_ago = str(
        today - timedelta(days=29)
    )

    milk_last_30_days = conn.execute(
        """
        SELECT
            date,
            SUM(total_milk) AS total_milk
        FROM milk_records
        WHERE date >= ?
        AND date <= ?
        GROUP BY date
        ORDER BY date
        """,
        (
            thirty_days_ago,
            today_str
        )
    ).fetchall()

    conn.close()

    # ========================================================
    # HEADER
    # ========================================================

    st.divider()

    st.markdown("""
    <div class="section-title">
        📅 Today's Farm Summary
    </div>
    <div style="
        color:#6b7280;
        font-size:14px;
        margin-bottom:15px;
    ">
        A quick overview of today's farm activity.
    </div>
""", unsafe_allow_html=True)

    # ========================================================
    # MOBILE-FRIENDLY SUMMARY CARDS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">🐄</div>
                <div class="metric-label">Total Cows</div>
                <div class="metric-value">{total_cows}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">🥛</div>
                <div class="metric-label">Today's Milk</div>
                <div class="metric-value">
                    {today_milk:.1f} L
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">💰</div>
                <div class="metric-label">Today's Income</div>
                <div class="metric-value">
                    ₹{today_income:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">💸</div>
                <div class="metric-label">Today's Expenses</div>
                <div class="metric-value">
                    ₹{today_expenses:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">💵</div>
            <div class="metric-label">Today's Profit</div>
            <div class="metric-value">
                ₹{today_profit:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    
    # ========================================================
    # MILK PRODUCTION CHART
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            📈 Milk Production — Last 30 Days
        </div>

        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:15px;
        ">
            Daily milk production recorded across the farm.
        </div>
        """,
        unsafe_allow_html=True
    )

    if milk_last_30_days:

        milk_chart = pd.DataFrame(
            milk_last_30_days,
            columns=[
                "Date",
                "Total Milk (L)"
            ]
        )

        milk_chart["Date"] = pd.to_datetime(
            milk_chart["Date"]
        )

        st.bar_chart(
            milk_chart,
            x="Date",
            y="Total Milk (L)",
            height=280,
            use_container_width=True
        )

    else:

        st.info(
            "🥛 No milk records available for the last 30 days."
        )

    st.divider()

    # ========================================================
    # MILK PERFORMANCE SUMMARY
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            📈 Milk Performance — Last 30 Days
        </div>

        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:15px;
        ">
            A quick summary of your farm's milk production.
        </div>
        """,
        unsafe_allow_html=True
    )

    if milk_last_30_days:

        total_30_day_milk = sum(
            record[1]
            for record in milk_last_30_days
        )

        average_daily_milk = (
            total_30_day_milk / len(milk_last_30_days)
        )

        highest_milk_day = max(
            milk_last_30_days,
            key=lambda record: record[1]
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">🥛</div>
                    <div class="metric-label">Total Milk</div>
                    <div class="metric-value">
                        {total_30_day_milk:.1f} L
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">📊</div>
                    <div class="metric-label">Average Daily Milk</div>
                    <div class="metric-value">
                        {average_daily_milk:.1f} L
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">🏆</div>
                <div class="metric-label">Highest Production</div>
                <div class="metric-value">
                    {highest_milk_day[1]:.1f} L
                </div>
                <div class="metric-label">
                    {pd.to_datetime(highest_milk_day[0]).strftime('%d-%m-%Y')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:

        st.info(
            "🥛 No milk production data available."
        )

    st.divider()

    # ========================================================
    # FINANCE PERFORMANCE — LAST 30 DAYS
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            💰 Finance Performance - Last 30 Days
        </div>

        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:15px;
        ">
            A quick overview of your farms income, expenses and balance.
        </div>
        """,
        unsafe_allow_html=True
    )

    thirty_days_ago = str(
        today - timedelta(days=29)
    )

    conn = get_connection()

    finance_summary = conn.execute(
        """
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN record_type = 'Income'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS total_income,

            COALESCE(
                SUM(
                    CASE
                        WHEN record_type = 'Expense'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS total_expenses

        FROM finance_records

        WHERE date >= ?
        AND date <= ?
        """,
        (
            thirty_days_ago,
            today_str
        )
    ).fetchone()

    conn.close()

    total_30_day_income = finance_summary[0]
    total_30_day_expenses = finance_summary[1]

    total_30_day_balance = (
        total_30_day_income
        - total_30_day_expenses
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">💰</div>
                <div class="metric-label">Total Income</div>
                <div class="metric-value">
                    ₹{total_30_day_income:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">💸</div>
                <div class="metric-label">Total Expenses</div>
                <div class="metric-value">
                    ₹{total_30_day_expenses:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">💵</div>
            <div class="metric-label">Net Balance</div>
            <div class="metric-value">
                ₹{total_30_day_balance:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    # ========================================================
    # HEALTH & VACCINATION ALERTS
    # ========================================================

    st.markdown(
    """
    <div class="section-title">
        💉 Health & Vaccination Alerts
    </div>

    <div style="
        color:#6b7280;
        font-size:14px;
        margin-bottom:15px;
    ">
        Monitor overdue and upcoming health or vaccination records.
    </div>
    """,
    unsafe_allow_html=True
)

    # ----------------------------------------------------
    # OVERDUE RECORDS
    # ----------------------------------------------------

    if overdue_records:

        st.error(
            f"🔴 {len(overdue_records)} health/vaccination "
            "record(s) are overdue."
        )

        overdue_df = pd.DataFrame(
            overdue_records,
            columns=[
                "Cow ID",
                "Record Type",
                "Due Date"
            ]
        )

        overdue_df["Due Date"] = pd.to_datetime(
            overdue_df["Due Date"]
        ).dt.strftime("%d-%m-%Y")

        st.dataframe(
            overdue_df,
            use_container_width=True,
            hide_index=True
        )

    # ----------------------------------------------------
    # UPCOMING RECORDS
    # ----------------------------------------------------

    if upcoming_records:

        st.warning(
            f"🟡 {len(upcoming_records)} health/vaccination "
            "record(s) are due within 30 days."
        )

        upcoming_df = pd.DataFrame(
            upcoming_records,
            columns=[
                "Cow ID",
                "Record Type",
                "Due Date"
            ]
        )

        upcoming_df["Due Date"] = pd.to_datetime(
            upcoming_df["Due Date"]
        ).dt.strftime("%d-%m-%Y")

        st.dataframe(
            upcoming_df,
            use_container_width=True,
            hide_index=True
        )

    # ----------------------------------------------------
    # NO ALERTS     
    # ----------------------------------------------------

    if not overdue_records and not upcoming_records:

        st.success(
            "✅ No overdue or upcoming health/vaccination "
            "records."
        )
    # ========================================================
    # FARM STATUS
    # ========================================================

    st.markdown("""
        <div class="section-title">
            🌾 Farm Status
        </div>
        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:15px;
        ">
            A quick look at your farm's current activity and status.
        </div>
    """, unsafe_allow_html=True)

    if total_cows > 0:

        st.success(
            "🐄 Farm is active"
        )

        st.write(
            f"**{total_cows}** cows registered."
        )

    else:

        st.warning(
            "⚠️ No cows registered yet."
        )

    st.write("")

    if today_milk > 0:

        st.success(
            f"🥛 {today_milk:.1f} L milk recorded today."
        )

    else:

        st.info(
            "🥛 No milk recorded today."
        )

    st.write("")

    if today_profit > 0:

        st.markdown(
            f"""
            <div style="
                background:#eaf7ea;
                border:1px solid #b9dfb9;
                border-radius:10px;
                padding:12px 15px;
                margin-top:5px;
            ">
                <div style="color:#2f6b3a; font-size:14px; font-weight:600;">
                    💵 Today's balance
                </div>
                <div style="color:#24552d; font-size:20px; font-weight:700;">
                    ₹{today_profit:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif today_profit < 0:

        st.markdown(
            f"""
            <div style="
                background:#fff0f0;
                border:1px solid #f0b8b8;
                border-radius:10px;
                padding:12px 15px;
                margin-top:5px;
            ">
                <div style="color:#a33a3a; font-size:14px; font-weight:600;">
                    💸 Today's balance
                </div>
                <div style="color:#8f2929; font-size:20px; font-weight:700;">
                    ₹{today_profit:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "💵 No income or expenses recorded today."
        )

    st.divider()

    # ========================================================
    # QUICK NAVIGATION
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            🚀 Quick Navigation
        </div>

        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:18px;
        ">
            Quickly access the main areas of your dairy farm system.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Cow Management
    st.markdown(
        """
        <div class="metric-card" style="margin-bottom:14px;">
            <div class="metric-icon">🐄</div>
            <div class="metric-label">Cow Management</div>
            <div style="
                color:#6b7280;
                font-size:14px;
                margin-top:8px;
                line-height:1.5;
            ">
                Manage cow details, breeds and ages.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Milk Management
    st.markdown(
        """
        <div class="metric-card" style="margin-bottom:14px;">
            <div class="metric-icon">🥛</div>
            <div class="metric-label">Milk Management</div>
            <div style="
                color:#6b7280;
                font-size:14px;
                margin-top:8px;
                line-height:1.5;
            ">
                Record and monitor daily milk production.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Income & Expenses
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-label">Income & Expenses</div>
            <div style="
                color:#6b7280;
                font-size:14px;
                margin-top:8px;
                line-height:1.5;
            ">
                Track farm income, expenses and balance.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ============================================================
# COW MANAGEMENT
# ============================================================

elif page == "🐄 Cow Management":

    st.markdown(
    """
    <div class="dashboard-title">
        🐄 Cow Management
    </div>

    <div class="dashboard-subtitle">
        Manage cow details, breeds and ages from one place.
    </div>
    """,
    unsafe_allow_html=True
)

    cow_option = st.radio(
        "🐄 Manage Cows",
        [
            "📋 All Cows",
            "➕ Add Cow",
            "✏️ Update Cow",
            "🗑️ Delete Cow"
        ],
        horizontal=False,
        key="cow_action",
    )

    # ========================================================
    # ALL COWS
    # ========================================================

    if cow_option == "📋 All Cows":

        st.markdown(
    """
    <div class="section-title">
        📋 All Cows
    </div>

    <div style="
        color:#6b7280;
        font-size:14px;
        margin-bottom:15px;
    ">
        View all registered cows and their basic details.
    </div>
    """,
    unsafe_allow_html=True
)

        conn = get_connection()

        cows = conn.execute(
            """
            SELECT cow_id, breed, age
            FROM cows
            ORDER BY cow_id
            """
        ).fetchall()

        conn.close()

        if cows:

            st.dataframe(
                cows,
                column_config={
                    1: "Cow ID",
                    2: "Breed",
                    3: "Age (Years)"
                },
                width="stretch",
                hide_index=True
            )

        else:

            st.info("No cows added yet.")

    # ========================================================
    # ADD COW
    # ========================================================

    elif cow_option == "➕ Add Cow":

        st.markdown(
    """
    <div class="section-title">
        ➕ Add New Cow
    </div>

    <div style="
        color:#6b7280;
        font-size:14px;
        margin-bottom:15px;
    ">
        Add a new cow and save its basic details to the farm.
    </div>
    """,
    unsafe_allow_html=True
)

        # MOBILE-FRIENDLY COW DETAILS

        col1, col2 = st.columns(2)

        with col1:
            cow_id = st.text_input(
                "Cow ID",
                placeholder="Example: C001",
                key="add_cow_id"
            )

        with col2:
            breed = st.text_input(
                "Breed",
                placeholder="Example: HF",
                key="add_breed"
            )

        st.write("")

        age = st.number_input(
            "Age (years)",
            min_value=0,
            max_value=30,
            step=1,
            key="add_age"
        )
        if st.button(
            "💾 Save Cow",
            width="stretch",
            key="save_cow"
        ):

            if cow_id.strip() == "" or breed.strip() == "":

                st.warning(
                    "Please enter Cow ID and Breed."
                )

            else:

                conn = get_connection()
                cursor = conn.cursor()

                try:

                    cursor.execute(
                        """
                        INSERT INTO cows
                        (cow_id, breed, age)
                        VALUES (?, ?, ?)
                        """,
                        (
                            cow_id.strip(),
                            breed.strip(),
                            age
                        )
                    )

                    conn.commit()

                    st.success(
                        f"🐄 Cow {cow_id} saved successfully!"
                    )

                except sqlite3.IntegrityError:

                    st.error(
                        "This Cow ID already exists."
                    )

                finally:

                    conn.close()

    # ========================================================
    # UPDATE COW
    # ========================================================

    elif cow_option == "✏️ Update Cow":

        st.markdown(
    """
    <div class="section-title">
        ✏️ Update Cow
    </div>

    <div style="
        color:#6b7280;
        font-size:14px;
        margin-bottom:15px;
    ">
        Update the breed or age of an existing cow.
    </div>
    """,
    unsafe_allow_html=True
    )

        # MOBILE-FRIENDLY UPDATE FORM

        col1, col2 = st.columns(2)

        with col1:
            update_cow_id = st.text_input(
                "Cow ID to update",
                key="update_cow_id"
            )

        with col2:
            new_breed = st.text_input(
                "New Breed",
                key="new_breed"
            )

        st.write("")

        new_age = st.number_input(
            "New Age",
            min_value=0,
            max_value=30,
            step=1,
            key="new_age"
        )
        if st.button(
            "✏️ Update Cow",
            width="stretch",
            key="update_cow_button"
        ):

            if update_cow_id.strip() and new_breed.strip():

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    UPDATE cows
                    SET breed = ?, age = ?
                    WHERE cow_id = ?
                    """,
                    (
                        new_breed.strip(),
                        new_age,
                        update_cow_id.strip()
                    )
                )

                conn.commit()

                if cursor.rowcount > 0:

                    st.success(
                        "🐄 Cow updated successfully!"
                    )

                else:

                    st.error(
                        "Cow ID not found."
                    )

                conn.close()

            else:

                st.warning(
                    "Please enter Cow ID and New Breed."
                )

    # ========================================================
    # DELETE COW
    # ========================================================

    elif cow_option == "🗑️ Delete Cow":

        st.markdown(
            """
            <div class="section-title">
                🗑️ Delete Cow
            </div>

            <div style="
                color:#6b7280;
                font-size:14px;
                margin-bottom:15px;
            ">
                Remove a cow from the farm records.
            </div>
            """,
            unsafe_allow_html=True
        )

        delete_cow_id = st.text_input(
            "Enter Cow ID to delete",
            key="delete_cow_id"
        )

        if st.button(
            "🗑️ Delete Cow",
            use_container_width=True,
            key="delete_cow_button"
        ):

            if delete_cow_id.strip():

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    DELETE FROM cows
                    WHERE cow_id = ?
                    """,
                    (delete_cow_id.strip(),)
                )

                conn.commit()

                if cursor.rowcount > 0:

                    st.success(
                        "🐄 Cow deleted successfully!"
                    )

                else:

                    st.error(
                        "Cow ID not found."
                    )

                conn.close()

            else:

                st.warning(
                    "Please enter a Cow ID."
                )


# ============================================================
# MILK MANAGEMENT
# ============================================================

elif page == "🥛 Milk Management":

    st.markdown(
    """
    <div class="dashboard-title">
        🥛 Milk Management
    </div>

    <div class="dashboard-subtitle">
        Record, monitor and manage daily milk production from your farm.
    </div>
    """,
    unsafe_allow_html=True
)

    milk_option = st.radio(
        "Manage Milk",
        [
            "➕ Add Milk Record",
            "📋 Milk Records",
            "🗑️ Delete Milk Record"
        ],
        horizontal=False,
        key="milk_action"
    )

    # ========================================================
    # ADD MILK RECORD
    # ========================================================

    if milk_option == "➕ Add Milk Record":

        st.markdown(
    """
    <div class="section-title">
        ➕ Add Milk Record
    </div>

    <div style="
        color:#6b7280;
        font-size:14px;
        margin-bottom:15px;
    ">
        Enter the daily morning and evening milk production details.
    </div>
    """,
    unsafe_allow_html=True
    )

        col1, col2 = st.columns(2)

        with col1:
            milk_cow_id = st.text_input(
                "Cow ID",
                key="milk_cow_id"
        )

        with col2:
            milk_date = st.date_input(
                "Date",
                key="milk_date"
            )


        # MOBILE-FRIENDLY MILK QUANTITY

        morning_milk = st.number_input(
            "Morning Milk (L)",
            min_value=0.0,
            step=0.1,
            key="morning_milk"
        )

        st.write("")

        evening_milk = st.number_input(
            "Evening Milk (L)",
            min_value=0.0,
            step=0.1,
            key="evening_milk"
        )

        total_milk = morning_milk + evening_milk

        st.info(
            f"🥛 Total Milk: {total_milk:.1f} Litres"
        )

        if st.button(
            "💾 Save Milk Record",
            use_container_width=True,
            key="save_milk"
        ):

            if milk_cow_id.strip() == "":

                st.warning(
                    "Please enter Cow ID."
                )

            elif total_milk <= 0:

                st.warning(
                    "Please enter milk quantity."
                )

            else:

                conn = get_connection()

                cow_exists = conn.execute(
                    """
                    SELECT COUNT(*)
                    FROM cows
                    WHERE cow_id = ?
                    """,
                    (milk_cow_id.strip(),)
                ).fetchone()[0]

                if cow_exists == 0:

                    st.error(
                        "Cow ID not found. Please add the cow first."
                    )

                else:

                    conn.execute(
                        """
                        INSERT INTO milk_records
                        (
                            cow_id,
                            date,
                            morning_milk,
                            evening_milk,
                            total_milk
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            milk_cow_id.strip(),
                            str(milk_date),
                            morning_milk,
                            evening_milk,
                            total_milk
                        )
                    )

                    conn.commit()

                    st.success(
                        "🥛 Milk record saved successfully!"
                    )

                conn.close()

    # ========================================================
    # VIEW MILK RECORDS
    # ========================================================

    elif milk_option == "📋 Milk Records":

        st.markdown(
    """
    <div class="section-title">
        📋 View Milk Records
    </div>

    <div style="
        color:#6b7280;
        font-size:14px;
        margin-bottom:15px;
    ">
        View and monitor all milk production records from the farm.
    </div>
    """,
    unsafe_allow_html=True
    )

        conn = get_connection()

        milk_records = conn.execute(
            """
            SELECT
                id,
                cow_id,
                date,
                morning_milk,
                evening_milk,
                total_milk
            FROM milk_records
            ORDER BY date DESC, id DESC
            """
        ).fetchall()

        conn.close()

        if milk_records:

            # MOBILE-FRIENDLY MILK TABLE

            milk_display = []

            for record in milk_records:
                milk_display.append(
                    (
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[5]
                    )
                )

            st.dataframe(
                milk_display,
                column_config={
                    1: "Cow ID",
                    2: "Date",
                    3: "Morning (L)",
                    4: "Evening (L)",
                    5: "Total (L)"
                },
                use_container_width=True,
                hide_index=True
            )
            
            total_farm_milk = sum(
                record[5]
                for record in milk_records
            )

            st.metric(
                "🥛 Total Milk",
                f"{total_farm_milk:.1f} L"
            )

        else:

            st.info(
                "No milk records found."
            )

    # ========================================================
    # DELETE MILK RECORD
    # ========================================================

    elif milk_option == "🗑️ Delete Milk Record":

        st.markdown(
    """
    <div class="section-title">
        🗑️ Delete Milk Record
    </div>

    <div style="
        color:#6b7280;
        font-size:14px;
        margin-bottom:15px;
    ">
        Remove an incorrect or unwanted milk record from the farm.
    </div>
    """,
    unsafe_allow_html=True
    )

        conn = get_connection()

        milk_records = conn.execute(
            """
            SELECT
                id,
                cow_id,
                date,
                morning_milk,
                evening_milk,
                total_milk
            FROM milk_records
            ORDER BY date DESC, id DESC
            """
        ).fetchall()

        conn.close()

        if milk_records:

            # MOBILE-FRIENDLY DELETE TABLE

            milk_delete_display = []

            for record in milk_records:
                milk_delete_display.append(
                    (
                        record[0],
                        record[1],
                        record[2],
                        record[5]
                    )
                )

            st.dataframe(
                milk_delete_display,
                column_config={
                    1: "ID",
                    2: "Cow ID",
                    3: "Date",
                    4: "Total (L)"
                },
                use_container_width=True,
                hide_index=True
            )

            delete_milk_id = st.number_input(
                "Milk Record ID to delete",
                min_value=1,
                step=1,
                key="delete_milk_id"
            )

            if st.button(
                "🗑️ Delete Milk Record",
                use_container_width=True,
                key="delete_milk_button"
            ):

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    DELETE FROM milk_records
                    WHERE id = ?
                    """,
                    (delete_milk_id,)
                )

                conn.commit()

                if cursor.rowcount > 0:

                    st.success(
                        "🥛 Milk record deleted successfully!"
                    )

                else:

                    st.error(
                        "Milk Record ID not found."
                    )

                conn.close()

        else:

            st.info(
                "No milk records found."
            )


# ============================================================
# HEALTH & VACCINATION
# ============================================================

elif page == "💉 Health & Vaccination":

    st.title("💉 Health & Vaccination")

    health_option = st.radio(
        "Choose an action",
        [
            "➕ Add Health Record",
            "📋 Health Records",
            "✏️ Update Health Record",
            "🗑️ Delete Health Record"
        ],
        horizontal=False,
        key="health_action"
    )

    health_types = [
        "Vaccination",
        "Health Check",
        "Treatment",
        "Medicine",
        "Other"
    ]

    # ========================================================
    # ADD HEALTH RECORD
    # ========================================================

    if health_option == "➕ Add Health Record":

        st.markdown(
    """
    <div class="section-title">
        ➕ Add Health Record
    </div>

    <div style="
        color:#6b7280;
        font-size:14px;
        margin-bottom:15px;
    ">
        Record treatments, health conditions and vaccination details for your cows.
    </div>
    """,
    unsafe_allow_html=True
    )

        col1, col2 = st.columns(2)

        with col1:
            health_cow_id = st.text_input(
                "Cow ID",
                placeholder="Example: C001",
                key="health_cow_id"
            )

        with col2:
            health_record_type = st.selectbox(
                "Record Type",
                health_types,
                key="health_record_type"
            )


        health_date = st.date_input(
            "Date",
            key="health_date"
        )

        st.write("")

        next_due_date = st.date_input(
            "Next Due Date",
            key="next_due_date"
        )


        health_description = st.text_area(
            "Description",
            placeholder="Example: FMD vaccination given",
            key="health_description"
        )
        if st.button(
            "💾 Save Health Record",
            use_container_width=True,
            key="save_health"
        ):

            if health_cow_id.strip() == "":

                st.warning(
                    "Please enter Cow ID."
                )

            else:

                conn = get_connection()

                cow_exists = conn.execute(
                    """
                    SELECT COUNT(*)
                    FROM cows
                    WHERE cow_id = ?
                    """,
                    (health_cow_id.strip(),)
                ).fetchone()[0]

                if cow_exists == 0:

                    st.error(
                        "Cow ID not found. Please add the cow first."
                    )

                else:

                    conn.execute(
                        """
                        INSERT INTO health_records
                        (
                            cow_id,
                            record_type,
                            description,
                            date,
                            next_due_date
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            health_cow_id.strip(),
                            health_record_type,
                            health_description,
                            str(health_date),
                            str(next_due_date)
                        )
                    )

                    conn.commit()

                    st.success(
                        "💉 Health record saved successfully!"
                    )

                conn.close()

    # ========================================================
    # VIEW HEALTH RECORDS
    # ========================================================

    elif health_option == "📋 Health Records":

        st.markdown(
    """
    <div class="section-title">
        📋 View Health Records
    </div>

    <div style="
        color:#6b7280;
        font-size:14px;
        margin-bottom:15px;
    ">
        View and monitor the health history and vaccination records of your cows.
    </div>
    """,
    unsafe_allow_html=True
    )

        conn = get_connection()

        health_records = conn.execute(
            """
            SELECT
                id,
                cow_id,
                record_type,
                description,
                date,
                next_due_date
            FROM health_records
            ORDER BY date DESC, id DESC
            """
        ).fetchall()

        conn.close()

        if health_records:

            # MOBILE-FRIENDLY HEALTH TABLE

            health_display = []

            for record in health_records:
                health_display.append(
                    (
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[5]
                    )
                )

            st.dataframe(
                health_display,
                column_config={
                    1: "Cow ID",
                    2: "Record Type",
                    3: "Description",
                    4: "Date",
                    5: "Next Due Date"
                },
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No health records found."
            )

    # ========================================================
    # UPDATE HEALTH RECORD
    # ========================================================

    elif health_option == "✏️ Update Health Record":

        st.markdown(
            """
            <div class="section-title">
                ✏️ Update Health Record
            </div>

            <div style="
                color:#6b7280;
                font-size:14px;
                margin-bottom:15px;
            ">
                Update existing health or vaccination information for your cows.
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            update_health_id = st.number_input(
                "Health Record ID",
                min_value=1,
                step=1,
                key="update_health_id"
            )

        with col2:
            new_record_type = st.selectbox(
                "New Record Type",
                health_types,
                key="new_record_type"
            )


        new_description = st.text_area(
            "New Description",
            placeholder="Example: FMD vaccination given",
            key="new_description"
        )
 
        
        new_health_date = st.date_input(
            "New Date",
            key="new_health_date"
        )

        st.write("")
        new_next_due_date = st.date_input(
            "New Next Due Date",
            key="new_next_due_date"
        )

        if st.button(
            "✏️ Update Health Record",
            use_container_width=True,
            key="update_health_button"
        ):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE health_records
                SET record_type = ?,
                    description = ?,
                    date = ?,
                    next_due_date = ?
                WHERE id = ?
                """,
                (
                    new_record_type,
                    new_description,
                    str(new_health_date),
                    str(new_next_due_date),
                    update_health_id
                )
            )

            conn.commit()

            if cursor.rowcount > 0:

                st.success(
                    "💉 Health record updated successfully!"
                )

            else:

                st.error(
                    "Health Record ID not found."
                )

            conn.close()

    # ========================================================
    # DELETE HEALTH RECORD
    # ========================================================

    elif health_option == "🗑️ Delete Health Record":

        st.markdown(
            """
            <div class="section-title">
                🗑️ Delete Health Record
            </div>

            <div style="
                color:#6b7280;
                font-size:14px;
                margin-bottom:15px;
            ">
                Remove an incorrect or unwanted health record from the farm.
            </div>
            """,
            unsafe_allow_html=True
        )

        # MOBILE-FRIENDLY DELETE FORM

        delete_health_id = st.number_input(
            "Health Record ID",
            min_value=1,
            step=1,
            key="delete_health_id"
        )

        st.write("")

        if st.button(
            "🗑️ Delete Health Record",
            use_container_width=True,
            key="delete_health_button"
        ):

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    DELETE FROM health_records
                    WHERE id = ?
                    """,
                    (delete_health_id,)
                )

                conn.commit()

                if cursor.rowcount > 0:
                    st.success(
                        "🩼 Health record deleted successfully!"
                    )
                else:
                    st.error(
                        "Health record ID not found."
                    )

                conn.close()

# ============================================================
# INCOME & EXPENSES
# ============================================================

elif page == "💰 Income & Expenses":

    st.markdown(
        """
        <div class="dashboard-title">
            💰 Income & Expenses
        </div>

        <div class="dashboard-subtitle">
            Track your farm income, expenses and financial balance from one place.
        </div>
        """,
        unsafe_allow_html=True
    )
    # ========================================================
    # FINANCE SUMMARY
    # ========================================================

    conn = get_connection()

    total_income = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM finance_records
        WHERE record_type = 'Income'
        """
    ).fetchone()[0]

    total_expenses = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM finance_records
        WHERE record_type = 'Expense'
        """
    ).fetchone()[0]

    conn.close()

    net_balance = total_income - total_expenses

    # MOBILE-FRIENDLY FINANCE SUMMARY

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">💰</div>
                <div class="metric-label">Total Income</div>
                <div class="metric-value">
                    ₹{total_income:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">💸</div>
                <div class="metric-label">Total Expenses</div>
                <div class="metric-value">
                    ₹{total_expenses:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">💵</div>
            <div class="metric-label">Net Balance</div>
            <div class="metric-value">
                ₹{net_balance:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    # ========================================================
    # INCOME VS EXPENSE CHART
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            📊 Income vs Expenses
        </div>

        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:15px;
        ">
            Compare your farm's total income and expenses.
        </div>
        """,
        unsafe_allow_html=True
    )

    finance_chart_data = pd.DataFrame(
        {
            "Type": [
                "Income",
                "Expenses"
            ],
            "Amount": [
                total_income,
                total_expenses
            ]
        }
    )

    st.bar_chart(
        finance_chart_data,
        x="Type",
        y="Amount",
        height=280,
        use_container_width=True
    )

    st.divider()
    # ========================================================
    # FINANCE ACTION
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            💼 Manage Financial Records
        </div>

        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:15px;
        ">
            Add, view, update or remove your farm's financial records.
        </div>
        """,
        unsafe_allow_html=True
    )

    finance_option = st.radio(
        "Choose an action",
        [
            "➕ Add Record",
            "📋 View Records",
            "✏️ Update Record",
            "🗑️ Delete Record"
        ],
        horizontal=False,
        key="finance_action"
    )
    # ========================================================
    # ADD RECORD
    # ========================================================

    if finance_option == "➕ Add Record":

        st.markdown(
            """
            <div class="section-title">
                ➕ Add Income / Expense
            </div>

            <div style="
                color:#6b7280;
                font-size:14px;
                margin-bottom:20px;
            ">
                Record money received or spent by the farm.
            </div>
            """,
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)

        with col1:
            record_type = st.selectbox(
                "Record Type",
                [
                    "Income",
                    "Expense"
                ],
                key="finance_record_type"
            )

        with col2:
            if record_type == "Income":
                category = st.selectbox(
                    "Category",
                    [
                        "Milk Sales",
                        "Other Income"
                    ],
                    key="income_category"
                )
            else:
                category = st.selectbox(
                    "Category",
                    [
                        "Cattle Feed",
                        "Medicine",
                        "Veterinary",
                        "Electricity",
                        "Labor",
                        "Other Expense"
                    ],
                    key="expense_category"
                )

        # MOBILE-FRIENDLY AMOUNT AND DATE

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=100.0,
            key="finance_amount"
        )

        st.write("")

        finance_date = st.date_input(
            "Date",
            key="finance_add_date"
        )
        description = st.text_area(
            "Description",
            placeholder="Example: Monthly cattle feed purchase",
            key="finance_description"
        )

        if st.button(
            "💾 Save Record",
            use_container_width=True,
            key="save_finance"
        ):

            if amount <= 0:

                st.warning(
                    "Please enter an amount greater than 0."
                )

            else:

                conn = get_connection()

                conn.execute(
                    """
                    INSERT INTO finance_records
                    (
                        record_type,
                        category,
                        amount,
                        date,
                        description
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        record_type,
                        category,
                        amount,
                        str(finance_date),
                        description
                    )
                )

                conn.commit()
                conn.close()

                st.success(
                    f"💰 {record_type} record saved successfully!"
                )

    # ========================================================
    # VIEW RECORDS
    # ========================================================

    elif finance_option == "📋 View Records":

        st.markdown(
            """
            <div class="section-title">
                📋 Income & Expense Records
            </div>

            <div style="
                color:#6b7280;
                font-size:14px;
                margin-bottom:15px;
            ">
                View all income and expense transactions recorded for your farm.
            </div>
            """,
            unsafe_allow_html=True
        )

        conn = get_connection()

        finance_records = conn.execute(
            """
            SELECT
                id,
                record_type,
                category,
                amount,
                date,
                description
            FROM finance_records
            ORDER BY date DESC, id DESC
            """
        ).fetchall()

        conn.close()

        if finance_records:

            # MOBILE-FRIENDLY FINANCE TABLE

            finance_df = pd.DataFrame(
                finance_records,
                columns=[
                    "ID",
                    "Type",
                    "Category",
                    "Amount (₹)",
                    "Date",
                    "Description"
                ]
            )

            # ID is only for internal record management
            finance_df = finance_df.drop(
                columns=["ID"]
            )

            finance_df["Date"] = pd.to_datetime(
                finance_df["Date"]
            ).dt.strftime("%d-%m-%Y")

            finance_df["Amount (₹)"] = finance_df[
                "Amount (₹)"
            ].apply(lambda x: f"₹{x:,.2f}")

            st.dataframe(
                finance_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No income or expense records found."
            )
    # ========================================================
    # UPDATE RECORD
    # ========================================================

    elif finance_option == "✏️ Update Record":

        st.markdown(
            """
            <div class="section-title">
                ✏️ Update Income / Expense Record
            </div>

            <div style="
                color:#6b7280;
                font-size:14px;
                margin-bottom:20px;
            ">
                Modify an existing financial record for your farm.
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            record_id = st.number_input(
                "Record ID to update",
                min_value=1,
                step=1,
                key="update_finance_id"
            )

        with col2:
            new_record_type = st.selectbox(
                "Record Type",
                [
                    "Income",
                    "Expense"
                ],
                key="update_finance_type"
            )

        if new_record_type == "Income":

            new_category = st.selectbox(
                "Category",
                [
                    "Milk Sales",
                    "Other Income"
                ],
                key="update_income_category"
            )

        else:

            new_category = st.selectbox(
                "Category",
                [
                    "Cattle Feed",
                    "Medicine",
                    "Veterinary",
                    "Electricity",
                    "Labor",
                    "Other Expense"
                ],
                key="update_expense_category"
            )

        # MOBILE-FRIENDLY AMOUNT AND DATE

        new_amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=100.0,
            key="update_finance_amount"
        )

        st.write("")

        new_date = st.date_input(
            "Date",
            key="update_finance_date"
        )

        new_description = st.text_area(
            "Description",
            key="update_finance_description"
        )

        if st.button(
            "✏️ Update Record",
            use_container_width=True,
            key="update_finance_button"
        ):

            if new_amount <= 0:

                st.warning(
                    "Please enter an amount greater than 0."
                )

            else:

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    UPDATE finance_records
                    SET record_type = ?,
                        category = ?,
                        amount = ?,
                        date = ?,
                        description = ?
                    WHERE id = ?
                    """,
                    (
                        new_record_type,
                        new_category,
                        new_amount,
                        str(new_date),
                        new_description,
                        record_id
                    )
                )

                conn.commit()

                if cursor.rowcount > 0:

                    st.success(
                        "💰 Record updated successfully!"
                    )

                else:

                    st.error(
                        "Record ID not found."
                    )

                conn.close()

    # ========================================================
    # DELETE RECORD
    # ========================================================

    elif finance_option == "🗑️ Delete Record":

        st.markdown(
            """
            <div class="section-title">
                🗑️ Delete Income / Expense Record
            </div>

            <div style="
                color:#6b7280;
                font-size:14px;
                margin-bottom:20px;
            ">
                Remove an incorrect or unwanted financial record from the farm.
            </div>
            """,
            unsafe_allow_html=True
        )

        conn = get_connection()

        finance_records = conn.execute(
            """
            SELECT
                id,
                record_type,
                category,
                amount,
                date,
                description
            FROM finance_records
            ORDER BY date DESC, id DESC
            """
        ).fetchall()

        conn.close()

        if finance_records:

            # MOBILE-FRIENDLY DELETE TABLE

            finance_delete_display = []

            for record in finance_records:
                finance_delete_display.append(
                    (
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4]
                    )
                )

            st.dataframe(
                finance_delete_display,
                column_config={
                    1: "ID",
                    2: "Type",
                    3: "Category",
                    4: "Amount (₹)",
                    5: "Date"
                },
                use_container_width=True,
                hide_index=True
)

            # MOBILE-FRIENDLY DELETE FORM

            delete_finance_id = st.number_input(
                "Record ID to delete",
                min_value=1,
                step=1,
                key="delete_finance_id"
            )

            st.write("")

            delete_button = st.button(
                "🗑️ Delete Record",
                use_container_width=True,
                key="delete_finance_button"
            )

            if delete_button:

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    DELETE FROM finance_records
                    WHERE id = ?
                    """,
                    (delete_finance_id,)
                )

                conn.commit()

                if cursor.rowcount > 0:

                    st.success(
                        "💰 Record deleted successfully!"
                    )

                else:

                    st.error(
                        "Record ID not found."
                    )

                conn.close()

        else:

            st.info(
                "No income or expense records found."
            )


# ============================================================
# REPORTS
# ============================================================

elif page == "📊 Reports":

    st.title("📊 Farm Reports")

    # ========================================================
    # FARM SUMMARY
    # ========================================================

    conn = get_connection()

    total_cows = conn.execute(
        """
        SELECT COUNT(*)
        FROM cows
        """
    ).fetchone()[0]

    total_milk = conn.execute(
        """
        SELECT COALESCE(SUM(total_milk), 0)
        FROM milk_records
        """
    ).fetchone()[0]

    total_milk_records = conn.execute(
        """
        SELECT COUNT(*)
        FROM milk_records
        """
    ).fetchone()[0]

    total_health_records = conn.execute(
        """
        SELECT COUNT(*)
        FROM health_records
        """
    ).fetchone()[0]

    total_income = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM finance_records
        WHERE record_type = 'Income'
        """
    ).fetchone()[0]

    total_expenses = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM finance_records
        WHERE record_type = 'Expense'
        """
    ).fetchone()[0]

    conn.close()

    net_balance = total_income - total_expenses

    # ========================================================
    # SUMMARY CARDS
    # ========================================================

    st.markdown("""
        <div class="section-title">
            📋 Farm Summary
        </div>
        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:20px;
        ">
            A quick overview of your farm's current records and performance.
        </div>
    """, unsafe_allow_html=True)


    # ROW 1
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🐄</div>
                <div class="metric-label">Total Cows</div>
                <div class="metric-value">{total_cows}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🥛</div>
                <div class="metric-label">Total Milk</div>
                <div class="metric-value">{total_milk:.1f} L</div>
            </div>
        """, unsafe_allow_html=True)


    st.write("")


    # ROW 2
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">💉</div>
                <div class="metric-label">Health Records</div>
                <div class="metric-value">{total_health_records}</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📋</div>
                <div class="metric-label">Milk Records</div>
                <div class="metric-value">{total_milk_records}</div>
            </div>
        """, unsafe_allow_html=True)


    st.write("")


    # ROW 3
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-label">Total Income</div>
            <div class="metric-value">₹{total_income:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)


    st.write("")


    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💸</div>
            <div class="metric-label">Total Expenses</div>
            <div class="metric-value">₹{total_expenses:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)
    # ========================================================
    # FINANCIAL SUMMARY
    # ========================================================

    st.divider()

    st.markdown("""
        <div class="section-title">
            💵 Financial Summary
        </div>
        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:20px;
        ">
            Overview of your farm's current financial position.
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💵</div>
            <div class="metric-label">Net Balance</div>
            <div class="metric-value">₹{net_balance:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    # ========================================================
    # FINANCIAL CHART
    # ========================================================

    st.markdown("""
        <div class="section-title">
            📊 Income vs Expenses
        </div>
        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:20px;
        ">
            Compare your total farm income and expenses at a glance.
        </div>
    """, unsafe_allow_html=True)

    report_finance_data = pd.DataFrame(
        {
            "Type": [
                "Income",
                "Expenses"
            ],
            "Amount": [
                total_income,
                total_expenses
            ]
        }
    )

    st.bar_chart(
        report_finance_data,
        x="Type",
        y="Amount",
        height=280,
        use_container_width=True
    )

    # ========================================================
    # MILK PRODUCTION REPORT
    # ========================================================

    st.divider()

    st.markdown("""
        <div class="section-title">
            🥛 Milk Production Report
        </div>
        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:20px;
        ">
            View daily milk production and track morning, evening and total milk output.
        </div>
    """, unsafe_allow_html=True)

    conn = get_connection()

    daily_milk = conn.execute(
        """
        SELECT
            date,
            SUM(morning_milk) AS morning_milk,
            SUM(evening_milk) AS evening_milk,
            SUM(total_milk) AS total_milk
        FROM milk_records
        GROUP BY date
        ORDER BY date
        """
    ).fetchall()

    conn.close()

    if daily_milk:

        milk_report_df = pd.DataFrame(
            daily_milk,
            columns=[
                "Date",
                "Morning Milk (L)",
                "Evening Milk (L)",
                "Total Milk (L)"
            ]
        )

        milk_report_df["Date"] = pd.to_datetime(
            milk_report_df["Date"]
        ).dt.strftime("%d-%m-%Y")

        st.dataframe(
            milk_report_df,
            use_container_width=True,
            hide_index=True
        )

        # ====================================================
        # DAILY MILK CHART
        # ====================================================

        st.markdown("""
            <div class="section-title">
                📊 Daily Milk Production
            </div>
            <div style="
                color:#6b7280;
                font-size:14px;
                margin-bottom:20px;
            ">
                Track your farm's total milk production day by day.
            </div>
        """, unsafe_allow_html=True)

        chart_data = pd.DataFrame(
            {
                "Date": [
                    record[0]
                    for record in daily_milk
                ],
                "Total Milk (L)": [
                    record[3]
                    for record in daily_milk
                ]
            }
        )

        chart_data["Date"] = pd.to_datetime(
            chart_data["Date"]
        )

        st.bar_chart(
            chart_data,
            x="Date",
            y="Total Milk (L)",
            height=280,
            use_container_width=True
        )

    else:

        st.info(
            "No milk records available for the report."
        )
    # ========================================================
    # FINANCE RECORD REPORT
    # ========================================================

    st.divider()

    st.markdown("""
        <div class="section-title">
            💰 Financial Records
        </div>
        <div style="
            color:#6b7280;
            font-size:14px;
            margin-bottom:20px;
        ">
            View all income and expense transactions recorded for your farm.
        </div>
    """, unsafe_allow_html=True)

    conn = get_connection()

    report_finance_records = conn.execute(
        """
        SELECT
            id,
            record_type,
            category,
            amount,
            date,
            description
        FROM finance_records
        ORDER BY date DESC, id DESC
        """
    ).fetchall()

    conn.close()

    if report_finance_records:

        finance_report_df = pd.DataFrame(
        report_finance_records,
        columns=[
            "ID",
            "Type",
            "Category",
            "Amount (₹)",
            "Date",
            "Description"
        ]
    )

    # ID is only for internal record management
    finance_report_df = finance_report_df.drop(
        columns=["ID"]
    )

    finance_report_df["Date"] = pd.to_datetime(
        finance_report_df["Date"]
    ).dt.strftime("%d-%m-%Y")

    finance_report_df["Amount (₹)"] = finance_report_df[
        "Amount (₹)"
    ].apply(lambda x: f"₹{x:,.2f}")

    st.dataframe(
        finance_report_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No financial records available."
    )