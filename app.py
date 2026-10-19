import streamlit as st
import streamlit.components.v1 as components
import yt_dlp
import os

# Configuración de la página
st.set_page_config(
    page_title="Python Media Downloader | MP4 & MP3",
    page_icon="📥",
    layout="centered"
)

# Enlace de monetización de Monetag
MONETAG_SMARTLINK = "https://uplcm.com/4/9616671"

# Estilos CSS personalizados
st.markdown(
    """
    <style>
    .main {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .stTextInput input {
        background-color: #1E293B;
        color: white;
        border-radius: 8px;
    }
    .ad-banner {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .monetag-btn {
        background-color: #22C55E;
        color: white !important;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        margin-top: 8px;
    }
    .monetag-btn:hover {
        background-color: #16A34A;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Panel Lateral / Sidebar (Publicidad Monetag)
with st.sidebar:
    st.header("⚡ Patrocinado")
    st.markdown(
        f"""
        <div class="ad-banner">
            <p style="font-size: 13px; color: #94A3B8; margin-bottom: 8px;">🔥 Descubre las mejores ofertas y contenido recomendado</p>
            <a href="{MONETAG_SMARTLINK}" target="_blank" class="monetag-btn">
                👉 Ver Oferta Especial
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("📥 Descargador de Videos y Audios")
st.write("Herramienta desarrollada con Python para descargar contenido en MP4 y MP3.")

# Banner superior publicitario
st.markdown(
    f"""
    <div style="background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%); padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 20px;">
        <span style="color: white; font-size: 14px; font-weight: 500;">✨ ¡Servicio gratuito! Apoya la plataforma visitando a nuestros patrocinadores:</span>
        <a href="{MONETAG_SMARTLINK}" target="_blank" style="color: #FACC15; font-weight: bold; margin-left: 10px; text-decoration: underline;">
            Haz Clic Aquí 🚀
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Entrada de la URL
url = st.text_input("🔗 Enlace del video (YouTube, etc.):", placeholder="https://www.youtube.com/watch?v=...")

# Formato
format_choice = st.radio(
    "📂 Selecciona el formato de salida:",
    ("Video (MP4)", "Audio (MP3)"),
    horizontal=True
)

# Botón principal
if st.button("🚀 Iniciar Conversión y Descarga", type="primary", use_container_width=True):
    if not url.strip():
        st.warning("⚠️ Por favor, ingresa un enlace válido antes de continuar.")
    else:
        with st.spinner("⏳ Procesando archivo con Python... Esto puede tomar unos segundos."):
            try:
                output_dir = "downloads"
                os.makedirs(output_dir, exist_ok=True)

                # Opciones robustas de yt-dlp para evitar errores de formato y restricciones de YouTube
                if "MP3" in format_choice:
                    ydl_opts = {
                        'format': 'ba[ext=m4a]/bestaudio/best',
                        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'noplaylist': True,
                    }
                else:
                    ydl_opts = {
                        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best',
                        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                        'noplaylist': True,
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    if "MP3" in format_choice:
                        filename = os.path.splitext(filename)[0] + ".mp3"
                    
                    file_name_only = os.path.basename(filename)

                st.success("✅ ¡Archivo procesado con éxito!")

                # Banner publicitario antes de guardar el archivo (Monetag)
                st.markdown(
                    f"""
                    <div class="ad-banner">
                        <p style="color: #E2E8F0; font-weight: bold; margin-bottom: 5px;">🎉 Tu archivo está listo</p>
                        <p style="font-size: 12px; color: #94A3B8;">Antes de descargar, apóyanos echando un vistazo a este enlace de nuestros anunciantes:</p>
                        <a href="{MONETAG_SMARTLINK}" target="_blank" class="monetag-btn">
                            🎁 Abrir Enlace del Patrocinador
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Botón de descarga local
                with open(filename, "rb") as file:
                    st.download_button(
                        label=f"💾 Guardar {file_name_only} en tu dispositivo",
                        data=file,
                        file_name=file_name_only,
                        mime="audio/mpeg" if "MP3" in format_choice else "video/mp4",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"❌ Ocurrió un error durante el proceso: {str(e)}")

# Pie de página
st.markdown("---")
st.markdown(
    f"""
    <p style='text-align: center; color: #64748B; font-size: 12px;'>
        Desarrollado con Python & Streamlit • <a href="{MONETAG_SMARTLINK}" target="_blank" style="color: #64748B;">Publicidad / Monetag</a>
    </p>
    """,
    unsafe_allow_html=True
)
