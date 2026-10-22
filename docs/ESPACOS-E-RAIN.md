# Espaços independentes e Rain

O pacote oferece quatro espaços, cada um com pasta própria e preferência própria de fundo. No espaço 1 permanece a pasta original da Área de Trabalho; nos demais, as pastas vazias “Espaço 2”, “Espaço 3” e “Espaço 4”. A opção “Copiar para outra área…” do Nemo copia arquivos mantendo os originais.

No menu “Espaços de trabalho independentes” você pode pausar, reativar, abrir as pastas e conferir versões. A separação é específica de X11 e pausa se detectar mudança nas versões registradas. Antes de revalidar após atualização, confira Cinnamon, Nemo, Muffin, mpv e Python Xlib. Não substitua o valor de versões apenas para silenciar o aviso.

“Fundos por espaço” salva a imagem escolhida somente para o espaço selecionado. Sem imagem, aparece o fundo sólido escuro Gruvbox. Imagens escolhidas posteriormente nas configurações do Cinnamon são registradas para o espaço que estava sendo exibido.

“Rain” permite escolher um vídeo local e aplicá-lo ao espaço atual. Antes de escolher o primeiro vídeo, use a janela do Rain; a bandeja também oferece “Escolher vídeo…”. Não acompanha um vídeo de exemplo e não exige uma pasta chamada Relaxamento. Não há downloads automáticos.

A bandeja oferece iniciar, parar, reiniciar, silenciar e controle de volume arrastável. Ao mudar para uma área estática, a janela de vídeo fica oculta e pausada. Na área com Rain, ela reaparece. O player começa com volume 35 e som silenciado, conforme a configuração de origem; você pode ajustar na bandeja.

Atalhos: Ctrl+F12 abre um vídeo em tela cheia (a primeira vez pede um arquivo local; depois lembra sua escolha); Ctrl+Alt+M alterna o silêncio do player em execução. Se não houver player, o segundo atalho não o inicia.

O Rain usa mpv, xwinwrap, X11, Python GTK e o serviço de usuário do systemd. O código completo acompanha o pacote; vídeos, codecs externos, drivers e serviços do sistema são dependências do computador. O fonte de xwinwrap é compilado localmente na instalação, sem baixar código, preservando a revisão registrada em `vendor/xwinwrap/ORIGIN.txt`.

Se houver falha, confira `$HOME/.local/state/video-wallpaper/runtime.log`, o estado em `$HOME/.local/share/gruvbox-cinnamon/espacos` e `systemctl --user status espacos-de-trabalho.service`. Arquivos de log, PID, lock e estado transitório da máquina de origem não são distribuídos.

## Copiar para outra área

No menu de contexto do Nemo, escolha “Copiar para outra área…” e clique uma vez no destino. Durante a cópia, os destinos ficam desativados. A janela fecha ao concluir e solicita uma notificação. A seleção é consumida e não pode iniciar outra cópia por cliques repetidos.

Se parte dos itens falhar, o aviso mostra os detalhes antes de fechar. Os originais e as cópias já concluídas são preservados; para tentar novamente, selecione apenas os itens que falharam. A janela aberta sem seleção continua disponível para novas operações por arraste.
