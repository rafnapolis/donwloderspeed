import streamlit as st
import yt_dlp
import os
import tempfile
import requests
import re

# ==========================================
# 🚨 CONFIGURACIÓN DE MONETAG
# ==========================================
MONETAG_DIRECT_LINK = "https://uplcm.com/4/9616671"

st.set_page_config(
    page_title="DonwloaderspeedF1 | MP4 & MP3",
    page_icon="🏎️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 🌍 DICCIONARIO DE IDIOMAS
# ==========================================
TEXTS = {
    "es": {
        "title": "🏎️ DonwloaderspeedF1",
        "subtitle": "Descarga videos y audios a máxima velocidad.",
        "lbl_url": "Pega el enlace del video aquí",
        "placeholder": "https://www.youtube.com/watch?v=...",
        "fmt_video": "🎬 Video (MP4)",
        "fmt_audio": "🎵 Audio (MP3)",
        "btn_process": "️ INICIAR DESCARGA RÁPIDA",
        "processing": "Procesando...",
        "fetching": "🔍 Obteniendo info...",
        "downloading": "⬇️ Descargando...",
        "trying_cobalt": "🔄 Usando servidor alternativo...",
        "success": "✅ ¡Listo!",
        "error_invalid": "⚠️ Enlace inválido.",
        "error_general": "❌ Error al procesar.",
        "step1_title": "✅ Archivo listo",
        "step1_desc": "Completa un paso de verificación para descargar.",
        "btn_monetag": "🛡️ Paso 1: Verificar (Nueva pestaña)",
        "step2_desc": "¿Ya verificaste? Descarga aquí 👇",
        "btn_download": "💾 Paso 2: Descargar",
        "footer": "DonwloaderspeedF1"
    },
    "en": {
        "title": "🏎️ DonwloaderspeedF1",
        "subtitle": "Download videos and audio at max speed.",
        "lbl_url": "Paste video link here",
        "placeholder": "https://www.youtube.com/watch?v=...",
        "fmt_video": "🎬 Video (MP4)",
        "fmt_audio": "🎵 Audio (MP3)",
        "btn_process": "️ START FAST DOWNLOAD",
        "processing": "Processing...",
        "fetching": "🔍 Fetching info...",
        "downloading": "⬇️ Downloading...",
        "trying_cobalt": "🔄 Using alternative server...",
        "success": "✅ Done!",
        "error_invalid": "⚠️ Invalid link.",
        "error_general": "❌ Processing error.",
        "step1_title": "✅ File ready",
        "step1_desc": "Complete verification to download.",
        "btn_monetag": "🛡️ Step 1: Verify (New tab)",
        "step2_desc": "Already verified? Download here 👇",
        "btn_download": "💾 Step 2: Download",
        "footer": "DonwloaderspeedF1"
    }
}

if 'lang' not in st.session_state:
    st.session_state.lang = 'es'
if 'file_ready' not in st.session_state:
    st.session_state.file_ready = False

t = TEXTS[st.session_state.lang]

def set_language(new_lang):
    st.session_state.lang = new_lang
    st.rerun()

# ==========================================
# 🎨 CSS
# ==========================================
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .main { background-color: #0F172A; padding: 2rem 1rem; }
    .stApp { background-color: #0F172A; }
    .stTextInput > div > div > input {
        background-color: #1E293B; color: #F8FAFC;
        border: 1px solid #334155; border-radius: 0.75rem;
        padding: 0.85rem 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #EF4444; box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2);
    }
    .stButton > button {
        background: linear-gradient(135deg, #EF4444, #B91C1C);
        color: white !important; border-radius: 0.75rem;
        padding: 0.85rem; font-weight: 700; font-size: 1rem;
        border: none; width: 100%;
    }
    .stRadio > div {
        background-color: #1E293B; padding: 0.5rem;
        border-radius: 0.75rem; border: 1px solid #334155;
    }
    .stRadio label { color: #F8FAFC; }
    .monetag-btn {
        display: block; text-align: center;
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: white !important; text-decoration: none;
        padding: 1rem; border-radius: 0.75rem;
        font-weight: 700; margin: 1rem 0;
    }
    .info-box {
        background: #1E293B; border: 1px solid #334155;
        border-radius: 0.75rem; padding: 1.5rem; text-align: center;
    }
    .info-box h3 { color: #F8FAFC; margin: 0 0 0.5rem 0; }
    .info-box p { color: #94A3B8; margin: 0; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🖥️ UI
# ==========================================
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f"<h1 style='text-align:center; color:#F8FAFC; font-size:2rem;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#94A3B8;'>{t['subtitle']}</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🇪🇸 ES", use_container_width=True, type="primary" if st.session_state.lang == "es" else "secondary"):
            set_language("es")
    with c2:
        if st.button("🇺🇸 EN", use_container_width=True, type="primary" if st.session_state.lang == "en" else "secondary"):
            set_language("en")

url = st.text_input(t["lbl_url"], placeholder=t["placeholder"])
format_choice = st.radio("", [t["fmt_video"], t["fmt_audio"]], horizontal=True, label_visibility="collapsed")

# ==========================================
#  FUNCIÓN COBALT API MEJORADA
# ==========================================
def download_with_cobalt(video_url, is_audio):
    try:
        # Usamos la API pública de Cobalt
        api_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        data = {
            "url": video_url,
            "vQuality": "720",
            "aFormat": "mp3" if is_audio else "best",
            "filenamePattern": "basic"
        }
        
        if is_audio:
            data["isAudioOnly"] = True
        
        response = requests.post(api_url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "stream" and result.get("url"):
                # Descargar el archivo
                file_resp = requests.get(result["url"], timeout=60, stream=True)
                if file_resp.status_code == 200:
                    temp_dir = tempfile.mkdtemp()
                    ext = ".mp3" if is_audio else ".mp4"
                    filename = os.path.join(temp_dir, f"file{ext}")
                    
                    with open(filename, 'wb') as f:
                        for chunk in file_resp.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    return filename, "audio/mpeg" if is_audio else "video/mp4"
        
        return None, None
    except Exception as e:
        st.warning(f"Cobalt error: {str(e)[:100]}")
        return None, None

# ==========================================
# ⚙️ PROCESAMIENTO
# ==========================================
if st.button(t["btn_process"], type="primary", use_container_width=True):
    if not url or not url.startswith("http"):
        st.error(t["error_invalid"])
    else:
        with st.status(t["processing"], expanded=True) as status:
            try:
                temp_dir = tempfile.mkdtemp()
                st.write(t["fetching"])
                
                is_audio = t["fmt_audio"] in format_choice
                
                # Configuración ultra-simple para yt-dlp
                ydl_opts = {
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'no_warnings': True,
                    'ignoreerrors': False,
                    'extract_flat': False,
                }
                
                if is_audio:
                    st.write(t["downloading"])
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '128',
                    }]
                    mime_type, ext = "audio/mpeg", ".mp3"
                else:
                    st.write(t["downloading"])
                    ydl_opts['format'] = 'best[ext=mp4]/best'
                    mime_type, ext = "video/mp4", ".mp4"

                filename = None
                error_occurred = False
                
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        
                        # Ajustar extensión
                        if not os.path.exists(filename):
                            # Buscar el archivo real
                            for f in os.listdir(temp_dir):
                                if f.endswith(ext) or (is_audio and f.endswith(('.mp3', '.m4a'))):
                                    filename = os.path.join(temp_dir, f)
                                    if is_audio and not f.endswith('.mp3'):
                                        new_name = os.path.join(temp_dir, f.replace(os.path.splitext(f)[1], '.mp3'))
                                        os.rename(filename, new_name)
                                        filename = new_name
                                    break
                except Exception as e:
                    error_occurred = True
                    st.warning(t["trying_cobalt"])
                    filename, mime_type = download_with_cobalt(url, is_audio)
                    if filename:
                        ext = ".mp3" if is_audio else ".mp4"

                if filename and os.path.exists(filename):
                    status.update(label=t["success"], state="complete", expanded=False)
                    
                    with open(filename, "rb") as file:
                        file_bytes = file.read()
                    
                    st.session_state.file_ready = True
                    st.session_state.file_data = file_bytes
                    st.session_state.file_name = os.path.basename(filename)
                    st.session_state.file_mime = mime_type
                    
                    # Limpieza
                    try:
                        os.remove(filename)
                        os.rmdir(temp_dir)
                    except:
                        pass
                    
                    st.rerun()
                else:
                    raise Exception("No file found after download")
                    
            except Exception as e:
                status.update(label="❌ Error", state="error")
                st.error(t["error_general"])
                with st.expander("🔍 Ver detalles"):
                    st.code(str(e))
                st.info("💡 Prueba con otro video. Algunos videos están protegidos.")

# ==========================================
# 💰 DESCARGA
# ==========================================
if st.session_state.file_ready:
    st.markdown("---")
    st.markdown(f"""
    <div class="info-box">
        <h3>{t['step1_title']}</h3>
        <p>{t['step1_desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <a href="{MONETAG_DIRECT_LINK}" target="_blank" class="monetag-btn">
        {t['btn_monetag']}
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<p style='text-align:center; color:#94A3B8;'>{t['step2_desc']}</p>", unsafe_allow_html=True)
    
    st.download_button(
        label=t["btn_download"],
        data=st.session_state.file_data,
        file_name=st.session_state.file_name,
        mime=st.session_state.file_mime,
        type="primary",
        use_container_width=True
    )

st.markdown(f"<p style='text-align:center; color:#475569; margin-top:2rem;'>{t['footer']}</p>", unsafe_allow_html=True)
