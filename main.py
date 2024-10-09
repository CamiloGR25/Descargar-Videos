import pytube
import streamlit as st #para mostrar GUI en la weeb


class YouTubeDownload:

    def __init__(self,url):
        self.url=url
        #atributo Youtube: con la url y su progreso de descarga
        self.youtube=pytube.YouTube(self.url, on_progress_callback=YouTubeDownload.onProgress)
        self.stream=None
    

    def mostrarTitulo(self):
        st.write(f"**Titulo:** {self.youtube.title}") #
        self.mostrarStreams()


    def mostrarStreams(self):
        streams=self.youtube.streams 
        #opciones de la calidad y tipo para descargar el video
        #streams.get_by_resolution
        stream_opciones=[
            f"Resolución: {stream.resolution or 'N/A'}/ FPS: {getattr(stream, 'fps', 'N/A')}/ Tipo: {stream.mime_type}"
              for stream in streams
        ]
        #indice = st.selectbox("Elija una opción de stream: ", list(range(len(stream_opciones))), format_func=lambda x: stream_opciones[x])
        #self.stream = streams[indice]  # Ahora selecciona el stream correcto usando el índice
        indice=st.selectbox("Elija una opción de stream: ", stream_opciones) #escojer una opcion mediante un selectbox
        self.stream=streams[stream_opciones(indice)] #guardar lo que se selecciono en el stream del metodo init


    def getTamañoArchivo(self):
        tamaño_archivo=self.stream.filesize/1000000 #tamaño del archivo en mega bites
        return tamaño_archivo
    

    def getContinuar(self, tamaño_archivo):
        st.write(f"**Titulo:** {self.youtube.title}")
        st.write(f"**Autor:** {self.youtube.author}")
        st.write(f"**Tamaño:**  {tamaño_archivo:.2f} MB")
        st.write(f"**Resolución:**  {self.stream.resolution or 'N/A'}" )
        st.write(f"**FPS:** {getattr(self.stream, 'FPS', 'N/A')}")

        if st.button("DESCARGAR"):
            st.descargar()
    

    def descargar(self):
        self.stream.download()
        st.success("¡DESCARGA COMPLETADA!")
    

    @staticmethod
    def onProgress(stream=None, chunk=None, remaining=None):
        file_size=stream.filesize/1000000 
        file_download=file_size-(remaining/1000000)
        st.progress(file_download/file_size)  


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

