# Uninstall and restore / Desinstalar e restaurar

[English](#english) · [Português](#português)

## English

In the extracted package folder, run `bash desinstalar.sh` as your regular user, without sudo. You can also use the installed command:

```sh
"$HOME/.local/bin/gruvbox-desinstalar"
```

The uninstaller stops the workspace service and Rain, restores previous files, and restores each changed preference individually. Values that were previously unset become unset again; it does not clear entire preference trees.

Installed files modified after installation are copied to `alterados-DATE` inside `$HOME/.local/state/gruvbox-cinnamon` before restoration. The journal and previous backups remain in that state directory.

**Workspace folders and documents are never deleted**, including files created after installation. The previous Desktop folder path is restored. Log out and back in so Nemo and Cinnamon reload the previous setup.

The command does not remove system dependencies, images or videos you selected, third-party applications, or accounts. Do not run it for another user or as root.

The terminal appearance profile, Fontconfig preferences, and merged menu files have their previous versions saved in the same journal. Later modifications to those files and the folder-color variants are preserved in the recovery directory before restoration. Application binaries and their original data remain untouched.

---

## Português

Na pasta extraída, execute `bash desinstalar.sh`, sem sudo. Há também o comando instalado:

```sh
"$HOME/.local/bin/gruvbox-desinstalar"
```

O desinstalador para o serviço dos espaços e o Rain, devolve os arquivos anteriores e restaura individualmente os valores de configuração alterados. Valores antes não definidos voltam a não estar definidos; nenhuma árvore inteira de preferências é apagada.

Arquivos instalados que tenham sido modificados depois da instalação são copiados para `alterados-DATA` dentro de `$HOME/.local/state/gruvbox-cinnamon` antes da restauração. Os registros e as cópias anteriores continuam guardados nessa pasta.

**As pastas e os documentos dos espaços nunca são apagados**, inclusive arquivos criados depois da instalação. O caminho anterior da Área de Trabalho é restaurado. Encerre a sessão e entre novamente para que Nemo e Cinnamon recarreguem o estado anterior.

O comando não remove dependências do sistema, imagens/vídeos que você escolheu, aplicativos de terceiros nem contas. Não execute sobre outra conta de usuário ou como root.

O perfil visual do terminal, as preferências Fontconfig e as mesclagens de menu têm os arquivos anteriores guardados no mesmo registro. Alterações posteriores nesses arquivos e nas variantes de pastas são preservadas na recuperação antes da restauração. Os binários dos aplicativos e seus dados originais permanecem intocados.
