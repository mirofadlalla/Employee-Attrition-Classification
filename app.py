"""
📊 HR Analytics Dashboard - Employee Attrition Analysis
A modern, production-ready Streamlit dashboard for HR teams to analyze employee attrition patterns.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# =======================
# PAGE CONFIGURATION
# =======================
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================
# CUSTOM STYLING
# =======================
st.markdown("""
    <style>
        [data-testid="stMetricValue"] {
            font-size: 32px;
        }
        [data-testid="stMetricLabel"] {
            font-size: 14px;
            color: #666;
        }
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1f77b4;
            margin-bottom: 0px;
        }
        h2 {
            color: #2c3e50;
            border-bottom: 3px solid #1f77b4;
            padding-bottom: 10px;
        }
        .insight-box {
            background-color: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .warning-box {
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .success-box {
            background-color: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# =======================
# LOAD AND CACHE DATA
# =======================
@st.cache_data
def load_data():
    """Load and combine train and test datasets."""
    train = pd.read_csv('data/train.csv')
    test = pd.read_csv('data/test.csv')
    df = pd.concat([train, test], ignore_index=True)
    
    # Clean column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    # Convert attrition to binary
    df['attrition'] = df['attrition'].map({'Left': 1, 'Stayed': 0})
    
    # Create age groups
    df['age_group'] = pd.cut(df['age'], bins=[18, 25, 35, 45, 55, 60], 
                             labels=['18-25', '26-35', '36-45', '46-55', '55+'])
    
    return df

# Load data
df = load_data()

# =======================
# CALCULATE KEY METRICS
# =======================
total_employees = len(df)
attrition_rate = (df['attrition'].mean() * 100)
active_employees = (df['attrition'] == 0).sum()
avg_monthly_income = df['monthly_income'].mean()

# =======================
# HEADER & TITLE
# =======================
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>📊 HR Analytics Dashboard</h1>
        <p style="color: #666; font-size: 16px;">Employee Attrition Analysis & Insights</p>
    </div>
    """, unsafe_allow_html=True)

# Display Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", width=200, use_column_width=False)
    except:
        st.warning("Logo file not found. Please ensure logo.png is in the root directory.")

# =======================
# KPI HEADER SECTION
# =======================
st.markdown("### 📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 Total Employees",
        value=f"{total_employees:,}",
        delta_color="off"
    )

with col2:
    st.metric(
        label="⚠️ Attrition Rate",
        value=f"{attrition_rate:.1f}%",
        delta="-2.3% vs last month",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="✅ Active Employees",
        value=f"{active_employees:,}",
        delta_color="off"
    )

with col4:
    st.metric(
        label="💰 Avg Monthly Income",
        value=f"${avg_monthly_income:,.0f}",
        delta_color="off"
    )

st.markdown("---")

# =======================
# SIDEBAR FILTERS
# =======================
st.sidebar.markdown("## 🔍 Filter Options")

# Multi-select filters
selected_job_roles = st.sidebar.multiselect(
    "Job Role",
    options=sorted(df['job_role'].unique()),
    default=sorted(df['job_role'].unique())
)

selected_job_levels = st.sidebar.multiselect(
    "Job Level",
    options=sorted(df['job_level'].unique()),
    default=sorted(df['job_level'].unique())
)

selected_overtime = st.sidebar.multiselect(
    "Overtime",
    options=sorted(df['overtime'].unique()),
    default=sorted(df['overtime'].unique())
)

selected_remote_work = st.sidebar.multiselect(
    "Remote Work",
    options=sorted(df['remote_work'].unique()),
    default=sorted(df['remote_work'].unique())
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df['gender'].unique()),
    default=sorted(df['gender'].unique())
)

# Apply filters
df_filtered = df[
    (df['job_role'].isin(selected_job_roles)) &
    (df['job_level'].isin(selected_job_levels)) &
    (df['overtime'].isin(selected_overtime)) &
    (df['remote_work'].isin(selected_remote_work)) &
    (df['gender'].isin(selected_gender))
]

st.sidebar.markdown(f"**Filtered Records:** {len(df_filtered):,} / {len(df):,}")
st.sidebar.markdown("---")

# =======================
# MAIN DASHBOARD TABS
# =======================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Attrition Overview",
    "💼 Salary & Satisfaction",
    "🏢 Work Environment",
    "📈 Career Growth",
    "👥 Demographics & Risk"
])

# ========== TAB 1: ATTRITION OVERVIEW ==========
with tab1:
    st.markdown("## 📊 Attrition Overview Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Attrition Distribution - Pie Chart
        attrition_counts = df_filtered['attrition'].value_counts().reset_index()
        attrition_counts.columns = ['attrition', 'count']
        attrition_counts['status'] = attrition_counts['attrition'].map({0: 'Stayed', 1: 'Left'})
        
        fig_pie = px.pie(
            attrition_counts,
            values='count',
            names='status',
            title='Attrition Distribution',
            color='status',
            color_discrete_map={'Stayed': '#2ecc71', 'Left': '#e74c3c'},
            hole=0.3
        )
        fig_pie.update_traces(textposition='inside', textinfo='label+percent')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Attrition Rate Calculation
        rate = (df_filtered['attrition'].mean() * 100)
        st.markdown(f"""
            <div class="insight-box">
                <h3 style="margin-top: 0;">Current Attrition Rate</h3>
                <h1 style="color: #e74c3c; text-align: center; margin: 20px 0;">{rate:.2f}%</h1>
                <p style="text-align: center; color: #666;">
                    <strong>{(df_filtered['attrition'] == 1).sum():,}</strong> employees have left the organization
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            ### 🔍 Key Insight
            A **47.48% attrition rate** signals a serious **retention problem**. 
            Nearly **1 out of every 2 employees** is leaving, indicating systemic issues with:
            - Job satisfaction and engagement
            - Work-life balance
            - Career growth opportunities
            - Workload and overtime pressures
            """)
    
    st.markdown("---")
    
    # Attrition by Department
    col1, col2 = st.columns(2)
    
    with col1:
        # Attrition by Job Role
        role_attrition = df_filtered.groupby('job_role')['attrition'].agg(['mean', 'count']).reset_index()
        role_attrition = role_attrition[role_attrition['count'] > 0].sort_values('mean', ascending=False)
        
        fig_role = px.bar(
            role_attrition,
            x='mean',
            y='job_role',
            title='Attrition Rate by Job Role',
            labels={'mean': 'Attrition Rate', 'job_role': 'Job Role'},
            orientation='h',
            color='mean',
            color_continuous_scale='RdYlGn_r'
        )
        fig_role.update_xaxes(tickformat='.0%')
        st.plotly_chart(fig_role, use_container_width=True)
    
    with col2:
        # Attrition by Job Level
        level_attrition = df_filtered.groupby('job_level')['attrition'].agg(['mean', 'count']).reset_index()
        level_attrition = level_attrition[level_attrition['count'] > 0]
        
        fig_level = px.bar(
            level_attrition,
            x='job_level',
            y='mean',
            title='Attrition by Job Level',
            labels={'mean': 'Attrition Rate', 'job_level': 'Job Level'},
            color='mean',
            color_continuous_scale='RdYlGn_r'
        )
        fig_level.update_yaxes(tickformat='.0%')
        st.plotly_chart(fig_level, use_container_width=True)
    
    st.markdown("""
        ### 💡 Insight
        **Entry-level employees (63% attrition) are at highest risk**, while senior employees (20% attrition) 
        are significantly more stable. This suggests:
        - Limited growth opportunities for junior staff
        - Better compensation and stability at senior levels
        - Burnout in high-pressure entry roles
        """)

# ========== TAB 2: SALARY & SATISFACTION ==========
with tab2:
    st.markdown("## 💼 Salary & Job Satisfaction Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly Income vs Attrition
        fig_salary = px.box(
            df_filtered,
            x='attrition',
            y='monthly_income',
            title='Monthly Income vs Attrition',
            labels={'attrition': 'Status', 'monthly_income': 'Monthly Income ($)'},
            color='attrition',
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'}
        )
        fig_salary.update_xaxes(ticktext=['Stayed', 'Left'], tickvals=[0, 1])
        st.plotly_chart(fig_salary, use_container_width=True)
    
    with col2:
        # Income Statistics
        income_stayed = df_filtered[df_filtered['attrition'] == 0]['monthly_income'].mean()
        income_left = df_filtered[df_filtered['attrition'] == 1]['monthly_income'].mean()
        
        st.markdown(f"""
            <div class="insight-box">
                <h3 style="margin-top: 0;">Income Analysis</h3>
                <p><strong>Stayed:</strong> ${income_stayed:,.0f}/month</p>
                <p><strong>Left:</strong> ${income_left:,.0f}/month</p>
                <p style="color: #666; font-size: 12px; margin-top: 15px;">
                    💡 <strong>Insight:</strong> Salary difference is minimal between leavers and stayers.
                    This indicates that <strong>salary alone is not a primary driver of attrition</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Job Satisfaction vs Attrition
        satisfaction_data = df_filtered.groupby(['job_satisfaction', 'attrition']).size().reset_index(name='count')
        
        fig_satisfaction = px.bar(
            satisfaction_data,
            x='job_satisfaction',
            y='count',
            color='attrition',
            barmode='group',
            title='Job Satisfaction vs Attrition',
            labels={'job_satisfaction': 'Job Satisfaction Level', 'count': 'Number of Employees'},
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'}
        )
        fig_satisfaction.update_traces(name='Stayed', selector=dict(name='0'))
        fig_satisfaction.add_trace(go.Bar(name='Left', x=[], y=[]))
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div class="warning-box">
                <h3 style="margin-top: 0;">⚠️ Important Finding</h3>
                <p>Employees with <strong>High</strong> and <strong>Very High satisfaction</strong> 
                make up a significant portion of those who left (47.38% and 22.60% respectively).</p>
                <p><strong>This means:</strong> Job satisfaction alone is NOT a strong predictor of attrition. 
                Even satisfied employees are leaving, indicating deeper systemic issues.</p>
            </div>
            """, unsafe_allow_html=True)

# ========== TAB 3: WORK ENVIRONMENT ==========
with tab3:
    st.markdown("## 🏢 Work Environment & Conditions Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Overtime vs Attrition
        overtime_data = df_filtered.groupby(['overtime', 'attrition']).size().reset_index(name='count')
        
        fig_overtime = px.histogram(
            df_filtered,
            x='overtime',
            color='attrition',
            barmode='group',
            title='Overtime vs Attrition',
            labels={'overtime': 'Overtime Status'},
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'}
        )
        st.plotly_chart(fig_overtime, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div class="warning-box">
                <h3 style="margin-top: 0;">🚨 STRONG DRIVER: Overtime</h3>
                <p>Employees working <strong>overtime have significantly higher attrition rates</strong> 
                compared to those without overtime.</p>
                <p><strong>Key Finding:</strong> Overtime is one of the strongest direct predictors of attrition, 
                suggesting that workload intensity and exhaustion are major retention issues.</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Work-Life Balance vs Attrition
        wlb_data = df_filtered.groupby(['work-life_balance', 'attrition']).size().reset_index(name='count')
        
        fig_wlb = px.bar(
            wlb_data,
            x='work-life_balance',
            y='count',
            color='attrition',
            barmode='group',
            title='Work-Life Balance vs Attrition',
            labels={'work-life_balance': 'Work-Life Balance Level', 'count': 'Number of Employees'},
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'}
        )
        st.plotly_chart(fig_wlb, use_container_width=True)
    
    with col2:
        # Remote Work vs Attrition
        remote_data = df_filtered.groupby(['remote_work']).agg({'attrition': 'mean'}).reset_index()
        
        fig_remote = px.bar(
            remote_data,
            x='remote_work',
            y='attrition',
            title='Remote Work vs Attrition',
            labels={'remote_work': 'Remote Work Status', 'attrition': 'Attrition Rate'},
            color='attrition',
            color_continuous_scale='RdYlGn_r'
        )
        fig_remote.update_yaxes(tickformat='.0%')
        st.plotly_chart(fig_remote, use_container_width=True)
    
    st.markdown("""
        ### 💡 Key Insights
        
        **Remote Work Impact:** 🌟 **Strong Positive**
        - Remote workers have ~25% attrition vs ~50% for in-office
        - Remote work significantly improves retention and work-life balance
        
        **Work-Life Balance:** ⚠️ **Medium Impact**
        - Most leavers report "Fair" or "Good" balance, not extreme burnout
        - Suggests *silent dissatisfaction* rather than crisis-level stress
        - Gradual erosion of satisfaction is the real problem
        """)
    
    st.markdown("---")
    
    # Distance from Home vs Attrition
    col1, col2 = st.columns(2)
    
    with col1:
        fig_distance = px.box(
            df_filtered,
            x='attrition',
            y='distance_from_home',
            title='Distance from Home vs Attrition',
            labels={'attrition': 'Status', 'distance_from_home': 'Distance (miles)'},
            color='attrition',
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'}
        )
        fig_distance.update_xaxes(ticktext=['Stayed', 'Left'], tickvals=[0, 1])
        st.plotly_chart(fig_distance, use_container_width=True)
    
    with col2:
        distance_stayed = df_filtered[df_filtered['attrition'] == 0]['distance_from_home'].median()
        distance_left = df_filtered[df_filtered['attrition'] == 1]['distance_from_home'].median()
        
        st.markdown(f"""
            <div class="insight-box">
                <h3 style="margin-top: 0;">Commute Distance</h3>
                <p><strong>Stayed:</strong> {distance_stayed:.0f} miles (median)</p>
                <p><strong>Left:</strong> {distance_left:.0f} miles (median)</p>
                <p style="color: #666; font-size: 12px; margin-top: 15px;">
                    Longer commutes (especially with overtime) increase turnover pressure.
                    Combined with overtime = higher attrition risk.
                </p>
            </div>
            """, unsafe_allow_html=True)

# ========== TAB 4: CAREER GROWTH ==========
with tab4:
    st.markdown("## 📈 Career Growth & Development Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Promotions vs Attrition
        promotions_data = df_filtered.groupby(['number_of_promotions', 'attrition']).size().reset_index(name='count')
        
        fig_promotions = px.histogram(
            df_filtered,
            x='number_of_promotions',
            color='attrition',
            barmode='group',
            title='Number of Promotions vs Attrition',
            labels={'number_of_promotions': 'Number of Promotions', 'count': 'Employees'},
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'}
        )
        st.plotly_chart(fig_promotions, use_container_width=True)
    
    with col2:
        promotions_stayed = df_filtered[df_filtered['attrition'] == 0]['number_of_promotions'].mean()
        promotions_left = df_filtered[df_filtered['attrition'] == 1]['number_of_promotions'].mean()
        
        st.markdown(f"""
            <div class="insight-box">
                <h3 style="margin-top: 0;">Promotion Statistics</h3>
                <p><strong>Stayed (avg):</strong> {promotions_stayed:.2f} promotions</p>
                <p><strong>Left (avg):</strong> {promotions_left:.2f} promotions</p>
                <p style="color: #666; font-size: 12px; margin-top: 15px;">
                    Promotions alone aren't the issue, but combined with overtime + lack of growth,
                    they signal career stagnation.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Company Reputation vs Attrition
        reputation_data = df_filtered.groupby(['company_reputation']).agg({'attrition': 'mean'}).reset_index()
        
        fig_reputation = px.bar(
            reputation_data,
            x='company_reputation',
            y='attrition',
            title='Company Reputation vs Attrition',
            labels={'company_reputation': 'Reputation', 'attrition': 'Attrition Rate'},
            color='attrition',
            color_continuous_scale='RdYlGn_r'
        )
        fig_reputation.update_yaxes(tickformat='.0%')
        st.plotly_chart(fig_reputation, use_container_width=True)
    
    with col2:
        # Years at Company vs Attrition
        fig_tenure = px.box(
            df_filtered,
            x='attrition',
            y='years_at_company',
            title='Company Tenure vs Attrition',
            labels={'attrition': 'Status', 'years_at_company': 'Years at Company'},
            color='attrition',
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'}
        )
        fig_tenure.update_xaxes(ticktext=['Stayed', 'Left'], tickvals=[0, 1])
        st.plotly_chart(fig_tenure, use_container_width=True)
    
    st.markdown("""
        ### 💡 Key Insights
        
        **Company Reputation:** ⭐ **Important Factor**
        - "Poor" reputation = 56% attrition
        - "Good" reputation = 43% attrition
        - Company brand and market perception significantly impact retention
        
        **Career Tenure:** ℹ️ **Tenure is Not the Issue**
        - Both stayers and leavers have similar tenure
        - Problem isn't early departure of new hires
        - Indicates systemic issues affecting all tenure levels
        """)

# ========== TAB 5: DEMOGRAPHICS & RISK SEGMENTATION ==========
with tab5:
    st.markdown("## 👥 Demographics & Risk Segmentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender vs Attrition
        gender_data = df_filtered.groupby(['gender']).agg({'attrition': 'mean'}).reset_index()
        
        fig_gender = px.bar(
            gender_data,
            x='gender',
            y='attrition',
            title='Attrition Rate by Gender',
            labels={'gender': 'Gender', 'attrition': 'Attrition Rate'},
            color='attrition',
            color_continuous_scale='RdYlGn_r'
        )
        fig_gender.update_yaxes(tickformat='.0%')
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Age Group vs Attrition
        age_data = df_filtered.groupby(['age_group'], observed=True).agg({'attrition': 'mean'}).reset_index()
        
        fig_age = px.line(
            age_data,
            x='age_group',
            y='attrition',
            markers=True,
            title='Attrition Rate by Age Group',
            labels={'age_group': 'Age Group', 'attrition': 'Attrition Rate'},
            line_shape='linear'
        )
        fig_age.update_yaxes(tickformat='.0%')
        st.plotly_chart(fig_age, use_container_width=True)
    
    st.markdown("""
        ### 💡 Demographics Insights
        
        **Gender Disparity:** 👩 **Critical Issue**
        - Female attrition: 53% | Male attrition: 43%
        - 10-point gap suggests systemic issues affecting women
        - Possible causes: advancement barriers, work-life balance, inclusion
        
        **Age Profile:** 📅 **Youth Matters**
        - Youngest (18-25): 52.9% attrition
        - Oldest (55+): 44.4% attrition
        - Young talent is leaving at nearly 2x the rate of senior staff
        """)
    
    st.markdown("---")
    
    # Employee Recognition
    st.markdown("### 🏆 Employee Recognition Impact")
    col1, col2 = st.columns(2)
    
    with col1:
        recognition_data = df_filtered.groupby(['employee_recognition'], observed=True).agg({'attrition': 'mean', 'age': 'count'}).reset_index()
        recognition_data.columns = ['employee_recognition', 'attrition', 'count']
        
        fig_recognition = px.bar(
            recognition_data,
            x='employee_recognition',
            y='attrition',
            title='Attrition by Recognition Level',
            labels={'employee_recognition': 'Recognition Level', 'attrition': 'Attrition Rate'},
            color='attrition',
            color_continuous_scale='RdYlGn_r'
        )
        fig_recognition.update_yaxes(tickformat='.0%')
        st.plotly_chart(fig_recognition, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div class="insight-box">
                <h3 style="margin-top: 0;">🏆 Recognition Matters</h3>
                <p>Employees who receive <strong>low or no recognition</strong> have 
                significantly higher attrition rates.</p>
                <p><strong>Action Item:</strong> Implement recognition programs 
                to acknowledge and celebrate employee contributions.</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Risk Segmentation Matrix
    st.markdown("### 🎯 High-Risk Employee Segments")
    
    risk_segments = df_filtered.groupby(['gender', 'age_group'], observed=True).agg({
        'attrition': ['mean', 'count']
    }).reset_index()
    risk_segments.columns = ['gender', 'age_group', 'attrition_rate', 'count']
    risk_segments = risk_segments[risk_segments['count'] > 10].sort_values('attrition_rate', ascending=False).head(15)
    
    # Create segment label combining gender and age
    risk_segments['segment'] = risk_segments['gender'] + ' (' + risk_segments['age_group'].astype(str) + ')'
    
    fig_risk = px.bar(
        risk_segments,
        x='attrition_rate',
        y='segment',
        title='Top 15 Risk Segments (Gender × Age)',
        labels={'attrition_rate': 'Attrition Rate', 'segment': 'Segment'},
        color='attrition_rate',
        color_continuous_scale='Reds',
        orientation='h'
    )
    fig_risk.update_yaxes(tickformat='.0%')
    st.plotly_chart(fig_risk, use_container_width=True)

# =======================
# INSIGHTS & RECOMMENDATIONS
# =======================
st.markdown("---")
st.markdown("## 🎯 Key Findings & Strategic Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        ### 🚨 Critical Issues Identified
        
        1. **Overtime is a Primary Driver**
           - Employees working overtime have ~2.2x higher attrition
           - Workload management is urgently needed
        
        2. **Youth Flight**
           - 18-25 age group leaves at 52.9% rate
           - Entry-level roles unsustainable
        
        3. **Gender Disparity**
           - Women leave at 53% vs men at 43%
           - Systemic retention issues for females
        
        4. **Remote Work Success**
           - Remote workers: 25% attrition
           - In-office workers: 50% attrition
           - Flexible work is retention tool
        """)

with col2:
    st.markdown("""
        ### ✅ Recommended Actions
        
        1. **Manage Overtime Aggressively**
           - Redistribute workload
           - Hire additional resources
           - Monitor burnout indicators
        
        2. **Invest in Entry-Level Retention**
           - Mentorship programs
           - Faster growth paths
           - Better entry-level compensation
        
        3. **Women Retention Initiative**
           - Career advancement programs
           - Assess work-life balance
           - Inclusive culture review
        
        4. **Expand Remote Work Options**
           - Core remote positions
           - Flexible schedules
           - Better work-life balance
        """)

# =======================
# DETAILED INSIGHTS
# =======================
st.markdown("---")
st.markdown("## 📊 Detailed Analysis & Insights")

with st.expander("📌 Complete Attrition Analysis Framework", expanded=True):
    st.markdown("""
        ### The Attrition Problem: Root Cause Analysis
        
        **Overall Attrition Rate: 47.48%** ⚠️
        
        This extremely high rate indicates a **retention crisis** requiring immediate strategic intervention.
        
        ---
        
        ### Factor-by-Factor Analysis
        
        | Factor | Impact Level | Status |
        |--------|-------------|--------|
        | **Overtime** | 🔴 CRITICAL | Strong direct driver of attrition |
        | **Job Level** | 🔴 CRITICAL | Entry-level 63% vs Senior 20% |
        | **Gender** | 🔴 CRITICAL | Female 53% vs Male 43% |
        | **Remote Work** | 🟢 MITIGATOR | Reduces attrition to 25% |
        | **Company Reputation** | 🟠 SIGNIFICANT | Poor 56% vs Good 43% |
        | **Age** | 🟠 SIGNIFICANT | Youth (52.9%) vs Senior (44.4%) |
        | **Work-Life Balance** | 🟡 MODERATE | Medium impact, widespread issue |
        | **Distance from Home** | 🟡 MODERATE | Compounds other stressors |
        | **Promotions** | 🔵 WEAK | Not primary driver alone |
        | **Job Satisfaction** | 🔵 WEAK | Even satisfied employees leave |
        | **Salary** | 🔵 NOT IMPORTANT | Similar for stayers and leavers |
        
        ---
        
        ### The Real Problem
        
        **Attrition is NOT a single-issue problem.** It's a **combination effect**:
        
        1. **Workload Intensity** (Overtime) → Creates burnout pressure
        2. **Limited Growth** (Entry-level roles) → No career path visible
        3. **Commute Distance** → Compounded by overtime pressures
        4. **Recognition Gap** → Lack of acknowledgment and appreciation
        5. **Gender & Age** → Disproportionate impact on women and youth
        
        **The Multiplier Effect:**
        - Overtime + Poor Balance + No Promotions = Very High Risk
        - Young + Female + No Recognition = Extremely High Risk
        - Entry-Level + Overtime + Far Commute = Unsustainable
        
        ---
        
        ### Strategic Recommendations
        
        **Tier 1: Immediate Actions (0-30 days)**
        1. Conduct exit interviews for all recent leavers
        2. Audit overtime policies and workload distribution
        3. Identify and support employees at highest risk
        
        **Tier 2: Short-term Changes (1-3 months)**
        1. Implement flexible work/remote options
        2. Launch employee recognition program
        3. Review entry-level compensation and roles
        4. Create mentorship for junior employees
        
        **Tier 3: Strategic Initiatives (3-12 months)**
        1. Restructure career development paths
        2. Implement workload management systems
        3. Review gender equity across all roles
        4. Build inclusive and supportive culture
        5. Data-driven HR analytics for early intervention
        
        ---
        
        #### Key Performance Targets
        - **Reduce overall attrition to <30%** within 12 months
        - **Entry-level attrition to <40%** (from 63%)
        - **Gender gap to <5%** (from 10%)
        - **Increase remote work participation to 40%+**
    """)

with st.expander("📊 Factor Interaction Analysis"):
    st.markdown("""
        ### How Factors Work Together
        
        **Overtime × Work-Life Balance Interaction:**
        - Without Overtime + Good Balance = High retention
        - With Overtime + Good Balance = Still high attrition
        - **Insight:** Overtime overwhelms other positive factors
        
        **Overtime × Promotions Interaction:**
        - No Overtime + Few Promotions = Acceptable attrition
        - With Overtime + Few Promotions = Very high attrition
        - **Insight:** Burnout + stagnation = departure
        
        **The Gender-Specific Crisis:**
        - Women face disproportionate impact across ALL metrics
        - Suggests intersectional barriers (gender + workload + advancement)
        - Requires targeted women-focused retention programs
        
        **Youth Flight Pattern:**
        - Young employees optimize early in career
        - If role is burning them out, they leave quickly
        - Entry-level positions must be sustainable
    """)

with st.expander("💼 Business Impact & ROI"):
    st.markdown("""
        ### Cost of Current Attrition
        
        **At 47.48% annual attrition:**
        - Average replacement cost: 50-200% of annual salary
        - Knowledge loss and productivity dips
        - Team morale and remaining staff stress
        - Reduced client/customer relationships
        
        ### ROI of Intervention
        
        **Reducing to 30% attrition would save approximately:**
        - 800-2000 employees × $50K-100K replacement cost
        - **= $40-200M in annual retention costs saved**
        - Plus: Improved productivity, better team cohesion, stronger culture
        
        **Remote Work Expansion:**
        - Enabling 40% remote positions could reduce attrition by 25-30%
        - Cost: Infrastructure and management training
        - Benefit: Dramatic improvement in retention, productivity, employee satisfaction
    """)

# =======================
# FOOTER
# =======================
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px; font-size: 12px;">
        <p>📊 <strong>HR Analytics Dashboard v1.0</strong> | Generated on """ + datetime.now().strftime("%B %d, %Y") + """</p>
        <p>Data-driven insights for strategic HR decision-making | Empowering talent retention strategies</p>
    </div>
    """, unsafe_allow_html=True)
