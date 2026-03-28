import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
from PIL import Image
import base64
from io import BytesIO

# ========================
# Page Configuration
# ========================
st.set_page_config(
    page_title="Bridora – Bridal Jewelry Marketplace",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# Custom CSS (Rose Gold Theme)
# ========================
st.markdown("""
<style>
    /* Main Theme */
    :root {
        --primary: #B76E79;
        --secondary: #F4E7E7;
        --accent: #D4AF37;
        --text: #4A4A4A;
        --bg: #FDF8F8;
    }
    .stApp {
        background: linear-gradient(135deg, #FDF8F8 0%, #F4E7E7 100%);
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2C3E50 0%, #1A252F 100%);
        color: white;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    /* Cards */
    .jewelry-card {
        background: white;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(183,110,121,0.1);
        transition: transform 0.3s ease;
        border-left: 4px solid #B76E79;
    }
    .jewelry-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(183,110,121,0.2);
    }
    .price-tag {
        font-size: 1.4em;
        font-weight: bold;
        color: #B76E79;
    }
    .shop-name {
        font-size: 0.9em;
        color: #6c757d;
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .status-available {
        background: #d4edda;
        color: #155724;
    }
    .status-rented {
        background: #f8d7da;
        color: #721c24;
    }
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #B76E79 0%, #D4AF37 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 8px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(183,110,121,0.4);
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
        font-size: 2.8em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Filter panel */
    .filter-panel {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    /* Chatbot */
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .user-message {
        background: #B76E79;
        color: white;
        margin-left: auto;
    }
    .bot-message {
        background: #f0f0f0;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# ========================
# Data Handling (JSON Files)
# ========================
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def load_json(filename, default_data):
    """Load JSON file, create with default if missing."""
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        save_json(filename, default_data)
        return default_data

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)

def load_all_data():
    """Load all JSON files into session state DataFrames."""
    # Default sample data
    default_shops = [
        {"Shop ID": "SHOP0001", "Shop Name": "Royal Jewellers", "Owner": "Kumar Sangakkara",
         "Email": "royal@jewellers.lk", "Location": "Colombo 07", "Status": "Approved",
         "Registration Date": (datetime.now() - timedelta(days=45)).isoformat(), "Jewelry Count": 45},
        {"Shop ID": "SHOP0002", "Shop Name": "Golden Palace", "Owner": "Mahela Jayawardene",
         "Email": "golden@palace.lk", "Location": "Kandy", "Status": "Approved",
         "Registration Date": (datetime.now() - timedelta(days=40)).isoformat(), "Jewelry Count": 32},
        {"Shop ID": "SHOP0003", "Shop Name": "Diamond Dreams", "Owner": "Lasith Malinga",
         "Email": "diamond@dreams.lk", "Location": "Galle", "Status": "Approved",
         "Registration Date": (datetime.now() - timedelta(days=35)).isoformat(), "Jewelry Count": 28},
    ]
    default_jewelry = []
    types = ['Necklace', 'Earrings', 'Bracelet', 'Ring', 'Tiara', 'Anklet', 'Bangle']
    materials = ['Gold', 'Diamond', 'Pearl', 'Silver', 'Platinum', 'Gemstone']
    shops = ["Royal Jewellers", "Golden Palace", "Diamond Dreams"]
    for i in range(1, 16):
        default_jewelry.append({
            "Item ID": f"JWL{i:05d}",
            "Item Name": f"{random.choice(['Royal', 'Elegant', 'Classic', 'Modern', 'Vintage'])} {random.choice(types)}",
            "Shop": random.choice(shops),
            "Type": random.choice(types),
            "Material": random.choice(materials),
            "Price (LKR)": random.randint(15000, 500000),
            "Rental Price/Day (LKR)": random.randint(2000, 25000),
            "Status": random.choice(['Available', 'Rented', 'Reserved']),
            "Date Added": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
            "Image": None  # placeholder
        })
    default_users = [
        {"User ID": "USR0001", "Username": "raslan", "Password": "raslan123",
         "Name": "Raslan Mohammadh", "Email": "raslan@example.com", "Phone": "0756561730"}
    ]
    default_bookings = []

    # Load or create
    shops = load_json("shops.json", default_shops)
    jewelry = load_json("jewelry.json", default_jewelry)
    users = load_json("users.json", default_users)
    bookings = load_json("bookings.json", default_bookings)

    # Convert to DataFrames
    st.session_state.shops_df = pd.DataFrame(shops)
    st.session_state.jewelry_df = pd.DataFrame(jewelry)
    st.session_state.users_df = pd.DataFrame(users)
    st.session_state.bookings_df = pd.DataFrame(bookings)

    # Ensure date columns are datetime
    if 'Registration Date' in st.session_state.shops_df.columns:
        st.session_state.shops_df['Registration Date'] = pd.to_datetime(st.session_state.shops_df['Registration Date'])
    if 'Date Added' in st.session_state.jewelry_df.columns:
        st.session_state.jewelry_df['Date Added'] = pd.to_datetime(st.session_state.jewelry_df['Date Added'])
    if 'Booking Date' in st.session_state.bookings_df.columns:
        st.session_state.bookings_df['Booking Date'] = pd.to_datetime(st.session_state.bookings_df['Booking Date'])
    if 'Wedding Date' in st.session_state.bookings_df.columns:
        st.session_state.bookings_df['Wedding Date'] = pd.to_datetime(st.session_state.bookings_df['Wedding Date'])

def save_all_data():
    """Save DataFrames back to JSON files."""
    save_json("shops.json", st.session_state.shops_df.to_dict('records'))
    save_json("jewelry.json", st.session_state.jewelry_df.to_dict('records'))
    save_json("users.json", st.session_state.users_df.to_dict('records'))
    save_json("bookings.json", st.session_state.bookings_df.to_dict('records'))

# ========================
# Helper Functions
# ========================
def authenticate_user(username, password):
    user = st.session_state.users_df[(st.session_state.users_df['Username'] == username) &
                                     (st.session_state.users_df['Password'] == password)]
    if not user.empty:
        st.session_state.user = user.iloc[0].to_dict()
        return True
    return False

def register_user(name, username, password, email, phone):
    if username in st.session_state.users_df['Username'].values:
        return False, "Username already exists"
    new_id = f"USR{len(st.session_state.users_df)+1:04d}"
    new_user = {
        "User ID": new_id,
        "Username": username,
        "Password": password,
        "Name": name,
        "Email": email,
        "Phone": phone
    }
    st.session_state.users_df = pd.concat([st.session_state.users_df, pd.DataFrame([new_user])], ignore_index=True)
    save_all_data()
    return True, "Registration successful! Please login."

def add_booking(jewelry_id, user_id, name, contact, wedding_date, type_rental, days=None):
    jewelry = st.session_state.jewelry_df[st.session_state.jewelry_df['Item ID'] == jewelry_id].iloc[0]
    if jewelry['Status'] != 'Available':
        return False, "This item is not available for booking."
    wedding_date_obj = datetime.strptime(wedding_date, "%Y-%m-%d")
    if wedding_date_obj < datetime.now():
        return False, "Wedding date must be in the future."

    # Calculate amount
    if type_rental == "Rental":
        price_per_day = jewelry['Rental Price/Day (LKR)']
        amount = price_per_day * days
    else:
        amount = jewelry['Price (LKR)']

    booking_id = f"BKG{len(st.session_state.bookings_df)+1:05d}"
    new_booking = {
        "Booking ID": booking_id,
        "Customer": name,
        "Jewelry Item": jewelry['Item Name'],
        "Jewelry ID": jewelry_id,
        "Shop": jewelry['Shop'],
        "User ID": user_id,
        "Booking Date": datetime.now().isoformat(),
        "Wedding Date": wedding_date,
        "Type": type_rental,
        "Amount (LKR)": amount,
        "Status": "Pending",
        "Rental Days": days if type_rental == "Rental" else None
    }
    st.session_state.bookings_df = pd.concat([st.session_state.bookings_df, pd.DataFrame([new_booking])], ignore_index=True)

    # Update jewelry status
    st.session_state.jewelry_df.loc[st.session_state.jewelry_df['Item ID'] == jewelry_id, 'Status'] = 'Reserved'
    save_all_data()
    return True, f"Booking request submitted! Booking ID: {booking_id}"

def get_jewelry_by_id(jewelry_id):
    return st.session_state.jewelry_df[st.session_state.jewelry_df['Item ID'] == jewelry_id].iloc[0]

def filter_jewelry(price_range, style, shop, availability_only):
    df = st.session_state.jewelry_df
    if price_range:
        df = df[(df['Price (LKR)'] >= price_range[0]) & (df['Price (LKR)'] <= price_range[1])]
    if style and style != "All":
        df = df[df['Type'] == style]
    if shop and shop != "All":
        df = df[df['Shop'] == shop]
    if availability_only:
        df = df[df['Status'] == 'Available']
    return df

# ========================
# Pages
# ========================
def show_home():
    st.markdown('<div class="main-header">💎 Bridora – Your Dream Bridal Jewelry Awaits</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Hero section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### ✨ Discover the Perfect Bridal Jewelry")
        st.markdown("""
        Bridora is Sri Lanka's first dedicated online marketplace for **bridal jewelry**.
        Browse hundreds of exquisite pieces from trusted local jewelers, compare prices,
        and book your favorite sets – all from the comfort of your home.
        """)
        if st.button("🛍️ Start Browsing →", use_container_width=False):
            st.session_state.current_page = "Browse"
            st.rerun()
    with col2:
        st.image("https://via.placeholder.com/400x300?text=Bridal+Jewelry", use_container_width=True)

    st.markdown("---")
    st.subheader("✨ Featured Jewelry")
    # Show 3 random featured items
    featured = st.session_state.jewelry_df.sample(min(3, len(st.session_state.jewelry_df)))
    cols = st.columns(3)
    for idx, (_, item) in enumerate(featured.iterrows()):
        with cols[idx]:
            with st.container():
                st.markdown(f'<div class="jewelry-card">', unsafe_allow_html=True)
                st.image("https://via.placeholder.com/200x150?text=Jewelry", use_container_width=True)
                st.markdown(f"**{item['Item Name']}**")
                st.markdown(f"<span class='price-tag'>LKR {item['Price (LKR)']:,}</span>", unsafe_allow_html=True)
                st.markdown(f"<span class='shop-name'>{item['Shop']}</span>", unsafe_allow_html=True)
                if st.button(f"View Details", key=f"featured_{item['Item ID']}"):
                    st.query_params["item_id"] = item['Item ID']
                    st.session_state.current_page = "Details"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Why Bridora?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🛍️ Wide Selection**\nHundreds of bridal sets from top jewelers.")
    with col2:
        st.markdown("**💰 Best Prices**\nCompare prices and rental options.")
    with col3:
        st.markdown("**🤖 Smart Chatbot**\nGet personalized recommendations instantly.")

def show_browse():
    st.markdown('<div class="main-header">💍 Browse Bridal Jewelry</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Filters panel
    with st.expander("🔍 Filter Jewelry", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            min_price = int(st.session_state.jewelry_df['Price (LKR)'].min())
            max_price = int(st.session_state.jewelry_df['Price (LKR)'].max())
            price_range = st.slider("Price Range (LKR)", min_price, max_price, (min_price, max_price))
        with col2:
            styles = ["All"] + sorted(st.session_state.jewelry_df['Type'].unique().tolist())
            style = st.selectbox("Style / Type", styles)
        with col3:
            shops = ["All"] + sorted(st.session_state.jewelry_df['Shop'].unique().tolist())
            shop = st.selectbox("Shop", shops)
        with col4:
            available_only = st.checkbox("Show only available items")

    # Apply filters
    filtered = filter_jewelry(price_range, style, shop, available_only)
    st.markdown(f"**{len(filtered)} items found**")

    # Display as cards
    for _, item in filtered.iterrows():
        with st.container():
            st.markdown(f'<div class="jewelry-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image("https://via.placeholder.com/150x150?text=Jewelry", use_container_width=True)
            with col2:
                st.markdown(f"### {item['Item Name']}")
                st.markdown(f"**Shop:** {item['Shop']}  &nbsp; | &nbsp; **Style:** {item['Type']}  &nbsp; | &nbsp; **Material:** {item['Material']}")
                st.markdown(f"<span class='price-tag'>Buy: LKR {item['Price (LKR)']:,}</span> &nbsp; | &nbsp; **Rental:** LKR {item['Rental Price/Day (LKR)']:,}/day", unsafe_allow_html=True)
                status_class = "status-available" if item['Status'] == 'Available' else "status-rented"
                st.markdown(f"<span class='status-badge {status_class}'>{item['Status']}</span>", unsafe_allow_html=True)
                if st.button("📖 View Details", key=f"view_{item['Item ID']}"):
                    st.query_params["item_id"] = item['Item ID']
                    st.session_state.current_page = "Details"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

def show_details():
    st.markdown('<div class="main-header">✨ Jewelry Details</div>', unsafe_allow_html=True)
    st.markdown("---")

    item_id = st.query_params.get("item_id")
    if not item_id:
        st.error("No item selected. Go back to browse.")
        if st.button("← Back to Browse"):
            st.session_state.current_page = "Browse"
            st.rerun()
        return

    try:
        item = get_jewelry_by_id(item_id)
    except IndexError:
        st.error("Item not found.")
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://via.placeholder.com/300x300?text=Jewelry", use_container_width=True)
    with col2:
        st.markdown(f"## {item['Item Name']}")
        st.markdown(f"**Shop:** {item['Shop']}")
        st.markdown(f"**Type:** {item['Type']} | **Material:** {item['Material']}")
        st.markdown(f"**Buy Price:** LKR {item['Price (LKR)']:,}")
        st.markdown(f"**Rental Price:** LKR {item['Rental Price/Day (LKR)']:,} per day")
        st.markdown(f"**Status:** {item['Status']}")

        if item['Status'] == 'Available':
            st.success("✅ Available for booking")
            if st.button("📝 Book Now", use_container_width=True):
                st.session_state.booking_item = item.to_dict()
                st.session_state.current_page = "Booking"
                st.rerun()
        else:
            st.warning("This item is currently not available for booking.")

    st.markdown("---")
    if st.button("← Back to Browse"):
        st.session_state.current_page = "Browse"
        st.rerun()

def show_booking_form():
    st.markdown('<div class="main-header">📝 Complete Your Booking</div>', unsafe_allow_html=True)
    st.markdown("---")

    if "booking_item" not in st.session_state:
        st.error("No item selected. Please go back and select an item.")
        if st.button("Back to Browse"):
            st.session_state.current_page = "Browse"
            st.rerun()
        return

    item = st.session_state.booking_item
    st.markdown(f"### Booking: **{item['Item Name']}**")
    st.markdown(f"**Shop:** {item['Shop']} | **Type:** {item['Type']}")

    # Booking type
    booking_type = st.radio("Booking Type", ["Purchase", "Rental"])
    days = None
    if booking_type == "Rental":
        days = st.number_input("Number of days", min_value=1, max_value=30, value=1)
        total = item['Rental Price/Day (LKR)'] * days
        st.markdown(f"**Total Rental Cost:** LKR {total:,}")

    # Customer details
    if 'user' in st.session_state:
        # Auto-fill if logged in
        name = st.session_state.user['Name']
        contact = st.session_state.user['Phone']
        email = st.session_state.user['Email']
        st.info(f"Logged in as {name}")
    else:
        name = st.text_input("Full Name")
        contact = st.text_input("Phone Number")
        email = st.text_input("Email")

    wedding_date = st.date_input("Wedding Date", min_value=datetime.now().date())

    if st.button("Confirm Booking", use_container_width=True):
        if not name or not contact or not email:
            st.error("Please fill all fields.")
        else:
            user_id = st.session_state.user['User ID'] if 'user' in st.session_state else None
            success, msg = add_booking(
                jewelry_id=item['Item ID'],
                user_id=user_id,
                name=name,
                contact=contact,
                wedding_date=wedding_date.strftime("%Y-%m-%d"),
                type_rental=booking_type,
                days=days
            )
            if success:
                st.success(msg)
                st.session_state.pop("booking_item", None)
                st.session_state.current_page = "My Bookings"
                st.rerun()
            else:
                st.error(msg)

    if st.button("Cancel"):
        st.session_state.pop("booking_item", None)
        st.session_state.current_page = "Browse"
        st.rerun()

def show_my_bookings():
    st.markdown('<div class="main-header">📋 My Bookings</div>', unsafe_allow_html=True)
    st.markdown("---")

    if 'user' not in st.session_state:
        st.warning("Please login to view your bookings.")
        if st.button("Login"):
            st.session_state.current_page = "Login"
            st.rerun()
        return

    user_bookings = st.session_state.bookings_df[st.session_state.bookings_df['User ID'] == st.session_state.user['User ID']]
    if user_bookings.empty:
        st.info("You have no bookings yet.")
    else:
        st.dataframe(user_bookings[['Booking ID', 'Jewelry Item', 'Wedding Date', 'Type', 'Amount (LKR)', 'Status']],
                     use_container_width=True, hide_index=True)

def show_chatbot():
    st.markdown('<div class="main-header">🤖 Bridora Assistant</div>', unsafe_allow_html=True)
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your bridal jewelry assistant. How can I help you today?\n\n💬 Ask me about:\n- Jewelry recommendations\n- Booking process\n- Price ranges\n- Styles (Temple, Gold, Modern)"}
        ]

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about bridal jewelry..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Simple rule-based response
        response = generate_chatbot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

def generate_chatbot_response(user_input):
    user_input = user_input.lower()

    # Greetings
    if any(word in user_input for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! I'm here to help you find the perfect bridal jewelry. What style are you looking for? (Temple, Gold, Modern, etc.)"

    # Booking help
    if "book" in user_input or "how to book" in user_input:
        return "To book a jewelry set:\n1. Browse the gallery\n2. Click 'View Details' on an available item\n3. Click 'Book Now' and fill in your details\n4. Submit the booking request. You'll receive a confirmation soon!"

    # Price
    if "price" in user_input or "cost" in user_input:
        return "Our jewelry pieces range from LKR 15,000 to LKR 500,000 for purchase. Rental starts from LKR 2,000 per day. You can filter by price in the Browse section."

    # Style recommendations
    if "temple" in user_input:
        return "Temple jewelry is traditional and intricate. Some popular temple sets: 'Royal Temple Necklace' and 'Golden Temple Earrings'. Check them out in the gallery!"
    if "gold" in user_input:
        return "Gold jewelry is timeless. We have many 22k and 18k gold sets. Would you like to see heavy gold sets or lightweight daily wear?"
    if "modern" in user_input:
        return "Modern designs include minimalist diamond sets and contemporary geometric patterns. We have several modern collections available."

    # Budget recommendation
    if "budget" in user_input or "under" in user_input:
        import re
        numbers = re.findall(r'\d+', user_input)
        if numbers:
            budget = int(numbers[0])
            available = st.session_state.jewelry_df[st.session_state.jewelry_df['Price (LKR)'] <= budget]
            if not available.empty:
                top = available.nsmallest(3, 'Price (LKR)')
                suggestions = "\n".join([f"- {row['Item Name']} (LKR {row['Price (LKR)']:,})" for _, row in top.iterrows()])
                return f"Here are some pieces within LKR {budget:,}:\n{suggestions}\n\nWould you like more details on any of these?"
            else:
                return f"Sorry, no pieces found under LKR {budget:,}. Try increasing your budget or explore our rental options!"
        else:
            return "Please specify your budget amount, e.g., 'budget under 50000'."

    # Fallback
    return "I'm still learning! For more details, please browse our catalog or contact the shop directly. Can I help you with a specific style or budget?"

def show_login():
    st.markdown('<div class="main-header">🔐 Login / Register</div>', unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if authenticate_user(username, password):
                    st.success("Login successful!")
                    st.session_state.current_page = "Home"
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    with tab2:
        with st.form("register_form"):
            name = st.text_input("Full Name")
            username = st.text_input("Choose a Username")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                if password != confirm:
                    st.error("Passwords do not match")
                else:
                    success, msg = register_user(name, username, password, email, phone)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

def logout():
    if 'user' in st.session_state:
        del st.session_state.user
    st.success("Logged out successfully")
    st.session_state.current_page = "Home"
    st.rerun()

# ========================
# Main App
# ========================
def main():
    # Load data
    if "shops_df" not in st.session_state:
        load_all_data()

    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #D4AF37;'>💎 Bridora</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #B76E79;'>Bridal Jewelry Marketplace</p>", unsafe_allow_html=True)
        st.markdown("---")

        # Navigation
        st.markdown("### 🧭 Navigation")
        nav_options = ["🏠 Home", "🛍️ Browse", "🤖 Chatbot"]
        if 'user' in st.session_state:
            nav_options.append("📋 My Bookings")
            nav_options.append("👤 Profile")
        else:
            nav_options.append("🔐 Login")

        for opt in nav_options:
            if st.button(opt, use_container_width=True):
                if opt == "🏠 Home":
                    st.session_state.current_page = "Home"
                elif opt == "🛍️ Browse":
                    st.session_state.current_page = "Browse"
                elif opt == "🤖 Chatbot":
                    st.session_state.current_page = "Chatbot"
                elif opt == "📋 My Bookings":
                    st.session_state.current_page = "My Bookings"
                elif opt == "👤 Profile":
                    st.session_state.current_page = "Profile"
                elif opt == "🔐 Login":
                    st.session_state.current_page = "Login"
                st.rerun()

        if 'user' in st.session_state:
            st.markdown("---")
            st.markdown(f"**Logged in as:** {st.session_state.user['Name']}")
            if st.button("🚪 Logout", use_container_width=True):
                logout()

    # Page routing
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    if st.session_state.current_page == "Home":
        show_home()
    elif st.session_state.current_page == "Browse":
        show_browse()
    elif st.session_state.current_page == "Details":
        show_details()
    elif st.session_state.current_page == "Booking":
        show_booking_form()
    elif st.session_state.current_page == "My Bookings":
        show_my_bookings()
    elif st.session_state.current_page == "Chatbot":
        show_chatbot()
    elif st.session_state.current_page == "Login":
        show_login()
    elif st.session_state.current_page == "Profile":
        st.markdown('<div class="main-header">👤 My Profile</div>', unsafe_allow_html=True)
        if 'user' in st.session_state:
            st.json(st.session_state.user)
        else:
            st.warning("Please login first.")
    else:
        show_home()

if __name__ == "__main__":
    main()