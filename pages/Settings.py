import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import ai_query_assistant
import random
from datetime import datetime

# ====== PAGE CONFIG ======
st.set_page_config(page_title="Settings", layout="wide")

# ====== STYLING ======
st.markdown("""
<style>
/* Main container styling */
.ai-query-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    color: white;
}

.ai-query-header {
    text-align: center;
    margin-bottom: 2rem;
}

.ai-query-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    background: linear-gradient(45deg, #FFD700, #FFA500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.ai-query-subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
    margin-bottom: 1rem;
}

/* Stats cards */
.stats-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin: 0.5rem;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

/* SQL display */
.sql-display {
    background: #f8f9fa;
    border-left: 4px solid #667eea;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ====== HEADER ======
st.markdown("""
<div class="ai-query-container">
    <div class="ai-query-header">
        <h1 class="ai-query-title">🤖 Settings ( Admin / Basic / Guest )</h1>
        <p style="font-size: 0.9rem; opacity: 0.7; margin-bottom: 1rem; font-style: italic;">
            Compiled by <strong>Datavue</strong> • Powered by OpenAI
        </p>
        <p class="ai-query-subtitle">Change key dashboard settings</p>
    </div>
</div>
""", unsafe_allow_html=True)

# # ====== EXAMPLE PROMPTS ======
# st.markdown("### 💡 **Try These Example Questions:**")
# examples = [
#     "💰 What are our total sales this year?",
#     "🏆 Show me top 10 customers by revenue", 
#     "📊 Which products sell best?",
#     "🌍 Sales breakdown by region",
#     "📈 Monthly revenue trends",
#     "⭐ Customers with high satisfaction",
#     "🎯 Export vs Local sales comparison",
#     "📦 Average order size by category",
#     "💎 Premium customers (>$100k revenue)",
#     "🔍 Sales in Northern region"
# ]

# cols = st.columns(5)
# for i, example in enumerate(examples):
#     with cols[i % 5]:
#         if st.button(example, key=f"example_{i}"):
#             st.session_state.query_input = example.split(' ', 1)[1]  # Remove emoji
#             st.rerun()

# st.markdown("---")

# # ====== QUERY INPUT ======
# st.markdown("### 🎯 **Ask Your Question:**")

# # Get input value
# query_value = ""
# if 'query_input' in st.session_state:
#     query_value = st.session_state.query_input
#     del st.session_state.query_input  # Clear after using

# user_question = st.text_input(
#     "Type your question here:",
#     value=query_value,
#     placeholder="e.g., What are the top 5 customers by revenue this year?",
#     label_visibility="collapsed"
# )

# # Ask AI button
# ask_button = st.button("🚀 Ask AI", type="primary", use_container_width=True)

# # ====== QUERY EXECUTION ======
# if ask_button and user_question.strip():
#     print("Button pressed.")
    
#     with st.spinner("🤖 Processing your query..."):
        
#         # Execute query
#         try:
#             assistant = ai_query_assistant.AIQueryAssistant()
#             result = assistant.query(user_question, verbose=False)
            
#             if result['error']:
#                 st.error(f"❌ **Query Failed:** {result['error']}")
                
#                 # Show SQL in expanded state if there's an error
#                 if result['sql']:
#                     st.markdown("### 🔧 **Generated SQL (Failed):**")
#                     st.markdown(f"""
#                     <div class="sql-display">
#                         <code>{result['sql']}</code>
#                     </div>
#                     """, unsafe_allow_html=True)
                
#             else:
#                 # SUCCESS - Show results
#                 df_result = result['result']
                
#                 st.success(f"✅ **Query Successful!** Found {len(df_result)} results")
                
#                 # Quick stats
#                 if len(df_result) > 0:
#                     col1, col2, col3, col4 = st.columns(4)
                    
#                     with col1:
#                         st.markdown(f"""
#                         <div class="stats-card">
#                             <h4>📊 Rows</h4>
#                             <h2>{len(df_result)}</h2>
#                         </div>
#                         """, unsafe_allow_html=True)
                    
#                     with col2:
#                         st.markdown(f"""
#                         <div class="stats-card">
#                             <h4>📋 Columns</h4>
#                             <h2>{len(df_result.columns)}</h2>
#                         </div>
#                         """, unsafe_allow_html=True)
                    
#                     with col3:
#                         # Find total value if sale_amount exists
#                         if 'sale_amount' in df_result.columns:
#                             total_value = df_result['sale_amount'].sum()
#                             st.markdown(f"""
#                             <div class="stats-card">
#                                 <h4>💰 Total Value</h4>
#                                 <h2>${total_value:,.0f}</h2>
#                             </div>
#                             """, unsafe_allow_html=True)
#                         else:
#                             st.markdown(f"""
#                             <div class="stats-card">
#                                 <h4>🔢 Data Type</h4>
#                                 <h2>Mixed</h2>
#                             </div>
#                             """, unsafe_allow_html=True)
                    
#                     with col4:
#                         st.markdown(f"""
#                         <div class="stats-card">
#                             <h4>⚡ Query Time</h4>
#                             <h2>< 1s</h2>
#                         </div>
#                         """, unsafe_allow_html=True)
                
#                 # SQL Query (collapsed by default)
#                 with st.expander("🔧 **View Generated SQL Query**"):
#                     st.markdown(f"""
#                     <div class="sql-display">
#                         <strong>Generated SQL:</strong><br>
#                         <code>{result['sql']}</code>
#                     </div>
#                     """, unsafe_allow_html=True)
                
#                 # Show results table
#                 st.markdown("### 📋 **Query Results:**")
#                 st.dataframe(df_result, use_container_width=True)
                
#                 # Download CSV
#                 csv = df_result.to_csv(index=False)
#                 st.download_button(
#                     label="📥 Download Results as CSV",
#                     data=csv,
#                     file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
#                     mime="text/csv"
#                 )
                
#                 # ====== CHART GENERATION LOGIC ======
                
#                 # Check if data is suitable for charting
#                 can_chart = False
#                 chart_reason = ""

#                 if len(df_result) <= 1:
#                     chart_reason = "Need at least 2 rows of data for charts"
#                 elif len(df_result.columns) < 2:
#                     chart_reason = "Need at least 2 columns for charts"
#                 else:
#                     # Check for numeric columns
#                     numeric_cols = df_result.select_dtypes(include=[np.number]).columns
#                     categorical_cols = df_result.select_dtypes(include=['object', 'category']).columns
                    
#                     if len(numeric_cols) > 0 and len(categorical_cols) > 0:
#                         can_chart = True
#                     elif len(numeric_cols) >= 2:
#                         can_chart = True
#                     elif len(categorical_cols) > 0:
#                         can_chart = True
#                     else:
#                         chart_reason = "No suitable column combinations for charts"

#                 if can_chart:
#                     st.markdown("---")
#                     st.markdown("### 🎨 **Auto-Generated Charts**")
                    
#                     # Analyze data for smart charting
#                     numeric_cols = list(df_result.select_dtypes(include=[np.number]).columns)
#                     categorical_cols = list(df_result.select_dtypes(include=['object', 'category']).columns)
                    
#                     # Determine best columns for charting
#                     chart_x = ""
#                     chart_y = ""
                    
#                     if len(categorical_cols) > 0 and len(numeric_cols) > 0:
#                         chart_x = categorical_cols[0]
#                         chart_y = numeric_cols[0]
#                     elif len(numeric_cols) >= 2:
#                         chart_x = numeric_cols[0]
#                         chart_y = numeric_cols[1]
#                     else:
#                         chart_x = df_result.columns[0]
#                         chart_y = df_result.columns[1] if len(df_result.columns) > 1 else df_result.columns[0]
                    
#                     st.info(f"🤖 **AI Analysis:** Using {chart_x} (X-axis) vs {chart_y} (Y-axis) for visualization")
                    
#                     # Create charts immediately - no buttons, no reruns!
#                     try:
#                         # Chart 1: Bar Chart
#                         st.markdown("#### 📊 **Bar Chart**")
#                         if chart_x == chart_y and df_result[chart_x].dtype == 'object':
#                             # Count occurrences
#                             value_counts = df_result[chart_x].value_counts().reset_index()
#                             value_counts.columns = [chart_x, 'count']
#                             fig_bar = px.bar(value_counts, x=chart_x, y='count', 
#                                         title=f"Distribution of {chart_x}")
#                         else:
#                             fig_bar = px.bar(df_result, x=chart_x, y=chart_y,
#                                         title=f"{chart_y} by {chart_x}")
                        
#                         fig_bar.update_layout(
#                             plot_bgcolor='rgba(244, 246, 251, 0.9)',
#                             paper_bgcolor='rgba(244, 246, 251, 0.9)',
#                             font=dict(family="Segoe UI", size=12, color="#1F2B3A"),
#                             height=400
#                         )
#                         st.plotly_chart(fig_bar, use_container_width=True)
                        
#                         # Download bar chart
#                         bar_html = fig_bar.to_html()
#                         st.download_button(
#                             label="📥 Save Bar Chart",
#                             data=bar_html,
#                             file_name=f"bar_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
#                             mime="text/html",
#                             key="download_bar"
#                         )
                        
#                         # Chart 2: Pie Chart (if suitable)
#                         if len(categorical_cols) > 0 and len(numeric_cols) > 0 and len(df_result) <= 15:
#                             st.markdown("#### 🥧 **Pie Chart**")
#                             fig_pie = px.pie(df_result, values=chart_y, names=chart_x,
#                                         title=f"{chart_y} Distribution by {chart_x}")
#                             fig_pie.update_layout(height=400)
#                             st.plotly_chart(fig_pie, use_container_width=True)
                            
#                             # Download pie chart
#                             pie_html = fig_pie.to_html()
#                             st.download_button(
#                                 label="📥 Save Pie Chart",
#                                 data=pie_html,
#                                 file_name=f"pie_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
#                                 mime="text/html",
#                                 key="download_pie"
#                             )
                        
#                         # Chart 3: Line Chart
#                         st.markdown("#### 📈 **Line Chart**")
#                         df_sorted = df_result.sort_values(chart_x)
#                         fig_line = px.line(df_sorted, x=chart_x, y=chart_y,
#                                         title=f"{chart_y} Trend over {chart_x}")
#                         fig_line.update_layout(
#                             plot_bgcolor='rgba(244, 246, 251, 0.9)',
#                             paper_bgcolor='rgba(244, 246, 251, 0.9)',
#                             font=dict(family="Segoe UI", size=12, color="#1F2B3A"),
#                             height=400
#                         )
#                         st.plotly_chart(fig_line, use_container_width=True)
                        
#                         # Download line chart
#                         line_html = fig_line.to_html()
#                         st.download_button(
#                             label="📥 Save Line Chart",
#                             data=line_html,
#                             file_name=f"line_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
#                             mime="text/html",
#                             key="download_line"
#                         )
                        
#                         # Chart 4: Scatter Plot (if we have 2+ numeric columns)
#                         if len(numeric_cols) >= 2:
#                             st.markdown("#### 🔵 **Scatter Plot**")
#                             fig_scatter = px.scatter(df_result, x=numeric_cols[0], y=numeric_cols[1],
#                                                 title=f"{numeric_cols[1]} vs {numeric_cols[0]}")
#                             fig_scatter.update_layout(
#                                 plot_bgcolor='rgba(244, 246, 251, 0.9)',
#                                 paper_bgcolor='rgba(244, 246, 251, 0.9)',
#                                 font=dict(family="Segoe UI", size=12, color="#1F2B3A"),
#                                 height=400
#                             )
#                             st.plotly_chart(fig_scatter, use_container_width=True)
                            
#                             # Download scatter chart
#                             scatter_html = fig_scatter.to_html()
#                             st.download_button(
#                                 label="📥 Save Scatter Plot",
#                                 data=scatter_html,
#                                 file_name=f"scatter_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
#                                 mime="text/html",
#                                 key="download_scatter"
#                             )
                        
#                     except Exception as e:
#                         st.error(f"Chart creation failed: {e}")
#                         st.info(f"Data preview: {df_result.head()}")

#                 else:
#                     st.info(f"📊 Chart generation not available: {chart_reason}")

                    
#                 # can_chart = False
#                 # chart_reason = ""
                
#                 # if len(df_result) <= 1:
#                 #     chart_reason = "Need at least 2 rows of data for charts"
#                 # elif len(df_result.columns) < 2:
#                 #     chart_reason = "Need at least 2 columns for charts"
#                 # else:
#                 #     # Check for numeric columns
#                 #     numeric_cols = df_result.select_dtypes(include=[np.number]).columns
#                 #     categorical_cols = df_result.select_dtypes(include=['object', 'category']).columns
                    
#                 #     if len(numeric_cols) > 0 and len(categorical_cols) > 0:
#                 #         can_chart = True
#                 #     elif len(numeric_cols) >= 2:
#                 #         can_chart = True
#                 #     elif len(categorical_cols) > 0:
#                 #         can_chart = True
#                 #     else:
#                 #         chart_reason = "No suitable column combinations for charts"
                
#                 # if can_chart:
#                 #     st.markdown("---")
#                 #     st.markdown("### 🎨 **Chart Generation**")
                    
#                 #     # Analyze data for AI recommendation
#                 #     numeric_cols = list(df_result.select_dtypes(include=[np.number]).columns)
#                 #     categorical_cols = list(df_result.select_dtypes(include=['object', 'category']).columns)
                    
#                 #     # AI Chart Recommendation Logic
#                 #     recommended_chart = "bar"
#                 #     recommended_x = ""
#                 #     recommended_y = ""
#                 #     ai_reasoning = ""
                    
#                 #     if len(categorical_cols) > 0 and len(numeric_cols) > 0:
#                 #         # Category vs Numeric - Best for bar/pie
#                 #         recommended_chart = "bar"
#                 #         recommended_x = categorical_cols[0]
#                 #         recommended_y = numeric_cols[0]
#                 #         ai_reasoning = f"Bar chart works well for comparing {recommended_y} across different {recommended_x}"
                        
#                 #         # If many categories, suggest pie chart
#                 #         if len(df_result) <= 8:
#                 #             recommended_chart = "pie"
#                 #             ai_reasoning = f"Pie chart shows {recommended_y} distribution across {recommended_x} categories"
                    
#                 #     elif len(numeric_cols) >= 2:
#                 #         # Two numeric columns - scatter or line
#                 #         recommended_chart = "scatter"
#                 #         recommended_x = numeric_cols[0]
#                 #         recommended_y = numeric_cols[1]
#                 #         ai_reasoning = f"Scatter plot shows relationship between {recommended_x} and {recommended_y}"
                    
#                 #     else:
#                 #         # Fallback to bar
#                 #         recommended_chart = "bar"
#                 #         recommended_x = df_result.columns[0]
#                 #         recommended_y = df_result.columns[1] if len(df_result.columns) > 1 else df_result.columns[0]
#                 #         ai_reasoning = "Bar chart for general data visualization"
                    
#                 #     # AI Recommendation Button
#                 #     st.info(f"🤖 **AI Recommends:** {recommended_chart.title()} Chart - {ai_reasoning}")
                    
#                 #     if st.button(f"✨ Create AI Recommended {recommended_chart.title()} Chart", type="primary"):
#                 #         print("Button pressed.")
                        
#                 #         # Create the recommended chart
#                 #         try:
#                 #             print("Creating chart.")
#                 #             if recommended_chart == "bar":
#                 #                 if recommended_x == recommended_y:
#                 #                     # Count occurrences
#                 #                     value_counts = df_result[recommended_x].value_counts().reset_index()
#                 #                     value_counts.columns = [recommended_x, 'count']
#                 #                     fig = px.bar(value_counts, x=recommended_x, y='count', 
#                 #                                title=f"Distribution of {recommended_x}")
#                 #                 else:
#                 #                     fig = px.bar(df_result, x=recommended_x, y=recommended_y,
#                 #                                title=f"{recommended_y} by {recommended_x}")
                            
#                 #             elif recommended_chart == "pie":
#                 #                 fig = px.pie(df_result, values=recommended_y, names=recommended_x,
#                 #                            title=f"{recommended_y} by {recommended_x}")
                            
#                 #             elif recommended_chart == "scatter":
#                 #                 fig = px.scatter(df_result, x=recommended_x, y=recommended_y,
#                 #                                title=f"{recommended_y} vs {recommended_x}")
                            
#                 #             else:
#                 #                 print("ELSE OPTION")
#                 #                 fig = px.line(df_result, x=recommended_x, y=recommended_y,
#                 #                             title=f"{recommended_y} over {recommended_x}")
                            
#                 #             # Style the chart
#                 #             fig.update_layout(
#                 #                 plot_bgcolor='rgba(244, 246, 251, 0.9)',
#                 #                 paper_bgcolor='rgba(244, 246, 251, 0.9)',
#                 #                 font=dict(family="Segoe UI", size=12, color="#1F2B3A"),
#                 #                 height=500
#                 #             )
                            
#                 #             # Display chart
#                 #             st.plotly_chart(fig, use_container_width=True)
                            
#                 #             # Download chart
#                 #             chart_html = fig.to_html()
#                 #             st.download_button(
#                 #                 label="📥 Save Chart as HTML",
#                 #                 data=chart_html,
#                 #                 file_name=f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
#                 #                 mime="text/html"
#                 #             )
                            
#                 #         except Exception as e:
#                 #             st.error(f"Chart creation failed: {e}")
                    
#                 #     # Manual Chart Options
#                 #     st.markdown("---")
#                 #     st.markdown("#### 🛠️ **Or Choose Your Own Chart:**")
                    
#                 #     manual_col1, manual_col2, manual_col3, manual_col4 = st.columns(4)
                    
#                 #     with manual_col1:
#                 #         if st.button("📊 Bar Chart"):
#                 #             fig = px.bar(df_result, x=df_result.columns[0], y=df_result.columns[1] if len(df_result.columns) > 1 else df_result.columns[0])
#                 #             fig.update_layout(height=500)
#                 #             st.plotly_chart(fig, use_container_width=True)
                    
#                 #     with manual_col2:
#                 #         if st.button("🥧 Pie Chart") and len(numeric_cols) > 0 and len(categorical_cols) > 0:
#                 #             fig = px.pie(df_result, values=numeric_cols[0], names=categorical_cols[0])
#                 #             fig.update_layout(height=500)
#                 #             st.plotly_chart(fig, use_container_width=True)
                    
#                 #     with manual_col3:
#                 #         if st.button("📈 Line Chart"):
#                 #             fig = px.line(df_result, x=df_result.columns[0], y=df_result.columns[1] if len(df_result.columns) > 1 else df_result.columns[0])
#                 #             fig.update_layout(height=500)
#                 #             st.plotly_chart(fig, use_container_width=True)
                    
#                 #     with manual_col4:
#                 #         if st.button("🔵 Scatter Plot") and len(numeric_cols) >= 2:
#                 #             fig = px.scatter(df_result, x=numeric_cols[0], y=numeric_cols[1])
#                 #             fig.update_layout(height=500)
#                 #             st.plotly_chart(fig, use_container_width=True)
                
#                 # else:
#                 #     st.info(f"📊 Chart generation not available: {chart_reason}")
                
#                 # ====== QUERY HISTORY ======
#                 if 'query_history' not in st.session_state:
#                     st.session_state.query_history = []
                
#                 # Add to history
#                 if user_question not in [q['question'] for q in st.session_state.query_history]:
#                     st.session_state.query_history.append({
#                         'question': user_question,
#                         'timestamp': datetime.now().strftime('%H:%M:%S'),
#                         'rows': len(df_result)
#                     })
                    
#                     # Keep only last 5 queries
#                     if len(st.session_state.query_history) > 5:
#                         st.session_state.query_history.pop(0)
        
#         except Exception as e:
#             st.error(f"❌ An error occurred: {str(e)}")

# elif ask_button and not user_question.strip():
#     st.warning("⚠️ Please enter a question before asking AI!")

# # ====== QUERY HISTORY DISPLAY ======
# if 'query_history' in st.session_state and st.session_state.query_history:
#     st.markdown("---")
#     st.markdown("### 📝 **Recent Queries:**")
    
#     for i, query in enumerate(reversed(st.session_state.query_history)):
#         with st.expander(f"🕐 {query['timestamp']} - {query['question'][:50]}{'...' if len(query['question']) > 50 else ''}"):
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.write(f"**Question:** {query['question']}")
#                 st.write(f"**Results:** {query['rows']} rows")
#             with col2:
#                 if st.button("🔄 Run Again", key=f"rerun_{i}"):
#                     st.session_state.query_input = query['question']
#                     st.rerun()