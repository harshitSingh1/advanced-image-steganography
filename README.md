# Advanced Image Steganography with Encryption

## Overview

This project aims to reduce cybercrime and data theft by providing a secure way to store sensitive information inside non-harmful images. In today's digital age, hackers often collect small pieces of information from social media accounts to build a profile of the user and access sensitive data. These attacks can cause significant financial and personal damage. 

In addition to social media information, people often store sensitive documents like Aadhaar cards, PAN cards, bank account details, and other essential files on their phones and laptops. These files are vulnerable to malware and phishing attacks. This project uses the technique of **steganography** to hide sensitive data within innocent images, making it difficult for hackers to steal them.

The key feature of this project is the combination of steganography with **encryption**. While traditional steganography has been used to hide messages or data in images, this project adds an extra layer of security by encrypting the data before embedding it. This ensures that even if the data is exposed, it cannot be easily accessed without the correct decryption key.

## Features

- **Message Encoding**: Users can hide any text message securely inside an image. The message is encrypted before being embedded in the image.
- **Image Encoding**: Users can hide one image inside another. This feature is helpful for protecting sensitive images or documents.
- **Decoding**: Users can retrieve hidden messages or images from an encoded image. The data is decrypted during the decoding process, ensuring privacy.
- **Encryption**: AES encryption is used to secure the message before hiding it. The user provides an encryption key, ensuring only authorized users can decode the data.
- **Easy to Use**: The project provides a simple interface for uploading images, entering messages, and retrieving hidden data.

## Technologies Used

- **Python**: The core logic of the project is implemented in Python.
- **Streamlit**: For creating a user-friendly web interface.
- **AES Encryption**: Advanced encryption standard (AES) is used to encrypt the data before embedding it in the image.
- **PIL (Pillow)**: For image manipulation.
- **OpenCV**: Used for handling images and ensuring proper encoding and decoding processes.

## How It Works

### 1. Encoding Process
- **Message Encoding**: 
    - The user uploads a cover image (any image of their choice).
    - The message to be hidden is entered by the user.
    - The encryption key is provided, and the message is encrypted using AES encryption.
    - The encrypted message is converted into binary and embedded into the image.
    - The final encoded image is ready for download.

- **Image Encoding**:
    - The user uploads a cover image (large image) and a secret image (the one to hide).
    - The secret image is resized to match the cover image size.
    - The least significant bits of the cover image are replaced with the secret image.
    - The final encoded image is ready for download.

### 2. Decoding Process
- **Message Decoding**:
    - The user uploads the encoded image.
    - The encryption key is provided.
    - The hidden message is decoded and decrypted using the provided key.

- **Image Decoding**:
    - The user uploads the encoded image.
    - The secret image is extracted and resized to the original dimensions.
    - The decoded image is ready for download.

## Getting Started

### Prerequisites

- **Python 3.6+**: Make sure Python is installed on your machine.
- **Required Python Libraries**: Install the required libraries using the following command:

### Running the Application

```bash

git clone https://github.com/yourusername/advanced-image-steganography.git
cd advanced-image-steganography
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

```
### Contributing
If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. Please make sure to follow the coding guidelines and include tests for any new features or bug fixes.

#### License
This project is licensed under the MIT License - see the LICENSE file for details.

