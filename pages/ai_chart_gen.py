import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ====== PAGE CONFIG ======
st.set_page_config(page_title="Button Sandbox", layout="wide")

st.title("🧪 Button + Dynamic Content Sandbox")
st.markdown("Testing different approaches to make buttons work with dynamic chart content")

# ====== SAMPLE DATA CREATION ======
st.markdown("---")
st.header("📊 Step 1: Create Sample Data")

# Initialize session state
if "sample_data" not in st.session_state:
    st.session_state.sample_data = None

if st.button("🎯 Generate Top 5 Customers Data", type="primary"):
    # Create sample data that mimics your real data
    sample_data = {
        'customer_name': ['Acme Corp', 'Global Foods', 'Mega Buyer', 'Local Market', 'Prime Trading'],
        'sale_amount': [150000, 125000, 200000, 85000, 110000],
        'final_tons_sold': [500, 420, 680, 280, 370],
        'warehouse_region': ['North', 'South', 'East', 'West', 'Central']
    }
    st.session_state.sample_data = pd.DataFrame(sample_data)
    st.success("✅ Sample data created!")

# Display data if it exists
if st.session_state.sample_data is not None:
    st.dataframe(st.session_state.sample_data, use_container_width=True)

# ====== APPROACH 1: SESSION STATE + STABLE DISPLAY ======
st.markdown("---")
st.header("🔬 Approach 1: Session State + Persistent Display")

if st.session_state.sample_data is not None:
    
    # Initialize chart state
    if "chart_created" not in st.session_state:
        st.session_state.chart_created = False
    if "chart_color" not in st.session_state:
        st.session_state.chart_color = "blue"
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**Chart Controls:**")
        
        # Create chart button
        if st.button("📈 Create Chart", key="create_chart_1"):
            st.session_state.chart_created = True
        
        # Color selection (only show if chart exists)
        if st.session_state.chart_created:
            st.markdown("**Change Colors:**")
            
            # Method 1: Buttons for colors
            color_cols = st.columns(3)
            with color_cols[0]:
                if st.button("🔴 Red", key="red_1"):
                    st.session_state.chart_color = "red"
            with color_cols[1]:
                if st.button("🔵 Blue", key="blue_1"):
                    st.session_state.chart_color = "blue"
            with color_cols[2]:
                if st.button("🟢 Green", key="green_1"):
                    st.session_state.chart_color = "green"
            
            # Method 2: Dropdown (alternative)
            color_map = {
                "Blue Theme": "blues",
                "Red Theme": "reds", 
                "Green Theme": "greens",
                "Purple Theme": "purples",
                "Orange Theme": "oranges"
            }
            
            selected_theme = st.selectbox(
                "Or pick a color theme:",
                options=list(color_map.keys()),
                key="theme_select_1"
            )
            
            if st.button("🎨 Apply Theme", key="apply_theme_1"):
                st.session_state.chart_color = color_map[selected_theme]
    
    with col2:
        # Display chart if it should be shown
        if st.session_state.chart_created:
            st.markdown(f"**Chart with {st.session_state.chart_color} colors:**")
            
            # Create chart with current color
            if st.session_state.chart_color in ["red", "blue", "green"]:
                fig = px.bar(
                    st.session_state.sample_data, 
                    x='customer_name', 
                    y='sale_amount',
                    title="Sales by Customer",
                    color_discrete_sequence=[st.session_state.chart_color] * 5
                )
            else:
                # Use color scale for themes
                fig = px.bar(
                    st.session_state.sample_data, 
                    x='customer_name', 
                    y='sale_amount',
                    title="Sales by Customer",
                    color='sale_amount',
                    color_continuous_scale=st.session_state.chart_color
                )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show current state for debugging
            st.info(f"Current color: {st.session_state.chart_color}")

# ====== APPROACH 2: FORM-BASED APPROACH ======
st.markdown("---")
st.header("🔬 Approach 2: Form-Based Approach")

if st.session_state.sample_data is not None:
    
    with st.form("chart_form"):
        st.markdown("**Create Chart with Form:**")
        
        chart_type = st.selectbox("Chart Type:", ["Bar", "Pie", "Scatter"])
        
        color_option = st.selectbox("Color Scheme:", [
            "Blue", "Red", "Green", "Rainbow", "Viridis", "Plasma"
        ])
        
        submitted = st.form_submit_button("🚀 Create/Update Chart")
        
        if submitted:
            st.markdown(f"**{chart_type} Chart with {color_option} colors:**")
            
            if chart_type == "Bar":
                if color_option == "Rainbow":
                    colors = ['red', 'orange', 'yellow', 'green', 'blue']
                elif color_option == "Blue":
                    colors = ['lightblue', 'blue', 'darkblue', 'navy', 'midnightblue']
                elif color_option == "Red":
                    colors = ['lightcoral', 'red', 'darkred', 'maroon', 'crimson']
                elif color_option == "Green":
                    colors = ['lightgreen', 'green', 'darkgreen', 'forestgreen', 'darkseagreen']
                else:
                    colors = None
                
                fig = px.bar(
                    st.session_state.sample_data,
                    x='customer_name',
                    y='sale_amount',
                    title=f"Sales by Customer ({color_option} Theme)",
                    color='customer_name' if colors is None else None,
                    color_discrete_sequence=colors,
                    color_continuous_scale=color_option.lower() if colors is None else None
                )
            
            elif chart_type == "Pie":
                fig = px.pie(
                    st.session_state.sample_data,
                    values='sale_amount',
                    names='customer_name',
                    title=f"Sales Distribution ({color_option} Theme)",
                    color_discrete_sequence=px.colors.qualitative.Set3 if color_option == "Rainbow" else None
                )
            
            else:  # Scatter
                fig = px.scatter(
                    st.session_state.sample_data,
                    x='final_tons_sold',
                    y='sale_amount',
                    color='customer_name',
                    title=f"Sales vs Tons ({color_option} Theme)",
                    size='sale_amount'
                )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# ====== APPROACH 3: COLUMNS + REAL-TIME UPDATES ======
st.markdown("---")
st.header("🔬 Approach 3: Columns + Real-Time Updates")

if st.session_state.sample_data is not None:
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Live Chart Controls:**")
        
        # These create immediate updates
        live_chart_type = st.radio("Chart Type:", ["bar", "pie", "line"])
        
        live_color_scheme = st.selectbox("Color Palette:", [
            "default", "reds", "blues", "greens", "viridis", "plasma", "rainbow"
        ], key="live_colors")
        
        show_values = st.checkbox("Show Values on Chart")
        
        chart_height = st.slider("Chart Height:", 300, 600, 400)
    
    with col2:
        st.markdown("**Live Preview:**")
        
        # Chart updates automatically when controls change
        if live_chart_type == "bar":
            if live_color_scheme == "rainbow":
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
            elif live_color_scheme == "default":
                colors = px.colors.qualitative.Set1
            else:
                colors = None
            
            fig = px.bar(
                st.session_state.sample_data,
                x='customer_name',
                y='sale_amount',
                title="Live Bar Chart",
                color='sale_amount' if colors is None else 'customer_name',
                color_continuous_scale=live_color_scheme if colors is None else None,
                color_discrete_sequence=colors if colors else None,
                text='sale_amount' if show_values else None
            )
        
        elif live_chart_type == "pie":
            fig = px.pie(
                st.session_state.sample_data,
                values='sale_amount',
                names='customer_name',
                title="Live Pie Chart"
            )
            
            if live_color_scheme != "default":
                fig.update_traces(
                    marker=dict(colors=px.colors.sequential.__dict__.get(live_color_scheme.title(), px.colors.qualitative.Set1))
                )
        
        else:  # line
            fig = px.line(
                st.session_state.sample_data.sort_values('final_tons_sold'),
                x='final_tons_sold',
                y='sale_amount',
                title="Live Line Chart",
                markers=True
            )
        
        fig.update_layout(height=chart_height)
        if show_values and live_chart_type == "bar":
            fig.update_traces(texttemplate='%{text}', textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)

# ====== APPROACH 4: AI-POWERED RECOMMENDATIONS ======
st.markdown("---")
st.header("🔬 Approach 4: AI-Powered Chart Recommendations")

if st.session_state.sample_data is not None:
    
    # Initialize AI state
    if "ai_recommendation" not in st.session_state:
        st.session_state.ai_recommendation = None
    
    if st.button("🤖 Get AI Chart Recommendation", type="primary"):
        # Simulate AI analysis
        data = st.session_state.sample_data
        
        # Simple AI logic (can be replaced with real AI later)
        num_rows = len(data)
        has_categories = data['customer_name'].dtype == 'object'
        has_numbers = len(data.select_dtypes(include=['number']).columns) > 0
        
        if has_categories and has_numbers and num_rows <= 8:
            recommendation = {
                "chart_type": "pie",
                "reasoning": "Pie chart works well for showing distribution across few categories",
                "color_scheme": "Set3",
                "x_col": "customer_name",
                "y_col": "sale_amount"
            }
        elif has_categories and has_numbers:
            recommendation = {
                "chart_type": "bar",
                "reasoning": "Bar chart is ideal for comparing values across categories",
                "color_scheme": "viridis",
                "x_col": "customer_name", 
                "y_col": "sale_amount"
            }
        else:
            recommendation = {
                "chart_type": "scatter",
                "reasoning": "Scatter plot shows relationships between numeric variables",
                "color_scheme": "plasma",
                "x_col": "final_tons_sold",
                "y_col": "sale_amount"
            }
        
        st.session_state.ai_recommendation = recommendation
        st.success("🤖 AI analysis complete!")
    
    # Display AI recommendation if available
    if st.session_state.ai_recommendation:
        rec = st.session_state.ai_recommendation
        
        st.info(f"🤖 **AI Recommends:** {rec['chart_type'].title()} Chart - {rec['reasoning']}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button("✨ Create AI Recommended Chart"):
                st.session_state.show_ai_chart = True
            
            # Allow user to override AI colors
            override_colors = st.checkbox("Override AI Color Choice")
            if override_colors:
                user_color = st.selectbox("Your Color Choice:", [
                    "reds", "blues", "greens", "viridis", "plasma", "rainbow"
                ])
                rec["color_scheme"] = user_color
        
        with col2:
            if st.session_state.get("show_ai_chart", False):
                # Create the AI recommended chart
                if rec["chart_type"] == "bar":
                    fig = px.bar(
                        st.session_state.sample_data,
                        x=rec["x_col"],
                        y=rec["y_col"], 
                        title="AI Recommended Bar Chart",
                        color=rec["y_col"],
                        color_continuous_scale=rec["color_scheme"]
                    )
                elif rec["chart_type"] == "pie":
                    fig = px.pie(
                        st.session_state.sample_data,
                        values=rec["y_col"],
                        names=rec["x_col"],
                        title="AI Recommended Pie Chart",
                        color_discrete_sequence=getattr(px.colors.qualitative, rec["color_scheme"], px.colors.qualitative.Set3)
                    )
                else:  # scatter
                    fig = px.scatter(
                        st.session_state.sample_data,
                        x=rec["x_col"],
                        y=rec["y_col"],
                        title="AI Recommended Scatter Plot",
                        color=rec["y_col"],
                        color_continuous_scale=rec["color_scheme"]
                    )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

# ====== SUMMARY & FINDINGS ======
st.markdown("---")
st.header("📝 Testing Summary")

st.markdown("""
**🔬 Experiment Results:**

1. **Approach 1 (Session State + Buttons):** 
   - ✅ Works but requires careful state management
   - ✅ Good for simple color changes
   - ⚠️ Can be complex with multiple states

2. **Approach 2 (Forms):**
   - ✅ Most reliable - prevents rerun issues
   - ✅ Great for complex configurations
   - ❌ Less interactive (requires submit)

3. **Approach 3 (Live Controls):**
   - ✅ Most user-friendly - immediate updates
   - ✅ Perfect for real-time previews
   - ✅ No rerun issues with selectbox/slider

4. **Approach 4 (AI + Manual Override):**
   - ✅ Best of both worlds
   - ✅ AI recommendations + user control
   - ✅ Works reliably with session state

**🎯 Best for Your Main App:** Combination of Approach 3 (live controls) + Approach 4 (AI recommendations)
""")

# Reset button for testing
if st.button("🔄 Reset All Tests"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()