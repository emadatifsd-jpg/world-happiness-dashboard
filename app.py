# ==========================
# World Happiness Dashboard (2016)
# ==========================

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# ---------------------------------
# 1. Load and clean the dataset
# ---------------------------------
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-AI0272EN-SkillsNetwork/labs/dataset/2016.csv"
df = pd.read_csv(url)

# Clean text columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Numeric columns
num_cols = [
    "Happiness Rank", "Happiness Score", "Economy (GDP per Capita)",
    "Family", "Health (Life Expectancy)", "Freedom",
    "Trust (Government Corruption)", "Generosity", "Dystopia Residual"
]

df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')
df[num_cols] = df[num_cols].fillna(df[num_cols].mean())

# ---------------------------------
# 2. Create Plotly Graphs
# ---------------------------------

# Top 10 happiest countries
top10 = df.nlargest(10, 'Happiness Score')
fig1 = px.bar(
    top10, x='Country', y='Happiness Score', color='Region',
    title='Top 10 Happiest Countries (2016)', text_auto=True
)

# Correlation heatmap
corr = df[num_cols].corr()
fig2 = px.imshow(
    corr, text_auto=True, color_continuous_scale='YlGnBu',
    title='Correlation between Happiness Factors (2016)'
)

# GDP vs Happiness
fig3 = px.scatter(
    df,
    x='Economy (GDP per Capita)',
    y='Happiness Score',
    color='Region',
    hover_name='Country',
    size='Health (Life Expectancy)',
    size_max=15,
    title='GDP per Capita vs Happiness Score'
)

# Pie chart
region_avg = df.groupby('Region')['Happiness Score'].mean().reset_index()
fig4 = px.pie(
    region_avg,
    values='Happiness Score',
    names='Region',
    title='Average Happiness Score by Region',
    hole=0.3
)

# Geo map
fig5 = px.scatter_geo(
    df,
    locations='Country',
    locationmode='country names',
    color='Economy (GDP per Capita)',
    hover_name='Country',
    size='Health (Life Expectancy)',
    projection='natural earth',
    title='Global GDP & Life Expectancy (2016)',
    color_continuous_scale='Viridis'
)

# ---------------------------------
# 3. Dashboard Layout
# ---------------------------------
app = Dash(__name__)
app.title = "World Happiness Dashboard"

app.layout = html.Div([
    html.H1("🌍 World Happiness Dashboard (2016)", style={'textAlign': 'center'}),

    html.Div([
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4),
        dcc.Graph(figure=fig5),
    ])
])

# ---------------------------------
# 4. Run
# ---------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
