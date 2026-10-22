# Folder colors / Cores das pastas

[English](#english) · [Português](#português)

## English

![All 25 folder colors available in the Gruvbox selector](imagens/folder-colors.png)

These are the actual SVGs included in the package. The English names match the selector and the `--color` options; `plasma` is the original upstream default. [Open the full-size chart](imagens/folder-colors.png).

After installing, open **Escolher cor das pastas Gruvbox** in the application menu or run `bash "$HOME/escolher-cor-pastas.sh"`. Both shell scripts are also included at the package root. Before installation, listing colors and help work, but changing colors is refused to prevent accidental changes on the packaging machine.

There are 25 colors, option `0` for the upstream plasma default, and option `r` to restore the appearance from before using the selector. The equivalent command is `bash "$HOME/folders-color-chooser.sh" -c blue`; `-C` selects plasma and `--restore` restores the previous appearance.

The original chooser changed links inside Gruvbox Plus. This integration builds two separate A/B variants and switches between them to refresh the icon cache. Gruvbox-Plus-Dark and Gruvbox-Sistema-Colorido remain intact. Other icons are inherited from the approved system theme; symbolic `xsi-*` system actions retain their specific colors. Changing folder colors does not modify categories, applications, audio, network, Bluetooth, cursors, desktop themes, wallpapers, or workspace files.

The change is refused if another icon theme is selected, the package is not installed, the managed variants have been replaced, the source resolves outside its theme, or another change is in progress. A complete variant is prepared before applying it; both icon preferences are restored if application fails. No sudo or Nemo/Cinnamon restart is required.

The variants are tracked by the installer and uninstaller. Uninstalling restores previous preferences and preserves modified copies in the recovery directory described in the [restoration guide](DESINSTALAR.md). Option `r` is the quick way to undo just the folder-color choice.

---

## Português

![As 25 cores de pastas disponíveis no seletor Gruvbox](imagens/folder-colors.png)

A imagem acima mostra os SVGs reais distribuídos no pacote. Os nomes em inglês correspondem às opções do seletor e do comando `--color`; `plasma` é o padrão original. [Abrir a imagem em tamanho completo](imagens/folder-colors.png).

Depois de instalar o pacote, abra “Escolher cor das pastas Gruvbox” no Iniciar ou execute `bash "$HOME/escolher-cor-pastas.sh"`. Os dois arquivos SH também acompanham a raiz do pacote. Antes da instalação, a listagem e a ajuda funcionam, mas uma troca é recusada: isso impede alterações acidentais no tema do computador de montagem.

Há 25 cores, opção 0 para o padrão upstream plasma e opção r para restaurar a aparência anterior ao uso do seletor. O comando equivalente é `bash "$HOME/folders-color-chooser.sh" -c blue`; `-C` seleciona plasma e `--restore` devolve a aparência anterior.

O seletor original trocava links no tema Gruvbox Plus. A versão integrada cria as pastas em duas variantes próprias, A/B, e alterna entre elas para atualizar o cache de ícones. Os temas Gruvbox-Plus-Dark e Gruvbox-Sistema-Colorido ficam intactos. Os demais ícones são herdados do tema de sistema aprovado; ícones simbólicos `xsi-*` de ações do sistema mantêm suas cores específicas. A troca não modifica categorias, aplicativos, áudio, rede, Bluetooth, cursores, temas visuais, papéis de parede ou arquivos dos espaços.

A troca é recusada se outro tema estiver selecionado, se faltar o pacote instalado, se as variantes próprias tiverem sido substituídas, se a origem apontar para fora do tema ou se houver outra troca em andamento. O tema é montado antes da aplicação e as duas preferências de ícones são restauradas se a aplicação falhar. Não requer sudo nem reiniciar Nemo ou Cinnamon.

As variantes são registradas pelo instalador e pelo restaurador do pacote. Na desinstalação, as preferências anteriores são restauradas e as cópias modificadas são preservadas na pasta de recuperação já documentada. A opção r é a forma rápida de desfazer somente a escolha de cor.
