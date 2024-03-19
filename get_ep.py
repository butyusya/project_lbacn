from random import choice


def random_ep(cur):
    ep_query = """
        SELECT * FROM episodes
        """
    cur.execute(ep_query)
    answer = choice(cur.fetchall())
    return answer


def ep_by_char(name, cur):
    name_query = f"""
        SELECT * FROM episodes
	        JOIN characters_lines ON episodes.ep_id=characters_lines.ep_id
        WHERE character = "{name}"
        """
    cur.execute(name_query)
    answer = choice(cur.fetchall())
    return answer


def ep_by_ep(title, cur):
    title_query = f"""
        SELECT top_1_id FROM episodes
	        JOIN similarity ON episodes.ep_id=similarity.ep_id
        WHERE ep_title = "{title}"
        """
    cur.execute(title_query)
    answer_id = cur.fetchone()[0]
    id_query = f"""
        SELECT * FROM episodes
        WHERE ep_id = {answer_id}
        """
    cur.execute(id_query)
    answer = cur.fetchone()
    return answer


def ep_by_ep_char(title, name, cur):
    name_query = f"""
        SELECT * FROM episodes
        	JOIN characters_lines ON episodes.ep_id=characters_lines.ep_id
        WHERE character = "{name}"
        """
    cur.execute(name_query)
    eps_with_char = cur.fetchall()
    title_query = f"""
        SELECT * FROM episodes
    	    JOIN similarity ON episodes.ep_id=similarity.ep_id
        WHERE ep_title = "{title}"
        """
    cur.execute(title_query)
    title_info = cur.fetchone()
    top = 8
    answer = ()
    while len(answer) == 0:
        possible_id = title_info[top]
        for x in eps_with_char:
            if x[0] == possible_id:
                answer = x
        top += 1
    return answer
