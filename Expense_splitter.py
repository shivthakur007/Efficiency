import streamlit as st

st.title("💸 Trip Expense Splitter")

# Names
people = ["Shiv", "Sneha", "Mantej", "Pratham", "Tanya"]

st.subheader("Enter amount paid by each person")

payments = []

for person in people:
    amount = st.number_input(
        f"{person} paid (₹)",
        min_value=0.0,
        step=100.0
    )
    payments.append(amount)

if st.button("Calculate Split"):
    total_expense = sum(payments)
    num_people = len(people)
    share = total_expense / num_people if num_people > 0 else 0

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
