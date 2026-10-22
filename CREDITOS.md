# Créditos e licenças

- **Pir ([82py](https://github.com/82py))** — concepção da personalização, direção visual, escolhas de desenhos e cores, revisão e aprovação dos ícones, integração desejada e testes de uso no Cinnamon.
- **OpenAI Codex** — assistência na criação e revisão dos ícones personalizados, investigação da renderização, implementação das integrações, portabilidade, documentação e empacotamento, sob orientação e aprovação de Pir.
- **Pavel Pertsev (morhetz)** — criador do [Gruvbox](https://github.com/morhetz/gruvbox), paleta que fundamenta este projeto; o upstream declara MIT/X11.
- **SylEleuth** e colaboradores — [Gruvbox Plus Icon Pack](https://github.com/SylEleuth/gruvbox-plus-icon-pack), base dos ícones; GPL-3.0 e licenças herdadas, preservadas em `LICENSES/gruvbox-plus`.
- **Sam Hewitt** (Suru), **Andrea Bonanni e Gustavo Costa** (Suru++), **Vince Liuice** (Tela), **Alexey Varfolomeev e Papirus Development Team**, **Numix Team**, **Keefer Rourke** (La Capitaine), **Adhe** (One Dark): bases reconhecidas pelo Gruvbox Plus; consultar os avisos originais completos.
- **Linux Mint, Clement Lefebvre e colaboradores** — Cinnamon, Nemo, Muffin, XApp, MintUpdate, Mint Themes e ícones de sistema usados como base. Os avisos de origem encontrados estão em `LICENSES/`. Mint Themes usa GPL-3.0-or-later; outras partes conservam seus avisos específicos.
- **Blueman Development Team** — desenhos de Bluetooth usados como base; aviso preservado em `LICENSES/icones-sistema`.
- **klangman**, com base na extensão de **hermes83** — [CinnamonMagicLamp](https://github.com/klangman/CinnamonMagicLamp); licença original acompanha a extensão.
- **claudiux** e colaboradores do Cinnamon Spices — [Radio3.0](https://cinnamon-spices.linuxmint.com/applets/view/360); licença original e licença da biblioteca XML acompanham o applet.
- **el-amine-404, claudiux e anaximeno** — ações adicionais de Nemo presentes na configuração. Metadados originais acompanham cada ação; o aviso GPL-2.0 do repositório oficial está em `LICENSES/nemo-actions`.
- **David Reveman / Novell**, **Shantanu Goel**, **Aaahh**, **mmhobi7** e colaboradores — [xwinwrap](https://github.com/mmhobi7/xwinwrap). Fonte fixado em uma revisão, com aviso permissivo Novell original preservado no cabeçalho.
- **mpv, FFmpeg, Python, PyGObject/GTK, python-xlib, systemd, X.Org, Socat e demais dependências** — projetos independentes; seus programas não passam a ser autoria deste pacote.

## Origens confirmadas por Pir

Em 21/10/2026, Pir confirmou os repositórios de origem dos ícones e do Gruvbox original:

- Ícones: https://github.com/SylEleuth/gruvbox-plus-icon-pack
- Gruvbox original: https://github.com/morhetz/gruvbox

Essas confirmações não identificam, por si só, a origem da cópia do tema visual Gruvbox-Dark-BL-MOD nem do cursor Gruvbox_Cursors_Dark.

## Tema visual e cursor identificados por comparação

**Tema visual:** [Gruvbox GTK Theme, de Fausto-Korpsvart](https://github.com/Fausto-Korpsvart/Gruvbox-GTK-Theme), baseado no trabalho de **Vince Liuice**. A própria cópia instalada registra `vinceliucie | mod: f.korpsvart` e `GPL` nos arquivos Metacity. Na revisão histórica `c0b7fb501938241a3b6b5734f8cb1f0982edc6b4`, 251 arquivos regulares de Gruvbox-Dark-BL são idênticos aos da cópia local; a diferença de conteúdo está em `cinnamon/cinnamon.css`. A licença GPL-3.0 original está em `LICENSES/gruvbox-gtk`.

**Cópia MOD:** a coleção [Twilight4/gnome-settings](https://github.com/Twilight4/gnome-settings), revisão `5560f12a465654d1808638ccb4e6e0968ac10240`, contém Gruvbox-Dark-BL-MOD. Coincidem 255 entradas (incluindo links); o CSS do Cinnamon instalado tem alterações adicionais. Essa coleção comprova a presença pública da variante, mas não identifica por si só o autor de cada alteração do CSS. [LinuxScoop](https://medium.com/@linuxscoop/customize-your-linux-mint-cinnamon-edition-look-warm-and-aesthetic-with-gruvbox-color-theme-9a168524a860) publicou uma montagem Gruvbox para Cinnamon em 2023; foi encontrado como referência de distribuição, não como prova de autoria de todos os arquivos. Os temas preservam a licença GPL-3.0 do projeto-base, com origem e modificações sinalizadas em ORIGIN.txt; a autoria individual de modificações históricas do CSS permanece não identificada e não foi atribuída a Pir ou ao Codex.

**Cursor:** o diretório instalado Gruvbox_Cursors_Dark é uma cópia renomeada de **Capitaine Cursors (Gruvbox) – White**, versão **r5**, do projeto [sainnhe/capitaine-cursors](https://github.com/sainnhe/capitaine-cursors). Os 113 arquivos coincidem byte a byte com a versão oficial Linux.zip. **Keefer Rourke** criou o [Capitaine original](https://github.com/keeferrourke/capitaine-cursors), baseado nos cursores **KDE Breeze**; **sainnhe** adicionou a variante Gruvbox. O projeto também reconhece **ful1e5/apple_cursor** pela base das ferramentas de compilação. O aviso LGPL-3.0-or-later do Capitaine foi recuperado e está em `LICENSES/capitaine-cursors/COPYING`; os SVGs e ferramentas da revisão r5 estão em `vendor/capitaine-cursors`.

O Gruvbox Plus Icon Pack fornece os ícones; os temas GTK/Cinnamon e o cursor são projetos separados. Compartilhar a paleta ou a palavra Gruvbox no nome não significa que todos esses componentes façam parte do pacote de ícones.

## Direitos dos desenhos e marcas

Ícones personalizados incluem adaptações de desenhos de terceiros e referências a produtos e marcas. A presença de um ícone não indica associação com seus titulares e não transfere os direitos sobre marcas ou artes originais. A licença GPL da integração não substitui as licenças de cada arte de origem. São preservados os avisos e as licenças do tema-base e das referências de sistema encontrados na montagem.

Não são distribuídos fotos pessoais, imagens de fundo, vídeos ou documentos da máquina de origem.

## Seletor de cor das pastas

**akarzim**, reconhecido no README do Gruvbox Plus, é creditado pelo seletor original `folders-color-chooser`. A cópia original está em `vendor/gruvbox-folder-colors`. O menu em português e a adaptação para variantes separadas fazem parte da integração de Pir (82py), com assistência do OpenAI Codex. A adaptação preserva os temas-base e de sistema e não altera applets ou aplicativos.

## Complementos da auditoria

O perfil visual do terminal é uma configuração de Pir para cool-retro-term (projeto Swordfish90); o programa é dependência externa, sem redistribuição do seu binário. As regras Fontconfig para excluir webfonts problemáticas são preferências de usuário. Relax usa Celluloid/mpv como dependências externas. Ubuntu Font Family (Canonical) e DejaVu são fornecidas pelos pacotes de fontes indicados no instalador. A emissora JB FM e seus recursos são externos; o pacote guarda apenas o endereço público do preset, sem áudio, gravações ou histórico.
