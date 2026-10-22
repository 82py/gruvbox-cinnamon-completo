# Estrutura para GitHub

Repositório público: https://github.com/82py/gruvbox-cinnamon-completo

A primeira publicação, v1.0.1, permanece como pré-lançamento histórico. A v1.0.2 incorpora as correções encontradas e a validação completa em uma VM Mint 22.3 Cinnamon X11; veja VALIDACAO-VM.md.

Execute `python3 scripts/exportar-publico.py` para criar uma árvore pública e um TAR.GZ ao lado deste projeto. A exportação inclui ícones, temas, cursor, código e documentação. O binário xwinwrap copiado da máquina de origem fica fora: o instalador compila o fonte fixado em `vendor/xwinwrap` no computador de destino.

Os avisos dos projetos de origem foram recuperados e preservados. A proveniência do tema e do cursor foi conferida por conteúdo; veja `docs/PROVENIENCIA.json` e `CREDITOS.md`. A autoria individual de algumas alterações históricas do CSS da variante MOD não foi estabelecida e não é atribuída aos autores desta integração.

## Antes do envio

1. Confira `CREDITOS.md`, os avisos em `LICENSES/` e os arquivos ORIGIN.txt. Não remova os créditos dos autores originais ou substitua licenças de terceiros pela licença da raiz.
2. Confira os arquivos preparados e execute `python3 tests/test_public.py` e `python3 tests/test_install.py`.
3. Para futuras alterações de instalação/runtime, repita o ciclo em uma VM Mint 22.3 Cinnamon X11, com reinicializações e comparação de arquivos/preferências. Os testes isolados complementam essa sessão gráfica; não a substituem.
4. Produza capturas novas numa conta limpa, sem foto, documentos ou locais de rede pessoais.
5. Para novas versões, confira o diff e as exclusões, execute os testes, gere o TAR.GZ com `python3 scripts/empacotar.py` e publique com sua assinatura SHA-256. Nunca envie `assets-locais/`, mídias ou perfis pessoais. Nenhum envio é realizado pelos scripts do tema.

Releases: disponibilizar TAR.GZ com links simbólicos preservados e SHA-256. Descrição sugerida: “Gruvbox para Linux Mint Cinnamon: ícones coloridos, painel, Rain e espaços independentes”. O GitHub pode gerar ZIPs de código sem conservar adequadamente os links; prefira o TAR.GZ fornecido pelo projeto para instalação.

A integração usa GPL-3.0-or-later. Componentes de terceiros conservam suas licenças específicas. Não anunciar suporte a Ubuntu GNOME/Wayland antes de adaptar e validar essa plataforma.
