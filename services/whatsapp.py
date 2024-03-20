import re
import pandas as pd


def analyze_chat(chat_file):
    with open(chat_file, 'r', encoding='utf-8') as file:
        chat_content = file.readlines()

    # Initialize variables
    users = {}
    total_messages = 0
    media_shared = 0
    emojis_sent = 0
    links_shared = 0

    # Regex patterns for detecting media, emojis, and links
    media_pattern = r'<Médias omis>'
    emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+'
    link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Loop through each line in the chat
    for line in chat_content:
        total_messages += 1

        # Detect media
        if re.search(media_pattern, line):
            media_shared += 1

        # Detect emojis
        emojis_sent += len(re.findall(emoji_pattern, line))

        # Detect links
        links_sent = re.findall(link_pattern, line)
        links_shared += len(links_sent)

        # Extract user and message
        match = re.match(r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.+)', line)
        if match:
            user = match.group(2)
            message = match.group(3).strip()

            # Update user message count
            if user in users:
                users[user] += 1
            else:
                users[user] = 1

    # Print statistics
    output = {}
    output["Total messages"] = total_messages
    output["Media shared:"] = media_shared
    output["Emojis sent:"] = emojis_sent
    output["Links shared:"] = links_shared
    utilisateurs = []
    for user, count in users.items():
        utilisateurs.append((user, count))
    output["Messages per user:"] = utilisateurs

    return pd.DataFrame(output)
