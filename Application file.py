import streamlit as st
import numpy as np
import spacy
import matplotlib.pyplot as plt

# Load NLP model (spaCy for entity recognition)
nlp = spacy.load("en_core_web_sm")

# Function to extract numerical values for demand and supply curves dynamically
def extract_equation_params(text):
    doc = nlp(text.lower())  # Process text with NLP
    numbers = [float(token.text) for token in doc if token.like_num]  # Extract all numerical values
    
    if len(numbers) < 4:
        return None  # Ensure we have at least 4 numbers
    
    demand_slope, demand_intercept, supply_intercept, supply_slope = numbers[:4]
    return demand_slope, demand_intercept, supply_slope, supply_intercept

# Function to calculate equilibrium price and quantity
def calculate_equilibrium(demand_slope, demand_intercept, supply_slope, supply_intercept):
    price_eq = (supply_intercept - demand_intercept) / (demand_slope - supply_slope)
    quantity_eq = demand_slope * price_eq + demand_intercept
    return round(price_eq, 2), round(quantity_eq, 2)

# Function to calculate consumer surplus
def calculate_consumer_surplus(demand_slope, demand_intercept, price_eq, quantity_eq):
    max_price = -demand_intercept / demand_slope  # Price when quantity is zero
    return round(0.5 * (max_price - price_eq) * quantity_eq, 2)

# Function to calculate producer surplus
def calculate_producer_surplus(supply_slope, supply_intercept, price_eq, quantity_eq):
    min_price = supply_intercept  # Price when quantity is zero
    return round(0.5 * (price_eq - min_price) * quantity_eq, 2)

# Function to plot demand and supply curves
def plot_curves(demand_slope, demand_intercept, supply_slope, supply_intercept, price_eq, quantity_eq):
    prices = np.linspace(0, max(price_eq * 2, 10), 100)
    demand_quantities = demand_slope * prices + demand_intercept
    supply_quantities = supply_slope * prices + supply_intercept

    plt.figure(figsize=(10, 6))
    plt.plot(demand_quantities, prices, label="Demand Curve", color="blue")
    plt.plot(supply_quantities, prices, label="Supply Curve", color="orange")
    plt.scatter(quantity_eq, price_eq, color="red", label="Equilibrium Point")
    plt.text(quantity_eq, price_eq, f'  ({quantity_eq}, {price_eq})', verticalalignment='bottom')
    plt.xlabel("Quantity")
    plt.ylabel("Price")
    plt.title("Demand and Supply Curves")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Streamlit App Interface
st.title("Linear Algebra Economics Helper")
st.write("Enter a question in natural language (e.g., 'Find the equilibrium for a demand curve with slope -4 and intercept 10 and a supply curve with an intercept of 2 and a slope of 5.')")

user_query = st.text_area("Type your question here:", "")

if st.button("Solve"):
    params = extract_equation_params(user_query)
    
    if params:
        demand_slope, demand_intercept, supply_slope, supply_intercept = params
        price_eq, quantity_eq = calculate_equilibrium(demand_slope, demand_intercept, supply_slope, supply_intercept)
        consumer_surplus = calculate_consumer_surplus(demand_slope, demand_intercept, price_eq, quantity_eq)
        producer_surplus = calculate_producer_surplus(supply_slope, supply_intercept, price_eq, quantity_eq)
        
        st.success(f"**Equilibrium Price:** ${price_eq}")
        st.success(f"**Equilibrium Quantity:** {quantity_eq} units")
        st.success(f"**Consumer Surplus:** ${consumer_surplus}")
        st.success(f"**Producer Surplus:** ${producer_surplus}")
        
        plot_curves(demand_slope, demand_intercept, supply_slope, supply_intercept, price_eq, quantity_eq)
    else:
        st.error("Could not extract demand and supply equation parameters. Please format your question correctly.")
