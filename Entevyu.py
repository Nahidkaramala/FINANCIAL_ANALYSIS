# Import necessary libraries
import pandas as pd
import numpy as np
import streamlit as st
import warnings
warnings.simplefilter("ignore")
from PIL import Image
import base64
import io
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pymysql
import cryptography


# Set page title and icon
icon = Image.open("icn.png")
st.set_page_config(
    page_title="Financial Analysis| By Nahid Banu",
    page_icon=icon,
    layout="wide"
)


box_style = """
    <style>
        .box {
            border: 1px solid #3F1209;
            padding: 1px;
            border-radius: 1px;
            background-color: #F7E4DE;
        }
    </style>
"""

# Apply the CSS style and the text within a box
st.markdown(box_style, unsafe_allow_html=True)
st.markdown("<div class='box'><h1 style='text-align: center; color:Black; font-size:35px;'>FINANCIAL ANALYSIS </h1></div>", unsafe_allow_html=True)


def setting_bg(background_image_url):
    st.markdown(f""" 
    <style>
        .stApp {{
            background: url('{background_image_url}') no-repeat center center fixed;
            background-size: cover;
            transition: background 0.5s ease;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #f3f3f3;
            font-family: 'Roboto', sans-serif;
        }}
        .stButton>button {{
            color: #4e4376;
            background-color: #f3f3f3;
            transition: all 0.3s ease-in-out;
        }}
        .stButton>button:hover {{
            color: #f3f3f3;
            background-color: #2b5876;
        }}
        .stTextInput>div>div>input {{
            color: #4e4376;
            background-color: #f3f3f3;
        }}
    </style>
    """, unsafe_allow_html=True)

# # Background image
background_image_url = "https://images.inc.com/uploaded_files/image/1920x1080/analysis_364470.jpg"
setting_bg(background_image_url)

with st.sidebar:
    st.header("FINANCIAL ANALYSIS")
        
    selected = option_menu(None,["Home","Insights","Dashboard"], 
                        icons=["house","trophy"],
                        default_index=0,
                        orientation="vertical",
                        styles={"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "0px", "--hover-color": "#6495ED"},
                                "icon": {"font-size": "35px"},
                                "container" : {"max-width": "6000px"},
                                "nav-link-selected": {"background-color": "#B4964E"}})
        

if selected== "Home":
    st.markdown('<p style="font-size: 44px; color: black;">Monitoring existing loans and identifying customers at risk of default helps banks manage and mitigate credit risk.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 44px; color: black;"Loan defaults pose financial risks to lending institutions, making accurate risk assessment crucial.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 44px; color: black;"> Exploratory Data Analysis of Customer data to conduct Risk Analysis for loan Default for a Consumer finance Company.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 44px; color: black;">Analyse historical laon Application data and identify the patterns and factors that indicate a clients status of default or Non- default.</p>', unsafe_allow_html=True)

if selected =="Insights":
    # Connection parameters
    # Database connection details
    host = 'localhost'
    user = 'root'
    password = 'Nahid123'
    database = 'financial_analysis'

    # Connect to the MySQL database using pymysql
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    mycursor = conn.cursor()


    Question = st.selectbox(":red[select your Question]", (' ',
                                                        '1.Credit Types:',
                                                        '2.Income Distribution & Descriptive Statistics wrt. Credit Type:',
                                                        '3.Analysis of Goods Amount for Cash Loans:',
                                                        '4.Age Brackets of the Clients:',
                                                        '5.Documents Submission Analysis:',
                                                        '6.Overall Analysis of Credit Enquiries on Clients:',
                                                        '7.Analysis of individual applications based on the credit enquiries:',
                                                        '8.Deeper analysis on the Contact reach for clients who had payment difficulties but were from the Very Low Risk social surroundings:',
                                                        '9.Integration of previous application data:',
                                                        '10.Top 15 customers and contact reach:'
                                                    )) 
    if Question == '1.Credit Types:':
        query1 = """SELECT NAME_CONTRACT_TYPE,
            SUM(count_application_data) AS total_count_application_data,
            SUM(count_previous_application) AS total_count_previous_application
        FROM (
            SELECT 
                NAME_CONTRACT_TYPE,
                COUNT(*) as count_application_data,
                0 as count_previous_application
            FROM financial_analysis.application_data 
            GROUP BY NAME_CONTRACT_TYPE
            UNION ALL
            SELECT 
                NAME_CONTRACT_TYPE,
                0 as count_application_data,
                COUNT(*) as count_previous_application
            FROM financial_analysis.previous_application 
            GROUP BY NAME_CONTRACT_TYPE
        ) AS merged_data
        GROUP BY NAME_CONTRACT_TYPE;"""
        

        # Execute the query
        mycursor = conn.cursor()
        mycursor.execute(query1)

        # Fetch the results into a DataFrame
        result = mycursor.fetchall()
        columns = [desc[0] for desc in mycursor.description]
        merged_df = pd.DataFrame(result, columns=columns)

        # Close the cursor and connection
        mycursor.close()
        # conn.close()

        # Print the merged DataFrame to check the result
        st.write (merged_df)

        # Plotting the merged data using Seaborn
        plt.figure(figsize=(14, 7))

        # Create a bar plot for application data
        sns.barplot(x='NAME_CONTRACT_TYPE', y='total_count_application_data', data=merged_df, color='b', label='Application Data')

        # Create another bar plot for previous application data with a different alpha value
        sns.barplot(x='NAME_CONTRACT_TYPE', y='total_count_previous_application', data=merged_df, color='r', label='Previous Application', alpha=0.7)

        # Adding labels and title
        plt.title('Counts of Loan Types in Application Data and Previous Application')
        plt.xlabel('Loan Type')
        plt.ylabel('Count')
        plt.legend()
        st.pyplot(plt)


    if Question == "2.Income Distribution & Descriptive Statistics wrt. Credit Type:":
        query2= """SELECT 
            NAME_CONTRACT_TYPE,
            COUNT(*) AS count,
            AVG(AMT_INCOME_TOTAL) AS mean_income,
            MIN(AMT_INCOME_TOTAL) AS min_income,
            MAX(AMT_INCOME_TOTAL) AS max_income,
            SUM(AMT_INCOME_TOTAL) AS sum_income
        FROM 
            application_data
        GROUP BY 
            NAME_CONTRACT_TYPE

        UNION ALL

        SELECT 
            NAME_CONTRACT_TYPE,
            COUNT(*) AS count,
            NULL AS mean_income,
            NULL AS min_income,
            NULL AS max_income,
            NULL AS sum_income
        FROM 
            previous_application
        GROUP BY 
            NAME_CONTRACT_TYPE;
            """
        # Execute the query and fetch the results into a DataFrame
        merged_df2 = pd.read_sql_query(query2, conn)

        # Print the merged DataFrame to check the result
        st.write (merged_df2)

        # Filter DataFrame to include only the first two rows
        df_filtered = merged_df2.head(2)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(df_filtered['NAME_CONTRACT_TYPE'], df_filtered['count'], color='blue', label='Count')
        plt.xlabel('Contract Type')
        plt.ylabel('Count')
        plt.title('Counts of Loan Types (First Two Rows)')
        plt.legend()
        st.pyplot(plt)


    if Question== "3.Analysis of Goods Amount for Cash Loans:":
        query3="""
            SELECT
            COUNT(*) AS count,
            MIN(AMT_GOODS_PRICE) AS min_price,
            MAX(AMT_GOODS_PRICE) AS max_price,
            AVG(AMT_GOODS_PRICE) AS avg_price
        FROM (
            SELECT AMT_GOODS_PRICE
            FROM application_data
            WHERE NAME_CONTRACT_TYPE = 'Cash loans'

            UNION ALL

            SELECT AMT_GOODS_PRICE
            FROM previous_application
            WHERE NAME_CONTRACT_TYPE = 'Cash loans'
        ) AS merged_data;
        """
    # Execute the query and fetch the results into a DataFrame
        merged_df3 = pd.read_sql_query(query3, conn)

        # Print the merged DataFrame to check the result
        st.write (merged_df3)

        df = pd.DataFrame(merged_df3)
        
        # Plotting bar plots
        plt.figure(figsize=(10, 6))

        # Plotting min_price
        plt.barh('Min Price', df['min_price'].mean(), color='blue', label='Min Price')
        # Plotting max_price
        plt.barh('Max Price', df['max_price'].mean(), color='green', label='Max Price')
        # Plotting avg_price
        plt.barh('Average Price', df['avg_price'].mean(), color='orange', label='Average Price')

        plt.title('Bar Plot of Min, Max, and Average Prices')
        plt.xlabel('Price')
        plt.ylabel('Price Type')
        plt.legend()
        st.pyplot(plt)
        
    if Question=="4.Age Brackets of the Clients:":
        query4= """
        SELECT CASE
        WHEN DAYS_BIRTH < -36500 THEN '70+'
        WHEN DAYS_BIRTH < -29200 THEN '60-69'
        WHEN DAYS_BIRTH < -21900 THEN '50-59'
        WHEN DAYS_BIRTH < -14600 THEN '40-49'
        WHEN DAYS_BIRTH < -7300 THEN '30-39'
        WHEN DAYS_BIRTH < 0 THEN '20-29'
        END AS age_group,
        COUNT(*) AS count
        FROM application_data
        GROUP BY age_group"""
        # Read data into DataFrame
        merged_df4 = pd.read_sql_query(query4, conn)
        st.write (merged_df4)

        # Plotting age distribution
        plt.figure(figsize=(10, 6))
        sns.barplot(x='age_group', y='count', data=merged_df4, palette='viridis')
        plt.title('Age Distribution of Clients')
        plt.xlabel('Age Group')
        plt.ylabel('Number of Clients')
        # Display the plot in Streamlit
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()


    if Question =='5.Documents Submission Analysis:':
        query5= """
        SELECT COUNT(*) AS num_clients
        FROM (
            SELECT SK_ID_CURR
            FROM application_data
            WHERE FLAG_DOCUMENT_2 = 1 OR FLAG_DOCUMENT_3 = 1 OR FLAG_DOCUMENT_4 = 1 OR FLAG_DOCUMENT_5 = 1
                OR FLAG_DOCUMENT_6 = 1 OR FLAG_DOCUMENT_7 = 1 OR FLAG_DOCUMENT_8 = 1 OR FLAG_DOCUMENT_9 = 1
                OR FLAG_DOCUMENT_10 = 1 OR FLAG_DOCUMENT_11 = 1 OR FLAG_DOCUMENT_12 = 1 OR FLAG_DOCUMENT_13 = 1
                OR FLAG_DOCUMENT_14 = 1 OR FLAG_DOCUMENT_15 = 1 OR FLAG_DOCUMENT_16 = 1 OR FLAG_DOCUMENT_17 = 1
                OR FLAG_DOCUMENT_18 = 1 OR FLAG_DOCUMENT_19 = 1 OR FLAG_DOCUMENT_20 = 1 OR FLAG_DOCUMENT_21 = 1
            GROUP BY SK_ID_CURR
        ) AS subquery;
        """
        # Read data into DataFrame
        merged_df5 = pd.read_sql_query(query5, conn)
        st.write (merged_df5)

    if Question =='6.Overall Analysis of Credit Enquiries on Clients:':
        query6= """
        SELECT 
        COUNT(AMT_REQ_CREDIT_BUREAU_HOUR) AS AMT_REQ_CREDIT_BUREAU_HOUR,
        COUNT(AMT_REQ_CREDIT_BUREAU_DAY) AS AMT_REQ_CREDIT_BUREAU_DAY,
        COUNT(AMT_REQ_CREDIT_BUREAU_WEEK) AS AMT_REQ_CREDIT_BUREAU_WEEK,
        COUNT(AMT_REQ_CREDIT_BUREAU_MON) AS AMT_REQ_CREDIT_BUREAU_MON,
        COUNT(AMT_REQ_CREDIT_BUREAU_QRT) AS AMT_REQ_CREDIT_BUREAU_QRT,
        COUNT(AMT_REQ_CREDIT_BUREAU_YEAR) AS AMT_REQ_CREDIT_BUREAU_YEAR
        FROM 
            application_data;
        """
        # Read data into DataFrame
        merged_df6 = pd.read_sql_query(query6, conn)
        st.write (merged_df6)

        # # Convert the result to a DataFrame
        # df = pd.DataFrame(result)

        # Plotting the bar plot
        plt.figure(figsize=(10, 6))
        merged_df6.plot(kind='bar')
        plt.title('Count of Non-null Values in Credit Bureau Requests')
        plt.xlabel('Columns')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        st.pyplot(plt)

    if Question == "7.Analysis of individual applications based on the credit enquiries:":
        query7= """
        SELECT 
            COUNT(AMT_REQ_CREDIT_BUREAU_HOUR) AS AMT_REQ_CREDIT_BUREAU_HOUR,
            COUNT(AMT_REQ_CREDIT_BUREAU_DAY) AS AMT_REQ_CREDIT_BUREAU_DAY,
            COUNT(AMT_REQ_CREDIT_BUREAU_WEEK) AS AMT_REQ_CREDIT_BUREAU_WEEK,
            COUNT(AMT_REQ_CREDIT_BUREAU_MON) AS AMT_REQ_CREDIT_BUREAU_MON,
            COUNT(AMT_REQ_CREDIT_BUREAU_QRT) AS AMT_REQ_CREDIT_BUREAU_QRT,
            COUNT(AMT_REQ_CREDIT_BUREAU_YEAR) AS AMT_REQ_CREDIT_BUREAU_YEAR
        FROM 
            application_data;"""
        
        df7 = pd.read_sql_query(query7, conn)
        st.write(df7)

    if Question =="8.Deeper analysis on the Contact reach for clients who had payment difficulties but were from the Very Low Risk social surroundings:":
        query8= """WITH PaymentDifficulties AS (
            SELECT 
                a.SK_ID_CURR,
                p.CHANNEL_TYPE,
                p.NAME_YIELD_GROUP
            FROM 
                application_data a
            INNER JOIN 
                previous_application p ON a.SK_ID_CURR = p.SK_ID_CURR
            WHERE 
                a.TARGET = 1 -- Assuming TARGET = 1 indicates payment difficulties
                AND a.REGION_RATING_CLIENT = 1 -- Assuming 1 represents very low-risk social surroundings
        )
        SELECT 
            CHANNEL_TYPE,
            COUNT(*) AS ContactAttempts,
            SUM(CASE WHEN NAME_YIELD_GROUP = 'XNA' THEN 1 ELSE 0 END) AS UnspecifiedAttempts,
            SUM(CASE WHEN NAME_YIELD_GROUP != 'XNA' THEN 1 ELSE 0 END) AS SpecifiedAttempts,
            COUNT(DISTINCT SK_ID_CURR) AS UniqueClients
        FROM 
            PaymentDifficulties
        GROUP BY 
            CHANNEL_TYPE
        ORDER BY 
            ContactAttempts DESC;"""
        
        merged_df8= pd.read_sql_query(query8, conn)
        st.write (merged_df8) 

        # Grouped bar chart
        plt.figure(figsize=(10, 6))

        # Plotting specified and unspecified attempts
        plt.bar(merged_df8['CHANNEL_TYPE'], merged_df8['SpecifiedAttempts'], color='blue', label='Specified Attempts')
        plt.bar(merged_df8['CHANNEL_TYPE'], merged_df8['UnspecifiedAttempts'], color='orange', label='Unspecified Attempts')

        # Plotting unique clients
        plt.plot(merged_df8['CHANNEL_TYPE'], merged_df8['UniqueClients'], color='green', marker='o', linestyle='dashed', linewidth=2, markersize=8, label='Unique Clients')

        # Adding labels and title
        plt.title('Contact Attempts and Unique Clients by Channel Type')
        plt.xlabel('Channel Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.legend()

        # Show plot
        plt.tight_layout()
        st.pyplot(plt)

    if Question =="9.Integration of previous application data:":
        query9= """SELECT current.SK_ID_CURR AS current_SK_ID_CURR,
            current.TARGET AS current_TARGET,
            current.NAME_CONTRACT_TYPE AS current_NAME_CONTRACT_TYPE,
            previous.SK_ID_CURR AS previous_SK_ID_CURR,
            previous.NAME_CONTRACT_TYPE AS previous_NAME_CONTRACT_TYPE
        FROM 
            application_data AS current
        INNER JOIN 
            previous_application AS previous ON current.SK_ID_CURR = previous.SK_ID_CURR 
        LIMIT 100;"""
        df9= pd.read_sql_query(query9, conn)
        st.write(df9)

    if Question =="10.Top 15 customers and contact reach:":
        query10= """WITH ContactReach AS (
            SELECT 
                a.SK_ID_CURR,
                p.CHANNEL_TYPE,
                p.NAME_YIELD_GROUP
            FROM 
                application_data a
            INNER JOIN 
                previous_application p ON a.SK_ID_CURR = p.SK_ID_CURR
        ),
        TopCustomers AS (
            SELECT 
                SK_ID_CURR,
                COUNT(*) AS TotalContactAttempts
            FROM 
                ContactReach
            GROUP BY 
                SK_ID_CURR
            ORDER BY 
                TotalContactAttempts DESC
            LIMIT 15
        )
        SELECT 
            tc.SK_ID_CURR,
            tc.TotalContactAttempts,
            cr.CHANNEL_TYPE,
            COUNT(*) AS ContactAttempts,
            SUM(CASE WHEN cr.NAME_YIELD_GROUP = 'XNA' THEN 1 ELSE 0 END) AS UnspecifiedAttempts,
            SUM(CASE WHEN cr.NAME_YIELD_GROUP != 'XNA' THEN 1 ELSE 0 END) AS SpecifiedAttempts
        FROM 
            TopCustomers tc
        INNER JOIN 
            ContactReach cr ON tc.SK_ID_CURR = cr.SK_ID_CURR
        GROUP BY 
            tc.SK_ID_CURR, cr.CHANNEL_TYPE
        ORDER BY 
            tc.TotalContactAttempts DESC LIMIT 15;
        """
        merged_df10= pd.read_sql_query(query10, conn)
        st.write(merged_df10)

if selected=="Dashboard":
    dashboard = Image.open("pbix.png")
    st.write(dashboard)