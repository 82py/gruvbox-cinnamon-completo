# Installation / Instalação

[English](#english) · [Português](#português)

## English

### Platform

The source setup is Linux Mint 22.3 Zena with Cinnamon 6.6.9, Nemo/Muffin 6.6.3, and X11. The installer accepts Cinnamon/Nemo 6.6.x on X11; other versions need validation. The supported installer checks and runtime integrations are specific to the tested Cinnamon/X11 environment. Version 1.0.2 was installed and uninstalled in a Mint 22.3 VM with Cinnamon 6.6.4, Nemo 6.6.3, and Muffin 6.6.1, including reboots and comparison of original files/preferences. The source machine was not changed by that VM test. See [VM validation](VALIDACAO-VM.md) for the scope.

### Steps

1. Extract the complete TAR.GZ with its directory structure intact. Prefer TAR.GZ to preserve icon symlinks.
2. In the extracted folder, run `bash verificar.sh`. This only checks requirements.
3. If dependencies are missing, review `scripts/instalar-dependencias.sh` and run `bash scripts/instalar-dependencias.sh`. This separate command uses sudo to install public Mint packages; the theme itself is installed without sudo.
4. Run `bash instalar.sh` as your regular user. It checks requirements, saves backups, and applies only the files and keys recorded in the inventory.
5. Log out and back in. This lets Nemo read the new Desktop path and starts the Rain tray and workspace service.
6. In the menu, open **Fundos por espaço** to choose images and **Rain** to choose a local video. No media is downloaded automatically.

Paths are resolved from `$HOME` and the current user. Desktop launchers receive correct absolute paths during installation because `.desktop` files do not expand `$HOME` or `$USER`.

### What changes

Themes in `$HOME/.themes`, icons in `$HOME/.local/share/icons`, cursors in `$HOME/.icons`, executables in `$HOME/.local/bin`, extensions/applets in `$HOME/.local/share/cinnamon`, selected preferences, Nemo actions, and user shortcuts. Preferences include panel layout, favorites, menus, notifications, gestures, appearance, fonts, and Rain shortcuts. Passwords, credentials, saved networks, accounts, run history, and location data are excluded.

Four workspaces are configured. Workspace 1 reuses the existing Desktop folder; workspaces 2–4 get empty folders under `$HOME/Espaços de trabalho Gruvbox`. Separation uses a single `.atual` symlink. No document is moved or deleted.

Your profile photo remains yours. The photo-refresh extension is included, but no photo or photo cache is distributed.

Radio3 keeps its visual preferences and the public JB FM preset; personal history, searches, and schedules are excluded. Applications, PWAs, games, and accounts are the user's responsibility. Launchers for absent programs are not invented, and favorites for programs not installed may not appear.

### Backups and upgrades

The journal and backups are kept in `$HOME/.local/state/gruvbox-cinnamon`. Do not delete that directory before uninstalling. If installation fails, the installer attempts to restore already recorded files and values automatically. A second installation over an existing journal is refused: restore the previous installation first.

The previous wallpaper is recorded only on the destination computer for restoration; the image is not copied into this package. Read the [uninstall and restoration guide](DESINSTALAR.md).

### Additional integrations from 1.0.1

Relax asks for a local video and opens Celluloid fullscreen, with mpv as a fallback. Ctrl+F12 uses mpv. The terminal's exported appearance profile is stored separately; commands started inside it receive their normal XDG paths. Personal shell commands and window positions are not transferred.

KClock and Materialgram font fixes are user preferences, not application edits. The installer merges FONTCONFIG_FILE with existing overrides without removing them. Chromium's menu category is also merged. Insync and Bitwarden receive autostart entries only if already installed; the package does not install them or copy accounts.

`optional/mimeapps.list` is a reference only and does not replace default applications automatically. Personal server, task, VPN, and synchronization services are not part of the theme.

### Fixes from 1.0.2 and 1.0.3

The workspace service checks versions on its first iteration, preventing a false update warning during boot. Rain waits for configured video output and falls back to X11 when GPU output is unavailable. Rain audio and the fullscreen mpv shortcut use Mint's PulseAudio compatibility interface with their own names, preventing Radio3 from capturing them. No applet was modified.

The installer snapshots all original preferences before making changes. Restoration disables managed components before removing their files and stops the package's Rain processes. System dependencies are installed before personalization and are not removed automatically during uninstallation.

In 1.0.3, a selection opened through Nemo's copy dialog performs only one operation, closes after completion, and requests a notification. Repeated clicks do not repeat successful copies, including after a partial failure.

---

## Português

### Plataforma

A configuração de origem é Linux Mint 22.3 Zena com Cinnamon 6.6.9, Nemo/Muffin 6.6.3 e X11. O instalador aceita Cinnamon/Nemo 6.6.x em X11; outras versões precisam de validação. As verificações do instalador e as integrações foram validadas nesse ambiente Cinnamon/X11. A versão 1.0.2 foi instalada e desinstalada em uma VM Mint 22.3 com Cinnamon 6.6.4, Nemo 6.6.3 e Muffin 6.6.1, incluindo reinicializações e comparação dos arquivos e preferências originais. O Cinnamon da máquina de origem permaneceu intacto. Veja VALIDACAO-VM.md para o alcance dos testes.

### Passos

1. Extraia o TAR.GZ completo mantendo sua estrutura. Prefira TAR.GZ: ele conserva os links internos do tema de ícones.
2. Abra um terminal na pasta extraída e execute `bash verificar.sh`. Esse comando apenas verifica requisitos.
3. Se faltarem dependências, leia `scripts/instalar-dependencias.sh` e execute `bash scripts/instalar-dependencias.sh`. Esse comando separado usa sudo para instalar pacotes públicos do Mint; o tema é instalado sem sudo.
4. Execute `bash instalar.sh` como usuário comum. O instalador verifica requisitos, guarda cópias de segurança e aplica somente os arquivos e chaves registrados no inventário.
5. Encerre a sessão e entre novamente. Isso permite que o Nemo leia o caminho novo da Área de Trabalho e inicia o Rain na bandeja e o serviço dos espaços.
6. No Iniciar, abra “Fundos por espaço” para selecionar imagens e “Rain” para selecionar um vídeo local. Nenhuma mídia é baixada automaticamente.

Os caminhos são resolvidos a partir de `$HOME` e do usuário atual. Os atalhos recebem caminhos absolutos corretos na instalação, porque arquivos `.desktop` não expandem `$HOME` ou `$USER`.

### O que muda

Temas em `$HOME/.themes`, ícones em `$HOME/.local/share/icons`, cursor em `$HOME/.icons`, executáveis em `$HOME/.local/bin`, extensões/applet em `$HOME/.local/share/cinnamon`, preferências selecionadas, ações do Nemo e atalhos do usuário. As configurações capturadas incluem painel, favoritos, menus, notificações, gestos, aparência, fontes e atalhos para Rain. Não inclui senhas, credenciais, redes salvas, contas, histórico de execução ou localização geográfica.

O ambiente fica com quatro espaços. O espaço 1 usa a pasta que já era a Área de Trabalho; os espaços 2–4 recebem pastas vazias em `$HOME/Espaços de trabalho Gruvbox`. A separação usa apenas um link `.atual`. Nenhum documento é movido ou apagado.

A foto de perfil do destinatário permanece sendo a dele; a extensão de atualização de foto acompanha o código, mas nenhuma foto ou cache de foto é distribuído.

A Radio3 conserva suas preferências visuais; o preset público JB FM é preservado; históricos, pesquisas e agendamentos pessoais não são distribuídos. A instalação de programas, PWAs, jogos e suas contas é responsabilidade de quem os usa. Atalhos associados a programas ausentes não são inventados, e favoritos de programas não instalados podem não aparecer.

### Cópia de segurança

O registro e as cópias ficam em `$HOME/.local/state/gruvbox-cinnamon`. Não apague essa pasta antes de desinstalar. Se houver erro durante a instalação, o instalador tenta restaurar automaticamente os arquivos e valores já registrados. Não é permitida uma segunda instalação sobre uma instalação registrada: restaure a anterior primeiro.

A instalação guarda o fundo anterior apenas no computador de destino, para permitir a restauração; essa imagem não é copiada para o pacote.

### Complementos da revisão 1.0.1

O atalho Relax pede um vídeo local e abre Celluloid em tela cheia (com alternativa mpv). Ctrl+F12 continua usando mpv. O terminal mantém o perfil visual exportado, em dados separados; os programas iniciados nele recebem seus caminhos XDG habituais. Comandos pessoais de shell e posições de janelas não são transferidos.

As correções de fontes de KClock e Materialgram são preferências do usuário, não alterações nos aplicativos. O instalador mescla FONTCONFIG_FILE com as outras permissões/variáveis já existentes, sem removê-las. A organização do menu Chromium também é mesclada. Insync e Bitwarden só recebem sua entrada de inicialização automática se já estiverem instalados; o pacote não instala esses programas nem copia suas contas.

As associações de arquivos ficam em `optional/mimeapps.list` como referência; não substituem automaticamente os aplicativos padrão do destinatário. Os programas e serviços pessoais de servidores, tarefas, VPN e sincronização não fazem parte do tema.

### Ajustes da revisão 1.0.2

O serviço dos espaços verifica suas versões já na primeira execução, sem o aviso falso de atualização durante o boot. O Rain aguarda a saída de vídeo ficar pronta e usa X11 como alternativa quando a aceleração gráfica não está disponível. Seu áudio e o atalho de vídeo mpv usam a interface PulseAudio compatível do Mint, com nomes próprios, para não serem confundidos com a Radio3. Nenhum applet foi alterado.

O instalador captura todas as preferências originais antes da primeira mudança. A restauração desativa os componentes gerenciados antes de remover seus arquivos e encerra os processos próprios do Rain. As dependências do sistema são instaladas antes da personalização e não são removidas automaticamente na desinstalação.

Na 1.0.3, a seleção aberta pelo menu de cópia do Nemo executa uma única operação, fecha ao concluir e solicita uma notificação. Cliques repetidos não repetem as cópias concluídas, inclusive em falhas parciais.
