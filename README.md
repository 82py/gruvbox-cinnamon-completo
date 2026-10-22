# Gruvbox Cinnamon Completo · GUI

[English](#english) · [Português](#português)

## English

A complete Gruvbox setup for Linux Mint Cinnamon, with a GTK interface to install, personalize, uninstall and restore selected components. Created by **Pir ([82py](https://github.com/82py))**, with assistance from **OpenAI Codex**.

**Version 1.1.0** · [Download the installer](https://github.com/82py/gruvbox-cinnamon-completo/releases/tag/v1.1.0) · Tested on Linux Mint 22.3, Cinnamon/Nemo 6.6.x, X11.

![Component selection](PREVIA-GUI-componentes.png)
![Appearance controls](PREVIA-GUI-aparencia.png)
![Independent workspaces](PREVIA-GUI-espacos.png)

![Menu and panel — historical base-theme VM screenshot](docs/imagens/menu-gruvbox-vm.png)

[![All 25 folder colors](docs/imagens/folder-colors-preview.png)](docs/CORES-DAS-PASTAS.md)

*Base-theme screenshot from the earlier VM validation; Radio3 is excluded from 1.1.0. GUI previews use sample data.*

### Extra workflow features

**Your files and backgrounds follow the workspace.** This setup adds per-workspace desktop folders and background management to Cinnamon's workspace workflow. Keep work files in one area, study material in another, and a different setup for relaxation. Switching areas changes the files shown on the desktop and that area's background. The first area keeps your existing Desktop folder; the other three start empty. Your files are not moved when you switch.

![Four independent workspace folders and backgrounds — concept illustration](docs/imagens/independent-workspaces.png)

**Copy directly to another area.** Nemo's “Copiar para outra área…” action shows the four destinations with previews. Originals remain in place. One selection makes one copy operation; the window closes and requests a notification when finished.

![Actual copy tool with four sample destinations](docs/imagens/copy-workspaces-preview.png)

**Rain turns your own local video into a looping background.** Choose a video you recorded or downloaded yourself; Rain plays it in an indefinite loop behind your desktop. Each area can remember a video or a static image. The tray lets you start, stop, restart, mute/unmute, and adjust volume. Switching to a static area hides and pauses the video. This uses one shared player, with the chosen video loaded for the active area.

![Actual Rain interface using a sample local filename](docs/imagens/rain-ui-preview.png)

No videos or wallpapers are bundled or downloaded automatically. MP4, WebM, and other local files work according to the installed mpv/FFmpeg codecs. The current application interfaces shown here use Portuguese; captions and guides explain the controls in both languages. See the [workspace and Rain guide](docs/ESPACOS-E-RAIN.md).

**Choose your folder color.** All 25 variants are shown in the [illustrated color guide](docs/CORES-DAS-PASTAS.md). The selector creates separate variants and preserves the original themes.

### Icon gallery

![A selection of actual application and system icons](docs/imagens/icons-gallery.png)

### Open

Download the supplied **TAR.GZ** from the release (it preserves icon symlinks). Extract the entire archive and run `iniciar-gui.sh` as your regular user. In the file manager, choose “Run” if prompted. Alternatively, open a terminal in the extracted folder and run `bash iniciar-gui.sh`. Opening the window does not install anything. Python 3, PyGObject and GTK 3 must already be available (included in the tested Mint installation). Choose English in the top right corner if desired.

1. Choose **Install / customize**, **Uninstall components**, or **Restore a previous point**.
2. Select components. On installation, unchecked components stay unchanged. On removal and restoration, checked components are the ones being changed; only managed components can be uninstalled.
3. Customize appearance, folder colors, fonts, Rain volume/mute, autostart and the four workspace folders, images and videos.
4. Review requirements and changes. Installation starts only after the final confirmation.
5. Log out and back in after changing desktop components so all processes load the new configuration.

There are **15 components**: application icons, system indicators, themes, cursor, panel/menu, profile-photo refresh, independent workspaces, Rain, folder colors, Nemo, terminal appearance, Relax shortcut, Flatpak fonts, optional application autostart and other preferences. **Radio3 and Magic Lamp are excluded**: the manager does not install them; an existing radio panel instance is preserved.

Current settings and workspace paths are read as defaults. The package layout button supplies the theme preset while keeping your media and folders. Dependencies are selected together; imported legacy workspaces that share Rain scripts are kept together. Fonts and selected preference values can be edited, and profiles can be exported/imported.

### Restore and personal data

Every operation creates a dated restore point before changing managed targets. Uninstall returns selected components to their state **before this manager first changed them**, which may already be customized; it does not mean factory Mint. Restore points can undo individual later operations. Failures attempt automatic rollback; an interrupted operation can be recovered from the safety tab on the next launch. Keep restore points until you are satisfied.

Documents in workspace folders, downloaded videos, background images and your profile photo are not included in the archive and are not deleted by uninstall. Created workspace folders remain. Removing Rain while retaining portable workspaces switches video backgrounds to static and retains video paths. The manager and its recovery history remain after component removal so you can restore them later.

By default the manager retains an offline copy of this installer under `~/.local/state/gruvbox-manager/installer`, along with its registry and private backups. Installed launchers use that copy, so the extracted source folder can be removed. If you disable retention, keep the source at its original location. Exported profiles contain local paths and preferences: treat them and restore points as private.

This manager does not adopt the old command-line installer's journal. If one exists, restore that installation using its original uninstaller first. Existing manual customization is backed up normally. Administrative authentication is requested only if you explicitly choose dependency installation. Optional applications are not bundled.

Magic Lamp was removed after a desktop diagnostic found an animation error and an orphan full-screen window clone. Native Cinnamon animations remain available.

This release fixes actor cleanup in the system-color and MintUpdate-color extensions. It also preserves the current Nemo disabled-extension list, including `ColumnExtension+NemoPython`, when installing, removing or restoring components. Antivirus settings are not changed.

### Scope and validation

Tested environment: Linux Mint 22.3, Cinnamon/Nemo 6.6.x, X11, systemd user session, four workspaces. Other environments have not been validated. The updated code passed 51 Python and 14 actor-lifecycle checks. The public installer completed an isolated Mint VM installation, reboot, feature, removal and post-removal reboot cycle with no differences in the compared files or preferences. Physical GPU, printer, Wi-Fi and Bluetooth hardware were not exercised in the VM. See [GUI validation](VALIDACAO-GUI.json). [Original theme documentation](README-TEMA.md) describes the base release and may mention its older command-line workflow and Radio3; this page is the guide for the GUI variant.

No wallpaper images, videos, personal photo, private keys or saved personal profiles are distributed. Media must be supplied by the user. Earlier releases remain available in the release history.

### Guides

[Applets and extensions](docs/APPLETS-E-EXTENSOES.md) · [Installation](docs/INSTALAR.md) · [Uninstall and restore](docs/DESINSTALAR.md) · [Workspaces and Rain](docs/ESPACOS-E-RAIN.md) · [Folder colors](docs/CORES-DAS-PASTAS.md) · [Changelog](CHANGELOG.md). All project guides include English first and Portuguese below.

### Credits, vibe coding and disclaimer

Created by **Pir (82py)** with **OpenAI Codex**, using vibe coding. Built on work by **morhetz** (Gruvbox), **SylEleuth** (Gruvbox Plus), and the authors of the included desktop themes, cursor and components. Full authorship and license notices remain in [credits](CREDITOS.md), [LICENSE](LICENSE) and [third-party licenses](LICENSES). Radio3 authors remain acknowledged in the base project's history; Radio3 itself is excluded here.

#### Acknowledgments

My thanks to the people whose code and artwork made this possible:

- **Pavel Pertsev (morhetz)** — the original [Gruvbox palette](https://github.com/morhetz/gruvbox).
- **SylEleuth** and contributors — [Gruvbox Plus Icon Pack](https://github.com/SylEleuth/gruvbox-plus-icon-pack).
- **Fausto-Korpsvart** and **Vince Liuice** — the [GTK theme](https://github.com/Fausto-Korpsvart/Gruvbox-GTK-Theme) used as the visual base.
- **Keefer Rourke** and **sainnhe** — Capitaine Cursors and its [Gruvbox variant](https://github.com/sainnhe/capitaine-cursors).
- **Clement Lefebvre** and the **Linux Mint contributors** — Cinnamon, Nemo, XApp, themes, and original system artwork.
- **klangman** and **hermes83** — [Magic Lamp](https://github.com/klangman/CinnamonMagicLamp), used in earlier releases, and its original extension base.
- **claudiux** and Cinnamon Spices contributors — [Radio3](https://cinnamon-spices.linuxmint.com/applets/view/360), included in earlier releases / incluído nas versões anteriores.
- **akarzim** — the original folder color chooser; **el-amine-404**, **claudiux**, and **anaximeno** — included Nemo actions.
- **David Reveman / Novell**, **Shantanu Goel**, **Aaahh**, and **mmhobi7** — the [xwinwrap code and forks](https://github.com/mmhobi7/xwinwrap).

The icon pack also builds on work by **Sam Hewitt**, **Andrea Bonanni**, **Gustavo Costa**, **Vince Liuice**, **Alexey Varfolomeev**, the **Papirus Development Team**, the **Numix Team**, **Keefer Rourke**, and **Adhe**. The MOD theme was traced to the **Twilight4** collection; this does not establish authorship of every historical CSS change. Full attribution, provenance details, and original license notices are in [CREDITOS.md](CREDITOS.md) and [LICENSES/](LICENSES/).

#### Disclaimer

Provided **“as is”**, without warranty of any kind, express or implied. To the extent permitted by applicable law, the authors and contributors are not liable for damages arising from use. Install and use at your own risk; keep an independent backup of personal files. Third-party components retain their respective licenses.

## Português

Uma personalização Gruvbox completa para Linux Mint Cinnamon, com interface GTK para instalar, personalizar, desinstalar e restaurar componentes selecionados. Criada por **Pir ([82py](https://github.com/82py))**, com assistência do **OpenAI Codex**.

**Versão 1.1.0** · [Baixar o instalador](https://github.com/82py/gruvbox-cinnamon-completo/releases/tag/v1.1.0) · Testada em Linux Mint 22.3, Cinnamon/Nemo 6.6.x, X11.

![Seleção de componentes](PREVIA-GUI-componentes.png)

![As 25 cores de pastas](docs/imagens/folder-colors-preview.png)

### Recursos extras da personalização

**Arquivos e fundos acompanham o espaço.** Esta configuração acrescenta pastas de desktop e gerenciamento de fundos por espaço ao fluxo de trabalho do Cinnamon. Você pode separar arquivos de trabalho, material de estudo e um ambiente para relaxar. Ao trocar de área, mudam os arquivos exibidos no desktop e o fundo escolhido para ela. A primeira área mantém sua pasta de Área de Trabalho; as outras três começam vazias. Trocar de área não move os arquivos.

![Quatro espaços com pastas e fundos próprios — ilustração do funcionamento](docs/imagens/independent-workspaces.png)

**Copie diretamente para outra área.** A ação “Copiar para outra área…” do Nemo mostra os quatro destinos com prévias. Os originais ficam onde estão. Cada seleção faz uma única operação de cópia; ao terminar, a janela fecha e solicita uma notificação.

![Ferramenta real de cópia com quatro destinos de exemplo](docs/imagens/copy-workspaces-preview.png)

**O Rain transforma seu vídeo local em fundo em loop.** Escolha um vídeo que você gravou ou baixou por conta própria; o Rain o reproduz repetidamente atrás do desktop. Cada área pode guardar a escolha de um vídeo ou de uma imagem estática. A bandeja permite iniciar, parar, reiniciar, silenciar/reativar o som e ajustar o volume. Em uma área estática, o vídeo fica oculto e pausado. Há um único reprodutor compartilhado, que carrega o vídeo escolhido para a área ativa.

![Interface real do Rain com um nome de arquivo de exemplo](docs/imagens/rain-ui-preview.png)

Nenhum vídeo ou fundo é incluído ou baixado automaticamente. MP4, WebM e outros arquivos locais dependem dos codecs disponíveis no mpv/FFmpeg instalado. As interfaces mostradas usam português; as legendas e os guias explicam os controles nos dois idiomas. Consulte o [guia dos espaços e do Rain](docs/ESPACOS-E-RAIN.md).

**Escolha a cor das pastas.** As 25 variantes aparecem no [guia ilustrado de cores](docs/CORES-DAS-PASTAS.md). O seletor cria variantes separadas e preserva os temas originais.

### Galeria de ícones

![Seleção de ícones reais de aplicativos e de sistema](docs/imagens/icons-gallery.png)

### Abrir

Baixe o **TAR.GZ** fornecido na versão (ele preserva os links dos ícones). Extraia o arquivo inteiro e execute `iniciar-gui.sh` como usuário comum. No gerenciador de arquivos, escolha “Executar” se solicitado. Como alternativa, abra o terminal na pasta extraída e execute `bash iniciar-gui.sh`. Abrir a janela não instala nada. Python 3, PyGObject e GTK 3 precisam estar disponíveis (já presentes no Mint testado). A interface inicia em português e permite mudar para inglês no canto superior direito.

1. Escolha **Instalar / personalizar**, **Desinstalar componentes** ou **Restaurar ponto anterior**.
2. Selecione os componentes. Na instalação, desmarcado significa manter como está. Na remoção e restauração, os marcados serão alterados; só é possível desinstalar componentes gerenciados.
3. Personalize aparência, cores de pastas, fontes, volume/mudo do Rain, inicialização e as quatro pastas, imagens e vídeos dos espaços.
4. Confira requisitos e alterações. A instalação começa somente após a confirmação final.
5. Saia da sessão e entre novamente depois de mudar componentes do desktop para que todos os processos carreguem a nova configuração.

São **15 componentes**: ícones de aplicativos, indicadores do sistema, temas, cursor, painel/menu, atualização da foto, espaços independentes, Rain, cores de pastas, Nemo, visual do terminal, atalho Relax, fontes Flatpak, inicialização opcional e outras preferências. **Radio3 e Magic Lamp foram excluídos**: o gerenciador não os instala; uma instância de rádio já existente no painel é preservada.

As configurações e caminhos atuais dos espaços são lidos como padrão. O botão de visual do pacote oferece o preset do tema mantendo suas mídias e pastas. Dependências são selecionadas juntas; espaços antigos que compartilham scripts com o Rain permanecem juntos. É possível editar fontes e preferências selecionadas, além de exportar/importar perfis.

### Restauração e dados pessoais

Cada operação cria um ponto datado antes de alterar arquivos e preferências gerenciados. Desinstalar retorna os componentes selecionados ao estado **anterior à primeira alteração por este gerenciador**, que pode já ser personalizado; não significa o padrão de fábrica do Mint. Pontos permitem desfazer operações posteriores individualmente. Falhas tentam reversão automática; uma operação interrompida pode ser recuperada na aba de segurança na próxima abertura. Guarde os pontos até estar satisfeito.

Documentos dos espaços, vídeos baixados, imagens de fundo e foto pessoal não entram no pacote e não são apagados pela desinstalação. Pastas criadas permanecem. Remover o Rain mantendo espaços portáveis troca fundos em vídeo por estáticos e conserva os caminhos dos vídeos. O gerenciador e o histórico permanecem após remover componentes para permitir recuperá-los.

Por padrão, uma cópia do instalador fica em `~/.local/state/gruvbox-manager/installer`, junto do registro e dos backups privados. Os atalhos instalados usam essa cópia, permitindo remover a pasta extraída. Se desativar essa retenção, mantenha a origem no mesmo local. Perfis exportados contêm caminhos locais e preferências: trate-os e os pontos de restauração como privados.

O gerenciador não assume o registro do antigo instalador de terminal. Se ele existir, restaure aquela instalação pelo desinstalador original primeiro. Personalizações manuais existentes são copiadas normalmente para backup. A autenticação administrativa aparece apenas se você escolher instalar dependências. Aplicativos opcionais não são incluídos.

Magic Lamp foi removido após o diagnóstico encontrar um erro de animação e um clone órfão de janela sobre a tela inteira. As animações nativas do Cinnamon continuam disponíveis.

Esta versão corrige a liberação de elementos nas extensões de cores do sistema e do MintUpdate. Ela também preserva a lista atual de extensões desativadas do Nemo, inclusive `ColumnExtension+NemoPython`, ao instalar, remover ou restaurar componentes. A configuração do antivírus não é alterada.

### Escopo e validação

Ambiente testado: Linux Mint 22.3, Cinnamon/Nemo 6.6.x, X11, sessão systemd do usuário e quatro espaços. Outros ambientes não foram validados. O código atualizado passou em 51 testes Python e 14 testes de ciclo de vida dos elementos. O instalador público completou na VM Mint isolada a instalação, o reinício, a conferência dos recursos, a remoção e outro reinício sem diferenças nos arquivos e preferências comparados. GPU física, impressora, Wi-Fi e Bluetooth físicos não foram exercitados na VM. Consulte a [validação da GUI](VALIDACAO-GUI.json). A [documentação original do tema](README-TEMA.md) descreve a versão base e pode mencionar o fluxo antigo de terminal e o Radio3; esta página orienta o uso da variante GUI.

O pacote não contém imagens de fundo, vídeos, foto pessoal, chaves privadas ou perfis pessoais salvos. As mídias são fornecidas pelo usuário. As versões anteriores continuam disponíveis no histórico de releases.

### Guias

[Applets e extensões](docs/APPLETS-E-EXTENSOES.md) · [Instalação](docs/INSTALAR.md) · [Desinstalação e restauração](docs/DESINSTALAR.md) · [Espaços e Rain](docs/ESPACOS-E-RAIN.md) · [Cores de pastas](docs/CORES-DAS-PASTAS.md) · [Alterações](CHANGELOG.md). Os guias do projeto incluem inglês primeiro e português abaixo.

### Créditos, vibe coding e aviso de responsabilidade

Criado por **Pir (82py)** com **OpenAI Codex**, usando vibe coding. Baseado no trabalho de **morhetz** (Gruvbox), **SylEleuth** (Gruvbox Plus) e dos autores dos temas, cursor e componentes incluídos. A autoria completa e as licenças permanecem nos [créditos](CREDITOS.md), na [licença](LICENSE) e nas [licenças de terceiros](LICENSES). Os autores do Radio3 continuam reconhecidos no histórico do projeto base; o Radio3 foi excluído desta variante.

#### Agradecimentos

Meu agradecimento às pessoas cujo código e desenhos tornaram isso possível:

- **Pavel Pertsev (morhetz)** — a [paleta Gruvbox original](https://github.com/morhetz/gruvbox).
- **SylEleuth** e colaboradores — [Gruvbox Plus Icon Pack](https://github.com/SylEleuth/gruvbox-plus-icon-pack).
- **Fausto-Korpsvart** e **Vince Liuice** — o [tema GTK](https://github.com/Fausto-Korpsvart/Gruvbox-GTK-Theme) usado como base visual.
- **Keefer Rourke** e **sainnhe** — Capitaine Cursors e sua [variante Gruvbox](https://github.com/sainnhe/capitaine-cursors).
- **Clement Lefebvre** e os **colaboradores do Linux Mint** — Cinnamon, Nemo, XApp, temas e desenhos originais do sistema.
- **klangman** e **hermes83** — [Magic Lamp](https://github.com/klangman/CinnamonMagicLamp), usado em versões anteriores, e a extensão que lhe serviu de base.
- **claudiux** e colaboradores do Cinnamon Spices — [Radio3](https://cinnamon-spices.linuxmint.com/applets/view/360), included in earlier releases / incluído nas versões anteriores.
- **akarzim** — seletor original de cores das pastas; **el-amine-404**, **claudiux** e **anaximeno** — ações do Nemo incluídas.
- **David Reveman / Novell**, **Shantanu Goel**, **Aaahh** e **mmhobi7** — o [código e as variantes do xwinwrap](https://github.com/mmhobi7/xwinwrap).

O pacote de ícones também se apoia no trabalho de **Sam Hewitt**, **Andrea Bonanni**, **Gustavo Costa**, **Vince Liuice**, **Alexey Varfolomeev**, **Papirus Development Team**, **Numix Team**, **Keefer Rourke** e **Adhe**. A variante MOD do tema foi localizada na coleção de **Twilight4**; isso não identifica a autoria de cada alteração histórica do CSS. Os créditos completos, os detalhes de origem e os avisos de licença estão em [CREDITOS.md](CREDITOS.md) e [LICENSES/](LICENSES/).

#### Aviso de responsabilidade

Fornecido **“no estado em que se encontra” (“as is”)**, sem garantias expressas ou implícitas. Na extensão permitida pela legislação aplicável, os autores e colaboradores não respondem por danos decorrentes do uso. Instale e use por sua conta e risco; mantenha uma cópia independente dos arquivos pessoais. Componentes de terceiros mantêm suas respectivas licenças.
