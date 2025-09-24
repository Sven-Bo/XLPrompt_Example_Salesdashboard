# Sales Analytics Dashboard 📊

A comprehensive and interactive Streamlit dashboard for analyzing sales data with advanced filtering, visualizations, and KPI tracking.

## Features 🚀

### Key Performance Indicators (KPIs)
- **Total Revenue**: Complete revenue across all orders
- **Total Orders**: Number of orders processed
- **Average Order Value**: Mean revenue per order
- **Total Quantity**: Sum of all items sold
- **Total Profit**: Estimated profit (20% margin)
- **Average Discount**: Mean discount percentage applied

### Interactive Filters 🔍
- **Date Range**: Filter by specific date periods
- **Countries**: Multi-select country filter
- **Segments**: Filter by customer segments (Consumer, SMB, Enterprise)
- **Channels**: Filter by sales channels (Web, Mobile, SalesRep)
- **Categories**: Filter by product categories
- **Revenue Range**: Slider to filter by revenue amounts

### Visualizations 📈
- **Revenue by Country**: Bar chart showing revenue distribution
- **Revenue by Segment**: Pie chart of segment performance
- **Monthly Revenue Trends**: Time series line chart
- **Revenue by Category**: Horizontal bar chart
- **Revenue by Channel**: Channel performance comparison
- **Top Subcategories**: Top 10 performing subcategories
- **Payment Method Analysis**: Payment preference distribution
- **Correlation Matrix**: Heatmap of numeric variable relationships

### Data Analysis Tools 📋
- **Interactive Data Table**: Searchable and sortable data grid
- **Column Selection**: Choose which columns to display
- **Data Export**: Download filtered data as CSV
- **Summary Statistics**: Descriptive statistics for key metrics

## Installation & Setup 🛠️

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Data File
Ensure the JSON data file `XLPrompt_Output_2025-09-24_09-55-41.json` is in the same directory as `dashboard.py`.

### Step 3: Run the Dashboard
```bash
streamlit run dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Usage Guide 📖

### Getting Started
1. **Launch the Dashboard**: Run the Streamlit command above
2. **Explore KPIs**: View the top metrics banner for quick insights
3. **Apply Filters**: Use the sidebar filters to focus on specific data segments
4. **Navigate Tabs**: Switch between Visualizations, Data Table, and Summary Stats

### Filter Usage
- **Multiple Selections**: Most filters support multiple selections
- **"All" Option**: Select "All" to include all options for that filter
- **Real-time Updates**: All charts and metrics update automatically when filters change
- **Filter Combinations**: Combine multiple filters for detailed analysis

### Visualization Insights
- **Interactive Charts**: Hover over chart elements for detailed information
- **Zoom & Pan**: Use chart controls to zoom into specific areas
- **Color Coding**: Charts use color gradients to highlight performance differences

### Data Export
- **Filtered Export**: Download only the data matching your current filters
- **Column Selection**: Choose specific columns before export
- **CSV Format**: Data exports in standard CSV format for Excel compatibility

## Data Structure 📊

The dashboard analyzes sales order data with the following key fields:
- **OrderID**: Unique order identifier
- **OrderDate**: Date of the order
- **Country/City**: Geographic information
- **Segment**: Customer segment (Consumer, SMB, Enterprise)
- **Channel**: Sales channel (Web, Mobile, SalesRep)
- **Category/Subcategory**: Product classification
- **Quantity**: Number of items ordered
- **UnitPrice**: Price per unit
- **DiscountPct**: Discount percentage applied
- **Revenue**: Total order revenue
- **PaymentMethod**: Payment type used
- **Carrier**: Shipping carrier

## Technical Details 🔧

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computing

### Performance Features
- **Data Caching**: Uses Streamlit's caching for improved performance
- **Responsive Design**: Adapts to different screen sizes
- **Memory Efficient**: Optimized data processing

### Customization Options
- **Color Schemes**: Multiple color palettes for different chart types
- **Layout**: Wide layout for maximum screen utilization
- **Styling**: Custom CSS for professional appearance

## Troubleshooting 🔧

### Common Issues

**Dashboard won't start:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.7+)
- Ensure data file is in the correct location

**Data not loading:**
- Verify the JSON file name matches exactly: `XLPrompt_Output_2025-09-24_09-55-41.json`
- Check file permissions and accessibility
- Validate JSON format using an online JSON validator

**Performance issues:**
- Close other resource-intensive applications
- Try refreshing the browser page
- Restart the Streamlit server

**Charts not displaying:**
- Check browser compatibility (Chrome, Firefox, Safari recommended)
- Disable browser ad-blockers temporarily
- Clear browser cache and cookies

## Future Enhancements 🚀

Potential improvements for future versions:
- **Real-time Data**: Connect to live data sources
- **Advanced Analytics**: Machine learning predictions
- **Custom Reports**: Automated report generation
- **User Authentication**: Multi-user access control
- **Database Integration**: Connect to SQL databases
- **Mobile Optimization**: Enhanced mobile experience

## Support 💬

For questions or issues:
1. Check the troubleshooting section above
2. Verify your setup matches the installation guide
3. Review the Streamlit documentation for advanced features

---

**Created with ❤️ using Streamlit and Python**
