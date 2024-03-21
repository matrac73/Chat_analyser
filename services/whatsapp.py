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
    messages_in_morning = whatsapp.messages_in_morning(users)
    messages_in_night = whatsapp.messages_in_night(users)
    start_conversation = whatsapp.start_conversation(users)
    end_conversation = whatsapp.end_conversation(users)
    unique_words = whatsapp.unique_words(users)
    average_response_time = whatsapp.average_response_time(users)

    return total_messages, media_shared, emojis_sent, links_shared, df_utilisateurs, image_messages_users, image_proportion_users, messages_in_morning, messages_in_night, start_conversation, end_conversation, unique_words, average_response_time
