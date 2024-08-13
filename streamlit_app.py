import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
# import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS database credentials
DB_HOST = "tellmoredb.cd24ogmcy170.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASS = "2yYKKH8lUzaBvc92JUxW"
DB_PORT = "3306"
DB_NAME = "claires_data"

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
#
# if "chat_visible" not in st.session_state:
#     st.session_state.chat_visible = False


# def get_openai_response(usr_inp):
#     client = openai.AzureOpenAI(
#         azure_endpoint="https://tellmoredemogpt.openai.azure.com/",
#         api_key="94173b7e3f284f2c8f8eb1804fa55699",
#         api_version="2023-09-01-preview"
#     )
#     response = client.chat.completions.create(
#         model= "tellmore-demo-gpt35",
#         messages=[{"role": "user", "content": usr_inp}],
#         max_tokens=50
#     )
#     return response.choices[0].message.content


def connect_to_db():
    return pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )

# def connect_to_db():
#     return pymysql.connect(
#         host=os.getenv("DB_HOST"),
#         port=int(os.getenv("DB_PORT")),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASS"),
#         db=os.getenv("DB_NAME")
#     )


def execute_query(query):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            getResult = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
        return pd.DataFrame(getResult, columns=columns)
    finally:
        conn.close()


st.subheader("Hey Store Manager!")
st.title("Store Analytics Dashboard")

# queries = {
#     "Select a query": None,
#     "Give details about all stores with shrinkage rate greater than or equal to 3": "SELECT s.Store_ID, s.Store_Location_Type, s.Shrinkage_Rate, s.`Store-Specific_Shrinkage_Reduction_Strategies`\nFROM shrinkageStores s\nWHERE s.Shrinkage_Rate >= 3\nORDER BY s.Store_ID ASC;",
#     "Give details about all products with shrinkage rates more than 4.9": "SELECT s.Product_ID, s.Shrinkage_Rate, s.Root_Cause_Analysis, s.Loss_Prevention_Measures\nFROM shrinkageAndLossPrevention s\nWHERE s.Shrinkage_Rate > 4.9\nORDER BY s.Shrinkage_Rate DESC;",
#     "List all customers aged over 50 who have spent more than $15000": "SELECT c.Customer_ID, c.Customer_Name, c.Age, c.Total_Spent, c.Gender, c.Loyalty_Status\nFROM customers c\nWHERE c.Age > 50 AND c.Total_Spent > 15000\nORDER BY c.Total_Spent DESC;",
#     "Give the performance evaluation of the suppliers with the top 25 order picking accuracies": "SELECT sm.Supplier_Name, sm.Supplier_Performance_Evaluation, opf.Order_Picking_Accuracy\nFROM supplierMetrics sm\nJOIN orderPickingAndFulfillment opf ON sm.Supplier_ID = opf.Supplier_ID\nORDER BY opf.Order_Picking_Accuracy DESC\nLIMIT 25;",
#     "List the allocation strategies for products with the 30 lowest inventory turnover rates": "SELECT p.Product_ID, p.Inventory_Allocation_Strategy, i.Safety_Stock_Levels, i.Inventory_Monthly_Turnover_Rate\nFROM promotionalAndMarketData p\nJOIN inventoryMetrics i ON p.Product_ID = i.Product_ID\nORDER BY i.Inventory_Monthly_Turnover_Rate DESC\nLIMIT 30;",
#     "Give the loss prevention audit findings of all stores with sales per square foot below 300": "SELECT s.Store_ID, s.LossPreventionAudit_Findings, se.Sales_per_SquareFoot\nFROM shrinkageStores s\nJOIN storeEfficiency se ON s.Store_ID = se.Store_ID\nWHERE se.Sales_per_SquareFoot < 300\nORDER BY s.Store_ID ASC;",
# }

queries = {
    "Select a query": None,
    "Compare the sales performance across all stores for this year against the previous year": "SELECT DISTINCT STORE_ID, STORE_NAME, SALES_TY, SALES_LY\nFROM claires_data.store_total;",

}

# toggle_button = st.button("💬 Chat", key="toggle_chat")
# if toggle_button:
#     st.session_state.chat_visible = not st.session_state.chat_visible

# st.markdown(
#     """
#     <style>
#     .floating-chatbox {
#         position: fixed;
#         bottom: 80px;
#         right: 20px;
#         width: 300px;
#         max-height: 400px;
#         padding: 10px;
#         border: 1px solid #ccc;
#         border-radius: 10px;
#         background-color: white;
#         box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
#         z-index: 1000;
#     }
#     .floating-chatbox-header {
#         font-weight: bold;
#         text-align: center;
#         padding: 5px 0;
#         background-color: #007BFF;
#         color: white;
#         border-radius: 5px 5px 0 0;
#     }
#     .floating-chatbox-body {
#         max-height: 300px;
#         overflow-y: auto;
#         margin-bottom: 10px;
#         background-color: #808080;
#     }
#     .floating-chatbox-input {
#         width: 100%;
#         padding: 5px;
#         border-radius: 5px;
#         border: 1px solid #ccc;
#     }
#     .floating-chatbox-button {
#         width: 100%;
#         padding: 5px;
#         margin-top: 5px;
#         background-color: #007BFF;
#         color: white;
#         border: none;
#         border-radius: 5px;
#         cursor: pointer;
#     }
#     .stButton>button {
#         position: fixed;
#         bottom: 20px;
#         right: 20px;
#         width: 60px;
#         height: 60px;
#         background-color: #007BFF;
#         color: white;
#         border-radius: 50%;
#         font-size: 24px;
#         z-index: 1000;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# if st.session_state.chat_visible:
#     with st.container(height=300, border=True):
#         st.markdown('<div class="floating-chatbox-header">Assistant</div>', unsafe_allow_html=True)
#         chat_placeholder = st.empty()
#         with chat_placeholder.container():
#             st.markdown('<div class="floating-chatbox-body">', unsafe_allow_html=True)
#             for message in st.session_state.chat_history:
#                 st.markdown(f"**{message['role']}:** {message['content']}")
#             st.markdown('</div>', unsafe_allow_html=True)
#
#         user_input = st.text_input("", key="input", placeholder="Type your message...", label_visibility="collapsed")
#
#         if st.button("Send", key="send", help="Send your message", use_container_width=True):
#             if user_input:
#                 st.session_state.chat_history.append({"role": "You", "content": user_input})
#                 bot_response = get_openai_response(user_input)
#                 st.session_state.chat_history.append({"role": "Bot", "content": bot_response})
#                 st.query_params = st.session_state.chat_history
#
#         st.markdown('</div>', unsafe_allow_html=True)

selected_query = st.selectbox("Select a query", list(queries.keys()))
if selected_query and selected_query != "Select a query":
    query_sql = queries[selected_query]
    result = execute_query(query_sql)
    st.dataframe(result, height = 300)

    if not result.empty:
        st.subheader("Visualizations")

        # if selected_query == "Give details about all products with shrinkage rates more than 4.9":
        #     root_cause_counts = result['Root_Cause_Analysis'].value_counts().reset_index()
        #     root_cause_counts.columns = ['Root_Cause_Analysis', 'Count']
        #     st.title("Count of Product by Root Cause Analysis")
        #     fig = px.bar(
        #         root_cause_counts,
        #         x = 'Root_Cause_Analysis',
        #         y = 'Count',
        #     )
        #     st.plotly_chart(fig)
        #
        #     measures_counts = result.groupby(['Root_Cause_Analysis', 'Loss_Prevention_Measures']).size().reset_index(name = 'Count')
        #     pivot_df = measures_counts.pivot(index = 'Root_Cause_Analysis', columns = 'Loss_Prevention_Measures', values = 'Count').fillna(0)
        #     st.title("Loss Prevention Measures by Root Cause Analysis")
        #     plotly_fig = px.bar(
        #         measures_counts,
        #         x = "Root_Cause_Analysis",
        #         y = "Count",
        #         color = "Loss_Prevention_Measures",
        #         barmode = "group",
        #         labels = {"Root_Cause_Analysis": "Root Cause Analysis", "Count": "Count of Loss Prevention Measures"}
        #     )
        #     st.plotly_chart(plotly_fig)
        #
        # elif selected_query == "Give details about all stores with shrinkage rate greater than or equal to 3":
        #     location_counts = result['Store_Location_Type'].value_counts().reset_index()
        #     location_counts.columns = ['Store_Location_Type', 'Count']
        #     st.title("Store Location Types")
        #     pie_fig = px.pie(
        #         location_counts,
        #         names = 'Store_Location_Type',
        #         values = 'Count',
        #     )
        #     st.plotly_chart(pie_fig)
        #
        #     strategy_counts = result['Store-Specific_Shrinkage_Reduction_Strategies'].value_counts().reset_index()
        #     strategy_counts.columns = ['Store-Specific_Shrinkage_Reduction_Strategies', 'Count']
        #     st.title("Shrinkage Reduction Strategies")
        #     bar_fig = px.bar(
        #         strategy_counts,
        #         x = 'Store-Specific_Shrinkage_Reduction_Strategies',
        #         y = 'Count',
        #     )
        #     st.plotly_chart(bar_fig)
        #
        # elif selected_query == "List all customers aged over 50 who have spent more than $15000":
        #     gender_spent = result.groupby('Gender')['Total_Spent'].sum().reset_index()
        #     st.title("Total Sum of Money Spent by Customers of Each Gender")
        #     pie_fig_gender = px.pie(
        #         gender_spent,
        #         names = 'Gender',
        #         values = 'Total_Spent',
        #         title = 'Total Spending by Gender'
        #     )
        #     st.plotly_chart(pie_fig_gender)
        #
        #     result['Age_Group'] = pd.cut(result['Age'], bins=range(50, 100, 5))
        #     result['Age_Group'] = result['Age_Group'].astype(str)
        #     age_spent = result.groupby('Age_Group')['Total_Spent'].sum().reset_index()
        #     st.title("Total Sum of Money Spent by Age Group")
        #     bar_fig_age = px.bar(
        #         age_spent,
        #         x = 'Age_Group',
        #         y = 'Total_Spent',
        #         title = 'Total Spending by Age Group'
        #     )
        #     st.plotly_chart(bar_fig_age)
        #
        #     loyalty_spent = result.groupby('Loyalty_Status')['Total_Spent'].sum().reset_index()
        #     st.title("Total Sum of Money Spent by Loyalty Status")
        #     pie_fig_loyalty = px.pie(
        #         loyalty_spent,
        #         names = 'Loyalty_Status',
        #         values = 'Total_Spent',
        #         title = 'Total Spending by Loyalty Status'
        #     )
        #     st.plotly_chart(pie_fig_loyalty)
        #
        # elif selected_query == "Give the performance evaluation of the suppliers with the top 25 order picking accuracies":
        #     evaluation_counts = result['Supplier_Performance_Evaluation'].value_counts().reset_index()
        #     evaluation_counts.columns = ['Supplier_Performance_Evaluation', 'Count']
        #     st.title("Performance Evaluation of Suppliers")
        #     pie_fig_evaluation = px.pie(
        #         evaluation_counts,
        #         names = 'Supplier_Performance_Evaluation',
        #         values = 'Count',
        #         title = 'Supplier Performance Evaluation'
        #     )
        #     st.plotly_chart(pie_fig_evaluation)
        #
        # elif selected_query == "List the allocation strategies for products with the 30 lowest inventory turnover rates":
        #     turnover_by_strategy = result.groupby('Inventory_Allocation_Strategy')['Inventory_Monthly_Turnover_Rate'].sum().reset_index()
        #     st.title("Sum of Inventory Turnover Rates by Allocation Strategy")
        #     bar_fig_turnover = px.bar(
        #         turnover_by_strategy,
        #         x = 'Inventory_Allocation_Strategy',
        #         y = 'Inventory_Monthly_Turnover_Rate',
        #         title = 'Sum of Inventory Turnover Rates by Allocation Strategy'
        #     )
        #     st.plotly_chart(bar_fig_turnover)
        #
        #     safety_stock_by_strategy = result.groupby('Inventory_Allocation_Strategy')['Safety_Stock_Levels'].sum().reset_index()
        #     st.title("Sum of Safety Stock Levels by Allocation Strategy")
        #     bar_fig_safety_stock = px.bar(
        #         safety_stock_by_strategy,
        #         x = 'Inventory_Allocation_Strategy',
        #         y = 'Safety_Stock_Levels',
        #         title = 'Sum of Safety Stock Levels by Allocation Strategy'
        #     )
        #     st.plotly_chart(bar_fig_safety_stock)
        #
        # elif selected_query == "Give the loss prevention audit findings of all stores with sales per square foot below 300":
        #     audit_counts = result['LossPreventionAudit_Findings'].value_counts().reset_index()
        #     audit_counts.columns = ['LossPreventionAudit_Findings', 'Count']
        #     st.title("Count of Store IDs for Each Loss Prevention Audit Finding")
        #     pie_fig_audit = px.pie(
        #         audit_counts,
        #         names = 'LossPreventionAudit_Findings',
        #         values = 'Count',
        #         title = 'Loss Prevention Audit Findings'
        #     )
        #     st.plotly_chart(pie_fig_audit)
        #
        #     avg_sales = result.groupby('Store_ID')['Sales_per_SquareFoot'].mean().reset_index()
        #     st.title("Average Sales per Square Foot by Store ID")
        #     line_fig_sales = px.line(
        #         avg_sales,
        #         x = 'Store_ID',
        #         y = 'Sales_per_SquareFoot',
        #         title='Average Sales per Square Foot by Store ID'
        #     )
        #     st.plotly_chart(line_fig_sales)
        if selected_query == "Compare the sales performance across all stores for this year against the previous year":
            # print(result)
            st.subheader("Sales Performance Comparison")

            # Reshape the data for plotting
            df_melted = result.melt(id_vars=["STORE_NAME"], value_vars=["SALES_TY", "SALES_LY"],
                                    var_name="Year", value_name="Sales")

            # Create the line chart with a logarithmic y-axis
            fig = px.line(df_melted, x="STORE_NAME", y="Sales", color="Year",
                          title="Sales Performance Comparison Across Stores",
                          labels={"Sales": "Sales Amount", "STORE_NAME": "Store Name"},
                          color_discrete_map={"SALES_TY": "red", "SALES_LY": "blue"},
                          height=700, width=1400)  # Adjusting the graph size

            fig.update_layout(
                xaxis_title="Store Name",
                yaxis_title="Sales Amount (Log Scale)",
                xaxis_tickangle=-45,
                yaxis_type="log",  # Setting y-axis to logarithmic scale
                yaxis=dict(
                    tickmode='auto'
                )
            )

            st.plotly_chart(fig)

else:
    st.write("Please select a query from the dropdown menu.")
