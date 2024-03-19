from flask import Flask, render_template, request
from stats import char_stats, ep_stats, sea_stats
from get_ep import random_ep, ep_by_char, ep_by_ep, ep_by_ep_char
import matplotlib.pyplot as plt
from matplotlib import use
import seaborn as sns
import sqlite3
from random import choice
import pickle


use('agg')

app = Flask(__name__)

with open('characters.txt', 'r', encoding='utf-8') as f:
    chars = f.read().split('\n')
with open('episodes.txt', 'r', encoding='utf-8') as f:
    eps = f.read().split('\n')


@app.route('/')
def main():
    return render_template('main.html', characters=chars, episodes=eps)


@app.route('/recommendation')
def recommendation():
    ep = request.args['episode']
    char = request.args['character']
    con = sqlite3.connect('lbacn.db')
    cursor = con.cursor()
    disc = ''
    if ep == '':
        if char == '':
            rec = random_ep(cursor)
        else:
            rec = ep_by_char(char, cursor)
    else:
        if char == '':
            rec = ep_by_ep(ep, cursor)
        else:
            try:
                rec = ep_by_ep_char(ep, char, cursor)
            except Exception as e:
                rec = ep_by_char(char, cursor)
                disc = 'This is the only episode with the character'
                with open('problems.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{ep} and {char}: {str(e)}\n')
    image = rec[0]
    link = 'https://miraculousladybug.fandom.com' + rec[2]
    title = rec[3]
    synopsis = rec[4]
    return render_template('recommendation.html', image=image, link=link, title=title, synopsis=synopsis, disc=disc)


@app.route('/character')
def character():
    return render_template('character.html', characters=chars)


@app.route('/episode')
def episode():
    return render_template('episode.html', episodes=eps)


@app.route('/season')
def season():
    return render_template('season.html')


@app.route('/overall')
def overall():
    with open('overall_stats.txt', 'rb') as file:
        information = pickle.load(file)
    return render_template('stats_overall.html', num_ep=information[0], num_char=information[1],
                           num_lines=information[2], av_chars_ep=information[3],
                           av_lines_ep=information[4], av_lines_char=information[5],
                           top_char_lines=information[6], top_char_eps=information[7],
                           top_ep_chars=information[8], top_ep_lines=information[9])


@app.route('/episode_stats')
def episode_stats():
    ep = request.args['episode']
    if ep == '':
        ep = choice(eps)
    con = sqlite3.connect('lbacn.db')
    cursor = con.cursor()
    information = ep_stats(ep, cursor)
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_title("Number of lines per character", fontname='Georgia', fontsize=30)
    pie = information['piechart']
    if len(pie[0]) % 3 != 1:
        cols = ['#e31e1e', '#f0a2a2', '#a92525']
    elif len(pie[0]) % 4 != 1:
        cols = ['#e31e1e', '#f0a2a2', '#a92525', '#ffefea']
    else:
        cols = ['#e31e1e', '#f0a2a2', '#a92525', '#ffefea', '#020202']
    plt.pie(pie[0], labels=pie[1], textprops={'fontsize': 25, 'fontname': 'Georgia'},
            colors=cols)
    fig.tight_layout()
    plt.savefig('static/episode_piechart.png', transparent=True, dpi=500)
    return render_template('stats_episode.html', episode=ep, num_char=information['num_char'],
                           num_lines=information['num_lines'], av_lines=information['av_lines'],
                           top_10=information['top_10'])


@app.route('/character_stats')
def character_stats():
    char = request.args['character']
    if char == '':
        char = choice(chars)
    con = sqlite3.connect('lbacn.db')
    cursor = con.cursor()
    information = char_stats(char, cursor)
    fig, ax = plt.subplots(figsize=(26, 6))
    ax.set_title("Number of lines per episode", fontname='Georgia', fontsize=30)
    sns.heatmap(
        information['heatmap_info'],
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
    plt.savefig('static/character_heatmap.png', transparent=True, dpi=500)
    return render_template('stats_character.html', character=char, num_ep=information['num_ep'],
                           num_lines=information['num_lines'], av_lines=information['av_lines'],
                           top_10=information['top_10'])


@app.route('/season_stats')
def season_stats():
    sea = request.args['season']
    if sea == '':
        sea = choice([1, 2, 3, 4, 5, 6])
    con = sqlite3.connect('lbacn.db')
    cursor = con.cursor()
    information = sea_stats(1, cursor)
    fig, ax = plt.subplots(figsize=(26, 6))
    ax.set_title("Number of character per episode", fontname='Georgia', fontsize=30)
    plt.bar(information['bar_char'][0], information['bar_char'][1], color=['#a92525'])
    plt.xlabel('episode', fontname='Georgia', fontsize=20)
    plt.ylabel('number of characters', fontname='Georgia', fontsize=20)
    for tick in ax.get_xticklabels():
        tick.set_fontname('Georgia')
        tick.set_fontsize(15)
    for tick in ax.get_yticklabels():
        tick.set_fontname('Georgia')
        tick.set_fontsize(15)
    fig.tight_layout()
    plt.savefig('static/bar_char.png', transparent=True, dpi=500)
    fig, ax = plt.subplots(figsize=(26, 6))
    ax.set_title("Number of lines per episode", fontname='Georgia', fontsize=30)
    plt.bar(information['bar_line'][0], information['bar_line'][1], color=['#a92525'])
    plt.xlabel('episode', fontname='Georgia', fontsize=20)
    plt.ylabel('number of lines', fontname='Georgia', fontsize=20)
    for tick in ax.get_xticklabels():
        tick.set_fontname('Georgia')
        tick.set_fontsize(15)
    for tick in ax.get_yticklabels():
        tick.set_fontname('Georgia')
        tick.set_fontsize(15)
    fig.tight_layout()
    plt.savefig('static/bar_line.png', transparent=True, dpi=500)
    return render_template('stats_season.html', season=sea, num_ep=information['num_ep'],
                           num_char=information['num_char'], num_lines=information['num_lines'],
                           av_chars_ep=information['av_chars_ep'], av_lines_ep=information['av_lines_ep'],
                           av_lines_char=information['av_lines_char'], top_char_lines=information['top_char_lines'],
                           top_char_eps=information['top_char_eps'], top_ep_chars=information['top_ep_chars'],
                           top_ep_lines=information['top_ep_lines'])


@app.route('/help')
def help_and_structure():
    return render_template('help.html')


if __name__ == '__main__':
    app.run()
