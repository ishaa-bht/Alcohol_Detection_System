import streamlit as st
from PIL import Image
import os
from datetime import datetime

# Set up Streamlit page
st.set_page_config(page_title="DUI Suspect Records Dashboard", layout="wide")
st.markdown(
    """
    <style>
    h1 {
        text-align: center;
        font-size: 2.5rem;
        color: #e74c3c;
    }
    /* Styling for the rectangular box containing title and metrics */
    .metric-container {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
    .metric-box {
        background: linear-gradient(135deg, #3498db, #1f8ff7);
        color: white;
        border-radius: 20px;
        padding: 25px;
        margin: 0 20px;
        width: 250px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
        border: 2px solid transparent;
    }
    .metric-box:hover {
        background: linear-gradient(135deg, #e74c3c, #f44336);
        transform: scale(1.05);
        box-shadow: 0 15px 25px rgba(0, 0, 0, 0.3);
        border-color: #e74c3c;
    }
    .metric-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #f1c40f;  /* Soft yellow for title */
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 10px;
        letter-spacing: 1px;
        color: #ffffff;  /* White color for metrics */
    }
    /* Hover effect on text */
    .metric-box:hover .metric-title {
        color: #fff;
    }
    .metric-box:hover .metric-value {
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered Title
st.title("🚔 DUI Suspect Records Dashboard")

# Custom CSS for aesthetics, top navigation bar, and centering text
st.markdown(
    """
    <style>
    /* General layout styling */
    .css-18e3th9 {
        padding-top: 0 !important;
    }
    /* Header and Navigation */
    header { 
        background-color: #1f2d3d;
        padding: 10px;
        text-align: center;
    }
    .header-content h1 {
        color: #e74c3c;
        font-size: 2rem;
        margin: 0;
        text-align: center;
    }
    .nav-links {
        text-align: center;
        padding: 5px;
    }
    .nav-links a {
        color: #3498db;
        margin: 0 15px;
        font-size: 1.1rem;
        text-decoration: none;
        font-weight: bold;
    }
    .nav-links a:hover {
        color: #e74c3c;
    }
    /* Center content */
    .content {
        text-align: center;
        margin: 20px;
    }
    </style>

    <header>
        <div class="nav-links">
            <a href="#home">🏠 Home</a>
            <a href="#suspect-list">📸 Suspect List</a>
            <a href="#insights">📊 Insights</a>
        </div>
    </header>
    """,
    unsafe_allow_html=True,
)

# Home Section
st.markdown('<a name="home"></a>', unsafe_allow_html=True)
st.markdown('<div class="content">', unsafe_allow_html=True)

# Rectangular box-styled metrics with title and value
st.markdown('<div class="metric-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

col1.markdown(
    """
    <div class="metric-box">
        <div class="metric-title">Total Suspects</div>
        <div class="metric-value">345</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col2.markdown(
    """
    <div class="metric-box">
        <div class="metric-title">Recent (24 hrs)</div>
        <div class="metric-value">5</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col3.markdown(
    """
    <div class="metric-box">
        <div class="metric-title">Avg BAC Level</div>
        <div class="metric-value">0.08</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Suspect List Section
st.markdown('<a name="suspect-list"></a>', unsafe_allow_html=True)
st.markdown('<div class="content">', unsafe_allow_html=True)
st.subheader("📸 Suspected Driver List")

screenshot_dir = "screenshots"  # Folder path for screenshots
if os.path.exists(screenshot_dir):
    screenshots = sorted([f for f in os.listdir(screenshot_dir) if f.endswith(".jpg")], reverse=True)
    filter_date = st.date_input("Filter by date", min_value=datetime(2022, 1, 1).date())
    filtered_screenshots = [f for f in screenshots if filter_date.strftime("%Y%m%d") in f] if filter_date else screenshots

    if filtered_screenshots:
        for screenshot_file in filtered_screenshots:
            image_path = os.path.join(screenshot_dir, screenshot_file)
            image = Image.open(image_path)
            with st.expander(f"Suspect: {screenshot_file.replace('.jpg', '')}") :
                st.image(image, caption=f"Captured on {screenshot_file.replace('suspect_', '').replace('.jpg', '')}", use_column_width=True)
    else:
        st.write("No records found for the selected date.")
else:
    st.write("No screenshots available.")
st.markdown('</div>', unsafe_allow_html=True)

# Insights Section
st.markdown('<a name="insights"></a>', unsafe_allow_html=True)
st.markdown('<div class="content">', unsafe_allow_html=True)
st.subheader("📊 Insights")
st.write("Visualize trends and analyze DUI case data over time.")

# Placeholder example data visualization
st.line_chart([10, 20, 15, 25, 30, 35, 40])
st.markdown('</div>', unsafe_allow_html=True)
