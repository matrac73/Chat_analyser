import re
import pandas as pd


class Whatsapp():

    def read_chat_file(chat_file):
        with open(chat_file, 'r', encoding='utf-8') as file:
            chat_content = file.readlines()
        return chat_content

    def count_media(chat_content):
        media_pattern = r'<Médias omis>'
        media_shared = sum(1 for line in chat_content if re.search(media_pattern, line))
        return media_shared

    def count_emojis(chat_content):
        emoji_pattern = (
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF'
            r'\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF'
            r'\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF'
            r'\U00002702-\U000027B0\U000024C2-\U0001F251]+'
            )
        emojis_sent = sum(len(re.findall(emoji_pattern, line)) for line in chat_content)
        return emojis_sent

    def count_links(chat_content):
        link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        links_shared = sum(len(re.findall(link_pattern, line)) for line in chat_content)
        return links_shared

    def count_messages_per_user(chat_content):
        users = {}
        total_messages = 0
        for line in chat_content:
            total_messages += 1
            match = re.match(r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.+)', line)
            if match:
                user = match.group(2)
                users[user] = users.get(user, 0) + 1
        return total_messages, users

    def create_dataframe(users):
        df_utilisateurs = pd.DataFrame({'Noms': list(users.keys()), 'Messages': list(users.values())})
        return df_utilisateurs
