# 💪 Heavy – Gerenciador de Treinos

Projeto desenvolvido por **Tiago Geovane** para a disciplina **Orientação a Objetos (01/2025)**  
Faculdade UnB Gama — Prof. Henrique Moura

---

## 🎯 Objetivo

O **Heavy** é um sistema de gerenciamento de treinos físicos. Ele permite que o usuário crie, edite, visualize e remova treinos compostos por exercícios personalizados, com informações como nome, carga (peso) e número de repetições. O sistema possui uma interface gráfica amigável e armazena os dados localmente em arquivos JSON.

---

## ✅ Casos de Uso

### 1. Criar Novo Treino
- O usuário digita um nome.
- O sistema cria o treino e permite adicionar exercícios.

### 2. Adicionar Exercícios
- O usuário insere nome, peso (kg) e repetições (x).
- O exercício é salvo no treino correspondente.

### 3. Editar Treino
- O usuário digita o nome do treino.
- O sistema permite renomear o treino ou editar os exercícios.
- Se o usuario colocar o nome de um exercicio que não exista no treino, o sistema edita o exercicio, caso contrario adiciona ele ao treino

### 4. Listar Treinos
- O sistema mostra todos os treinos salvos e seus respectivos exercícios.

### 5. Remover Treino
- O usuário digita o nome do treino.
- O sistema solicita confirmação e exclui o treino e seus dados.

---



