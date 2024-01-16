import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
import base64
from reportlab.platypus import Image

# Function to create or load the database
def initialize_database():
    try:
        db = pd.read_csv('blood_pressure_data.csv', parse_dates=['Timestamp'])
    except FileNotFoundError:
        db = pd.DataFrame(columns=['Timestamp', 'Systolic_BP', 'Diastolic_BP'])
        db.to_csv('blood_pressure_data.csv', index=False)
    return db


def plot_trends(data, start_date, end_date, chart_type):
    filtered_data = data[(data['Timestamp'] >= pd.to_datetime(start_date)) & (data['Timestamp'] <= pd.to_datetime(end_date) + pd.Timedelta(days=1))]
    
    # Sort the DataFrame by 'Timestamp'
    filtered_data = filtered_data.sort_values(by='Timestamp')
    
    st.dataframe(filtered_data)
    
    fig = px.line(filtered_data, x='Timestamp', y=['Systolic_BP', 'Diastolic_BP'], title='Blood Pressure Trends Over Time')
    st.plotly_chart(fig)

# Function to plot average blood pressure values per day
def plot_average_values(data, start_date, end_date, chart_type):
    st.dataframe(data)
    aggregated_data = data.groupby(data['Timestamp'].dt.date).mean().reset_index()
    st.dataframe(aggregated_data)
    filtered_data = aggregated_data[(aggregated_data['Timestamp'] >= pd.to_datetime(start_date)) & (aggregated_data['Timestamp'] <= pd.to_datetime(end_date) + pd.Timedelta(days=1))]
    if chart_type == "Line":
        fig = px.line(filtered_data, x='Timestamp', y=['Systolic_BP', 'Diastolic_BP'], title='Average Blood Pressure Values Per Day')
    elif chart_type == "Bar":
        fig = px.bar(filtered_data, x='Timestamp', y=['Systolic_BP', 'Diastolic_BP'], title='Average Blood Pressure Values Per Day', barmode='overlay', opacity=0.9)
    st.plotly_chart(fig)

# Function to plot maximum blood pressure values per day
def plot_maximum_values(data, start_date, end_date, chart_type):
    st.dataframe(data)  
    aggregated_data = data.groupby(data['Timestamp'].dt.date).max().reset_index(drop=True)
    st.dataframe(aggregated_data)
    filtered_data = aggregated_data[(aggregated_data['Timestamp'] >= pd.to_datetime(start_date)) & (aggregated_data['Timestamp'] <= pd.to_datetime(end_date) + pd.Timedelta(days=1))]
    if chart_type == "Line":
        fig = px.line(filtered_data, x='Timestamp', y=['Systolic_BP', 'Diastolic_BP'], title='Maximum Blood Pressure Values Per Day')
    elif chart_type == "Bar":
        fig = px.bar(filtered_data, x='Timestamp', y=['Systolic_BP', 'Diastolic_BP'], title='Maximum Blood Pressure Values Per Day', barmode='overlay', opacity=0.9)
    st.plotly_chart(fig)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf_report(data, start_date, end_date, chart_type):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Add content to the PDF
    content = []

    # Styles
    styles = getSampleStyleSheet()
    style_normal = styles["BodyText"]
    style_heading = styles["Heading1"]
    style_heading3 = styles["Heading3"]

    # Header
    header_text = "<u>Blood Pressure Monitoring Report</u>"
    content.append(Paragraph(header_text, style_heading))
    content.append(Paragraph("<br/>", style_normal))

    # Additional Text
    additional_text = "Patient Name: Arvind Vyankatrao Deshmukh"
    content.append(Paragraph(additional_text, style_normal))
    content.append(Paragraph("<br/>", style_normal))

    # Date Range
    date_range_text = f"Report for {start_date} to {end_date}"
    content.append(Paragraph(date_range_text, style_normal))
    content.append(Paragraph("<br/>", style_normal))

    # Header
    header_text = "<u>Blood Pressure Values Tablet</u>"
    content.append(Paragraph(header_text, style_heading3))
    content.append(Paragraph("<br/>", style_normal))

    # Blood Pressure Values Table
    blood_pressure_table = data[(data['Timestamp'] >= pd.to_datetime(start_date)) & (data['Timestamp'] <= pd.to_datetime(end_date) + pd.Timedelta(days=1))]
    table_data = [['Timestamp', 'Systolic_BP', 'Diastolic_BP']] + blood_pressure_table[['Timestamp', 'Systolic_BP', 'Diastolic_BP']].astype(str).values.tolist()
    table_style = TableStyle(
        [('BACKGROUND', (0, 0), (-1, 0), colors.grey),
         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
         ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
         ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table = Table(table_data, colWidths=[150, 150, 150], rowHeights=20, style=table_style)
    content.append(table)

    content.append(Paragraph("<br/>", style_normal))

    # Blood Pressure Trends Graph
    blood_pressure_trends_data = data[(data['Timestamp'] >= pd.to_datetime(start_date)) & (data['Timestamp'] <= pd.to_datetime(end_date) + pd.Timedelta(days=1))]
    # Sort the DataFrame by 'Timestamp'
    blood_pressure_trends_data = blood_pressure_trends_data.sort_values(by='Timestamp')
    fig_trends = px.line(blood_pressure_trends_data, x='Timestamp', y=['Systolic_BP', 'Diastolic_BP'], title='Blood Pressure Trends Over Time')
    img_data_trends = BytesIO()
    fig_trends.write_image(img_data_trends, format='png')
    img_data_trends.seek(0)
    img_data_trends = Image(img_data_trends, width=480, height=300)

    # Check if there is enough space on the current page for the image
    remaining_space = doc.pagesize[1] - doc.bottomMargin - sum(c.getSpaceBefore() + c.getSpaceAfter() for c in content)
    
    if remaining_space < img_data_trends._height:
        # If the image doesn't fit, add a page break
        content.append(PageBreak())
    
    content.append(img_data_trends)

    # Header
    header_text = "<u>Mean Aggregated Blood Pressure Values Tablet</u>"
    content.append(Paragraph(header_text, style_heading3))
    content.append(Paragraph("<br/>", style_normal))


    # Aggregated Blood Pressure Values Table
    aggregated_data_mean = data.groupby(data['Timestamp'].dt.date).mean().reset_index()
    aggregated_table_data_mean = [['Date', 'Average Systolic_BP', 'Average Diastolic_BP']] + aggregated_data_mean[['Timestamp', 'Systolic_BP', 'Diastolic_BP']].astype(str).values.tolist()
    table_style_mean = TableStyle(
        [('BACKGROUND', (0, 0), (-1, 0), colors.grey),
         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
         ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
         ('GRID', (0, 0), (-1, -1), 1, colors.grey)])
    table_mean = Table(aggregated_table_data_mean, colWidths=[150, 150, 150], rowHeights=20, style=table_style_mean)
    content.append(table_mean)

    content.append(Paragraph("<br/>", style_normal))

    # Visualization for Average Blood Pressure
    fig_line_mean = px.line(aggregated_data_mean, x='Timestamp', y=['Systolic_BP', 'Diastolic_BP'], title='Average Blood Pressure Values Per Day')
    img_data_line_mean = BytesIO()
    fig_line_mean.write_image(img_data_line_mean, format='png')
    img_data_line_mean.seek(0)
    img_data_line_mean = Image(img_data_line_mean, width=480, height=300)
    content.append(img_data_line_mean)

    fig_bar_mean = px.bar(aggregated_data_mean, x='Timestamp', y=['Systolic_BP', 'Diastolic_BP'], title='Average Blood Pressure Values Per Day', barmode='overlay', opacity=0.9)
    img_data_bar_mean = BytesIO()
    fig_bar_mean.write_image(img_data_bar_mean, format='png')
    img_data_bar_mean.seek(0)
    img_data_bar_mean = Image(img_data_bar_mean, width=480, height=300)
    content.append(img_data_bar_mean)

    # Header
    header_text = "<u>Max Aggregated Blood Pressure Values Tablet</u>"
    content.append(Paragraph(header_text, style_heading3))
    content.append(Paragraph("<br/>", style_normal))

    # Aggregated Maximum Blood Pressure Values Table
    aggregated_data_max = data.groupby(data['Timestamp'].dt.date).max().reset_index(drop=True)
    aggregated_table_data_max = [['Date', 'Maximum Systolic_BP', 'Maximum Diastolic_BP']] + aggregated_data_max[['Timestamp', 'Systolic_BP', 'Diastolic_BP']].astype(str).values.tolist()
    table_style_max = TableStyle(
        [('BACKGROUND', (0, 0), (-1, 0), colors.grey),
         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
         ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
         ('GRID', (0, 0), (-1, -1), 1, colors.grey)])
    table_max = Table(aggregated_table_data_max, colWidths=[150, 150, 150], rowHeights=20, style=table_style_max)
    content.append(table_max)

    content.append(Paragraph("<br/>", style_normal))

    # Visualization for Maximum Blood Pressure
    fig_line_max = px.line(aggregated_data_max, x='Timestamp', y=['Systolic_BP', 'Diastolic_BP'], title='Maximum Blood Pressure Values Per Day')
    img_data_line_max = BytesIO()
    fig_line_max.write_image(img_data_line_max, format='png')
    img_data_line_max.seek(0)
    img_data_line_max = Image(img_data_line_max, width=480, height=300)
    content.append(img_data_line_max)

    fig_bar_max = px.bar(aggregated_data_max, x='Timestamp', y=['Systolic_BP', 'Diastolic_BP'], title='Maximum Blood Pressure Values Per Day', barmode='overlay', opacity=0.9)
    img_data_bar_max = BytesIO()
    fig_bar_max.write_image(img_data_bar_max, format='png')
    img_data_bar_max.seek(0)
    img_data_bar_max = Image(img_data_bar_max, width=480, height=300)
    content.append(img_data_bar_max)

    # Header
    content.append(PageBreak()) 
    header_text = "<u>Cosolidating Vidualisations</u>"
    content.append(Paragraph(header_text, style_heading))
    content.append(Paragraph("<br/>", style_normal))
    # Header
    header_text = "<u>Blood Pressure Values Tablet</u>"
    content.append(Paragraph(header_text, style_heading3))
    content.append(Paragraph("<br/>", style_normal))
    content.append(img_data_trends)

    # Header
    content.append(PageBreak()) 
    header_text = "<u>Mean Aggregated Blood Pressure Values Tablet</u>"
    content.append(Paragraph(header_text, style_heading3))
    content.append(Paragraph("<br/>", style_normal))
    content.append(img_data_line_mean)
    content.append(img_data_bar_mean)

    # Header
    content.append(PageBreak()) 
    header_text = "<u>Max Aggregated Blood Pressure Values Tablet</u>"
    content.append(Paragraph(header_text, style_heading3))
    content.append(Paragraph("<br/>", style_normal))       
    content.append(img_data_line_max)
    content.append(img_data_bar_max)

    # Save the PDF
    doc.build(content)
    pdf_buffer.seek(0)

    # Download the PDF
    st.markdown("### Download PDF Report")
    st.markdown("Click the link below to download the complete report in PDF format.")
    st.markdown(get_binary_file_downloader_html(pdf_buffer, 'Blood_Pressure_Report'), unsafe_allow_html=True)



def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file.getvalue()).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}.pdf" target="_blank">{file_label}</a>'
    return href

# # Function to input new blood pressure data
# def input_blood_pressure(db):
#     default_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
#     timestamp_input = st.text_input("Enter Timestamp (YYYY-MM-DD HH:MM, or leave empty for current time):", default_timestamp)
    
#     if timestamp_input.strip() == '':
#         timestamp_input = datetime.now().strftime('%Y-%m-%d %H:%M')
#     else:
#         timestamp_input = pd.to_datetime(timestamp_input)  # Convert to datetime format
    
#     systolic_bp = st.number_input("Enter Systolic Blood Pressure:", min_value=0)
#     diastolic_bp = st.number_input("Enter Diastolic Blood Pressure:", min_value=0)

#     if st.button("Submit"):
#         new_data = pd.DataFrame([[timestamp_input, systolic_bp, diastolic_bp]], columns=['Timestamp', 'Systolic_BP', 'Diastolic_BP'])
#         db = pd.concat([db, new_data], ignore_index=True)
#         db.to_csv('blood_pressure_data.csv', index=False)
#         st.success("Data submitted successfully!")

from datetime import datetime

def input_blood_pressure(db):
    default_timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')  # Format with AM/PM
    timestamp_input = st.text_input("Enter Timestamp (YYYY-MM-DD HH:MM AM/PM, or leave empty for current time):", default_timestamp)

    if timestamp_input.strip() == '':
        timestamp_input = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    else:
        try:
            # Try to parse the input in both 24-hour and AM/PM formats
            timestamp_input = datetime.strptime(timestamp_input, '%Y-%m-%d %H:%M')
        except ValueError:
            try:
                timestamp_input = datetime.strptime(timestamp_input, '%Y-%m-%d %I:%M %p')
            except ValueError:
                st.error("Invalid timestamp format. Please use either 'YYYY-MM-DD HH:MM' or 'YYYY-MM-DD HH:MM AM/PM'")
                return

    systolic_bp = st.number_input("Enter Systolic Blood Pressure:", min_value=0)
    diastolic_bp = st.number_input("Enter Diastolic Blood Pressure:", min_value=0)

    if st.button("Submit"):
        new_data = pd.DataFrame([[timestamp_input, systolic_bp, diastolic_bp]], columns=['Timestamp', 'Systolic_BP', 'Diastolic_BP'])
        db = pd.concat([db, new_data], ignore_index=True)
        db.to_csv('blood_pressure_data.csv', index=False)
        st.success("Data submitted successfully!")

# Function to input historical data manually
def input_historical_data(db):
    uploaded_file = st.file_uploader("Upload a CSV file with historical data", type=["csv"])
    if uploaded_file is not None:
        historical_data = pd.read_csv(uploaded_file, parse_dates=['Timestamp'])
        db = pd.concat([db, historical_data], ignore_index=True)
        db.to_csv('blood_pressure_data.csv', index=False)
        st.success("Historical data added successfully!")

def main():
    st.title("Blood Pressure Monitoring App")

    db = initialize_database()

    # Sidebar
    st.sidebar.header("Menu")
    menu = st.sidebar.radio("Select an option", ["Input Blood Pressure", "Input Historical Data", "Generate Reports", "Average Values Report", "Maximum Values Report"])

    if menu == "Input Blood Pressure":
        input_blood_pressure(db)
    elif menu == "Input Historical Data":
        input_historical_data(db)
    elif menu == "Generate Reports":
        start_date = st.date_input("Select start date", value=min(db['Timestamp']),  min_value=min(db['Timestamp']), max_value=max(db['Timestamp'])).strftime('%Y-%m-%d')
        end_date = st.date_input("Select end date", value=max(db['Timestamp']), min_value=min(db['Timestamp']), max_value=max(db['Timestamp'])).strftime('%Y-%m-%d')
        chart_type = None
        if start_date > end_date:
            st.error("End date must be greater than or equal to start date.")
        else:
            if st.button("Generate PDF Report"):
                create_pdf_report(db, start_date, end_date, chart_type)
            plot_trends(db, start_date, end_date, chart_type)
    elif menu == "Average Values Report":
        start_date = st.date_input("Select start date", value=min(db['Timestamp']),  min_value=min(db['Timestamp']), max_value=max(db['Timestamp'])).strftime('%Y-%m-%d')
        end_date = st.date_input("Select end date", value=max(db['Timestamp']), min_value=min(db['Timestamp']), max_value=max(db['Timestamp'])).strftime('%Y-%m-%d')
        chart_type = st.selectbox("Select Chart Type", ["Line", "Bar"])
        
        if start_date > end_date:
            st.error("End date must be greater than or equal to start date.")
        else:
            if st.button("Generate PDF Report"):
                create_pdf_report(db, start_date, end_date, chart_type)
            plot_average_values(db, start_date, end_date, chart_type)
    elif menu == "Maximum Values Report":
        start_date = st.date_input("Select start date", value=min(db['Timestamp']),  min_value=min(db['Timestamp']), max_value=max(db['Timestamp'])).strftime('%Y-%m-%d')
        end_date = st.date_input("Select end date", value=max(db['Timestamp']), min_value=min(db['Timestamp']), max_value=max(db['Timestamp'])).strftime('%Y-%m-%d')
        chart_type = st.selectbox("Select Chart Type", ["Line", "Bar"])
        
        if start_date > end_date:
            st.error("End date must be greater than or equal to start date.")
        else:
            if st.button("Generate PDF Report"):
                create_pdf_report(db, start_date, end_date, chart_type)
            plot_maximum_values(db, start_date, end_date, chart_type)

if __name__ == '__main__':
    main()
