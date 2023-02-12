from modules.audio import record, process
from modules.google import cloud

# Iniciar conversa
cloud.text_to_wav("pt-BR-Neural2-A",
                  "Boa tarde Gabriel,"
                   "Tudo bem com você? aqui é da imobiliária Casa dos sonhos, em que posso te ajudar? as opções são: Vendas, Aluguel, Administrativo e Financeiro"
                  )

process.executar_audio_gerado()

resposta = {"finalizar": False}

while resposta["finalizar"] == False:
    resposta = process.identificar_resposta(cloud.transcribe_speech(record.write_audio(3)))
    cloud.text_to_wav("pt-BR-Neural2-A", resposta["resposta"])
    process.executar_audio_gerado()
