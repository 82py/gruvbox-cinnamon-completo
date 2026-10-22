# Applets and extensions / Applets e extensões

[English](#english) · [Português](#português)

## English

Version 1.1.0 configures **14 Cinnamon built-in applets**: Menu, Separator, Grouped window list, System tray, XApp status, Printers, Keyboard, Network, Sound, Notifications, Calendar, Settings, Window quick list and Corner bar (show desktop). Their code comes from Cinnamon; it is not copied into or patched by this package. The panel component supplies layout and selected appearance preferences.

**Radio3 and Magic Lamp are excluded from 1.1.0**: the Radio3 applet/configuration/dependencies and the Magic Lamp extension/settings are not shipped or installed. A radio instance already enabled on the destination desktop is preserved. Older releases in GitHub's history can still contain Radio3.

Four extensions are included:

| Extension | Purpose | GUI component |
| --- | --- | --- |
| `gruvbox-microphone-colors@gruvbox-cinnamon` | Preserve microphone indicator colors | System icons and indicators |
| `gruvbox-mintupdate-colors@gruvbox-cinnamon` | Preserve MintUpdate indicator colors | System icons and indicators |
| `gruvbox-system-colors@gruvbox-cinnamon` | Color system/menu icons and places | System icons and indicators |
| `gruvbox-profile-photo@gruvbox-cinnamon` | Refresh the account photo shown in the menu | Profile photo refresh |

The three color extensions are selected together with the system-icons group. The photo extension uses the recipient's account photo; no personal photo is bundled. Profile-photo refresh is separately selectable.

**Rain is a tray application**, with supporting player scripts. **Independent workspaces use user scripts and a systemd user service**. Neither is a Cinnamon applet or extension. See [workspaces and Rain](ESPACOS-E-RAIN.md) and [credits](../CREDITOS.md).

## Português

A versão 1.1.0 configura **14 applets nativos do Cinnamon**: Menu Iniciar, Separador, Lista agrupada de janelas, Bandeja do sistema, Indicadores XApp, Impressoras, Teclado, Rede, Som, Notificações, Calendário, Configurações, Lista rápida de janelas e Botão de canto (mostrar desktop). O código vem do Cinnamon; não é copiado nem modificado pelo pacote. O componente de painel fornece disposição e preferências visuais selecionadas.

**Radio3 e Magic Lamp estão excluídos da 1.1.0**: o applet/configuração/dependências do Radio3 e a extensão/configurações do Magic Lamp não são distribuídos nem instalados. Uma instância de rádio já habilitada no computador de destino é preservada. Versões antigas no histórico do GitHub ainda podem conter Radio3.

Quatro extensões acompanham o pacote:

| Extensão | Finalidade | Componente na GUI |
| --- | --- | --- |
| `gruvbox-microphone-colors@gruvbox-cinnamon` | Preservar as cores do indicador de microfone | Ícones e indicadores do sistema |
| `gruvbox-mintupdate-colors@gruvbox-cinnamon` | Preservar as cores do indicador de atualizações | Ícones e indicadores do sistema |
| `gruvbox-system-colors@gruvbox-cinnamon` | Colorir ícones de sistema/menu e lugares | Ícones e indicadores do sistema |
| `gruvbox-profile-photo@gruvbox-cinnamon` | Atualizar a foto da conta mostrada no menu | Atualização da foto de perfil |

As três extensões de cores são selecionadas juntas pelo grupo de ícones de sistema. A extensão de foto usa a imagem da própria conta do destinatário; nenhuma foto pessoal acompanha o pacote. A atualização da foto pode ser selecionada separadamente.

**Rain é um aplicativo de bandeja**, com scripts de reprodução. **Os espaços independentes usam scripts e um serviço systemd do usuário**. Nenhum dos dois é um applet ou extensão do Cinnamon. Veja [espaços e Rain](ESPACOS-E-RAIN.md) e os [créditos](../CREDITOS.md).
