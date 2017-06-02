import cherrypy
import webapp.libs.utils as u
from datetime import date
from webapp.libs.database_helper import DatabaseHelper

__all__ = ['RatingApp']


class RatingApp(object):
    @cherrypy.expose
    @cherrypy.tools.render(template='index.html')
    def index(self):
        calc_date = date.today()
        db = DatabaseHelper(cherrypy.request.db)
        shooters = db.load_shooters_with_rating()
        return {
            'shooters': shooters,
            'calc_date': calc_date,
            'path': 'shooters'
        }

    @cherrypy.expose
    @cherrypy.tools.render(template='shooter.html')
    def shooter(self, shooter_id):
        db = DatabaseHelper(cherrypy.request.db)
        shooter = db.load_shooter(shooter_id)
        competitions = db.load_shooter_competitions(shooter_id)
        return {
            'shooter': shooter,
            'competitions': competitions,
            'calc_date': date.today()
        }

    @cherrypy.expose
    @cherrypy.tools.render(template='competition.html')
    def match(self, match_id):
        db = DatabaseHelper(cherrypy.request.db)
        competition = db.load_competition(match_id)
        shooters = db.load_competition_shooters(match_id)
        return {
            'competition': competition,
            'shooters': shooters
        }

    @cherrypy.expose
    @cherrypy.tools.render(template='statistics.html')
    def statistics(self):
        db = DatabaseHelper(cherrypy.request.db)
        competitions = db.load_competitions()
        shooters = db.load_shooters_with_rating()
        return {
            'competitions': competitions,
            'shooters': shooters,
            'path': 'statistics'
        }

    @cherrypy.expose
    @cherrypy.tools.render(template='message.html')
    def calc_rating(self):
        calc_date = date.today()
        db = DatabaseHelper(cherrypy.request.db)
        shooters = db.load_shooters()
        competitions = db.load_competitions()
        competition_rating = {}
        db.clear_competition_rating()
        # считаем рейтинг стрелков для каждого соревнования и складываем его в competition_rating
        for competition in competitions:
            # пары shooter_id, value для соревнования competition_id
            points = db.load_points(competition['competition_id'])
            # сумма рейтингов стрелков, участвующих в соревновании
            rating_sum = u.calc_ratings_sum(shooters, points.keys())
            # сумма очков стрелков, участвующих в соревновании
            points_sum = u.calc_points_sum(points)
            for shooter_id in points:
                # считаем коэф. затухания
                k = u.calc_attenuation_constant(calc_date, competition['date'])
                # складываем высчитанный рейтинг в rating_of_competition с ключом (shooter_id, competition_id)
                competition_rating[shooter_id, competition['competition_id']] = \
                    (rating_sum * points[shooter_id] / points_sum) * k
                # инкрементим стрелку посчитанный рейтинг за данное соревнование к общему рейтингу
                lookup_item = next(item for item in shooters if item["shooter_id"] == shooter_id)
                lookup_item['rating'] += competition_rating[shooter_id, competition['competition_id']]
                # нужно рассчитать рейтинг У ВСЕХ стрелков
                shooters = u.calc_rating_in_percents(shooters)
            db.put_competition_rating(competition['competition_id'], shooters)
        return {
            'title': "Success",
            'message': "Rating table recalculation is done."
        }
