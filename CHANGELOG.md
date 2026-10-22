# Alterações

## 1.0.3 — 21/10/2026

- Documentação dos compactados atualizada: README bilíngue (inglês primeiro), apresentação visual com ícones reais, catálogo das 25 cores de pastas e agradecimentos nominais e aviso de responsabilidade após a nota de vibe coding. Código instalado e preferências permanecem iguais.

- A janela “Copiar para outra área…” aberta pelo menu do Nemo agora executa uma única operação por seleção. Os destinos ficam bloqueados durante a cópia; no sucesso, a janela fecha e solicita uma notificação.
- Seleções concluídas são consumidas. Cliques adicionais, inclusive após uma falha parcial, não criam cópias duplicadas dos itens que já foram copiados. Erros continuam sendo apresentados antes do fechamento.
- O modo independente de arrastar arquivos continua aceitando novas operações deliberadas.
- Quatro testes GTK de regressão cobrem cliques repetidos, falha parcial, modo de arraste e ausência do serviço de notificações. Nenhum arquivo pessoal é usado nos testes.
- Mantida a validação completa de instalação e desinstalação em VM da 1.0.2 como evidência histórica; esse ciclo completo não foi repetido para a 1.0.3.

## 1.0.2 — 21/10/2026

- Instalação e desinstalação reais em VM Mint 22.3 Cinnamon X11, com reinicializações e comparação de 115 destinos, 936 preferências e arquivos internos.
- Verificação das versões dos espaços já no primeiro ciclo de boot.
- Saídas incorporadas GPU/X11 e confirmação de vídeo pronto antes da seleção do modo Rain.
- Áudio próprio Rain/vídeo via compatibilidade PulseAudio, evitando a captura do player pela Radio3 sem modificar o applet.
- Captura de todas as preferências antes das alterações; desligamento dos componentes antes da restauração dos arquivos.
- Encerramento da janela e da bandeja próprias do Rain na desinstalação.
- Regressões para boot antecipado e sincronização entre schemas, evidências e capturas da VM.

## 1.0.1 — 2026-10-21

- Auditoria dos componentes realmente carregados, do menu e das preferências atuais.
- Incluídos Relax, o perfil visual isolado do terminal, Fontconfig de KClock/Materialgram e a organização da categoria Chromium.
- Exportadas 936 preferências explícitas; sincronizadas as cópias locais dos temas Mint.
- Preservado o preset público da Radio3 e completadas suas dependências e as do controle auxiliar de volume do Rain.
- Mesclagem de preferências de aplicativos e inicialização condicional de Insync/Bitwarden.

## 1.0.0 — 2026-10-21

- Captura da personalização ativa de Pir (82py), com cópia dos ícones aprovados e variante de sistema colorida.
- Portabilidade dos caminhos, Rain e espaços independentes sem mídias ou dados pessoais.
- Instalador e restaurador com cópias de segurança e registro individual das preferências.
- Estrutura para GitHub, créditos, separação de componentes pendentes de licença e análise do Ubuntu.

### Complemento do seletor de pastas

- Incluídos os dois SH da pasta pessoal, menu no Iniciar e créditos a akarzim.
- O auxiliar usa variantes A/B próprias e mantém os temas originais intactos.
- Compatibilidade verificada a partir dos próprios TAR.GZ: todas as cores, resolução/renderização GTK, restauração, falha simulada, conflitos e desinstalação.
