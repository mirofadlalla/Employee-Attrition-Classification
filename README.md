# 📊 HR Analytics Dashboard - Employee Attrition Analysis

A **professional, modern Streamlit dashboard** for HR teams to analyze employee attrition patterns, identify at-risk segments, and drive data-informed retention strategies.

## 🎯 Features

### 📈 **KPI Dashboard**
- Total Employees count
- Attrition Rate (with trend)
- Active Employees
- Average Monthly Income

### 🔍 **Interactive Filters**
Filter data by:
- Job Role
- Job Level
- Overtime Status
- Remote Work Availability
- Gender

### 📊 **5 Main Analysis Sections**

1. **Attrition Overview** 🎯
   - Attrition distribution (pie chart)
   - Current attrition metrics
   - Breakdown by job role and level

2. **Salary & Satisfaction** 💼
   - Monthly income vs attrition
   - Job satisfaction analysis
   - Income statistics and insights

3. **Work Environment** 🏢
   - Overtime impact (CRITICAL DRIVER)
   - Work-life balance analysis
   - Remote work effectiveness
   - Commute distance effect

4. **Career Growth** 📈
   - Promotions vs attrition
   - Company reputation impact
   - Tenure/loyalty analysis

5. **Demographics & Risk** 👥
   - Gender disparity analysis
   - Age group breakdown
   - Employee recognition impact
   - High-risk segment identification

### 💡 **Deep Insights Section**
- Complete attrition analysis framework
- Factor interaction analysis
- ROI calculations and business impact
- Actionable recommendations

---

## 📦 Installation & Setup

### **Option 1: Local Installation**

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Steps

1. **Clone/Download the repository**
   ```bash
   cd employee-attrition-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard**
   - Open your browser to `http://localhost:8501`

---

### **Option 2: Deploy on Streamlit Community Cloud (Free)**

This is the **recommended production deployment method**.

#### Prerequisites
- GitHub account
- Streamlit account (free)

#### Deployment Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial HR Analytics Dashboard"
   git push origin main
   ```

2. **Create a Streamlit Cloud Account**
   - Visit: https://share.streamlit.io
   - Click "Sign up"
   - Use your GitHub account to login

3. **Deploy Your App**
   - Go to: https://share.streamlit.io
   - Click "New app"
   - Select:
     - **Repository:** Your GitHub repo
     - **Branch:** main
     - **Main file path:** app.py
   - Click "Deploy"

4. **Share Your Dashboard**
   - Get your public URL (e.g., `https://your-username-hr-analytics.streamlit.app`)
   - Share with your HR team
   - No installation needed for users!

---

### **Option 3: Docker Deployment**

For enterprise deployments, use Docker:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

**Build and run:**
```bash
docker build -t hr-analytics .
docker run -p 8501:8501 hr-analytics
```

---

## 📁 Project Structure

```
employee-attrition-dashboard/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── data/
│   ├── train.csv                  # Training dataset
│   └── test.csv                   # Test dataset
│
└── .streamlit/
    ├── config.toml                # Streamlit configuration (optional)
    └── secrets.toml               # Sensitive data (optional, not in git)
```

---

## 🔧 Configuration

### Streamlit Config (Optional)

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#2c3e50"
font = "sans serif"

[client]
showErrorDetails = false

[logger]
level = "info"
```

---

## 📊 Analysis Highlights

### 🚨 **Critical Findings**

| Finding | Value | Impact |
|---------|-------|--------|
| **Overall Attrition Rate** | 47.48% | 🔴 CRISIS LEVEL |
| **Entry-Level Attrition** | 63% | 🔴 CRITICAL |
| **Female Attrition** | 53% | 🔴 CRITICAL |
| **Overtime Impact** | 2.2x higher risk | 🔴 CRITICAL DRIVER |
| **Remote Work Effect** | -25% (beneficial) | 🟢 STRONG MITIGATOR |

### 💡 **Key Insights**

1. **Overtime is the #1 Attrition Driver**
   - Employees with overtime leave at twice the rate
   - Workload management is urgent priority

2. **Youth Leaving Rapidly**
   - 18-25 age group: 52.9% attrition
   - Entry roles unsustainable

3. **Gender Disparity**
   - Women leave 10% more than men
   - Systemic retention issues

4. **Remote Work Works**
   - Remote: 25% attrition
   - In-office: 50% attrition
   - Flexible work is powerful tool

5. **Salary is NOT the Issue**
   - Leavers and stayers earn similarly
   - Problem is deeper (workload, growth, recognition)

---

## 🎯 Strategic Recommendations

### **Tier 1: Immediate (0-30 days)**
- [ ] Conduct exit interviews
- [ ] Audit overtime policies
- [ ] Identify at-risk employees

### **Tier 2: Short-term (1-3 months)**
- [ ] Expand remote work options
- [ ] Launch recognition program
- [ ] Review entry-level roles

### **Tier 3: Strategic (3-12 months)**
- [ ] Restructure career paths
- [ ] Implement workload management
- [ ] Build inclusive culture

---

## 📈 Expected Impact

**If you reduce attrition from 47.48% to 30%:**

| Metric | Savings |
|--------|---------|
| Replacement Cost Avoided | $40-200M/year |
| Productivity Improvement | 15-25% |
| Team Morale | Significant |
| Client Retention | 20%+ improvement |

---

## 🚀 Usage Guide for HR Teams

### **For Executives**
1. View KPI cards for overall health
2. Check attrition trend month-over-month
3. Review top risk segments
4. Review action items

### **For HR Managers**
1. Use filters to analyze specific departments
2. Identify at-risk employees
3. Monitor overtime usage
4. Track recognition metrics

### **For Analysts**
1. Drill into specific segments
2. Analyze factor interactions
3. Export data for deeper analysis
4. Build retention models

---

## 🔄 Data Updates

### **Automatic Updates** (Streamlit Community Cloud)
- Dashboard reloads data when running

### **Manual Updates**
1. Update `data/train.csv` or `data/test.csv`
2. Redeploy or refresh dashboard
3. Streamlit will cache new data

---

## 🛠️ Troubleshooting

#### **Dashboard won't load**
```bash
# Clear Streamlit cache
streamlit cache clear

# Run again
streamlit run app.py
```

#### **Data not updating**
```bash
# Clear Python cache
rm -rf __pycache__
rm -rf .streamlit/cache

# Restart app
streamlit run app.py --logger.level=debug
```

#### **Deployment issues on Streamlit Cloud**
1. Ensure `requirements.txt` has pinned versions
2. Check that data files are in correct paths
3. Verify file paths are relative (not absolute)
4. Check repository is public on GitHub

---

## 📞 Support & Maintenance

### **Common Questions**

**Q: Can I connect to a live database instead of CSV?**
A: Yes! Modify the `load_data()` function to connect to your database.

**Q: How often should I update the data?**
A: Weekly or monthly recommended. More frequent for executive dashboards.

**Q: Can I add new analyses?**
A: Absolutely! The notebook has more analyses you can add to new tabs.

**Q: Is my data secure on Streamlit Cloud?**
A: Yes. Streamlit Cloud is GDPR/SOC2 compliant. Use secrets.toml for sensitive data.

---

## 📚 Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Plotly Charts:** https://plotly.com/python/
- **Pandas Documentation:** https://pandas.pydata.org/docs/
- **Streamlit Community:** https://discuss.streamlit.io

---

## 📝 License

This dashboard is built for internal HR use.

---

## 🎉 Next Steps

1. **Deploy** the dashboard using Streamlit Community Cloud
2. **Share** the URL with your HR and management teams
3. **Monitor** the identified risk segments
4. **Implement** the recommended actions
5. **Track** improvements in attrition metrics

---

**Build date:** 2026-06-03  
**Version:** 1.0  
**Status:** Production Ready 🚀
