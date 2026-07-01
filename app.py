import streamlit as st
import google.generativeai as genai
from clues import LOCATIONS
from evidence_details import EVIDENCE_INFO
from suspects import SUSPECTS

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Campus Conspiracy - AI Detective Thriller",
    page_icon="🕵️",
    layout="wide"
)

# --- GEMINI API SETUP ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    model = None

# --- DETECTIVE NOIR CUSTOM CSS ---
st.markdown("""
<style>
/* FULL DARK THEME & HEADER REMOVAL */
header, [data-testid="stHeader"], .stAppHeader, #MainMenu {
    background-color: transparent !important;
    display: none !important;
}

.stApp {
    background-color: #0b0f19;
    color: #f3f4f6;
    padding-top: 0px !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #f59e0b !important;
    font-family: 'Courier New', Courier, monospace;
    text-shadow: 0 0 8px rgba(245, 158, 11, 0.3);
}

/* SLEEK DARK SIDEBAR OVERRIDE */
section[data-testid="stSidebar"], [data-testid="stSidebar"], .stSidebar {
    background-color: #0f172a !important;
    border-right: 1px solid #1e293b !important;
}

[data-testid="stSidebar"] *, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, 
[data-testid="stSidebar"] p, [data-testid="stSidebar"] h4 {
    color: #f8fafc !important;
}

/* CARDS AND PADS */
.detective-badge-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 2px solid #f59e0b;
    border-radius: 24px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 10px 35px rgba(245, 158, 11, 0.25);
    margin-top: 20px;
}

.suspect-profile-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 15px;
}

.evidence-box {
    background: rgba(30, 41, 59, 0.9);
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 12px;
}

/* BUTTON OVERRIDES */
.stButton > button {
    background: linear-gradient(135deg, #d97706, #b45309) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: 1px solid #f59e0b !important;
    padding: 8px 18px !important;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #f59e0b, #d97706) !important;
    box-shadow: 0 6px 18px rgba(245, 158, 11, 0.5) !important;
}
</style>
""", unsafe_allow_html=True)

# --- SUSPECT PORTRAITS & WEAKNESS MAPPING ---
SUSPECT_METADATA = {
    "Nisha Verma": {"portrait": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300", "weakness": "Borrowed Book Record", "role": "Librarian"},
    "Rohan Malhotra": {"portrait": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300", "weakness": "Security Camera Footage", "role": "Security Head"},
    "Karan Mehta": {"portrait": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300", "weakness": "Deleted Email", "role": "Research Assistant"},
    "Dr. Meera Kapoor": {"portrait": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300", "weakness": "Torn Note", "role": "Senior Assistant"},
    "Vikram Rao": {"portrait": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300", "weakness": "Lab Access Log", "role": "Lab Technician"},
    "Aarav Sharma": {"portrait": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=300", "weakness": "Login History", "role": "Failed Student"}
}

# --- SESSION STATE INITIALIZATION ---
if "detective_name" not in st.session_state:
    st.session_state.detective_name = ""
if "evidence" not in st.session_state:
    st.session_state.evidence = []
if "score" not in st.session_state:
    st.session_state.score = 100
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "suspect_stress" not in st.session_state:
    st.session_state.suspect_stress = {s: 15 for s in SUSPECTS.keys()}
if "usb_unlocked" not in st.session_state:
    st.session_state.usb_unlocked = False

# ==============================================================================
# SCREEN 1: DETECTIVE REGISTRATION DASHBOARD
# ==============================================================================
if not st.session_state.detective_name:
    st.markdown("""
    <div class="detective-badge-card">
        <h1 style="font-size: 44px; margin-bottom:0;">🕵️ CAMPUS CONSPIRACY</h1>
        <h3 style="color:#cbd5e1 !important; margin-top:5px;">Case File #409: The Missing Professor</h3>
        <p style="font-size: 18px; color: #94a3b8; max-width:700px; margin: 15px auto;">Professor Sharma disappeared after discovering an illegal AI research project. 6 suspects hold secrets. Enter your credentials to take command of the investigation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        d_name = st.text_input("Enter Your Detective Name / Badge ID:", placeholder="e.g. Detective Sherlock")
        if st.button("🚀 Accept Investigation & Access Crime Scene", use_container_width=True, type="primary"):
            if d_name.strip():
                st.session_state.detective_name = d_name.strip()
                st.balloons()
                st.rerun()
            else:
                st.error("Please enter a Detective Name to proceed.")

# ==============================================================================
# SCREEN 2: MAIN INVESTIGATION DASHBOARD
# ==============================================================================
else:
    # Header Banner
    col_h1, col_h2 = st.columns([3.5, 1.5])
    with col_h1:
        st.markdown(f"### 🕵️ Lead Detective: **{st.session_state.detective_name}**")
    with col_h2:
        if st.button("🔄 Restart Investigation", use_container_width=True):
            st.session_state.evidence = []
            st.session_state.chat_history = []
            st.session_state.score = 100
            st.session_state.suspect_stress = {s: 15 for s in SUSPECTS.keys()}
            st.rerun()

    # --- SIDEBAR CASE BOARD ---
    st.sidebar.title("📋 Case Board")
    st.sidebar.metric("Detective Reputation Score", st.session_state.score)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎒 Evidence Log")
    for clue in st.session_state.evidence:
        st.sidebar.success(f"🔍 {clue}")

    total_clues = sum(len(clues) for clues in LOCATIONS.values())
    progress = min(len(st.session_state.evidence) / total_clues, 1.0)
    st.sidebar.progress(progress)
    st.sidebar.write(f"**{len(st.session_state.evidence)}/{total_clues}** clues collected")

    # --- MAIN TABS ---
    tab_search, tab_interrogate, tab_suspects, tab_evidence, tab_verdict = st.tabs([
        "🔍 Search Crime Scenes", 
        "💬 Interrogate Suspects", 
        "🧑 Suspect Profiles", 
        "📂 Evidence Board", 
        "⚖️ Final Verdict"
    ])

    LOCATION_IMAGES = {
        "Professor's Office": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=600",
        "Library": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=600",
        "Computer Lab": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600"
    }

    # --- TAB 1: SEARCH SCENES ---
    with tab_search:
        st.subheader("📍 Investigate Campus Locations")
        selected_location = st.selectbox("Select Area to Search:", list(LOCATIONS.keys()))
        
        col_img, col_clues = st.columns([1.2, 2])
        with col_img:
            st.image(LOCATION_IMAGES.get(selected_location), use_container_width=True, caption=selected_location)
            
        with col_clues:
            st.markdown(f"### Inspecting: {selected_location}")
            
            for clue in LOCATIONS[selected_location]:
                if clue in st.session_state.evidence:
                    st.success(f"✅ Collected: **{clue}**")
                else:
                    # SPECIAL PUZZLE FOR USB DRIVE
                    if clue == "USB Drive" and not st.session_state.usb_unlocked:
                        with st.expander("🧩 LOCKED TERMINAL CIPHER PUZZLE"):
                            st.write("To extract the encrypted USB Drive, crack the 4-digit security code.")
                            st.caption("Hint: The year Professor Sharma founded the lab (2024).")
                            code_in = st.text_input("Enter 4-Digit Passcode:", key="cipher_in")
                            if st.button("🔓 Decrypt Terminal"):
                                if code_in == "2024":
                                    st.session_state.usb_unlocked = True
                                    st.session_state.evidence.append(clue)
                                    st.session_state.score += 25
                                    st.success("🎉 Passcode Accepted! USB Drive Extracted!")
                                    st.rerun()
                                else:
                                    st.error("❌ Access Denied! Wrong Passcode.")
                    else:
                        if st.button(f"🔎 Inspect & Collect: {clue}", key=f"clue_{clue}"):
                            st.session_state.evidence.append(clue)
                            st.session_state.score += 15
                            st.success(f"Collected: **{clue}**")
                            st.info(EVIDENCE_INFO[clue])
                            st.rerun()

    # --- TAB 2: INTERROGATE SUSPECTS WITH STRESS & EVIDENCE CONFRONTATION ---
    with tab_interrogate:
        st.subheader("🗣️ AI Interrogation & Evidence Confrontation")
        
        selected_suspect = st.selectbox("Select Suspect to Question:", list(SUSPECTS.keys()))
        meta = SUSPECT_METADATA.get(selected_suspect, {"portrait": "", "weakness": "", "role": "Suspect"})
        
        col_s1, col_s2 = st.columns([1, 2.5])
        with col_s1:
            st.image(meta["portrait"], width=220)
            st.markdown(f"**{selected_suspect}** ({meta['role']})")
            
            # STRESS BAR
            stress_val = st.session_state.suspect_stress.get(selected_suspect, 15)
            st.markdown(f"**Stress / Panic Level:** {stress_val}%")
            st.progress(stress_val / 100.0)
            
        with col_s2:
            st.write(f"**Background:** {SUSPECTS[selected_suspect]}")
            st.divider()
            
            question = st.text_input(f"Ask {selected_suspect} a question:", key="interrogate_q")
            
            # CONFRONT WITH EVIDENCE DROPDOWN
            ev_options = ["None (Standard Question)"] + st.session_state.evidence
            confront_ev = st.selectbox("Confront Suspect with Evidence from Inventory:", ev_options)
            
            if st.button("🚨 Question / Confront Suspect", key="interrogate_btn", type="primary"):
                if question.strip() or confront_ev != "None (Standard Question)":
                    stress_boost = 0
                    confront_text = ""
                    
                    if confront_ev != "None (Standard Question)":
                        confront_text = f"*(Confronts with {confront_ev})* "
                        if confront_ev == meta["weakness"]:
                            stress_boost = 35
                            st.session_state.suspect_stress[selected_suspect] = min(100, stress_val + stress_boost)
                            st.warning(f"⚡ COUNTER-EVIDENCE MATCH! {selected_suspect}'s stress spiked by +35%!")
                        else:
                            stress_boost = 10
                            st.session_state.suspect_stress[selected_suspect] = min(100, stress_val + stress_boost)
                            
                    prompt = f"""
                    You are {selected_suspect} in a detective mystery game.
                    Character Background: {SUSPECTS[selected_suspect]}
                    Current Stress Level: {st.session_state.suspect_stress[selected_suspect]}% out of 100%.
                    Rules: Stay completely in character. If stress is high (>50%), sound nervous and defensive. If confronted with relevant evidence, react nervously. Never confess outright. Keep answers under 80 words.
                    Question: {confront_text} {question}
                    """
                    
                    try:
                        if model:
                            response = model.generate_content(prompt)
                            ans_text = response.text
                        else:
                            ans_text = "I have nothing to hide from you, Detective."
                    except Exception:
                        if confront_ev == meta["weakness"]:
                            ans_text = f"*(Sweats visibly)* Where did you get that {confront_ev}?! Look, Detective, I was there, but I didn't harm the Professor!"
                        else:
                            ans_text = "That item proves nothing regarding my whereabouts."
                            
                    st.session_state.chat_history.append((selected_suspect, question, ans_text))
                    st.rerun()

        st.markdown("---")
        st.markdown("### 📜 Interrogation Transcript")
        for s_name, q, a in reversed(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(f"**Q to {s_name}:** {q}")
            with st.chat_message("assistant"):
                st.write(f"**{s_name}:** {a}")

    # --- TAB 3: SUSPECT PROFILES ---
    with tab_suspects:
        st.subheader("🧑 Campus Suspect Dossiers")
        cols = st.columns(3)
        for idx, (s_name, s_desc) in enumerate(SUSPECTS.items()):
            s_meta = SUSPECT_METADATA.get(s_name, {"portrait": "", "role": "Suspect"})
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="suspect-profile-card">
                    <img src="{s_meta['portrait']}" style="width:100%; height:160px; object-fit:cover; border-radius:10px; margin-bottom:10px;">
                    <h4 style="margin:0;">{s_name}</h4>
                    <p style="color:#a1a1aa; font-size:12px; margin-bottom:8px;">Role: {s_meta['role']}</p>
                    <p style="font-size:13px;">{s_desc}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- TAB 4: EVIDENCE BOARD ---
    with tab_evidence:
        st.subheader("📂 Collected Evidence Pinboard")
        if not st.session_state.evidence:
            st.warning("No clues collected yet! Visit locations in the 'Search Crime Scenes' tab.")
        else:
            for item in st.session_state.evidence:
                st.markdown(f"""
                <div class="evidence-box">
                    <h4 style="margin:0;">🔍 {item}</h4>
                    <p style="margin-top:5px; color:#e2e8f0;">{EVIDENCE_INFO[item]}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- TAB 5: FINAL VERDICT ---
    with tab_verdict:
        st.subheader("⚖️ Issue Official Arrest Warrant")
        suspect_choice = st.selectbox("Who do you believe is the true culprit?", list(SUSPECTS.keys()), key="verdict_sel")
        
        if st.button("🔥 SUBMIT FINAL VERDICT", type="primary"):
            if suspect_choice == "Vikram Rao":
                st.balloons()
                st.success(f"🎉 **CASE SOLVED, DETECTIVE {st.session_state.detective_name.upper()}!** Vikram Rao used his lab access to enter Lab 3 at 8:57 PM and cover his tracks. Excellent deduction!")
            else:
                st.error(f"❌ **WRONG SUSPECT!** {suspect_choice} was innocent. The true culprit escaped! Review the evidence and interrogations again.")