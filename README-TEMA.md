# Gruvbox Cinnamon Completo

![Gruvbox Cinnamon: actual icons from the package](docs/imagens/gruvbox-cinnamon-preview.png)

[English](#english) · [Português](#português)

## English

A complete Gruvbox desktop setup for **Linux Mint Cinnamon**, with custom icons, a colorful panel, independent workspaces, and video wallpapers.

Created by **Pir ([82py](https://github.com/82py))**, with assistance from **OpenAI Codex**. Based on Gruvbox and the work of the authors credited in [CREDITOS.md](CREDITOS.md).

**Current release:** [1.0.3](https://github.com/82py/gruvbox-cinnamon-completo/releases/tag/v1.0.3) · **Target:** Linux Mint 22.3, Cinnamon/Nemo 6.6, X11.

![Menu and panel in the Linux Mint test VM](docs/imagens/menu-gruvbox-vm.png)

[![Folder color preview — see all 25 options](docs/imagens/folder-colors-preview.png)](docs/CORES-DAS-PASTAS.md)

*Actual Mint test VM above; artwork samples are rendered from the package SVGs. No personal wallpaper or profile photo is included.*

### What's included

- Customized Gruvbox Plus Dark application icons, colorful system icons, menu categories, and panel indicators.
- Desktop themes, cursor, panel and menu layout, Magic Lamp, Radio3, and custom extensions.
- **Rain:** video wallpapers with tray controls for playback, volume, and mute.
- Four workspaces with their own folders and backgrounds, plus a tool to copy files between them.
- A folder color picker, Nemo actions, the Relax fullscreen video launcher, an isolated terminal appearance profile, and font fixes for selected Flatpak apps.

**Personal videos, wallpaper images, profile photos, and documents are not included.** The setup starts with a solid Gruvbox background; you choose your own media. Third-party applications are installed separately.

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

### Install

Download the **TAR.GZ** and its **SHA-256 checksum file** from [Releases](https://github.com/82py/gruvbox-cinnamon-completo/releases). Use the TAR.GZ rather than GitHub's automatic ZIP to preserve icon symlinks. Extract it and open a terminal in the extracted folder:

```sh
bash verificar.sh
bash instalar.sh
```

Run as your regular user, then log out and back in. The installer creates backups and does not modify internal Cinnamon or application files. Dependencies are installed separately as described in the [installation guide](docs/INSTALAR.md).

To restore the previous setup:

```sh
bash desinstalar.sh
```

An existing managed installation must be uninstalled before installing another version. Read the [restoration guide](docs/DESINSTALAR.md) first. All project guides provide English first, followed by Portuguese: [workspaces and Rain](docs/ESPACOS-E-RAIN.md), [folder colors](docs/CORES-DAS-PASTAS.md).

### Compatibility and testing

Tested environment: **Linux Mint 22.3, Cinnamon/Nemo 6.6.x, X11**. The source machine runs Cinnamon 6.6.9 and Nemo/Muffin 6.6.3; the VM validation used Cinnamon 6.6.4, Nemo 6.6.3, and Muffin 6.6.1. Testing is limited to these environments. See the [platform assessment](docs/UBUNTU.md) for technical details.

- **1.0.3:** 22 automated tests passed, including GTK regression tests for repeated clicks in the file-copy dialog. Both final archives were also checked for folder colors and icon resolution.
- **1.0.2:** full installation, feature checks, uninstallation, and reboots were tested in a Linux Mint 22.3 QEMU/KVM VM. The final comparison found no differences in 115 installation destinations and 936 preferences; test documents were preserved.

The full VM cycle was not repeated for 1.0.3. See the [VM report](docs/VALIDACAO-VM.md), [copy-dialog tests](tests/test_copy_dialog.py), [coverage audit](docs/AUDITORIA-FINAL.md), and [GitHub Actions](https://github.com/82py/gruvbox-cinnamon-completo/actions).

### Source, credits, and licenses

`payload/` contains the portable desktop components; `scripts/` contains the installation and restoration tools; `tests/` contains the automated checks. The public installer builds xwinwrap from the source included in `vendor/xwinwrap/`.

The integration code is licensed under **GPL-3.0-or-later**. Third-party components retain their own licenses and attribution. See [credits](CREDITOS.md), [license notices](LICENSES/), [provenance](docs/PROVENIENCIA.md), and [contributing](CONTRIBUTING.md).

### Made with vibe coding

This project grew out of a personal desktop experiment, built through **vibe coding**. I brought the ideas, chose the look, and reviewed the results; OpenAI Codex helped turn that back-and-forth into icons, scripts, integrations, documentation, and a distributable package. The process included trying things in Cinnamon, refining them, and testing installation and restoration. The original projects and their authors remain credited throughout.

#### Disclaimer

This project is provided **“as is”**, without warranties of any kind, express or implied. To the extent permitted by applicable law, the author and contributors shall not be liable for damages, data loss, or other consequences arising from its installation or use. **Install and use at your own risk.** Review the scripts and keep backups before making changes. See [LICENSE](LICENSE) for the applicable terms. Third-party components retain their own licenses.

#### Acknowledgments

My thanks to the people whose code and artwork made this possible:

- **Pavel Pertsev (morhetz)** — the original [Gruvbox palette](https://github.com/morhetz/gruvbox).
- **SylEleuth** and contributors — [Gruvbox Plus Icon Pack](https://github.com/SylEleuth/gruvbox-plus-icon-pack).
- **Fausto-Korpsvart** and **Vince Liuice** — the [GTK theme](https://github.com/Fausto-Korpsvart/Gruvbox-GTK-Theme) used as the visual base.
- **Keefer Rourke** and **sainnhe** — Capitaine Cursors and its [Gruvbox variant](https://github.com/sainnhe/capitaine-cursors).
- **Clement Lefebvre** and the **Linux Mint contributors** — Cinnamon, Nemo, XApp, themes, and original system artwork.
- **klangman** and **hermes83** — [Magic Lamp](https://github.com/klangman/CinnamonMagicLamp) and its original extension base.
- **claudiux** and Cinnamon Spices contributors — [Radio3](https://cinnamon-spices.linuxmint.com/applets/view/360).
- **akarzim** — the original folder color chooser; **el-amine-404**, **claudiux**, and **anaximeno** — included Nemo actions.
- **David Reveman / Novell**, **Shantanu Goel**, **Aaahh**, and **mmhobi7** — the [xwinwrap code and forks](https://github.com/mmhobi7/xwinwrap).

The icon pack also builds on work by **Sam Hewitt**, **Andrea Bonanni**, **Gustavo Costa**, **Vince Liuice**, **Alexey Varfolomeev**, the **Papirus Development Team**, the **Numix Team**, **Keefer Rourke**, and **Adhe**. The MOD theme was traced to the **Twilight4** collection; this does not establish authorship of every historical CSS change. Full attribution, provenance details, and original license notices are in [CREDITOS.md](CREDITOS.md) and [LICENSES/](LICENSES/).


---

## Português

Uma personalização Gruvbox completa para o **Linux Mint Cinnamon**, com ícones próprios, painel colorido, espaços de trabalho independentes e fundos em vídeo.

Criada por **Pir ([82py](https://github.com/82py))**, com assistência do **OpenAI Codex**. Baseada no Gruvbox e no trabalho dos autores reconhecidos em [CREDITOS.md](CREDITOS.md).

**Versão atual:** [1.0.3](https://github.com/82py/gruvbox-cinnamon-completo/releases/tag/v1.0.3) · **Plataforma:** Linux Mint 22.3, Cinnamon/Nemo 6.6, X11.

### O que está incluído

- Ícones de aplicativos Gruvbox Plus Dark personalizados, ícones de sistema coloridos, categorias do menu e indicadores do painel.
- Temas visuais, cursor, organização do painel e dos menus, Magic Lamp, Radio3 e extensões próprias.
- **Rain:** fundos em vídeo com controles de reprodução, volume e som na bandeja.
- Quatro espaços com pastas e fundos próprios, além de uma ferramenta para copiar arquivos entre eles.
- Seletor de cores das pastas, ações do Nemo, atalho Relax para vídeo em tela cheia, perfil visual isolado do terminal e correções de fontes para determinados aplicativos Flatpak.

**Vídeos, imagens de fundo, foto de perfil e documentos pessoais não acompanham o pacote.** A configuração começa com um fundo sólido Gruvbox; cada pessoa escolhe suas mídias. Aplicativos de terceiros são instalados separadamente.

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

### Instalação

Baixe o **TAR.GZ** e seu **arquivo de verificação SHA-256** em [Releases](https://github.com/82py/gruvbox-cinnamon-completo/releases). Prefira o TAR.GZ ao ZIP automático do GitHub para preservar os links dos ícones. Extraia e abra um terminal na pasta extraída:

```sh
bash verificar.sh
bash instalar.sh
```

Execute como usuário comum; depois, encerre a sessão e entre novamente. O instalador cria cópias de segurança e não modifica arquivos internos do Cinnamon ou dos aplicativos. As dependências são instaladas separadamente, conforme o [guia de instalação](docs/INSTALAR.md).

Para restaurar a configuração anterior:

```sh
bash desinstalar.sh
```

Uma instalação gerenciada anterior precisa ser desinstalada antes de instalar outra versão. Leia primeiro o [guia de restauração](docs/DESINSTALAR.md). Veja também os guias de [espaços e Rain](docs/ESPACOS-E-RAIN.md) e [cores das pastas](docs/CORES-DAS-PASTAS.md).

### Compatibilidade e testes

Ambiente testado: **Linux Mint 22.3, Cinnamon/Nemo 6.6.x, X11**. A máquina de origem usa Cinnamon 6.6.9 e Nemo/Muffin 6.6.3; a validação em VM usou Cinnamon 6.6.4, Nemo 6.6.3 e Muffin 6.6.1. Os testes se limitam a esses ambientes. Veja a [avaliação de plataformas](docs/UBUNTU.md) para os detalhes técnicos.

- **1.0.3:** 22 testes automatizados aprovados, incluindo testes GTK contra cliques repetidos na janela de cópia. Os dois compactados finais também foram verificados quanto às cores das pastas e à resolução dos ícones.
- **1.0.2:** instalação completa, recursos, desinstalação e reinicializações testados em uma VM QEMU/KVM com Linux Mint 22.3. A comparação final não encontrou diferenças em 115 destinos de instalação e 936 preferências; os documentos de teste foram preservados.

O ciclo completo de VM não foi repetido para a 1.0.3. Consulte o [relatório da VM](docs/VALIDACAO-VM.md), os [testes da janela de cópia](tests/test_copy_dialog.py), a [auditoria de cobertura](docs/AUDITORIA-FINAL.md) e o [GitHub Actions](https://github.com/82py/gruvbox-cinnamon-completo/actions).

### Código, créditos e licenças

`payload/` reúne os componentes portáteis; `scripts/`, as ferramentas de instalação e restauração; `tests/`, as verificações automatizadas. O instalador público compila o xwinwrap a partir do código incluído em `vendor/xwinwrap/`.

O código de integração usa **GPL-3.0-or-later**. Componentes de terceiros mantêm suas próprias licenças e atribuições. Consulte os [créditos](CREDITOS.md), [avisos de licença](LICENSES/), [registro de origem](docs/PROVENIENCIA.md) e [orientações para contribuir](CONTRIBUTING.md).

### Feito com vibe coding

Este projeto nasceu da vontade de deixar meu desktop com a minha cara e foi construído com **vibe coding**. Eu trouxe as ideias, escolhi a aparência e revisei os resultados; o OpenAI Codex ajudou a transformar essa conversa em ícones, scripts, integrações, documentação e um pacote compartilhável. O processo teve experimentação no Cinnamon, ajustes e testes de instalação e restauração. Os projetos que serviram de base e seus autores continuam reconhecidos nos créditos.

#### Aviso de responsabilidade

Este projeto é fornecido **“no estado em que se encontra” (“as is”)**, sem garantias de qualquer natureza, expressas ou implícitas. Na medida permitida pela legislação aplicável, o autor e os colaboradores não se responsabilizam por danos, perda de dados ou outras consequências decorrentes de sua instalação ou uso. **Instale e use por sua conta e risco.** Revise os scripts e mantenha cópias de segurança antes de fazer alterações. Consulte a [licença](LICENSE) para os termos aplicáveis. Componentes de terceiros mantêm suas próprias licenças.

#### Agradecimentos

Meu agradecimento às pessoas cujo código e desenhos tornaram isso possível:

- **Pavel Pertsev (morhetz)** — a [paleta Gruvbox original](https://github.com/morhetz/gruvbox).
- **SylEleuth** e colaboradores — [Gruvbox Plus Icon Pack](https://github.com/SylEleuth/gruvbox-plus-icon-pack).
- **Fausto-Korpsvart** e **Vince Liuice** — o [tema GTK](https://github.com/Fausto-Korpsvart/Gruvbox-GTK-Theme) usado como base visual.
- **Keefer Rourke** e **sainnhe** — Capitaine Cursors e sua [variante Gruvbox](https://github.com/sainnhe/capitaine-cursors).
- **Clement Lefebvre** e os **colaboradores do Linux Mint** — Cinnamon, Nemo, XApp, temas e desenhos originais do sistema.
- **klangman** e **hermes83** — [Magic Lamp](https://github.com/klangman/CinnamonMagicLamp) e a extensão que lhe serviu de base.
- **claudiux** e colaboradores do Cinnamon Spices — [Radio3](https://cinnamon-spices.linuxmint.com/applets/view/360).
- **akarzim** — seletor original de cores das pastas; **el-amine-404**, **claudiux** e **anaximeno** — ações do Nemo incluídas.
- **David Reveman / Novell**, **Shantanu Goel**, **Aaahh** e **mmhobi7** — o [código e as variantes do xwinwrap](https://github.com/mmhobi7/xwinwrap).

O pacote de ícones também se apoia no trabalho de **Sam Hewitt**, **Andrea Bonanni**, **Gustavo Costa**, **Vince Liuice**, **Alexey Varfolomeev**, **Papirus Development Team**, **Numix Team**, **Keefer Rourke** e **Adhe**. A variante MOD do tema foi localizada na coleção de **Twilight4**; isso não identifica a autoria de cada alteração histórica do CSS. Os créditos completos, os detalhes de origem e os avisos de licença estão em [CREDITOS.md](CREDITOS.md) e [LICENSES/](LICENSES/).
