import datetime
import gspread
import streamlit as st
import toml
import smtplib
import datetime
from email.mime.text import MIMEText

secrets = toml.load("secrets.toml")

# Authenticate with Google Sheets API using the credentials
client = gspread.service_account_from_dict({
    "type": secrets["connections"]["gsheets"]["type"],
    "project_id": secrets["connections"]["gsheets"]["project_id"],
    "private_key_id": secrets["connections"]["gsheets"]["private_key_id"],
    "private_key": secrets["connections"]["gsheets"]["private_key"],
    "client_email": secrets["connections"]["gsheets"]["client_email"],
    "client_id": secrets["connections"]["gsheets"]["client_id"],
    "auth_uri": secrets["connections"]["gsheets"]["auth_uri"],
    "token_uri": secrets["connections"]["gsheets"]["token_uri"],
    "auth_provider_x509_cert_url": secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": secrets["connections"]["gsheets"]["client_x509_cert_url"]
})

# Open the Google Sheet
spreadsheet_key = secrets["connections"]["gsheets"]["spreadsheet"]
worksheet_index = int(secrets["connections"]["gsheets"]["worksheet"])
sheet = client.open_by_key(spreadsheet_key).get_worksheet(worksheet_index)

# post_url = "https://formsubmit.co/deeptigulati79@gmail.com"



st.image("studyshala.png")

st.title("Welcome to Studyshala!")
name = st.text_input("Student's name")
phone = st.text_input("Your Phone Number")

# Select class
selected_class = st.selectbox("Select your class", [None, "Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"])

# Dictionary containing subjects for each class
class_subjects = {
    "Class 1": ["All Subjects (English + Hindi + Maths + EVS)"],
    "Class 2": ["All Subjects (English + Hindi + Maths + EVS)"],
    "Class 3": ["All Subjects (English + Hindi + Maths + EVS)"],
    "Class 4": ["All Subjects (English + Hindi + Maths + EVS)"],
    "Class 5": ["All Subjects (English + Hindi + Maths + EVS)"],
    "Class 6": ["English", "Maths", "Science", "Social Science"],
    "Class 7": ["English", "Maths", "Science", "Social Science"],
    "Class 8": ["English", "Maths", "Science", "Social Science"],
    "Class 9": ["English", "Maths", "Science", "Social Science"],
    "Class 10": ["English", "Maths", "Science", "Social Science"],
    "Class 11": ["IP + Project work"],
    "Class 12": ["IP + Project work"],
}

# Render selectbox for subjects based on selected class
if selected_class:
    selected_subjects = st.multiselect("Select your subjects", class_subjects[selected_class])

    # Text area for optional message
message = st.text_area("Optional Message")

# Handle form submission
if st.button("Submit"):
    # Check if all required fields are filled
    if name.strip() and phone.strip() and len(phone.strip()) == 10 and selected_class and selected_subjects:
        phone_numbers = sheet.col_values(3)  # Assuming phone numbers are in the third column
        if phone in phone_numbers:
            st.error("This phone number already exists in the database.")
            st.stop()
        row_data = [str(datetime.datetime.now()), name, phone, selected_class, ", ".join(selected_subjects), message]
        sheet.append_row(row_data)

        try:
            body = f"Name: {name}\nPhone: {phone}\nClass: {selected_class}\nSubjects: {', '.join(selected_subjects)}\nMessage: {message}" 
            msg = MIMEText(body)
            msg['From'] = "studyshala79@gmail.com"
            msg['To'] = "deeptigulati79@gmail.com"
            msg['Subject'] = "Form submitted successfully!"

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("studyshala79@gmail.com", "enas kyza rypc ygpg" )
            server.sendmail("studyshala79@gmail.com", "deeptigulati79@gmail.com", msg.as_string())
            server.quit()
            st.success("Form submitted successfully!")
        except Exception as e:
            st.error(f"An error occurred")
        # else:
        #     st.error("Something went wrong. Please try again.")
    else:
        if len(phone.strip()) != 10:
            st.error("Please enter a 10-digit phone number.")
        else:
            st.error("Please fill in all the required fields.")


# Get the current year
current_year = datetime.datetime.now().year

# Footer
footer = f"""
<div style="text-align: center;">
    <hr>
    <p>© {current_year} Studyshala. All rights reserved.</p>
</div>
"""

# Render footer
st.markdown(footer, unsafe_allow_html=True)
