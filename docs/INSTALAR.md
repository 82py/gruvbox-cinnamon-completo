# Installation / Instalação

[English](#english) · [Português](#português)

## English

The theme preserves the user's current list of disabled Nemo extensions, including when applying old profiles or restoring older points. It does not install antivirus software or change antivirus configuration.

### Tested environment

Linux Mint 22.3, Cinnamon/Nemo 6.6.x, X11 and a systemd user session. The source desktop uses Cinnamon 6.6.9 and Nemo/Muffin 6.6.3; the isolated GUI test VM used Cinnamon 6.6.4, Nemo 6.6.3 and Muffin 6.6.1. Other environments have not been validated. See [GUI validation](../VALIDACAO-GUI.json).

### Start the GUI

1. Download `Gruvbox-Cinnamon-GitHub-1.1.0.tar.gz` and its `.sha256` file from the release. Use the supplied TAR.GZ to preserve icon symlinks.
2. Extract the entire archive. Open the extracted folder in the file manager and run `iniciar-gui.sh`, choosing **Run** if prompted. Alternatively, open a terminal in that folder and run `bash iniciar-gui.sh`.
3. Run as your regular user, without sudo. Python 3, PyGObject and GTK 3 are needed to open the GUI; they are present in the tested Mint installation.
4. Choose English in the top right if desired. Opening or reviewing does not apply changes.
5. Choose **Install / customize**, select the components, and edit appearance, Rain and workspace choices. Current local values are the default. **Unchecked means leave unchanged.** Dependencies are selected together. The package-layout preset retains your folder/media references.
6. Use **Check requirements**. If needed, choose **Install dependencies…** and review the package list. Only this explicit action requests administrator authentication; system packages are not removed when uninstalling the theme.
7. Click **Review changes…**, inspect the destinations/components and confirm. A restore point is saved first.
8. Log out and back in to let Nemo and Cinnamon load all changes. Open Rain or background settings to select your own local media; nothing is downloaded automatically.

`instalar.sh` opens the same GUI in installation mode; `desinstalar.sh` opens removal mode. `verificar.sh` performs a read-only requirement check. Installed launchers open **Gruvbox Manager** from the application menu.

### Components and choices

The 15 selectable groups cover application icons, system indicators, themes, cursor, panel/menu, profile-photo refresh, four independent workspaces, Rain, folder colors, Nemo actions, terminal appearance, Relax shortcut, Flatpak font fixes, optional application autostart and other preferences. Radio3, its dependencies and Magic Lamp are excluded; an existing enabled radio instance is preserved.

Original desktop themes and Cinnamon/application internal files are not edited. Managed targets are per-user files and selected preferences. Four workspace folders can be chosen independently. Fresh setups reuse the current Desktop for area 1 and create empty folders for areas 2–4; existing workspace setups are read as defaults. Documents are never moved by installation. Imported legacy workspaces that share Rain scripts are treated as one dependent bundle.

Choose images/videos and volume/mute/autostart preferences in the GUI. Media files and the profile photo are not copied into the package. The photo extension uses the recipient's own account photo. Optional applications, accounts, passwords and saved networks are not bundled; absent programs do not receive invented application launchers.

### Backups, profiles and upgrades

Registry, dated points and retained installer: `~/.local/state/gruvbox-manager`. Backups and exported profiles contain local paths/preferences and should stay private. By default an offline installer copy is kept there, allowing the extracted folder to be removed; if retention is disabled, keep the source at the original location.

Existing GUI-managed components can be customized again; each operation creates a point. A registered installation made by the old terminal installer must first be restored using that original version's uninstaller. Do not delete its `~/.local/state/gruvbox-cinnamon` backups. Manual customization without an old journal is backed up normally.

Read [uninstall and restoration](DESINSTALAR.md) before changing an existing installation. Optional MIME associations remain reference-only. Personal server, VPN, task and synchronization services are outside this theme.

## Português

O tema preserva a lista atual de extensões desativadas do Nemo, inclusive ao aplicar perfis antigos ou restaurar pontos anteriores. Não instala antivírus nem altera sua configuração.

### Ambiente testado

Linux Mint 22.3, Cinnamon/Nemo 6.6.x, X11 e sessão systemd do usuário. O desktop de origem usa Cinnamon 6.6.9 e Nemo/Muffin 6.6.3; a VM isolada da GUI usou Cinnamon 6.6.4, Nemo 6.6.3 e Muffin 6.6.1. Outros ambientes não foram validados. Consulte a [validação da GUI](../VALIDACAO-GUI.json).

### Abrir a GUI

1. Baixe `Gruvbox-Cinnamon-GitHub-1.1.0.tar.gz` e seu arquivo `.sha256` na release. Use o TAR.GZ fornecido para preservar os links dos ícones.
2. Extraia o arquivo inteiro. Na pasta extraída, execute `iniciar-gui.sh` pelo gerenciador de arquivos, escolhendo **Executar** se solicitado. Como alternativa, abra o terminal nessa pasta e execute `bash iniciar-gui.sh`.
3. Execute como usuário comum, sem sudo. Python 3, PyGObject e GTK 3 são necessários para abrir a GUI e já estão presentes no Mint testado.
4. O idioma pode ser alterado no canto superior direito. Abrir ou revisar não aplica mudanças.
5. Escolha **Instalar / personalizar**, marque os componentes e ajuste aparência, Rain e espaços. Os valores locais atuais são o padrão. **Desmarcado significa manter como está.** Dependências são selecionadas juntas. O preset visual do pacote conserva suas referências de pastas/mídias.
6. Use **Verificar requisitos**. Se necessário, escolha **Instalar dependências…** e revise a lista. Só essa ação explícita pede autenticação administrativa; os pacotes do sistema não são removidos ao desinstalar o tema.
7. Clique em **Revisar alterações…**, confira os destinos/componentes e confirme. Um ponto de restauração é criado antes.
8. Encerre a sessão e entre novamente para Nemo e Cinnamon carregarem tudo. Abra o Rain ou as configurações de fundos para escolher mídias locais; nada é baixado automaticamente.

`instalar.sh` abre a mesma GUI no modo de instalação; `desinstalar.sh`, no modo de remoção. `verificar.sh` confere requisitos sem aplicar mudanças. O atalho instalado abre **Gerenciador Gruvbox** pelo menu de aplicativos.

### Componentes e escolhas

Os 15 grupos selecionáveis abrangem ícones de aplicativos, indicadores do sistema, temas, cursor, painel/menu, atualização da foto, quatro espaços independentes, Rain, cores de pastas, ações do Nemo, visual do terminal, atalho Relax, fontes Flatpak, inicialização opcional e outras preferências. Radio3, suas dependências e Magic Lamp foram excluídos; uma instância de rádio já habilitada é preservada.

Temas originais e arquivos internos do Cinnamon/aplicativos não são editados. Os destinos gerenciados são arquivos do usuário e preferências selecionadas. As quatro pastas dos espaços podem ser escolhidas separadamente. Em uma instalação nova, a área 1 usa o Desktop atual e as áreas 2–4 recebem pastas vazias; configurações existentes são lidas como padrão. A instalação não move documentos. Espaços antigos importados que compartilham scripts com o Rain são tratados como um conjunto dependente.

Escolha imagens/vídeos, volume/mudo e inicialização na GUI. Mídias e foto pessoal não são copiadas para o pacote. A extensão usa a foto da própria conta do destinatário. Aplicativos opcionais, contas, senhas e redes salvas não acompanham o tema; programas ausentes não recebem atalhos de aplicativos inventados.

### Backups, perfis e atualizações

Registro, pontos datados e instalador retido ficam em `~/.local/state/gruvbox-manager`. Backups e perfis exportados contêm caminhos/preferências locais e devem permanecer privados. Por padrão, uma cópia offline do instalador permite remover a pasta extraída; se desativar a retenção, mantenha a origem no local original.

Componentes já gerenciados pela GUI podem ser personalizados novamente; cada operação cria um ponto. Uma instalação registrada pelo antigo instalador de terminal precisa ser restaurada pelo desinstalador daquela versão antes. Não apague seus backups em `~/.local/state/gruvbox-cinnamon`. Personalizações manuais sem esse registro são copiadas normalmente para backup.

Leia o [guia de remoção e restauração](DESINSTALAR.md) antes de alterar uma instalação existente. Associações MIME opcionais são apenas referência. Serviços pessoais de servidor, VPN, tarefas e sincronização estão fora deste tema.
