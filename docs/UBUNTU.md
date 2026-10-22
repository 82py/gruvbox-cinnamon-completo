# Possível adaptação ao Ubuntu

Avaliação em 21/10/2026; nenhuma adaptação foi feita.

A versão mais recente nesta data é Ubuntu 26.10, lançada em 15/10/2026. O Ubuntu Desktop padrão usa GNOME e Wayland; desde Ubuntu 25.10 deixou de oferecer a sessão GNOME em Xorg.

Fontes oficiais:
- https://documentation.ubuntu.com/release-notes/26.10/
- https://lists.ubuntu.com/archives/ubuntu-announce/2026-October/000330.html
- https://documentation.ubuntu.com/release-notes/25.10/
- https://discourse.ubuntu.com/t/ubuntu-25-10-drops-support-for-gnome-on-xorg/62538

## Ubuntu Desktop com GNOME

É possível adaptar a aparência, mas não instalar esta configuração inteira sem mudanças. Os ícones e parte dos cursores/temas GTK podem ser reaproveitados. Aplicativos GTK4/libadwaita podem apresentar limites de tematização e exigem verificação própria.

O tema de painel, os applets e as extensões deste pacote usam APIs do Cinnamon. Seria necessário desenvolver equivalentes para GNOME Shell e refazer a configuração de painel/menu. Os próprios desenhos coloridos podem servir de base.

Rain e espaços independentes são a maior parte do trabalho: usam xwinwrap, janelas do desktop X11 e `_NET_CURRENT_DESKTOP`. XWayland permitir executar aplicativos X11 não oferece automaticamente o controle do fundo e dos espaços de trabalho da sessão Wayland. A conclusão técnica é que essas integrações precisam de outra implementação, provavelmente uma extensão GNOME e uma solução de vídeo de fundo própria para Wayland. A separação de arquivos deve ser redesenhada junto ao componente que desenhará o desktop.

## Ubuntu com Cinnamon

Usar Ubuntu Cinnamon ou instalar uma sessão Cinnamon X11 é o caminho mais próximo do ambiente atual. Ainda seria necessário conferir versões, dependências, integração do gerenciador de arquivos e comportamento das extensões. Não há garantia de que o Ubuntu Cinnamon mais recente mantenha exatamente as APIs e o comportamento de Cinnamon 6.6/Nemo 6.6. Este pacote bloqueia a aplicação em versões não validadas.

Plano futuro: testar primeiro os ícones numa máquina virtual, depois painel/extensões, Rain e por último a separação de pastas e a restauração. Para preservar o conjunto quase integralmente, priorizar Cinnamon X11; para o Ubuntu GNOME padrão, tratar como uma nova variante do projeto.
