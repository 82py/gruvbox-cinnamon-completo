# Uninstall and restore / Desinstalar e restaurar

[English](#english) · [Português](#português)

## English

### Remove selected components

Open **Gruvbox Manager** from the menu or run `bash iniciar-gui.sh` from the extracted folder. Choose **Uninstall components**, check what you want to remove, click **Review changes…** and confirm. `bash desinstalar.sh` opens this same removal view. Only components installed by this manager can be removed; dependencies that remain in use prevent incompatible removals.

Removal restores each selected component to its state **before this manager first changed it**. That state can already be customized: it is not a Mint factory reset. Unchecked components stay installed. Previously unset preference values become unset again; no entire unrelated preference tree is cleared.

A new dated restore point saves the current affected files/preferences before removing them, including changes made since installation. The package's selected extensions and Rain processes are stopped before their files are restored. Removing Rain while retaining portable workspaces switches video modes to static and retains media references. Legacy workspaces sharing Rain scripts are kept together.

**Workspace folders, documents, local videos, background images and your profile photo are not deleted.** Files created after installation remain. When workspace management is removed, the previous Desktop path is restored. Log out and back in after completion. System packages, third-party applications and accounts are not uninstalled.

### Restore a point or recover an interruption

Choose **Restore a previous point**, select a dated operation and check components to return to their state immediately before that operation. The current state is saved in another point first. This can also undo a previous removal.

If a process or computer stopped during an operation, use **Profiles and safety → Recover interrupted operation…** before starting another change. Ordinary failures attempt automatic rollback; keep the backup history until the result is checked.

The manager launcher, registry, offline installer and restore history remain in `~/.local/state/gruvbox-manager` after component removal, allowing later recovery. Do not delete that directory while you need its backups. Exported profiles and restore points contain private local information; do not publish them.

### Older terminal-installer releases

If the GUI detects an existing `~/.local/state/gruvbox-cinnamon/install.json`, use the **original release's** `desinstalar.sh` or `~/.local/bin/gruvbox-desinstalar` to restore it first. Keep that release's backups until restoration is complete. The new GUI does not take ownership of the old journal.

## Português

### Remover componentes selecionados

Abra **Gerenciador Gruvbox** no menu ou execute `bash iniciar-gui.sh` na pasta extraída. Escolha **Desinstalar componentes**, marque o que deseja remover, clique em **Revisar alterações…** e confirme. `bash desinstalar.sh` abre essa mesma tela de remoção. Só componentes instalados pelo gerenciador podem ser removidos; dependências ainda em uso impedem remoções incompatíveis.

A remoção devolve cada componente ao estado **anterior à primeira alteração por este gerenciador**. Esse estado pode já ser personalizado: não é um retorno ao padrão de fábrica do Mint. Componentes desmarcados continuam instalados. Preferências antes não definidas voltam a não estar definidas; nenhuma árvore inteira de preferências sem relação é apagada.

Um ponto datado guarda os arquivos/preferências atuais antes de remover, inclusive alterações feitas depois da instalação. As extensões selecionadas e os processos próprios do Rain são encerrados antes de restaurar seus arquivos. Remover Rain mantendo espaços portáveis troca os modos de vídeo por estáticos e conserva as referências de mídia. Espaços antigos que compartilham scripts com o Rain são mantidos juntos.

**Pastas dos espaços, documentos, vídeos locais, imagens de fundo e foto pessoal não são apagados.** Arquivos criados depois da instalação permanecem. Ao remover o gerenciamento dos espaços, o caminho anterior do Desktop é restaurado. Encerre a sessão e entre novamente ao terminar. Pacotes do sistema, aplicativos de terceiros e contas não são desinstalados.

### Restaurar um ponto ou recuperar uma interrupção

Escolha **Restaurar ponto anterior**, selecione uma operação datada e marque os componentes para voltar ao estado imediatamente anterior àquela operação. O estado atual é guardado em outro ponto antes. Isso também permite desfazer uma remoção anterior.

Se o processo ou computador parou durante uma operação, use **Perfis e segurança → Recuperar operação interrompida…** antes de iniciar outra alteração. Falhas comuns tentam reversão automática; mantenha o histórico até conferir o resultado.

O atalho do gerenciador, registro, instalador offline e histórico ficam em `~/.local/state/gruvbox-manager` mesmo depois de remover componentes, permitindo recuperar depois. Não apague essa pasta enquanto precisar dos backups. Perfis exportados e pontos contêm informações locais privadas; não os publique.

### Versões antigas do instalador de terminal

Se a GUI detectar `~/.local/state/gruvbox-cinnamon/install.json`, restaure primeiro usando `desinstalar.sh` **da versão original** ou `~/.local/bin/gruvbox-desinstalar`. Guarde os backups daquela versão até concluir a restauração. A GUI nova não assume o registro antigo.
