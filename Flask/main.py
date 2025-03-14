import datetime
import random
import os

from flask import Flask, render_template, request, redirect, abort
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from data import db_session
from data.users import User
from data.post import Posts
from data.comment import Comments
from data.news import News
from data.needs import checked_email, get_hashed_password, check_password_hashed,\
    random_avatar, password_check_regular, checked_avatar

from forms.setting import SettingForm
from forms.comments import CommentsForm
from forms.News import NewsForm
from forms.posts import PostsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_teacher_secret_key'
code_for_email, param_for_user = "", []
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/delete_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def str_19(id):
    db_sess = db_session.create_session()
    comment = db_sess.query(Comments).filter(Comments.id == id).first()
    post_id = comment.post_id
    if comment and current_user == comment.user:
        db_sess.delete(comment)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/post/{post_id}')



@app.route('/shop', methods=['GET', 'POST'])
@login_required
def str_18():
    print(current_user.id)
    return render_template('shop.html')


@app.route('/add_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def str_17(id):
    form = CommentsForm()
    db_sess = db_session.create_session()
    post = db_sess.query(Posts).filter(Posts.id == id).first()
    if form.validate_on_submit():
        comment = Comments()
        comment.text = form.text.data
        comment.post_id = id
        current_user.comments.append(comment)
        db_sess.merge(current_user)
        db_sess.merge(db_sess.query(Posts).filter(Posts.id == id).first())
        db_sess.commit()
        return redirect(f'/post/{id}')
    return render_template('coment.html', form=form, post=post)


@app.route('/delete_post/<int:id>', methods=['GET', 'POST'])
@login_required
def str_16(id):
    db_sess = db_session.create_session()
    post = db_sess.query(Posts).filter(Posts.id == id).first()

    if post:
        db_sess.delete(post)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/lecture')


@app.route('/post/<int:id>')
@login_required
def str_15(id):
    db_sess = db_session.create_session()
    post = db_sess.query(Posts).filter(Posts.id == id).first()
    post_comments = db_sess.query(Comments).filter(Comments.post_id == id).all()
    return render_template('im_post.html',
                           title='Пост' + str(post.id), post=post, post_comments=post_comments)

@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def str_14(id):
    form = PostsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        post = db_sess.query(Posts).filter(Posts.id == id).first()
        form.type_post.data = post.type
        form.title.data = post.title
        form.content.data = post.content
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        post = db_sess.query(Posts).filter(Posts.id == id).first()
        post.type = form.type_post.data
        post.title = form.title.data
        post.content = form.content.data
        post.crat_content = form.crat_content.data
        if form.photo.data:
            photo = form.photo.data
            if photo.filename.split('.')[-1] not in ['png', 'jpeg', 'jpg', 'ico', 'gif', 'bmp']:
                return render_template('creater_post.html', title='Редактирование поста',
                                       form=form, message="Файл не являтся изображением")
            photo_name = "post-" + current_user.email + "-" + str(current_user.id) + "-" + str(id) \
                         + '.' + photo.filename.split('.')[-1]
            photo.save("static/img/post/" + photo_name)
            post.photo = photo_name
        db_sess.merge(post)
        db_sess.commit()
        return redirect('/lecture')
    return render_template('creater_post.html',
                           title='Редактирование поста',
                           form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def str_13(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/news')


@app.route('/add_news/<int:id>', methods=['GET', 'POST'])
@login_required
def str_12(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            db_sess.commit()
            return redirect('/news')
        else:
            abort(404)
    return render_template('add_news.html',
                           main_title='Редактирование новости',
                           form=form)


@app.route('/add_news',  methods=['GET', 'POST'])
@login_required
def str_11():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/news')
    return render_template('add_news.html', main_title='Добавление новости',
                           form=form)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def str_10():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    return render_template("news.html", news=news)


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def str_9():
    if current_user.role in ['Менеджер', 'Админ']:
        form = PostsForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            post = Posts()
            post.type = form.type_post.data
            post.title = form.title.data
            post.crat_content = form.crat_content.data
            post.content = form.content.data
            if not form.photo.data:
                post.image = 'post-1.jpg'
            else:
                photo = form.photo.data
                if photo.filename.split('.')[-1] not in ['png', 'jpeg', 'jpg', 'ico', 'gif', 'bmp']:
                    return render_template('creater_post.html', title='Добавление поста',
                                           form=form, message="Файл не являтся изображением")
                photo_name = "post-" + current_user.email + "-" + str(current_user.id) + "-" + str(id) \
                             + '.' + photo.filename.split('.')[-1]
                photo.save("static/img/post/" + photo_name)
                post.photo = photo_name

            current_user.posts.append(post)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/lecture')
        return render_template('creater_post.html', form=form, title="Создание поста")
    else:
        redirect("/")



@app.route('/lecture', methods=['GET', 'POST'])
def str_8():
    db_sess = db_session.create_session()
    post = db_sess.query(Posts).all()
    return render_template("lecture.html", posts=post)


@app.route('/delete_user', methods=['GET', 'POST'])
@login_required
def str_7():
    message = ""
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user:
        if request.method == 'POST':
            if check_password_hashed(request.form["code_for_email"], user.hashed_password):
                print("ok")
                for post in user.posts:
                    if os.path.isfile('static/img/post/' + post.photo):
                        os.remove('static/img/post/' + post.photo)
                    for comment in post.comments:
                        db_sess.delete(comment)
                    db_sess.delete(post)
                for comment in user.comments:
                    db_sess.delete(comment)

                for new in user.news:
                    db_sess.delete(new)

                if os.path.isfile('static/img/Ava/' + user.avatar) and not checked_avatar('static/img/Ava/' + user.avatar):
                    os.remove('static/img/Ava/' + user.avatar)
                db_sess.delete(user)
                db_sess.commit()
                return redirect("/")
            else:
                message = "Пароль неверен"
    return render_template('register_2_step.html', message=message, title="Удаление аккаунта!",
                           subtitle="Подтвердите пароль")


@app.route('/setting', methods=['POST', 'GET'])
@login_required
def str_6():
    global code_for_email
    title = "Настройки"
    form = SettingForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if request.method == 'GET':
        form.email.data = user.email
        form.nickname.data = user.nickname
        form.role.data = user.role
    if request.method == 'POST':
        if form.avatar.data:
            avatar = form.avatar.data
            if avatar.filename.split('.')[-1] not in ['png', 'jpeg', 'jpg', 'ico', 'gif', 'bmp']:
                return render_template('setting.html', title=title, form=form,
                                       message="Файл не является картинкой")
            avatar_name = "avatar-" + current_user.email + "-" + str(current_user.id) + '.' + \
                          avatar.filename.split('.')[-1]
            avatar.save("static/img/Ava/" + avatar_name)
            user.avatar = avatar_name

        if form.nickname.data:
            user.nickname = form.nickname.data

        if form.role.data:
            user.role = form.role.data

        if form.new_password.data:
            if password_check_regular(form.new_password.data) != "ok":
                return render_template('setting.html', title=title, form=form,
                                       message=password_check_regular(form.new_password.data))

        if not check_password_hashed(form.old_password.data, user.hashed_password):
            return render_template('setting.html', title=title, form=form,
                                   message="Не правильный старый пароль")

        if check_password_hashed(form.old_password.data, user.hashed_password):
            if form.new_password.data:
                user.hashed_password = get_hashed_password(form.new_password.data)
            db_sess.merge(user)
            db_sess.commit()
        return redirect('/guest')
    else:
        return render_template('setting.html', title=title, form=form)


@app.route('/guest', methods=['POST', 'GET'])
@login_required
def str_5():
    if request.method == 'POST':
        if request.form["btnAddMore"] == "Edit Profile":
            return redirect("/setting")
        if request.form["btnAddMore"] == "Logout":
            return redirect("/logout")
    else:
        users = db_session.create_session().query(User).filter(User.id == current_user.id).first()
        return render_template("guest.html", nickname=users.nickname, id=users.id, email=users.email,
                               user=users.nickname, img="../static/img/ava/" + str(users.avatar),
                               role=users.role)


@app.route("/login", methods=['POST', 'GET'])
def str_4():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        db_sess = db_session.create_session()

        if not(db_sess.query(User).filter(User.email == email).first()):
            message = "Такого пользователь нет"
            return render_template('login.html', message=message)
        check_user = db_sess.query(User).filter(User.email == email).first()

        if not(check_password_hashed(password, check_user.hashed_password)):
            message = "Пароли не совпадают"
            return render_template('login.html', message=message)

        login_user(check_user, remember=True)
        return redirect("/guest")
    else:
        return render_template("login.html")


@app.route("/register", methods=['POST', 'GET'])
def str_3():
    global code_for_email, param_for_user
    message = ""
    if request.method == 'POST':
        nickname = request.form["nickname"]
        email = request.form["email"]
        password = request.form["password"]
        rep_password = request.form["rep_password"]

        check = password_check_regular(password)
        if check != "ok":
            message = check
            return render_template('register.html', message=message)

        if password != rep_password:
            message = "Пароли не совпадают"
            return render_template('register.html', message=message)

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == email).first():
            message = "Такой пользователь уже есть"
            return render_template('register.html', message=message)

        if len(email) == 0 or len(nickname) == 0 or len(password) == 0:
            message = "Не заполнены поля"
            return render_template('register.html', message=message)

        code_for_email = checked_email(email)
        param_for_user = [nickname, email, password]
        return redirect("/register_2_step")
    else:
        return render_template('register.html', message=message)


@app.route("/register_2_step", methods=['POST', 'GET'])
def str_2():
    message = ""
    if request.method == 'POST':
        code_for_email2 = request.form["code_for_email"]
        if code_for_email == code_for_email2:
            db_sess = db_session.create_session()

            user = User(
                nickname=param_for_user[0],
                email=param_for_user[1],
                hashed_password=get_hashed_password(param_for_user[2]),
                role="Пользователь",
                avatar=random_avatar()
            )

            db_sess.add(user)
            db_sess.commit()

            login_user(user, remember=True)

            return redirect("/")
        else:
            message = "Код неправильный"
            return render_template('register_2_step.html', message=message, title="Добро пожаловать!",
                                   subtitle="Подтверждение почты.")
    else:
        return render_template('register_2_step.html', message=message, title="Добро пожаловать!",
                               subtitle="Подтверждение почты.")



@app.route('/')
def str_1():
    return render_template("main.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    print("Пользователь вышел")
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(int(user_id))


def main():
    db_session.global_init("data/astronomy.db")
    app.run(port=8080, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()