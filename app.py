import gradio as gr
from services.whatsapp import analyze_chat_whatsapp


def interface_calculateur():
    inputs = [
            gr.components.File(label="Fichier", file_count='single')
            ]
    outputs = [
            gr.components.Number(label='Messages totaux envoyés'),
            gr.components.Number(label='Medias partagés'),
            gr.components.Number(label='Emojis envoyés'),
            gr.components.Number(label='Liens partagés'),
            gr.components.Dataframe(label="messages par utilisateur"),
            gr.components.Image(label="Timeline"),
            gr.components.Image(label="proportion"),
            ]

    return gr.Interface(
        analyze_chat_whatsapp,
        inputs=inputs,
        outputs=outputs,
        css="footer {visibility: hidden}",
        allow_flagging="never",
        submit_btn="Calculer",
        clear_btn="Effacer"
        )


interfaces = [
    interface_calculateur()
]


demo = gr.TabbedInterface(
    interface_list=interfaces,
    tab_names=["Analyser"],
    css="footer {visibility: hidden}",
    title="Chat Analyser",
    theme=gr.themes.Base()
    )

demo.launch(favicon_path="data/favicon.ico")
# demo.launch(favicon_path="./data/favicon.ico", share=True)
