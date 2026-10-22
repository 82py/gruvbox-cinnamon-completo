# Gruvbox Cinnamon Completo

Personalização organizada por **Pir ([82py](https://github.com/82py))**, com assistência do **OpenAI Codex** na criação e revisão de ícones, integração, documentação e empacotamento.

Versão 1.0.3 · retrato da configuração ativa em 21/10/2026 · Linux Mint 22.3, Cinnamon 6.6 / Nemo 6.6, sessão X11.

Inclui Relax, o perfil visual isolado do terminal, as correções de fontes por aplicativo Flatpak e o tema Gruvbox Plus Dark personalizado, a variante Gruvbox Sistema Colorido, as categorias e indicadores coloridos, temas visuais, cursor, layout do painel e menus, Magic Lamp, Radio3, extensões próprias, ações do Nemo, Rain completo e quatro espaços com pastas e fundos independentes.

**Sem vídeos, imagens de fundo, foto de perfil ou documentos pessoais.** O primeiro acesso usa fundo sólido Gruvbox; cada pessoa escolhe suas mídias. Aplicativos de terceiros não são instalados pelo tema: seus ícones são fornecidos e os atalhos existentes recebem as associações correspondentes.

## Usar a cópia completa

Baixe o TAR.GZ e sua assinatura SHA-256 em [Releases](https://github.com/82py/gruvbox-cinnamon-completo/releases). Prefira esse arquivo ao ZIP automático do GitHub, para preservar os links dos ícones. Extraia em uma pasta de sua escolha. Leia [instalação](docs/INSTALAR.md), [restauração](docs/DESINSTALAR.md) e [espaços e Rain](docs/ESPACOS-E-RAIN.md).

```sh
bash verificar.sh
bash instalar.sh
# Depois: encerrar a sessão e entrar novamente.
# Para voltar ao estado anterior:
bash desinstalar.sh
```

Execute os três comandos como usuário comum. O instalador não baixa dependências nem altera arquivos internos do Cinnamon ou aplicativos. O comando separado de dependências é descrito no guia.

## Cor das pastas

O seletor em português e seu script auxiliar acompanham a raiz do pacote e são instalados na pasta pessoal. Depois da instalação, também aparecem no Iniciar. Veja [cores das pastas](docs/CORES-DAS-PASTAS.md).

## Publicar e compatibilidade

A estrutura pública inclui os componentes visuais, código, créditos e licenças recuperadas. O binário xwinwrap da máquina original fica separado; a instalação pública compila o fonte incluído. Consulte [publicação](docs/PUBLICAR.md), [créditos](CREDITOS.md) e [proveniência](docs/PROVENIENCIA.json). Repositório: [82py/gruvbox-cinnamon-completo](https://github.com/82py/gruvbox-cinnamon-completo).

[Análise de Ubuntu](docs/UBUNTU.md): adaptação possível, mas esta versão não é um instalador para GNOME/Wayland. Nenhuma adaptação foi aplicada.

## Estrutura

- `payload/`: ícones, temas com licença conhecida, extensões, applet e código portátil.
- `assets-locais/`: cópias locais separadas, somente o binário xwinwrap da máquina de origem; excluídas do Git.
- `vendor/xwinwrap/`: fonte original com revisão fixa e aviso de licença no cabeçalho.
- `scripts/manage.py`: instalação com registro de alterações, cópias de segurança e restauração.
- `settings.json`, `app-icons.json`, `manifest.json`: configuração e inventário portáteis.
- `LICENSES/`, `CREDITOS.md`: avisos dos projetos de origem.
- `tests/`, `.github/workflows/`: verificação de instalação e desinstalação isoladas.

O código de integração deste projeto está sob GPL-3.0-or-later. Cada componente de terceiros mantém sua própria licença; a licença da raiz não substitui os avisos dos autores originais.

## Auditoria final

A personalização foi comparada com os componentes carregados no Cinnamon: 15 applets, cinco extensões, 180 entradas visíveis no menu e 936 preferências explícitas. Veja [auditoria](docs/AUDITORIA-FINAL.md) e [inventário do menu](docs/MENU-INVENTARIADO.json). `scripts/auditar-desktop.py` repete a comparação somente de leitura.

## Validação em máquina virtual

A 1.0.2 foi instalada e desinstalada em Linux Mint 22.3 Cinnamon X11, em VM QEMU/KVM. Os 15 applets e as cinco extensões carregaram; os quatro espaços, fundos locais, Rain e cores das pastas foram exercitados. Após desinstalar e reiniciar, a comparação de 115 destinos e 936 preferências não encontrou diferenças; documentos foram preservados.

Veja [método e resultados](docs/VALIDACAO-VM.md) e [relatório estruturado](docs/VALIDACAO-VM.json). A 1.0.3 acrescenta a correção da janela de cópia: uma seleção aberta pelo menu executa uma única operação, fecha ao concluir e envia uma notificação. Cliques repetidos e falhas parciais não repetem os itens já copiados. A correção tem [testes GTK próprios](tests/test_copy_dialog.py) e [relatório](docs/VALIDACAO-COPIA.json); a instalação e desinstalação em VM documentadas acima foram realizadas com a 1.0.2.

![Menu e painel na máquina virtual](docs/imagens/menu-gruvbox-vm.png)
