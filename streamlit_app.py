import streamlit as st
import streamlit.components.v1 as components

# Configure full-width viewport and browser title
st.set_page_config(
    page_title="Nari 2.0 - Aapki AI Saathi",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit UI chrome to keep full focus on the application
st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      header {visibility: hidden;}
      footer {visibility: hidden;}
      .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
      }
      iframe {
        border: none !important;
        width: 100% !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Raw HTML/JS App
HTML_APP = r"""<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Nari 2.0 - Aapki AI Saathi</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <style>
    @keyframes pulse-ring {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.7); }
      70% { transform: scale(1.1); box-shadow: 0 0 0 25px rgba(225, 29, 72, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(225, 29, 72, 0); }
    }
    .mic-active {
      animation: pulse-ring 1.8s infinite cubic-bezier(0.4, 0, 0.6, 1);
    }
    body {
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }
  </style>
</head>
<body class="bg-rose-50/50 text-slate-800 font-sans min-h-screen flex flex-col items-center justify-between p-4 selection:bg-rose-200">

  <!-- HTTPS Security Warning for Remote Clients -->
  <div id="https-alert" class="hidden w-full max-w-md bg-amber-100 border border-amber-300 text-amber-900 px-4 py-2 rounded-xl text-xs font-semibold mb-3">
    ⚠️ माइक का उपयोग करने के लिए वेबसाइट का HTTPS (सुरक्षित लिंक) पर होना अनिवार्य है।
  </div>

  <!-- Top Navigation & Indian Languages Dropdown -->
  <header class="w-full max-w-md flex justify-between items-center bg-white/90 backdrop-blur-md p-3 rounded-2xl shadow-sm border border-rose-100">
    <div class="flex items-center gap-2.5">
      <div class="w-10 h-10 rounded-full bg-rose-600 text-white flex items-center justify-center font-bold text-lg shadow-inner">
        🌸
      </div>
      <div>
        <h1 class="font-extrabold text-rose-900 text-lg leading-tight tracking-tight">नारी 2.0 (Nari 2.0)</h1>
        <p class="text-xs text-rose-600 font-medium" id="sub-title">आपकी डिजिटल साथी</p>
      </div>
    </div>

    <!-- Multi-Language Dropdown -->
    <div class="relative">
      <select id="lang-select" onchange="setLanguage(this.value)" class="bg-rose-100/70 border border-rose-300 text-rose-950 text-xs font-bold rounded-xl px-2.5 py-1.5 focus:outline-none focus:ring-2 focus:ring-rose-500 cursor-pointer">
        <option value="hi" selected>🇮🇳 हिन्दी (Hindi)</option>
        <option value="ta">🇮🇳 தமிழ் (Tamil)</option>
        <option value="te">🇮🇳 తెలుగు (Telugu)</option>
        <option value="kn">🇮🇳 ಕನ್ನಡ (Kannada)</option>
        <option value="bn">🇮🇳 বাংলা (Bengali)</option>
        <option value="mr">🇮🇳 मराठी (Marathi)</option>
        <option value="gu">🇮🇳 ગુજરાતી (Gujarati)</option>
        <option value="ml">🇮🇳 മലയാളം (Malayalam)</option>
        <option value="en">🌐 English</option>
      </select>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="w-full max-w-md flex-1 flex flex-col justify-center my-4 space-y-4">

    <!-- Interactive Card -->
    <div class="bg-white rounded-3xl p-6 shadow-md border border-rose-100 flex flex-col items-center text-center relative overflow-hidden">
      <!-- Speaker button to re-read current prompt -->
      <button onclick="speakCurrentPrompt()" class="absolute top-4 right-4 p-2 bg-rose-100 text-rose-700 rounded-full hover:bg-rose-200 transition" title="Listen again">
        <i data-lucide="volume-2" class="w-5 h-5"></i>
      </button>

      <!-- Visual Avatar -->
      <div class="w-20 h-20 rounded-full bg-rose-100 flex items-center justify-center mb-3 shadow-inner">
        <span class="text-4xl">🧕</span>
      </div>

      <!-- Spoken Text Response Area -->
      <h2 id="ai-speech-text" class="text-xl font-bold text-slate-800 leading-snug">
        नमस्ते मैडम! आपकी आवश्यकताओं के लिए आपातकालीन मदद या हेल्पलाइन चुनें अथवा बोलकर बताएं।
      </h2>
      <p id="ai-sub-helper" class="text-sm text-slate-500 mt-2">
        नीचे लाल बटन दबाकर बोलें या सीधे हेल्पलाइन नंबर पर टैप करें।
      </p>

      <!-- Action Card -->
      <div id="visual-steps" class="w-full mt-4 text-left hidden">
        <div class="p-3 bg-red-50 rounded-xl border border-red-200 mb-3 flex items-start justify-between gap-3">
          <div class="flex items-start gap-3">
            <span class="text-2xl" id="helpline-icon">🚨</span>
            <div>
              <h4 class="font-bold text-red-900 text-sm" id="helpline-name">आपातकालीन सहायता (112)</h4>
              <p class="text-xs text-red-800" id="helpline-desc">तत्काल पुलिस और आपातकालीन सेवा।</p>
            </div>
          </div>
          <a id="call-direct-btn" href="tel:112" class="bg-red-600 hover:bg-red-700 text-white font-bold text-xs px-3 py-2 rounded-xl flex items-center gap-1 shadow-sm whitespace-nowrap active:scale-95 transition">
            <i data-lucide="phone-call" class="w-3.5 h-3.5"></i>
            <span id="call-now-text">कॉल करें</span>
          </a>
        </div>

        <p class="text-xs font-bold text-slate-600 mb-2 uppercase tracking-wider" id="doc-req-title">मदद के लिए क्या बताएं:</p>
        <div class="grid grid-cols-3 gap-2 text-center text-xs">
          <div class="p-2 bg-slate-50 border border-slate-200 rounded-xl flex flex-col items-center">
            <span class="text-2xl mb-1">📍</span>
            <span class="font-semibold text-slate-700" id="doc-id">सटीक स्थान</span>
          </div>
          <div class="p-2 bg-slate-50 border border-slate-200 rounded-xl flex flex-col items-center">
            <span class="text-2xl mb-1">⚠️</span>
            <span class="font-semibold text-slate-700" id="doc-bank">समस्या बताएं</span>
          </div>
          <div class="p-2 bg-slate-50 border border-slate-200 rounded-xl flex flex-col items-center">
            <span class="text-2xl mb-1">📱</span>
            <span class="font-semibold text-slate-700" id="doc-phone">फोन चालू रखें</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Buttons -->
    <div class="w-full">
      <p class="text-xs text-center text-slate-500 font-semibold mb-2" id="quick-prompt-title">या नीचे सीधा आपातकालीन नंबर चुनें:</p>
      <div class="grid grid-cols-2 gap-2.5">
        <button onclick="handleQuickSelect('POLICE')" class="p-3 bg-white hover:bg-rose-50 border border-rose-100 rounded-2xl flex items-center gap-3 shadow-sm transition active:scale-95 text-left">
          <span class="text-2xl">🚨</span>
          <div>
            <p class="font-bold text-slate-800 text-sm leading-tight" id="btn-police-title">पुलिस / आपातकाल</p>
            <p class="text-[11px] font-bold text-red-600" id="btn-police-sub">डायल 112</p>
          </div>
        </button>

        <button onclick="handleQuickSelect('AMBULANCE')" class="p-3 bg-white hover:bg-rose-50 border border-rose-100 rounded-2xl flex items-center gap-3 shadow-sm transition active:scale-95 text-left">
          <span class="text-2xl">🚑</span>
          <div>
            <p class="font-bold text-slate-800 text-sm leading-tight" id="btn-amb-title">एंबुलेंस / अस्पताल</p>
            <p class="text-[11px] font-bold text-red-600" id="btn-amb-sub">डायल 108 / 102</p>
          </div>
        </button>

        <button onclick="handleQuickSelect('WOMEN_HELPLINE')" class="p-3 bg-white hover:bg-rose-50 border border-rose-100 rounded-2xl flex items-center gap-3 shadow-sm transition active:scale-95 text-left">
          <span class="text-2xl">👩‍🦰</span>
          <div>
            <p class="font-bold text-slate-800 text-sm leading-tight" id="btn-women-title">महिला हेल्पलाइन</p>
            <p class="text-[11px] font-bold text-rose-600" id="btn-women-sub">डायल 181</p>
          </div>
        </button>

        <button onclick="handleQuickSelect('SCHEME_SUPPORT')" class="p-3 bg-white hover:bg-rose-50 border border-rose-100 rounded-2xl flex items-center gap-3 shadow-sm transition active:scale-95 text-left">
          <span class="text-2xl">📞</span>
          <div>
            <p class="font-bold text-slate-800 text-sm leading-tight" id="btn-scheme-title">योजना सहायता</p>
            <p class="text-[11px] font-bold text-amber-700" id="btn-scheme-sub">डायल 14445</p>
          </div>
        </button>
      </div>
    </div>
  </main>

  <!-- Voice Input Action -->
  <footer class="w-full max-w-md flex flex-col items-center gap-3 mb-2">
    <div id="transcript-box" class="h-6 text-xs text-rose-600 font-semibold italic text-center px-2"></div>

    <div class="flex items-center justify-center gap-4 w-full">
      <button id="mic-btn" onclick="toggleVoiceInput()" class="w-20 h-20 rounded-full bg-rose-600 hover:bg-rose-700 text-white flex flex-col items-center justify-center shadow-lg transition active:scale-95 focus:outline-none ring-4 ring-rose-200">
        <i data-lucide="mic" class="w-8 h-8"></i>
        <span class="text-[10px] font-bold mt-0.5" id="mic-text">बोलें</span>
      </button>
    </div>

    <details class="text-[11px] text-slate-400 mt-2 cursor-pointer w-full text-center">
      <summary class="hover:text-slate-600">⚙️ Gemini API सेटिंग्स (वैकल्पिक)</summary>
      <div class="mt-2 p-2 bg-white rounded-lg border border-slate-200 flex gap-2">
        <input type="password" id="gemini-key" placeholder="Paste Gemini API Key" class="flex-1 text-xs border rounded p-1" />
        <button onclick="saveApiKey()" class="bg-rose-600 text-white px-2 rounded text-xs">Save</button>
      </div>
    </details>
  </footer>

  <script>
    lucide.createIcons();

    if (window.location.protocol !== 'https:' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
      document.getElementById('https-alert').classList.remove('hidden');
    }

    const TRANSLATIONS = {
      hi: {
        bcp47: "hi-IN",
        subtitle: "आपकी डिजिटल साथी",
        greeting: "नमस्ते मैडम! आपकी आवश्यकताओं के लिए आपातकालीन मदद या हेल्पलाइन चुनें अथवा बोलकर बताएं।",
        subHelper: "नीचे लाल बटन दबाकर बोलें या सीधे हेल्पलाइन नंबर पर टैप करें।",
        quickTitle: "या नीचे सीधा आपातकालीन नंबर चुनें:",
        micText: "बोलें",
        listening: "हम सुन रहे हैं, बोलिए...",
        docTitle: "कॉल करते समय ध्यान रखें:",
        docs: ["सटीक स्थान", "समस्या बताएं", "फोन चालू रखें"],
        callNow: "कॉल करें",
        buttons: {
          police: ["पुलिस / आपातकाल", "डायल 112"],
          ambulance: ["एंबुलेंस / अस्पताल", "डायल 108 / 102"],
          women: ["महिला हेल्पलाइन", "डायल 181"],
          scheme: ["योजना सहायता", "डायल 14445"]
        },
        services: {
          POLICE: {
            title: "आपातकालीन प्रतिक्रिया सेवा (112)",
            desc: "24x7 तत्काल पुलिस, अग्निशमन और आपातकालीन सुरक्षा।",
            tel: "112",
            icon: "🚨",
            spoken: "मैडम, किसी भी खतरे या आपात स्थिति के लिए तुरंत 112 पर कॉल करें।"
          },
          AMBULANCE: {
            title: "एंबुलेंस व अस्पताल आपातकाल (108 / 102)",
            desc: "तत्काल आपातकालीन चिकित्सा और प्रसव सहायता सेवा।",
            tel: "108",
            icon: "🚑",
            spoken: "मैडम, अस्पताल और एंबुलेंस के लिए 108 या प्रसव सहायता के लिए 102 पर संपर्क करें।"
          },
          WOMEN_HELPLINE: {
            title: "महिला हेल्पलाइन (181)",
            desc: "घरेलू हिंसा, संकट और महिला सुरक्षा के लिए 24 घंटे मुफ्त परामर्श।",
            tel: "181",
            icon: "👩‍🦰",
            spoken: "मैडम, किसी भी परेशानी या सुरक्षा के लिए 181 महिला हेल्पलाइन पर निःशुल्क बात करें।"
          },
          SCHEME_SUPPORT: {
            title: "सरकारी योजना सहायता (14445)",
            desc: "सरकारी योजनाओं की जानकारी और शिकायत निवारण हेल्पलाइन।",
            tel: "14445",
            icon: "📞",
            spoken: "मैडम, सरकारी योजनाओं की जानकारी के लिए 14445 हेल्पलाइन पर कॉल करें।"
          }
        }
      },
      ta: {
        bcp47: "ta-IN",
        subtitle: "உங்கள் டிஜிட்டல் தோழி",
        greeting: "வணக்கம் மேடம்! உங்கள் தேவைகளுக்கான அவசர உதவி அல்லது உதவி எண்களுக்கு கீழே தொடுங்கள் அல்லது பேசுங்கள்.",
        subHelper: "சிவப்பு பொத்தானை அழுத்திப் பேசுங்கள் அல்லது நேரடியாக எண்ணைத் தொடவும்.",
        quickTitle: "அல்லது நேரடியாக அவசர எண்ணைத் தொடவும்:",
        micText: "பேசவும்",
        listening: "கேட்கிறது, சொல்லுங்கள்...",
        docTitle: "அழைக்கும் போது கூற வேண்டியவை:",
        docs: ["சரியான இடம்", "சிக்கலைக் கூறவும்", "தொலைபேசி இயக்கத்தில்"],
        callNow: "அழைக்க",
        buttons: {
          police: ["காவல்துறை உதவி", "டயல் 112"],
          ambulance: ["ஆம்புலன்ஸ் அவசரம்", "டயல் 108 / 102"],
          women: ["பெண்கள் உதவி எண்", "டயல் 181"],
          scheme: ["திட்டங்கள் உதவி", "டயல் 14445"]
        },
        services: {
          POLICE: {
            title: "காவல்துறை அவசர உதவி (112)",
            desc: "24 மணி நேர காவல்துறை மற்றும் அவசர பாதுகாப்பு உதவி.",
            tel: "112",
            icon: "🚨",
            spoken: "மேடம், எந்தவொரு அவசர நேரத்திலும் உடனடியாக 112 என்ற எண்ணை அழைக்கவும்."
          },
          AMBULANCE: {
            title: "ஆம்புலன்ஸ் மருத்துவ உதவி (108 / 102)",
            desc: "உடனடி மருத்துவமனை மற்றும் பிரசவ கால ஆம்புலன்ஸ் சேவை.",
            tel: "108",
            icon: "🚑",
            spoken: "மேடம், அவசர மருத்துவ உதவிக்கு 108 எண்ணை உடனடியாக அழைக்கவும்."
          },
          WOMEN_HELPLINE: {
            title: "பெண்கள் உதவி மையம் (181)",
            desc: "பெண்களுக்கான பாதுகாப்பு மற்றும் சட்ட உதவி மையம்.",
            tel: "181",
            icon: "👩‍🦰",
            spoken: "மேடம், பெண்களுக்கு எதிரான வன்முறை அல்லது உதவிக்கு 181 என்ற எண்ணை அழைக்கவும்."
          },
          SCHEME_SUPPORT: {
            title: "அரசு திட்டங்கள் உதவி மையம் (14445)",
            desc: "அனைத்து அரசு நலத்திட்டங்கள் பற்றிய விவரங்கள் மற்றும் உதவி.",
            tel: "14445",
            icon: "📞",
            spoken: "மேடம், அரசு திட்டங்களின் தகவல்களைப் பெற 14445 என்ற எண்ணை அழைக்கலாம்."
          }
        }
      },
      te: {
        bcp47: "te-IN",
        subtitle: "మీ డిజిటల్ స్నేహితురాలు",
        greeting: "నమస్కారం మేడమ్! మీ అవసరాలకు అత్యవసర సహాయం లేదా హెల్ప్‌లైన్ నంబర్ల కోసం మాట్లాడండి లేదా ఎంచుకోండి.",
        subHelper: "క్రింది ఎరుపు బటన్ నొక్కి మాట్లాడండి లేదా నేరుగా నంబర్‌‌పై నొక్కండి.",
        quickTitle: "లేదా నేరుగా అత్యవసర నంబర్‌ను ఎంచుకోండి:",
        micText: "మాట్లాడండి",
        listening: "వింటున్నాను, మాట్లాడండి...",
        docTitle: "కాల్ చేసినప్పుడు చెప్పవలసినవి:",
        docs: ["ఖచ్చితమైన చిరునామా", "సమస్య వివరాలు", "ఫోన్ అందుబాటులో ఉంచండి"],
        callNow: "కాల్ చేయండి",
        buttons: {
          police: ["పోలీస్ / అత్యవసరం", "డయల్ 112"],
          ambulance: ["అంబులెన్స్ / ఆసుపత్రి", "డయల్ 108 / 102"],
          women: ["మహిళా హెల్ప్‌లైన్", "డయల్ 181"],
          scheme: ["పథకాల సహాయం", "డయల్ 14445"]
        },
        services: {
          POLICE: {
            title: "పోలీస్ ఎమర్జెన్సీ రెస్పాన్స్ (112)",
            desc: "24 గంటల తక్షణ పోలీసు మరియు భద్రతా సహాయం.",
            tel: "112",
            icon: "🚨",
            spoken: "మేడమ్, అత్యవసర పరిస్థితి ఉంటే వెంటనే 112 కి కాల్ చేయండి."
          },
          AMBULANCE: {
            title: "అంబులెన్స్ / వైద్య అత్యవసరం (108 / 102)",
            desc: "తక్షణ వైద్య చికిత్స మరియు ప్రసవ సహాయక అంబులెన్స్.",
            tel: "108",
            icon: "🚑",
            spoken: "మేడమ్, అత్యవసర వైద్యం కోసం 108 నంబర్‌కు కాల్ చేయవచ్చు."
          },
          WOMEN_HELPLINE: {
            title: "మహిళా హెల్ప్‌‌లైన్ (181)",
            desc: "మహిళా భద్రత, గృహహింస నుండి రక్షణ మరియు ఉచిత కౌన్సెలింగ్.",
            tel: "181",
            icon: "👩‍🦰",
            spoken: "మేడమ్, రక్షణ లేదా సహాయం కోసం 181 మహిళా హెల్ప్‌లైన్‌కు కాల్ చేయండి."
          },
          SCHEME_SUPPORT: {
            title: "ప్రభుత్వ పథకాల హెల్ప్‌లైన్ (14445)",
            desc: "ప్రభుత్వ సంక్షేమ పథకాల సమాచారం మరియు సహాయం.",
            tel: "14445",
            icon: "📞",
            spoken: "మేడమ్, ప్రభుత్వ పథకాల వివరాల కోసం 14445 కు కాల్ చేయండి."
          }
        }
      },
      kn: {
        bcp47: "kn-IN",
        subtitle: "ನಿಮ್ಮ ಡಿಜಿಟಲ್ ಒಡನಾಡಿ",
        greeting: "ನಮಸ್ಕಾರ ಮೇಡಂ! ನಿಮ್ಮ ಅಗತ್ಯಗಳಿಗೆ ತುರ್ತು ಸಹಾಯ ಅಥವಾ ಸಹಾಯವಾಣಿಗಾಗಿ ಮಾತನಾಡಿ ಅಥವಾ ಕೆಳಗೆ ಆಯ್ಕೆಮಾಡಿ.",
        subHelper: "ಕೆಳಗಿನ ಕೆಂಪು ಗುಂಡಿಯನ್ನು ಒತ್ತಿ ಅಥವಾ ನೇರವಾಗಿ ಸಂಖ್ಯೆಯ ಮೇಲೆ ಟ್ಯಾಪ್ ಮಾಡಿ.",
        quickTitle: "ಅಥವಾ ನೇರವಾಗಿ ತುರ್ತು ಸಂಖ್ಯೆ ಆಯ್ಕೆಮಾಡಿ:",
        micText: "ಮಾತನಾಡಿ",
        listening: "ಕೇಳಿಸಿಕೊಳ್ಳುತ್ತಿದ್ದೇನೆ, ಮಾತನಾಡಿ...",
        docTitle: "ಕರೆ ಮಾಡುವಾಗ ತಿಳಿಸಬೇಕಾದ ವಿವರಗಳು:",
        docs: ["ನಿಖರ ಸ್ಥಳ", "ಸಮಸ್ಯೆ ತಿಳಿಸಿ", "ಫೋನ್ ಆನ್ ಇರಲಿ"],
        callNow: "ಕರೆ ಮಾಡಿ",
        buttons: {
          police: ["ಪೊಲೀಸ್ ತುರ್ತು ಸೇವೆ", "ಡಯಲ್ 112"],
          ambulance: ["ಆಂಬ್ಯುಲೆನ್ಸ್ / ಆಸ್ಪತ್ರೆ", "ಡಯಲ್ 108 / 102"],
          women: ["ಮಹಿಳಾ ಸಹಾಯವಾಣಿ", "ಡಯಲ್ 181"],
          scheme: ["ಯೋಜನೆಗಳ ನೆರವು", "ಡಯಲ್ 14445"]
        },
        services: {
          POLICE: {
            title: "ತುರ್ತು ಪ್ರತಿಕ್ರಿಯೆ ಸೇವೆ (112)",
            desc: "ಯಾವುದೇ ತುರ್ತು ಪರಿಸ್ಥಿತಿಗೆ 24 ಗಂಟೆ ಪೊಲೀಸ್ ರಕ್ಷಣೆ.",
            tel: "112",
            icon: "🚨",
            spoken: "ಮೇಡಂ, ಯಾವುದೇ ತುರ್ತು ಸಂದರ್ಭದಲ್ಲಿ ತಕ್ಷಣ 112 ಗೆ ಕರೆ ಮಾಡಿ."
          },
          AMBULANCE: {
            title: "ಆಂಬ್ಯುಲೆನ್ಸ್ ಸೇವೆ (108 / 102)",
            desc: "ತುರ್ತು ಚಿಕಿತ್ಸೆ ಮತ್ತು ಆಸ್ಪತ್ರೆ ವಾಹನ ಸೇವೆ.",
            tel: "108",
            icon: "🚑",
            spoken: "ಮೇಡಂ, ಆಂಬ್ಯುಲೆನ್ಸ್‌ಗಾಗಿ ತಕ್ಷಣ 108 ಅಥವಾ 102 ಗೆ ಕರೆ ಮಾಡಿ."
          },
          WOMEN_HELPLINE: {
            title: "ಮಹಿಳಾ ಸಹಾಯವಾಣಿ (181)",
            desc: "ಮಹಿಳೆಯರ ರಕ್ಷಣೆ ಮತ್ತು ಕಾನೂನು ಸಲಹಾ ಸೇವೆ.",
            tel: "181",
            icon: "👩‍🦰",
            spoken: "ಮೇಡಂ, ಮಹಿಳೆಯರ ಸುರಕ್ಷತೆಗಾಗಿ 181 ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ."
          },
          SCHEME_SUPPORT: {
            title: "ಯೋಜನೆ ಸಹಾಯವಾಣಿ (14445)",
            desc: "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಮಾಹಿತಿ ಮತ್ತು ನೆರವು.",
            tel: "14445",
            icon: "📞",
            spoken: "ಮೇಡಂ, ಸರ್ಕಾರದ ಯೋಜನೆಗಳ ಮಾಹಿತಿಗಾಗಿ 14445 ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ."
          }
        }
      },
      bn: {
        bcp47: "bn-IN",
        subtitle: "আপনার ডিজিটাল সাথী",
        greeting: "নমস্কার ম্যাডাম! আপনার প্রয়োজনের জন্য জরুরি সাহায্য বা হেল্পলাইনের তথ্য জানতে কথা বলুন বা নিচে স্পর্শ করুন।",
        subHelper: "লাল বোতাম টিপে কথা বলুন অথবা হেল্পলাইন নম্বরে সরাসরি ট্যাপ করুন।",
        quickTitle: "বা সরাসরি জরুরি নম্বর বেছে নিন:",
        micText: "বলুন",
        listening: "শুনছি, বলুন...",
        docTitle: "ফোন করার সময় মনে রাখবেন:",
        docs: ["সঠিক ঠিকানা", "সমস্যা বলুন", "ফোন चालू রাখুন"],
        callNow: "কল করুন",
        buttons: {
          police: ["পুলিশ / জরুরি সেবা", "ডায়াল 112"],
          ambulance: ["অ্যাম্বুলেন্স / হাসপাতাল", "ডায়াল 108 / 102"],
          women: ["নারী হেল্পলাইন", "ডায়াল 181"],
          scheme: ["সরকারি প্রকল্প সহায়তা", "ডায়াল 14445"]
        },
        services: {
          POLICE: {
            title: "জরুরি প্রতিক্রিয়া সেবা (112)",
            desc: "২৪ ঘণ্টা পুলিশ ও জরুরি সুরক্ষা পরিষেবা।",
            tel: "112",
            icon: "🚨",
            spoken: "ম্যাডাম, বিপদে পড়লে অবিলম্বে ১১২ নম্বরে ফোন করুন।"
          },
          AMBULANCE: {
            title: "অ্যাম্বুলেন্স সেবা (108 / 102)",
            desc: "জরুরি চিকিৎসা এবং প্রসূতি সহায়তা পরিষেবা।",
            tel: "108",
            icon: "🚑",
            spoken: "ম্যাডাম, চিকিৎসার জন্য অবিলম্বে ১০৮ নম্বরে কল করুন।"
          },
          WOMEN_HELPLINE: {
            title: "নারী হেল্পলাইন (181)",
            desc: "নারীদের সুরক্ষা ও সংকটে বিনামূল্যে সহায়তা।",
            tel: "181",
            icon: "👩‍🦰",
            spoken: "ম্যাডাম, নারী সুরক্ষার প্রয়োজনে বিনামূল্যে ১৮১ নম্বরে ফোন করুন।"
          },
          SCHEME_SUPPORT: {
            title: "সরকারি প্রকল্প সহায়তা (14445)",
            desc: "সরকারি সুযোগ-সুবিধার তথ্য কেন্দ্র।",
            tel: "14445",
            icon: "📞",
            spoken: "ম্যাডাম, প্রকল্পের তথ্য জানতে ১৪৪৪৫ নম্বরে কল করুন।"
          }
        }
      },
      mr: {
        bcp47: "mr-IN",
        subtitle: "तुमची डिजिटल मैत्रीण",
        greeting: "नमस्कार मॅडम! आपल्या गरजांसाठी आपत्कालीन मदत किंवा हेल्पलाइनसाठी बोला किंवा खाली निवडा.",
        subHelper: "लाल बटण दाबून बोला किंवा थेट हेल्पलाइन नंबरवर टॅप करा.",
        quickTitle: "किंवा थेट खालील आपत्कालीन नंबर निवडा:",
        micText: "बोला",
        listening: "ऐकत आहे, बोला...",
        docTitle: "कॉल करताना सांगायचे तपशील:",
        docs: ["अचूक पत्ता", "समस्या सांगा", "फोन चालू ठेवा"],
        callNow: "कॉल करा",
        buttons: {
          police: ["पोलीस / आपत्कालीन", "डायल 112"],
          ambulance: ["रुग्णवाहिका / रुग्णालय", "डायल 108 / 102"],
          women: ["महिला हेल्पलाइन", "डायल 181"],
          scheme: ["योजना मदत केंद्र", "डायल 14445"]
        },
        services: {
          POLICE: {
            title: "आपत्कालीन प्रतिसाद सेवा (112)",
            desc: "२४ तास पोलीस आणि आपत्कालीन मदत.",
            tel: "112",
            icon: "🚨",
            spoken: "मॅडम, संकटाच्या वेळी लगेच 112 नंबरवर कॉल करा."
          },
          AMBULANCE: {
            title: "रुग्णवाहिका सेवा (108 / 102)",
            desc: "तातडीने वैद्यकीय मदत व रुग्णवाहिका सेवा.",
            tel: "108",
            icon: "🚑",
            spoken: "मॅडम, वैद्यकीय मदतीसाठी 108 डायल करा."
          },
          WOMEN_HELPLINE: {
            title: "महिला हेल्पलाइन (181)",
            desc: "महिला सुरक्षा व मोफत मदत केंद्र.",
            tel: "181",
            icon: "👩‍🦰",
            spoken: "मॅडम, महिला सुरक्षेसाठी 181 महिला हेल्पलाइनवर संपर्क करा."
          },
          SCHEME_SUPPORT: {
            title: "योजना सहाय्यता केंद्र (14445)",
            desc: "शासकीय योजनांची माहिती आणि मदत.",
            tel: "14445",
            icon: "📞",
            spoken: "मॅडम, शासकीय योजनांच्या माहितीसाठी 14445 क्रमांकावर संपर्क करा."
          }
        }
      },
      gu: {
        bcp47: "gu-IN",
        subtitle: "તમારી ડિજિટલ સાથી",
        greeting: "નમસ્તે મેડમ! તમારી જરૂરિયાતો માટે ઇમરજન્સી મદદ અથવા હેલ્પલાઇન માટે બોલો અથવા નીચે પસંદ કરો.",
        subHelper: "લાલ બટન દબાવીને બોલો અથવા સીધા હેલ્પલાઇન નંબર પર ટેપ કરો.",
        quickTitle: "અથવા સીધો ઇમરજન્સી નંબર પસંદ કરો:",
        micText: "બોલો",
        listening: "સાંભળી રહ્યા છીએ, બોલો...",
        docTitle: "કૉલ કરતી વખતે જણાવો:",
        docs: ["ચોક્કસ સ્થળ", "સમસ્યા જણાવો", "ફોન ચાલુ રાખો"],
        callNow: "કૉલ કરો",
        buttons: {
          police: ["પોલીસ / ઇમરજન્સી", "ડાયલ 112"],
          ambulance: ["એમ્બ્યુલન્સ / હોસ્પિટલ", "ડાયલ 108 / 102"],
          women: ["મહિલા હેલ્પલાઇન", "ડાયલ 181"],
          scheme: ["યોજના સહાય", "ડાયલ 14445"]
        },
        services: {
          POLICE: {
            title: "પોલીસ ઇમરજન્સી રિસ્પોન્સ (112)",
            desc: "24 કલાક પોલીસ અને સુરક્ષા સહાય.",
            tel: "112",
            icon: "🚨",
            spoken: "મેડમ, કોઈપણ મુશ્કેલીમાં તરત જ 112 પર કૉલ કરો."
          },
          AMBULANCE: {
            title: "એમ્બ્યુલન્સ સેવા (108 / 102)",
            desc: "તાત્કાલિક હોસ્પિટલ અને પ્રસુતિ સહાય.",
            tel: "108",
            icon: "🚑",
            spoken: "મેડમ, ઇમરજન્સી સારવાર માટે 108 પર સંપર્ક કરો."
          },
          WOMEN_HELPLINE: {
            title: "મહિલા હેલ્પલાઇન અભયમ (181)",
            desc: "મહિલાઓની સુરક્ષા માટે 24 કલાક મફત સહાય.",
            tel: "181",
            icon: "👩‍🦰",
            spoken: "મેડમ, સુરક્ષા માટે 181 મહિલા હેલ્પલાઇન પર કૉલ કરો."
          },
          SCHEME_SUPPORT: {
            title: "યોજના સહાય હેલ્પલાઇન (14445)",
            desc: "સરકારી યોજનાઓની વિગતો અને સહાય.",
            tel: "14445",
            icon: "📞",
            spoken: "મેડમ, સરકારી યોજનાઓની માહિતી માટે 14445 પર સંપર્ક કરો."
          }
        }
      },
      ml: {
        bcp47: "ml-IN",
        subtitle: "നിങ്ങളുടെ ഡിജിറ്റൽ സുഹൃത്ത്",
        greeting: "നമസ്കാരം മാഡം! നിങ്ങളുടെ ആവശ്യങ്ങൾക്കുള്ള അടിയന്തര സഹായത്തിനോ ഹെൽപ്പ്‌ലൈനുകൾക്കോ സംസാരിക്കൂ അല്ലെങ്കിൽ തിരഞ്ഞെടുക്കൂ.",
        subHelper: "ചുവന്ന ബട്ടൺ അമർത്തി സംസാരിക്കൂ അല്ലെങ്കിൽ നമ്പറിൽ തൊടൂ.",
        quickTitle: "അല്ലെങ്കിൽ എമർജൻസി നമ്പർ തിരഞ്ഞെടുക്കൂ:",
        micText: "സംസാരിക്കൂ",
        listening: "കേൾക്കുന്നു, പറയൂ...",
        docTitle: "വിളിക്കുമ്പോൾ ശ്രദ്ധിക്കേണ്ടവ:",
        docs: ["കൃത്യമായ സ്ഥലം", "കാര്യം പറയുക", "ഫോൺ കയ്യിൽ കരുതുക"],
        callNow: "വിളിക്കൂ",
        buttons: {
          police: ["പോലീസ് / എമർജൻസി", "ഡയൽ 112"],
          ambulance: ["ആംബുലൻസ് / ആശുപത്രി", "ഡയൽ 108 / 102"],
          women: ["വനിതാ ഹെൽപ്പ്‌ലൈൻ", "ഡയൽ 181"],
          scheme: ["പദ്ധതി സഹായം", "ഡയൽ 14445"]
        },
        services: {
          POLICE: {
            title: "എമർജൻസി റെസ്‌പോൺസ് സപ്പോർട്ട് (112)",
            desc: "24 മണിക്കൂറും പോലീസ്, സുരക്ഷാ സഹായം.",
            tel: "112",
            icon: "🚨",
            spoken: "മാഡം, അടിയന്തര ഘട്ടങ്ങളിൽ ഉടനടി 112 എന്ന നമ്പറിലേക്ക് വിളിക്കൂ."
          },
          AMBULANCE: {
            title: "ആംബുലൻസ് സേവനം (108 / 102)",
            desc: "അടിയന്തര ചികിത്സയ്ക്കും ആശുപത്രി യാത്രയ്ക്കും.",
            tel: "108",
            icon: "🚑",
            spoken: "മാഡം, ചികിത്സാ സഹായത്തിന് 108 വിളിക്കുക."
          },
          WOMEN_HELPLINE: {
            title: "വനിതാ ഹെൽപ്പ്‌ലൈൻ (181)",
            desc: "സ്ത്രീ സുരക്ഷയ്ക്കും അടിയന്തര സഹായത്തിനും.",
            tel: "181",
            icon: "👩‍🦰",
            spoken: "മാഡം, സ്ത്രീകൾക്ക് സഹായത്തിനായി 181 എന്ന നമ്പറിൽ ബന്ധപ്പെടാം."
          },
          SCHEME_SUPPORT: {
            title: "പദ്ധതി ഹെൽപ്പ്‌ലൈൻ (14445)",
            desc: "സർക്കാർ പദ്ധതി വിവരങ്ങളും സഹായവും.",
            tel: "14445",
            icon: "📞",
            spoken: "മാഡം, സർക്കാർ പദ്ധതികളുടെ സഹായത്തിന് 14445 എന്ന നമ്പറിൽ വിളിക്കുക."
          }
        }
      },
      en: {
        bcp47: "en-IN",
        subtitle: "Your Emergency & Support Guide",
        greeting: "Hello Madam! Speak or tap below for emergency and helpline numbers for your needs.",
        subHelper: "Tap the red microphone button or select an emergency helpline directly.",
        quickTitle: "Or select a direct helpline number:",
        micText: "Speak",
        listening: "Listening now, please speak...",
        docTitle: "Key details to share during call:",
        docs: ["Exact Location", "State Emergency", "Keep Phone Active"],
        callNow: "Call Now",
        buttons: {
          police: ["Police / Emergency", "Dial 112"],
          ambulance: ["Ambulance / Hospital", "Dial 108 / 102"],
          women: ["Women Helpline", "Dial 181"],
          scheme: ["Scheme Support", "Dial 14445"]
        },
        services: {
          POLICE: {
            title: "Emergency Response Support System (112)",
            desc: "24x7 all-in-one emergency service for Police, Fire, and Rescue.",
            tel: "112",
            icon: "🚨",
            spoken: "Madam, in any danger or crisis, dial 112 immediately."
          },
          AMBULANCE: {
            title: "Ambulance & Hospital Emergency (108 / 102)",
            desc: "Urgent medical transport and free maternity ambulance services.",
            tel: "108",
            icon: "🚑",
            spoken: "Madam, call 108 for emergency medical transport or 102 for maternity assistance."
          },
          WOMEN_HELPLINE: {
            title: "Women Helpline (181)",
            desc: "24x7 toll-free emergency response and rescue for women in distress.",
            tel: "181",
            icon: "👩‍🦰",
            spoken: "Madam, call 181 for 24-hour confidential support and protection for women."
          },
          SCHEME_SUPPORT: {
            title: "Scheme Support & Grievance (14445)",
            desc: "Dedicated helpline for government scheme queries and status help.",
            tel: "14445",
            icon: "📞",
            spoken: "Madam, for government scheme queries, contact the helpline at 14445."
          }
        }
      }
    };

    let currentLang = 'hi';
    let isListening = false;
    let recognition = null;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;

      recognition.onstart = () => {
        isListening = true;
        document.getElementById('mic-btn').classList.add('mic-active');
        document.getElementById('transcript-box').innerText = TRANSLATIONS[currentLang].listening;
      };

      recognition.onresult = (event) => {
        const transcript = Array.from(event.results).map(r => r[0].transcript).join('');
        document.getElementById('transcript-box').innerText = `"${transcript}"`;

        if (event.results[0].isFinal) {
          processVoiceQuery(transcript);
        }
      };

      recognition.onerror = (e) => {
        stopVoiceInput();
        if (e.error === 'not-allowed') {
          document.getElementById('transcript-box').innerText = "कृपया ब्राउज़र सेटिंग में माइक्रोफ़ोन की अनुमति दें (Permission denied).";
        } else {
          document.getElementById('transcript-box').innerText = "आवाज नहीं सुनाई दी, दोबारा बोलें (Please try again)";
        }
      };

      recognition.onend = () => {
        stopVoiceInput();
      };
    }

    function toggleVoiceInput() {
      if (!recognition) {
        alert("Your browser does not support Speech Recognition. Please open this link in Google Chrome, Edge, or Safari on iOS.");
        return;
      }
      if (isListening) {
        recognition.stop();
        stopVoiceInput();
      } else {
        try {
          recognition.lang = TRANSLATIONS[currentLang].bcp47;
          recognition.start();
        } catch (err) {
          console.warn("Recognition start issue:", err);
        }
      }
    }

    function stopVoiceInput() {
      isListening = false;
      document.getElementById('mic-btn').classList.remove('mic-active');
    }

    function setLanguage(lang) {
      currentLang = lang;
      const t = TRANSLATIONS[lang];

      document.getElementById('sub-title').innerText = t.subtitle;
      document.getElementById('ai-speech-text').innerText = t.greeting;
      document.getElementById('ai-sub-helper').innerText = t.subHelper;
      document.getElementById('quick-prompt-title').innerText = t.quickTitle;
      document.getElementById('mic-text').innerText = t.micText;
      document.getElementById('doc-req-title').innerText = t.docTitle;
      document.getElementById('doc-id').innerText = t.docs[0];
      document.getElementById('doc-bank').innerText = t.docs[1];
      document.getElementById('doc-phone').innerText = t.docs[2];
      document.getElementById('call-now-text').innerText = t.callNow;

      document.getElementById('btn-police-title').innerText = t.buttons.police[0];
      document.getElementById('btn-police-sub').innerText = t.buttons.police[1];
      document.getElementById('btn-amb-title').innerText = t.buttons.ambulance[0];
      document.getElementById('btn-amb-sub').innerText = t.buttons.ambulance[1];
      document.getElementById('btn-women-title').innerText = t.buttons.women[0];
      document.getElementById('btn-women-sub').innerText = t.buttons.women[1];
      document.getElementById('btn-scheme-title').innerText = t.buttons.scheme[0];
      document.getElementById('btn-scheme-sub').innerText = t.buttons.scheme[1];

      document.getElementById('visual-steps').classList.add('hidden');
      speak(t.greeting);
    }

    function handleQuickSelect(serviceKey) {
      const item = TRANSLATIONS[currentLang].services[serviceKey];
      if (!item) return;

      document.getElementById('ai-speech-text').innerText = item.title;
      document.getElementById('ai-sub-helper').innerText = item.desc;
      document.getElementById('helpline-name').innerText = item.title;
      document.getElementById('helpline-desc').innerText = item.desc;
      document.getElementById('helpline-icon').innerText = item.icon;
      
      const callBtn = document.getElementById('call-direct-btn');
      callBtn.href = `tel:${item.tel}`;
      
      document.getElementById('visual-steps').classList.remove('hidden');

      speak(item.spoken);
    }

    async function processVoiceQuery(query) {
      const lower = query.toLowerCase();
      const apiKey = localStorage.getItem('gemini_api_key');

      if (apiKey) {
        document.getElementById('ai-speech-text').innerText = "नारी 2.0 सोच रही है...";
        try {
          const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{
                parts: [{
                  text: `You are Nari 2.0, a courteous emergency helpline assistant addressing the user as Madam. The user spoke in ${TRANSLATIONS[currentLang].bcp47}: "${query}". Address them respectfully as Madam and guide them on helplines for their needs (112 for Police, 108 for Ambulance, 181 for Women Helpline, or 14445 for Scheme support). Reply in 2 short sentences in that language.`
                }]
              }]
            })
          });
          const data = await res.json();
          const reply = data.candidates?.[0]?.content?.parts?.[0]?.text || "सहायता नंबर उपलब्ध है।";
          document.getElementById('ai-speech-text').innerText = reply;
          document.getElementById('visual-steps').classList.remove('hidden');
          speak(reply);
          return;
        } catch (err) {
          console.warn("API fallback to local heuristic", err);
        }
      }

      if (lower.includes('police') || lower.includes('पुलिस') || lower.includes('कावल') || lower.includes('పోలీస్') || lower.includes('112') || lower.includes('danger') || lower.includes('खतरा')) {
        handleQuickSelect('POLICE');
      } else if (lower.includes('hospital') || lower.includes('doctor') || lower.includes('अस्पताल') || lower.includes('एम्बुलेंस') || lower.includes('ambulance') || lower.includes('மருத்துவமனை') || lower.includes('108') || lower.includes('102')) {
        handleQuickSelect('AMBULANCE');
      } else if (lower.includes('woman') || lower.includes('महिला') || lower.includes('हिंसा') || lower.includes('பெண்') || lower.includes('మహిళ') || lower.includes('181')) {
        handleQuickSelect('WOMEN_HELPLINE');
      } else {
        handleQuickSelect('SCHEME_SUPPORT');
      }
    }

    function speak(text) {
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = TRANSLATIONS[currentLang].bcp47;
      utterance.rate = 0.95;
      window.speechSynthesis.speak(utterance);
    }

    function speakCurrentPrompt() {
      const text = document.getElementById('ai-speech-text').innerText;
      speak(text);
    }

    function saveApiKey() {
      const key = document.getElementById('gemini-key').value.trim();
      if (key) {
        localStorage.setItem('gemini_api_key', key);
        alert('Gemini Key Saved for Nari 2.0!');
      }
    }
  </script>
</body>
</html>
"""

# Render full screen app inside Streamlit iframe
components.html(HTML_APP, height=960, scrolling=True)