from flask import Blueprint, render_template, request
from . import db_session
from .users import User

gg = Blueprint('gg_api', __name__, template_folder='templates')


@gg.route('/gg', methods=['GET', 'POST'])
def set_gg():
    db_sess = db_session.create_session()
    us_found = False
    if request.method == 'POST':
        us_id = request.form.get("id")
        user = db_sess.query(User).get(us_id)
        if not user:
            return render_template('gg.html', message='Ошибка: Пользователь не найден.')
        else:
            us_found = True
            return render_template('gg.html', message=f'Вы действительно хотите удалить '
                                                      f'пользователя {user.login}?', us_found=us_found)
    return render_template('gg.html')


@gg.route('/gg_f', methods=['GET', 'POST'])
def gg_f():
    gg_is_here = True
    return render_template('gg.html', message=f'Ох и зря ты сюда полез... Ладно, не бойся, '
                                              f'мы тебя разыграли.', gg_is_here=gg_is_here)