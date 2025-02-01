import streamlit as st
import re
import numpy as np
import spacy
import matplotlib.pyplot as plt

# Load spaCy model (ensure it's installed)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("spaCy model 'en_core_web_sm' not found. Please run: `python -m spacy download en_core_web_sm`")
    st.stop()

# Function to extract equation parameters
def extract_equation_params(equation: str):
    pattern = r"(\d*\.?\d*)\s*\*\s*Q\s*([+-])\s*(\d*\.?\d*)"
    match = re.search(pattern, equation.replace(" ", ""))

    if match:
        a = float(match.group(1)) if match.group(1) else 1
        sign = 1 if match.group(2) == "+" else -1
        b = float(match.group(3)) * sign if match.group(3) else 0
        return a, b
    else:
        return None

# Streamlit UI
st.title("Demand-Supply Curve Visualizer 📊")

# User input for demand equation
demand_equation = st.text_input("Enter demand equation (e.g., `10*Q + 50`):")

# User input for supply equation
supply_equation = st.text_input("Enter supply equation (e.g., `5*Q + 20`):")

if demand_equation and supply_equation:
    demand_params = extract_equation_params(demand_equation)
    supply_params = extract_equation_params(supply_equation)

    if not demand_params or not supply_params:
        st.error("Invalid equation format. Please use the form `a*Q + b` or `a*Q - b`.")
    else:
        a_d, b_d = demand_params
        a_s, b_s = supply_params

        # Generate Q values
        Q_values = np.linspace(0, 100, 100)

        # Calculate price values
        demand_prices = a_d * Q_values + b_d
        supply_prices = a_s * Q_values + b_s

        # Find equilibrium (where demand = supply)
        equilibrium_Q = (b_s - b_d) / (a_d - a_s) if a_d != a_s else None
        equilibrium_P = a_d * equilibrium_Q + b_d if equilibrium_Q is not None else None

        # Plot curves
        fig, ax = plt.subplots()
        ax.plot(Q_values, demand_prices, label="Demand Curve", color="blue")
        ax.plot(Q_values, supply_prices, label="Supply Curve", color="red")

        if equilibrium_Q is not None and 0 <= equilibrium_Q <= 100:
            ax.scatter([equilibrium_Q], [equilibrium_P], color="green", zorder=5)
            ax.annotate(f"Equilibrium ({equilibrium_Q:.2f}, {equilibrium_P:.2f})",
                        (equilibrium_Q, equilibrium_P), textcoords="offset points",
                        xytext=(-15,10), ha="center", fontsize=10, color="green")

        ax.set_xlabel("Quantity (Q)")
        ax.set_ylabel("Price (P)")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)
