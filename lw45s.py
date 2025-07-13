import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="🏠 Electric Fitting Estimator", layout="centered")
st.title("🏠 Electric Fitting Cost Estimator")
st.markdown("Estimate your house's electric fitting cost based on number of rooms, size, and wire thickness.")

# --- Cost Constants ---
COST_PER_LIGHT = 150
COST_PER_FAN = 1200
COST_PER_SWITCH = 40
COST_PER_SOCKET = 120
COST_PER_MCB = 500

WIRE_COST = {
    "1.0 mm": 20,
    "1.5 mm": 30,
    "2.5 mm": 40,
    "4.0 mm": 60
}

# --- User Inputs ---
st.sidebar.header("🏠 Room Details")

num_rooms = st.sidebar.number_input("Number of Rooms", min_value=1, value=2)
num_halls = st.sidebar.number_input("Number of Halls", min_value=0, value=1)

room_area = st.sidebar.number_input("Average Area of a Room (sq. ft.)", min_value=50, value=120)
hall_area = st.sidebar.number_input("Average Area of a Hall (sq. ft.)", min_value=100, value=180)

wire_size = st.sidebar.selectbox("Select Wire Thickness", options=list(WIRE_COST.keys()))

# --- Logic: Calculate number of items per sq. ft. ---
total_area = (num_rooms * room_area) + (num_halls * hall_area)

# Estimate fittings based on area
lights = int(total_area // 50)         # 1 light per 50 sq ft
fans = int(total_area // 120)          # 1 fan per 120 sq ft
switches = lights + fans
sockets = int(total_area // 100)       # 1 socket per 100 sq ft
mcb = 1                                # Assume 1 MCB Box

# Estimate wiring: assume 10 meters per 100 sq. ft.
wiring_length = int((total_area / 100) * 10)

# --- Cost Calculation ---
total_cost = (
    lights * COST_PER_LIGHT +
    fans * COST_PER_FAN +
    switches * COST_PER_SWITCH +
    sockets * COST_PER_SOCKET +
    mcb * COST_PER_MCB +
    wiring_length * WIRE_COST[wire_size]
)

# --- Show Estimation ---
st.subheader("📊 Cost Estimation Summary")
st.write(f"🧱 Total Area: {total_area} sq. ft.")
st.write(f"🔌 Estimated Lights: {lights}")
st.write(f"🌀 Estimated Fans: {fans}")
st.write(f"🎚️ Estimated Switches: {switches}")
st.write(f"🔌 Estimated Power Sockets: {sockets}")
st.write(f"🧯 Wire Length Required: {wiring_length} meters ({wire_size})")
st.write(f"📦 MCB Box: {mcb}")

st.markdown("---")
st.success(f"💰 **Total Estimated Cost: ₹{total_cost}**")

# --- Tip Section ---
with st.expander("📌 Tips"):
    st.write("- Always keep 10–15% extra wiring for flexibility.")
    st.write("- For kitchen and AC, use 2.5 mm or 4 mm wire.")
    st.write("- Confirm socket placements with an electrician.")
