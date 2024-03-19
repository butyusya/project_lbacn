from stats import overall_stats
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import pickle


con = sqlite3.connect('lbacn.db')
cursor = con.cursor()
information = overall_stats(cursor)
fig, ax = plt.subplots(figsize=(26, 6))
ax.set_title("Number of character per episode", fontname='Georgia', fontsize=30)
sns.heatmap(
    information['heat_char'],
    annot=True,
    xticklabels=range(1, 27),
    yticklabels=range(1, 6)
)
plt.xlabel('episode', fontname='Georgia', fontsize=20)
plt.ylabel('season', fontname='Georgia', fontsize=20)
for tick in ax.get_xticklabels():
    tick.set_fontname('Georgia')
    tick.set_fontsize(15)
for tick in ax.get_yticklabels():
    tick.set_fontname('Georgia')
    tick.set_fontsize(15)
fig.tight_layout()
plt.savefig('static/heat_char.png', transparent=True, dpi=500)
fig, ax = plt.subplots(figsize=(26, 6))
ax.set_title("Number of lines per episode", fontname='Georgia', fontsize=30)
sns.heatmap(
    information['heat_line'],
    annot=True,
    xticklabels=range(1, 27),
    yticklabels=range(1, 6),
    fmt='.0f'
)
plt.xlabel('episode', fontname='Georgia', fontsize=20)
plt.ylabel('season', fontname='Georgia', fontsize=20)
for tick in ax.get_xticklabels():
    tick.set_fontname('Georgia')
    tick.set_fontsize(15)
for tick in ax.get_yticklabels():
    tick.set_fontname('Georgia')
    tick.set_fontsize(15)
fig.tight_layout()
plt.savefig('static/heat_line.png', transparent=True, dpi=500)
overall = [information['num_ep'], information['num_char'], information['num_lines'], information['av_chars_ep'],
           information['av_lines_ep'], information['av_lines_char'], information['top_char_lines'],
           information['top_char_eps'], information['top_ep_chars'], information['top_ep_lines']]
with open('overall_stats.txt', 'wb') as f:
    pickle.dump(overall, f)
