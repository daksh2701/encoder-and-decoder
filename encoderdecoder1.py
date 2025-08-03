import streamlit as st
import string
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Caesar Cipher Pro",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #6C757D;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .encryption-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .result-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    .result-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .result-text {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        word-break: break-all;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 30%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #ff9800;
        margin: 1rem 0;
    }
    
    .stats-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    
    .stat-item {
        display: flex;
        justify-content: space-between;
        margin: 0.8rem 0;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .stat-label {
        font-weight: 500;
        color: #555;
    }
    
    .stat-value {
        font-weight: 600;
        color: #667eea;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8 0%, #6b5b95 100%);
    }
    
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.2);
    }
    
    .history-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .cipher-wheel {
        text-align: center;
        font-size: 4rem;
        margin: 1rem 0;
        animation: rotate 10s linear infinite;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .success-animation {
        animation: pulse 1s ease-in-out;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .sidebar-content {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_operations' not in st.session_state:
    st.session_state.total_operations = 0

# Caesar cipher function
def caesar_cipher(text, shift, mode):
    """
    Encrypts or decrypts text using Caesar cipher
    """
    alphabet = string.ascii_lowercase
    result = ""
    
    if mode == "decode":
        shift = -shift
    
    for char in text:
        if char.lower() in alphabet:
            # Handle both uppercase and lowercase
            is_upper = char.isupper()
            char_lower = char.lower()
            shifted_pos = (alphabet.index(char_lower) + shift) % len(alphabet)
            new_char = alphabet[shifted_pos]
            result += new_char.upper() if is_upper else new_char
        else:
            # Keep non-alphabetic characters unchanged
            result += char
    
    return result

def add_to_history(original, result, shift, mode):
    """Add operation to history"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.history.insert(0, {
        'original': original,
        'result': result,
        'shift': shift,
        'mode': mode,
        'timestamp': timestamp
    })
    if len(st.session_state.history) > 10:  # Keep only last 10
        st.session_state.history.pop()
    st.session_state.total_operations += 1

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 🔐 Cipher Settings")
    
    # Mode selection
    mode = st.selectbox(
        "Choose Operation",
        ["encode", "decode"],
        format_func=lambda x: "🔒 Encrypt" if x == "encode" else "🔓 Decrypt"
    )
    
    # Shift amount
    shift = st.slider("Shift Amount", 1, 25, 3, help="Number of positions to shift in the alphabet")
    
    # Quick shift presets
    st.markdown("**Quick Presets:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("ROT13", help="Classic ROT13 cipher"):
            shift = 13
            st.rerun()
    with col2:
        if st.button("Caesar", help="Historical Caesar shift"):
            shift = 3
            st.rerun()
    with col3:
        if st.button("Random", help="Random shift"):
            import random
            shift = random.randint(1, 25)
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics
    if st.session_state.total_operations > 0:
        st.markdown("### 📊 Statistics")
        st.markdown('<div class="stats-container">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-item">
            <span class="stat-label">Total Operations:</span>
            <span class="stat-value">{st.session_state.total_operations}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Current Shift:</span>
            <span class="stat-value">{shift}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Mode:</span>
            <span class="stat-value">{'🔒 Encrypt' if mode == 'encode' else '🔓 Decrypt'}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="main-header">🔐 Caesar Cipher Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Professional encryption and decryption tool with advanced features</p>', unsafe_allow_html=True)

# Cipher wheel animation
st.markdown('<div class="cipher-wheel">⚙️</div>', unsafe_allow_html=True)

# Main input section
st.markdown('<div class="encryption-container">', unsafe_allow_html=True)

# Information about current settings
action_word = "Encrypting" if mode == "encode" else "Decrypting"
st.markdown(f"""
<div class="info-box">
    <strong>🎯 Current Operation:</strong> {action_word} with shift of <strong>{shift}</strong> positions<br>
    <strong>📝 Instructions:</strong> Enter your text below and click the button to {mode} it.
</div>
""", unsafe_allow_html=True)

# Text input
text_input = st.text_area(
    "Enter your message:",
    height=100,
    placeholder="Type your message here... (supports both uppercase and lowercase)",
    help="Enter the text you want to encrypt or decrypt"
)

# Process button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    process_button = st.button(
        f"🔒 {action_word.upper()}" if mode == "encode" else f"🔓 {action_word.upper()}",
        type="primary"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Process the text
if process_button and text_input:
    result = caesar_cipher(text_input, shift, mode)
    add_to_history(text_input, result, shift, mode)
    
    # Display result
    st.markdown('<div class="result-container success-animation">', unsafe_allow_html=True)
    
    icon = "🔒" if mode == "encode" else "🔓"
    operation = "Encrypted" if mode == "encode" else "Decrypted"
    
    st.markdown(f"""
    <div class="result-header">
        {icon} {operation} Result:
    </div>
    <div class="result-text">
        {result}
    </div>
    """, unsafe_allow_html=True)
    
    # Copy button simulation
    st.code(result, language=None)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis
    if result:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Length", len(text_input))
        with col2:
            st.metric("Result Length", len(result))
        with col3:
            alpha_chars = sum(1 for c in text_input if c.isalpha())
            st.metric("Letters Shifted", alpha_chars)

elif process_button and not text_input:
    st.warning("⚠️ Please enter some text to process!")

# How it works section
with st.expander("🧠 How Caesar Cipher Works", expanded=False):
    st.markdown("""
    <div class="info-box">
    <h4>🔍 About Caesar Cipher:</h4>
    
    The Caesar cipher is one of the simplest and most widely known encryption techniques. It's a substitution cipher where each letter in the plaintext is shifted a certain number of places down or up the alphabet.
    
    <h4>📋 Key Features:</h4>
    • <strong>Shift Value:</strong> Determines how many positions to move each letter<br>
    • <strong>Wrap Around:</strong> After 'Z', it continues from 'A'<br>
    • <strong>Case Preservation:</strong> Maintains original letter casing<br>
    • <strong>Non-alphabetic:</strong> Numbers, spaces, and symbols remain unchanged
    
    <h4>💡 Example:</h4>
    With shift = 3: A→D, B→E, C→F, ..., X→A, Y→B, Z→C
    </div>
    """, unsafe_allow_html=True)

# History section
if st.session_state.history:
    with st.expander("📜 Operation History", expanded=False):
        st.markdown("### Recent Operations")
        for i, item in enumerate(st.session_state.history[:5]):
            operation_icon = "🔒" if item['mode'] == 'encode' else "🔓"
            operation_name = "Encrypted" if item['mode'] == 'encode' else "Decrypted"
            
            st.markdown(f"""
            <div class="history-item">
                <strong>{operation_icon} {operation_name}</strong> (Shift: {item['shift']}) - {item['timestamp']}<br>
                <strong>Input:</strong> {item['original'][:50]}{'...' if len(item['original']) > 50 else ''}<br>
                <strong>Output:</strong> {item['result'][:50]}{'...' if len(item['result']) > 50 else ''}
            </div>
            """, unsafe_allow_html=True)

# Control buttons
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Clear History"):
        st.session_state.history = []
        st.session_state.total_operations = 0
        st.success("History cleared!")
        st.rerun()

with col2:
    if st.button("📋 About Caesar Cipher"):
        st.info("""
        **Caesar Cipher** was used by Julius Caesar to communicate with his generals. 
        It's a simple but effective way to encode messages. While not secure by modern standards, 
        it's perfect for learning cryptography basics!
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; font-size: 0.9rem;">
    <strong>🔐 Caesar Cipher Pro</strong> | Built with Streamlit | 
    <em>Historical encryption made modern</em>
</div>
""", unsafe_allow_html=True)