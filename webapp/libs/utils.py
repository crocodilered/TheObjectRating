from datetime import date
import math


def days_from(d1, d2):
    """
    Рассчет кол-ва дней между двумя датами s1 и s2
    :param d1: дата 1
    :param d2: дата 2
    :return: количество дней
    """
    delta = d1 - d2
    return delta.days


def days_from_now(d):
    """
    Обертка для специализированного вызова days_from, когда один из параметров -- "сегодня"
    :param d: дата
    :return: количество дней от сегодня до указанной даты
    """
    return days_from(date.today(), d)


def calc_ratings_sum(shooters, shooters_list_to_calc):
    """
    Рассчет общей суммы рейтингов списка выбранных стрелков
    :param shooters: глобальная таблица рейтингами стрелков
    :param shooters_list_to_calc: список стрелков, чьи рейтинги необходимо просуммировать
    :return: суммы рейтингов списка выбранных стрелков
    """
    # TODO: возможно, такой lookup требуется переписать
    r = 0
    for shooter_id in shooters_list_to_calc:
        lookup_item = next(item for item in shooters if item["shooter_id"] == shooter_id)
        r += lookup_item["rating"]
    return r


def calc_points_sum(points):
    """
    Рассчет общей суммы очков стрелков в рамках одного соревнования
    :param points: Таблица стрелков с очками
    :return: суммы очков
    """
    return sum(points.values()) or 0


def calc_attenuation_constant(d1, d2):
    """
    Вачисляем коэф затухания для периода времени d1—d2
    :param d1: дата 1
    :param d2: дата 2
    :return: коэф.
    """
    # среднее кол-во дней в месяце
    days_in_month = (365 * 4 + 1) / (4 * 12)
    # количество месяцев между сегодня и датой соревнования
    months = days_from(d1, d2) / days_in_month
    # считаем коэф. затухания. Целые числа -- экспериментально подобранные коэфф.
    return math.exp(1 / -200 * months ** (0.6 + months / 20))


def calc_rating_in_percents(shooters):
    """
    Рассчет рейтинга в процентах на основании абсолютных величин
    :return:
    """
    # поиск максимального рейтинга
    max_rating = max(shooters, key=lambda d: d['rating'])['rating']
    # теперь посчитаем рейтинг
    for shooter in shooters:
        shooter['rating_percents_prev'] = shooter['rating_percents_curr']
        shooter['rating_percents_curr'] = 100 * shooter['rating'] / max_rating
    # print(shooters[454])  # посмотреть данные стрелка
    return shooters


if __name__ == "__main__":
    # just to test
    print(days_from_now("03.01.2015"))
