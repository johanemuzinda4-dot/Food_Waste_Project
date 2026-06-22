import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🍲",
    layout="wide"
)

# 2. Shared DB connection config (FIX: avoid duplicating credentials everywhere)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "AJScores#111",
    "database": "food_waste_management_db"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# 3. Database Core Communication Engine
def fetch_data(query, params=None):
    try:
        conn = get_connection()
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Database Engine Connection Fault: {err}")
        return None

def execute_action(query, data=()):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        st.error(f"Write Execution Error: {err}")
        return False

# --- UNIFIED SIDEBAR NAVIGATION MATRIX ---
with st.sidebar:
    st.markdown("## 🍲 Food Wastage System")
    st.markdown("### **Author: Johane Muzinda**")
    st.markdown("*Connecting surplus with need*")
    st.markdown("---")
    
    menu_choice = st.radio(
        "Navigation Menu Paths:",
        [
            "📊 Dashboard Overview",
            "🔍 View & Filter Records",
            "✍️ Manage CRUD System",
            "💻 Analytics SQL (15)",
            "📈 Deep Data Analysis"
        ]
    )
    st.markdown("---")
    st.caption("⚙️ Engine Status: Fully Relational Connected")
    st.caption("📅 Session Sync: June 18, 2026")

# --- UNIFIED CONTROL BLOCK ROUTING ---

if menu_choice == "📊 Dashboard Overview":
    st.title("🌿 Local Food Wastage Management System")
    st.markdown("👨‍💻 **Developed by: Johane Muzinda**")
    st.markdown("### Combined Architecture: Multi-Table Relational KPIs & Live Pipeline Analytics")
    st.markdown("---")
    
    summary_df = fetch_data("""
        SELECT 
            (SELECT COUNT(*) FROM providers) as p_count,
            (SELECT COUNT(*) FROM receivers) as r_count,
            (SELECT SUM(Quantity) FROM food_listings) as fl_count,
            (SELECT COUNT(*) FROM claims) as c_count
    """)
    
    if summary_df is not None and not summary_df.empty:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1: st.metric(label="🏪 Total Providers", value=f"{int(summary_df['p_count'].iloc[0] or 0):,}")
        with kpi2: st.metric(label="❤️ Registered Receivers (NGOs)", value=f"{int(summary_df['r_count'].iloc[0] or 0):,}")
        with kpi3: st.metric(label="🍱 Total Inventory Meals", value=f"{int(summary_df['fl_count'].iloc[0] or 0):,}")
        with kpi4: st.metric(label="📝 Claims Logs Registered", value=f"{int(summary_df['c_count'].iloc[0] or 0):,}")

    st.markdown("###")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### 📍 Operational Supply Concentration across City Hubs")
        chart_data = fetch_data("SELECT Location, SUM(Quantity) as Total_Quantity FROM food_listings GROUP BY Location ORDER BY Total_Quantity DESC LIMIT 8;")
        if chart_data is not None and not chart_data.empty:
            fig = px.bar(chart_data, x="Location", y="Total_Quantity", color="Total_Quantity", color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### 📌 Current Settlements Status Breakdown")
        status_data = fetch_data("SELECT Status, COUNT(*) as Count FROM claims GROUP BY Status;")
        if status_data is not None and not status_data.empty:
            fig_pie = px.pie(status_data, names="Status", values="Count", hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
            st.plotly_chart(fig_pie, use_container_width=True)

elif menu_choice == "🔍 View & Filter Records":
    st.title("🔍 Multi-Dimensional Dataset Filtering Workbench")
    st.markdown("---")
    
    filter_target = st.selectbox("Select Target Database Matrix:", ["Food Listings Inventory", "Registered Providers", "Receiver Associations"])
    
    if filter_target == "Food Listings Inventory":
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            city_opts = fetch_data("SELECT DISTINCT Location FROM food_listings;")
            selected_city = st.multiselect("Filter by Target Location Zone:", city_opts['Location'].tolist() if city_opts is not None else [])
        with col_f2:
            type_opts = fetch_data("SELECT DISTINCT Food_Type FROM food_listings;")
            selected_type = st.multiselect("Filter by Food Dietary Category:", type_opts['Food_Type'].tolist() if type_opts is not None else [])

        # FIX: Use parameterized queries instead of f-string injection
        conditions = []
        params = []
        base_query = "SELECT * FROM food_listings WHERE 1=1"
        if selected_city:
            placeholders = ", ".join(["%s"] * len(selected_city))
            conditions.append(f"Location IN ({placeholders})")
            params.extend(selected_city)
        if selected_type:
            placeholders = ", ".join(["%s"] * len(selected_type))
            conditions.append(f"Food_Type IN ({placeholders})")
            params.extend(selected_type)
        query = base_query + ("" if not conditions else " AND " + " AND ".join(conditions))
        df_res = fetch_data(query, params=params if params else None)
        if df_res is not None:
            st.markdown(f"**Found {len(df_res)} matching records:**")
            st.dataframe(df_res, use_container_width=True)

    elif filter_target == "Registered Providers":
        prov_opts = fetch_data("SELECT DISTINCT Type FROM providers;")
        selected_p_type = st.multiselect("Filter by Institution Sector:", prov_opts['Type'].tolist() if prov_opts is not None else [])

        # FIX: Parameterized query
        params = []
        base_query = "SELECT * FROM providers WHERE 1=1"
        if selected_p_type:
            placeholders = ", ".join(["%s"] * len(selected_p_type))
            base_query += f" AND Type IN ({placeholders})"
            params.extend(selected_p_type)
        df_res = fetch_data(base_query, params=params if params else None)
        if df_res is not None:
            st.dataframe(df_res, use_container_width=True)
        
    else:
        df_res = fetch_data("SELECT * FROM receivers;")
        if df_res is not None:
            st.dataframe(df_res, use_container_width=True)

elif menu_choice == "✍️ Manage CRUD System":
    st.title("✍️ Live Database Row Manipulation Framework (CRUD)")
    st.markdown("---")
    
    crud_op = st.tabs(["➕ Insert New Batch", "📝 Update Existing Quantities", "🗑️ Delete Records"])
    
    with crud_op[0]:
        st.subheader("Add Live Food Batch Entry")
        f_name = st.text_input("Surplus Food Item Name:")
        f_qty = st.number_input("Batch Quantity Units:", min_value=1, value=10)
        f_exp = st.date_input("Batch Expiry Log Target:", datetime.now())
        f_loc = st.text_input("Operational Logistics City:")
        f_cat = st.selectbox("Food Categorization Group:", ["Vegetarian", "Non-Vegetarian", "Vegan", "Dairy Items", "Baked Goods"])
        f_meal = st.selectbox("Meal Time Type Allocation:", ["Breakfast", "Lunch", "Dinner", "Snacks"])
        f_pid = st.number_input("Authorized Provider Registry Identification Code (ID):", min_value=1, value=1)
        
        if st.button("Commit New Row to MySQL Instance"):
            if f_name and f_loc:
                success = execute_action(
                    "INSERT INTO food_listings (Food_Name, Quantity, Expiry_Date, Location, Food_Type, Meal_Type, Provider_ID) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                    (f_name, f_qty, str(f_exp), f_loc, f_cat, f_meal, f_pid)
                )
                if success:
                    st.success("Row item successfully added into MySQL table architecture.")
            else:
                st.warning("Please populate required fields before execution.")

    with crud_op[1]:
        st.subheader("Modify Target Record Parameters")
        up_id = st.number_input("Target Food ID Key Identifier:", min_value=1)
        new_qty = st.number_input("Revised System Quantity Level:", min_value=1)
        if st.button("Execute UPDATE Database Query"):
            success = execute_action("UPDATE food_listings SET Quantity = %s WHERE Food_ID = %s;", (new_qty, up_id))
            if success:
                st.success("Target database values updated.")

    with crud_op[2]:
        st.subheader("Drop Relational Record Entry Block")
        del_id = st.number_input("Delete Item Row Matching Food ID Key ID:", min_value=1)
        if st.button("Execute Dangerous DELETE Sequence", type="primary"):
            success = execute_action("DELETE FROM food_listings WHERE Food_ID = %s;", (del_id,))
            if success:
                st.error("Database structural index entry row dropped successfully.")

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
    
    # FIX: Initialize df to None so the render block below never hits NameError
    df = None

    if query_option.startswith("1."):
        df = fetch_data("SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Location, Food_Type FROM food_listings WHERE Expiry_Date <= '2026-06-30' ORDER BY Expiry_Date ASC;")
    elif query_option.startswith("2."):
        df = fetch_data("SELECT p.Name, p.Type, p.City, SUM(f.Quantity) as Total_Meals_Contributed FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID GROUP BY p.Provider_ID, p.Name, p.Type, p.City ORDER BY Total_Meals_Contributed DESC LIMIT 10;")
    elif query_option.startswith("3."):
        df = fetch_data("SELECT Location as City_Zone, SUM(Quantity) as Available_Stock FROM food_listings GROUP BY Location ORDER BY Available_Stock DESC;")
    elif query_option.startswith("4."):
        df = fetch_data("SELECT c.Claim_ID, f.Food_Name, r.Name as Receiver_Organization, c.Status, c.Timestamp FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID JOIN receivers r ON c.Receiver_ID = r.Receiver_ID WHERE c.Status = 'Pending' ORDER BY c.Timestamp ASC;")
    elif query_option.startswith("5."):
        df = fetch_data("SELECT Food_Type, COUNT(*) as Total_Batches, ROUND(AVG(DATEDIFF(Expiry_Date, '2026-06-16')), 1) as Avg_Days_Until_Expiry FROM food_listings GROUP BY Food_Type ORDER BY Avg_Days_Until_Expiry ASC;")
    elif query_option.startswith("6."):
        df = fetch_data("SELECT r.Name as Receiver_Name, r.Type, COUNT(c.Claim_ID) as Total_Claims_Made FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID GROUP BY r.Receiver_ID, r.Name, r.Type ORDER BY Total_Claims_Made DESC LIMIT 10;")
    elif query_option.startswith("7."):
        df = fetch_data("SELECT Status, COUNT(*) as Count FROM claims GROUP BY Status;")
    elif query_option.startswith("8."):
        df = fetch_data("SELECT p.Name as Donor_Provider, r.Name as Recipient_NGO, COUNT(c.Claim_ID) as Shared_Transactions FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID JOIN providers p ON f.Provider_ID = p.Provider_ID JOIN receivers r ON c.Receiver_ID = r.Receiver_ID GROUP BY p.Name, r.Name ORDER BY Shared_Transactions DESC LIMIT 15;")
    elif query_option.startswith("9."):
        df = fetch_data("SELECT HOUR(Timestamp) as Transaction_Hour, COUNT(*) as Activity_Count FROM claims GROUP BY HOUR(Timestamp) ORDER BY Transaction_Hour ASC;")
    elif query_option.startswith("10."):
        df = fetch_data("SELECT p.Provider_ID, p.Name, p.Type, p.Contact FROM providers p LEFT JOIN food_listings f ON p.Provider_ID = f.Provider_ID WHERE f.Food_ID IS NULL;")
    elif query_option.startswith("11."):
        # FIX: food_listings has no Provider_Type column; join providers to get Type
        df = fetch_data("""
            SELECT p.Type as Provider_Type, f.Location, SUM(f.Quantity) as Packaged_Volume
            FROM food_listings f
            JOIN providers p ON f.Provider_ID = p.Provider_ID
            GROUP BY p.Type, f.Location;
        """)
    elif query_option.startswith("12."):
        df = fetch_data("SELECT Status, COUNT(*) as Total_Claims, MIN(Timestamp) as Earliest_Log, MAX(Timestamp) as Latest_Log FROM claims GROUP BY Status;")
    elif query_option.startswith("13."):
        df = fetch_data("SELECT f.Food_Type, SUM(f.Quantity) as Supply_Volume, COUNT(c.Claim_ID) as Total_Demand_Claims FROM food_listings f LEFT JOIN claims c ON f.Food_ID = c.Food_ID GROUP BY f.Food_Type;")
    elif query_option.startswith("14."):
        df = fetch_data("SELECT f.Food_ID, f.Food_Name, f.Quantity, f.Expiry_Date FROM food_listings f LEFT JOIN claims c ON f.Food_ID = c.Food_ID AND c.Status = 'Accepted' WHERE f.Expiry_Date < '2026-06-16' AND c.Claim_ID IS NULL;")
    elif query_option.startswith("15."):
        df = fetch_data("""
            SELECT c.Claim_ID, p.Name as Donor_Name, f.Food_Name, f.Quantity, r.Name as Recipient_NGO, c.Status, c.Timestamp
            FROM claims c
            JOIN food_listings f ON c.Food_ID = f.Food_ID
            JOIN providers p ON f.Provider_ID = p.Provider_ID
            JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
            ORDER BY c.Timestamp DESC LIMIT 100;
        """)

    if df is not None:
        st.dataframe(df, use_container_width=True)
        st.markdown("#### 📊 Dynamic Query Visual Representation")
        
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
            fig = px.bar(df, x="Receiver_Name", y="Total_Claims_Made", title="Top 10 High Demand NGOs")
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
            fig = px.scatter(df, x="Supply_Volume", y="Total_Demand_Claims", text="Food_Type", size="Supply_Volume", title="Supply Volume vs Request Densities")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("System relational records for this specific query are cleanly rendered above in tabular matrix formatting.")

elif menu_choice == "📈 Deep Data Analysis":
    st.title("📈 Multi-Variable Exploratory Data Analysis Panel")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🍲 Total Volume Share by Food Categories")
        df1 = fetch_data("SELECT Food_Type, SUM(Quantity) as Quantity FROM food_listings GROUP BY Food_Type;")
        if df1 is not None:
            fig1 = px.bar(df1, x="Food_Type", y="Quantity", color="Quantity", color_continuous_scale="Tealgrn")
            st.plotly_chart(fig1, use_container_width=True)
            
        st.subheader("🏢 Operational Provider Type Ratios")
        df3 = fetch_data("SELECT Type, COUNT(*) as Count FROM providers GROUP BY Type;")
        if df3 is not None:
            fig3 = px.pie(df3, names="Type", values="Count", hole=0.4, color_discrete_sequence=px.colors.sequential.YlGnBu)
            st.plotly_chart(fig3, use_container_width=True)

        st.subheader("🗺️ Geographic Supply Hub Clusters")
        df5 = fetch_data("SELECT Location, COUNT(*) as Listings_Count FROM food_listings GROUP BY Location ORDER BY Listings_Count DESC LIMIT 10;")
        if df5 is not None:
            fig5 = px.bar(df5, y="Location", x="Listings_Count", orientation='h', color="Listings_Count", color_continuous_scale="Mint")
            st.plotly_chart(fig5, use_container_width=True)

    with col_b:
        st.subheader("🕒 Operational Claims Traffic by Hour Block")
        df2 = fetch_data("SELECT HOUR(Timestamp) as Hour, COUNT(*) as Logs FROM claims GROUP BY HOUR(Timestamp) ORDER BY Hour ASC;")
        if df2 is not None:
            fig2 = px.area(df2, x="Hour", y="Logs", color_discrete_sequence=["#4c78a8"])
            st.plotly_chart(fig2, use_container_width=True)
            
        st.subheader("📦 Meal Scheduling Category Weights")
        df4 = fetch_data("SELECT Meal_Type, SUM(Quantity) as Qty FROM food_listings GROUP BY Meal_Type;")
        if df4 is not None:
            fig4 = px.pie(df4, names="Meal_Type", values="Qty", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig4, use_container_width=True)

        st.subheader("📈 Core Trend: Monthly Allocation Metrics")
        # FIX: SUM(c.Claim_ID) sums arbitrary IDs — use COUNT(*) for meaningful totals
        df6 = fetch_data("SELECT MONTHNAME(Timestamp) as Month, COUNT(*) as Total_Count FROM claims GROUP BY MONTHNAME(Timestamp);")
        if df6 is not None and not df6.empty:
            fig6 = px.line(df6, x="Month", y="Total_Count", markers=True, color_discrete_sequence=["#e15759"])
            st.plotly_chart(fig6, use_container_width=True)
