# nari-ai
# 🌸 Nari 2.0 (नारी 2.0) - Aapki AI Saathi

A voice-first, multilingual emergency and public assistance web app built for women across India. Nari 2.0 allows users to quickly trigger emergency services or inquire about essential government helplines via real-time speech recognition, text-to-speech feedback, or one-tap emergency calling.

---

## ✨ Features

- 🎙️ **Voice-First Navigation:** Integrated Web Speech API for real-time speech recognition in multiple Indic languages.
- 🗣️ **Text-to-Speech (TTS):** Speaks back instructions and confirmations clearly in the user's selected language.
- 🚨 **One-Tap Emergency Dialing:** Instant click-to-call direct links for:
  - **112** — Police & Universal Emergency Response Support System (ERSS)
  - **108 / 102** — Ambulance & Maternal Healthcare
  - **181** — Women Helpline (Domestic Abuse, Safety & Legal Counseling)
  - **14445** — Government Scheme Assistance & Grievance
- 🌐 **9 Indian Languages Supported:** Hindi (`hi-IN`), Tamil (`ta-IN`), Telugu (`te-IN`), Kannada (`kn-IN`), Bengali (`bn-IN`), Marathi (`mr-IN`), Gujarati (`gu-IN`), Malayalam (`ml-IN`), and English (`en-IN`).
- 🤖 **Gemini AI Integration (Optional):** Supports direct Gemini API keys for dynamic contextual emergency triage and conversational guidance.
- 📱 **Mobile-First & Accessible:** Designed with Tailwind CSS and Lucide icons for high contrast, touch targets, and offline fallback heuristics.

---

## 🚀 Live Demo & Deployment

> **Important:** Web Speech API (Microphone) requires a secure **HTTPS** connection or `localhost`. Plain `http://` on remote devices will automatically block microphone access.

### Deploying Free in Seconds (HTTPS)

1. **Netlify Drop:**
   - Go to [app.netlify.com/drop](https://app.netlify.com/drop).
   - Drag and drop your project folder containing `index.html`.
   - Your site will instantly go live with an `https://*.netlify.app` URL.

2. **GitHub Pages:**
   - Push this repository to GitHub.
   - Go to **Settings** > **Pages**.
   - Under **Build and deployment**, select **Source** as `Deploy from a branch` and set branch to `main` / `root`.
   - Click **Save**.

---

## 💻 Running Locally

### Option 1: VS Code Live Server
1. Open this folder in VS Code.
2. Install the **Live Server** extension (`ms-vscode.live-server` or Ritwick Dey).
3. Right-click `index.html` and select **Open with Live Server**.

### Option 2: PowerShell (Built-in HTTP Server)
Run the following native one-liner in PowerShell (no Python/Node.js required):

```powershell
$l = [System.Net.HttpListener]::new(); $l.Prefixes.Add("http://localhost:8080/"); $l.Start(); Write-Host "Server running at http://localhost:8080/"; while($l.IsListening){ $c = $l.GetContext(); $b = [IO.File]::ReadAllBytes("$PWD/index.html"); $c.Response.ContentType='text/html'; $c.Response.OutputStream.Write($b,0,$b.Length); $c.Response.Close() }
