# RentBuy Geneva — Project Proposal

## Project Title
RentBuy Geneva: Rent vs Buy Real-Estate Calculator with ML Market Predictions

## Category
Data Analysis + Machine Learning + Simulation

## Motivation
Deciding whether to rent or buy property in Geneva is one of the biggest financial decisions individuals face. Given high prices and strong renter protection laws, intuition is often wrong — people need **data-driven guidance**.

The goal is to build a tool that compares:

- Estimated monthly rent cost
- Total cost of buying (mortgage payments, taxes, maintenance, opportunity cost)
- Future property price predictions (machine learning model)

Final output will show:

> “Buying becomes better than renting after **X years** with **Y% probability**.”

## Data Source
- Geneva real estate price datasets (OpenData Geneva, ImmoScout24 scraping, FSO)
- Mortgage rates (SNB API or BFS dataset)
- Macroeconomic indicators: inflation, income index

## Approach
1. Collect data (CSV + scraping ImmoScout24 for home prices)
2. Clean & merge datasets using pandas
3. Machine learning model:
   - Regression model (predict price evolution after X years)
4. Financial simulation:
   - Monte Carlo simulation on economic assumptions
5. Output:
   - Visual comparison (rent vs buy over time)
   - Probability of buy > rent

## Expected Challenges
- Scraping / collecting usable real estate data
- Converting mortgage rules for Switzerland (down payment 20%, amortization)
- Time constraints

## Success Criteria
- A fully working calculator (CLI or notebook)
- Plot showing rent vs buy cost curves for Geneva
- ML model that predicts future price values
- Clean documentation and tests
