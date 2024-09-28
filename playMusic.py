import threading
import flet as ft
import pygame

from time import sleep

pygame.init()


class PlayMusic(ft.Column):
    def __init__(self, listMusic, musicInitial, page) -> None:
        super().__init__()
        self.bgImg              =  ft.Image(src='./assets/img/fundoPlayList.png', width=300, height=300)
        self.listaMusica        =  listMusic
        self.musicInitial       =  musicInitial
        self.page               =  page
        self.statusMusica       =  True
        self.countMusic         =  self.listaMusica.index(self.musicInitial)

        # Titulo da música
        self.titleMusic         =  ft.Text(value=self.musicInitial)

        # Botões
        self.buttonSkipPrevious =  ft.IconButton(ft.icons.SKIP_PREVIOUS, on_click=lambda _: self.skipPrevious())
        self.buttonPlayPause    =  ft.IconButton(ft.icons.PAUSE_CIRCLE, on_click=lambda _: self.playPause())
        self.buttonSkipNext     =  ft.IconButton(ft.icons.SKIP_NEXT, on_click=lambda _: self.skipNext())
        
        # Configurações Padrão do PlayMusic
        self.horizontal_alignment   =  ft.CrossAxisAlignment.CENTER

        # variáveis padrão
        self.vertical_alignment     =  ft.MainAxisAlignment.CENTER

        # Inicializando o mixer do pygame
        self.mixer = pygame.mixer
        self.mixer.init()

        # Define um evento quando a música terminar
        self.mixer.music.set_endevent(pygame.USEREVENT)

        # Iniciando a música
        self.mixer.music.load(f'./musics/{self.listaMusica[self.countMusic]}')
        self.mixer.music.play()

        self.duration         =  self.mixer.Sound(f'./musics/{self.listaMusica[self.countMusic]}').get_length()
        
        # Barra de carregamento
        self.loadingBar         =  ft.Slider(min=0, max=self.duration, width=300, on_change_end=self.seekAudio)

        # Inicializando os botões
        self.renderLayout()

        #self.stats_on_change_end = False
        self.pos = 0

        # Inicializa o reprodução das musicas
        self.threadingMain              =  threading.Thread(target=self.main, daemon=True)
        self.threadingLoadingBar        =  threading.Thread(target=self.updateProgressBar, daemon=True)

        self.threadingMain.start()
        self.threadingLoadingBar.start()


    def seekAudio(self, e):
        self.mixer.music.pause()
        self.pos = e.control.value
        self.mixer.music.play(start=self.pos)
        self.buttonPlayPause.icon    =  ft.icons.PAUSE_CIRCLE
        self.statusMusica            =  True
        self.update()

    def updateProgressBar(self):
        sleep(0.2)
        while self.mixer.music.get_busy():
            musicPosMilliseconds = self.mixer.music.get_pos()
            if musicPosMilliseconds == -1:
                break

            current_time = (musicPosMilliseconds / 1000) + self.pos
            
            if current_time < 0:
                current_time = 0
            if current_time > self.duration:
                current_time = self.duration

            self.loadingBar.value = current_time
            self.update()
            sleep(0.5)

    def updateLoadingBar(self):
        self.pos = 0
        self.loadingBar.max = self.duration
        self.loadingBar.value = 0

    def renderLayout(self):
        self.controls.clear()
        self.controls.extend([
            ft.Row(controls         =  [
                self.bgImg],
                alignment           =  self.vertical_alignment
                ),
            ft.Row(controls         =  [
                self.titleMusic
                ],
                alignment           =  self.vertical_alignment, 
                ),
            ft.Row(controls         =  [
                self.loadingBar
                ],
                alignment           =  self.vertical_alignment
            ),
            ft.Row(
                controls            =  [
                    self.buttonSkipPrevious,
                    self.buttonPlayPause,
                    self.buttonSkipNext
                ],
                alignment           =  self.vertical_alignment
                )
        ])
        self.page.update()

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if (self.countMusic + 1) < len(self.listaMusica):
                        self.countMusic += 1
                        self.mixer.music.load(f'./musics/{self.listaMusica[self.countMusic]}')
                        self.duration = pygame.mixer.Sound(f'./musics/{self.listaMusica[self.countMusic]}').get_length()
                        self.mixer.music.play()
                        self.titleMusic.value = self.listaMusica[self.countMusic]
                        self.updateLoadingBar()
                        self.renderLayout()
                        self.updateProgressBar()

                    else:
                        self.countMusic = 0
                        self.buttonPlayPause.icon = ft.icons.REPLAY
                        self.updateLoadingBar()
                        self.renderLayout()
                        self.mixer.music.stop()
                        break
    
    def skipPrevious(self):
        if (self.countMusic - 1) >= 0:
            self.countMusic -= 1
            self.buttonPlayPause.icon = ft.icons.PAUSE_CIRCLE
            self.mixer.music.load(f'./musics/{self.listaMusica[self.countMusic]}')
            self.duration = pygame.mixer.Sound(f'./musics/{self.listaMusica[self.countMusic]}').get_length()

            self.mixer.music.play()  
            self.titleMusic.value = self.listaMusica[self.countMusic]
            self.updateLoadingBar()
            self.renderLayout()
            self.updateProgressBar()

    def playPause(self):
        if self.statusMusica:
            self.buttonPlayPause.icon    =  ft.icons.PLAY_CIRCLE
            self.statusMusica            =  False
            self.mixer.music.pause()
        else:
            self.buttonPlayPause.icon    =  ft.icons.PAUSE_CIRCLE
            self.statusMusica            =  True
            self.mixer.music.unpause()
            self.updateProgressBar()
        
        self.renderLayout()

    def skipNext(self):
        if (self.countMusic + 1) < len(self.listaMusica):
            self.countMusic += 1
            self.buttonPlayPause.icon = ft.icons.PAUSE_CIRCLE
            self.mixer.music.load(f'./musics/{self.listaMusica[self.countMusic]}')
            self.duration = pygame.mixer.Sound(f'./musics/{self.listaMusica[self.countMusic]}').get_length()
            self.mixer.music.play()
            self.titleMusic.value = self.listaMusica[self.countMusic]
            self.updateLoadingBar()
            self.renderLayout()
            self.updateProgressBar()
        
