import streamlit as st
import pandas as pd
import plotly.express as px

#page configration
st.set_page_config(
    page_title="Online Retail Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

#Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_retail_sample.csv")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()

# sidebar filters
st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Select Country",
    options=sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

filtered_df = df[df["Country"].isin(country)]


#Dashboard title
st.title("🛒 Online Retail Sales Dashboard")
st.markdown("### Sales Performance & Customer Analytics")


#KPI Cards

total_revenue = filtered_df["TotalAmount"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["CustomerID"].nunique()
avg_order_value = filtered_df.groupby("InvoiceNo")["TotalAmount"].sum().mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"£{total_revenue:,.0f}")
col2.metric("🧾 Total Orders", f"{total_orders:,}")
col3.metric("👥 Total Customers", f"{total_customers:,}")
col4.metric("🛍 Avg Order Value", f"£{avg_order_value:,.2f}")

st.markdown("---")

#top 10 countries by revenue
country_sales = (
    filtered_df.groupby("Country")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_country = px.bar(
    country_sales,
    x="Country",
    y="TotalAmount",
    title="Top 10 Countries by Revenue",
    text_auto=".2s",
    color="TotalAmount"
)

fig_country.update_layout(
    xaxis_title="Country",
    yaxis_title="Revenue (£)"
)

st.plotly_chart(fig_country, use_container_width=True)

#top 10 selling products
top_products = (
    filtered_df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="Quantity",
    y="Description",
    orientation="h",
    title="Top 10 Selling Products",
    text_auto=True,
    color="Quantity"
)

fig_products.update_layout(
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig_products, use_container_width=True)

#Monthly Revenue Trend
monthly_sales = (
    filtered_df.groupby(["MonthNo", "Month"])["TotalAmount"]
    .sum()
    .reset_index()
    .sort_values("MonthNo")
)

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="TotalAmount",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig_month, use_container_width=True)

#Charts slider
left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig_country,
        use_container_width=True,
        key="country_chart"
    )

with right:
    st.plotly_chart(
        fig_products,
        use_container_width=True,
        key="product_chart"
    )


    #montlely trend left side
    monthly_sales = (
    filtered_df.groupby(["MonthNo", "Month"])["TotalAmount"]
    .sum()
    .reset_index()
    .sort_values("MonthNo")
)

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="TotalAmount",
    markers=True,
    title="📈 Monthly Revenue Trend"
)



#top 10 customers
top_customers = (
    filtered_df.groupby("CustomerID")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_customer = px.bar(
    top_customers,
    x="CustomerID",
    y="TotalAmount",
    title="🏆 Top 10 Customers by Revenue",
    text_auto=".2s",
    color="TotalAmount"
)


#display sidebar filters
left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig_month,
        use_container_width=True,
        key="monthly_chart"
    )

with right:
    st.plotly_chart(
        fig_customer,
        use_container_width=True,
        key="customer_chart"
    )


# Country share pie chart
country_share = (
    filtered_df.groupby("Country")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_pie = px.pie(
    country_share,
    values="TotalAmount",
    names="Country",
    title="🌍 Revenue Share by Country",
    hole=0.45
)

# Weekday sales bar chart
weekday_order = [
    "Monday","Tuesday","Wednesday",
    "Thursday","Friday","Saturday","Sunday"
]

weekday_sales = (
    filtered_df.groupby("Weekday")["TotalAmount"]
    .sum()
    .reindex(weekday_order)
    .reset_index()
)

fig_weekday = px.bar(
    weekday_sales,
    x="Weekday",
    y="TotalAmount",
    title="📅 Weekday Sales",
    color="TotalAmount"
)


#display sidebar filters
left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig_pie,
        use_container_width=True,
        key="pie_chart"
    )

with right:
    st.plotly_chart(
        fig_weekday,
        use_container_width=True,
        key="weekday_chart"
    )

#Hour sales analysis
hourly_sales = (
    filtered_df.groupby("Hour")["TotalAmount"]
    .sum()
    .reset_index()
)

fig_hour = px.line(
    hourly_sales,
    x="Hour",
    y="TotalAmount",
    markers=True,
    title="🕒 Hourly Sales Analysis"
)

st.plotly_chart(
    fig_hour,
    use_container_width=True,
    key="hourly_chart"
)

#Top 10 products by revenue
top_revenue_products = (
    filtered_df.groupby("Description")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_rev_product = px.bar(
    top_revenue_products,
    x="TotalAmount",
    y="Description",
    orientation="h",
    title="💰 Top 10 Products by Revenue",
    color="TotalAmount",
    text_auto=".2s"
)

st.plotly_chart(
    fig_rev_product,
    use_container_width=True,
    key="revenue_product_chart"
)


#interactive data table
st.subheader("📋 Retail Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# Download filtered data as CSV
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_retail.csv",
    mime="text/csv"
)



# filtered data based on user selection
# Year Filter
year = st.sidebar.multiselect(
    "Select Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

# Month Filter
month = st.sidebar.multiselect(
    "Select Month",
    sorted(df["Month"].unique()),
    default=sorted(df["Month"].unique())
)

filtered_df = df[
    (df["Country"].isin(country)) &
    (df["Year"].isin(year)) &
    (df["Month"].isin(month))
]

#About project
st.markdown("## 📌 About Project")

st.info("""
This dashboard analyzes online retail sales data to provide insights into revenue, customer behavior,
product performance, and sales trends. Interactive filters and visualizations help businesses make
data-driven decisions.
""")

# Footer
st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:25px;">

<h2>👨‍💻 Vikas Babu</h2>

<p>
<a href="https://github.com/vikrampratab" target="_blank">
<img src="https://img.shields.io/badge/GitHub-vikrampratab-black?style=for-the-badge&logo=github">
</a>

&nbsp;

<a href="https://www.linkedin.com/in/vikasbabu07/" target="_blank">
<img src="https://img.shields.io/badge/LinkedIn-Vikas%20Babu-blue?style=for-the-badge&logo=linkedin">
</a>
</p>

<p style="color:gray;">
📊 Online Retail Analytics Dashboard
</p>

<p style="font-size:13px;color:gray;">
Built with ❤️ using Python • Streamlit • Plotly
</p>

</div>
""", unsafe_allow_html=True)