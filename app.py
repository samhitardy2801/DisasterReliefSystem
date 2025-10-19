import streamlit as st
from supabase import create_client, Client
import folium
from streamlit_folium import st_folium
from datetime import date

# --- CONFIG ---
st.set_page_config(page_title="Disaster Relief Resource Allocation", layout="wide")

# --- SUPABASE CONNECTION ---
url = "https://knjsdmknmwfvfjimpllf.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtuanNkbWtubXdmdmZqaW1wbGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTAwNjYsImV4cCI6MjA3NjIyNjA2Nn0.A0HrKTFpqcFQVkMScI8GwqgPueomRR-tRO0ykEsYoKo"
supabase: Client = create_client(url, key)

# --- HEADER ---
st.title("🌐 Disaster Relief Resource Allocation")
st.markdown("Welcome! This platform helps coordinate relief requests, lost & found reports, and map-based disaster tracking.")

# --- SIDEBAR NAVIGATION ---
menu = st.sidebar.radio("Navigate", ["Dashboard", "Submit Request", "Lost & Found", "Safety Guidelines", "Map"])

# --- DASHBOARD ---
if menu == "Dashboard":
    st.header("📊 Relief Requests Dashboard")
    data = supabase.table("relief_requests").select("*").execute()
    if data.data:
        st.dataframe(data.data, use_container_width=True)
    else:
        st.info("No relief requests yet!")

# --- SUBMIT REQUEST FORM ---
elif menu == "Submit Request":
    st.header("📨 Submit a Help Request")

    with st.form("help_form"):
        name = st.text_input("Your Name")
        location = st.text_input("Location")
        need = st.text_area("Type of Need (Food, Medicine, Shelter...)")
        priority = st.selectbox("Priority Level", ["Critical", "High", "Medium", "Low"])
        submitted = st.form_submit_button("Submit Request")

        if submitted:
            if name and location and need:
                supabase.table("relief_requests").insert(
                    {"name": name, "location": location, "need": need, "priority": priority, "status": "Pending"}
                ).execute()
                st.success("✅ Relief request submitted successfully!")
            else:
                st.error("Please fill all required fields.")

# --- LOST & FOUND HUB ---
elif menu == "Lost & Found":
    st.header("🧍 Lost & Found Hub")

    lf_data = supabase.table("lost_found").select("*").execute()
    if lf_data.data:
        st.dataframe(lf_data.data, use_container_width=True)
    else:
        st.info("No lost/found reports yet.")

    tab1, tab2 = st.tabs(["Report Lost", "Report Found"])

    with tab1:
        with st.form("lost_form"):
            desc = st.text_area("Description")
            loc = st.text_input("Last Seen Location")
            dt = st.date_input("Date", date.today())
            contact = st.text_input("Contact Information")
            submit_lost = st.form_submit_button("Submit Lost Report")

            if submit_lost:
                if desc and loc and contact:
                    supabase.table("lost_found").insert(
                        {"type": "Lost", "description": desc, "location": loc, "date": str(dt), "contact": contact, "status": "Searching"}
                    ).execute()
                    st.success("🔴 Lost report added successfully!")
                else:
                    st.error("Please fill all fields.")

    with tab2:
        with st.form("found_form"):
            desc = st.text_area("Description")
            loc = st.text_input("Location Found")
            dt = st.date_input("Date", date.today())
            contact = st.text_input("Contact Information")
            submit_found = st.form_submit_button("Submit Found Report")

            if submit_found:
                if desc and loc and contact:
                    supabase.table("lost_found").insert(
                        {"type": "Found", "description": desc, "location": loc, "date": str(dt), "contact": contact, "status": "Waiting for Match"}
                    ).execute()
                    st.success("🟢 Found report added successfully!")
                else:
                    st.error("Please fill all fields.")

# --- SAFETY GUIDELINES ---
elif menu == "Safety Guidelines":
    st.header("⚠️ Disaster Do’s and Don’ts")

    disasterInfo = {
        "Cyclone": {
            "dos": [
                "Stay indoors and away from windows.",
                "Keep emergency kits, torches, food, and water ready.",
                "Listen to official weather and evacuation updates."
            ],
            "donts": [
                "Don’t go outside during strong winds or rain.",
                "Avoid using electrical appliances during the storm.",
                "Don’t ignore government evacuation orders."
            ]
        },
        "Flood": {
            "dos": [
                "Move to higher ground and stay alert for updates.",
                "Turn off power and gas supply before leaving your home.",
                "Keep emergency supplies and clean drinking water ready."
            ],
            "donts": [
                "Avoid walking or driving through floodwaters.",
                "Do not touch electric wires or poles in water.",
                "Don’t spread false information or panic."
            ]
        },
        "Earthquake": {
            "dos": [
                "Drop, Cover, and Hold On during tremors.",
                "Move to an open area after shaking stops.",
                "Keep an emergency contact and first aid kit handy."
            ],
            "donts": [
                "Don’t run outside during shaking.",
                "Avoid elevators and unstable furniture.",
                "Don’t use open flames until leaks are checked."
            ]
        },
        "Rainfall": {
            "dos": [
                "Use raincoats and waterproof shoes.",
                "Stay away from flooded roads and open drains.",
                "Check weather alerts before traveling."
            ],
            "donts": [
                "Don’t drive fast in heavy rain.",
                "Avoid sheltering under trees during lightning.",
                "Don’t ignore government rain warnings."
            ]
        },
        "Tsunami": {
            "dos": [
                "Move to higher ground or inland immediately.",
                "Listen to sirens, alerts, and official broadcasts.",
                "Keep emergency documents and essentials ready."
            ],
            "donts": [
                "Do not go near the shore to watch waves.",
                "Avoid returning to coastal areas too soon.",
                "Don’t ignore tsunami warning sirens."
            ]
        },
        "Landslide": {
            "dos": [
                "Stay away from steep slopes and loose rocks.",
                "Listen for warning sounds like cracking trees or soil movement.",
                "Evacuate immediately if you notice warning signs."
            ],
            "donts": [
                "Don’t travel near hills during heavy rainfall.",
                "Avoid building or staying near slope edges.",
                "Don’t block drainage paths with debris."
            ]
        },
        "Wildfire": {
            "dos": [
                "Follow official evacuation orders quickly.",
                "Wear masks to reduce smoke inhalation.",
                "Keep emergency supplies and water ready."
            ],
            "donts": [
                "Don’t burn garbage or dry leaves.",
                "Avoid driving near wildfire zones.",
                "Don’t block fire service access roads."
            ]
        },
        "Drought": {
            "dos": [
                "Conserve and reuse water wisely.",
                "Promote drought-resistant crops and trees.",
                "Report water leakages and broken pipelines."
            ],
            "donts": [
                "Don’t waste water unnecessarily.",
                "Avoid overusing groundwater.",
                "Don’t burn vegetation that can damage soil quality."
            ]
        }
    }

    disaster = st.selectbox("Select a Disaster", list(disasterInfo.keys()))
    if disaster:
        st.subheader(f"✅ Do’s for {disaster}")
        for d in disasterInfo[disaster]["dos"]:
            st.write(f"✔️ {d}")
        st.subheader(f"❌ Don’ts for {disaster}")
        for d in disasterInfo[disaster]["donts"]:
            st.write(f"🚫 {d}")

# --- MAP SECTION ---
elif menu == "Map":
    st.header("🗺️ Disaster Relief Map")
    m = folium.Map(location=[17.385, 78.4867], zoom_start=6)

    reqs = supabase.table("relief_requests").select("*").execute()
    if reqs.data:
        for r in reqs.data:
            color = (
                "red" if r["priority"] == "Critical"
                else "orange" if r["priority"] == "High"
                else "blue" if r["priority"] == "Medium"
                else "green"
            )
            folium.Marker(
                location=[17.385 + 0.1, 78.4867 + 0.1],
                popup=f"{r['name']} - {r['need']} ({r['priority']})",
                icon=folium.Icon(color=color),
            ).add_to(m)

    st_folium(m, width=700, height=450)
