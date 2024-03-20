from utils.utils import Whatsapp


def analyze_chat_whatsapp(chat_file):
    chat_content = Whatsapp.read_chat_file(chat_file)

    total_messages, users = Whatsapp.count_messages_per_user(chat_content)
    media_shared = Whatsapp.count_media(chat_content)
    emojis_sent = Whatsapp.count_emojis(chat_content)
    links_shared = Whatsapp.count_links(chat_content)

    df_utilisateurs = Whatsapp.create_dataframe(users)

    return total_messages, media_shared, emojis_sent, links_shared, df_utilisateurs
