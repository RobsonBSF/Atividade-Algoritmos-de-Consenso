# Atividade-Algoritmos-de-Consenso
## Descrição do Projeto

Este projeto implementa uma simulação do algoritmo de consenso **Raft**, utilizado em sistemas distribuídos para garantir a consistência e integridade dos dados em uma rede descentralizada. O Raft é um algoritmo de consenso projetado para ser compreensível e eficaz, com um líder responsável por coordenar a replicação de logs entre os nós participantes da rede.

A implementação simula um ambiente distribuído onde múltiplos nós participam de eleições, replicam logs e tomam decisões sobre o estado do sistema. Além disso, falhas e recuperação de nós são simuladas para testar a resiliência do sistema.

### Algoritmo Raft
O algoritmo Raft funciona com três estados principais dos nós:
- **Follower**: O nó segue as instruções do líder, aguardando comandos e registros.
- **Candidate**: O nó inicia uma eleição para tentar se tornar o líder, caso o atual líder falhe.
- **Leader**: O nó coordena as operações, como a proposta de entradas de log, e mantém os seguidores atualizados.

## Instruções para Configurar o Ambiente

### Pré-requisitos
Para executar este código, você precisará de:
- **Python 3.x** instalado.
- **Bibliotecas padrão**: Este projeto usa apenas bibliotecas padrão do Python, portanto não há necessidade de instalar dependências externas.

### Passos para Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/RobsonBSF/Atividade-Algoritmos-de-Consenso.git
   cd Atividade-Algoritmos-de-Consenso
   ```

2. **Execute o código**:
   O código pode ser executado diretamente no terminal com o seguinte comando:
   ```bash
   python Raft.py
   ```

3. **Saída Esperada**:
   O código irá imprimir no terminal as mensagens de log detalhadas sobre as ações dos nós, como eleições, envio de batimentos cardíacos, e propostas de logs.

## Explicação das Fases do Algoritmo Raft

O Raft consiste nas seguintes fases principais:

### 1. **Eleição de Líder**
   - **Objetivo**: Garantir que apenas um líder seja responsável por coordenar as operações e manter a consistência entre os nós.
   - **Processo**:
     - Quando um nó começa a operar, ele entra no estado de **Seguidor**.
     - Se um nó não recebe batimentos cardíacos do líder em um intervalo de tempo aleatório, ele se torna um **candidato** e inicia uma eleição.
     - O **candidato** envia um pedido de voto para todos os outros nós na rede.
     - Os nós que recebem o pedido de voto respondem com um voto, se não tiverem votado em outro nó ou se o nó candidato for mais novo (maior termo).
     - O nó que receber a maioria dos votos se torna o novo **líder**.
   
### 2. **Replicação de Logs**
   - **Objetivo**: Garantir que todos os nós tenham logs consistentes e sincronizados.
   - **Processo**:
     - O **líder** cria entradas de log e as envia para os **seguidores**.
     - Os seguidores registram as entradas e, quando a maioria dos nós confirma a entrada de log, ela é considerada **comprometida**.
     - Quando uma entrada é comprometida, todos os nós aplicam a entrada ao seu estado local.

### 3. **Batimentos Cardíacos**
   - **Objetivo**: Manter a liderança e evitar novas eleições.
   - **Processo**:
     - O **líder** envia batimentos cardíacos periodicamente aos seguidores para garantir que eles continuem reconhecendo-o como o líder atual.
     - Caso os seguidores não recebam um batimento cardíaco dentro de um período de tempo específico, eles podem iniciar uma nova eleição.

## Descrição de Falhas Simuladas e Como o Sistema Responde

O sistema simula falhas de rede e de nós, e é projetado para lidar com essas falhas de maneira robusta. Aqui estão algumas falhas simuladas e as respostas do sistema:

### 1. **Falha de Comunicação (Timeout)**
   - **Descrição**: Se um nó não receber um batimento cardíaco do líder dentro do tempo limite, ele pode iniciar uma nova eleição, tentando se tornar o novo líder.
   - **Resposta**: O nó que não recebe o batimento se torna um **candidato** e inicia uma nova eleição. Caso ele receba votos suficientes, ele se torna o novo **líder**.

### 2. **Falha de Nó (Crash e Recuperação)**
   - **Descrição**: Um nó pode falhar (simulado por um nó que não responde a mensagens).
   - **Resposta**: O sistema detecta a falha pela ausência de batimentos cardíacos e, se necessário, um novo líder é eleito. Quando o nó falho recupera, ele pode se juntar à rede e sincronizar seus logs com o líder.

### 3. **Falha de Líder**
   - **Descrição**: Se o líder falha (não envia batimentos cardíacos ou não responde), um novo líder será eleito automaticamente pelos nós.
   - **Resposta**: Os nós detectam a falha do líder e iniciam uma eleição para eleger um novo líder, garantindo que o processo de consenso continue sem interrupções significativas.
