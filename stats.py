def char_stats(name: str, cur):
    name_query = f"""
        SELECT * FROM characters_lines
    	    JOIN episodes ON characters_lines.ep_id=episodes.ep_id
        WHERE character = "{name}"
        """
    cur.execute(name_query)
    info = cur.fetchall()
    answer = dict()
    answer['num_ep'] = len(info)
    lines = 0
    for x in info:
        lines += x[2]
    answer['num_lines'] = lines
    answer['av_lines'] = round(lines/len(info), 2)
    info_sort = sorted(info, key=lambda a: a[2], reverse=True)
    top = []
    if len(info) < 10:
        for x in info_sort:
            place = (x[6], x[2])
            top.append(place)
    else:
        for i in range(10):
            x = info_sort[i]
            place = (x[6], x[2])
            top.append(place)
    answer['top_10'] = top
    heatmap = []
    for s in range(1, 6):
        s_num = []
        for e in range(1, 27):
            cur_id = 100 * s + e
            cur_lines = 0
            for x in info:
                if x[0] == cur_id:
                    cur_lines = x[2]
            s_num.append(cur_lines)
        heatmap.append(s_num)
    answer['heatmap_info'] = heatmap
    return answer


def ep_stats(title: str, cur):
    title_query = f"""
        SELECT * FROM episodes
        	JOIN characters_lines ON episodes.ep_id = characters_lines.ep_id
        WHERE ep_title = "{title}"
        """
    cur.execute(title_query)
    info = cur.fetchall()
    answer = dict()
    answer['num_char'] = len(info)
    lines = 0
    for x in info:
        lines += x[9]
    answer['num_lines'] = lines
    answer['av_lines'] = round(lines / len(info), 2)
    info_sort = sorted(info, key=lambda a: a[9], reverse=True)
    top = []
    if len(info) < 10:
        for x in info_sort:
            place = (x[8], x[9])
            top.append(place)
    else:
        for i in range(10):
            x = info_sort[i]
            place = (x[8], x[9])
            top.append(place)
    answer['top_10'] = top
    lines_char = []
    chars = []
    for x in info_sort:
        if x[9] > 2:
            lines_char.append(x[9])
            chars.append(x[8])
    answer['piechart'] = (lines_char, chars)
    return answer


def sea_stats(number: int, cur):
    season_query1 = f"""
        SELECT * from episodes
        WHERE season = {number}
        """
    cur.execute(season_query1)
    season1 = cur.fetchall()
    answer = dict()
    answer['num_ep'] = len(season1)
    season_query2 = f"""
        SELECT season, character, SUM(num_of_replics) as total_lines FROM episodes
            JOIN characters_lines ON episodes.ep_id = characters_lines.ep_id
        WHERE season = {number}
        GROUP BY character
        """
    cur.execute(season_query2)
    season2 = cur.fetchall()
    answer['num_char'] = len(season2)
    lines = 0
    for x in season2:
        lines += x[2]
    answer['num_lines'] = lines
    season_query2_1 = f"""
        SELECT season, character FROM episodes
            JOIN characters_lines ON episodes.ep_id = characters_lines.ep_id
        WHERE season = {number}
        """
    cur.execute(season_query2_1)
    season2_1 = cur.fetchall()
    answer['av_chars_ep'] = round(len(season2_1) / answer['num_ep'], 2)
    answer['av_lines_ep'] = round(answer['num_lines'] / answer['num_ep'], 2)
    answer['av_lines_char'] = round(answer['num_lines'] / answer['num_char'], 2)
    season2_sort = sorted(season2, key=lambda a: a[2], reverse=True)
    top_char_lines = []
    if len(season2) < 10:
        for x in season2_sort:
            place = (x[1], x[2])
            top_char_lines.append(place)
    else:
        for i in range(10):
            x = season2_sort[i]
            place = (x[1], x[2])
            top_char_lines.append(place)
    answer['top_char_lines'] = top_char_lines
    season_query3 = f"""
        SELECT season, character, COUNT(character) as total_ep FROM episodes
            JOIN characters_lines ON episodes.ep_id = characters_lines.ep_id
        WHERE season = {number}
        GROUP BY character
        """
    cur.execute(season_query3)
    season3 = cur.fetchall()
    season3_sort = sorted(season3, key=lambda a: a[2], reverse=True)
    top_char_eps = []
    if len(season3) < 10:
        for x in season3_sort:
            place = (x[1], x[2])
            top_char_eps.append(place)
    else:
        for i in range(10):
            x = season3_sort[i]
            place = (x[1], x[2])
            top_char_eps.append(place)
    answer['top_char_eps'] = top_char_eps
    season_query4 = f"""
        SELECT *, COUNT(character) as num_char, SUM(num_of_replics) as total_rep FROM episodes
            JOIN characters_lines ON episodes.ep_id = characters_lines.ep_id
        WHERE season = {number}
        GROUP BY ep_title
        ORDER BY ep_id
    """
    cur.execute(season_query4)
    season4 = cur.fetchall()
    season4_sort_char = sorted(season4, key=lambda a: a[10], reverse=True)
    top_ep_chars = []
    for i in range(5):
        x = season4_sort_char[i]
        place = (x[3], x[10])
        top_ep_chars.append(place)
    answer['top_ep_chars'] = top_ep_chars
    season4_sort_lines = sorted(season4, key=lambda a: a[11], reverse=True)
    top_ep_lines = []
    for i in range(5):
        x = season4_sort_lines[i]
        place = (x[3], x[11])
        top_ep_lines.append(place)
    answer['top_ep_lines'] = top_ep_lines
    x = []
    y_char = []
    y_lines = []
    for i in range(answer['num_ep']):
        x.append(i+1)
        y_char.append(season4[i][10])
        y_lines.append(season4[i][11])
    answer['bar_char'] = [x, y_char]
    answer['bar_line'] = [x, y_lines]
    return answer


def overall_stats(cur):
    query1 = """
            SELECT * from episodes
            """
    cur.execute(query1)
    info1 = cur.fetchall()
    answer = dict()
    answer['num_ep'] = len(info1)
    query2 = """
        SELECT season, character, SUM(num_of_replics) as total_lines FROM episodes
            JOIN characters_lines ON episodes.ep_id = characters_lines.ep_id
        GROUP BY character
        """
    cur.execute(query2)
    info2 = cur.fetchall()
    answer['num_char'] = len(info2)
    lines = 0
    for x in info2:
        lines += x[2]
    answer['num_lines'] = lines
    query2_1 = """
        SELECT character FROM episodes
            JOIN characters_lines ON episodes.ep_id = characters_lines.ep_id
        """
    cur.execute(query2_1)
    info2_1 = cur.fetchall()
    answer['av_chars_ep'] = round(len(info2_1) / answer['num_ep'], 2)
    answer['av_lines_ep'] = round(answer['num_lines'] / answer['num_ep'], 2)
    answer['av_lines_char'] = round(answer['num_lines'] / answer['num_char'], 2)
    info2_sort = sorted(info2, key=lambda a: a[2], reverse=True)
    top_char_lines = []
    if len(info2) < 10:
        for x in info2_sort:
            place = (x[1], x[2])
            top_char_lines.append(place)
    else:
        for i in range(10):
            x = info2_sort[i]
            place = (x[1], x[2])
            top_char_lines.append(place)
    answer['top_char_lines'] = top_char_lines
    query3 = """
        SELECT season, character, COUNT(character) as total_ep FROM episodes
            JOIN characters_lines ON episodes.ep_id = characters_lines.ep_id
        GROUP BY character
        """
    cur.execute(query3)
    info3 = cur.fetchall()
    info3_sort = sorted(info3, key=lambda a: a[2], reverse=True)
    top_char_eps = []
    if len(info3) < 10:
        for x in info3_sort:
            place = (x[1], x[2])
            top_char_eps.append(place)
    else:
        for i in range(10):
            x = info3_sort[i]
            place = (x[1], x[2])
            top_char_eps.append(place)
    answer['top_char_eps'] = top_char_eps
    query4 = """
        SELECT *, COUNT(character) as num_char, SUM(num_of_replics) as total_rep FROM episodes
            JOIN characters_lines ON episodes.ep_id = characters_lines.ep_id
        GROUP BY ep_title
        ORDER BY ep_id
        """
    cur.execute(query4)
    info4 = cur.fetchall()
    info4_sort_char = sorted(info4, key=lambda a: a[10], reverse=True)
    top_ep_chars = []
    for i in range(5):
        x = info4_sort_char[i]
        place = (x[3], x[10])
        top_ep_chars.append(place)
    answer['top_ep_chars'] = top_ep_chars
    info4_sort_lines = sorted(info4, key=lambda a: a[11], reverse=True)
    top_ep_lines = []
    for i in range(5):
        x = info4_sort_lines[i]
        place = (x[3], x[11])
        top_ep_lines.append(place)
    answer['top_ep_lines'] = top_ep_lines
    heat_char = []
    heat_line = []
    for s in range(1, 6):
        season = sea_stats(s, cur)
        char = season['bar_char'][1]
        if len(char) == 27:
            char = char[:-1]
        line = season['bar_line'][1]
        if len(line) == 27:
            line = line[:-1]
        heat_char.append(char)
        heat_line.append(line)
    answer['heat_char'] = heat_char
    answer['heat_line'] = heat_line
    return answer
