import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import json
import math
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────
# PAGE CONFIG (must be first st. call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="⚡ Streamlit Mega Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://docs.streamlit.io",
        "Report a bug": "https://github.com/streamlit/streamlit/issues",
        "About": "# Streamlit Mega Dashboard\nBuilt for Cloud Applications Lab 🎓",
    },
)

# ─────────────────────────────────────────────
# CUSTOM CSS INJECTION
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    .block-container { padding-top: 1rem; }
    .stMetric { background: linear-gradient(135deg, #1e2130, #2d3250); border-radius: 12px; padding: 10px; }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 8px;
        font-weight: bold; transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: scale(1.05); box-shadow: 0 4px 15px rgba(102,126,234,0.5); }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; }
    .hero-title {
        font-size: 3.5rem; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #667eea, #f093fb, #f5576c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-sub {
        text-align: center; font-size: 1.2rem; color: #a0aec0; margin-top: 0;
    }
    .card {
        background: linear-gradient(135deg, #1a1f35, #2d3250);
        border: 1px solid #3d4270; border-radius: 16px; padding: 20px;
        margin: 10px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .badge {
        display: inline-block; padding: 4px 12px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 20px; color: white; font-size: 0.8rem; font-weight: 600;
    }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "counter" not in st.session_state:
    st.session_state.counter = 0
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hi! I'm your AI assistant. Ask me anything!"}
    ]
if "todo_list" not in st.session_state:
    st.session_state.todo_list = ["Deploy on Community Cloud ✅", "Finish Lab Report 📝"]
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# ─────────────────────────────────────────────
# CACHING DEMO
# ─────────────────────────────────────────────
@st.cache_data
def generate_large_dataset(rows=500):
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=rows, freq="D")
    return pd.DataFrame({
        "Date": dates,
        "Revenue": np.cumsum(np.random.randn(rows) * 100 + 50) + 10000,
        "Users": np.random.randint(100, 1000, rows),
        "Sessions": np.random.randint(200, 2000, rows),
        "Bounce_Rate": np.random.uniform(0.2, 0.8, rows),
        "Conversion": np.random.uniform(0.01, 0.15, rows),
        "Region": np.random.choice(["North", "South", "East", "West"], rows),
        "Platform": np.random.choice(["Mobile", "Desktop", "Tablet"], rows),
        "Satisfaction": np.random.choice([1, 2, 3, 4, 5], rows, p=[0.05, 0.1, 0.2, 0.35, 0.3]),
    })

@st.cache_resource
def load_model_mock():
    time.sleep(0.1)
    return {"name": "MockML v2.0", "accuracy": 0.947, "loaded": True}

df = generate_large_dataset()
model = load_model_mock()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">⚡ MegaDash</div>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub" style="font-size:0.9rem;">Community Cloud Edition</p>', unsafe_allow_html=True)
    st.divider()

    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "Go to",
        ["🏠 Home", "📊 Analytics", "🎛️ Widgets Gallery", "📋 Forms & State",
         "🤖 AI Chat", "📁 File Tools", "🎨 Media & Visuals", "ℹ️ About"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### ⚙️ Settings")
    theme = st.selectbox("Theme", ["Dark", "Light", "Ocean", "Sunset"])
    st.session_state.theme = theme

    font_size = st.slider("Font Scale", 0.8, 1.5, 1.0, 0.1)
    show_debug = st.checkbox("Show Debug Info", value=False)

    st.divider()
    st.markdown("### 📈 Live Stats")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Users", f"{random.randint(1200, 1500):,}", f"+{random.randint(10,50)}")
    with col_s2:
        st.metric("Uptime", "99.9%", "+0.1%")

    st.markdown("### 🕐 Time")
    st.markdown(f"**{datetime.now().strftime('%a, %b %d %Y')}**")
    st.markdown(f"`{datetime.now().strftime('%H:%M:%S')} IST`")

    if show_debug:
        st.divider()
        st.markdown("### 🐛 Debug")
        st.json({"session_keys": list(st.session_state.keys()), "df_shape": list(df.shape)})

# ─────────────────────────────────────────────
# ══════════════ PAGE: HOME ══════════════
# ─────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown('<h1 class="hero-title">⚡ Streamlit Mega Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">The most complete Streamlit showcase — Cloud Applications Lab 🎓</p>', unsafe_allow_html=True)
    st.markdown("")

    # Metrics Row
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("🌍 Total Users", "1,284,302", "+12.4%")
    m2.metric("💰 Revenue", "$94,230", "+8.1%")
    m3.metric("📦 Deployments", "2,047", "+23")
    m4.metric("⚡ Uptime", "99.98%", "+0.02%")
    m5.metric("🤖 AI Queries", "482,910", "+1,200")

    st.divider()

    # Info boxes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### ☁️ Community Cloud\nThis app is deployed on **Streamlit Community Cloud** — a free, shared cloud platform ideal for Python web apps.", icon="☁️")
    with col2:
        st.success("### ✅ All Systems Go\nAll services are **operational**. Database, API, and CDN are running at full capacity.", icon="✅")
    with col3:
        st.warning("### ⚠️ Maintenance\nScheduled maintenance on **Mar 1, 2026 at 2:00 AM IST**. Expected downtime: ~10 min.", icon="⚠️")

    st.divider()

    # Feature Highlights
    st.markdown("## 🚀 Features Showcased")
    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("🎛️", "All Widgets", "Buttons, sliders, inputs, selects, date pickers, and more"),
        ("📊", "Full Charts", "Line, bar, area, scatter, map, Plotly, Altair, and more"),
        ("🤖", "Chat UI", "Full chat interface with session history and AI responses"),
        ("📁", "File Tools", "Upload and process CSV/text files on the fly"),
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        col.markdown(
            f'<div class="card"><h3>{icon} {title}</h3><p style="color:#a0aec0;">{desc}</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    # Progress indicators
    st.markdown("## 📊 Project Progress")
    tasks = {"Frontend UI": 95, "Backend API": 88, "ML Integration": 72, "Cloud Deployment": 100, "Documentation": 60}
    for task, pct in tasks.items():
        col_t, col_p = st.columns([1, 3])
        col_t.markdown(f"**{task}**")
        col_p.progress(pct / 100, text=f"{pct}%")

    st.divider()
    # Expander with text elements
    with st.expander("📖 About This Application — Click to Expand"):
        st.markdown("""
        ## What is This?
        This dashboard is a **complete showcase** of the Streamlit framework, demonstrating every major feature.

        ### Text Elements Used
        - `st.title`, `st.header`, `st.subheader`, `st.markdown`, `st.write`, `st.text`, `st.caption`
        - `st.code`, `st.latex`, `st.divider`

        ### Layout Elements
        - `st.columns`, `st.tabs`, `st.expander`, `st.container`, `st.sidebar`

        ### Input Widgets
        - `st.button`, `st.checkbox`, `st.radio`, `st.selectbox`, `st.multiselect`
        - `st.slider`, `st.text_input`, `st.number_input`, `st.text_area`
        - `st.date_input`, `st.time_input`, `st.color_picker`, `st.file_uploader`

        ### Data & Charts
        - `st.dataframe`, `st.table`, `st.metric`, `st.json`
        - `st.line_chart`, `st.bar_chart`, `st.area_chart`, `st.scatter_chart`, `st.map`

        ### Status & Feedback
        - `st.spinner`, `st.progress`, `st.toast`, `st.balloons`, `st.snow`
        - `st.success`, `st.info`, `st.warning`, `st.error`, `st.exception`

        ### Advanced
        - `st.chat_message`, `st.chat_input`
        - `st.session_state`, `@st.cache_data`, `@st.cache_resource`
        - `st.components.v1.html`, `st.markdown` with raw HTML/CSS
        """)

        st.latex(r"E = mc^2 \quad \Rightarrow \quad \text{Energy} = \text{Mass} \times c^2")
        st.code("""
# This is how caching works in Streamlit
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")
""", language="python")

    # Counter demo
    st.markdown("## 🔢 Interactive Counter")
    cc1, cc2, cc3 = st.columns([1, 2, 1])
    with cc1:
        if st.button("➖ Decrease"):
            st.session_state.counter -= 1
    with cc2:
        st.markdown(
            f'<div style="text-align:center; font-size:3rem; font-weight:900; color:#667eea;">{st.session_state.counter}</div>',
            unsafe_allow_html=True,
        )
    with cc3:
        if st.button("➕ Increase"):
            st.session_state.counter += 1
    if st.button("🔄 Reset Counter"):
        st.session_state.counter = 0
        st.toast("Counter reset!", icon="🔄")

# ─────────────────────────────────────────────
# ══════════════ PAGE: ANALYTICS ══════════════
# ─────────────────────────────────────────────
elif page == "📊 Analytics":
    st.title("📊 Analytics Dashboard")
    st.caption("Real-time data analysis powered by Streamlit + Pandas + NumPy")

    # Filters
    with st.container():
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            region_filter = st.multiselect("🌍 Region", df["Region"].unique().tolist(), default=df["Region"].unique().tolist())
        with f2:
            platform_filter = st.multiselect("📱 Platform", df["Platform"].unique().tolist(), default=df["Platform"].unique().tolist())
        with f3:
            date_range = st.date_input(
                "📅 Date Range",
                value=(date(2023, 1, 1), date(2023, 12, 31)),
            )
        with f4:
            metric_choice = st.selectbox("📈 Primary Metric", ["Revenue", "Users", "Sessions", "Bounce_Rate", "Conversion"])

    filtered_df = df[df["Region"].isin(region_filter) & df["Platform"].isin(platform_filter)]
    if len(date_range) == 2:
        start, end = date_range
        filtered_df = filtered_df[
            (filtered_df["Date"].dt.date >= start) & (filtered_df["Date"].dt.date <= end)
        ]

    st.divider()

    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Avg Revenue/Day", f"${filtered_df['Revenue'].mean():,.0f}", f"{filtered_df['Revenue'].pct_change().mean()*100:.2f}%")
    k2.metric("Total Users", f"{filtered_df['Users'].sum():,}")
    k3.metric("Avg Bounce Rate", f"{filtered_df['Bounce_Rate'].mean()*100:.1f}%")
    k4.metric("Avg Conversion", f"{filtered_df['Conversion'].mean()*100:.2f}%")

    st.divider()

    # Charts Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Line", "📊 Bar", "🏔️ Area", "🔵 Scatter", "🗺️ Map"])

    with tab1:
        st.subheader(f"{metric_choice} Over Time")
        st.line_chart(filtered_df.set_index("Date")[metric_choice], use_container_width=True)

    with tab2:
        st.subheader("Users by Region")
        region_data = filtered_df.groupby("Region")["Users"].sum().reset_index()
        st.bar_chart(region_data.set_index("Region"), use_container_width=True)

    with tab3:
        st.subheader("Revenue & Users — Area Chart")
        area_data = filtered_df.set_index("Date")[["Revenue", "Users"]].head(100)
        st.area_chart(area_data, use_container_width=True)

    with tab4:
        st.subheader("Sessions vs Revenue (Scatter)")
        scatter_data = filtered_df[["Sessions", "Revenue"]].rename(columns={"Sessions": "x", "Revenue": "y"})
        st.scatter_chart(scatter_data, x="x", y="y", use_container_width=True)

    with tab5:
        st.subheader("🗺️ Random Location Map")
        map_df = pd.DataFrame({
            "lat": np.random.uniform(8, 37, 100),
            "lon": np.random.uniform(68, 97, 100),
        })
        st.map(map_df, zoom=3)

    st.divider()

    # Dataframe
    st.markdown("### 📋 Raw Data Explorer")
    rows_to_show = st.slider("Rows to show", 5, 100, 20)
    st.dataframe(
        filtered_df.head(rows_to_show).style.background_gradient(subset=["Revenue"], cmap="Blues"),
        use_container_width=True,
        height=300,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 📌 Static Table (Top 5)")
        st.table(filtered_df[["Date", "Revenue", "Users", "Region"]].head(5))
    with col_b:
        st.markdown("### 📦 JSON Sample")
        st.json(filtered_df.head(3).to_dict(orient="records"))

# ─────────────────────────────────────────────
# ══════════════ PAGE: WIDGETS GALLERY ════════
# ─────────────────────────────────────────────
elif page == "🎛️ Widgets Gallery":
    st.title("🎛️ Complete Widgets Gallery")
    st.caption("Every single Streamlit input widget in one place")

    # Button row
    st.markdown("### 🔘 Buttons")
    b1, b2, b3, b4, b5 = st.columns(5)
    if b1.button("🎉 Balloons!"):
        st.balloons()
    if b2.button("❄️ Snow!"):
        st.snow()
    if b3.button("🍞 Toast"):
        st.toast("This is a toast message! 🍞", icon="🔥")
    if b4.button("⏳ Spinner"):
        with st.spinner("Loading something heavy..."):
            time.sleep(2)
        st.success("Done!")
    if b5.button("💥 Error"):
        st.error("This is what an error looks like!", icon="🚨")

    st.divider()
    st.markdown("### ☑️ Checkboxes & Toggles")
    ch1, ch2, ch3 = st.columns(3)
    with ch1:
        cb1 = st.checkbox("Enable Feature A")
        cb2 = st.checkbox("Enable Feature B", value=True)
        if cb1: st.success("Feature A is ON")
        if cb2: st.info("Feature B is ON")
    with ch2:
        toggle = st.toggle("🌙 Dark Mode")
        if toggle:
            st.caption("Dark mode enabled!")
        else:
            st.caption("Light mode enabled!")
    with ch3:
        radio_val = st.radio("Choose Option", ["Option A", "Option B", "Option C"], horizontal=True)
        st.caption(f"Selected: **{radio_val}**")

    st.divider()
    st.markdown("### 📝 Text Inputs")
    ti1, ti2 = st.columns(2)
    with ti1:
        name_in = st.text_input("👤 Your Name", placeholder="Praharsh Andole")
        email_in = st.text_input("📧 Email", placeholder="praharsh@example.com", type="default")
        pwd = st.text_input("🔑 Password", type="password")
        if name_in:
            st.success(f"Hello, **{name_in}**! 👋")
    with ti2:
        bio = st.text_area("📄 Bio", height=120, placeholder="Tell us about yourself...")
        search = st.text_input("🔍 Search", placeholder="Type to search...")
        if search:
            results = df[df["Region"].str.contains(search, case=False)].head(3)
            if not results.empty:
                st.dataframe(results[["Date", "Region", "Revenue"]], use_container_width=True)
            else:
                st.caption("No results found.")

    st.divider()
    st.markdown("### 🎚️ Sliders & Numbers")
    sl1, sl2 = st.columns(2)
    with sl1:
        age = st.slider("🎂 Age", 1, 100, 22)
        temp = st.slider("🌡️ Temperature (°C)", -20.0, 50.0, 25.0, 0.5)
        range_val = st.slider("📏 Range Selector", 0, 1000, (200, 800))
        st.caption(f"Age: {age} | Temp: {temp}°C | Range: {range_val}")
    with sl2:
        num = st.number_input("🔢 Number Input", min_value=0, max_value=1000, value=42, step=1)
        float_num = st.number_input("💫 Float Input", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        st.caption(f"Integer: {num} | Float: {float_num:.2f}")

    st.divider()
    st.markdown("### 📋 Selectors")
    sel1, sel2 = st.columns(2)
    with sel1:
        country = st.selectbox("🌍 Country", ["India", "USA", "UK", "Germany", "Japan", "Australia"])
        lang = st.multiselect("💻 Languages", ["Python", "JavaScript", "Rust", "Go", "Java", "C++"], default=["Python", "Rust"])
        st.caption(f"Country: {country} | Languages: {', '.join(lang)}")
    with sel2:
        priority = st.select_slider("⚡ Priority", options=["Low", "Medium", "High", "Critical"], value="Medium")
        rating = st.select_slider("⭐ Rating", options=[1, 2, 3, 4, 5], value=4)
        st.caption(f"Priority: {priority} | Rating: {'⭐' * rating}")

    st.divider()
    st.markdown("### 📅 Date & Time")
    dt1, dt2, dt3 = st.columns(3)
    with dt1:
        dob = st.date_input("🎂 Date of Birth", value=date(2003, 1, 1))
        today = date.today()
        age_calc = (today - dob).days // 365
        st.caption(f"Age: **{age_calc} years old**")
    with dt2:
        event_time = st.time_input("⏰ Event Time", value=datetime.now().time())
        st.caption(f"Set time: **{event_time}**")
    with dt3:
        color = st.color_picker("🎨 Favorite Color", "#667eea")
        st.markdown(
            f'<div style="width:100%;height:60px;background:{color};border-radius:10px;"></div>',
            unsafe_allow_html=True,
        )
        st.caption(f"HEX: {color}")

# ─────────────────────────────────────────────
# ══════════════ PAGE: FORMS & STATE ══════════
# ─────────────────────────────────────────────
elif page == "📋 Forms & State":
    st.title("📋 Forms, State & Interactivity")

    # Registration Form
    st.markdown("## 📝 Registration Form")
    with st.form("registration_form", clear_on_submit=False):
        st.markdown("#### Fill in your details")
        fc1, fc2 = st.columns(2)
        with fc1:
            f_name = st.text_input("First Name*", placeholder="Praharsh")
            f_email = st.text_input("Email*", placeholder="praharsh@example.com")
            f_age = st.number_input("Age*", min_value=1, max_value=120, value=22)
            f_gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
        with fc2:
            f_lname = st.text_input("Last Name*", placeholder="Andole")
            f_phone = st.text_input("Phone", placeholder="+91 XXXXX XXXXX")
            f_dob = st.date_input("Date of Birth", value=date(2003, 1, 1))
            f_country = st.selectbox("Country", ["India", "USA", "UK", "Germany", "Japan"])
        f_bio = st.text_area("About Yourself", placeholder="Brief bio...", height=80)
        f_lang = st.multiselect("Programming Languages", ["Python", "JavaScript", "Rust", "Java", "Go", "C++"])
        f_newsletter = st.checkbox("Subscribe to Newsletter")
        f_terms = st.checkbox("I agree to Terms & Conditions *")
        submitted = st.form_submit_button("🚀 Submit Registration", use_container_width=True)

        if submitted:
            if not f_name or not f_email or not f_terms:
                st.error("Please fill all required fields and accept terms!", icon="🚨")
            else:
                st.session_state.form_submitted = True
                st.balloons()

    if st.session_state.form_submitted:
        st.success(f"✅ Registration Successful! Welcome, **{f_name} {f_lname}**!", icon="🎉")
        c1, c2, c3 = st.columns(3)
        c1.metric("Name", f"{f_name} {f_lname}")
        c2.metric("Country", f_country)
        c3.metric("Languages", str(len(f_lang)))

    st.divider()

    # TODO List with session state
    st.markdown("## ✅ Todo List (Session State Demo)")
    todo_col1, todo_col2 = st.columns([3, 1])
    with todo_col1:
        new_todo = st.text_input("Add new task", placeholder="Type a task and press Add")
    with todo_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Task"):
            if new_todo and new_todo not in st.session_state.todo_list:
                st.session_state.todo_list.append(new_todo)
                st.toast(f"Added: {new_todo}", icon="✅")

    for i, task in enumerate(st.session_state.todo_list):
        tc1, tc2 = st.columns([5, 1])
        tc1.markdown(f"{'✅' if i == 0 else '⏳'} {task}")
        if tc2.button("🗑️", key=f"del_{i}"):
            st.session_state.todo_list.pop(i)
            st.rerun()

    st.divider()

    # Progress simulation
    st.markdown("## ⏳ Progress Simulation")
    if st.button("▶️ Run Progress Bar Demo"):
        prog_bar = st.progress(0, text="Starting...")
        status_text = st.empty()
        for i in range(101):
            time.sleep(0.02)
            prog_bar.progress(i / 100, text=f"Processing... {i}%")
            if i < 30: status_text.info(f"📦 Loading data... {i}%")
            elif i < 60: status_text.warning(f"⚙️ Processing... {i}%")
            elif i < 90: status_text.info(f"🧮 Analyzing... {i}%")
            else: status_text.success(f"✅ Almost done! {i}%")
        status_text.success("🎉 Task completed successfully!")
        st.balloons()

    st.divider()

    # Columns & containers
    st.markdown("## 🏗️ Layout Containers Demo")
    with st.container(border=True):
        st.markdown("**This is inside `st.container(border=True)`**")
        inner1, inner2 = st.columns(2)
        inner1.success("Left Column ✅")
        inner2.info("Right Column ℹ️")

    with st.expander("🔍 Click to see Session State"):
        st.json(dict(st.session_state))

    st.markdown("### 🧮 Live Calculator")
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    with calc_col1:
        num1 = st.number_input("First Number", value=10.0)
    with calc_col2:
        operator = st.selectbox("Operator", ["+", "−", "×", "÷", "^ (power)", "% (mod)"])
    with calc_col3:
        num2 = st.number_input("Second Number", value=5.0)

    result_map = {
        "+": num1 + num2,
        "−": num1 - num2,
        "×": num1 * num2,
        "÷": num1 / num2 if num2 != 0 else "∞ (div by zero)",
        "^ (power)": num1 ** num2,
        "% (mod)": num1 % num2 if num2 != 0 else "∞",
    }
    result = result_map[operator]
    st.markdown(
        f'<div class="card" style="text-align:center;"><h2>{num1} {operator} {num2} = <span style="color:#667eea;">{result}</span></h2></div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# ══════════════ PAGE: AI CHAT ════════════════
# ─────────────────────────────────────────────
elif page == "🤖 AI Chat":
    st.title("🤖 AI Assistant Chat")
    st.caption("Powered by Streamlit Chat Elements + Session State")

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about data, code, or the cloud..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Simulated AI response
        responses = {
            "hello": "👋 Hello! I'm your Streamlit AI demo. I can answer questions about this dashboard!",
            "streamlit": "⚡ Streamlit is an open-source Python framework to build web apps in minutes. This entire dashboard was built with it!",
            "cloud": "☁️ This app is deployed on **Streamlit Community Cloud** — a free shared cloud platform. It auto-deploys from GitHub!",
            "python": "🐍 Python powers this entire app! Streamlit, Pandas, NumPy, and Plotly are all Python libraries.",
            "help": "I can help with: streamlit, cloud, python, data, charts, session_state, caching. Try asking about any of these!",
            "data": "📊 This app uses a **500-row synthetic dataset** with Revenue, Users, Sessions, Bounce Rate, and more. Check the Analytics tab!",
            "session_state": "🧠 `st.session_state` is how Streamlit persists variables across reruns. It's like a dictionary that survives page refresh!",
            "caching": "⚡ `@st.cache_data` caches function output so Streamlit doesn't recompute it on every rerun. Super useful for data loading!",
        }
        key_found = None
        for key in responses:
            if key in prompt.lower():
                key_found = key
                break
        ai_reply = responses.get(key_found, f"🤖 Interesting question! You asked: *\"{prompt}\"*\n\nI'm a demo bot, but in a real app you'd connect me to GPT-4 or Gemini via API! Try asking about: **streamlit, cloud, python, data, caching, session_state**.")

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(0.5)
            st.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "Chat cleared! How can I help you? 👋"}]
        st.rerun()

# ─────────────────────────────────────────────
# ══════════════ PAGE: FILE TOOLS ═════════════
# ─────────────────────────────────────────────
elif page == "📁 File Tools":
    st.title("📁 File Upload & Processing")

    ft1, ft2 = st.columns(2)

    with ft1:
        st.markdown("### 📂 Upload CSV File")
        uploaded_csv = st.file_uploader("Choose a CSV file", type=["csv"])
        if uploaded_csv:
            user_df = pd.read_csv(uploaded_csv)
            st.success(f"✅ Loaded {len(user_df)} rows × {len(user_df.columns)} columns")
            st.dataframe(user_df.head(10), use_container_width=True)
            st.markdown("#### Quick Stats")
            st.write(user_df.describe())
            if st.button("📊 Chart First Column"):
                col_name = user_df.select_dtypes(include=np.number).columns[0]
                st.line_chart(user_df[col_name].head(50))
        else:
            st.info("Upload any CSV file to explore it here!", icon="📂")

    with ft2:
        st.markdown("### 📄 Upload Text/Code File")
        uploaded_txt = st.file_uploader("Choose a .txt or .py file", type=["txt", "py", "md", "json"])
        if uploaded_txt:
            content = uploaded_txt.read().decode("utf-8")
            st.success(f"✅ Read {len(content)} characters, {len(content.splitlines())} lines")
            ext = uploaded_txt.name.split(".")[-1]
            if ext == "json":
                try:
                    st.json(json.loads(content))
                except Exception:
                    st.code(content, language="json")
            elif ext == "py":
                st.code(content, language="python")
            else:
                st.text_area("File Content", content, height=300)
        else:
            st.info("Upload a text or Python file to view it here!", icon="📄")

    st.divider()

    st.markdown("### 🖼️ Upload Image")
    uploaded_img = st.file_uploader("Upload any image", type=["png", "jpg", "jpeg", "gif", "svg"])
    if uploaded_img:
        img_col1, img_col2 = st.columns(2)
        with img_col1:
            st.image(uploaded_img, caption=f"Uploaded: {uploaded_img.name}", use_container_width=True)
        with img_col2:
            st.markdown("#### Image Details")
            st.metric("Filename", uploaded_img.name)
            st.metric("File Type", uploaded_img.type)
            st.metric("File Size", f"{uploaded_img.size / 1024:.1f} KB")
    else:
        st.info("Upload any image file to preview and inspect it!", icon="🖼️")

    st.divider()

    st.markdown("### 🎵 Upload Audio")
    uploaded_audio = st.file_uploader("Upload audio file", type=["mp3", "wav", "ogg"])
    if uploaded_audio:
        st.audio(uploaded_audio, format=uploaded_audio.type)
        st.success(f"Playing: {uploaded_audio.name}")
    else:
        st.info("Upload an audio file to play it in-browser!", icon="🎵")

# ─────────────────────────────────────────────
# ══════════════ PAGE: MEDIA & VISUALS ════════
# ─────────────────────────────────────────────
elif page == "🎨 Media & Visuals":
    st.title("🎨 Media, Text & Visual Elements")

    # Text types
    st.markdown("## ✍️ All Text Elements")
    st.title("st.title — Large Title")
    st.header("st.header — Section Header")
    st.subheader("st.subheader — Subsection")
    st.markdown("**st.markdown** — supports `code`, **bold**, *italic*, > blockquotes, lists, tables")
    st.write("**st.write** — magic function, handles anything: strings, dicts, DataFrames, charts")
    st.text("st.text — monospace plain text, great for logs")
    st.caption("st.caption — small caption text, used for metadata")

    st.divider()

    st.markdown("### 🧮 LaTeX Math")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.latex(r"\hat{y} = \sigma(W \cdot x + b)")
        st.latex(r"\nabla_\theta J(\theta) = \frac{1}{m}\sum_{i=1}^{m}(h_\theta(x^{(i)}) - y^{(i)})x^{(i)}")
    with col_l2:
        st.latex(r"F(x) = \int_{-\infty}^{x} f(t)\, dt")
        st.latex(r"\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V")

    st.divider()

    st.markdown("### 💻 Code Blocks")
    code_tabs = st.tabs(["Python", "JavaScript", "Rust", "SQL"])
    with code_tabs[0]:
        st.code("""
@st.cache_data
def fetch_data(url: str) -> pd.DataFrame:
    response = requests.get(url)
    return pd.DataFrame(response.json())

df = fetch_data("https://api.example.com/data")
st.dataframe(df)
""", language="python")

    with code_tabs[1]:
        st.code("""
const fetchData = async (url) => {
  const response = await fetch(url);
  const data = await response.json();
  return data;
};

fetchData("https://api.example.com/users")
  .then(data => console.log(data));
""", language="javascript")

    with code_tabs[2]:
        st.code("""
use std::collections::HashMap;

fn word_count(text: &str) -> HashMap<&str, usize> {
    let mut map = HashMap::new();
    for word in text.split_whitespace() {
        *map.entry(word).or_insert(0) += 1;
    }
    map
}
""", language="rust")

    with code_tabs[3]:
        st.code("""
SELECT
    region,
    COUNT(*) AS total_users,
    AVG(revenue) AS avg_revenue,
    MAX(sessions) AS peak_sessions
FROM analytics
WHERE date >= '2023-01-01'
GROUP BY region
ORDER BY avg_revenue DESC;
""", language="sql")

    st.divider()

    # Status elements
    st.markdown("## 🚦 Status & Feedback Elements")
    st1, st2, st3, st4 = st.columns(4)
    st1.success("✅ Success!")
    st2.info("ℹ️ Info message")
    st3.warning("⚠️ Warning!")
    st4.error("❌ Error occurred!")

    st.exception(ValueError("This is how st.exception() looks — shows full traceback style"))

    st.divider()

    # HTML component
    st.markdown("## 🌐 Custom HTML Component")
    import streamlit.components.v1 as components
    components.html(
        """
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                    border-radius:16px;padding:30px;text-align:center;font-family:sans-serif;">
          <h2 style="color:white;margin:0 0 10px;">🌐 Custom HTML via st.components.v1.html</h2>
          <p style="color:rgba(255,255,255,0.8);">You can embed <strong>any HTML, CSS, and JavaScript</strong> directly into Streamlit!</p>
          <div style="display:flex;justify-content:center;gap:15px;margin-top:20px;">
            <div style="background:rgba(255,255,255,0.2);border-radius:10px;padding:15px 25px;color:white;">
              <div style="font-size:2rem;">⚡</div><div>Fast</div>
            </div>
            <div style="background:rgba(255,255,255,0.2);border-radius:10px;padding:15px 25px;color:white;">
              <div style="font-size:2rem;">☁️</div><div>Cloud</div>
            </div>
            <div style="background:rgba(255,255,255,0.2);border-radius:10px;padding:15px 25px;color:white;">
              <div style="font-size:2rem;">🐍</div><div>Python</div>
            </div>
          </div>
        </div>
        """,
        height=220,
    )

    st.divider()

    # Animated number counter in HTML
    st.markdown("## 🔢 Animated Counter (JS in HTML)")
    components.html("""
    <style>
      .counter-box { display: flex; justify-content: space-around; }
      .counter { text-align:center; font-family: monospace; }
      .num { font-size: 3rem; font-weight:900; color:#667eea; }
      .label { color: #a0aec0; font-size: 0.9rem; }
    </style>
    <div class="counter-box">
      <div class="counter"><div class="num" id="c1">0</div><div class="label">Users</div></div>
      <div class="counter"><div class="num" id="c2">0</div><div class="label">Deployments</div></div>
      <div class="counter"><div class="num" id="c3">0</div><div class="label">Stars</div></div>
    </div>
    <script>
    function animateCounter(id, target, duration) {
      let start = 0;
      const step = target / (duration / 16);
      const el = document.getElementById(id);
      const timer = setInterval(() => {
        start = Math.min(start + step, target);
        el.textContent = Math.floor(start).toLocaleString();
        if (start >= target) clearInterval(timer);
      }, 16);
    }
    animateCounter('c1', 128430, 2000);
    animateCounter('c2', 20470, 2000);
    animateCounter('c3', 31450, 2000);
    </script>
    """, height=130)

# ─────────────────────────────────────────────
# ══════════════ PAGE: ABOUT ══════════════════
# ─────────────────────────────────────────────
elif page == "ℹ️ About":
    st.title("ℹ️ About This App")
    st.markdown(
        '<span class="badge">Cloud Applications Lab</span> &nbsp; <span class="badge">Streamlit Community Cloud</span> &nbsp; <span class="badge">Python</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    a1, a2 = st.columns([2, 1])
    with a1:
        st.markdown("""
        ## 🚀 Streamlit Mega Dashboard

        This application demonstrates the **full power of Streamlit** as a web application framework,
        deployed on **Streamlit Community Cloud** — a free, shared cloud platform.

        ### 📦 Tech Stack
        - **Framework:** Streamlit
        - **Language:** Python 3.11+
        - **Libraries:** Pandas, NumPy
        - **Deployment:** Streamlit Community Cloud
        - **Repository:** GitHub

        ### 🎓 Lab Objectives
        1. Understand the concept of **Community Cloud** computing
        2. Develop a full-featured **Python web application**
        3. Deploy the application on a **public cloud** platform
        4. Demonstrate all major **Streamlit UI components**

        ### 📚 Key Concepts
        - **Community Cloud:** A shared cloud model where infrastructure is provided to a community with shared interests
        - **PaaS:** Platform-as-a-Service — no server management, just push code and deploy
        - **Continuous Deployment:** App auto-updates when you push to GitHub
        """)

    with a2:
        st.markdown("### 📊 App Stats")
        st.metric("Lines of Code", "1,100+")
        st.metric("Streamlit Functions Used", "50+")
        st.metric("Pages", "8")
        st.metric("Widgets Demonstrated", "30+")
        st.metric("Chart Types", "6+")

        st.divider()
        st.markdown("### 🔗 Links")
        st.markdown("- 📖 [Streamlit Docs](https://docs.streamlit.io)")
        st.markdown("- ☁️ [Community Cloud](https://share.streamlit.io)")
        st.markdown("- 🐍 [Python.org](https://python.org)")
        st.markdown("- 📦 [Pandas Docs](https://pandas.pydata.org)")

    st.divider()

    # System info
    st.markdown("### 🖥️ Runtime Info")
    ri1, ri2, ri3, ri4 = st.columns(4)
    ri1.metric("Python", "3.11+")
    ri2.metric("Streamlit", "Latest")
    ri3.metric("Platform", "Community Cloud")
    ri4.metric("Timestamp", datetime.now().strftime("%H:%M:%S"))

    with st.expander("📋 Complete Feature Checklist"):
        features_list = {
            "Text": ["st.title", "st.header", "st.subheader", "st.markdown", "st.write", "st.text", "st.caption", "st.code", "st.latex", "st.divider"],
            "Input Widgets": ["st.button", "st.checkbox", "st.toggle", "st.radio", "st.selectbox", "st.multiselect", "st.slider", "st.select_slider", "st.text_input", "st.number_input", "st.text_area", "st.date_input", "st.time_input", "st.color_picker", "st.file_uploader"],
            "Data Display": ["st.dataframe", "st.table", "st.metric", "st.json"],
            "Charts": ["st.line_chart", "st.bar_chart", "st.area_chart", "st.scatter_chart", "st.map"],
            "Layout": ["st.sidebar", "st.columns", "st.tabs", "st.expander", "st.container"],
            "Media": ["st.image", "st.audio", "st.video"],
            "Status": ["st.success", "st.info", "st.warning", "st.error", "st.exception", "st.spinner", "st.progress", "st.toast", "st.balloons", "st.snow"],
            "Chat": ["st.chat_message", "st.chat_input"],
            "State & Config": ["st.session_state", "st.cache_data", "st.cache_resource", "st.set_page_config", "st.rerun"],
            "Advanced": ["st.components.v1.html", "Custom CSS via st.markdown"],
        }
        for category, items in features_list.items():
            st.markdown(f"**{category}:** " + " · ".join([f"`{i}`" for i in items]))

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#555;font-size:0.85rem;">⚡ Streamlit Mega Dashboard &nbsp;|&nbsp; Cloud Applications Lab &nbsp;|&nbsp; Deployed on <strong>Streamlit Community Cloud</strong> &nbsp;|&nbsp; Built with 🐍 Python</p>',
    unsafe_allow_html=True,
)
