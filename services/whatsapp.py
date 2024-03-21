from utils.utils import Whatsapp

whatsapp = Whatsapp()


def analyze_chat_whatsapp(chat_file):
    chat_content = whatsapp.read_chat_file(chat_file)

    users, total_messages = whatsapp.count_messages_per_user(chat_content)
    media_shared = whatsapp.count_media(chat_content)
    emojis_sent = whatsapp.count_emojis(chat_content)
    links_shared = whatsapp.count_links(chat_content)
    df_utilisateurs = whatsapp.create_dataframe(users)
    image_messages_users = whatsapp.display_messages_users(chat_content)
    image_proportion_users = whatsapp.plot_nested_pie(chat_content)

    return total_messages, media_shared, emojis_sent, links_shared, df_utilisateurs, image_messages_users, image_proportion_users
