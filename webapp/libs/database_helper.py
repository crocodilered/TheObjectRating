__all__ = ['DatabaseHelper']


class DatabaseHelper:
    def __init__(self, session):
        self._session = session

    def load_points(self, competition_id=0):
        """
        Загрузка количества очков стрелков в соревновании
        :param competition_id: ID соревнования
        :return: dict of dicts {value}
        """
        r = {}
        if competition_id:
            sql = "SELECT shooter_id, value FROM points WHERE competition_id = %s" % competition_id
            rows = self._session.execute(sql).fetchall()
            for (shooter_id, value) in rows:
                r[shooter_id] = value
        return r

    def load_shooters(self):
        """
        Загрузка списка стрелков
        :return:
        """
        r = []
        sql = """
            SELECT
                shooter.shooter_id, 
                shooter.name, 
                COUNT(points.competition_id) as competitions_count
            FROM shooter
            LEFT JOIN points ON shooter.shooter_id = points.shooter_id
            GROUP BY shooter.shooter_id ORDER BY shooter.name
        """
        rows = self._session.execute(sql).fetchall()
        for (shooter_id, name, competitions_count) in rows:
            r.append({
                'shooter_id': shooter_id,
                'name': name,
                'rating': 1,  # сначала у всех по единице
                'rating_percents_curr': 0,  # в процентах
                'rating_percents_prev': 0,  # в процентах
                'competitions_count': competitions_count
            })
        return r

    def load_shooters_with_rating(self):
        """
        Загрузка информации о стрелке, включая рейтинг
        :return:
        """
        r = []
        sql = """
            SELECT
                shooter.shooter_id, 
                shooter.name as name, 
                COUNT(points.competition_id), 
                r_last.value_abs, 
                r_last.value_percents,  
                (r_last.value_percents - r_prev.value_percents)
            FROM shooter 
            LEFT JOIN points ON shooter.shooter_id = points.shooter_id 
            LEFT JOIN ratings as r_last ON shooter.shooter_id = r_last.shooter_id AND r_last.competition_id = 
                ( SELECT competition_id FROM competition ORDER BY dt DESC LIMIT 1 )
            LEFT JOIN ratings as r_prev ON shooter.shooter_id = r_prev.shooter_id AND r_prev.competition_id = 
                ( SELECT competition_id FROM competition ORDER BY dt DESC LIMIT 1,1 )
            GROUP BY shooter.shooter_id
            ORDER BY r_last.value_abs DESC
        """
        rows = self._session.execute(sql).fetchall()
        for (shooter_id, name, competitions_count, rating, rating_percents, rating_percents_delta) in rows:
            r.append({
                'shooter_id': shooter_id,
                'name': name,
                'competitions_count': competitions_count,
                'rating': rating,
                'rating_percents': rating_percents,
                'rating_percents_delta': rating_percents_delta
            })
        return r

    def load_shooter(self, shooter_id):
        """
        Загрузка информации о стрелке
        :param shooter_id:
        :return:
        """
        r = {}
        sql = """
            SELECT
                shooter.shooter_id,
                shooter.name,
                COUNT(points.competition_id),
                ratings.value_abs,
                ratings.value_percents
            FROM shooter
            LEFT JOIN points ON shooter.shooter_id = points.shooter_id
            LEFT JOIN ratings ON shooter.shooter_id = ratings.shooter_id AND ratings.competition_id = 
                ( SELECT competition_id FROM competition ORDER BY dt DESC LIMIT 1 )
            WHERE shooter.shooter_id = %s
            GROUP BY shooter.shooter_id
            LIMIT 1
        """ % shooter_id
        row = self._session.execute(sql).first()
        r['shooter_id'] = row[0]
        r['name'] = row[1]
        r['competitions_count'] = row[2]
        r['rating'] = row[3]
        r['rating_percents'] = row[4]
        return r

    def load_shooter_competitions(self, shooter_id):
        """
        Загрузка соревнований, в которых принимал участие стрелок
        :param shooter_id:
        :return:
        """
        r = []
        sql = """
            SELECT
                competition.competition_id,
                competition.title,
                competition.dt,
                ratings.value_abs,
                ratings.value_percents,
                points.value
            FROM competition
            LEFT JOIN ratings ON ratings.competition_id = competition.competition_id AND ratings.shooter_id = %s
            LEFT JOIN points ON points.competition_id = competition.competition_id AND points.shooter_id = %s
            ORDER BY competition.dt DESC
        """ % (shooter_id, shooter_id)
        rows = self._session.execute(sql).fetchall()
        for row in rows:
            row_pos = rows.index(row)
            next_rating_percents = rows[row_pos+1][4] if row_pos < len(rows)-1 else 0
            r.append({
                "competition_id": row[0],
                "title": row[1],
                "date": row[2],
                "rating": row[3],
                "rating_percents": row[4],
                "points": row[5],
                "gain": (row[4] - next_rating_percents)
            })
        return r

    def load_competition(self, competition_id):
        """
        Загрузка информации о соревновании
        :param competition_id:
        :return:
        """
        r = {}
        sql = """
            SELECT competition_id, title, dt
            FROM competition
            WHERE competition_id = %s
        """ % competition_id
        row = self._session.execute(sql).first()
        r['competition_id'] = row[0]
        r['title'] = row[1]
        r['date'] = row[2]
        return r

    def load_competition_shooters(self, competition_id):
        """
        Загрузка стрелков, выступавших на соревновании
        :param competition_id:
        :return:
        """
        r = []
        sql = """
            SELECT
                points.value,
                shooter.shooter_id,
                shooter.name
            FROM competition
            LEFT JOIN points ON competition.competition_id = points.competition_id
            LEFT JOIN shooter ON shooter.shooter_id = points.shooter_id
            WHERE competition.competition_id = %s
            ORDER BY points.value DESC
        """ % competition_id
        rows = self._session.execute(sql).fetchall()
        for (points, shooter_id, name) in rows:
            r.append({
                'points': points,
                'shooter_id': shooter_id,
                'name': name
            })
        return r

    def load_competitions(self):
        """
        Получение списка соревнований
        :return: таблица соревнований
        """
        r = []
        sql = """
            SELECT
                competition.competition_id,
                competition.title,
                competition.dt,
                COUNT(points.shooter_id)
            FROM competition
            LEFT JOIN points ON points.competition_id = competition.competition_id
            GROUP BY points.competition_id
            ORDER BY competition.dt
        """
        rows = self._session.execute(sql).fetchall()
        for (competition_id, title, dt, shooters_count) in rows:
            r.append({
                "competition_id": competition_id,
                "title": title,
                "date": dt,
                "shooters_count": shooters_count
            })
        return r

    def clear_competition_rating(self):
        """
        Обнуление рейтингов
        :return:
        """
        self._session.execute("DELETE FROM ratings")

    def put_competition_rating(self, competition_id, shooters):
        """
        Сохранение рейтингов
        :param competition_id:
        :param shooters:
        :return:
        """
        sql = "INSERT INTO ratings (competition_id, shooter_id, value_abs, value_percents) VALUES "
        for shooter in shooters:
            sql += "(%s, %s, %s, %s)," % (competition_id,
                                          shooter['shooter_id'],
                                          shooter['rating'],
                                          shooter['rating_percents_curr'])
        self._session.execute(sql[:-1])  # откусить ненужную запятую

