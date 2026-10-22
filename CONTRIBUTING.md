# Contributing / Contribuir

[English](#english) · [Português](#português)

## English

Open an issue with your Cinnamon version, session type, and steps to reproduce the problem. Do not submit personal photos, videos, wallpapers, documents, or logs containing sensitive information. Icon proposals should keep the subject recognizable and identify the source and license of the artwork. System icons use varied Gruvbox colors while avoiding pink; application icons retain the existing visual approvals.

Integration changes must preserve per-user installation and restoration without deleting workspace files. Run `python3 tests/test_public.py`; also run `python3 tests/test_install.py` in an isolated environment for the complete package. The copy-dialog regression tests run with `xvfb-run -a /usr/bin/python3 tests/test_copy_dialog.py` when GTK, its introspection bindings, and Xvfb are installed.

---

## Português

Abra uma issue com versão do Cinnamon, tipo de sessão e reprodução do problema. Não envie fotos, vídeos, fundos, documentos pessoais ou logs com dados sensíveis. Propostas de ícones devem preservar a forma reconhecível e explicar a origem/licença do desenho. Ícones de sistema usam cores Gruvbox variadas evitando rosa; ícones de aplicativos preservam as aprovações visuais existentes.

Mudanças de integração devem conservar instalação por usuário e restauração sem apagar arquivos dos espaços. Execute `python3 tests/test_public.py`; para o pacote completo, execute também `python3 tests/test_install.py` em ambiente isolado.
