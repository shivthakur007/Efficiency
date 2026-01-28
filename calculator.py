import streamlit as st

st.title("Calculator🏦")

# Inputs
a = st.number_input("Enter first number", min_value = 0, step=100)
b = st.number_input("Enter second number", min_value = 0, step=100)

choose = st.selectbox("Choose the Operation",
            ("Addition", "Subtraction", "Multiplication", "Division"))
 
if st.button("Calculate"):
    if choose == "Addition":
        st.success(f"The sum is: {a+b}")
    elif choose == "Subtraction":
        st.success(f"The difference is: {a - b}")
    elif choose == "Multiplication":
        st.success(f"The Product is: {a * b}")
    elif choose == "Division": 
        st.success(f"The division is: {a / b} ")
    else:
        print("Invalid Operator")

  

 
