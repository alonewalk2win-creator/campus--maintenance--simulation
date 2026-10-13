import streamlit as st
import pandas as pd

st.set_page_config(page_title="CampusCare | Maintenance Control Center", page_icon="🏫", layout="wide")

st.markdown("""
<style>
.stApp{background:#f3f6fb;color:#17263d}
.block-container{max-width:1450px;padding-top:1.4rem}
.hero{background:linear-gradient(115deg,#102a43,#176b61);padding:28px 32px;border-radius:18px;color:white;margin-bottom:22px}
.hero h1{color:white;margin:0;font-size:2.25rem}
.hero p{color:#d8e9e8;margin:8px 0 0}
.kpi{background:white;border:1px solid #dfe7f0;border-radius:15px;padding:18px}
.kpi-label{color:#61748a;font-size:.9rem;font-weight:600}
.kpi-value{font-size:2rem;font-weight:800;color:#14253d}
.stTabs [data-baseweb="tab"]{font-weight:700}
</style>
""", unsafe_allow_html=True)

PRIORITY = {"High": 1, "Medium": 2, "Low": 3}
SEED = [
    {"ID":101,"Request":"Water leak inspection","Location":"Block A · Floor 1","Category":"Plumbing","Priority":"High","Hours left":1,"Technician":"Ravi","Status":"Open"},
    {"ID":102,"Request":"Lab projector issue","Location":"Science Lab","Category":"Electrical","Priority":"High","Hours left":2,"Technician":"Meena","Status":"Open"},
    {"ID":103,"Request":"Network room cooling","Location":"IT Block","Category":"HVAC","Priority":"High","Hours left":2,"Technician":"Arjun","Status":"Open"},
    {"ID":104,"Request":"Classroom fan repair","Location":"Block B · Room 204","Category":"Electrical","Priority":"Medium","Hours left":3,"Technician":"Ravi","Status":"Open"},
    {"ID":105,"Request":"Restroom tap repair","Location":"Main Building","Category":"Plumbing","Priority":"Medium","Hours left":4,"Technician":"Meena","Status":"Open"},
    {"ID":106,"Request":"Library light replacement","Location":"Library","Category":"Electrical","Priority":"Low","Hours left":5,"Technician":"Arjun","Status":"Open"},
    {"ID":107,"Request":"Desk repair","Location":"Block C · Room 12","Category":"Carpentry","Priority":"Low","Hours left":6,"Technician":"Ravi","Status":"Open"},
    {"ID":108,"Request":"Corridor cleaning","Location":"Admin Block","Category":"Cleaning","Priority":"Low","Hours left":5,"Technician":"Meena","Status":"Open"},
]

def reset_state():
    st.session_state.work_orders = [dict(x) for x in SEED]
    st.session_state.clock_hour = 8
    st.session_state.techs = 3
    st.session_state.next_id = 109
    st.session_state.activity = ["08:00 — Simulation initialized with 8 sample requests."]

if "work_orders" not in st.session_state:
    reset_state()

def log(message):
    st.session_state.activity.insert(0, f"{st.session_state.clock_hour:02d}:00 — {message}")
    st.session_state.activity = st.session_state.activity[:30]

def metric(label, value, note):
    st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div style="color:#718096;font-size:.8rem">{note}</div></div>', unsafe_allow_html=True)

def advance_hour():
    st.session_state.clock_hour += 1
    open_items = [x for x in st.session_state.work_orders if x["Status"] == "Open"]
    for item in open_items:
        item["Hours left"] -= 1
    queue = sorted([x for x in st.session_state.work_orders if x["Status"] == "Open"],
                   key=lambda x: (PRIORITY[x["Priority"]], x["Hours left"], x["ID"]))
    completed_now = queue[:min(st.session_state.techs, len(queue))]
    for item in completed_now:
        item["Status"] = "Completed"
    log(f"Advanced one hour; {len(completed_now)} request(s) completed by the priority-based queue.")

with st.sidebar:
    st.markdown("## 🏫 CampusCare")
    st.caption("Maintenance Control Center")
    page = st.radio("WORKSPACE", ["Dashboard", "Requests", "Simulation Lab", "Manual vs Database"])
    st.divider()
    st.markdown("### Quick controls")
    st.write(f"**Simulation time:** {st.session_state.clock_hour:02d}:00")
    st.write(f"**Technicians available:** {st.session_state.techs}")
    if st.button("⏭️ Advance 1 hour", use_container_width=True, type="primary"):
        advance_hour()
        st.rerun()
    c1,c2 = st.columns(2)
    with c1:
        if st.button("➕ Request surge", use_container_width=True):
            for title,cat,pri,hours in [("Urgent classroom repair","Electrical","High",2),("Additional plumbing request","Plumbing","Medium",4)]:
                st.session_state.work_orders.append({"ID":st.session_state.next_id,"Request":title,"Location":"Campus","Category":cat,"Priority":pri,"Hours left":hours,"Technician":"Unassigned","Status":"Open"})
                st.session_state.next_id += 1
            log("Two new maintenance requests added.")
            st.rerun()
    with c2:
        if st.button("🧰 Staff leave", use_container_width=True):
            st.session_state.techs = max(0, st.session_state.techs - 1)
            log("One technician marked unavailable.")
            st.rerun()
    if st.button("↻ Reset demo", use_container_width=True):
        reset_state()
        st.rerun()
    st.caption("Sample data · Educational simulation")

st.markdown("""
<div class="hero">
  <div style="font-size:.75rem;font-weight:800;letter-spacing:.14em;color:#9de1d1">CAMPUS OPERATIONS / LIVE DEMO</div>
  <h1>Maintenance Control Center</h1>
  <p>Monitor requests, deadlines, priority, and technician capacity in one place.</p>
</div>
""", unsafe_allow_html=True)

orders = st.session_state.work_orders
opened = [x for x in orders if x["Status"] == "Open"]
done = [x for x in orders if x["Status"] == "Completed"]
overdue = [x for x in opened if x["Hours left"] <= 0]
high = [x for x in opened if x["Priority"] == "High"]

if page == "Dashboard":
    st.subheader("Operations overview")
    cols = st.columns(4)
    with cols[0]: metric("OPEN REQUESTS",len(opened),"Waiting for action")
    with cols[1]: metric("COMPLETED",len(done),"Resolved in simulation")
    with cols[2]: metric("OVERDUE",len(overdue),"Deadline passed")
    with cols[3]: metric("HIGH PRIORITY",len(high),"Urgent attention")
    left,right = st.columns([1.6,1])
    with left:
        st.markdown("### 📋 Active work orders")
        if opened:
            st.dataframe(pd.DataFrame(opened), use_container_width=True, hide_index=True)
        else:
            st.success("All maintenance requests are completed.")
    with right:
        st.markdown("### 📊 Open requests by priority")
        counts = pd.DataFrame({"Requests":[sum(x["Priority"]==p for x in opened) for p in ["High","Medium","Low"]]},index=["High","Medium","Low"])
        st.bar_chart(counts)
        st.markdown("### 🧰 Technician capacity")
        st.progress(st.session_state.techs/5)
        st.write(f"{st.session_state.techs} of 5 technicians available")
    st.markdown("### 🕘 Recent activity")
    st.dataframe(pd.DataFrame({"Activity":st.session_state.activity[:8]}),use_container_width=True,hide_index=True)

elif page == "Requests":
    st.subheader("Maintenance request register")
    with st.expander("＋ Create a new request"):
        with st.form("create_request",clear_on_submit=True):
            title=st.text_input("Request title")
            location=st.text_input("Building / location")
            category=st.selectbox("Category",["Electrical","Plumbing","HVAC","Carpentry","Cleaning","Other"])
            priority=st.selectbox("Priority",["High","Medium","Low"])
            deadline=st.number_input("Deadline (hours)",min_value=1,max_value=72,value=4)
            tech=st.selectbox("Technician",["Unassigned","Ravi","Meena","Arjun","Priya","Kiran"])
            submit=st.form_submit_button("Add request",type="primary")
            if submit:
                if not title.strip():
                    st.error("Enter a request title.")
                else:
                    st.session_state.work_orders.append({"ID":st.session_state.next_id,"Request":title.strip(),"Location":location.strip() or "Not specified","Category":category,"Priority":priority,"Hours left":int(deadline),"Technician":tech,"Status":"Open"})
                    st.session_state.next_id += 1
                    log(f"Request added: {title.strip()}.")
                    st.success("Request added.")
                    st.rerun()
    f1,f2,f3=st.columns(3)
    with f1: status=st.selectbox("Filter status",["All","Open","Completed"])
    with f2: pri=st.selectbox("Filter priority",["All","High","Medium","Low"])
    with f3: query=st.text_input("Search")
    filtered=[x for x in orders if (status=="All" or x["Status"]==status) and (pri=="All" or x["Priority"]==pri) and query.lower() in (x["Request"]+" "+x["Location"]).lower()]
    st.dataframe(pd.DataFrame(filtered),use_container_width=True,hide_index=True)
    if opened:
        ids=[x["ID"] for x in opened]
        selected=st.selectbox("Mark a request completed",ids,format_func=lambda i:f"#{i} — {next(x['Request'] for x in opened if x['ID']==i)}")
        if st.button("✓ Complete selected request",type="primary"):
            for item in orders:
                if item["ID"]==selected: item["Status"]="Completed"
            log(f"Request #{selected} manually marked completed.")
            st.rerun()

elif page == "Simulation Lab":
    st.subheader("Hour-by-hour simulation")
    st.write("Advance time to reduce deadlines and let the database-style queue prioritize urgent work.")
    a,b,c=st.columns(3)
    with a: metric("SIMULATION TIME",f"{st.session_state.clock_hour:02d}:00","Current simulated hour")
    with b: metric("TECHNICIANS",st.session_state.techs,"Available capacity")
    with c: metric("OPEN QUEUE",len(opened),"Awaiting completion")
    if st.button("▶ Run next hour",type="primary"):
        advance_hour()
        st.rerun()
    st.markdown("### Deadlines and status")
    st.dataframe(pd.DataFrame(orders),use_container_width=True,hide_index=True)
    st.markdown("### Event log")
    st.dataframe(pd.DataFrame({"Event":st.session_state.activity}),use_container_width=True,hide_index=True)

else:
    st.subheader("Manual register vs database-style workflow")
    st.info("Educational comparison: manual processing is first-in, first-out; the database-style queue sorts by priority and deadline.")
    manual=sorted(opened,key=lambda x:x["ID"])
    database=sorted(opened,key=lambda x:(PRIORITY[x["Priority"]],x["Hours left"],x["ID"]))
    left,right=st.columns(2)
    with left:
        st.markdown("### 📒 Manual register")
        st.caption("Oldest request first")
        st.dataframe(pd.DataFrame([{"Order":i+1,"Request":x["Request"],"Priority":x["Priority"],"Hours left":x["Hours left"]} for i,x in enumerate(manual)]),use_container_width=True,hide_index=True)
    with right:
        st.markdown("### 🗃️ Database-style queue")
        st.caption("High priority and nearest deadline first")
        st.dataframe(pd.DataFrame([{"Order":i+1,"Request":x["Request"],"Priority":x["Priority"],"Hours left":x["Hours left"]} for i,x in enumerate(database)]),use_container_width=True,hide_index=True)
    st.markdown("### Current status")
    status_df=pd.DataFrame({"Status":["Open","Completed","Overdue"],"Requests":[len(opened),len(done),len(overdue)]}).set_index("Status")
    st.bar_chart(status_df)

st.divider()
st.caption("CampusCare · Campus Maintenance Simulation · Demo data only; no persistent database is connected.")

