# Ubuntu adaptation assessment / Possível adaptação ao Ubuntu

[English](#english) · [Português](#português)

## English

Tested specifications: **Linux Mint 22.3, Cinnamon/Nemo 6.6.x, X11**. Source: Cinnamon 6.6.9 and Nemo/Muffin 6.6.3. VM: Cinnamon 6.6.4, Nemo 6.6.3, Muffin 6.6.1. Other environments have not been validated. The following is a technical assessment dated **2026-10-21**. The release identified in the original assessment is Ubuntu 26.10, released on 2026-10-15. Standard Ubuntu Desktop uses GNOME and Wayland; Ubuntu 25.10 stopped offering GNOME on Xorg.

Official references recorded for that assessment:

- [Ubuntu 26.10 release notes](https://documentation.ubuntu.com/release-notes/26.10/)
- [Release announcement](https://lists.ubuntu.com/archives/ubuntu-announce/2026-October/000330.html)
- [Ubuntu 25.10 release notes](https://documentation.ubuntu.com/release-notes/25.10/)
- [GNOME on Xorg support change](https://discourse.ubuntu.com/t/ubuntu-25-10-drops-support-for-gnome-on-xorg/62538)

### Standard Ubuntu Desktop with GNOME

Adapting the complete setup would require reviewing its desktop integrations. Icons and some cursors/GTK themes can be reused. GTK4/libadwaita applications may limit theming and need separate verification.

The panel theme, applets, and extensions use Cinnamon APIs. GNOME Shell equivalents and a new panel/menu configuration would be needed. The colored artwork could be reused as a starting point.

Rain and independent workspace files require most of the work. They use xwinwrap, X11 desktop windows, and `_NET_CURRENT_DESKTOP`. Running X11 applications through XWayland does not automatically provide control over a Wayland session's desktop background or workspaces. These integrations therefore need a different implementation, likely a GNOME extension and a Wayland-specific video wallpaper solution. File separation must be designed alongside whichever component draws the desktop.

### Ubuntu with Cinnamon

Ubuntu Cinnamon or a Cinnamon X11 session is closer to the current environment. Versions, dependencies, file-manager integration, and extension behavior still need checking. The latest Ubuntu Cinnamon is not guaranteed to preserve exactly the Cinnamon 6.6/Nemo 6.6 APIs and behavior. This package blocks application on unvalidated versions.

A future adaptation should test icons in a VM first, followed by panel/extensions, Rain, and finally folder separation and restoration. Prefer Cinnamon X11 to preserve most of this setup; treat standard Ubuntu GNOME as a new project variant.

---

## Português

Especificações testadas: **Linux Mint 22.3, Cinnamon/Nemo 6.6.x, X11**. Origem: Cinnamon 6.6.9 e Nemo/Muffin 6.6.3. VM: Cinnamon 6.6.4, Nemo 6.6.3 e Muffin 6.6.1. Outros ambientes não foram validados. A seguir, avaliação técnica de 21/10/2026.

A versão mais recente nesta data é Ubuntu 26.10, lançada em 15/10/2026. O Ubuntu Desktop padrão usa GNOME e Wayland; desde Ubuntu 25.10 deixou de oferecer a sessão GNOME em Xorg.

Fontes oficiais:
- https://documentation.ubuntu.com/release-notes/26.10/
- https://lists.ubuntu.com/archives/ubuntu-announce/2026-October/000330.html
- https://documentation.ubuntu.com/release-notes/25.10/
- https://discourse.ubuntu.com/t/ubuntu-25-10-drops-support-for-gnome-on-xorg/62538

### Ubuntu Desktop com GNOME

A adaptação do conjunto completo exigiria revisar as integrações do desktop. Os ícones e parte dos cursores/temas GTK podem ser reaproveitados. Aplicativos GTK4/libadwaita podem apresentar limites de tematização e exigem verificação própria.

O tema de painel, os applets e as extensões deste pacote usam APIs do Cinnamon. Seria necessário desenvolver equivalentes para GNOME Shell e refazer a configuração de painel/menu. Os próprios desenhos coloridos podem servir de base.

Rain e espaços independentes são a maior parte do trabalho: usam xwinwrap, janelas do desktop X11 e `_NET_CURRENT_DESKTOP`. XWayland permitir executar aplicativos X11 não oferece automaticamente o controle do fundo e dos espaços de trabalho da sessão Wayland. A conclusão técnica é que essas integrações precisam de outra implementação, provavelmente uma extensão GNOME e uma solução de vídeo de fundo própria para Wayland. A separação de arquivos deve ser redesenhada junto ao componente que desenhará o desktop.

### Ubuntu com Cinnamon

Usar Ubuntu Cinnamon ou instalar uma sessão Cinnamon X11 é o caminho mais próximo do ambiente atual. Ainda seria necessário conferir versões, dependências, integração do gerenciador de arquivos e comportamento das extensões. Não há garantia de que o Ubuntu Cinnamon mais recente mantenha exatamente as APIs e o comportamento de Cinnamon 6.6/Nemo 6.6. Este pacote bloqueia a aplicação em versões não validadas.

Plano futuro: testar primeiro os ícones numa máquina virtual, depois painel/extensões, Rain e por último a separação de pastas e a restauração. Para preservar o conjunto quase integralmente, priorizar Cinnamon X11; para o Ubuntu GNOME padrão, tratar como uma nova variante do projeto.
