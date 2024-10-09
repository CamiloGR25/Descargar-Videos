from pytubefix import YouTube
from pytubefix.cli import on_progress
import streamlit as st #para mostrar GUI en la weeb
import os 

class YouTubeDownload:

    def __init__(self,url):
        self.url=url
        #atributo Youtube: con la url y su progreso de descarga
        self.youtube = YouTube(self.url, on_progress_callback=YouTubeDownload.onProgress)
        self.stream=None
    

    def mostrarTitulo(self):
        st.write(f"**Título:** {self.youtube.title}")
        self.opcion_descarga = st.radio("**¿Qué desea descargar?**", ("Audio","Video"))  # Opción entre video o audio
        if self.opcion_descarga == "Video":
            self.mostrarStreamsVideo()
        else:
            self.mostrarStreamsAudio()


    def mostrarStreamsVideo(self):
        # Mostrar streams progresivos (video con audio) en cualquier formato 
        streams = self.youtube.streams.filter(progressive=True)  #minima calidad, si se quiere mas toca sin audio
        stream_opciones = [
            f"Resolución: {stream.resolution}/ FPS: {getattr(stream, 'fps', 'N/A')}/ Tipo: {stream.mime_type}"
            for stream in streams
        ]
        indice = st.selectbox("Elija una opción de stream de video: ", list(range(len(stream_opciones))),
                              format_func=lambda x: stream_opciones[x])
        self.stream = streams[indice]


    def mostrarStreamsAudio(self):
        streams = self.youtube.streams.filter(only_audio=True)  # Solo obtener streams de audio
        stream_opciones = [
            f"Audio bitrate: {stream.abr}/ Tipo: {stream.mime_type}"
            for stream in streams
        ]
        indice = st.selectbox("Elija una opción de stream de audio: ", list(range(len(stream_opciones))),
                              format_func=lambda x: stream_opciones[x])
        self.stream = streams[indice]


    def getTamañoArchivo(self):
        tamaño_archivo=self.stream.filesize/1000000 #tamaño del archivo en mega bites
        return tamaño_archivo
    

    def getContinuar(self, tamaño_archivo):
        st.write(f"**Título:** {self.youtube.title}")
        st.write(f"**Autor:** {self.youtube.author}")
        st.write(f"**Tamaño:**  {tamaño_archivo:.2f} MB")

        if self.opcion_descarga == "Video":
            st.write(f"**Resolución:** {self.stream.resolution or 'N/A'}")
            st.write(f"**FPS:** {getattr(self.stream, 'fps', 'N/A')}")
        else:
            st.write(f"**Bitrate de audio:** {self.stream.abr}")

        if st.button("DESCARGAR"):
            if self.opcion_descarga == "Video":
                self.descargar_video()  # Descargar video
            else:
                self.descargar_mp3()  # Descargar audio y convertir a MP3


    def descargar_video(self):
        self.stream.download(output_path="Videos")  # Descargar el video
        st.success("¡Video descargado!")

    def descargar_mp3(self):
        # Descargar en MP4 o WEMB
        archivo_descargado=self.stream.download(output_path="Audios")  # Descargar el audio
        st.success("¡Audio descargado!")

        # Convertir a MP3:
        # Obtener la ruta del archivo de salida, renombrándolo a .mp3
        archivo_mp3 = os.path.splitext(archivo_descargado)[0] + ".mp3"
        
        # Renombrar el archivo descargado a .mp3
        os.rename(archivo_descargado, archivo_mp3)

        st.success("¡Audio guardado en formato MP3!")
           

    @staticmethod
    def onProgress(stream=None, chunk=None, remaining=None):
        tamaño_archivo=stream.filesize/1000000 
        tamaño_descarga=tamaño_archivo-(remaining/1000000)
        st.progress(tamaño_descarga/tamaño_archivo)  


if __name__=="__main__":
    st.title("Descargador de videos YT") #titulo web
    url=st.text_input("Ingrese la URL del video") #input url

    #si la url no esta vacia:
    if url:
        descargar=YouTubeDownload(url)
        descargar.mostrarTitulo()

        if descargar.stream:
            tamaño_archivo=descargar.getTamañoArchivo()
            descargar.getContinuar(tamaño_archivo)

