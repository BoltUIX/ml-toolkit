import streamlit as st
import pandas as pd
import plotly.express as px

# Function to display data with pagination and search option
def display_data_with_pagination(df, page_size=10):
    search_query = st.text_input("Search", "")
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    
    page_number = st.number_input("Page number", min_value=1, max_value=(len(df) // page_size) + 1, step=1)
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    st.dataframe(df.iloc[start_idx:end_idx])

# Function to generate a pie chart of unique vs duplicate records
def generate_pie_chart(df):
    total_records = len(df)
    unique_records = len(df.drop_duplicates())
    duplicate_records = total_records - unique_records
    data = pd.DataFrame({
        "Record Type": ["Unique", "Duplicate"],
        "Count": [unique_records, duplicate_records]
    })
    fig = px.pie(data, values="Count", names="Record Type", title="Unique vs Duplicate Records")
    fig.update_traces(marker=dict(colors=['red', 'lightcoral']))  # Updated to red color scheme
    return fig, unique_records, duplicate_records, total_records

# Function to download cleaned CSV
def download_clean_data(df, convert_lowercase=False):
    if convert_lowercase:
        df = df.applymap(lambda s: s.lower() if type(s) == str else s)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"Download cleaned CSV",
        data=csv,
        file_name='cleaned_data.csv',
        mime='text/csv',
    )

# Function to display column shapes as a bar chart
def display_column_shapes(df):
    column_shapes = pd.DataFrame({
        "Column": df.columns,
        "Records": [df[col].shape[0] for col in df.columns]
    })
    fig = px.bar(column_shapes, x="Column", y="Records", title="Shape of Each Column", color='Records', labels={'Records': 'Count'})
    fig.update_traces(marker_color='red')  # Setting chart color to red
    st.plotly_chart(fig)

# Additional User Features
def display_data_summary(df):
    st.subheader("Data Summary")
    st.write(df.describe())

# Merge multiple CSV files
def merge_data_files(uploaded_files):
    dfs = []
    for file in uploaded_files:
        file_extension = file.name.split('.')[-1].lower()
        if file_extension == 'csv':
            dfs.append(pd.read_csv(file))
    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df

# Streamlit app
st.markdown('<h1 style="color:red;">ML Data Preprocessing</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:gray;">You can upload multiple CSV files, remove duplicates, and get a summary report. After that, you can download a cleaned CSV file, perfect for your model.</p>', unsafe_allow_html=True)
st.markdown('<hr style="border-top: 2px solid red;">', unsafe_allow_html=True)


st.markdown('<h2 style="color:red;">Step 1: Upload your data file</h2>', unsafe_allow_html=True)

uploaded_files = st.file_uploader("", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 1:
        df = merge_data_files(uploaded_files)
        st.write("Multiple files uploaded and merged.")
    else:
        file = uploaded_files[0]
        df = pd.read_csv(file)

    st.markdown('<hr style="border-top: 2px solid red;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:red;">Step 2: Paginated Table View</h2>', unsafe_allow_html=True)
    st.markdown('<div style="background-color:lightcoral;padding:10px;">', unsafe_allow_html=True)
    display_data_with_pagination(df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    fig, unique_count, duplicate_count, total_count = generate_pie_chart(df)
    
    st.markdown('<hr style="border-top: 2px solid red;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:red;">Step 3: Unique and Duplicate Records Pie Chart</h2>', unsafe_allow_html=True)
    st.plotly_chart(fig)
    
    st.markdown('<hr style="border-top: 2px solid red;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:red;">Step 4: Detailed Report</h2>', unsafe_allow_html=True)
    st.write(f"**Total Records:** {total_count}")
    st.write(f"**Duplicate Records:** {duplicate_count}")
    st.write(f"**Unique Records:** {unique_count}")
    
    st.markdown('<hr style="border-top: 2px solid red;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:red;">Step 5: Shape of Each Column</h2>', unsafe_allow_html=True)
    display_column_shapes(df)

    display_data_summary(df)

    st.markdown('<hr style="border-top: 2px solid red;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:red;">Step 6: Download Cleaned Data</h2>', unsafe_allow_html=True)
    convert_lowercase = st.checkbox("Convert all text to lowercase", key="lowercase_checkbox")
    
    if st.button("Download cleaned data", key="download_button"):
        download_clean_data(df, convert_lowercase=convert_lowercase)



# Add footer
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: red; /* Changed background color to red */
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        Design & Developed by boltuix | Ver 1.0.0
    </div>
    """, unsafe_allow_html=True)
