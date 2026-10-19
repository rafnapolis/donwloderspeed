import streamlit as st
import yt_dlp
import os
import tempfile
import subprocess
import sys

# ==========================================
# 🔄 ACTUALIZAR YT-DLP AUTOMÁTICAMENTE
# ==========================================
@st.cache_resource(show_spinner=False)
def update_yt_dlp():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp", "-q"])
        return True
    except Exception:
        return False

update_yt_dlp()

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
        "subtitle": "Descarga videos y audios a máxima velocidad. Sin frenos.",
        "lbl_url": "Pega el enlace del video aquí",
        "placeholder": "https://www.youtube.com/watch?v=...",
        "fmt_video": " Video (MP4)",
        "fmt_audio": "🎵 Audio (MP3)",
        "btn_process": "⬇️ INICIAR DESCARGA RÁPIDA",
        "processing": "Procesando en pista...",
        "fetching": "🔍 Obteniendo información del video...",
        "downloading": "️ Descargando archivo...",
        "success": "✅ ¡Archivo procesado con éxito!",
        "error_invalid": "⚠️ Por favor, ingresa un enlace URL válido.",
        "error_general": "❌ Ocurrió un error al procesar el video.",
        "error_no_format": "❌ No se encontró el formato solicitado. Intenta con otro video.",
        "step1_title": "✅ Archivo listo para descargar",
        "step1_desc": "Para mantener este servicio gratuito y rápido, completa un breve paso de verificación.",
        "btn_monetag": "🛡️ Paso 1: Verificar y Apoyar (Abrir en nueva pestaña)",
        "step2_desc": "¿Ya completaste el paso 1? Tu archivo está listo aquí 👇",
        "btn_download": "💾 Paso 2: Descargar Archivo",
        "footer": "DonwloaderspeedF1 • Potenciado por yt-dlp"
    },
    "en": {
        "title": "🏎️ DonwloaderspeedF1",
        "subtitle": "Download videos and audio at maximum speed. No brakes.",
        "lbl_url": "Paste video link here",
        "placeholder": "https://www.youtube.com/watch?v=...",
        "fmt_video": "🎬 Video (MP4)",
        "fmt_audio": "🎵 Audio (MP3)",
        "btn_process": "️ START FAST DOWNLOAD",
        "processing": "Processing on track...",
        "fetching": " Fetching video info...",
        "downloading": "⬇️ Downloading file...",
        "success": "✅ File processed successfully!",
        "error_invalid": "⚠️ Please enter a valid URL link.",
        "error_general": " An error occurred while processing the video.",
        "error_no_format": "❌ Requested format not found. Try another video.",
        "step1_title": "✅ File ready for download",
        "step1_desc": "To keep this service free and fast, please complete a brief verification step.",
        "btn_monetag": "🛡️ Step 1: Verify & Support (Open in new tab)",
        "step2_desc": "Already completed Step 1? Your file is ready here 👇",
        "btn_download": "💾 Step 2: Download File",
        "footer": "DonwloaderspeedF1 • Powered by yt-dlp"
    }
}

# ==========================================
# 🔄 GESTIÓN DE ESTADO E IDIOMA
# ==========================================
if 'lang' not in st.session_state:
    st.session_state.lang = 'es'
if 'file_ready' not in st.session_state:
    st.session_state.file_ready = False

t = TEXTS[st.session_state.lang]

def set_language(new_lang):
    st.session_state.lang = new_lang
    st.rerun()

# ==========================================
# 🎨 CSS PERSONALIZADO
# ==========================================
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .main { background-color: #0F172A; padding: 2rem 1rem; }
    .stApp { background-color: #0F172A; }
    
    .stTextInput > div > div > input {
        background-color: #1E293B; color: #F8FAFC;
        border: 1px solid #334155; border-radius: 0.75rem;
        padding: 0.85rem 1rem; font-size: 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #EF4444; box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #EF4444, #B91C1C);
        color: white !important; border-radius: 0.75rem;
        padding: 0.85rem; font-weight: 700; font-size: 1rem;
        border: none; width: 100%; transition: all 0.2s;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4); }
    .stButton > button:disabled { background: #475569; cursor: not-allowed; transform: none; }
    
    .stRadio > div {
        background-color: #1E293B; padding: 0.5rem;
        border-radius: 0.75rem; border: 1px solid #334155;
    }
    .stRadio label { color: #F8FAFC; font-weight: 500; }
    
    .monetag-btn {
        display: block; text-align: center;
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: white !important; text-decoration: none;
        padding: 1rem; border-radius: 0.75rem;
        font-weight: 700; font-size: 1.05rem;
        margin: 1rem 0; transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    .monetag-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(245, 158, 11, 0.4); }
    
    .info-box {
        background: #1E293B; border: 1px solid #334155;
        border-radius: 0.75rem; padding: 1.5rem; text-align: center;
    }
    .info-box h3 { color: #F8FAFC; margin: 0 0 0.5rem 0; }
    .info-box p { color: #94A3B8; font-size: 0.9rem; margin: 0; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🖥️ INTERFAZ DE USUARIO
# ==========================================
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f"<h1 style='text-align:center; color:#F8FAFC; margin-bottom:0.2rem; font-size:2rem; white-space:nowrap;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#94A3B8; margin-top:0;'>{t['subtitle']}</p>", unsafe_allow_html=True)
    
    # Switch de idioma compacto
    st.markdown("""
    <div style="display:flex; justify-content:center; gap:0.5rem; margin:1rem 0;">
    """, unsafe_allow_html=True)
    
    lang_col1, lang_col2 = st.columns(2)
    with lang_col1:
        if st.button("🇪🇸 ES", use_container_width=True, type="primary" if st.session_state.lang == "es" else "secondary"):
            set_language("es")
    with lang_col2:
        if st.button("🇺🇸 EN", use_container_width=True, type="primary" if st.session_state.lang == "en" else "secondary"):
            set_language("en")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

url = st.text_input(t["lbl_url"], placeholder=t["placeholder"])
format_choice = st.radio("", [t["fmt_video"], t["fmt_audio"]], horizontal=True, label_visibility="collapsed")

# ==========================================
# ⚙️ LÓGICA DE PROCESAMIENTO (SIN FFMPEG)
# ==========================================
if st.button(t["btn_process"], type="primary", use_container_width=True):
    if not url or not url.startswith("http"):
        st.error(t["error_invalid"])
    else:
        with st.status(t["processing"], expanded=True) as status:
            try:
                temp_dir = tempfile.mkdtemp()
                st.write(t["fetching"])
                
                ydl_opts = {
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                    'quiet': True, 
                    'no_warnings': True,
                    'ignoreerrors': False,
                }
                
                # SIN FFMPEG: Solo descarga formatos nativos
                if t["fmt_audio"] in format_choice:
                    st.write(t["downloading"])
                    # Busca MP3 nativo, si no, M4A (que es audio)
                    ydl_opts.update({
                        'format': 'bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio',
                    })
                    mime_type = "audio/mpeg"
                    ext = ".mp3"
                else:
                    st.write(t["downloading"])
                    # Busca MP4 nativo sin merging
                    ydl_opts.update({
                        'format': 'best[ext=mp4]/bestvideo[ext=mp4]/best',
                    })
                    mime_type = "video/mp4"
                    ext = ".mp4"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # Ajustar extensión si es necesario
                    if not filename.endswith(ext):
                        # Si descargó m4a pero queremos mp3, renombramos
                        if ext == ".mp3" and filename.endswith(".m4a"):
                            new_filename = filename[:-4] + ext
                            os.rename(filename, new_filename)
                            filename = new_filename
                        else:
                            filename = os.path.splitext(filename)[0] + ext

                status.update(label=t["success"], state="complete", expanded=False)
                
                if os.path.exists(filename):
                    with open(filename, "rb") as file:
                        file_bytes = file.read()
                    
                    st.session_state.file_ready = True
                    st.session_state.file_data = file_bytes
                    st.session_state.file_name = os.path.basename(filename)
                    st.session_state.file_mime = mime_type
                    
                    os.remove(filename)
                    os.rmdir(temp_dir)
                    
                    st.rerun()
                    
            except Exception as e:
                status.update(label="❌ Error", state="error")
                st.error(t["error_general"])
                with st.expander("🔍 Ver detalles del error"):
                    st.code(str(e))
                st.info("💡 *Consejo: Algunos videos pueden no tener el formato solicitado disponible.*")

# ==========================================
# 💰 ZONA DE DESCARGA Y MONETIZACIÓN
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
    <a href="{MONETAG_DIRECT_LINK}" 
       target="_blank" 
       rel="noopener noreferrer"
       class="monetag-btn">
        {t['btn_monetag']}
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<p style='text-align:center; color:#94A3B8; margin-top:1.5rem; font-size:0.95rem;'>{t['step2_desc']}</p>", unsafe_allow_html=True)
    
    st.download_button(
        label=t["btn_download"],
        data=st.session_state.file_data,
        file_name=st.session_state.file_name,
        mime=st.session_state.file_mime,
        type="primary",
        use_container_width=True
    )

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#475569; font-size:0.8rem;'>{t['footer']}</p>", unsafe_allow_html=True)
