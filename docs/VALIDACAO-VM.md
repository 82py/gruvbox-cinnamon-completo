# Mint Cinnamon VM validation / Validação em máquina virtual

[English](#english) · [Português](#português)

## English

**The updated 1.1.0 GUI installer completed a separate full install, feature, uninstall and reboot cycle in an isolated Mint VM, including the 2026-10-22 actor cleanup and Nemo preference protection. See the [GUI report](../VALIDACAO-GUI.json). The 1.0.2 report below is historical.**

**Historical validation of version 1.0.2, 2026-10-21.** QEMU/KVM VM: 4 vCPUs, 8 GiB RAM, and a 40 GiB virtual disk. Linux Mint 22.3 was installed from the official Cinnamon ISO after checking SHA-256 and the official signing-key signature. Guest versions: Cinnamon 6.6.4, Nemo 6.6.3, Muffin 6.6.1, X11.

No physical host disk, home folder, clipboard, or audio device was shared. Networking used NAT and a test SSH port bound only to 127.0.0.1. Private keys, credentials, and VM disks are not distributed.

### Procedure and results

1. Install Mint and the public installer's dependencies before taking the baseline; dependencies remain after theme removal.
2. Record 115 possible installation destinations, 936 original preference values, and hashes under `/usr/share/cinnamon`, `/usr/share/themes`, and `/usr/share/applications`. Create a test document on the Desktop.
3. Install as a regular user and reboot. All 15 applets, including Radio3, and five extensions loaded. Theme, icons, and four workspaces were correct.
4. Switch among all four workspaces: independent folders and backgrounds, without mixing documents. Exercise blue, orange, and jade using the actual folder selector and restore its prior appearance; archive tests separately cover all 25 colors.
5. Generate synthetic video/audio inside the VM. Rain played embedded in the desktop via X11, with volume, mute/unmute, and automatic pause when leaving its workspace. Its Rain audio client was not captured by Radio3. No test video or wallpaper is included.
6. Start the real terminal with its separate profile. Child commands receive normal XDG paths, preserving original application data.
7. Uninstall using the installed command, check documents, preferences, and files, then reboot again. There were no differences in the compared destinations/preferences; internal files were preserved and no package extension remained running.

[Structured results](VALIDACAO-VM.json). Screenshots use a disposable account without a personal photo or documents: [before](imagens/mint-antes.png), [theme applied](imagens/menu-gruvbox-vm.png), [restored](imagens/mint-restaurado.png).

### Fixes discovered during testing

The first beta could issue a false version-update warning during early boot, select a video output that opened a separate window, and let Radio3 mistake Rain for its player. Sequential preference snapshots could capture values already synchronized across Cinnamon/GNOME schemas; a Radio3 file could also be rewritten during restoration.

Version 1.0.2 checks versions immediately, restricts video to embedded outputs and checks readiness, identifies the audio client through PulseAudio compatibility, snapshots all preferences before the first change, and disables managed components before restoring files. Only integration scripts were changed; the third-party applet remained untouched.

### Scope

This covers Mint 22.3 Cinnamon 6.6 X11. The VM did not exercise a physical GPU or real Wi-Fi, Bluetooth, printer, or microphone hardware. Validation is limited to the environments listed above. Automated tests, the source-machine audit, and the VM session provide complementary evidence.

The full VM cycle was not repeated for 1.0.3. Its copy-dialog changes have [separate GTK regression tests](../tests/test_copy_dialog.py) and a [report](VALIDACAO-COPIA.json).

To repeat the VM test, use a disposable VM, record files/preferences, follow [installation](INSTALAR.md), exercise features, follow [restoration](DESINSTALAR.md), and compare again after a new session. Do not run destructive test scenarios in your main account.

References: [official Mint 22.3 ISO](https://www.linuxmint.com/edition.php?id=326), [authenticity verification](https://linuxmint-installation-guide.readthedocs.io/en/latest/verify.html), [mpv options](https://mpv.io/manual/stable/).

---

## Português

**O instalador GUI 1.1.0 atualizado completou um ciclo separado de instalação, recursos, remoção e reinicializações numa VM Mint isolada, incluindo as correções de 22/10/2026 para liberação de elementos e preservação da preferência do Nemo. Veja o [relatório da GUI](../VALIDACAO-GUI.json). O relatório da versão 1.0.2 abaixo é histórico.**

Versão 1.0.2, 21/10/2026. VM QEMU/KVM com 4 vCPUs, 8 GiB de RAM e disco virtual de 40 GiB. Linux Mint 22.3 instalado a partir da ISO oficial Cinnamon; SHA-256 e assinatura da chave oficial foram verificados. Cinnamon 6.6.4, Nemo 6.6.3, Muffin 6.6.1 e X11.

Nenhum disco físico, pasta pessoal, área de transferência ou dispositivo de áudio do host foi compartilhado. A rede usa NAT; a porta de teste SSH é vinculada apenas a 127.0.0.1. Chaves privadas, credenciais e discos virtuais não acompanham o projeto.

### Procedimento e resultados

1. Instalar o Mint no disco virtual e as dependências do script público. Só depois registrar a linha de base: as dependências permanecem após desinstalar o tema.
2. Registrar 115 destinos possíveis de instalação, os valores originais de 936 preferências e hashes de `/usr/share/cinnamon`, `/usr/share/themes` e `/usr/share/applications`. Criar um documento de teste na Área de Trabalho.
3. Instalar como usuário comum e reiniciar. Os 15 applets, incluindo Radio3, e as cinco extensões carregaram. Tema, ícones e quatro espaços corretos.
4. Alternar entre os quatro espaços: pastas e fundos independentes, sem misturar os documentos. Testar azul, laranja e jade no seletor real e restaurar sua aparência anterior; as 25 cores são cobertas adicionalmente pelos testes dos dois compactados.
5. Gerar vídeo e áudio sintéticos na própria VM. Rain reproduziu incorporado ao desktop pela saída X11, com volume, silenciar/reativar e pausa automática ao sair do espaço. O cliente de áudio identificado como Rain não foi capturado pela Radio3. Nenhum vídeo ou fundo de teste acompanha o pacote.
6. Executar o terminal real: perfil em pasta própria, com os caminhos XDG habituais devolvidos ao comando filho; dados originais do aplicativo preservados.
7. Desinstalar pelo comando instalado, conferir documentos, valores e arquivos e reiniciar novamente. Nenhuma diferença nos destinos e preferências comparados; arquivos internos preservados e nenhuma extensão do pacote em execução.

Resultados estruturados: [VALIDACAO-VM.json](VALIDACAO-VM.json). As capturas mostram uma conta descartável, sem foto ou conteúdo pessoal: [antes](imagens/mint-antes.png), [tema aplicado](imagens/menu-gruvbox-vm.png), [restaurado](imagens/mint-restaurado.png).

### Correções encontradas nos testes

A primeira beta podia mostrar um aviso de atualização nos primeiros segundos de boot, escolher uma saída de vídeo que abria outra janela e permitir que a Radio3 confundisse o áudio do Rain com seu player. A captura sequencial das preferências também registrava valores já sincronizados pelo Cinnamon; um arquivo da Radio3 podia ser regravado durante a restauração.

A 1.0.2 verifica as versões imediatamente, usa apenas saídas de vídeo incorporadas e testa sua prontidão, identifica o cliente de áudio pela interface PulseAudio compatível, captura o estado completo antes da primeira mudança e desliga os componentes gerenciados antes de restaurar seus arquivos. Os scripts próprios foram corrigidos; o applet de terceiros permaneceu intacto.

### Alcance

A validação cobre Mint 22.3 Cinnamon 6.6 X11. A VM não exercita aceleração por uma GPU física nem hardware real Wi-Fi, Bluetooth, impressora ou microfone. A validação se limita aos ambientes listados acima. Os testes automatizados, a auditoria da máquina de origem e a sessão virtual são verificações complementares.

Para repetir: use uma VM descartável, registre seus arquivos e preferências antes de instalar, siga INSTALAR.md, exercite os recursos e siga DESINSTALAR.md. Compare também depois da nova sessão. Não execute roteiros de teste destrutivos na conta principal.

Referências: [ISO oficial Mint 22.3](https://www.linuxmint.com/edition.php?id=326), [verificação de autenticidade](https://linuxmint-installation-guide.readthedocs.io/en/latest/verify.html), [opções do mpv](https://mpv.io/manual/stable/).
