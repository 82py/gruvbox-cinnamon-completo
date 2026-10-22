# Validação em Mint Cinnamon real

Versão 1.0.2, 21/10/2026. VM QEMU/KVM com 4 vCPUs, 8 GiB de RAM e disco virtual de 40 GiB. Linux Mint 22.3 instalado a partir da ISO oficial Cinnamon; SHA-256 e assinatura da chave oficial foram verificados. Cinnamon 6.6.4, Nemo 6.6.3, Muffin 6.6.1 e X11.

Nenhum disco físico, pasta pessoal, área de transferência ou dispositivo de áudio do host foi compartilhado. A rede usa NAT; a porta de teste SSH é vinculada apenas a 127.0.0.1. Chaves privadas, credenciais e discos virtuais não acompanham o projeto.

## Procedimento e resultados

1. Instalar o Mint no disco virtual e as dependências do script público. Só depois registrar a linha de base: as dependências permanecem após desinstalar o tema.
2. Registrar 115 destinos possíveis de instalação, os valores originais de 936 preferências e hashes de `/usr/share/cinnamon`, `/usr/share/themes` e `/usr/share/applications`. Criar um documento de teste na Área de Trabalho.
3. Instalar como usuário comum e reiniciar. Os 15 applets, incluindo Radio3, e as cinco extensões carregaram. Tema, ícones e quatro espaços corretos.
4. Alternar entre os quatro espaços: pastas e fundos independentes, sem misturar os documentos. Testar azul, laranja e jade no seletor real e restaurar sua aparência anterior; as 25 cores são cobertas adicionalmente pelos testes dos dois compactados.
5. Gerar vídeo e áudio sintéticos na própria VM. Rain reproduziu incorporado ao desktop pela saída X11, com volume, silenciar/reativar e pausa automática ao sair do espaço. O cliente de áudio identificado como Rain não foi capturado pela Radio3. Nenhum vídeo ou fundo de teste acompanha o pacote.
6. Executar o terminal real: perfil em pasta própria, com os caminhos XDG habituais devolvidos ao comando filho; dados originais do aplicativo preservados.
7. Desinstalar pelo comando instalado, conferir documentos, valores e arquivos e reiniciar novamente. Nenhuma diferença nos destinos e preferências comparados; arquivos internos preservados e nenhuma extensão do pacote em execução.

Resultados estruturados: [VALIDACAO-VM.json](VALIDACAO-VM.json). As capturas mostram uma conta descartável, sem foto ou conteúdo pessoal: [antes](imagens/mint-antes.png), [tema aplicado](imagens/menu-gruvbox-vm.png), [restaurado](imagens/mint-restaurado.png).

## Correções encontradas nos testes

A primeira beta podia mostrar um aviso de atualização nos primeiros segundos de boot, escolher uma saída de vídeo que abria outra janela e permitir que a Radio3 confundisse o áudio do Rain com seu player. A captura sequencial das preferências também registrava valores já sincronizados pelo Cinnamon; um arquivo da Radio3 podia ser regravado durante a restauração.

A 1.0.2 verifica as versões imediatamente, usa apenas saídas de vídeo incorporadas e testa sua prontidão, identifica o cliente de áudio pela interface PulseAudio compatível, captura o estado completo antes da primeira mudança e desliga os componentes gerenciados antes de restaurar seus arquivos. Os scripts próprios foram corrigidos; o applet de terceiros permaneceu intacto.

## Alcance

A validação cobre Mint 22.3 Cinnamon 6.6 X11. A VM não exercita aceleração por uma GPU física nem hardware real Wi-Fi, Bluetooth, impressora ou microfone. Não se anuncia suporte a Ubuntu GNOME/Wayland. Os testes automatizados, a auditoria da máquina de origem e a sessão virtual são verificações complementares.

Para repetir: use uma VM descartável, registre seus arquivos e preferências antes de instalar, siga INSTALAR.md, exercite os recursos e siga DESINSTALAR.md. Compare também depois da nova sessão. Não execute roteiros de teste destrutivos na conta principal.

Referências: [ISO oficial Mint 22.3](https://www.linuxmint.com/edition.php?id=326), [verificação de autenticidade](https://linuxmint-installation-guide.readthedocs.io/en/latest/verify.html), [opções do mpv](https://mpv.io/manual/stable/).
