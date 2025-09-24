import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.2rem;
    }
    .filter-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process the JSON data"""
    try:
        with open('XLPrompt_Output_2025-09-24_09-55-41.json', 'r') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data['data'])
        
        # Convert OrderDate to datetime
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        
        # Extract date components for filtering
        df['Year'] = df['OrderDate'].dt.year
        df['Month'] = df['OrderDate'].dt.month
        df['MonthName'] = df['OrderDate'].dt.month_name()
        df['Quarter'] = df['OrderDate'].dt.quarter
        df['DayOfWeek'] = df['OrderDate'].dt.day_name()
        
        # Calculate additional metrics
        df['Profit'] = df['Revenue'] * 0.2  # Assuming 20% profit margin
        df['DiscountAmount'] = df['UnitPrice'] * df['Quantity'] * df['DiscountPct']
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def create_kpi_metrics(df):
    """Create KPI metrics section"""
    st.markdown('<div class="main-header">📊 Sales Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Calculate KPIs
    total_revenue = df['Revenue'].sum()
    total_orders = len(df)
    avg_order_value = df['Revenue'].mean()
    total_quantity = df['Quantity'].sum()
    total_profit = df['Profit'].sum()
    avg_discount = df['DiscountPct'].mean() * 100
    
    # Display KPIs in columns
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">${total_revenue:,.0f}</div>
            <div class="kpi-label">Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">${avg_order_value:,.0f}</div>
            <div class="kpi-label">Avg Order Value</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">{total_quantity:,}</div>
            <div class="kpi-label">Total Quantity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">${total_profit:,.0f}</div>
            <div class="kpi-label">Total Profit</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">{avg_discount:.1f}%</div>
            <div class="kpi-label">Avg Discount</div>
        </div>
        """, unsafe_allow_html=True)

def create_filters(df):
    """Create sidebar filters"""
    st.sidebar.markdown('<div class="filter-container">', unsafe_allow_html=True)
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = df['OrderDate'].min().date()
    max_date = df['OrderDate'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Country filter
    countries = ['All'] + sorted(df['Country'].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        countries,
        default=['All']
    )
    
    # Segment filter
    segments = ['All'] + sorted(df['Segment'].unique().tolist())
    selected_segments = st.sidebar.multiselect(
        "Select Segments",
        segments,
        default=['All']
    )
    
    # Channel filter
    channels = ['All'] + sorted(df['Channel'].unique().tolist())
    selected_channels = st.sidebar.multiselect(
        "Select Channels",
        channels,
        default=['All']
    )
    
    # Category filter
    categories = ['All'] + sorted(df['Category'].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        categories,
        default=['All']
    )
    
    # Revenue range filter
    min_revenue = float(df['Revenue'].min())
    max_revenue = float(df['Revenue'].max())
    
    revenue_range = st.sidebar.slider(
        "Revenue Range",
        min_value=min_revenue,
        max_value=max_revenue,
        value=(min_revenue, max_revenue),
        format="$%.0f"
    )
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'date_range': date_range,
        'countries': selected_countries,
        'segments': selected_segments,
        'channels': selected_channels,
        'categories': selected_categories,
        'revenue_range': revenue_range
    }

def apply_filters(df, filters):
    """Apply selected filters to the dataframe"""
    filtered_df = df.copy()
    
    # Date filter
    if len(filters['date_range']) == 2:
        start_date, end_date = filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['OrderDate'].dt.date >= start_date) &
            (filtered_df['OrderDate'].dt.date <= end_date)
        ]
    
    # Country filter
    if 'All' not in filters['countries'] and filters['countries']:
        filtered_df = filtered_df[filtered_df['Country'].isin(filters['countries'])]
    
    # Segment filter
    if 'All' not in filters['segments'] and filters['segments']:
        filtered_df = filtered_df[filtered_df['Segment'].isin(filters['segments'])]
    
    # Channel filter
    if 'All' not in filters['channels'] and filters['channels']:
        filtered_df = filtered_df[filtered_df['Channel'].isin(filters['channels'])]
    
    # Category filter
    if 'All' not in filters['categories'] and filters['categories']:
        filtered_df = filtered_df[filtered_df['Category'].isin(filters['categories'])]
    
    # Revenue filter
    filtered_df = filtered_df[
        (filtered_df['Revenue'] >= filters['revenue_range'][0]) &
        (filtered_df['Revenue'] <= filters['revenue_range'][1])
    ]
    
    return filtered_df

def create_visualizations(df):
    """Create various visualizations"""
    
    # Revenue by Country
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Revenue by Country")
        country_revenue = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
        fig_country = px.bar(
            x=country_revenue.index,
            y=country_revenue.values,
            title="Revenue by Country",
            labels={'x': 'Country', 'y': 'Revenue ($)'},
            color=country_revenue.values,
            color_continuous_scale='Blues'
        )
        fig_country.update_layout(showlegend=False)
        st.plotly_chart(fig_country, use_container_width=True)
    
    with col2:
        st.subheader("📈 Revenue by Segment")
        segment_revenue = df.groupby('Segment')['Revenue'].sum()
        fig_segment = px.pie(
            values=segment_revenue.values,
            names=segment_revenue.index,
            title="Revenue Distribution by Segment"
        )
        st.plotly_chart(fig_segment, use_container_width=True)
    
    # Time series analysis
    st.subheader("📅 Revenue Trends Over Time")
    monthly_revenue = df.groupby(df['OrderDate'].dt.to_period('M'))['Revenue'].sum()
    monthly_revenue.index = monthly_revenue.index.to_timestamp()
    
    fig_time = px.line(
        x=monthly_revenue.index,
        y=monthly_revenue.values,
        title="Monthly Revenue Trend",
        labels={'x': 'Month', 'y': 'Revenue ($)'}
    )
    fig_time.update_traces(line_color='#1f77b4', line_width=3)
    st.plotly_chart(fig_time, use_container_width=True)
    
    # Category and Channel Analysis
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🛍️ Revenue by Category")
        category_revenue = df.groupby('Category')['Revenue'].sum().sort_values(ascending=True)
        fig_category = px.bar(
            x=category_revenue.values,
            y=category_revenue.index,
            orientation='h',
            title="Revenue by Category",
            labels={'x': 'Revenue ($)', 'y': 'Category'},
            color=category_revenue.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col4:
        st.subheader("📱 Revenue by Channel")
        channel_revenue = df.groupby('Channel')['Revenue'].sum()
        fig_channel = px.bar(
            x=channel_revenue.index,
            y=channel_revenue.values,
            title="Revenue by Channel",
            labels={'x': 'Channel', 'y': 'Revenue ($)'},
            color=channel_revenue.values,
            color_continuous_scale='Plasma'
        )
        st.plotly_chart(fig_channel, use_container_width=True)
    
    # Advanced Analytics
    st.subheader("🔍 Advanced Analytics")
    
    col5, col6 = st.columns(2)
    
    with col5:
        # Top performing subcategories
        st.write("**Top 10 Subcategories by Revenue**")
        top_subcategories = df.groupby('Subcategory')['Revenue'].sum().sort_values(ascending=False).head(10)
        fig_sub = px.bar(
            x=top_subcategories.values,
            y=top_subcategories.index,
            orientation='h',
            title="Top Subcategories",
            color=top_subcategories.values,
            color_continuous_scale='RdYlBu'
        )
        st.plotly_chart(fig_sub, use_container_width=True)
    
    with col6:
        # Payment method analysis
        st.write("**Revenue by Payment Method**")
        payment_revenue = df.groupby('PaymentMethod')['Revenue'].sum().sort_values(ascending=False)
        fig_payment = px.pie(
            values=payment_revenue.values,
            names=payment_revenue.index,
            title="Payment Method Distribution"
        )
        st.plotly_chart(fig_payment, use_container_width=True)
    
    # Correlation heatmap
    st.subheader("🔥 Correlation Analysis")
    numeric_cols = ['Quantity', 'UnitPrice', 'DiscountPct', 'Revenue', 'Profit']
    correlation_matrix = df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        correlation_matrix,
        title="Correlation Matrix of Numeric Variables",
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

def create_data_table(df):
    """Create interactive data table"""
    st.subheader("📋 Detailed Data Table")
    
    # Add search functionality
    search_term = st.text_input("🔍 Search in data:", "")
    
    if search_term:
        # Search across multiple columns
        search_columns = ['Country', 'City', 'Category', 'Subcategory', 'PaymentMethod', 'Carrier']
        mask = df[search_columns].astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        display_df = df[mask]
    else:
        display_df = df
    
    # Column selection
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect(
        "Select columns to display:",
        all_columns,
        default=['OrderID', 'OrderDate', 'Country', 'Category', 'Subcategory', 'Quantity', 'Revenue']
    )
    
    if selected_columns:
        # Sort options
        sort_column = st.selectbox("Sort by:", selected_columns, index=0)
        sort_order = st.radio("Sort order:", ["Ascending", "Descending"], horizontal=True)
        
        # Apply sorting
        ascending = sort_order == "Ascending"
        display_df = display_df.sort_values(by=sort_column, ascending=ascending)
        
        # Display the table
        st.dataframe(
            display_df[selected_columns],
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = display_df[selected_columns].to_csv(index=False)
        st.download_button(
            label="📥 Download filtered data as CSV",
            data=csv,
            file_name=f"sales_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def main():
    """Main application function"""
    # Load data
    df = load_data()
    
    if df.empty:
        st.error("No data available. Please check the data file.")
        return
    
    # Create filters
    filters = create_filters(df)
    
    # Apply filters
    filtered_df = apply_filters(df, filters)
    
    # Show filtered data info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Filtered Results:** {len(filtered_df)} orders")
    st.sidebar.markdown(f"**Total Revenue:** ${filtered_df['Revenue'].sum():,.0f}")
    
    # Create KPI metrics
    create_kpi_metrics(filtered_df)
    
    # Add tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📊 Visualizations", "📋 Data Table", "📈 Summary Stats"])
    
    with tab1:
        create_visualizations(filtered_df)
    
    with tab2:
        create_data_table(filtered_df)
    
    with tab3:
        st.subheader("📈 Summary Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Revenue Statistics**")
            st.write(filtered_df['Revenue'].describe())
            
            st.write("**Quantity Statistics**")
            st.write(filtered_df['Quantity'].describe())
        
        with col2:
            st.write("**Order Distribution by Country**")
            country_counts = filtered_df['Country'].value_counts()
            st.write(country_counts)
            
            st.write("**Order Distribution by Segment**")
            segment_counts = filtered_df['Segment'].value_counts()
            st.write(segment_counts)

if __name__ == "__main__":
    main()
