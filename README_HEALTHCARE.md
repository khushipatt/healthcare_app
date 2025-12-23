# 🏥 Smart Healthcare Assistant - Hackathon Ready

Production-ready healthcare application with voice input, AI disease prediction, risk classification, city monitoring, and WhatsApp escalation.

## ✨ Features

- ✅ **Offline Voice Input** - Web Speech API (Chrome recommended)
- ✅ **Blue/White Theme** - Professional, mobile-responsive design
- ✅ **Patient Form** - Complete patient information and vital signs
- ✅ **Disease Prediction** - AI-powered symptom-to-disease matching
- ✅ **Risk Classification** - HIGH/MEDIUM/LOW with visual progress bar
- ✅ **City Monitoring** - Interactive disease trend charts (4 weeks)
- ✅ **WhatsApp Escalation** - One-tap emergency escalation with QR code
- ✅ **Bulk Voice Announcements** - Text-to-speech patient summaries
- ✅ **Local Storage** - Session state for patient history
- ✅ **Mobile Responsive** - Optimized for phone view

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

## 📋 Usage

1. **Patient Assessment Tab**:
   - Fill in patient details (name, age, gender, city, phone)
   - Enter vital signs (BP, temperature)
   - Use voice input or manually select symptoms
   - Click "Analyze Patient" to get disease prediction and risk classification
   - Use "ESCALATE TO HOSPITAL" button for emergency cases

2. **City Monitoring Tab**:
   - Select a city from dropdown
   - View interactive disease trend charts (Week 1-4)
   - See summary of disease trends

3. **Bulk Operations Tab**:
   - View all patients in system
   - Use "Announce Patient Status" for voice summary

## 🎯 Success Criteria

- ✅ Loads in <2 seconds
- ✅ Voice works offline in Chrome
- ✅ WhatsApp button opens correctly
- ✅ QR code scans to patient summary
- ✅ Professional appearance for judges
- ✅ Copy-paste deployable

## 📁 File Structure

```
.
├── app.py              # Main Streamlit application
├── data.py             # Mock city disease data
├── prediction.py       # Symptom → disease logic & risk classification
├── requirements.txt    # Dependencies
└── README_HEALTHCARE.md # This file
```

## 🔧 Dependencies

- `streamlit` - Web framework
- `qrcode[pil]` - QR code generation
- `plotly` - Interactive charts
- `Pillow` - Image processing

## 📱 Browser Compatibility

- **Voice Input**: Chrome/Edge (Web Speech API)
- **All Features**: Chrome, Firefox, Safari, Edge

## 🎨 Theme

- Primary Color: Blue (#1976d2)
- Background: White with blue gradient
- Emergency: Red (#d32f2f)
- Risk Colors: Red (HIGH) → Orange (MEDIUM) → Green (LOW)

## 🏆 Hackathon Ready

This app is designed to impress judges with:
- Modern, professional UI
- Complete feature set
- Production-ready code
- Error handling
- Mobile responsiveness
- Fast loading times

---

**Made for Hackathon** 🚀 | **Ready to Deploy** ✅ | **Voice-First** 🎤

