import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os

# Set page configuration
st.set_page_config(page_title="Mother's Day Card", layout="wide")

# Title and description
st.title("🌸 𝕮𝖗𝖊𝖆𝖙𝖊 𝖆 𝕾𝖕𝖊𝖈𝖎𝖆𝖑 𝕸𝖔𝖙𝖍𝖊𝖗'𝖘 𝕯𝖆𝖞 𝕮𝖆𝖗𝖑 🌸")
st.markdown("Celebrate your mom by designing a heartfelt card with her name, photo, and a loving quote.")

# Create assets directory if it doesn't exist
os.makedirs("assets", exist_ok=True)

# Sidebar for customization
st.sidebar.title("𝕄𝕆𝕋ℍ𝔼ℝ'𝕊 𝔻𝔸𝕐 🌸")

# Add image at the top of the sidebar
st.sidebar.image("assets/sidebar.png", use_container_width=True)

# Add song to sidebar (upload and play)
st.sidebar.subheader("💐 ᴍᴏᴛʜᴇʀ's ᴅᴀʏ sᴏɴɢ 🎶")
default_song = "assets/mothers_day_song.mp3"
st.sidebar.audio(default_song, start_time=0)

# Option to upload a custom song
song_file = st.sidebar.file_uploader("Or Upload Your Song (optional)", type=["mp3", "wav"])
if song_file:
    st.sidebar.audio(song_file)

# Background theme options
bg_choice = st.sidebar.selectbox("Choose Background Theme ✨", ["Pink Floral", "Golden Love", "Simple White"])

# Set background paths (using placeholder colors if images don't exist)
if bg_choice == "Pink Floral":
    bg_color = "#FFD1DC"  # Light pink
elif bg_choice == "Golden Love":
    bg_color = "#FFD700"  # Gold
else:
    bg_color = "#FFFFFF"  # White

# User inputs with placeholders
mom_name = st.text_input("🌟 Your Mother's Name", placeholder="Enter your mother's name")
quote = st.text_area("💗 Your Loving Message 💬", placeholder="Enter your loving message here...")

# Limit to 120 characters
if len(quote) > 120:
    st.warning("❗ Please limit your message to 120 characters.")
    quote = quote[:120]  # Trim the input

your_name = st.text_input("💮 Your's Name", placeholder="Enter your name")
image_file = st.file_uploader("📷 Upload a Picture of Your Mom (optional)", type=["png", "jpg", "jpeg"])

# Use a better font if available, otherwise use default
try:
    font_title = ImageFont.truetype("arial.ttf", 30)
    font_quote = ImageFont.truetype("arial.ttf", 20)
except:
    font_title = ImageFont.load_default()
    font_quote = ImageFont.load_default()

# Function to create the card
def create_card(mom_name, quote, mom_image, bg_color, your_name):
    # Create a blank image with the selected background color
    bg = Image.new("RGB", (800, 600), bg_color)
    draw = ImageDraw.Draw(bg)
    
    # Add decorative elements if no image background
    if bg_choice == "Simple White":
        # Draw some decorative elements
        draw.rectangle([50, 50, 750, 550], outline="pink", width=5)
        draw.ellipse([100, 100, 150, 150], fill="gold")
        draw.ellipse([650, 100, 700, 150], fill="gold")
    
    # Place user image if provided
    if mom_image:
        try:
            user_img = Image.open(mom_image).resize((200, 200))
            # Create circular mask for the image
            mask = Image.new('L', (200, 200), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, 200, 200), fill=255)
            bg.paste(user_img, (550, 50), mask)
        except Exception as e:
            st.warning(f"Couldn't process the image: {e}")

    # Text
    draw.text((50, 60), f"Dear {mom_name}: ", font=font_title, fill="black")
    draw.text((50, 120), "💗🌸 Happy Mother's Day! 🌟💖", font=font_title, fill="darkred")

    # Wrap quote
    lines = []
    words = quote.split(' ')
    line = ''
    for word in words:
        if len(line + word) < 40:
            line += word + ' '
        else:
            lines.append(line.strip())
            line = word + ' '
    lines.append(line.strip())

    y_text = 200
    for line in lines:
        draw.text((50, y_text), line, font=font_quote, fill="black")
        y_text += 30

    draw.text((220, y_text), f"💮😊 From {your_name}: ", font=font_quote, fill="black")
    
    return bg

# Generate button
if st.button("💗 Generate My Mother's Day Card 💮"):
    if mom_name and quote and your_name:
        final_card = create_card(mom_name, quote, image_file, bg_color, your_name)

        # Display animation
        st.balloons()

        # Two-column layout
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"💗🌸 Dear {mom_name}:")
            st.markdown("### 💌 Your Message: ")
            st.write(quote)
            st.write(f"💮😊 From {your_name}:")
        with col2:
            st.image(final_card, caption="💖 Your Personalized Card", use_container_width=True)

        # Download button
        buf = io.BytesIO()
        final_card.save(buf, format="PNG")
        byte_im = buf.getvalue()
        b64 = base64.b64encode(byte_im).decode()
        st.markdown(
            f'<a href="data:file/png;base64,{b64}" download="mothers_day_card.png">📥 Download Your Card</a>',
            unsafe_allow_html=True
        )
    else:
        st.warning("Please at least enter your mother's name, your name, and a message to generate your card.")
