import re
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


class Whatsapp:

    def read_chat_file(self, chat_file):
        with open(chat_file, 'r', encoding='utf-8') as file:
            chat_content = file.readlines()
        return chat_content

    def count_media(self, chat_content):
        media_pattern = r'<Médias omis>'
        media_shared = sum(1 for line in chat_content if re.search(media_pattern, line))
        return media_shared

    def count_emojis(self, chat_content):
        emoji_pattern = (
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF'
            r'\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF'
            r'\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF'
            r'\U00002702-\U000027B0\U000024C2-\U0001F251]+'
            )
        emojis_sent = sum(len(re.findall(emoji_pattern, line)) for line in chat_content)
        return emojis_sent

    def count_links(self, chat_content):
        link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        links_shared = sum(len(re.findall(link_pattern, line)) for line in chat_content)
        return links_shared

    def count_messages_per_user(self, chat_content):
        users = {}
        total_messages = 0
        for line in chat_content:
            total_messages += 1
            match = re.match(r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.+)', line)
            if match:
                time_str = match.group(1)
                user = match.group(2)
                message = match.group(3)
                time = datetime.strptime(time_str, "%d/%m/%Y, %H:%M")
                users[user] = users.get(user, [])
                users[user].append((time, message))
        return users, total_messages

    def create_dataframe(self, users):
        sorted_users = sorted(users.items(), key=lambda x: len(x[1]) - 1, reverse=True)
        details_absolute = [len(user[1]) - 1 for user in sorted_users]
        total_messages = sum(details_absolute)
        details_percentage = [f"{(count / total_messages) * 100:.2f} %" for count in details_absolute]
        df_utilisateurs = pd.DataFrame({
            'Noms': [user[0] for user in sorted_users],
            'Compte absolu': details_absolute,
            'Compte relatif': details_percentage,
        })

        return df_utilisateurs

    def display_messages_users(self, chat_content):
        messages_per_user = self.count_messages_per_user(chat_content)

        sorted_users = sorted(messages_per_user[0].items(), key=lambda x: len(x[1]), reverse=True)

        data = []
        for user, messages in sorted_users:
            for time, _ in messages:
                data.append((user, time))

        df = pd.DataFrame(data, columns=['User', 'Time'])

        pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
        g = sns.FacetGrid(df, row="User", hue="User", aspect=15, height=1.5, palette=pal)

        echantillonage = 0.2
        g.map(sns.kdeplot, "Time", bw_adjust=echantillonage, clip_on=False, fill=True, alpha=1, linewidth=1.5)
        g.map(sns.kdeplot, "Time", clip_on=False, color="w", lw=2, bw_adjust=echantillonage)
        g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

        def label(x, color, label):
            ax = plt.gca()
            ax.text(0, .2, label, fontweight="bold", color=color,
                    ha="left", va="center", transform=ax.transAxes)

        g.map(label, "Time")
        g.figure.subplots_adjust(hspace=-.25)
        g.set_titles("")
        g.set(yticks=[], ylabel="")
        g.despine(bottom=True, left=True)

        plt.xticks(rotation=45)
        g.figure.tight_layout()

        temp_file = "data/timetable_image.png"
        g.savefig(temp_file)
        plt.close()

        return temp_file

    def plot_nested_pie(self, chat_content):
        messages_per_user = self.count_messages_per_user(chat_content)
        sorted_users = sorted(messages_per_user[0].items(), key=lambda x: len(x[1]), reverse=True)
        labels = [user[0] for user in sorted_users]
        messages_count = [len(messages) for user, messages in sorted_users]

        size = 0.35
        fig, ax = plt.subplots(figsize=(10, 6))
        cmap = plt.get_cmap('Blues')
        colors = cmap(np.linspace(0.3, 1, 10))
        wedges, texts, autotexts = ax.pie(
            x=messages_count,
            autopct=lambda pct: "{:.2f}%\n({:d})".format(pct, int(pct/100.*np.sum(messages_count))),
            shadow=True,
            startangle=180,
            radius=1,
            wedgeprops={'width': size, 'edgecolor': 'black'},
            colors=colors)

        for i, (text, autotext) in enumerate(zip(texts, autotexts)):
            percent = messages_count[i] / sum(messages_count) * 100
            text.set_text(f"{labels[i]}\n{percent:.2f}%")
            autotext.set_text(f"{messages_count[i]}")

        plt.setp(autotexts, size=12, weight="bold")
        plt.setp(texts, size=14)

        temp_file = "data/proportion_image.png"
        plt.savefig(temp_file)
        plt.close()

        return temp_file
