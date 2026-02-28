import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Bridora Admin Panel",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Bridal/Jewelry Theme
st.markdown("""
<style>
    /* Main Theme Colors - Rose Gold & Elegant */
    :root {
        --primary-color: #B76E79;
        --secondary-color: #F4E7E7;
        --accent-color: #D4AF37;
        --text-color: #4A4A4A;
        --bg-color: #FDF8F8;
    }
    
    .stApp {
        background: linear-gradient(135deg, #FDF8F8 0%, #F4E7E7 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2C3E50 0%, #1A252F 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Cards */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(183, 110, 121, 0.15);
        border-left: 5px solid #B76E79;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(183, 110, 121, 0.25);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #B76E79 0%, #D4AF37 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(183, 110, 121, 0.4);
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2C3E50;
        font-family: 'Georgia', serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #B76E79 0%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Status Badges */
    .status-approved {
        background: #28a745;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    
    .status-pending {
        background: #ffc107;
        color: #000;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    
    .status-rejected {
        background: #dc3545;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    
    /* Login Form */
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(183, 110, 121, 0.2);
        border: 2px solid #F4E7E7;
    }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'shops' not in st.session_state:
    # Generate sample shop data
    st.session_state.shops = pd.DataFrame({
        'Shop ID': [f'SHOP{str(i).zfill(4)}' for i in range(1, 11)],
        'Shop Name': [
            'Royal Jewellers', 'Golden Palace', 'Diamond Dreams', 'Pearl Paradise',
            'Gemstone Gallery', 'Bridal Bliss', 'Eternal Elegance', 'Luxury Links',
            'Crystal Crown', 'Jewel Junction'
        ],
        'Owner': [
            'Kumar Sangakkara', 'Mahela Jayawardene', 'Lasith Malinga', 'Angelo Mathews',
            'Dinesh Chandimal', 'Dimuth Karunaratne', 'Kusal Perera', 'Danushka Gunathilaka',
            'Pathum Nissanka', 'Charith Asalanka'
        ],
        'Email': [
            'royal@jewellers.lk', 'golden@palace.lk', 'diamond@dreams.lk', 'pearl@paradise.lk',
            'gem@gallery.lk', 'bridal@bliss.lk', 'eternal@elegance.lk', 'luxury@links.lk',
            'crystal@crown.lk', 'jewel@junction.lk'
        ],
        'Location': [
            'Colombo 07', 'Kandy', 'Galle', 'Negombo', 'Jaffna',
            'Colombo 03', 'Matara', 'Kurunegala', 'Ratnapura', 'Anuradhapura'
        ],
        'Status': ['Approved', 'Approved', 'Approved', 'Pending', 'Approved', 
                   'Pending', 'Approved', 'Rejected', 'Approved', 'Pending'],
        'Registration Date': [
            datetime.now() - timedelta(days=x) for x in [45, 40, 35, 2, 30, 1, 25, 5, 20, 3]
        ],
        'Jewelry Count': [45, 32, 28, 0, 15, 0, 22, 0, 18, 0]
    })

if 'jewelry' not in st.session_state:
    # Generate sample jewelry data
    jewelry_types = ['Necklace', 'Earrings', 'Bracelet', 'Ring', 'Tiara', 'Anklet', 'Bangle']
    materials = ['Gold', 'Diamond', 'Pearl', 'Silver', 'Platinum', 'Gemstone']
    statuses = ['Available', 'Rented', 'Reserved', 'Maintenance']
    
    st.session_state.jewelry = pd.DataFrame({
        'Item ID': [f'JWL{str(i).zfill(5)}' for i in range(1, 51)],
        'Item Name': [f'{random.choice(["Royal", "Elegant", "Classic", "Modern", "Vintage"])} {random.choice(jewelry_types)}' for _ in range(50)],
        'Shop': [random.choice(st.session_state.shops['Shop Name'].tolist()) for _ in range(50)],
        'Type': [random.choice(jewelry_types) for _ in range(50)],
        'Material': [random.choice(materials) for _ in range(50)],
        'Price (LKR)': [random.randint(15000, 500000) for _ in range(50)],
        'Rental Price/Day (LKR)': [random.randint(2000, 25000) for _ in range(50)],
        'Status': [random.choice(statuses) for _ in range(50)],
        'Date Added': [datetime.now() - timedelta(days=random.randint(1, 60)) for _ in range(50)]
    })

if 'bookings' not in st.session_state:
    # Generate sample booking data
    st.session_state.bookings = pd.DataFrame({
        'Booking ID': [f'BKG{str(i).zfill(5)}' for i in range(1, 26)],
        'Customer': [f'Bride {i}' for i in range(1, 26)],
        'Jewelry Item': [st.session_state.jewelry.iloc[i]['Item Name'] for i in range(25)],
        'Shop': [st.session_state.jewelry.iloc[i]['Shop'] for i in range(25)],
        'Booking Date': [datetime.now() - timedelta(days=random.randint(1, 30)) for _ in range(25)],
        'Wedding Date': [datetime.now() + timedelta(days=random.randint(7, 180)) for _ in range(25)],
        'Type': [random.choice(['Rental', 'Purchase']) for _ in range(25)],
        'Amount (LKR)': [random.randint(25000, 450000) for _ in range(25)],
        'Status': [random.choice(['Confirmed', 'Pending', 'Completed', 'Cancelled']) for _ in range(25)]
    })

# Authentication Function
def login():
    st.markdown('<div class="main-header">💎 Bridora Admin Panel</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("### 🔐 Secure Admin Login")
        st.markdown("---")
        
        username = st.text_input("Username", placeholder="Enter admin username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "bridora2024":
                st.session_state.authenticated = True
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>Default: admin / bridora2024</p>", unsafe_allow_html=True)

# Dashboard Page
def show_dashboard():
    st.markdown('<h1 style="text-align: center; color: #B76E79;">📊 System Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_shops = len(st.session_state.shops)
        active_shops = len(st.session_state.shops[st.session_state.shops['Status'] == 'Approved'])
        st.markdown(f'''
        <div class="metric-card">
            <h3 style="color: #B76E79; margin: 0;">🏪 Total Shops</h3>
            <h1 style="font-size: 2.5em; margin: 10px 0; color: #2C3E50;">{total_shops}</h1>
            <p style="color: #28a745; margin: 0;">✓ {active_shops} Active</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        total_jewelry = len(st.session_state.jewelry)
        available_jewelry = len(st.session_state.jewelry[st.session_state.jewelry['Status'] == 'Available'])
        st.markdown(f'''
        <div class="metric-card">
            <h3 style="color: #B76E79; margin: 0;">💍 Total Jewelry</h3>
            <h1 style="font-size: 2.5em; margin: 10px 0; color: #2C3E50;">{total_jewelry}</h1>
            <p style="color: #17a2b8; margin: 0;">✓ {available_jewelry} Available</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        total_bookings = len(st.session_state.bookings)
        confirmed_bookings = len(st.session_state.bookings[st.session_state.bookings['Status'] == 'Confirmed'])
        st.markdown(f'''
        <div class="metric-card">
            <h3 style="color: #B76E79; margin: 0;">📅 Total Bookings</h3>
            <h1 style="font-size: 2.5em; margin: 10px 0; color: #2C3E50;">{total_bookings}</h1>
            <p style="color: #ffc107; margin: 0;">⏳ {confirmed_bookings} Confirmed</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        total_revenue = st.session_state.bookings['Amount (LKR)'].sum()
        st.markdown(f'''
        <div class="metric-card">
            <h3 style="color: #B76E79; margin: 0;">💰 Total Revenue</h3>
            <h1 style="font-size: 2em; margin: 10px 0; color: #2C3E50;">LKR {total_revenue:,.0f}</h1>
            <p style="color: #6c757d; margin: 0;">Across all bookings</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Shop Registration Trends")
        
        # Prepare data for chart
        shop_dates = st.session_state.shops.copy()
        shop_dates['Month'] = shop_dates['Registration Date'].dt.strftime('%B')
        monthly_counts = shop_dates.groupby('Month').size().reset_index(name='Count')
        
        fig = px.line(monthly_counts, x='Month', y='Count', 
                     markers=True, line_shape="spline",
                     color_discrete_sequence=['#B76E79'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🥧 Jewelry Distribution by Type")
        
        type_counts = st.session_state.jewelry['Type'].value_counts()
        fig = px.pie(values=type_counts.values, names=type_counts.index, 
                     hole=0.4, color_discrete_sequence=px.colors.sequential.Rose)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔔 Recent Activity")
    
    tab1, tab2, tab3 = st.tabs(["🆕 New Shops", "📦 Recent Listings", "📅 Recent Bookings"])
    
    with tab1:
        recent_shops = st.session_state.shops.nlargest(5, 'Registration Date')
        st.dataframe(recent_shops[['Shop Name', 'Owner', 'Location', 'Status', 'Registration Date']], 
                    use_container_width=True, hide_index=True)
    
    with tab2:
        recent_jewelry = st.session_state.jewelry.nlargest(5, 'Date Added')
        st.dataframe(recent_jewelry[['Item Name', 'Shop', 'Type', 'Price (LKR)', 'Status']], 
                    use_container_width=True, hide_index=True)
    
    with tab3:
        recent_bookings = st.session_state.bookings.nlargest(5, 'Booking Date')
        st.dataframe(recent_bookings[['Booking ID', 'Customer', 'Jewelry Item', 'Amount (LKR)', 'Status']], 
                    use_container_width=True, hide_index=True)

# Shop Approval Page
def show_shop_approval():
    st.markdown('<h1 style="text-align: center; color: #B76E79;">🏪 Shop Approval Management</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Filter tabs
    tab1, tab2, tab3 = st.tabs(["⏳ Pending Approval", "✅ Approved Shops", "❌ Rejected Shops"])
    
    with tab1:
        pending = st.session_state.shops[st.session_state.shops['Status'] == 'Pending']
        if len(pending) > 0:
            st.info(f"📋 {len(pending)} shops awaiting approval")
            
            for idx, row in pending.iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                    with col1:
                        st.markdown(f"**{row['Shop Name']}**")
                        st.caption(f"Owner: {row['Owner']}")
                    with col2:
                        st.markdown(f"📍 {row['Location']}")
                        st.caption(f"📧 {row['Email']}")
                    with col3:
                        st.markdown(f"<span class='status-pending'>Pending</span>", unsafe_allow_html=True)
                    with col4:
                        if st.button(f"✓ Approve", key=f"approve_{idx}"):
                            st.session_state.shops.at[idx, 'Status'] = 'Approved'
                            st.success(f"Approved {row['Shop Name']}")
                            st.rerun()
                        if st.button(f"✗ Reject", key=f"reject_{idx}"):
                            st.session_state.shops.at[idx, 'Status'] = 'Rejected'
                            st.error(f"Rejected {row['Shop Name']}")
                            st.rerun()
                    st.markdown("---")
        else:
            st.success("🎉 No pending approvals! All caught up.")
    
    with tab2:
        approved = st.session_state.shops[st.session_state.shops['Status'] == 'Approved']
        st.success(f"✅ {len(approved)} approved shops")
        st.dataframe(approved[['Shop ID', 'Shop Name', 'Owner', 'Location', 'Registration Date', 'Jewelry Count']], 
                    use_container_width=True, hide_index=True)
    
    with tab3:
        rejected = st.session_state.shops[st.session_state.shops['Status'] == 'Rejected']
        if len(rejected) > 0:
            st.error(f"❌ {len(rejected)} rejected shops")
            st.dataframe(rejected[['Shop ID', 'Shop Name', 'Owner', 'Location', 'Registration Date']], 
                        use_container_width=True, hide_index=True)
        else:
            st.info("No rejected shops")

# Manage Listings Page
def show_listings():
    st.markdown('<h1 style="text-align: center; color: #B76E79;">💍 Jewelry Listings Management</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_shop = st.selectbox("Filter by Shop", ["All"] + st.session_state.shops['Shop Name'].tolist())
    with col2:
        filter_type = st.selectbox("Filter by Type", ["All"] + st.session_state.jewelry['Type'].unique().tolist())
    with col3:
        filter_status = st.selectbox("Filter by Status", ["All"] + st.session_state.jewelry['Status'].unique().tolist())
    
    # Apply filters
    filtered_df = st.session_state.jewelry.copy()
    if filter_shop != "All":
        filtered_df = filtered_df[filtered_df['Shop'] == filter_shop]
    if filter_type != "All":
        filtered_df = filtered_df[filtered_df['Type'] == filter_type]
    if filter_status != "All":
        filtered_df = filtered_df[filtered_df['Status'] == filter_status]
    
    st.markdown(f"**Showing {len(filtered_df)} items**")
    
    # Display as expandable cards
    for idx, row in filtered_df.iterrows():
        with st.expander(f"{row['Item Name']} - {row['Shop']} ({row['Status']})"):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"**Type:** {row['Type']}")
                st.markdown(f"**Material:** {row['Material']}")
                st.markdown(f"**Date Added:** {row['Date Added'].strftime('%Y-%m-%d')}")
            with col2:
                st.markdown(f"**Price:** LKR {row['Price (LKR)']:,}")
                st.markdown(f"**Rental/Day:** LKR {row['Rental Price/Day (LKR)']:,}")
                status_color = "#28a745" if row['Status'] == 'Available' else "#dc3545" if row['Status'] == 'Rented' else "#ffc107"
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{row['Status']}</span>", unsafe_allow_html=True)
            with col3:
                if st.button("🗑️ Remove", key=f"remove_{idx}"):
                    st.session_state.jewelry = st.session_state.jewelry.drop(idx)
                    st.warning(f"Removed {row['Item Name']}")
                    st.rerun()
                if st.button("✏️ Edit", key=f"edit_{idx}"):
                    st.info("Edit functionality would open a modal here")
    
    # Bulk actions
    st.markdown("---")
    st.subheader("📊 Listing Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Items", len(st.session_state.jewelry))
    with col2:
        available = len(st.session_state.jewelry[st.session_state.jewelry['Status'] == 'Available'])
        st.metric("Available", available)
    with col3:
        rented = len(st.session_state.jewelry[st.session_state.jewelry['Status'] == 'Rented'])
        st.metric("Rented", rented)
    with col4:
        maintenance = len(st.session_state.jewelry[st.session_state.jewelry['Status'] == 'Maintenance'])
        st.metric("Maintenance", maintenance)

# View Bookings Page
def show_bookings():
    st.markdown('<h1 style="text-align: center; color: #B76E79;">📅 Booking Management</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        confirmed = len(st.session_state.bookings[st.session_state.bookings['Status'] == 'Confirmed'])
        st.metric("Confirmed", confirmed)
    with col2:
        pending = len(st.session_state.bookings[st.session_state.bookings['Status'] == 'Pending'])
        st.metric("Pending", pending)
    with col3:
        completed = len(st.session_state.bookings[st.session_state.bookings['Status'] == 'Completed'])
        st.metric("Completed", completed)
    with col4:
        cancelled = len(st.session_state.bookings[st.session_state.bookings['Status'] == 'Cancelled'])
        st.metric("Cancelled", cancelled)
    
    st.markdown("---")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.multiselect("Filter by Status", st.session_state.bookings['Status'].unique(), default=[])
    with col2:
        type_filter = st.multiselect("Filter by Type", st.session_state.bookings['Type'].unique(), default=[])
    
    filtered_bookings = st.session_state.bookings.copy()
    if status_filter:
        filtered_bookings = filtered_bookings[filtered_bookings['Status'].isin(status_filter)]
    if type_filter:
        filtered_bookings = filtered_bookings[filtered_bookings['Type'].isin(type_filter)]
    
    # Display bookings
    st.subheader(f"All Bookings ({len(filtered_bookings)})")
    
    # Styled dataframe
    def color_status(val):
        if val == 'Confirmed':
            return 'background-color: #d4edda; color: #155724'
        elif val == 'Pending':
            return 'background-color: #fff3cd; color: #856404'
        elif val == 'Completed':
            return 'background-color: #d1ecf1; color: #0c5460'
        elif val == 'Cancelled':
            return 'background-color: #f8d7da; color: #721c24'
        return ''
    
    styled_df = filtered_bookings.style.applymap(color_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Booking Timeline Chart
    st.markdown("---")
    st.subheader("📊 Booking Timeline")
    
    timeline_data = st.session_state.bookings.copy()
    timeline_data['Month'] = timeline_data['Booking Date'].dt.strftime('%B %Y')
    monthly_bookings = timeline_data.groupby('Month').size().reset_index(name='Count')
    
    fig = px.bar(monthly_bookings, x='Month', y='Count', 
                 color_discrete_sequence=['#B76E79'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# System Statistics Page
def show_statistics():
    st.markdown('<h1 style="text-align: center; color: #B76E79;">📈 System Statistics</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💰 Revenue by Shop")
        revenue_by_shop = st.session_state.bookings.groupby('Shop')['Amount (LKR)'].sum().sort_values(ascending=True)
        fig = px.bar(revenue_by_shop, orientation='h', color_discrete_sequence=['#D4AF37'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Booking Status Distribution")
        status_counts = st.session_state.bookings['Status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                     color_discrete_sequence=['#28a745', '#ffc107', '#17a2b8', '#dc3545'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed Statistics Table
    st.markdown("---")
    st.subheader("📋 Detailed Metrics")
    
    stats_data = {
        'Metric': [
            'Total Registered Shops',
            'Active (Approved) Shops',
            'Pending Approvals',
            'Total Jewelry Items',
            'Available for Rent',
            'Currently Rented',
            'Total Bookings',
            'Confirmed Bookings',
            'Total Revenue (LKR)',
            'Average Booking Value (LKR)'
        ],
        'Value': [
            len(st.session_state.shops),
            len(st.session_state.shops[st.session_state.shops['Status'] == 'Approved']),
            len(st.session_state.shops[st.session_state.shops['Status'] == 'Pending']),
            len(st.session_state.jewelry),
            len(st.session_state.jewelry[st.session_state.jewelry['Status'] == 'Available']),
            len(st.session_state.jewelry[st.session_state.jewelry['Status'] == 'Rented']),
            len(st.session_state.bookings),
            len(st.session_state.bookings[st.session_state.bookings['Status'] == 'Confirmed']),
            f"{st.session_state.bookings['Amount (LKR)'].sum():,.0f}",
            f"{st.session_state.bookings['Amount (LKR)'].mean():,.0f}"
        ]
    }
    
    stats_df = pd.DataFrame(stats_data)
    st.table(stats_df)

# System Monitoring Page
def show_monitoring():
    st.markdown('<h1 style="text-align: center; color: #B76E79;">🔍 System Monitoring</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # System Health Indicators
    st.subheader("🖥️ System Health")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Simulated system metrics
    import random
    
    with col1:
        cpu_usage = random.randint(20, 45)
        st.metric("CPU Usage", f"{cpu_usage}%", delta=f"{random.randint(-5, 5)}%")
        st.progress(cpu_usage / 100)
    
    with col2:
        memory_usage = random.randint(40, 60)
        st.metric("Memory Usage", f"{memory_usage}%", delta=f"{random.randint(-3, 3)}%")
        st.progress(memory_usage / 100)
    
    with col3:
        disk_usage = random.randint(30, 50)
        st.metric("Disk Usage", f"{disk_usage}%", delta=f"{random.randint(-2, 2)}%")
        st.progress(disk_usage / 100)
    
    with col4:
        st.metric("Active Users", random.randint(15, 45), delta=f"+{random.randint(1, 5)}")
    
    st.markdown("---")
    
    # Data Integrity Checks
    st.subheader("✅ Data Integrity Checks")
    
    checks = [
        ("Database Connection", "✅ Connected", "#28a745"),
        ("Backup Status", "✅ Last backup: 2 hours ago", "#28a745"),
        ("Orphaned Records", "✅ No issues found", "#28a745"),
        ("Payment Gateway", "✅ Operational", "#28a745"),
        ("Image Storage", "⚠️ 3 images pending optimization", "#ffc107"),
    ]
    
    for check_name, status, color in checks:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{check_name}**")
        with col2:
            st.markdown(f"<span style='color: {color}; font-weight: bold;'>{status}</span>", unsafe_allow_html=True)
    
    # Issue Reporting
    st.markdown("---")
    st.subheader("🚨 Report System Issues")
    
    with st.form("issue_form"):
        issue_type = st.selectbox("Issue Type", ["Bug", "Performance", "Security", "Data Integrity", "Other"])
        severity = st.select_slider("Severity", options=["Low", "Medium", "High", "Critical"])
        description = st.text_area("Description", placeholder="Describe the issue in detail...")
        
        if st.form_submit_button("🚀 Submit Report"):
            st.success(f"Issue reported successfully! Ticket ID: TKT{random.randint(1000, 9999)}")
    
    # Activity Log
    st.markdown("---")
    st.subheader("📝 Recent Admin Activity")
    
    activity_log = pd.DataFrame({
        'Timestamp': [datetime.now() - timedelta(minutes=x*15) for x in range(10)],
        'Admin': ['admin'] * 10,
        'Action': [
            'Approved shop: Crystal Crown',
            'Removed jewelry item: Vintage Ring',
            'Viewed booking report',
            'Updated system settings',
            'Approved shop: Jewel Junction',
            'Viewed dashboard statistics',
            'Exported booking data',
            'Reviewed pending listings',
            'System health check',
            'Backup initiated'
        ],
        'Status': ['Success'] * 10
    })
    
    st.dataframe(activity_log, use_container_width=True, hide_index=True)

# Main App Logic
def main():
    if not st.session_state.authenticated:
        login()
    else:
        # Sidebar Navigation
        with st.sidebar:
            st.markdown("<h2 style='text-align: center; color: #D4AF37;'>💎 Bridora</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #B76E79;'>Admin Control Panel</p>", unsafe_allow_html=True)
            st.markdown("---")
            
            # Navigation
            st.markdown("### 📍 Navigation")
            
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
            if st.button("🏪 Approve Shops", use_container_width=True):
                st.session_state.current_page = "Shops"
                st.rerun()
            if st.button("💍 Manage Listings", use_container_width=True):
                st.session_state.current_page = "Listings"
                st.rerun()
            if st.button("📅 View Bookings", use_container_width=True):
                st.session_state.current_page = "Bookings"
                st.rerun()
            if st.button("📈 Statistics", use_container_width=True):
                st.session_state.current_page = "Statistics"
                st.rerun()
            if st.button("🔍 Monitoring", use_container_width=True):
                st.session_state.current_page = "Monitoring"
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 👤 Admin Profile")
            st.markdown("**Username:** admin")
            st.markdown("**Role:** Super Administrator")
            st.markdown(f"**Last Login:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
        
        # Page Routing
        if st.session_state.current_page == "Dashboard":
            show_dashboard()
        elif st.session_state.current_page == "Shops":
            show_shop_approval()
        elif st.session_state.current_page == "Listings":
            show_listings()
        elif st.session_state.current_page == "Bookings":
            show_bookings()
        elif st.session_state.current_page == "Statistics":
            show_statistics()
        elif st.session_state.current_page == "Monitoring":
            show_monitoring()

if __name__ == "__main__":
    main()