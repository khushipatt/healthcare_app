"""
Healthcare Hackathon App - Production Ready
Features: Voice input, Disease prediction, Risk classification, City monitoring, WhatsApp escalation
"""

import streamlit as st
import qrcode
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import json
import urllib.parse

from data import get_city_trends, get_all_cities, get_city_summary
from prediction import predict_disease, classify_risk

# Page Configuration
st.set_page_config(
    page_title="Smart Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "patients" not in st.session_state:
    st.session_state.patients = []
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = False


# ==================== STYLING ====================
def inject_custom_css():
    """Inject blue/white theme CSS"""
    st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 50%, #e8f5e9 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Headers */
    h1 {
        color: #1976d2 !important;
        font-weight: 700 !important;
    }
    
    h2, h3 {
        color: #1565c0 !important;
    }
    
    /* Buttons - Big and Blue */
    .stButton > button {
        background-color: #1976d2 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #1565c0 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(25, 118, 210, 0.3);
    }
    
    /* Emergency Button - Red */
    .emergency-btn {
        background-color: #d32f2f !important;
    }
    
    .emergency-btn:hover {
        background-color: #c62828 !important;
    }
    
    /* Cards */
    .card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 4px solid #1976d2;
    }
    
    /* Risk Progress Bar */
    .risk-high {
        background: linear-gradient(90deg, #d32f2f 0%, #f44336 100%);
    }
    
    .risk-medium {
        background: linear-gradient(90deg, #ff9800 0%, #ffb74d 100%);
    }
    
    .risk-low {
        background: linear-gradient(90deg, #4caf50 0%, #81c784 100%);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        border: 2px solid #1976d2;
        border-radius: 6px;
    }
    
    .stSelectbox > div > div > select {
        border: 2px solid #1976d2;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .stButton > button {
            font-size: 16px !important;
            padding: 10px 20px !important;
        }
    }
    
    /* Voice Input Section */
    .voice-section {
        background: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 2px dashed #1976d2;
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== VOICE INPUT (Web Speech API) ====================
def render_voice_input():
    """Render voice input interface using Web Speech API"""
    st.markdown("""
    <div class="voice-section">
        <h4>🎤 Voice Input (Offline - Chrome Recommended)</h4>
        <p>Click the button below and speak your symptoms. The recognized text will appear below.</p>
        <button id="startVoice" onclick="startVoiceRecognition()" style="background-color: #1976d2; color: white; padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px;">
            🎤 Start Voice Input
        </button>
        <button id="stopVoice" onclick="stopVoiceRecognition()" style="background-color: #d32f2f; color: white; padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; margin-left: 10px;">
            ⏹ Stop
        </button>
        <div id="voiceStatus" style="margin-top: 10px; font-weight: bold; color: #1976d2;"></div>
        <div id="voiceResult" style="margin-top: 10px; padding: 10px; background: white; border-radius: 4px; min-height: 40px; border: 1px solid #1976d2;"></div>
    </div>
    
    <script>
    let recognition = null;
    let isListening = false;
    let finalTranscript = '';
    
    function initVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            
            recognition.onstart = function() {
                isListening = true;
                document.getElementById('voiceStatus').textContent = '🎤 Listening... Speak now!';
                document.getElementById('startVoice').disabled = true;
                finalTranscript = '';
            };
            
            recognition.onresult = function(event) {
                let interimTranscript = '';
                finalTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript + ' ';
                    } else {
                        interimTranscript += transcript;
                    }
                }
                
                document.getElementById('voiceResult').innerHTML = 
                    '<strong>Final:</strong> ' + finalTranscript + '<br>' +
                    '<em>Interim:</em> ' + interimTranscript;
            };
            
            recognition.onerror = function(event) {
                document.getElementById('voiceStatus').textContent = '❌ Error: ' + event.error;
                isListening = false;
                document.getElementById('startVoice').disabled = false;
            };
            
            recognition.onend = function() {
                isListening = false;
                document.getElementById('voiceStatus').textContent = '⏹ Stopped. Click "Copy Text" to use.';
                document.getElementById('startVoice').disabled = false;
            };
        } else {
            document.getElementById('voiceStatus').textContent = '❌ Voice recognition not supported. Please use Chrome browser.';
            document.getElementById('startVoice').disabled = true;
        }
    }
    
    function startVoiceRecognition() {
        if (!recognition) {
            initVoiceRecognition();
        }
        if (recognition && !isListening) {
            recognition.start();
        }
    }
    
    function stopVoiceRecognition() {
        if (recognition && isListening) {
            recognition.stop();
        }
    }
    
    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initVoiceRecognition);
    } else {
        initVoiceRecognition();
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Display voice input result in Streamlit
    if "voice_text" not in st.session_state:
        st.session_state.voice_text = ""
    
    # Text area to show/manually edit voice input
    voice_input = st.text_area(
        "Voice Input Result (or type manually)",
        value=st.session_state.voice_text,
        key="voice_input_area",
        help="Use voice input above or type symptoms manually here (comma-separated)"
    )
    
    if voice_input:
        st.session_state.voice_text = voice_input


# ==================== PATIENT FORM ====================
def render_patient_form():
    """Render patient input form"""
    st.markdown("### 👤 Patient Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        patient_name = st.text_input("Patient Name", value="Ram", key="patient_name")
        age = st.number_input("Age", min_value=1, max_value=120, value=45, key="age")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
    
    with col2:
        city = st.selectbox("City", get_all_cities(), key="city")
        phone = st.text_input("Phone Number", value="917878000000", key="phone")
    
    st.markdown("---")
    st.markdown("### 🌡️ Vital Signs")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        bp_systolic = st.number_input("BP Systolic", min_value=60, max_value=200, value=90, key="bp_sys")
    with col2:
        bp_diastolic = st.number_input("BP Diastolic", min_value=40, max_value=150, value=60, key="bp_dia")
    with col3:
        temperature = st.number_input("Temperature (°F)", min_value=95.0, max_value=110.0, value=98.6, step=0.1, key="temp")
    
    st.markdown("---")
    st.markdown("### 🩺 Symptoms")
    
    # Voice input section
    render_voice_input()
    
    # Parse voice input if available
    voice_symptoms = []
    if st.session_state.get("voice_text"):
        voice_text = st.session_state.voice_text.lower()
        # Try to match voice input to symptom list
        common_symptoms_lower = [s.lower() for s in [
            "Fever", "Headache", "Cough", "Joint Pain", "Rash", "Bleeding",
            "Nausea", "Stomach Pain", "Diarrhea", "Weakness", "Loss of Appetite",
            "Sore Throat", "Body Ache", "Fatigue", "Runny Nose", "Weight Loss",
            "Night Sweats", "Chest Pain", "Chills", "Breathing Difficulty", "Loss of Taste"
        ]]
        for symptom in common_symptoms_lower:
            if symptom in voice_text:
                voice_symptoms.append(symptom.capitalize())
    
    # Manual symptom input
    common_symptoms = [
        "Fever", "Headache", "Cough", "Joint Pain", "Rash", "Bleeding",
        "Nausea", "Stomach Pain", "Diarrhea", "Weakness", "Loss of Appetite",
        "Sore Throat", "Body Ache", "Fatigue", "Runny Nose", "Weight Loss",
        "Night Sweats", "Chest Pain", "Chills", "Breathing Difficulty", "Loss of Taste"
    ]
    
    default_symptoms = voice_symptoms if voice_symptoms else []
    
    symptoms = st.multiselect(
        "Select Symptoms",
        options=common_symptoms,
        default=default_symptoms,
        key="symptoms"
    )
    
    return {
        "name": patient_name,
        "age": age,
        "gender": gender,
        "city": city,
        "phone": phone,
        "symptoms": [s.lower() for s in symptoms],
        "vitals": {
            "bp_systolic": bp_systolic,
            "bp_diastolic": bp_diastolic,
            "temperature": temperature
        }
    }


# ==================== RISK CLASSIFICATION ====================
def render_risk_classification(disease: str, confidence: float, risk_level: str, risk_score: int):
    """Render risk classification with progress bar"""
    st.markdown("### 📊 Risk Classification")
    
    # Determine color based on risk level
    if risk_level == "HIGH":
        color_class = "risk-high"
        emoji = "🔴"
    elif risk_level == "MEDIUM":
        color_class = "risk-medium"
        emoji = "🟡"
    else:
        color_class = "risk-low"
        emoji = "🟢"
    
    # Display risk level
    st.markdown(f"""
    <div class="card">
        <h3>{emoji} Risk Level: {risk_level}</h3>
        <p><strong>Disease:</strong> {disease}</p>
        <p><strong>Confidence:</strong> {confidence:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar (Red → Green)
    progress_color = "#d32f2f" if risk_score >= 70 else "#ff9800" if risk_score >= 40 else "#4caf50"
    
    st.markdown(f"""
    <div style="margin: 20px 0;">
        <p style="font-size: 18px; font-weight: bold; color: {progress_color};">
            Stroke Risk {risk_score}%
        </p>
        <div style="background: #e0e0e0; height: 30px; border-radius: 15px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, {progress_color} 0%, {progress_color} 100%); 
                        height: 100%; width: {risk_score}%; transition: width 0.5s ease;">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==================== CITY MONITORING ====================
def render_city_monitoring(city: str):
    """Render city-wise disease trends with interactive chart"""
    st.markdown("### 🌆 City-Wise Monitoring")
    
    trends = get_city_trends(city)
    summary = get_city_summary(city)
    
    st.info(f"**{city}:** {summary}")
    
    # Create interactive line chart
    fig = go.Figure()
    
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
    
    colors = px.colors.qualitative.Set3
    for idx, (disease, cases) in enumerate(trends.items()):
        fig.add_trace(go.Scatter(
            x=weeks,
            y=cases,
            mode='lines+markers',
            name=disease,
            line=dict(width=3, color=colors[idx % len(colors)]),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title=f"Disease Trends in {city} (4 Weeks)",
        xaxis_title="Week",
        yaxis_title="Number of Cases",
        hovermode='x unified',
        template="plotly_white",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ==================== WHATSAPP ESCALATION ====================
def generate_whatsapp_qr(patient_data: Dict, disease: str, confidence: float, risk_level: str):
    """Generate WhatsApp link and QR code"""
    try:
        # Create summary message
        summary = (
            f"Patient: {patient_data['name']}, {patient_data['age']}{patient_data['gender'][0]}, "
            f"{disease} {confidence:.0f}%, BP {patient_data['vitals']['bp_systolic']}/{patient_data['vitals']['bp_diastolic']}, "
            f"Risk: {risk_level}"
        )
        
        # WhatsApp URL with proper encoding
        phone = patient_data.get('phone', '917878000000').replace('+', '').replace('-', '').replace(' ', '')
        encoded_text = urllib.parse.quote(summary)
        whatsapp_url = f"https://wa.me/{phone}?text={encoded_text}"
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5, error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(whatsapp_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        
        return whatsapp_url, buf
    except Exception as e:
        st.error(f"Error generating QR code: {str(e)}")
        return "", None


def render_escalation(patient_data: Dict, disease: str, confidence: float, risk_level: str):
    """Render escalation button and QR code"""
    st.markdown("### 🚨 Emergency Escalation")
    
    whatsapp_url, qr_buffer = generate_whatsapp_qr(patient_data, disease, confidence, risk_level)
    
    if not whatsapp_url:
        st.error("Failed to generate escalation link. Please check patient data.")
        return
    
    # Emergency button
    st.markdown(f"""
    <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
        <button style="background-color: #d32f2f; color: white; padding: 20px; 
                      font-size: 24px; font-weight: bold; border: none; 
                      border-radius: 10px; width: 100%; cursor: pointer;
                      box-shadow: 0 4px 8px rgba(211, 47, 47, 0.3);">
            🚨 ESCALATE TO HOSPITAL
        </button>
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📱 WhatsApp Link")
        st.markdown(f"[Click to open WhatsApp]({whatsapp_url})")
        st.code(whatsapp_url, language=None)
    
    with col2:
        st.markdown("### 📷 QR Code")
        if qr_buffer:
            st.image(qr_buffer, caption="Scan to send WhatsApp message", use_container_width=True)
        else:
            st.warning("QR code not available")


# ==================== BULK VOICE ANNOUNCEMENT ====================
def render_bulk_voice():
    """Render bulk voice announcement feature"""
    st.markdown("### 💊 Bulk Voice Announcement")
    
    if st.session_state.patients:
        st.info(f"Total patients in system: {len(st.session_state.patients)}")
        
        # Group patients by status
        normal_patients = [p for p in st.session_state.patients if p.get('risk_level') == 'LOW']
        medium_patients = [p for p in st.session_state.patients if p.get('risk_level') == 'MEDIUM']
        high_patients = [p for p in st.session_state.patients if p.get('risk_level') == 'HIGH']
        
        if st.button("🔊 Announce Patient Status", use_container_width=True):
            announcement = f"Patients {len(normal_patients)} normal, {len(medium_patients)} medium risk, {len(high_patients)} high risk"
            
            st.markdown(f"""
            <div class="card">
                <p style="font-size: 18px;"><strong>Announcement:</strong></p>
                <p style="font-size: 16px;">{announcement}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Web Speech Synthesis
            st.markdown(f"""
            <script>
            if ('speechSynthesis' in window) {{
                const utterance = new SpeechSynthesisUtterance('{announcement}');
                utterance.lang = 'en-US';
                utterance.rate = 0.9;
                speechSynthesis.speak(utterance);
            }}
            </script>
            """, unsafe_allow_html=True)
    else:
        st.info("No patients recorded yet. Add a patient first.")


# ==================== MAIN APP ====================
def main():
    inject_custom_css()
    
    # Header
    st.title("🏥 Smart Healthcare Assistant")
    st.markdown("**Voice-First • AI-Powered • Production Ready**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Quick Actions")
        if st.button("🔄 Clear All Data", use_container_width=True):
            st.session_state.patients = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Patient History")
        if st.session_state.patients:
            for idx, patient in enumerate(st.session_state.patients[-5:]):  # Show last 5
                st.markdown(f"**{patient.get('name', 'Unknown')}** - {patient.get('disease', 'N/A')} ({patient.get('risk_level', 'N/A')})")
        else:
            st.info("No patients yet")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["👤 Patient Assessment", "🌆 City Monitoring", "💊 Bulk Operations"])
    
    with tab1:
        # Patient Form
        patient_data = render_patient_form()
        
        # Analyze button
        if st.button("🔍 Analyze Patient", type="primary", use_container_width=True):
            with st.spinner("Analyzing symptoms and calculating risk..."):
                # Predict disease
                disease, confidence = predict_disease(
                    patient_data['symptoms'],
                    patient_data['age'],
                    patient_data['city'],
                    patient_data['vitals']
                )
                
                # Classify risk
                risk_level, risk_score = classify_risk(
                    patient_data['age'],
                    patient_data['symptoms'],
                    patient_data['vitals'],
                    patient_data['city'],
                    disease,
                    confidence
                )
                
                # Store patient data
                patient_record = {
                    **patient_data,
                    "disease": disease,
                    "confidence": confidence,
                    "risk_level": risk_level,
                    "risk_score": risk_score
                }
                st.session_state.patients.append(patient_record)
                
                # Display results
                st.success("✅ Analysis Complete!")
                
                # Risk Classification
                render_risk_classification(disease, confidence, risk_level, risk_score)
                
                # Escalation
                render_escalation(patient_data, disease, confidence, risk_level)
    
    with tab2:
        # City selection
        selected_city = st.selectbox("Select City", get_all_cities(), key="monitor_city")
        render_city_monitoring(selected_city)
    
    with tab3:
        render_bulk_voice()
        
        # Patient list
        if st.session_state.patients:
            st.markdown("### 📋 All Patients")
            for idx, patient in enumerate(st.session_state.patients):
                with st.expander(f"Patient {idx+1}: {patient.get('name', 'Unknown')} - {patient.get('disease', 'N/A')}"):
                    st.json(patient)


if __name__ == "__main__":
    main()
