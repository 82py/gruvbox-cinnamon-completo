# Independent workspaces and Rain / Espaços independentes e Rain

[English](#english) · [Português](#português)

## English

### A separate desktop for each workspace

The package provides four workspaces, each with its **own folder, visible files, and background choice**. Workspace 1 keeps the original Desktop folder; workspaces 2–4 start with empty folders named “Espaço 2”, “Espaço 3”, and “Espaço 4”. Switching workspaces changes the folder shown by Nemo without moving or deleting documents.

![How independent workspace folders and backgrounds work — illustration](imagens/independent-workspaces.png)

Use **Espaços de trabalho independentes** in the menu to pause or resume separation, open the folders, or check versions. Separation is X11-specific and pauses if the recorded package versions change. Review Cinnamon, Nemo, Muffin, mpv, and Python Xlib compatibility before revalidating after an update. Do not replace the recorded versions just to hide a warning.

**Fundos por espaço** saves the image only for the selected workspace. Without an image, the background is solid dark Gruvbox. Images subsequently chosen in Cinnamon settings are remembered for the workspace currently displayed. Each workspace may use an image or Rain.

### Rain: your own videos, looping on the desktop

![Rain interface with a sample local filename; no video is included](imagens/rain-ui-preview.png)

**Rain** lets you choose a local video and apply it to the current workspace. You may use a video you recorded or downloaded yourself; Rain plays the selected file **in an indefinite loop**. It does not download media automatically. No example video is bundled, and no folder named Relaxamento is required. Playback depends on the codecs supported by the installed mpv/FFmpeg.

Open Rain to choose the first video, or use **Escolher vídeo…** (“Choose video…”) in its tray menu. In the window, **Escolher arquivo…** chooses a file, **Usar vídeo nesta área** applies it to this workspace, and **Usar imagem estática** switches this workspace back to an image. The screenshots show the current Portuguese UI with sample data; the guides are bilingual.

The tray provides start, stop, restart, mute, and a draggable volume slider. Rain starts at volume 35 with sound muted; adjust it in the tray. On a static workspace, the video window is hidden and paused; returning to a Rain workspace shows it again. Workspaces can remember different video choices, but this is **one shared player**, not four simultaneous players.

Shortcuts: **Ctrl+F12** opens a video fullscreen, asking for a local file the first time and remembering the choice afterward. **Ctrl+Alt+M** toggles mute on the running player; it does not start a stopped player. The separate Relax launcher uses Celluloid fullscreen, with mpv as a fallback.

### Copy files between workspaces

![Actual copy-dialog widgets with example folders and files](imagens/copy-workspaces-preview.png)

Choose **Copiar para outra área…** (“Copy to another workspace…”) in Nemo's context menu, then click the destination once. Originals stay where they are; name collisions receive a numbered copy name. The destination buttons are disabled during copying; on success, the window closes and requests a notification. That selection cannot be copied again by repeated clicks.

If some items fail, an error dialog shows details before closing. Originals and completed copies are kept. To retry, select only the failed items. Opening the tool without a selection keeps it available for new drag-and-drop operations.

### Dependencies and troubleshooting

Rain uses mpv, xwinwrap, X11, Python GTK, and a systemd user service. Its complete integration code is included. Videos, codecs, drivers, and system services come from the destination computer. The bundled, pinned xwinwrap source is compiled locally without downloading code; see `vendor/xwinwrap/ORIGIN.txt` at the package root.

For errors, inspect `$HOME/.local/state/video-wallpaper/runtime.log`, the state files in `$HOME/.local/share/gruvbox-cinnamon/espacos`, and `systemctl --user status espacos-de-trabalho.service`. Source-machine logs, PIDs, locks, and transient state are not distributed.

---

## Português

![Espaços com arquivos e fundos próprios — ilustração](imagens/independent-workspaces.png)

O Rain reproduz em **loop contínuo** o vídeo local escolhido por você, inclusive vídeos que tenha gravado ou baixado por conta própria. Cada espaço pode guardar uma escolha diferente de vídeo ou imagem; um único reprodutor compartilhado carrega o vídeo da área ativa. Os formatos dependem dos codecs do mpv/FFmpeg instalado. Nenhuma mídia é incluída ou baixada automaticamente.

![Interface real do Rain com dados de exemplo](imagens/rain-ui-preview.png)

![Interface real de cópia entre áreas com dados de exemplo](imagens/copy-workspaces-preview.png)

O pacote oferece quatro espaços, cada um com pasta própria e preferência própria de fundo. No espaço 1 permanece a pasta original da Área de Trabalho; nos demais, as pastas vazias “Espaço 2”, “Espaço 3” e “Espaço 4”. A opção “Copiar para outra área…” do Nemo copia arquivos mantendo os originais.

No menu “Espaços de trabalho independentes” você pode pausar, reativar, abrir as pastas e conferir versões. A separação é específica de X11 e pausa se detectar mudança nas versões registradas. Antes de revalidar após atualização, confira Cinnamon, Nemo, Muffin, mpv e Python Xlib. Não substitua o valor de versões apenas para silenciar o aviso.

“Fundos por espaço” salva a imagem escolhida somente para o espaço selecionado. Sem imagem, aparece o fundo sólido escuro Gruvbox. Imagens escolhidas posteriormente nas configurações do Cinnamon são registradas para o espaço que estava sendo exibido.

“Rain” permite escolher um vídeo local e aplicá-lo ao espaço atual. Antes de escolher o primeiro vídeo, use a janela do Rain; a bandeja também oferece “Escolher vídeo…”. Não acompanha um vídeo de exemplo e não exige uma pasta chamada Relaxamento. Não há downloads automáticos.

A bandeja oferece iniciar, parar, reiniciar, silenciar e controle de volume arrastável. Ao mudar para uma área estática, a janela de vídeo fica oculta e pausada. Na área com Rain, ela reaparece. O player começa com volume 35 e som silenciado, conforme a configuração de origem; você pode ajustar na bandeja.

Atalhos: Ctrl+F12 abre um vídeo em tela cheia (a primeira vez pede um arquivo local; depois lembra sua escolha); Ctrl+Alt+M alterna o silêncio do player em execução. Se não houver player, o segundo atalho não o inicia.

O Rain usa mpv, xwinwrap, X11, Python GTK e o serviço de usuário do systemd. O código completo acompanha o pacote; vídeos, codecs externos, drivers e serviços do sistema são dependências do computador. O fonte de xwinwrap é compilado localmente na instalação, sem baixar código, preservando a revisão registrada em `vendor/xwinwrap/ORIGIN.txt`.

Se houver falha, confira `$HOME/.local/state/video-wallpaper/runtime.log`, o estado em `$HOME/.local/share/gruvbox-cinnamon/espacos` e `systemctl --user status espacos-de-trabalho.service`. Arquivos de log, PID, lock e estado transitório da máquina de origem não são distribuídos.

### Copiar para outra área

No menu de contexto do Nemo, escolha “Copiar para outra área…” e clique uma vez no destino. Durante a cópia, os destinos ficam desativados. A janela fecha ao concluir e solicita uma notificação. A seleção é consumida e não pode iniciar outra cópia por cliques repetidos.

Se parte dos itens falhar, o aviso mostra os detalhes antes de fechar. Os originais e as cópias já concluídas são preservados; para tentar novamente, selecione apenas os itens que falharam. A janela aberta sem seleção continua disponível para novas operações por arraste.
