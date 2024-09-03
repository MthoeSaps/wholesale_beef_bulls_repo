import streamlit as st
import qrcode
import io
from PIL import Image

# Streamlit app title and logo
logo_path = "qr_code_app/img/img8.jpg"  # Specify your logo file path here
try:
    logo = Image.open(logo_path)
    st.image(logo, width=280)
except Exception as e:
    st.error("Error loading logo. Please check the file path.")

st.title("Wholesale Beef Bulls T2 FunDay Team Registration")

# Initialize session state to hold the generated image
if 'combined_image' not in st.session_state:
    st.session_state.combined_image = None

# Input fields for personal data
team_name = st.text_input("Enter your team name (optional):")
email = st.text_input("Enter your email (optional):")
phone = st.text_input("Enter your phone number (optional):")
team_list = st.text_area("Enter team list (optional):")

# Backend image file path (modify this path as needed)
image_path = "qr_code_app/img/img8.png"  # Specify your image file path here

# Button to generate QR Code
if st.button("Generate QR Code"):
    # Check if at least one field is filled
    if team_name or email or phone or team_list:
        # Combine all inputs into a single string
        combined_data = ""
        if team_name:
            combined_data += f"Team Name: {team_name}\n"
        if email:
            combined_data += f"Email: {email}\n"
        if phone:
            combined_data += f"Phone: {phone}\n"
        if team_list:
            combined_data += f"Team List: {team_list}\n"
        
        # Add status to the QR code data
        combined_data += "Status: UNPAID ($10)"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(combined_data)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img_qr = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image to a BytesIO object
        buf_qr = io.BytesIO()
        img_qr.save(buf_qr, format='PNG')
        buf_qr.seek(0)

        # Display the image from the backend file path
        try:
            uploaded_image = Image.open(image_path)
        except Exception as e:
            st.error("Error loading image. Please check the file path.")
            uploaded_image = None

        # Create a new image to combine the QR code and uploaded image side by side
        if uploaded_image:
            # Resize images to match height
            img_qr = img_qr.resize((200, 200))
            uploaded_image = uploaded_image.resize((200, 200))

            # Create a new blank image with width for both images
            combined_width = img_qr.width + uploaded_image.width
            combined_height = max(img_qr.height, uploaded_image.height)

            combined_image = Image.new('RGB', (combined_width, combined_height))
            combined_image.paste(img_qr, (0, 0))
            combined_image.paste(uploaded_image, (img_qr.width, 0))

            # Save combined image to session state
            buf_combined = io.BytesIO()
            combined_image.save(buf_combined, format='PNG')
            buf_combined.seek(0)
            st.session_state.combined_image = buf_combined.getvalue()

            # Display the combined image
            st.image(combined_image, use_column_width=True)

            # Construct the file name using the team name
            combined_file_name = f"{team_name}_registration.png" if team_name else "registration.png"

            # Download link for the QR code
            if st.download_button(
                label="Download QR Code",
                data=st.session_state.combined_image,
                file_name=combined_file_name,
                mime="image/png"
            ):
                st.toast("Thank you for registering! Your QR code has been downloaded.")
        else:
            st.warning("Could not generate the combined image.")
    else:
        st.warning("Please fill in at least one field.")
