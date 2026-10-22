# Publishing on GitHub / Publicar no GitHub

[English](#english) · [Português](#português)

## English

**Current release: 1.1.0 adds the GTK manager and removes Radio3. On a prepared public checkout, run `python3 scripts/empacotar.py` to rebuild the versioned TAR.GZ, checksums and report. Run the GUI engine/GTK tests in addition to existing checks. Inspect the archive for private data before uploading it. The export procedure below describes creating a separate public tree from a source tree; it refuses an existing destination.**

Public repository: [82py/gruvbox-cinnamon-completo](https://github.com/82py/gruvbox-cinnamon-completo).

The initial v1.0.1 remains a historical prerelease. Version 1.0.2 includes fixes and complete Mint 22.3 Cinnamon X11 VM validation; see [VM validation](VALIDACAO-VM.md). Version 1.0.3 fixes repeated copies and adds bilingual visual documentation.

Run `python3 scripts/exportar-publico.py` at the package root to create a public tree and TAR.GZ alongside the project. The export includes icons, themes, cursors, code, and documentation. The xwinwrap binary copied from the source machine is excluded: the installer builds the pinned source in `vendor/xwinwrap` on the destination machine. The exporter refuses to overwrite an existing destination.

Original license notices were recovered and preserved. Theme and cursor provenance were checked by file content; see [provenance](PROVENIENCIA.md), [raw data](PROVENIENCIA.json), and [credits](../CREDITOS.md). Individual authorship of some historical MOD CSS changes could not be established and is not attributed to this integration's authors.

### Before publishing

1. Review credits, `LICENSES/`, and ORIGIN.txt files. Do not remove upstream attribution or replace third-party licenses with the root license.
2. Review staged files and run `python3 tests/test_public.py` and `python3 tests/test_install.py`.
3. For future installer/runtime changes, repeat the full cycle in a Mint 22.3 Cinnamon X11 VM, with reboots and before/after file and preference comparison. Isolated tests complement, rather than replace, that graphical session.
4. Make new screenshots in a clean account without personal photos, documents, or network locations. Mark illustrations and sample data clearly.
5. Review the diff and exclusions, run tests, generate the TAR.GZ using `python3 scripts/empacotar.py`, and publish it with its SHA-256 checksum file. Never upload `assets-locais/`, personal media, or user profiles. The theme scripts do not publish anything automatically.

Release assets should preserve symlinks and include SHA-256 checksums. Suggested description: “Gruvbox for Linux Mint Cinnamon: colorful icons, panel, Rain, and independent workspaces.” Prefer the supplied TAR.GZ for installation over GitHub's automatic ZIP, which may not preserve symlinks appropriately.

The integration uses GPL-3.0-or-later; third-party components retain their own licenses. Describe compatibility using the environments actually tested.

---

## Português

**Versão atual: 1.1.0 inclui o gerenciador GTK e retira Radio3. Em uma cópia pública preparada, execute `python3 scripts/empacotar.py` para gerar TAR.GZ versionado, somas e relatório. Execute os testes de mecanismo/GTK da GUI além das verificações existentes. Confira dados privados no pacote antes de enviar. O fluxo abaixo descreve a criação de outra árvore pública a partir de uma árvore de origem; ele recusa um destino existente.**

Repositório público: https://github.com/82py/gruvbox-cinnamon-completo

A primeira publicação, v1.0.1, permanece como pré-lançamento histórico. A v1.0.2 incorpora as correções encontradas e a validação completa em uma VM Mint 22.3 Cinnamon X11; veja VALIDACAO-VM.md.

Execute `python3 scripts/exportar-publico.py` para criar uma árvore pública e um TAR.GZ ao lado deste projeto. A exportação inclui ícones, temas, cursor, código e documentação. O binário xwinwrap copiado da máquina de origem fica fora: o instalador compila o fonte fixado em `vendor/xwinwrap` no computador de destino.

Os avisos dos projetos de origem foram recuperados e preservados. A proveniência do tema e do cursor foi conferida por conteúdo; veja `docs/PROVENIENCIA.json` e `CREDITOS.md`. A autoria individual de algumas alterações históricas do CSS da variante MOD não foi estabelecida e não é atribuída aos autores desta integração.

### Antes do envio

1. Confira `CREDITOS.md`, os avisos em `LICENSES/` e os arquivos ORIGIN.txt. Não remova os créditos dos autores originais ou substitua licenças de terceiros pela licença da raiz.
2. Confira os arquivos preparados e execute `python3 tests/test_public.py` e `python3 tests/test_install.py`.
3. Para futuras alterações de instalação/runtime, repita o ciclo em uma VM Mint 22.3 Cinnamon X11, com reinicializações e comparação de arquivos/preferências. Os testes isolados complementam essa sessão gráfica; não a substituem.
4. Produza capturas novas numa conta limpa, sem foto, documentos ou locais de rede pessoais.
5. Para novas versões, confira o diff e as exclusões, execute os testes, gere o TAR.GZ com `python3 scripts/empacotar.py` e publique com sua assinatura SHA-256. Nunca envie `assets-locais/`, mídias ou perfis pessoais. Nenhum envio é realizado pelos scripts do tema.

Releases: disponibilizar TAR.GZ com links simbólicos preservados e SHA-256. Descrição sugerida: “Gruvbox para Linux Mint Cinnamon: ícones coloridos, painel, Rain e espaços independentes”. O GitHub pode gerar ZIPs de código sem conservar adequadamente os links; prefira o TAR.GZ fornecido pelo projeto para instalação.

A integração usa GPL-3.0-or-later. Componentes de terceiros conservam suas licenças específicas. Descrever a compatibilidade pelas especificações efetivamente testadas.
