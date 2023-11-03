import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Upwork Earnings Tracker", page_icon=":bar_chart:")

st.write("""
# Upwork Earnings Tracker 📊
""")

# Upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the uploaded data
    # st.write("Uploaded Data:")
    # st.write(df)

    # Filter the data by 'Fixed Price' and 'Hourly' in the 'type' column
    filtered_df = df[df['Type'].isin(['Fixed Price', 'Hourly'])]
    filtered_df_fee = df[df['Type'].isin(['Service Fee'])]

    # Extract the month from the 'date' column and sum the 'amount' for each month
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    filtered_df['Month'] = filtered_df['Date'].dt.strftime('%b')
    monthly_summary = filtered_df.groupby('Month')['Amount'].sum().reset_index()

    filtered_df_fee['Date'] = pd.to_datetime(filtered_df_fee['Date'])
    filtered_df_fee['Month'] = filtered_df_fee['Date'].dt.strftime('%b')
    monthly_summary_fee = filtered_df_fee.groupby('Month')['Amount'].sum().reset_index()

    # Create a custom sorting order for the 'Month' column
    month_order = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_summary['Month'] = pd.Categorical(monthly_summary['Month'], categories=month_order, ordered=True)
    monthly_summary = monthly_summary.sort_values('Month')

    monthly_summary_fee['Month'] = pd.Categorical(monthly_summary_fee['Month'], categories=month_order, ordered=True)
    monthly_summary_fee = monthly_summary_fee.sort_values('Month')
    
    st.markdown("---")

    # Display total 'Fixed Price' and 'Hourly' amounts
    # st.write("##### Total Earning: ", f"<span style='color:green;'>$ {filtered_df['Amount'].sum():,}</span>", unsafe_allow_html=True)
    # st.write("##### Charity (2.5%): ", f"<span style='color:red;'>$ {filtered_df['Amount'].sum() * 2.5 / 100:,}</span>", unsafe_allow_html=True)

    # # Display sum of 'Fixed Price' and 'Hourly' amounts
    # # st.write(" #### Sum of Fixed Price and Hourly")
    # st.write(filtered_df.groupby('Type')['Amount'].sum())

    # Add a radio button to select between "Included fee" and "Without fee" calculations
    fee_option = st.radio("Choose fee option", ["Without fee", "Included fee"])

    if fee_option == "Without fee":
        # Display total 'Fixed Price' and 'Hourly' amounts with service fee
        st.write("##### Total Earning: ", f"<span style='color:green;'>$ {filtered_df['Amount'].sum():,}</span>", unsafe_allow_html=True)
        st.write("##### Charity (2.5%): ", f"<span style='color:red;'>$ {filtered_df['Amount'].sum() * 2.5 / 100:,}</span>", unsafe_allow_html=True)

        # Display sum of 'Fixed Price' and 'Hourly' amounts
        st.write(filtered_df.groupby('Type')['Amount'].sum())

        # Create a bar chart for the monthly summary
        st.write("##### Monthly Bar Chart")
        fig, ax = plt.subplots()
        bar_chart = ax.bar(monthly_summary['Month'], monthly_summary['Amount'])

        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')

        ax.bar_label(bar_chart, fmt='{:,.0f}')

        st.pyplot(fig)

        # Display the monthly summary
        st.write("##### Monthly Summary")
        st.write(monthly_summary)

    elif fee_option == "Included fee":
        # Calculate the total amount without service fee
        total_earning_included_fee = filtered_df['Amount'].sum() - abs(df[df['Type'].isin(['Service Fee'])].sum()['Amount'])
        st.write("##### Total Earning: ", f"<span style='color:green;'>$ {total_earning_included_fee:,}</span>", unsafe_allow_html=True)
        charity_percentage = 2.5
        st.write("##### Charity (2.5%): ", f"<span style='color:red;'>$ {total_earning_included_fee * charity_percentage / 100:.2f}</span>", unsafe_allow_html=True)
        st.write("##### Total Fee: ", f"<span style='color:red;'>$ {abs(df[df['Type'].isin(['Service Fee'])]['Amount'].sum()):.2f}</span>", unsafe_allow_html=True)


        # Display sum of 'Fixed Price' and 'Hourly' amounts
        # st.write(filtered_df.groupby('Type')['Amount'].sum() - abs(df[df['Type'] == 'Service Fee']['Amount'].sum()))
        # st.write(abs(df[df['Type'] == 'Service Fee']['Amount'].sum()))

        # Create a bar chart for the monthly summary
        st.write("##### Monthly Bar Chart")
        fig, ax = plt.subplots()
        bar_chart = ax.bar(monthly_summary['Month'], monthly_summary['Amount'] - abs(monthly_summary_fee['Amount']))

        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')

        ax.bar_label(bar_chart, fmt='{:,.0f}')

        st.pyplot(fig)

        # Display the monthly summary
        # st.write("##### Monthly Summary")
        # st.write(monthly_summary)

st.markdown("---")
st.markdown("Made with ❤️ by [Zein](https://www.upwork.com/freelancers/zeini)")