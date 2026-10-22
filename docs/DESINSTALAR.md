# Desinstalar e restaurar

Na pasta extraída, execute `bash desinstalar.sh`, sem sudo. Há também o comando instalado:

```sh
"$HOME/.local/bin/gruvbox-desinstalar"
```

O desinstalador para o serviço dos espaços e o Rain, devolve os arquivos anteriores e restaura individualmente os valores de configuração alterados. Valores antes não definidos voltam a não estar definidos; nenhuma árvore inteira de preferências é apagada.

Arquivos instalados que tenham sido modificados depois da instalação são copiados para `alterados-DATA` dentro de `$HOME/.local/state/gruvbox-cinnamon` antes da restauração. Os registros e as cópias anteriores continuam guardados nessa pasta.

**As pastas e os documentos dos espaços nunca são apagados**, inclusive arquivos criados depois da instalação. O caminho anterior da Área de Trabalho é restaurado. Encerre a sessão e entre novamente para que Nemo e Cinnamon recarreguem o estado anterior.

O comando não remove dependências do sistema, imagens/vídeos que você escolheu, aplicativos de terceiros nem contas. Não execute sobre outra conta de usuário ou como root.

O perfil visual do terminal, as preferências Fontconfig e as mesclagens de menu têm os arquivos anteriores guardados no mesmo registro. Alterações posteriores nesses arquivos e nas variantes de pastas são preservadas na recuperação antes da restauração. Os binários dos aplicativos e seus dados originais permanecem intocados.
