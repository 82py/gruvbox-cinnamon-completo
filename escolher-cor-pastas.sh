#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHOOSER="$SCRIPT_DIR/folders-color-chooser.sh"

if [[ ! -x "$CHOOSER" ]]; then
    echo "Erro: não encontrei o script executável:"
    echo "$CHOOSER"
    read -rp "Pressione Enter para sair..."
    exit 1
fi

while true; do
    clear
    echo "======================================"
    echo "   Escolher cor das pastas - Gruvbox"
    echo "======================================"
    echo
    echo "Cores disponíveis:"
    echo " 1) black       2) blue        3) caramel     4) citron"
    echo " 5) firebrick   6) gold        7) green       8) grey"
    echo " 9) highland   10) jade       11) lavender   12) lime"
    echo "13) olive      14) orange     15) pistachio  16) plasma"
    echo "17) pumpkin    18) purple     19) red        20) rust"
    echo "21) sapphire   22) tomato     23) violet     24) white"
    echo "25) yellow"
    echo
    echo " 0) Voltar para o padrão (plasma)"
    echo " r) Restaurar a aparência anterior ao seletor"
    echo " q) Sair"
    echo
    read -rp "Digite o número da cor desejada: " opcao

    case "$opcao" in
        1) cor="black" ;;
        2) cor="blue" ;;
        3) cor="caramel" ;;
        4) cor="citron" ;;
        5) cor="firebrick" ;;
        6) cor="gold" ;;
        7) cor="green" ;;
        8) cor="grey" ;;
        9) cor="highland" ;;
        10) cor="jade" ;;
        11) cor="lavender" ;;
        12) cor="lime" ;;
        13) cor="olive" ;;
        14) cor="orange" ;;
        15) cor="pistachio" ;;
        16) cor="plasma" ;;
        17) cor="pumpkin" ;;
        18) cor="purple" ;;
        19) cor="red" ;;
        20) cor="rust" ;;
        21) cor="sapphire" ;;
        22) cor="tomato" ;;
        23) cor="violet" ;;
        24) cor="white" ;;
        25) cor="yellow" ;;
        0)
            echo
            "$CHOOSER" -C
            read -rp "Pressione Enter para continuar..."
            continue
            ;;
        r|R)
            "$CHOOSER" --restore
            read -rp "Pressione Enter para continuar..."
            continue
            ;;
        q|Q)
            exit 0
            ;;
        *)
            echo "Opção inválida."
            sleep 1
            continue
            ;;
    esac

    echo
    "$CHOOSER" -c "$cor"
    read -rp "Pressione Enter para continuar..."
done
