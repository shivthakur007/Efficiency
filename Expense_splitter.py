import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trip Expense Splitter", layout="centered")

st.title("💸 Trip Expense Splitter")

# ----------------------------
# Number of people
# ----------------------------
num_people = st.number_input(
    "Enter number of people",
    min_value=1,
    step=1
)

people = []
payments = []

st.subheader("👥 Enter Names")

for i in range(num_people):
    name = st.text_input(f"Name of person {i+1}", key=f"name_{i}")
    people.append(name)

st.subheader("💰 Enter Amount Paid")

for i in range(num_people):
    amount = st.number_input(
        f"{people[i] if people[i] else 'Person ' + str(i+1)} paid (₹)",
        min_value=0.0,
        step=100.0,
        key=f"pay_{i}"
    )
    payments.append(amount)

# ----------------------------
# Calculate Split
# ----------------------------
if st.button("Calculate Split"):

    if "" in people:
        st.warning("⚠ Please enter all names.")
    else:
        total_expense = sum(payments)
        share = total_expense / num_people

        st.divider()
        st.subheader("📊 Expense Summary")

        st.write(f"**Total Expense:** ₹ {total_expense}")
        st.write(f"**Each Person Should Pay:** ₹ {round(share, 2)}")

        # ----------------------------
        # Settlement calculation
        # ----------------------------
        balance = {}
        for i in range(num_people):
            balance[people[i]] = round(payments[i] - share, 2)

        creditors = []
        debtors = []

        for person, amount in balance.items():
            if amount > 0:
                creditors.append([person, amount])
            elif amount < 0:
                debtors.append([person, abs(amount)])

        st.divider()
        st.subheader("💸 Who Pays Whom")

        settlements = []

        i = j = 0
        while i < len(debtors) and j < len(creditors):
            debtor, debt_amt = debtors[i]
            creditor, cred_amt = creditors[j]

            pay = min(debt_amt, cred_amt)

            settlements.append({
                "From": debtor,
                "To": creditor,
                "Amount (₹)": pay
            })

            debtors[i][1] -= pay
            creditors[j][1] -= pay

            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1

        for s in settlements:
            st.write(f"➡ **{s['From']} pays ₹{s['Amount (₹)']} to {s['To']}**")

        # ----------------------------
        # Save Trip History
        # ----------------------------
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({
            "People": ", ".join(people),
            "Total Expense": total_expense,
            "Each Share": round(share, 2)
        })

        # ----------------------------
        # Export to CSV (NO DEPENDENCY ISSUES)
        # ----------------------------
        df = pd.DataFrame(settlements)

        if not df.empty:
            st.divider()
            st.subheader("📥 Download Settlement")

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download CSV File",
                data=csv,
                file_name="trip_settlement.csv",
                mime="text/csv"
            )

# ----------------------------
# Trip History
# ----------------------------
if "history" in st.session_state and len(st.session_state.history) > 0:
    st.divider()
    st.subheader("🕒 Trip History (This Session)")

    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df)
