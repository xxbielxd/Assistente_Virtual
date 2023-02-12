import tkinter as tk
from tkinter import ttk
from modules.audio import record, process
from modules.google import cloud
import asyncio

event = asyncio.get_event_loop()
class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show()
class Window(tk.Tk):
    def __init__(self, loop):
        self.loop = loop
        self.root = tk.Tk()
        self.em_ligacao = False
        self.label = tk.Label(text="Clique abaixo para ligar para a nossa central")
        self.label.grid(row=0, columnspan=2, padx=(8, 8), pady=(16, 0))
        self.button_block = tk.Button(text="Ligar", width=10, command=lambda: self.loop.create_task(self.ligar()))
        self.button_block.grid(row=2, column=1, sticky=tk.W, padx=8, pady=8)

    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(.1)
    async def ligar(self):
        global em_ligacao
        print("entrei")
        if (self.em_ligacao):
            return False

        self.button_block["state"] = "disabled"
        self.button_block["text"] = "Em Ligação"
        self.em_ligacao = True

        self.label["text"] = "Vamos Começar"

        await asyncio.sleep(.1)

        cloud.text_to_wav("pt-BR-Neural2-A",
                            "Boa tarde Gabriel,"
                            "Tudo bem com você? aqui é da imobiliária Casa dos sonhos, em que posso te ajudar? as opções são: Vendas, Aluguel, Administrativo e Financeiro"
                          )
        process.executar_audio_gerado()

        await asyncio.sleep(.1)

        resposta = {"finalizar": False}

        while resposta["finalizar"] == False:

            self.label["text"] = "Estou ouvindo..."
            await asyncio.sleep(.1)
            audio = record.write_audio(3,self.label)
            await asyncio.sleep(.1)
            resposta = process.identificar_resposta(cloud.transcribe_speech(audio))
            cloud.text_to_wav("pt-BR-Neural2-A", resposta["resposta"])
            process.executar_audio_gerado()

        self.button_block["state"] = "normal"
        self.button_block["text"] = "Ligar"
        self.em_ligacao = False
        self.label["text"] = "Você foi tranferido para a area: " + resposta["area"]


asyncio.run(App().exec())