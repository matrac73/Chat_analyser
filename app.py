import gradio as gr
from services.whatsapp import analyze_chat


def interface_calculateur():
    inputs = [
            gr.components.File(label="Fichier")
            ]
    outputs = [
            gr.components.Dataframe(label="Informations")
            ]

    return gr.Interface(
        analyze_chat,
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
