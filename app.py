# Import necessary libraries
import streamlit as st
import pdfplumber
import openai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Set OpenAI API Key
openai.api_key = os.getenv("***REMOVED***")

# Function to Extract Data from PDF
def extract_data_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to Generate Credit Analysis using the Updated OpenAI Chat API
def generate_credit_analysis(extracted_data):
    messages = [
        {"role": "system", "content": "You are a financial analyst that provides summaries of credit data."},
        {"role": "user", "content": f"Analyze the following credit data and provide a summary:\n\n{extracted_data}"}
    ]
    response = openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )
    return response.choices[0].message['content'].strip()

# Function to Generate PDF Report
def create_pdf_report(analysis_text, output_path="credit_analysis_report.pdf"):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.drawString(100, 750, "Credit Analysis Report")
    c.drawString(100, 725, "Generated Analysis:")
    text_object = c.beginText(100, 700)
    text_object.setLeading(14)
    text_object.textLines(analysis_text)
    c.drawText(text_object)
    c.save()
    return output_path

# Streamlit App Interface
st.title("Credit Report Analysis Tool")
uploaded_file = st.file_uploader("Upload Credit Report (PDF)", type="pdf")

if uploaded_file is not None:
    # Ensure the temp directory exists
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save uploaded file to the temp directory
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract data from the uploaded PDF
    extracted_text = extract_data_from_pdf(temp_file_path)
    
    # Generate credit analysis
    analysis = generate_credit_analysis(extracted_text)
    
    # Create and save PDF report
    report_path = create_pdf_report(analysis)
    
    # Provide download link for the generated report
    with open(report_path, "rb") as f:
        st.download_button(
            label="Download Credit Analysis Report",
            data=f,
            file_name="credit_analysis_report.pdf",
            mime="application/pdf"
        )
