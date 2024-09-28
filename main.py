import flet as ft
import os

from playMusic import PlayMusic

def carregarMusicas(folder_path):
    musics = [
        fileMusic for fileMusic in os.listdir(folder_path)
        if fileMusic.endswith(('.mp3', '.wav'))
    ]
    return musics

def removeExtensions(listMusics):
    musicTitles = []
    for music in listMusics:
        if '.mp3' in music:
            musicTitles.append(music.replace('.mp3', ''))
        else:
            musicTitles.append(music.replace('.wav', ''))
    return musicTitles

def addExtensions(titleMusica, listMusics):
    music = [music for music in listMusics if titleMusica in music]
    return music[0]

def main(page: ft.Page):
    page.title = "PlayMusic"

    musicFileList = carregarMusicas('./musics')
    musicTitles = removeExtensions(removeExtensions(musicFileList))

    selectedMusic = ''

    def checkMusicClicked(page, music):
        nonlocal selectedMusic, musicFileList
        page.go('/player')
        selectedMusic = addExtensions(music, musicFileList)

    def playList(musicsList):
        listTextButton = []
        for music in musicsList:
            listTextButton.append(ft.Row(controls=[ft.TextButton(
                music,
                on_click=lambda _, m=music: checkMusicClicked(page, m)
                )]))

        return listTextButton

    listTextButton = playList(musicTitles)

    def routeChange(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                controls=[ft.Column(
                    controls=listTextButton
                )
                ]
            )
        )
        if page.route == '/player':
            page.views.append(
                ft.View(
                    "/player",
                    controls=[
                        PlayMusic(musicFileList, selectedMusic, page)
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )
        page.update()
        
        
    def viewPop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = routeChange
    page.on_view_pop = viewPop
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main, assets_dir='./assets')