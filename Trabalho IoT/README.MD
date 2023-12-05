# Estacionamento Inteligente - Projeto Final IoT
Este projeto se baseia no conceito de um estacionamento inteligente, onde um conjunto de sensores em um estacionamento indica para o usuário a disponibilidade de vagas.

## Sobre
O intuito do projeto é que o usuário consulte e até mesmo reserve vagas antes de estacionar, para economizar o tempo e gasolina gastos ao procurar uma vaga. A comunicação entre sensores e aplicativo funciona por MQTT. No protótipo do aplicativo, o usuário tem controle completo do estado da vaga.

### Tecnologias Utilizadas
* **NodeMCU (ESP8266)**: O ESP8266 é usado para coletar os dados dos sensores ultrassônicos e enviar via MQTT para o broker. Ele também é responsável por controlar os LEDs que indicam o estado da vaga.
* **MQTT**: O MQTT foi utilizado como protocolo de comunicação entre o ESP8266 e o aplicativo Python.
* **Python**: O aplicativo do usuário foi programado em Python, utilizando a biblioteca para criação de interfaces gráficas TKinter.


## Montagem
[O protótipo do circuito está disponível pelo TinkerCad.](https://www.tinkercad.com/things/em7qJfiqkgs-epic-kup?sharecode=uP8d6hj8rrVXdLQXbamtVZ1Qe503zD-5Gjr1E3Qy0PQ)

## Instalação
Abra a pasta que deseja instalar pelo terminal, e clone o repositório:
```
git clone https://github.com/GualterMM/C115_Repositorio.git
```
O projeto se encontra na pasta "Projeto IoT".

### ESP8266
Configure a IDE do Arduino para programar no ESP8266. Considerando a montagem acima, suba o código para o CI.

### Python

No terminal, crie um ambiente virtual utilizando o comando:
```
python -m venv '.\venv'
```

Ative o ambiente virtual:
```
.\venv\Scripts\activate
```

Instale as dependências do projeto:
```
pip install -r requirements
```

Execute a aplicação:
```
python app.py
```

### Equipe de Desenvolvimento

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/GualterMM">
        <img src="https://avatars.githubusercontent.com/u/35864822?v=4" width="100px;" alt="Foto do Gualter Machado no GitHub"/><br>
        <sub>
          <b>Gualter Machado</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/IsabelaRezendeB">
        <img src="https://avatars.githubusercontent.com/u/49520751?v=4" width="100px;" alt="Foto da Isabela Rezende no GitHub"/><br>
        <sub>
          <b>Isabela Rezende</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
