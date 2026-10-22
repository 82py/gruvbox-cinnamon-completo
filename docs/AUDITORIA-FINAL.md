# Conferência final da personalização ativa — 21/10/2026

Conferência histórica da revisão 1.0.2. A 1.0.3 atualiza somente o utilitário de cópia e seus testes/documentação; veja VALIDACAO-COPIA.json. A conferência leu o estado do Cinnamon e comparou os arquivos ativos com as duas árvores de distribuição. Nada foi aplicado na sessão real da máquina de origem; a instalação completa foi exercitada em uma VM separada.

| Componente ativo | Cobertura |
| --- | --- |
| Gruvbox Plus e Sistema Colorido | Arquivos e links comparados; nenhuma arte ausente ou diferente. |
| Tema visual, GTK, janelas e cursor | Cópias locais incluídas; os dois CSS locais Mint foram sincronizados. |
| 15 applets do painel | 14 fornecidos pelo Cinnamon; Radio3 completa no pacote. Preferências de instância incluídas. |
| Cinco extensões em execução | Magic Lamp e quatro extensões da personalização incluídas; UUIDs pessoais tornados genéricos. |
| Menu Iniciar | 180 entradas inventariadas por CMenu, sem copiar comandos privados; categoria Chromium preservada por mesclagem. |
| Rain | GUI, bandeja, controle deslizante, iniciar/parar, volume auxiliar, sessão, wrapper e código de vídeo incluídos. |
| Quatro espaços | Serviço, pastas independentes, fundos por espaço e cópia entre áreas incluídos. |
| Seletor de pastas | Dois SH, motor, menu e variantes A/B incluídos; temas originais preservados. |
| Relax | Atalho incluído; escolhe vídeo local e mantém reprodução em tela cheia via Celluloid, com alternativa mpv. |
| Terminal padrão | Perfil visual ativo exportado para configuração separada, sem comandos pessoais; ambiente normal devolvido aos processos filhos. |
| Fontes em aplicativos Flatpak | Fontconfig de KClock e Materialgram incluídos, com mesclagem dos overrides existentes. |
| Preferências | 936 valores explícitos de aparência, painel, menus, janelas, teclado, atalhos, gestos, Nemo e temas. |
| Inicialização | Rain e espaços incluídos; Insync/Bitwarden condicionados à presença dos programas. As duas entradas já desativadas permanecem desativadas. |
| Ações Nemo | Seis ações e seus auxiliares incluídos; Timo continua sendo dependência externa. Sem scripts de Nemo, desklets ou provedores de pesquisa pessoais ativos. |

## O que a conferência acrescentou

Relax, o perfil visual do terminal, duas configurações Fontconfig, a categoria Chromium, valores padrão antes implícitos, os CSS locais Mint e dependências da Radio3/controle auxiliar de volume. O preset público JB FM foi mantido; o histórico e as pesquisas continuam excluídos.

## Exclusões deliberadas

Não são um esquecimento: vídeos, imagens de fundo, foto de perfil, documentos dos espaços, contas, credenciais, registros, localização geográfica e histórico. Os espaços começam com fundo sólido até a escolha de mídia pelo destinatário. O primeiro espaço reutiliza sua Área de Trabalho existente; os demais são criados vazios.

Binários de aplicativos de terceiros, seus perfis/contas e serviços pessoais de servidores, tarefas, VPN ou sincronização não são um tema Cinnamon. Seus ícones são incluídos, e o menu os identifica como dependências externas. Não foram copiadas integrações com servidores pessoais. As associações MIME estão apenas como referência opcional.

Os instaladores/restauradores antigos de áreas, datados e vinculados ao estado anterior da máquina de origem, são substituídos pelo instalador, desinstalador e controles portáteis do novo pacote. Não se distribuem cópias antigas de vídeos nem backups de documentos para reproduzi-los.

## Verificação e limites

A comparação de cobertura é reproduzível com `python3 scripts/auditar-desktop.py` enquanto a máquina de origem mantiver esta configuração. As adaptações intencionais são enumeradas em `AUDITORIA-COBERTURA.json`.

A instalação/restauração e o seletor são testados em HOME e preferências isolados. Os dois arquivos finais são extraídos para testar as 25 cores e a resolução/renderização GTK dos ícones. O terminal real também foi iniciado sem janela visível e em barramento privado: carregou o perfil exportado, executou o comando de teste e preservou os dados originais. A revisão 1.0.2 também foi instalada e desinstalada em uma segunda sessão Cinnamon real, dentro de uma VM Mint 22.3. A restauração foi conferida antes e depois de reiniciar: nenhuma diferença nos 115 destinos, nas 936 preferências e nos três conjuntos de arquivos internos comparados. Consulte VALIDACAO-VM.md.
