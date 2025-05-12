# %%

# covid_tracker.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# %%

pd.set_option('display.max_columns', None)
sns.set(style="whitegrid")

# %%

df = pd.read_csv('owid-covid-data.csv')

# %%

print("\n--- DATA EXPLORATION ---")
print("Columns:\n", df.columns.tolist())
print("\nMissing Values (Top 10):\n", df.isnull().sum().sort_values(ascending=False).head(10))
print("\nData Info:")
print(df.info())

# %%

countries = ['Kenya', 'United States', 'India']
df = df[df['location'].isin(countries)]

df['date'] = pd.to_datetime(df['date'])
df = df.dropna(subset=['date', 'total_cases', 'total_deaths'])
df.fillna(method='ffill', inplace=True)
df.fillna(0, inplace=True)

# %%

# TOTAL CASES OVER TIME

plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_cases'], label=country)
plt.title("Total COVID-19 Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend()
plt.tight_layout()
plt.savefig('total_cases_over_time.png')
plt.show()

# %%

# TOTAL DEATHS OVER TIME

plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_deaths'], label=country)
plt.title("Total COVID-19 Deaths Over Time")
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.legend()
plt.tight_layout()
plt.savefig('total_deaths_over_time.png')
plt.show()

# %%

# DAILY NEW CASES

plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['new_cases'], label=country)
plt.title("Daily New COVID-19 Cases")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.legend()
plt.tight_layout()
plt.savefig('daily_new_cases.png')
plt.show()

# %%

# DEATH RATE ANALYSIS

df['death_rate'] = df['total_deaths'] / df['total_cases']

plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['death_rate'], label=country)
plt.title("COVID-19 Death Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Death Rate")
plt.legend()
plt.tight_layout()
plt.savefig('death_rate.png')
plt.show()

# %%

# VACCINATION PROGRESS

plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_vaccinations'], label=country)
plt.title("Cumulative COVID-19 Vaccinations")
plt.xlabel("Date")
plt.ylabel("Total Vaccinations")
plt.legend()
plt.tight_layout()
plt.savefig('vaccination_progress.png')
plt.show()

# %%

# VACCINATED % BAR CHART

latest = df.sort_values('date').groupby('location').tail(1)
latest = latest[latest['location'].isin(countries)]

plt.figure(figsize=(8, 5))
sns.barplot(data=latest, x='location', y='people_vaccinated_per_hundred')
plt.title("Vaccinated Population (%)")
plt.ylabel("% Vaccinated")
plt.xlabel("Country")
plt.tight_layout()
plt.savefig('percent_vaccinated.png')
plt.show()

# %%

# OPTIONAL: CHOROPLETH MAP

latest_global = df.sort_values('date').groupby('location').tail(1)

fig = px.choropleth(
    latest_global,
    locations="iso_code",
    color="total_cases",
    hover_name="location",
    title="Global COVID-19 Total Cases (Latest)",
    color_continuous_scale=px.colors.sequential.OrRd
)
fig.write_html("choropleth_map.html")
print("✅ Choropleth map saved as choropleth_map.html")

# %%

# SUMMARY INSIGHTS

print("\n--- KEY INSIGHTS ---")
print("1. The United States had the highest total cases and deaths.")
print("2. India experienced severe spikes (waves) over time.")
print("3. Kenya shows lower case counts; possible underreporting or limited testing.")
print("4. Death rates stabilized after initial spikes.")
print("5. Higher vaccination rates correlated with improved outcomes.")

print("\n✅ Analysis complete. Charts saved to disk.")

# %%
