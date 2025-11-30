import qrcode

# Data for the QR code
url = "https://neverloseajob.com"

# Create QR code instance
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

# Add data
qr.add_data(url)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
img.save("FounderCard_URL_QR.png")
print(f"QR code generated for {url} and saved as FounderCard_URL_QR.png")
