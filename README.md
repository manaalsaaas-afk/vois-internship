# VOIS AICTE Internship Major Project
## Seasonal Agriculture Performance Analysis (Batch 1: 2026–2027)

**Candidate / Author:** Manal Sas  
**GitHub Repository:** [https://github.com/manaalsaaas-afk/vois-internship.git](https://github.com/manaalsaaas-afk/vois-internship.git)  
**Deliverables:** PowerPoint Presentation Deck (`.pptx`), Jupyter Notebook (`.ipynb`), Cleaned Dataset (`.csv`), High-Resolution Visual Dashboards (`assets/`)

---

## 📌 Project Overview
Agricultural systems across India are deeply influenced by seasonal micro-climates, monsoon patterns, and input variations across **Kharif** (monsoon), **Rabi** (winter), and **Zaid** (summer) seasons. This project analyzes **4,000 farm profiles** across 8 Indian states (Andhra Pradesh, Maharashtra, Telangana, Karnataka, Gujarat, Tamil Nadu, Punjab, Madhya Pradesh) and 10 districts covering 28 variables spanning soil health, environmental parameters, resource allocation, and economic returns.

---

## 🔬 Key Analytical Findings

1. **Seasonal Productivity Dynamics**:
   - **Kharif (Monsoon)** dominates overall agricultural production, accounting for **48% of annual output**, with an average yield of **5.64 Tonnes/Ha** and net profit of **₹1,78,915**.
   - **Rabi (Winter)** offers high operational stability with average yield of **5.08 Tonnes/Ha**, moderate costs (₹5.14 Lakh), and reliable returns (₹87,689).
   - **Zaid (Summer)** suffers from severe heat stress (31.0°C) and water deficits (299 mm rainfall), resulting in lowest yields (4.67 Tonnes/Ha) and an average net loss of **-₹24,805** under conventional flood farming.

2. **Environmental & Pest Risk Nexus**:
   - High relative atmospheric humidity (>70%) strongly correlates with elevated crop disease and pest outbreak risk ($r = +0.48, p < 10^{-10}$).
   - Kharif experiences peak disease incidence (**54.5% risk**), requiring proactive Integrated Pest Management (IPM).

3. **Irrigation & Water Productivity**:
   - **Drip irrigation** delivers the highest water efficiency (**6.27 t/1000m³**) and highest average profit (**₹2.35 Lakh**).
   - **Flood irrigation** consumes 8,026 m³ per farm (35% more water than drip) while generating lower yields, producing heavy losses (**-₹69,787**) during Zaid.
   - **Rainfed cultivation** is viable during monsoon Kharif (+₹1.59 Lakh), but produces catastrophic losses (**-₹79,467**) in summer Zaid.

4. **Statistical Significance (One-Way ANOVA)**:
   - Differences in Net Profit across seasons are highly statistically significant:  
     $$\mathbf{F = 34.29, \quad p = 1.71 \times 10^{-15}}$$
     (Reject $H_0$: Seasonal climatic differences fundamentally govern farming profitability).

5. **Crop Economics**:
   - High-value commercial crops like **Chilli** (₹1,03,373/t market price) and **Sugarcane** (46.9 t/ha yield) maintain strong profitability (>₹4.5L to ₹10.0L/farm) across all seasons.
   - **Wheat** farmers face margin compression across seasons due to elevated input costs relative to realization prices.

---

## 📂 Repository Structure

```
├── VOIS_Major_Project_Seasonal_Agriculture_Performance_Analysis.pptx  # Official 14-slide submission deck
├── Seasonal_Agriculture_Performance_Analysis.ipynb                  # Executed Jupyter Notebook (12 questions, ANOVA, EDA)
├── cleaned_seasonal_agriculture_dataset.csv                         # Fully imputed and validated dataset (4,000 rows)
├── seasonal_agriculture_performance_dataset (2).csv                # Raw source dataset
├── Major Project_Seasonal Agriculture Performance Analysis. (2).pdf # Official project guidelines & problem statement
├── build_presentation.py                                            # Automated PowerPoint synthesis script
├── generate_analytics_and_assets.py                                 # Visual charts & code card generator
├── build_notebook.py                                                # Jupyter notebook generation script
├── execute_notebook.py                                              # Programmatic notebook execution engine
├── assets/                                                          # 300-DPI publication-grade visuals
│   ├── chart0_overview.png                                          # 4-panel seasonal KPI executive dashboard
│   ├── chart1_yield_production.png                                  # Yield & production dynamics across crops
│   ├── chart2_environmental_disease.png                             # Climatic regimes & pest risk scatter/KDE
│   ├── chart3_irrigation_efficiency.png                             # Water efficiency & irrigation profit comparison
│   ├── chart4_economic_profitability.png                            # Financial breakdown & crop profitability
│   ├── code_snippet_1.png                                           # Syntax-highlighted code card (Analysis 1)
│   ├── code_snippet_2.png                                           # Syntax-highlighted code card (Analysis 2)
│   ├── code_snippet_3.png                                           # Syntax-highlighted code card (Analysis 3)
│   └── code_snippet_4.png                                           # Syntax-highlighted code card (Analysis 4)
└── README.md                                                        # Project documentation and reproduction guide
```

---

## 🚀 How to Run & Reproduce

### 1. Environment Requirements
Ensure Python 3.10+ is installed. Install required packages:
```bash
pip install pandas numpy matplotlib seaborn scipy python-pptx pillow
```

### 2. Regenerate All Analytical Charts & Code Cards
```bash
python generate_analytics_and_assets.py
```

### 3. Rebuild the PowerPoint Presentation Deck
```bash
python build_presentation.py
```

### 4. Build and Execute the Jupyter Notebook
```bash
python build_notebook.py
python execute_notebook.py
```

---

## 🎯 Presentation Slides Breakdown (14 Slides)

| Slide # | Slide Title | Content / Highlights |
| :---: | :--- | :--- |
| **1** | Title Slide | Project Title, Student Name (`Aswini Kumar`), College & AICTE ID placeholders |
| **2** | Problem Statement | Agricultural volatility, information gaps, research objectives & strategic impact |
| **3** | Project Description | 4,000 farm records, 28 attributes, 6-phase analytical pipeline & exact mathematical imputation |
| **4** | Who are the End Users? | Farmers/FPOs, Extension Agronomists, Policymakers, Agribusinesses, Crop Insurers |
| **5** | Technology Stack | Python 3.11, Pandas, NumPy, Matplotlib, Seaborn, SciPy Stats, Jupyter, Git |
| **6** | RESULTS: Executive Dashboard | Embedded 4-panel KPI dashboard + seasonal performance metrics |
| **7** | RESULTS: Yield & Production Dynamics | Code snippet card + comparative yield barplot + volume analysis |
| **8** | RESULTS: Environmental & Pest Risk | Code snippet card + humidity/pest scatter + climatic KDE contours |
| **9** | RESULTS: Resource & Irrigation Efficiency | Code snippet card + water efficiency barplot + irrigation net profit comparison |
| **10** | RESULTS: Economic Outcomes & ANOVA | Code snippet card + financial structure breakdown + ANOVA test ($p = 1.71 \times 10^{-15}$) |
| **11** | Future Scope & Recommendations | Machine learning yield forecasting, IoT smart irrigation, crop diversification |
| **12** | GitHub Link & Repository Structure | Official repo link, directory tree, documentation, and reproducibility guide |
| **13** | Course Completion Certificate | Framed placeholder for VOIS Data Visualization certificate + core competencies |
| **14** | Thank You | Acknowledgments to VOIS & AICTE, discussion & Q&A invitation |

---

## 📜 Acknowledgments
Special thanks to the mentoring team at **Vodafone Intelligent Solutions (VOIS)** and the **All India Council for Technical Education (AICTE)** for providing this research opportunity and real-world dataset.
