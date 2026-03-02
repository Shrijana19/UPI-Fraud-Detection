import streamlit as st
import matplotlib.pyplot as plt
from graph_engine import GraphEngine
from behavior_engine import BehaviorEngine
from ml_engine import MLEngine
from risk_engine import RiskEngine
import networkx as nx

st.set_page_config(layout="wide")

st.title("🛡 Real-Time UPI Fraud Prevention Engine")

graph_engine = GraphEngine()
behavior_engine = BehaviorEngine()
ml_engine = MLEngine()
risk_engine = RiskEngine()

st.sidebar.header("Enter Transaction")

sender = st.sidebar.selectbox("Sender", ["U1", "U2", "U3"])
receiver = st.sidebar.selectbox("Receiver", ["U1", "U2", "U3"])
amount = st.sidebar.number_input("Amount", min_value=100)
hour = st.sidebar.slider("Transaction Hour", 0, 23, 12)
device = st.sidebar.selectbox("Device", ["Android", "iPhone", "NewDevice"])
city = st.sidebar.selectbox("City", ["Delhi", "Mumbai", "Kolkata", "Chennai"])

if st.sidebar.button("Process Transaction"):

    graph_engine.add_transaction(sender, receiver, amount)

    ml_prob = ml_engine.predict_probability(amount)
    graph_risk, graph_exp = graph_engine.compute_graph_risk(receiver)
    behavior_risk, behavior_exp = behavior_engine.compute_behavior_risk(
        sender, amount, hour, device, city
    )

    final_risk = risk_engine.aggregate_risk(ml_prob, graph_risk, behavior_risk)
    decision = risk_engine.make_decision(final_risk)

    st.subheader("📊 Risk Analysis")
    st.write(f"ML Probability: {round(ml_prob,2)}")
    st.write(f"Graph Risk: {round(graph_risk,2)}")
    st.write(f"Behavior Risk: {round(behavior_risk,2)}")
    st.write(f"### Final Risk Score: {round(final_risk,2)}")

    if decision == "APPROVED":
        st.success("✅ Transaction Approved")
    elif decision == "STEP-UP AUTH":
        st.warning("🟡 Step-Up Authentication Required")
    else:
        st.error("🔴 Transaction Blocked")

    st.subheader("🔍 Risk Breakdown")
    st.write("Graph Factors:", graph_exp)
    st.write("Behavior Factors:", behavior_exp)

    st.subheader("🌐 Transaction Graph")

    fig, ax = plt.subplots()
    colors = []
    for node in graph_engine.G.nodes():
        if node == receiver and final_risk > 0.7:
            colors.append("red")
        else:
            colors.append("green")

    nx.draw(graph_engine.G, with_labels=True, node_color=colors, ax=ax)
    st.pyplot(fig)
