import streamlit as st
import re
import numpy as np
import spacy
import matplotlib.pyplot as plt

# Load NLP model (spaCy for entity recognition)
nlp = spacy.load("en_core_web_sm")

# Function to extract numerical values for demand and supply curves dynamically
def extract_equation_params(text):
    """
    Extracts demand and supply equation parameters from a natural language query.
    Dynamically assigns slope and intercept values based on detected keywords.
    """
    doc = nlp(text.lower())  # Process text with NLP
    numbers = [float(token.text) for token in doc if token.like_num]  # Extract all numerical values
   
    if len(numbers) < 4:
        return None  # Ensure we have at least 4 numbers
   
    # Initialize variables
    demand_slope = demand_intercept = supply_slope = supply_intercept = None
    demand_detected = supply_detected = False
   
    # Scan text for demand and supply keywords and match order dynamically
    for sent in doc.sents:
        sent_text = sent.text.lower()
       
        if "demand" in sent_text and not demand_detected:
            demand_detected = True
            if "intercept" in sent_text and numbers:
                demand_intercept = numbers.pop(0)
            if "slope" in sent_text and numbers:
                demand_slope = numbers.pop(0)
       
        if "supply" in sent_text and not supply_detected:
            supply_detected = True
            if "intercept" in sent_text and numbers:
                supply_intercept = numbers.pop(0)
            if "slope" in sent_text and numbers:
                supply_slope = numbers.pop(0)
   
    # Ensure values are correctly swapped if intercept and slope are reversed
    if demand_slope and demand_intercept and abs(demand_slope) > abs(demand_intercept):
        demand_slope, demand_intercept = demand_intercept, demand_slope
    if supply_slope and supply_intercept and abs(supply_slope) > abs(supply_intercept):
        supply_slope, supply_intercept = supply_intercept, supply_slope
   
    # Debugging: Display extracted values in Streamlit
    st.info(f"Extracted Values:\n Demand Intercept: {demand_intercept}\n Demand Slope: {demand_slope}\n Supply Intercept: {supply_intercept}\n Supply Slope: {supply_slope}")

    # Ensure all values are assigned correctly
    if None in (demand_slope, demand_intercept, supply_slope, supply_intercept):
        return None

    return demand_intercept, demand_slope, supply_intercept, supply_slope

# Code for the application
import streamlit as st
import re
import numpy as np
import spacy
import matplotlib.pyplot as plt

# Load NLP model (spaCy for entity recognition)
nlp = spacy.load("en_core_web_sm")

# Function to extract numerical values for demand and supply curves
def extract_equation_params(text):
    doc = nlp(text.lower())

    # Extract numbers and their associated words
    numbers = [float(token.text) for token in doc if token.like_num]

    # Assume format is always "demand slope, demand intercept, supply intercept, supply slope"
    if len(numbers) < 4:
        return None

    demand_slope, demand_intercept, supply_intercept, supply_slope = numbers
    return demand_slope, demand_intercept, supply_slope, supply_intercept

# Function to calculate equilibrium price and quantity
def calculate_equilibrium(demand_slope, demand_intercept, supply_slope, supply_intercept):
    # Solve for price and quantity where Qd = Qs
    price_equilibrium = (supply_intercept - demand_intercept) / (demand_slope - supply_slope)
    quantity_equilibrium = demand_slope * price_equilibrium + demand_intercept
    return round(price_equilibrium, 2), round(quantity_equilibrium, 2)

# Function to calculate consumer surplus
def calculate_consumer_surplus(demand_slope, demand_intercept, price_eq, quantity_eq):
    # Consumer surplus is the area of the triangle above the price and below the demand curve
    max_price = -demand_intercept / demand_slope  # Price when quantity is zero
    consumer_surplus = 0.5 * (max_price - price_eq) * quantity_eq
    return round(consumer_surplus, 2)

# Function to calculate producer surplus
def calculate_producer_surplus(supply_slope, supply_intercept, price_eq, quantity_eq):
    # Producer surplus is the area of the triangle below the price and above the supply curve
    min_price = supply_intercept  # Price when quantity is zero
    producer_surplus = 0.5 * (price_eq - min_price) * quantity_eq
    return round(producer_surplus, 2)

# Function to plot demand and supply curves
def plot_curves(demand_slope, demand_intercept, supply_slope, supply_intercept, price_eq, quantity_eq):
    # Generate a range of prices
    prices = np.linspace(0, max(price_eq * 2, 10), 100)

    # Calculate demand and supply quantities
    demand_quantities = demand_slope * prices + demand_intercept
    supply_quantities = supply_slope * prices + supply_intercept

    # Plot the curves
    plt.figure(figsize=(10, 6))
    plt.plot(demand_quantities, prices, label="Demand Curve", color="blue")
    plt.plot(supply_quantities, prices, label="Supply Curve", color="orange")

    # Highlight the equilibrium point
    plt.scatter(quantity_eq, price_eq, color="red", label="Equilibrium Point")
    plt.text(quantity_eq, price_eq, f'  ({quantity_eq}, {price_eq})', verticalalignment='bottom')

    # Add labels and title
    plt.xlabel("Quantity")
    plt.ylabel("Price")
    plt.title("Demand and Supply Curves")
    plt.legend()
    plt.grid(True)

    # Show the plot
    st.pyplot(plt)

# Streamlit App Interface
st.title("Linear Algebra Economics Helper")

st.write("Enter a question in natural language (e.g., 'Find the equilibrium for a demand curve with slope -4 and intercept 10 and a supply curve with an intercept of 2 and a slope of 5.')")

# User Input
user_query = st.text_area("Type your question here:", "")

if st.button("Solve"):
    params = extract_equation_params(user_query)

    if params:
        demand_slope, demand_intercept, supply_slope, supply_intercept = params
        price_eq, quantity_eq = calculate_equilibrium(demand_slope, demand_intercept, supply_slope, supply_intercept)

        # Calculate consumer and producer surplus
        consumer_surplus = calculate_consumer_surplus(demand_slope, demand_intercept, price_eq, quantity_eq)
        producer_surplus = calculate_producer_surplus(supply_slope, supply_intercept, price_eq, quantity_eq)

        # Display Results
        st.success(f"**Equilibrium Price:** ${price_eq}")
        st.success(f"**Equilibrium Quantity:** {quantity_eq} units")
        st.success(f"**Consumer Surplus:** ${consumer_surplus}")
        st.success(f"**Producer Surplus:** ${producer_surplus}")

        # Plot the curves
        plot_curves(demand_slope, demand_intercept, supply_slope, supply_intercept, price_eq, quantity_eq)
    else:
        st.error("Could not extract demand and supply equation parameters. Please format your question correctly.")
