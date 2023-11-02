import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("""
# Upwork Earnings Tracker 📊
""")

# Upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)

     # Filter the data by 'Fixed Price' and 'Hourly' in the 'type' column
    filtered_df = df[df['Type'].isin(['Fixed Price', 'Hourly'])]

    # Extract the month from the 'date' column and sum the 'amount' for each month
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    filtered_df['Month'] = filtered_df['Date'].dt.strftime('%b')
    monthly_summary = filtered_df.groupby('Month')['Amount'].sum().reset_index()

    # Create a custom sorting order for the 'Month' column
    month_order = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_summary['Month'] = pd.Categorical(monthly_summary['Month'], categories=month_order, ordered=True)
    monthly_summary = monthly_summary.sort_values('Month')

    # Display the uploaded data
    # st.write("Uploaded Data:")
    # st.write(df)
    
    st.markdown("---")

    # Display total 'Fixed Price' and 'Hourly' amounts
    st.write("#### Total Earning: ", f"<span style='color:green;'>${filtered_df['Amount'].sum():,}</span>", unsafe_allow_html=True)

    # Display sum of 'Fixed Price' and 'Hourly' amounts
    # st.write(" #### Sum of Fixed Price and Hourly")
    st.write(filtered_df.groupby('Type')['Amount'].sum())

    # Create a bar chart for the monthly summary
    st.write("#### Monthly Bar Chart")
    fig, ax = plt.subplots()
    bar_chart = ax.bar(monthly_summary['Month'], monthly_summary['Amount'])

    ax.set_xlabel('Month')
    ax.set_ylabel('Amount ($)')

    ax.bar_label(bar_chart, fmt='{:,.0f}')

    st.pyplot(fig)

    # Display the monthly summary
    st.write("#### Monthly Summary")
    st.write(monthly_summary)

st.markdown("---")
st.markdown("Made with ❤️ by [Zein](https://www.upwork.com/freelancers/zeini)")