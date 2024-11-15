import streamlit as st
from PIL import Image
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import numpy as np
import io


# AES Cipher Class
class AESCipher:
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)

    def __pad(self, plain_text):
        padding_needed = self.block_size - len(plain_text) % self.block_size
        return plain_text + chr(padding_needed) * padding_needed

    @staticmethod
    def __unpad(plain_text):
        return plain_text[:-ord(plain_text[-1])]


# Helper Functions
def to_binary(data):
    if isinstance(data, str):
        return ''.join([format(ord(char), "08b") for char in data])
    elif isinstance(data, (bytes, np.ndarray)):
        return [format(byte, "08b") for byte in data]
    elif isinstance(data, (int, np.uint8)):
        return format(data, "08b")
    else:
        raise TypeError("Unsupported input type")


def encode_message(image, message, aes_cipher):
    img = image.convert("RGB")
    encrypted_message = aes_cipher.encrypt(message) + "$$$"
    message_bin = to_binary(encrypted_message)
    width, height = img.size
    idx = 0

    for x in range(width):
        for y in range(height):
            if idx >= len(message_bin):
                return img
            r, g, b = img.getpixel((x, y))
            r = int(to_binary(r)[:-1] + message_bin[idx], 2)
            g = int(to_binary(g)[:-1] + (message_bin[idx + 1] if idx + 1 < len(message_bin) else '0'), 2)
            b = int(to_binary(b)[:-1] + (message_bin[idx + 2] if idx + 2 < len(message_bin) else '0'), 2)
            img.putpixel((x, y), (r, g, b))
            idx += 3
    return img


def decode_message(image, aes_cipher):
    binary_data = ""
    width, height = image.size

    # Read pixel values
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            binary_data += to_binary(r)[-1] + to_binary(g)[-1] + to_binary(b)[-1]

            # Check for the presence of the end marker "$$$"
            if len(binary_data) >= 8 * 3:  # Ensure enough bits for initial decoding
                try:
                    all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
                    decoded_text = "".join([chr(int(byte, 2)) for byte in all_bytes])
                    end_marker = decoded_text.find("$$$")
                    if end_marker != -1:
                        decrypted_message = aes_cipher.decrypt(decoded_text[:end_marker])
                        return decrypted_message
                except Exception:
                    continue

    # If we exit the loop without finding the end marker
    raise ValueError("Decoding failed: No valid message or incorrect decryption key.")



def encode_image(cover_image, secret_image):
    cover_img = cover_image.convert("RGB")
    secret_img = secret_image.resize(cover_img.size).convert("RGB")

    cover_pixels = np.array(cover_img)
    secret_pixels = np.array(secret_img) // 16  # Use 4 LSB for encoding

    encoded_pixels = (cover_pixels & 240) | secret_pixels
    encoded_img = Image.fromarray(encoded_pixels.astype("uint8"), "RGB")
    return encoded_img


def decode_image(encoded_image, secret_size):
    encoded_img = np.array(encoded_image)
    secret_pixels = (encoded_img & 15) * 16
    secret_img = Image.fromarray(secret_pixels.astype("uint8"), "RGB")
    return secret_img.resize(secret_size)


# Main Streamlit App
def main():
    # Set page config for a colorful and attractive app
    st.set_page_config(page_title="Advanced Image Steganography", layout="centered")
    
    # Inject custom CSS
    st.markdown("""
        <style>
        body {
            background-color: #f7f7f7;
            font-family: 'Arial', sans-serif;
            color: #333;
        }
        .css-1d391kg {
            background: linear-gradient(to right, #ff7e5f, #feb47b);
        }
        .stButton>button {
            background-color: #ff6347;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: white;
        }
        .stTextInput>div>input {
            background-color: #fafafa;
            border-radius: 8px;
            padding: 10px;
        }
        .stTextArea>div>textarea {
            background-color: #fafafa;
            border-radius: 8px;
            padding: 10px;
        }
        h1, h2 {
            color: #ff6347;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title and Header
    st.title("🔐 Data Protection with Image Steganography 🖼️")
    st.subheader("Store your personal data securely inside images. Keep your data hidden and safe!")

    action = st.radio("🎯 Choose Action:", ("Encode", "Decode"))

    if action == "Encode":
        encode_choice = st.radio("💬 Choose Encoding Type:", ("Message", "Image"))
        uploaded_file = st.file_uploader("Upload Cover Image 📷", type=["png", "jpg", "jpeg"])

        if encode_choice == "Message":
            message = st.text_area("Enter the Message to Hide 📝")
            key = st.text_input("Enter Encryption Key 🔑")
            if st.button("Encode 📩"):
                if uploaded_file and message and key:
                    image = Image.open(uploaded_file)
                    aes_cipher = AESCipher(key)
                    encoded_img = encode_message(image, message, aes_cipher)
                    buffer = io.BytesIO()
                    encoded_img.save(buffer, format="PNG")
                    st.download_button("Download Encoded Image 📥", buffer.getvalue(), "encoded_image.png", "image/png")
                else:
                    st.error("🚨 Please upload an image, enter a message, and provide a key.")

        elif encode_choice == "Image":
            secret_file = st.file_uploader("Upload Secret Image 🖼️", type=["png", "jpg", "jpeg"])
            if st.button("Encode 📩"):
                if uploaded_file and secret_file:
                    cover_image = Image.open(uploaded_file)
                    secret_image = Image.open(secret_file)
                    encoded_img = encode_image(cover_image, secret_image)
                    buffer = io.BytesIO()
                    encoded_img.save(buffer, format="PNG")
                    st.download_button("Download Encoded Image 📥", buffer.getvalue(), "encoded_image.png", "image/png")
                else:
                    st.error("🚨 Please upload both cover and secret images.")

    elif action == "Decode":
        decode_choice = st.radio("🔍 Choose Decoding Type:", ("Message", "Image"))
        uploaded_file = st.file_uploader("Upload Encoded Image 📷", type=["png", "jpg", "jpeg"])

        if decode_choice == "Message":
            key = st.text_input("Enter Encryption Key 🔑")
            if st.button("Decode 🕵️‍♂️"):
                if uploaded_file and key:
                    image = Image.open(uploaded_file)
                    aes_cipher = AESCipher(key)
                    try:
                        decoded_message = decode_message(image, aes_cipher)
                        st.text_area("Decoded Message 📜:", decoded_message)
                    except ValueError:
                        st.error("🚨 Failed to decode the message.")
                else:
                    st.error("🚨 Please upload an encoded image and provide a key.")

        elif decode_choice == "Image":
            secret_size = st.slider("🔄 Resize Decoded Image", 50, 500, 200)
            if st.button("Decode 🕵️‍♂️"):
                if uploaded_file:
                    encoded_image = Image.open(uploaded_file)
                    decoded_img = decode_image(encoded_image, (secret_size, secret_size))
                    st.image(decoded_img, caption="Decoded Secret Image 🖼️")
                    buffer = io.BytesIO()
                    decoded_img.save(buffer, format="PNG")
                    st.download_button("Download Decoded Secret Image 📥", buffer.getvalue(), "decoded_secret_image.png", "image/png")
                else:
                    st.error("🚨 Please upload an encoded image.")



if __name__ == "__main__":
    main()
