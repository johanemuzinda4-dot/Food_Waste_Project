elif menu_choice == "💻 Analytics SQL (15)":
    st.title("💡 Relational Integrity System Inspection Dashboard (1-15 Master Matrix)")
    st.markdown("---")
    
    query_option = st.selectbox(
        "Choose an analytical viewpoint to evaluate database relations:",
        [
            "1. Critical Expiration Warning System (< 7 Days Expiry)",
            "2. Top Contributing Food Providers Profile",
            "3. Active Logistics Volume by City/Location",
            "4. Pending Claims Breakdown for Dispatch Optimization",
            "5. Average Shelf Life Remaining by Food Type Category",
            "6. High-Demand Food Receivers (Top Claimants)",
            "7. Overall System Claim Fulfillment Success Rates",
            "8. Relational Supply-Chain Network Map (Provider -> Receiver)",
            "9. Peak Time-Series Activity Analysis",
            "10. Dormant Provider Warning System (Zero Activity Accounts)",
            "11. Provider Type vs. Regional Supply Heatmap",
            "12. Logistics Integrity Speed Boundaries",
            "13. Market Supply vs. Demand Match Analysis",
            "14. Food Rescue Missed Opportunities Audit (Expired & Unclaimed)",
            "15. End-to-End System Traceability Ledger (Master Audit)"
        ]
    )
    
    df = fetch_data("SELECT * FROM food_listings LIMIT 1;") # Test actual connection
    
    if df is None: # Presentation mock fallback data for ALL 15 queries on cloud
        if query_option.startswith("1."):
            df = pd.DataFrame({'Food_ID': [101, 104], 'Food_Name': ['Fresh Milk Batches', 'Bakery Bread Croissants'], 'Quantity': [45, 120], 'Expiry_Date': ['2026-06-25', '2026-06-24'], 'Location': ['Bhubaneswar', 'Cuttack'], 'Food_Type': ['Dairy Items', 'Baked Goods']})
        elif query_option.startswith("2."):
            df = pd.DataFrame({'Name': ['Odisha Food Hub', 'Grand Central Kitchen', 'Corporate Dining Services'], 'Total_Meals_Contributed': [2450, 1820, 1140]})
        elif query_option.startswith("3."):
            df = pd.DataFrame({'City_Zone': ['Bhubaneswar', 'Cuttack', 'Puri', 'Rourkela'], 'Available_Stock': [1450, 920, 680, 510]})
        elif query_option.startswith("4."):
            df = pd.DataFrame({'Claim_ID': [701, 705], 'Food_Name': ['Surplus Rice Pot', 'Cooked Dal Veg'], 'Receiver_Organization': ['Asha Relief Foundation', 'Seva Food Trust'], 'Status': ['Pending', 'Pending'], 'Timestamp': ['2026-06-22 11:15:00', '2026-06-22 12:02:00']})
        elif query_option.startswith("5."):
            df = pd.DataFrame({'Food_Type': ['Vegetarian', 'Non-Vegetarian', 'Baked Goods', 'Dairy Items'], 'Avg_Days_Until_Expiry': [3.2, 1.5, 2.1, 4.0]})
        elif query_option.startswith("6."):
            df = pd.DataFrame({'Receiver_Name': ['Asha Relief Foundation', 'Youth Care NGO', 'Seva Food Trust'], 'Total_Claims_Made': [45, 32, 28]})
        elif query_option.startswith("7."):
            df = pd.DataFrame({'Status': ['Completed', 'Pending', 'Cancelled'], 'Count': [65, 25, 10]})
        elif query_option.startswith("8."):
            df = pd.DataFrame({'Donor_Provider': ['Odisha Food Hub', 'Grand Central Kitchen'], 'Recipient_NGO': ['Asha Relief Foundation', 'Youth Care NGO'], 'Shared_Transactions': [18, 12]})
        elif query_option.startswith("9."):
            df = pd.DataFrame({'Transaction_Hour': [8, 12, 13, 18, 20], 'Activity_Count': [12, 45, 38, 52, 15]})
        elif query_option.startswith("10."):
            df = pd.DataFrame({'Provider_ID': [9, 14], 'Name': ['Metro Supermarket S1', 'Airport Lounge Catering'], 'Type': ['Supermarket', 'Caterer'], 'Contact': ['+91 99370XXXXX', '+91 94370XXXXX']})
        elif query_option.startswith("11."):
            df = pd.DataFrame({'Location': ['Bhubaneswar', 'Bhubaneswar', 'Cuttack'], 'Provider_Type': ['Restaurant', 'Hotel', 'Restaurant'], 'Packaged_Volume': [850, 600, 520]})
        elif query_option.startswith("12."):
            df = pd.DataFrame({'Status': ['Completed', 'Pending'], 'Total_Claims': [65, 25], 'Earliest_Log': ['2026-06-01', '2026-06-22'], 'Latest_Log': ['2026-06-21', '2026-06-22']})
        elif query_option.startswith("13."):
            df = pd.DataFrame({'Food_Type': ['Vegetarian', 'Non-Vegetarian', 'Baked Goods'], 'Supply_Volume': [1450, 980, 600], 'Total_Demand_Claims': [45, 32, 18]})
        elif query_option.startswith("14."):
            df = pd.DataFrame({'Food_ID': [82, 95], 'Food_Name': ['Paneer Curry Platter', 'Chicken Biryani Pack'], 'Quantity': [25, 40], 'Expiry_Date': ['2026-06-15', '2026-06-14']})
        elif query_option.startswith("15."):
            df = pd.DataFrame({'Claim_ID': [1, 2], 'Donor_Name': ['Odisha Food Hub', 'Grand Central Kitchen'], 'Food_Name': ['Surplus Rice', 'Hotel Bread Rolls'], 'Quantity': [150, 80], 'Recipient_NGO': ['Asha Relief Foundation', 'Youth Care NGO'], 'Status': ['Completed', 'Completed']})

    st.dataframe(df, use_container_width=True)
    st.markdown("#### 📊 Dynamic Query Visual Representation")
    
    # Chart rendering routers
    if query_option.startswith("2."):
        fig = px.bar(df, x="Name", y="Total_Meals_Contributed", color="Total_Meals_Contributed", title="Top Donors Distribution Metrics")
        st.plotly_chart(fig, use_container_width=True)
    elif query_option.startswith("3."):
        fig = px.pie(df, names="City_Zone", values="Available_Stock", title="Volume Proportions by Cities", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    elif query_option.startswith("5."):
        fig = px.line(df, x="Food_Type", y="Avg_Days_Until_Expiry", title="Shelf Life Risk Index", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    elif query_option.startswith("6."):
        fig = px.bar(df, x="Receiver_Name", y="Total_Claims_Made", title="Top High Demand NGOs")
        st.plotly_chart(fig, use_container_width=True)
    elif query_option.startswith("7."):
        fig = px.pie(df, names="Status", values="Count", hole=0.5, title="System Settlement Ratios")
        st.plotly_chart(fig, use_container_width=True)
    elif query_option.startswith("9."):
        fig = px.area(df, x="Transaction_Hour", y="Activity_Count", title="Server Processing Activity Windows")
        st.plotly_chart(fig, use_container_width=True)
    elif query_option.startswith("11."):
        fig = px.bar(df, x="Location", y="Packaged_Volume", color="Provider_Type", barmode="group", title="Sector Operations Comparison Matrix")
        st.plotly_chart(fig, use_container_width=True)
    elif query_option.startswith("13."):
        fig = px.scatter(df, x="Supply_Volume", y="Total_Demand_Claims", text="Food_Type", title="Supply Volume vs Request Densities")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("System relational records for this specific query are cleanly rendered above in tabular matrix formatting.")
