import streamlit as st
import sqlite3
import hashlib
import re

# ----------- DATABASE SETUP -----------
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
             username TEXT PRIMARY KEY, 
             password TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS cart (
             id INTEGER PRIMARY KEY, 
             name TEXT, 
             price REAL, 
             image TEXT, 
             quantity INTEGER)""")

# ----------- SESSION STATE -----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ----------- RERUN HELPER FUNCTION -----------
def rerun():
    st.session_state['_rerun_flag'] = not st.session_state.get('_rerun_flag', False)

# ----------- PASSWORD UTILITIES -----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*]", password)
    )

# ----------- CART FUNCTIONS -----------
def add_to_cart(product):
    c.execute("SELECT quantity FROM cart WHERE name=?", (product['name'],))
    result = c.fetchone()
    if result:
        c.execute("UPDATE cart SET quantity = quantity + 1 WHERE name=?", (product['name'],))
    else:
        c.execute("INSERT INTO cart (name, price, image, quantity) VALUES (?, ?, ?, ?)",
                  (product['name'], product['price'], product['image'], 1))
    conn.commit()

def get_cart():
    c.execute("SELECT * FROM cart")
    return c.fetchall()

def clear_cart():
    c.execute("DELETE FROM cart")
    conn.commit()

# ----------- STYLES AND THEME -----------
st.set_page_config(page_title="Shasmeen's Bracelet Shop", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    body {
        background-color: #f9f6f7;
        color: #4b4b4b;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #f4c4c4;
        color: #5a3e3e;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #eaa8a8;
        color: #3b2e2e;
    }
    .stSidebar {
        background-color: #fff0f3;
        padding: 20px;
        border-radius: 12px;
        color: #5a3e3e; /* 💡 Fix: Sidebar text color made dark */
    }
    .css-1d391kg {
        background-color: #f9f6f7;
    }
    .css-1v3fvcr {
        background-color: transparent;
    }
    header, footer {
        text-align: center;
        padding: 12px;
        font-weight: 700;
        font-size: 22px;
        color: #a86d7d;
    }
</style>
""", unsafe_allow_html=True)

# ----------- HEADER & FOOTER -----------
def header():
    st.markdown("<header>💎 Shasmeen's Elegant Bracelet Boutique 💎</header>", unsafe_allow_html=True)

def footer():
    st.markdown("<footer>© 2025 Shasmeen's Bracelet Shop | Designed with ❤️</footer>", unsafe_allow_html=True)

header()

# ----------- NAVIGATION -----------
if st.session_state.logged_in:
    pages = ["Home", "Products", "Cart", "Checkout", "Logout"]
else:
    pages = ["Sign Up", "Login", "Home"]

choice = st.sidebar.selectbox("Navigate", pages)

# 💡 FIXED SIDEBAR FOOTER TEXT COLOR
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="font-size:14px; color:#5a3e3e; padding: 20px;">
        <strong>About Me:</strong><br>
        Hey! I'm Shasmeen 💗<br>
        Creator of this bracelet shop.<br><br>
        <strong>Contact IDs:</strong><br>
        Instagram: @shasmeen_official<br>
        Email: shasmeenasim@gmail.com<br>
        LinkedIn: shasmeenZahra
    </div>
    """,
    unsafe_allow_html=True
)

# ----------- ABOUT ME SECTION -----------
def about_me():
    st.markdown(
        """
        <div style="background:#fff0f3; padding:20px; border-radius:12px; margin-bottom:25px;">
            <h2 style="color:#a86d7d;">About Me</h2>
            <p>Hey there! I’m Shasmeen, the heart behind My Bracelets Shop! 💖
This is my little space full of love, colors, and cute handmade bracelets made just for you! 🎨✨

Each bracelet is designed with care — some are fun, some are simple, and some are totally unique (just like you!) 🌈 Whether you’re gifting it to a friend or treating yourself, you’ll definitely find something that makes you smile. 😊🎁

My bracelets aren’t just accessories — they’re tiny pieces of joy and style that brighten up your day! 💕
Thank you for stopping by and being part of my small creative world. Your support means the world to me! 🌍💫

Stay happy, stay shiny — just like our bracelets! ✨

— Shasmeen 💗

 </div>
        """, unsafe_allow_html=True)

# ----------- PAGES -----------

if choice == "Home":
    st.header("🏠 Welcome to Shasmeen's Boutique")
    about_me()
    st.write("Your one-stop shop for beautiful bracelets 💍✨")

elif choice == "Products" and st.session_state.logged_in:
    st.header("🛍️ All Bracelets")
    enhanced_products = [
        {"id": 1, "name": "Silver Chain", "price": 25.0, "images": ["silver_chain.jpg", "silver_chain1.jpg", "silver_chain2.jpg"]},
        {"id": 2, "name": "Gold Charm", "price": 40.0, "images": ["gold_charm.jpg", "gold_charm1.jpg", "gold_charm2.jpg"]},
        {"id": 3, "name": "Beaded Set", "price": 18.0, "images": ["beaded_set.jpg", "beaded_set1.jpg", "beaded_set2.jpg"]},
        {"id": 4, "name": "Pearl Bracelet", "price": 32.0, "images": ["pearl_bracelet.jpg", "pearl_bracelet1.jpg", "pearl_bracelet2.jpg"]},
        {"id": 5, "name": "Leather Wrap", "price": 22.0, "images": ["leather_wrap.jpg", "leather_wrap1.jpg", "leather_wrap2.jpg"]},
        {"id": 6, "name": "Diamond Tennis", "price": 120.0, "images": ["diamond_tennis.jpg", "diamond_tennis1.jpg", "diamond_tennis2.jpg"]},
        {"id": 7, "name": "Friendship Bracelet", "price": 15.0, "images": ["friendship.jpg", "friendship1.jpg", "friendship2.jpg"]},
        {"id": 8, "name": "Hero Bracelet", "price": 38.0, "images": ["hero_bracelet.jpg", "hero_bracelet1.jpg", "hero_bracelet2.jpg"]},
    ]
    for p in enhanced_products:
        st.subheader(f"{p['name']} - ${p['price']}")
        cols = st.columns(len(p["images"]))
        for idx, img in enumerate(p["images"]):
            with cols[idx]:
                st.image(f"images/{img.strip()}", use_container_width=True)
        if st.button(f"Add to Cart {p['id']}"):
            add_to_cart({"name": p["name"], "price": p["price"], "image": p["images"][0]})
            st.success(f"Added {p['name']} to cart!")

elif choice == "Login":
    st.header("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if result and verify_password(password, result[0]):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            rerun()
        else:
            st.error("Invalid username or password")

elif choice == "Sign Up":
    st.header("📝 Create Account")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")

    st.markdown("""
    **Password must include:**
    - At least 8 characters  
    - One uppercase and one lowercase letter  
    - One number  
    - One special character (!@#$%^&*)
    """)

    if st.button("Create Account"):
        if not is_strong_password(password):
            st.warning("Password does not meet the requirements.")
        else:
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            if c.fetchone():
                st.error("Username already exists.")
            else:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                          (username, hash_password(password)))
                conn.commit()
                st.success("Account created successfully! Please login.")

elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully.")
    rerun()

elif choice == "Cart" and st.session_state.logged_in:
    st.header("🛒 Your Cart")
    items = get_cart()
    if items:
        total = 0
        for i in items:
            st.image(f"images/{i[3]}", width=100)
            st.write(f"{i[1]} - ${i[2]} x {i[4]}")
            total += i[2] * i[4]
        st.write(f"**Total: ${total:.2f}**")
        if st.button("Clear Cart"):
            clear_cart()
            st.success("Cart cleared!")
    else:
        st.info("Your cart is empty.")

elif choice == "Checkout" and st.session_state.logged_in:
    st.header("💳 Checkout")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    address = st.text_area("Shipping Address")
    if st.button("Place Order"):
        if not name or not email or not address:
            st.warning("Please fill in all fields.")
        else:
            clear_cart()
            st.success("Thank you for your order!")

footer()
