import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Set Streamlit page config
st.set_page_config(page_title="🏠 PG Price Predictor", layout="centered")

st.title("🏠 PG Price Predictor")
st.write("Predict the monthly PG price based on room sharing, AC, and food.")

# --- Sample training data ---
data = {
    'Persons': [1, 2, 2, 3, 3, 1, 1, 2, 3],
    'AC': [1, 1, 0, 1, 0, 0, 1, 0, 1],         # 1 = AC, 0 = Non-AC
    'Food': [1, 0, 1, 1, 0, 1, 1, 0, 1],        # 1 = Food Included
    'Price': [9000, 6500, 5500, 5000, 4000, 8500, 9500, 5200, 4800]  # in ₹
}
df = pd.DataFrame(data)

# --- Train model ---
X = df[['Persons', 'AC', 'Food']]
y = df['Price']
model = LinearRegression().fit(X, y)

# --- Sidebar input ---
st.sidebar.header("📝 Your Room Preferences")

persons = st.sidebar.selectbox("Number of Persons in Room", [1, 2, 3])
ac_room = st.sidebar.radio("Room Type", ["AC", "Non-AC"])
food = st.sidebar.radio("Food Included", ["Yes", "No"])

# Convert input to model-ready format
ac_flag = 1 if ac_room == "AC" else 0
food_flag = 1 if food == "Yes" else 0

# Predict price
input_features = [[persons, ac_flag, food_flag]]
predicted_price = model.predict(input_features)[0]

# --- Show prediction ---
st.subheader("💰 Estimated Monthly PG Rent")
st.success(f"For a {persons}-person {'AC' if ac_flag else 'Non-AC'} room with{'out' if not food_flag else ''} food: ₹{predicted_price:.2f}")

# --- Show training data (optional) ---
with st.expander("📂 Show Sample Training Data"):
    st.dataframe(df)

# --- Show model info (optional) ---
with st.expander("📈 Model Equation"):
    coef = model.coef_
    intercept = model.intercept_
    st.code(f"Price = {coef[0]:.2f} × Persons + {coef[1]:.2f} × AC + {coef[2]:.2f} × Food + {intercept:.2f}")
import pandas as pd
from sklearn.linear_model import LinearRegression

# Sample data: You can expand this as needed
data = {
    'Persons': [1, 2, 2, 3, 3, 1, 1, 2, 3],
    'AC': [1, 1, 0, 1, 0, 0, 1, 0, 1],         # 1 = AC, 0 = Non-AC
    'Food': [1, 0, 1, 1, 0, 1, 1, 0, 1],        # 1 = Food Included
    'Price': [9000, 6500, 5500, 5000, 4000, 8500, 9500, 5200, 4800]  # in INR
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Features and Target
X = df[['Persons', 'AC', 'Food']]
y = df['Price']

# Train the model
model = LinearRegression()
model.fit(X, y)

# --- User Input Example ---
# Let's say user selects: 2 persons, AC room, food included
user_input = [[2, 1, 1]]  # 2 persons, AC=1, Food=1
predicted_price = model.predict(user_input)[0]

# Show result
print("🔮 Predicted PG Price:")
print(f"For 2 persons in an AC room with food: ₹{predicted_price:.2f}")
