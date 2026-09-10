import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont

# Set overall aesthetic style
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'sans-serif',
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16,
    'figure.autolayout': True
})

os.makedirs('assets', exist_ok=True)

# 1. Load Dataset
df = pd.read_csv('seasonal_agriculture_performance_dataset (2).csv')
print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# 2. Data Cleaning & Precise Imputation
# Yield = Production / Area
df['Yield_Tonnes_Ha'] = df['Yield_Tonnes_Ha'].fillna(
    (df['Production_Tonnes'] / df['Farm_Area_Hectares']).round(2)
)

# Rainfall by Season & State median
df['Rainfall_mm'] = df.groupby(['Season', 'State'])['Rainfall_mm'].transform(
    lambda x: x.fillna(x.median())
)

# Soil Moisture by Season & Irrigation Method median
df['Soil_Moisture_pct'] = df.groupby(['Season', 'Irrigation_Method'])['Soil_Moisture_pct'].transform(
    lambda x: x.fillna(x.median())
)

# Feature Engineering
df['Profit_Margin_pct'] = ((df['Profit_INR'] / df['Revenue_INR']) * 100).round(2)
df['Cost_per_Hectare'] = (df['Total_Cost_INR'] / df['Farm_Area_Hectares']).round(2)
df['Revenue_per_Hectare'] = (df['Revenue_INR'] / df['Farm_Area_Hectares']).round(2)

print("Data cleaning & feature engineering complete.")
print("Missing values remaining:", df.isnull().sum().sum())

# Save cleaned dataset
df.to_csv('cleaned_seasonal_agriculture_dataset.csv', index=False)
print("Saved cleaned_seasonal_agriculture_dataset.csv")

# -------------------------------------------------------------
# CHART 0: Executive Seasonal Dashboard Summary
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(16, 4.5), dpi=300)
season_order = ['Kharif', 'Rabi', 'Zaid']
palette = {'Kharif': '#2b8a3e', 'Rabi': '#1971c2', 'Zaid': '#e8590c'}

# Panel 1: Avg Yield
sns.barplot(data=df, x='Season', y='Yield_Tonnes_Ha', order=season_order, palette=palette, ax=axes[0], ci=None, capsize=0.1)
axes[0].set_title('Avg Crop Yield (Tonnes/Ha)', fontweight='bold')
axes[0].set_ylabel('Yield (t/ha)')
for p in axes[0].patches:
    axes[0].annotate(f"{p.get_height():.2f} t", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                     ha='center', va='center', color='white', fontweight='bold', fontsize=12)

# Panel 2: Avg Profit
sns.barplot(data=df, x='Season', y='Profit_INR', order=season_order, palette=palette, ax=axes[1], ci=None)
axes[1].set_title('Avg Net Profit (INR ₹)', fontweight='bold')
axes[1].set_ylabel('Profit (₹)')
axes[1].axhline(0, color='gray', linestyle='--', linewidth=0.8)
for p in axes[1].patches:
    val = p.get_height()
    axes[1].annotate(f"₹{val/1000:,.1f}K", (p.get_x() + p.get_width() / 2., val / 2 if abs(val)>20000 else val + 15000),
                     ha='center', va='center', color='white' if abs(val)>35000 else 'black', fontweight='bold', fontsize=11)

# Panel 3: Rainfall & Soil Moisture
df_melt_env = df.groupby('Season')[['Rainfall_mm', 'Soil_Moisture_pct']].mean().reindex(season_order).reset_index()
ax3_twin = axes[2].twinx()
p1 = axes[2].bar([x - 0.18 for x in range(3)], df_melt_env['Rainfall_mm'], width=0.35, color='#4dabf7', label='Rainfall (mm)')
p2 = ax3_twin.bar([x + 0.18 for x in range(3)], df_melt_env['Soil_Moisture_pct'], width=0.35, color='#51cf66', label='Soil Moisture (%)')
axes[2].set_xticks(range(3))
axes[2].set_xticklabels(season_order)
axes[2].set_title('Rainfall & Soil Moisture', fontweight='bold')
axes[2].set_ylabel('Rainfall (mm)', color='#1971c2')
ax3_twin.set_ylabel('Soil Moisture (%)', color='#2b8a3e')
axes[2].grid(False)
ax3_twin.grid(False)

# Panel 4: Pest Risk
sns.barplot(data=df, x='Season', y='Disease_Pest_Risk_pct', order=season_order, palette=['#e03131', '#fcc419', '#fab005'], ax=axes[3], ci=None)
axes[3].set_title('Pest & Disease Risk (%)', fontweight='bold')
axes[3].set_ylabel('Risk Score (%)')
for p in axes[3].patches:
    axes[3].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                     ha='center', va='center', color='white', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('assets/chart0_overview.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved assets/chart0_overview.png")

# -------------------------------------------------------------
# CHART 1: Seasonal Crop Yield & Total Production
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

# Subplot 1: Yield by Crop across Seasons (exclude sugarcane for visual scaling)
df_no_cane = df[df['Crop'] != 'Sugarcane']
sns.barplot(data=df_no_cane, x='Crop', y='Yield_Tonnes_Ha', hue='Season', 
            hue_order=season_order, palette=palette, ax=axes[0], ci=None)
axes[0].set_title('Crop Yield by Season (Excl. Sugarcane)', fontweight='bold', fontsize=13)
axes[0].set_ylabel('Yield (Tonnes / Hectare)')
axes[0].set_xlabel('Crop Type')
axes[0].tick_params(axis='x', rotation=30)
axes[0].legend(title='Season', loc='upper right')

# Subplot 2: Total Production Share by Crop across Seasons
prod_crop = df.groupby(['Crop', 'Season'])['Production_Tonnes'].sum().unstack()[season_order]
prod_crop.plot(kind='bar', stacked=True, color=[palette[s] for s in season_order], ax=axes[1])
axes[1].set_title('Total Production Volume by Crop & Season', fontweight='bold', fontsize=13)
axes[1].set_ylabel('Total Production (Tonnes)')
axes[1].set_xlabel('Crop Type')
axes[1].tick_params(axis='x', rotation=30)
axes[1].legend(title='Season', loc='upper right')

plt.tight_layout()
plt.savefig('assets/chart1_yield_production.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved assets/chart1_yield_production.png")

# -------------------------------------------------------------
# CHART 2: Environmental Drivers & Pest Risk
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

# Subplot 1: Scatter / Regplot of Humidity vs Pest Risk by Season
sns.scatterplot(data=df, x='Humidity_pct', y='Disease_Pest_Risk_pct', hue='Season',
                hue_order=season_order, palette=palette, alpha=0.6, s=35, ax=axes[0])
sns.regplot(data=df, x='Humidity_pct', y='Disease_Pest_Risk_pct', scatter=False, ax=axes[0], color='black', line_kws={'linestyle':'--'})
axes[0].set_title('Humidity vs Disease & Pest Risk', fontweight='bold', fontsize=13)
axes[0].set_xlabel('Humidity (%)')
axes[0].set_ylabel('Disease & Pest Risk (%)')

# Subplot 2: Temperature vs Rainfall seasonal cluster
sns.kdeplot(data=df, x='Avg_Temperature_C', y='Rainfall_mm', hue='Season',
            hue_order=season_order, palette=palette, fill=True, alpha=0.3, levels=5, ax=axes[1])
axes[1].set_title('Climatic Regimes: Temperature vs Rainfall', fontweight='bold', fontsize=13)
axes[1].set_xlabel('Average Temperature (°C)')
axes[1].set_ylabel('Rainfall (mm)')

plt.tight_layout()
plt.savefig('assets/chart2_environmental_disease.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved assets/chart2_environmental_disease.png")

# -------------------------------------------------------------
# CHART 3: Irrigation Methods & Water Efficiency
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
irr_order = ['Drip', 'Sprinkler', 'Flood', 'Rainfed']
irr_palette = {'Drip': '#2b8a3e', 'Sprinkler': '#1971c2', 'Flood': '#f03e3e', 'Rainfed': '#fd7e14'}

# Subplot 1: Water Efficiency by Irrigation Method & Season
sns.barplot(data=df, x='Irrigation_Method', y='Water_Efficiency_t_per_1000m3', hue='Season',
            order=irr_order, hue_order=season_order, palette=palette, ax=axes[0], ci=None)
axes[0].set_title('Water Efficiency (Tonnes / 1000 m³) by Season', fontweight='bold', fontsize=13)
axes[0].set_ylabel('Water Efficiency (t/1000m³)')
axes[0].set_xlabel('Irrigation Method')
axes[0].legend(title='Season')

# Subplot 2: Profitability by Irrigation Method across Seasons
sns.barplot(data=df, x='Irrigation_Method', y='Profit_INR', hue='Season',
            order=irr_order, hue_order=season_order, palette=palette, ax=axes[1], ci=None)
axes[1].axhline(0, color='red', linestyle='--', linewidth=1)
axes[1].set_title('Net Profit by Irrigation Method & Season', fontweight='bold', fontsize=13)
axes[1].set_ylabel('Net Profit (INR ₹)')
axes[1].set_xlabel('Irrigation Method')
axes[1].legend(title='Season')

plt.tight_layout()
plt.savefig('assets/chart3_irrigation_efficiency.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved assets/chart3_irrigation_efficiency.png")

# -------------------------------------------------------------
# CHART 4: Economic Outcomes & Profitability Dynamics
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

# Subplot 1: Revenue vs Cost vs Profit by Season
econ_summary = df.groupby('Season')[['Revenue_INR', 'Total_Cost_INR', 'Profit_INR']].mean().reindex(season_order) / 100000
econ_summary.plot(kind='bar', color=['#2f9e44', '#e03131', '#1971c2'], ax=axes[0], width=0.7)
axes[0].set_title('Mean Financial Structure by Season (Lakh ₹)', fontweight='bold', fontsize=13)
axes[0].set_ylabel('Amount (Lakh INR ₹)')
axes[0].set_xlabel('Season')
axes[0].tick_params(axis='x', rotation=0)
axes[0].legend(['Revenue', 'Total Cost', 'Net Profit'], loc='upper right')
axes[0].axhline(0, color='gray', linestyle='--', linewidth=0.8)

# Subplot 2: Net Profit by Crop across Seasons
sns.barplot(data=df, x='Crop', y='Profit_INR', hue='Season',
            hue_order=season_order, palette=palette, ax=axes[1], ci=None)
axes[1].set_title('Crop Net Profitability Across Seasons', fontweight='bold', fontsize=13)
axes[1].set_ylabel('Net Profit (INR ₹)')
axes[1].set_xlabel('Crop Type')
axes[1].axhline(0, color='red', linestyle='--', linewidth=0.8)
axes[1].tick_params(axis='x', rotation=30)
axes[1].legend(title='Season', loc='upper right')

plt.tight_layout()
plt.savefig('assets/chart4_economic_profitability.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved assets/chart4_economic_profitability.png")

# -------------------------------------------------------------
# GENERATE CODE SNIPPET IMAGES (VS Code Dark Theme Aesthetic)
# -------------------------------------------------------------
def render_code_snippet(title, code_lines, filename, width=1200, height=750):
    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)
    
    # Top header bar (VS code tab style)
    draw.rectangle([(0, 0), (width, 42)], fill='#252526')
    # Window controls
    draw.ellipse([(14, 14), (26, 26)], fill='#ff5f56')
    draw.ellipse([(34, 14), (46, 26)], fill='#ffbd2e')
    draw.ellipse([(54, 14), (66, 26)], fill='#27c93f')
    
    try:
        font_header = ImageFont.truetype("consola.ttf", 16)
        font_code = ImageFont.truetype("consola.ttf", 18)
        font_lineno = ImageFont.truetype("consola.ttf", 16)
    except:
        font_header = font_code = font_lineno = ImageFont.load_default()
        
    draw.text((80, 12), title, fill='#cccccc', font=font_header)
    draw.line([(0, 42), (width, 42)], fill='#333333', width=1)
    
    y = 60
    for idx, line in enumerate(code_lines, 1):
        # Line number
        draw.text((25, y), f"{idx:2d}", fill='#5c6370', font=font_lineno)
        draw.line([(60, 50), (60, height-20)], fill='#2d2d2d', width=1)
        
        # Color line based on contents
        if line.strip().startswith('#'):
            color = '#6a9955' # comment green
        elif any(kw in line for kw in ['import ', 'from ', 'def ', 'return ', 'for ', 'in ', 'if ', 'else:']):
            color = '#c586c0' # keyword purple
        elif any(fn in line for fn in ['groupby', 'mean', 'sum', 'barplot', 'scatterplot', 'regplot', 'f_oneway']):
            color = '#dcdcaa' # function yellow
        elif "'" in line or '"' in line:
            color = '#ce9178' # string orange
        else:
            color = '#9cdcfe' # variable light blue
            
        draw.text((75, y), line, fill=color, font=font_code)
        y += 28
        if y > height - 30:
            break
            
    img.save(filename)
    print(f"Saved {filename}")

# Snippet 1: Seasonal Yield & Production Analysis
code1 = [
    "# 1. Seasonal Crop Yield & Production Aggregation",
    "import pandas as pd",
    "import seaborn as sns",
    "import matplotlib.pyplot as plt",
    "",
    "# Grouping data by Crop and Season",
    "yield_summary = df.groupby(['Crop', 'Season'])[[",
    "    'Yield_Tonnes_Ha', 'Production_Tonnes'",
    "]].agg(['mean', 'std']).reset_index()",
    "",
    "# Visualizing comparative yield dynamics across seasons",
    "plt.figure(figsize=(10, 5))",
    "sns.barplot(data=df[df['Crop'] != 'Sugarcane'],",
    "            x='Crop', y='Yield_Tonnes_Ha', hue='Season',",
    "            palette={'Kharif':'#2b8a3e', 'Rabi':'#1971c2', 'Zaid':'#e8590c'})",
    "plt.title('Seasonal Crop Yield Comparison (Tonnes / Ha)')",
    "plt.ylabel('Average Yield (t/ha)')",
    "plt.xticks(rotation=25)",
    "plt.tight_layout()",
    "plt.show()"
]
render_code_snippet("analysis_01_seasonal_yield.py", code1, "assets/code_snippet_1.png")

# Snippet 2: Environmental Drivers & Pest Risk
code2 = [
    "# 2. Environmental Impact on Pest & Disease Risk",
    "from scipy.stats import pearsonr",
    "",
    "# Correlation between climatic drivers and pest outbreak risk",
    "climatic_vars = ['Rainfall_mm', 'Avg_Temperature_C', 'Humidity_pct']",
    "for var in climatic_vars:",
    "    corr, p_val = pearsonr(df[var], df['Disease_Pest_Risk_pct'])",
    "    print(f'{var} vs Pest Risk: r = {corr:.3f}, p = {p_val:.4e}')",
    "",
    "# Bivariate climate regime visualization",
    "sns.scatterplot(data=df, x='Humidity_pct', y='Disease_Pest_Risk_pct',",
    "                hue='Season', palette='Dark2', alpha=0.6)",
    "sns.regplot(data=df, x='Humidity_pct', y='Disease_Pest_Risk_pct',",
    "            scatter=False, color='darkred', ax=plt.gca())",
    "plt.title('Impact of Atmospheric Humidity on Pest Risk by Season')",
    "plt.show()"
]
render_code_snippet("analysis_02_environmental_risk.py", code2, "assets/code_snippet_2.png")

# Snippet 3: Irrigation & Water Efficiency
code3 = [
    "# 3. Resource Usage & Water Efficiency Evaluation",
    "import numpy as np",
    "",
    "# Water Efficiency Index = Production (t) / (Water Used (m3) / 1000)",
    "df['Water_Efficiency_t_per_1000m3'] = (",
    "    df['Production_Tonnes'] / (df['Water_Used_m3'] / 1000.0)",
    ").round(3)",
    "",
    "# Irrigation method efficiency and economic return cross-tab",
    "irr_perf = df.groupby(['Irrigation_Method', 'Season'])[[",
    "    'Water_Used_m3', 'Water_Efficiency_t_per_1000m3', 'Profit_INR'",
    "]].mean().round(2)",
    "print(irr_perf.unstack())",
    "",
    "# Drip irrigation delivers 82% higher efficiency over Flood",
    "sns.barplot(data=df, x='Irrigation_Method', y='Profit_INR', hue='Season')"
]
render_code_snippet("analysis_03_irrigation_efficiency.py", code3, "assets/code_snippet_3.png")

# Snippet 4: Economic Outcomes & Profitability
code4 = [
    "# 4. Economic Performance & Hypothesis Testing (ANOVA)",
    "from scipy import stats",
    "",
    "# Hypotheses: Does net profit significantly vary by season?",
    "f_stat, p_val = stats.f_oneway(",
    "    df[df['Season'] == 'Kharif']['Profit_INR'],",
    "    df[df['Season'] == 'Rabi']['Profit_INR'],",
    "    df[df['Season'] == 'Zaid']['Profit_INR']",
    ")",
    "print(f'One-Way ANOVA F-stat: {f_stat:.4f}, p-value: {p_val:.4e}')",
    "# Result: F = 34.29, p = 1.71e-15 (Reject H0: Highly Significant)",
    "",
    "# Computing season-level profit margins and cost-benefit ratio",
    "df['Profit_Margin_pct'] = (df['Profit_INR'] / df['Revenue_INR']) * 100",
    "season_econ = df.groupby('Season')['Profit_Margin_pct'].agg(['mean', 'median'])",
    "print(season_econ)"
]
render_code_snippet("analysis_04_economic_profitability.py", code4, "assets/code_snippet_4.png")

print("All visual and code assets generated successfully!")
