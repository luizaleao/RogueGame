# RogueGame
# Sky Jumper

Um pequeno jogo de plataforma 2D desenvolvido com [Pygame Zero](https://pygame-zero.readthedocs.io/en/stable/).

## 🎮 Sobre o Jogo

Sky Jumper é um jogo onde o objetivo é pular entre plataformas, evitar inimigos e alcançar a plataforma mais alta da tela. Se o jogador colidir com um inimigo, o jogo exibe uma mensagem de **Game Over** e retorna ao menu. Se o jogador alcançar a plataforma final, recebe a mensagem **You Win!**.

## 🕹️ Controles

- `←` ou `→`: move o personagem para os lados
- `Espaço`: pular

## 🧠 Lógica do Jogo

- O jogador começa em uma plataforma inferior.
- Existem múltiplas plataformas distribuídas em diferentes alturas.
- Inimigos patrulham determinadas plataformas.
- Ao tocar um inimigo, o jogador perde.
- Ao alcançar a plataforma mais alta, o jogador vence.

## 🚀 Como Rodar

1. Instale o **Pygame Zero**:
   ```bash
   pip install pgzero
   
2.Navegue até a pasta onde está o arquivo game.py.

Execute o jogo com o seguinte comando:

 ```bash
pgzrun game.py

Importante: Use pgzrun e não python game.py.
