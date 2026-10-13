
import streamlit as st

st.set_page_config(
    page_title="Campus Maintenance Simulation",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 Campus Maintenance Simulation")
st.write("Compare manual registers with a database-style workflow.")

option = st.sidebar.selectbox(
    "Choose a system",
    ["Manual Register", "Database System"]
)

if option == "Manual Register":
    st.subheader("📒 Manual Register")
    st.info("Maintenance requests are tracked manually.")
else:
    st.subheader("🗃️ Database System")
    st.success("Requests can be organized by priority and deadline.")

if st.button("Advance Simulation"):
    st.success("Simulation advanced successfully!")
