# Instalação

## Plataforma

A configuração de origem é Linux Mint 22.3 Zena com Cinnamon 6.6.9, Nemo/Muffin 6.6.3 e X11. O instalador aceita Cinnamon/Nemo 6.6.x em X11; outras versões precisam de validação. Não execute em GNOME/Wayland. A versão 1.0.2 foi instalada e desinstalada em uma VM Mint 22.3 com Cinnamon 6.6.4, Nemo 6.6.3 e Muffin 6.6.1, incluindo reinicializações e comparação dos arquivos e preferências originais. O Cinnamon da máquina de origem permaneceu intacto. Veja VALIDACAO-VM.md para o alcance dos testes.

## Passos

1. Extraia o TAR.GZ completo mantendo sua estrutura. Prefira TAR.GZ: ele conserva os links internos do tema de ícones.
2. Abra um terminal na pasta extraída e execute `bash verificar.sh`. Esse comando apenas verifica requisitos.
3. Se faltarem dependências, leia `scripts/instalar-dependencias.sh` e execute `bash scripts/instalar-dependencias.sh`. Esse comando separado usa sudo para instalar pacotes públicos do Mint; o tema é instalado sem sudo.
4. Execute `bash instalar.sh` como usuário comum. O instalador verifica requisitos, guarda cópias de segurança e aplica somente os arquivos e chaves registrados no inventário.
5. Encerre a sessão e entre novamente. Isso permite que o Nemo leia o caminho novo da Área de Trabalho e inicia o Rain na bandeja e o serviço dos espaços.
6. No Iniciar, abra “Fundos por espaço” para selecionar imagens e “Rain” para selecionar um vídeo local. Nenhuma mídia é baixada automaticamente.

Os caminhos são resolvidos a partir de `$HOME` e do usuário atual. Os atalhos recebem caminhos absolutos corretos na instalação, porque arquivos `.desktop` não expandem `$HOME` ou `$USER`.

## O que muda

Temas em `$HOME/.themes`, ícones em `$HOME/.local/share/icons`, cursor em `$HOME/.icons`, executáveis em `$HOME/.local/bin`, extensões/applet em `$HOME/.local/share/cinnamon`, preferências selecionadas, ações do Nemo e atalhos do usuário. As configurações capturadas incluem painel, favoritos, menus, notificações, gestos, aparência, fontes e atalhos para Rain. Não inclui senhas, credenciais, redes salvas, contas, histórico de execução ou localização geográfica.

O ambiente fica com quatro espaços. O espaço 1 usa a pasta que já era a Área de Trabalho; os espaços 2–4 recebem pastas vazias em `$HOME/Espaços de trabalho Gruvbox`. A separação usa apenas um link `.atual`. Nenhum documento é movido ou apagado.

A foto de perfil do destinatário permanece sendo a dele; a extensão de atualização de foto acompanha o código, mas nenhuma foto ou cache de foto é distribuído.

A Radio3 conserva suas preferências visuais; o preset público JB FM é preservado; históricos, pesquisas e agendamentos pessoais não são distribuídos. A instalação de programas, PWAs, jogos e suas contas é responsabilidade de quem os usa. Atalhos associados a programas ausentes não são inventados, e favoritos de programas não instalados podem não aparecer.

## Cópia de segurança

O registro e as cópias ficam em `$HOME/.local/state/gruvbox-cinnamon`. Não apague essa pasta antes de desinstalar. Se houver erro durante a instalação, o instalador tenta restaurar automaticamente os arquivos e valores já registrados. Não é permitida uma segunda instalação sobre uma instalação registrada: restaure a anterior primeiro.

A instalação guarda o fundo anterior apenas no computador de destino, para permitir a restauração; essa imagem não é copiada para o pacote.

## Complementos da revisão 1.0.1

O atalho Relax pede um vídeo local e abre Celluloid em tela cheia (com alternativa mpv). Ctrl+F12 continua usando mpv. O terminal mantém o perfil visual exportado, em dados separados; os programas iniciados nele recebem seus caminhos XDG habituais. Comandos pessoais de shell e posições de janelas não são transferidos.

As correções de fontes de KClock e Materialgram são preferências do usuário, não alterações nos aplicativos. O instalador mescla FONTCONFIG_FILE com as outras permissões/variáveis já existentes, sem removê-las. A organização do menu Chromium também é mesclada. Insync e Bitwarden só recebem sua entrada de inicialização automática se já estiverem instalados; o pacote não instala esses programas nem copia suas contas.

As associações de arquivos ficam em `optional/mimeapps.list` como referência; não substituem automaticamente os aplicativos padrão do destinatário. Os programas e serviços pessoais de servidores, tarefas, VPN e sincronização não fazem parte do tema.

## Ajustes da revisão 1.0.2

O serviço dos espaços verifica suas versões já na primeira execução, sem o aviso falso de atualização durante o boot. O Rain aguarda a saída de vídeo ficar pronta e usa X11 como alternativa quando a aceleração gráfica não está disponível. Seu áudio e o atalho de vídeo mpv usam a interface PulseAudio compatível do Mint, com nomes próprios, para não serem confundidos com a Radio3. Nenhum applet foi alterado.

O instalador captura todas as preferências originais antes da primeira mudança. A restauração desativa os componentes gerenciados antes de remover seus arquivos e encerra os processos próprios do Rain. As dependências do sistema são instaladas antes da personalização e não são removidas automaticamente na desinstalação.
