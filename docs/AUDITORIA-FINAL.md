# Personalization coverage audit / Auditoria da personalização

[English](#english) · [Português](#português)

## English

**Historical audit of 1.0.2, dated 2026-10-21.** Version 1.0.3 updates the copy tool and its tests/documentation; see [copy validation](VALIDACAO-COPIA.json). The audit read Cinnamon's loaded components and compared active files with both distribution trees. It did not install the package on the source session; full installation was exercised in a separate VM.

| Active component | Included coverage |
| --- | --- |
| Gruvbox Plus and colorful system theme | Files and links compared; no missing or different artwork. |
| Desktop/GTK/window themes and cursor | Local copies included; both local Mint CSS copies synchronized. |
| 15 panel applets | 14 supplied by Cinnamon; full Radio3 applet and instance preferences included. |
| Five running extensions | Magic Lamp and four integration extensions; personal UUIDs made generic. |
| Application menu | 180 entries inventoried through CMenu without private commands; Chromium category preserved by merging. |
| Rain | Window, tray, slider, start/stop, auxiliary volume, session launcher, wrapper, and video integration. |
| Four workspaces | Service, independent folders, per-workspace backgrounds, and copying between them. |
| Folder color picker | Both shell scripts, engine, menu, and A/B variants; original themes preserved. |
| Relax | Local video choice and Celluloid fullscreen, with mpv fallback. |
| Default terminal | Visual profile exported separately without personal commands; normal environment returned to child commands. |
| Flatpak fonts | KClock and Materialgram Fontconfig, merging existing overrides. |
| Preferences | 936 explicit appearance, panel, menu, window, keyboard, shortcut, gesture, Nemo, and theme values. |
| Autostart | Rain/workspaces; Insync and Bitwarden conditional on existing programs. Two previously disabled entries stay disabled. |
| Nemo actions | Six actions and helpers; Timo remains an external dependency. No personal Nemo scripts, desklets, or search providers were active. |

### Additions from the audit

Relax, the terminal appearance profile, two Fontconfig files, Chromium's menu category, previously implicit defaults, local Mint CSS, and Radio3/auxiliary volume dependencies. The public JB FM preset was retained; history and searches remain excluded.

### Deliberate exclusions

Videos, wallpaper images, profile photos, workspace documents, accounts, credentials, logs, location, and history. Workspaces initially use a solid background until the recipient selects media. Workspace 1 reuses the existing Desktop; others start empty.

Third-party application binaries, profiles/accounts, and personal server, task, VPN, or synchronization services are not part of a Cinnamon theme. Their icons are included; menu inventory identifies applications as external dependencies. Personal server integrations were not copied. MIME associations are optional reference data only.

Old dated workspace installers/restorers tied to the source machine are replaced by the portable installer, uninstaller, and controls. Old media copies and document backups are not distributed to recreate them.

### Verification and limits

Run `python3 scripts/auditar-desktop.py` while the source machine retains the audited setup to repeat the read-only comparison. Intended adaptations are listed in [coverage data](AUDITORIA-COBERTURA.json).

Install/restore and selector tests use isolated HOME/preferences. Both original final archives were extracted to test all 25 colors and GTK icon lookup/rendering. The real terminal also loaded its exported profile and executed a test command in a private bus without a visible window, preserving original data. Version 1.0.2 additionally passed installation/removal in a real Cinnamon session inside Mint 22.3: no differences across 115 destinations, 936 preferences, or the three internal-file trees before/after reboot. See [VM validation](VALIDACAO-VM.md).

---

## Português

Conferência histórica da revisão 1.0.2. A 1.0.3 atualiza somente o utilitário de cópia e seus testes/documentação; veja VALIDACAO-COPIA.json. A conferência leu o estado do Cinnamon e comparou os arquivos ativos com as duas árvores de distribuição. Nada foi aplicado na sessão real da máquina de origem; a instalação completa foi exercitada em uma VM separada.

| Componente ativo | Cobertura |
| --- | --- |
| Gruvbox Plus e Sistema Colorido | Arquivos e links comparados; nenhuma arte ausente ou diferente. |
| Tema visual, GTK, janelas e cursor | Cópias locais incluídas; os dois CSS locais Mint foram sincronizados. |
| 15 applets do painel | 14 fornecidos pelo Cinnamon; Radio3 completa no pacote. Preferências de instância incluídas. |
| Cinco extensões em execução | Magic Lamp e quatro extensões da personalização incluídas; UUIDs pessoais tornados genéricos. |
| Menu Iniciar | 180 entradas inventariadas por CMenu, sem copiar comandos privados; categoria Chromium preservada por mesclagem. |
| Rain | GUI, bandeja, controle deslizante, iniciar/parar, volume auxiliar, sessão, wrapper e código de vídeo incluídos. |
| Quatro espaços | Serviço, pastas independentes, fundos por espaço e cópia entre áreas incluídos. |
| Seletor de pastas | Dois SH, motor, menu e variantes A/B incluídos; temas originais preservados. |
| Relax | Atalho incluído; escolhe vídeo local e mantém reprodução em tela cheia via Celluloid, com alternativa mpv. |
| Terminal padrão | Perfil visual ativo exportado para configuração separada, sem comandos pessoais; ambiente normal devolvido aos processos filhos. |
| Fontes em aplicativos Flatpak | Fontconfig de KClock e Materialgram incluídos, com mesclagem dos overrides existentes. |
| Preferências | 936 valores explícitos de aparência, painel, menus, janelas, teclado, atalhos, gestos, Nemo e temas. |
| Inicialização | Rain e espaços incluídos; Insync/Bitwarden condicionados à presença dos programas. As duas entradas já desativadas permanecem desativadas. |
| Ações Nemo | Seis ações e seus auxiliares incluídos; Timo continua sendo dependência externa. Sem scripts de Nemo, desklets ou provedores de pesquisa pessoais ativos. |

### O que a conferência acrescentou

Relax, o perfil visual do terminal, duas configurações Fontconfig, a categoria Chromium, valores padrão antes implícitos, os CSS locais Mint e dependências da Radio3/controle auxiliar de volume. O preset público JB FM foi mantido; o histórico e as pesquisas continuam excluídos.

### Exclusões deliberadas

Não são um esquecimento: vídeos, imagens de fundo, foto de perfil, documentos dos espaços, contas, credenciais, registros, localização geográfica e histórico. Os espaços começam com fundo sólido até a escolha de mídia pelo destinatário. O primeiro espaço reutiliza sua Área de Trabalho existente; os demais são criados vazios.

Binários de aplicativos de terceiros, seus perfis/contas e serviços pessoais de servidores, tarefas, VPN ou sincronização não são um tema Cinnamon. Seus ícones são incluídos, e o menu os identifica como dependências externas. Não foram copiadas integrações com servidores pessoais. As associações MIME estão apenas como referência opcional.

Os instaladores/restauradores antigos de áreas, datados e vinculados ao estado anterior da máquina de origem, são substituídos pelo instalador, desinstalador e controles portáteis do novo pacote. Não se distribuem cópias antigas de vídeos nem backups de documentos para reproduzi-los.

### Verificação e limites

A comparação de cobertura é reproduzível com `python3 scripts/auditar-desktop.py` enquanto a máquina de origem mantiver esta configuração. As adaptações intencionais são enumeradas em `AUDITORIA-COBERTURA.json`.

A instalação/restauração e o seletor são testados em HOME e preferências isolados. Os dois arquivos finais são extraídos para testar as 25 cores e a resolução/renderização GTK dos ícones. O terminal real também foi iniciado sem janela visível e em barramento privado: carregou o perfil exportado, executou o comando de teste e preservou os dados originais. A revisão 1.0.2 também foi instalada e desinstalada em uma segunda sessão Cinnamon real, dentro de uma VM Mint 22.3. A restauração foi conferida antes e depois de reiniciar: nenhuma diferença nos 115 destinos, nas 936 preferências e nos três conjuntos de arquivos internos comparados. Consulte VALIDACAO-VM.md.
