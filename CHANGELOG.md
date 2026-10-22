# Changelog / Alterações

[English](#english) · [Português](#português)

## English

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
