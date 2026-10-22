# Changelog / Alterações

[English](#english) · [Português](#português)

## English

The theme preserves the user's current list of disabled Nemo extensions, including when applying old profiles or restoring older points. It does not install antivirus software or change antivirus configuration.

### System-icon lifecycle correction — 2026-10-22

- System-color extension v3 releases removed actor subtrees and their signal handlers, and excludes the client-window group. The previous watcher could retain closed-window surfaces.
- MintUpdate-color extension v2 also releases removed indicator and texture subtrees. Its previous watcher retained replaced texture actors. An isolated regression repeats 25 texture replacements while checking bounded tracking, disconnected signals and preserved icon color.
- Adds isolated JavaScript lifecycle regressions for removal, reattachment, existing style classes, window-group exclusion and repeated disable. These fixes address the identified retention defects; they do not establish that every reported desktop slowdown is resolved.

### 1.1.0 — 2026-10-22

- Magic Lamp removed after an observed animation exception and a source-less full-screen clone were found in the source desktop. Native animations remain available. / Magic Lamp removido após erro de animação e clone sem origem sobre a tela inteira. Animações nativas preservadas.

- Adds the GTK manager for selective installation, customization, uninstall and restore across 15 components, with English and Portuguese UI and instructions.
- Adds profiles, dependency checks, confirmation review, dated restore points, rollback, interrupted-operation recovery and a retained offline installer.
- Keeps current local settings, workspace folders and media references as defaults. Excludes personal media/photo, Radio3 and Magic Lamp from this release; an existing radio instance is preserved.
- GUI: 51 Python and 14 actor-lifecycle checks passed. The public installer passed an isolated Mint VM install, feature, uninstall and reboot cycle, preserving original files/preferences and workspace documents.


### 1.0.3 — 2026-10-21

- Bilingual documentation, English first, with a visual presentation, actual icon galleries, all 25 folder colors, and independent-workspace/Rain explanations. Named acknowledgments and an “as is” disclaimer follow the vibe-coding note. Installed code and preferences are unchanged by the documentation refresh.
- A selection opened through Nemo's “Copy to another workspace…” dialog performs one operation, disables destinations while copying, closes on success, and requests a notification.
- Completed selections are consumed. Extra clicks, including after partial failure, cannot repeat successful copies. Errors are shown before closing.
- Standalone drag-and-drop mode still accepts deliberate new operations.
- Four GTK regressions cover repeated clicks, partial failures, drag mode, and a missing notification command using temporary data.
- The complete 1.0.2 VM install/uninstall validation remains historical evidence; the full VM cycle was not repeated for 1.0.3.

### 1.0.2 — 2026-10-21

- Actual Mint 22.3 Cinnamon X11 VM installation/removal with reboots and comparison of 115 destinations, 936 preferences, and internal files.
- Workspace version checks on the first boot iteration.
- Embedded GPU/X11 video outputs and video-readiness checks before selecting a Rain mode.
- Separate Rain/fullscreen-video audio identities via PulseAudio compatibility, avoiding Radio3 capture without applet edits.
- Snapshot all preferences before changing anything; disable components before restoring files.
- Stop Rain's own window/tray during uninstallation.
- Regressions for early boot and cross-schema synchronization, plus VM evidence/screenshots.

### 1.0.1 — 2026-10-21

- Audited loaded components, menu entries, and actual preferences.
- Included Relax, isolated terminal appearance, KClock/Materialgram Fontconfig, and Chromium menu organization.
- Exported 936 explicit preferences; synchronized local Mint theme copies.
- Kept the public Radio3 preset and completed applet/auxiliary-volume dependencies.
- Merged application preferences and conditional Insync/Bitwarden autostart.

### 1.0.0 — 2026-10-21

- Captured Pir (82py)'s active personalization, approved icons, and colorful system variant.
- Portable paths, Rain, and independent workspaces without media or personal data.
- Installer/restorer with backups and per-key preference records.
- GitHub structure, credits, license handling, and Ubuntu assessment.

#### Folder selector addition

- Included both home-folder shell scripts, menu entry, and akarzim attribution.
- The helper uses its own A/B variants, preserving original themes.
- Tested from the TAR.GZ archives: all colors, GTK lookup/rendering, restoration, simulated failure, conflicts, and uninstallation.

---

## Português

O tema preserva a lista atual de extensões desativadas do Nemo, inclusive ao aplicar perfis antigos ou restaurar pontos anteriores. Não instala antivírus nem altera sua configuração.

### Correção do ciclo de vida dos ícones de sistema — 2026-10-22

- A extensão de cores de sistema v3 libera subárvores de atores removidas e seus sinais, e exclui o grupo de janelas de aplicativos. O observador anterior podia reter superfícies de janelas fechadas.
- A extensão de cores do MintUpdate v2 também libera subárvores de indicadores e texturas removidas. O observador anterior retinha atores de texturas substituídas. Uma regressão isolada repete 25 trocas, conferindo contagem limitada, sinais desconectados e cor preservada.
- Inclui regressões JavaScript isoladas para remoção, reconexão, classes de estilo preexistentes, exclusão das janelas e desativação repetida. Corrige as retenções identificadas; não comprova a resolução de todas as lentidões relatadas.

### 1.1.0 — 2026-10-22

- Inclui o gerenciador GTK para instalação, personalização, remoção e restauração seletivas de 15 componentes, com interface e instruções em inglês e português.
- Inclui perfis, conferência de dependências, revisão antes de aplicar, pontos datados, reversão de falhas, recuperação de operações interrompidas e cópia offline do instalador.
- Mantém valores atuais, pastas e referências de mídia como padrão. Não distribui mídia/foto pessoal nem Radio3 ou Magic Lamp; preserva uma instância de rádio existente.
- GUI: 51 testes Python e 14 testes de ciclo de vida dos elementos aprovados. O instalador público passou num ciclo de instalação, recursos, remoção e reinicializações em VM Mint isolada, preservando arquivos/preferências anteriores e documentos.


### 1.0.3 — 21/10/2026

- Documentação dos compactados atualizada: README bilíngue (inglês primeiro), apresentação visual com ícones reais, catálogo das 25 cores de pastas e agradecimentos nominais e aviso de responsabilidade após a nota de vibe coding. Código instalado e preferências permanecem iguais.

- A janela “Copiar para outra área…” aberta pelo menu do Nemo agora executa uma única operação por seleção. Os destinos ficam bloqueados durante a cópia; no sucesso, a janela fecha e solicita uma notificação.
- Seleções concluídas são consumidas. Cliques adicionais, inclusive após uma falha parcial, não criam cópias duplicadas dos itens que já foram copiados. Erros continuam sendo apresentados antes do fechamento.
- O modo independente de arrastar arquivos continua aceitando novas operações deliberadas.
- Quatro testes GTK de regressão cobrem cliques repetidos, falha parcial, modo de arraste e ausência do serviço de notificações. Nenhum arquivo pessoal é usado nos testes.
- Mantida a validação completa de instalação e desinstalação em VM da 1.0.2 como evidência histórica; esse ciclo completo não foi repetido para a 1.0.3.

### 1.0.2 — 21/10/2026

- Instalação e desinstalação reais em VM Mint 22.3 Cinnamon X11, com reinicializações e comparação de 115 destinos, 936 preferências e arquivos internos.
- Verificação das versões dos espaços já no primeiro ciclo de boot.
- Saídas incorporadas GPU/X11 e confirmação de vídeo pronto antes da seleção do modo Rain.
- Áudio próprio Rain/vídeo via compatibilidade PulseAudio, evitando a captura do player pela Radio3 sem modificar o applet.
- Captura de todas as preferências antes das alterações; desligamento dos componentes antes da restauração dos arquivos.
- Encerramento da janela e da bandeja próprias do Rain na desinstalação.
- Regressões para boot antecipado e sincronização entre schemas, evidências e capturas da VM.

### 1.0.1 — 2026-10-21

- Auditoria dos componentes realmente carregados, do menu e das preferências atuais.
- Incluídos Relax, o perfil visual isolado do terminal, Fontconfig de KClock/Materialgram e a organização da categoria Chromium.
- Exportadas 936 preferências explícitas; sincronizadas as cópias locais dos temas Mint.
- Preservado o preset público da Radio3 e completadas suas dependências e as do controle auxiliar de volume do Rain.
- Mesclagem de preferências de aplicativos e inicialização condicional de Insync/Bitwarden.

### 1.0.0 — 2026-10-21

- Captura da personalização ativa de Pir (82py), com cópia dos ícones aprovados e variante de sistema colorida.
- Portabilidade dos caminhos, Rain e espaços independentes sem mídias ou dados pessoais.
- Instalador e restaurador com cópias de segurança e registro individual das preferências.
- Estrutura para GitHub, créditos, separação de componentes pendentes de licença e análise do Ubuntu.

#### Complemento do seletor de pastas

- Incluídos os dois SH da pasta pessoal, menu no Iniciar e créditos a akarzim.
- O auxiliar usa variantes A/B próprias e mantém os temas originais intactos.
- Compatibilidade verificada a partir dos próprios TAR.GZ: todas as cores, resolução/renderização GTK, restauração, falha simulada, conflitos e desinstalação.
