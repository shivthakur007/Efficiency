import streamlit as st

st.title("💸 Trip Expense Splitter")

# Step 1: Number of people
num_people = st.number_input(
    "Enter number of people",
    min_value=1,
    step=1
)

people = []
payments = []

# Step 2: Enter names
st.subheader("Enter names")

for i in range(num_people):
    name = st.text_input(f"Name of person {i+1}")
    people.append(name)

# Step 3: Enter payments
st.subheader("Enter amount paid")

for i in range(num_people):
    if people[i] != "":
        amount = st.number_input(
            f"{people[i]} paid (₹)",
            min_value=0.0,
            step=100.0,
            key=f"payment_{i}"
        )
        payments.append(amount)
    else:
        payments.append(0.0)

# Step 4: Calculate
if st.button("Calculate Split"):

    if "" in people:
        st.warning("Please enter all names before calculating.")
    else:
        total_expense = sum(payments)
        share = total_expense / num_people

        st.divider()
        st.subheader("📊 Summary")

        st.write(f"**Total Expense:** ₹ {total_expense}")
        st.write(f"**Each Person Should Pay:** ₹ {share}")

        st.divider()
        st.subheader("💰 Settlement Details")

        for i in range(num_people):
            difference = payments[i] - share

            if difference > 0:
                st.success(f"{people[i]} should get back ₹ {difference}")
            elif difference < 0:
                st.error(f"{people[i]} owes ₹ {abs(difference)}")
            else:
                st.info(f"{people[i]} has settled exactly")
