### O que foi pedido?

Gerar um texto, em português, como se fosse um atendente virtual de uma imobiliária.

Através da sintetização do texto, a AV precisa dizer ao cliente que está “ligando” o que ele pode pedir. 

São quatro áreas obrigatórias:
Vendas
Aluguel
Administrativo
Financeiro

Com o microfone, a pessoa responde uma dessas áreas e através de alguma das funções de reconhecimento de áudio, a área deverá ser identificada e, novamente por sintetização de voz, deverá gerar um áudio indicando que a ligação será transferida para a área correspondente. Por exemplo: “Ótimo, vou transferir você para um de nossos corretores de vendas.”

Deve estar em um loop. E deve haver uma palavra-chave para encerrar o loop. 

Entregar:
Texto descrevendo o problema e a solução desenvolvida
Código em Python
Link para vídeo demonstrando a execução do programa

### O que foi utilizado?

- Google cloud, usamos os serviços texttospeech, speechtotext e bucket 
- sounddevice, uma ferramenta no python que nos ajudou a gravar os áudios em WAV
- base64, componente que nos permitiu converter os audios para base64, assim conseguimos mandar o áudio diretamente, sem precisar enviar para o bucket antes
- JSON, usamos esse componente para ler o arquivo JSON que contém todas as opções possíveis da nossa aplicação ( data/areas.json )
- asyncio, utilizamos para nos ajudar em algumas funções que criamos assync.
- tkinter, ferramenta que utilizamos para fazer uma tela simples da aplicação.

### Instruções 

A aplicação pode ser executada via console no arquivo "init.py", ou executando o arquivo Tela.py, onde criamos uma tela simples, para facilitar a execução. 

Para adicionar novas opções, deve-se alterar o arquivo "data/areas.json".

Atualmente, quando a assistente está escutando, configuramos 3 segundo, mas é possível alterar esse tempo no código, ou futuramente adicionar uma detecção de voz.

Deve-se ser configurado o nome do projeto na google cloud e ativado os serviços, para que a aplicação funcione corretamente "config.py".
