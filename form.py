import datetime
import gspread
import streamlit as st
import toml
import smtplib
import datetime
from email.mime.text import MIMEText
import streamlit.components.v1 as components

st.image("studyshala.png")

st.title("Welcome to Studyshala!")
name = st.text_input("Student's name")
phone = st.text_input("Your Phone Number")

class_options = [None, "Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"]
selected_class = st.selectbox("Select your class", class_options)

    
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

if selected_class in ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5"]:
    selected_subjects = st.multiselect("Select your subjects", class_subjects[selected_class], default=["All Subjects (English + Hindi + Maths + EVS)"])
elif selected_class:
    selected_subjects = st.multiselect("Select your subjects", class_subjects[selected_class])

    # Text area for optional message
message = st.text_area("Optional Message")

# Handle form submission
if st.button("Submit"):
    with st.spinner("Submitting..."):
    # Check if all required fields are filled
        if name.strip() and phone.strip() and len(phone.strip()) == 10 and selected_class and selected_subjects:
            try:
                client = gspread.service_account_from_dict({
                "type": st.secrets["connections"]["gsheets"]["type"],
                "project_id": st.secrets["connections"]["gsheets"]["project_id"],
                "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
                "private_key": st.secrets["connections"]["gsheets"]["private_key"],
                "client_email": st.secrets["connections"]["gsheets"]["client_email"],
                "client_id": st.secrets["connections"]["gsheets"]["client_id"],
                "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
                "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"]
                })
                spreadsheet_key = st.secrets["connections"]["gsheets"]["spreadsheet"]
                worksheet_index = int(st.secrets["connections"]["gsheets"]["worksheet"])
                sheet = client.open_by_key(spreadsheet_key).get_worksheet(worksheet_index)
            except Exception as e:
                st.error(f"An error occurred: {e}")
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
        else:
            if len(phone.strip()) != 10 or not phone.isdigit():
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

home = """<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1749.7819055980215!2d77.13587193865565!3d28.70269189390665!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390d03d758d01921%3A0x73ffd1a27ff23462!2sGD-193%2C%20GD%20Block%2C%20Dakshini%20Pitampura%2C%20Pitampura%2C%20Delhi%2C%20110034!5e0!3m2!1sen!2sin!4v1710650733053!5m2!1sen!2sin" width="400" height="300" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""

# Render footer
st.subheader("Our Location")
st.markdown(home, unsafe_allow_html=True)
st.markdown(footer, unsafe_allow_html=True)
