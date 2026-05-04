import yfinance as yf
import pandas as pd

# Step 1: Define only required companies
companies = {
    "ABB": "ABB.NS",
    "Siemens": "SIEMENS.NS",
    "Schneider Electric": "SU.PA",
    "Havells": "HAVELLS.NS",
    "Crompton": "CROMPTON.NS"
}

data = []
projects_data = {
    "ABB": "Industrial automation, robotics, electrification",
    "Siemens": "Smart infrastructure, digital industries, mobility",
    "Schneider Electric": "Energy management, smart grids, sustainability",
    "Havells": "Consumer electricals, smart homes, lighting",
    "Crompton": "Fans, pumps, lighting solutions"
}

# Step 2: Fetch multi-year revenue
for name, ticker in companies.items():
    try:
        stock = yf.Ticker(ticker)
        financials = stock.financials

        if not financials.empty and "Total Revenue" in financials.index:
            revenues = financials.loc["Total Revenue"]

            for year, revenue in revenues.items():
                data.append({
                    "Company": name,
                    "Year": year.year,
                    "Revenue": revenue,
                    "Sector": "Electrical",
                    "Projects": projects_data.get(name, "N/A")
                })

    except Exception as e:
        print(f"Error fetching {name}: {e}")

# Step 3: Create DataFrame
df = pd.DataFrame(data)

# Step 4: Clean data
df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
df = df.dropna(subset=["Revenue"])

# Step 5: Sort properly
df = df.sort_values(["Company", "Year"])

# Step 6: Correct Growth Calculation
df["Growth %"] = df.groupby("Company")["Revenue"].pct_change() * 100

# Step 7: Save to CSV
df.to_csv("electrical_companies_data.csv", index=False)

print("✅ Final clean data saved!")
print(df)