from uuid import uuid4

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename

from . import db
from .forms import DeleteForm, LoginForm, RegisterForm, UploadForm
from .models import Model, User


main_bp = Blueprint("main", __name__)


def save_upload(file_storage, destination):
    filename = secure_filename(file_storage.filename or "")
    if not filename:
        raise ValueError("Файл повинен мати коректне ім’я.")
    stored_name = f"{uuid4().hex}_{filename}"
    file_storage.save(destination / stored_name)
    return stored_name, filename


def cleanup_saved_uploads(stl_filename=None, photo_filename=None):
    remove_file_if_exists(current_app.config["STL_UPLOAD_FOLDER"], stl_filename)
    remove_file_if_exists(current_app.config["PHOTO_UPLOAD_FOLDER"], photo_filename)


def remove_file_if_exists(folder, filename):
    if not filename:
        return
    path = folder / filename
    if path.exists():
        path.unlink()


@main_bp.route("/")
def index():
    models = Model.query.order_by(Model.created_at.desc()).all()
    return render_template("index.html", models=models)


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Реєстрація успішна. Тепер увійдіть у систему.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html", form=form)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Вхід виконано успішно.", "success")
            return redirect(url_for("main.index"))
        flash("Невірний email або пароль.", "danger")

    return render_template("login.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("main.index"))


@main_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        saved_stl_filename = None
        original_filename = None
        saved_photo_filename = None
        try:
            saved_stl_filename, original_filename = save_upload(
                form.stl_file.data,
                current_app.config["STL_UPLOAD_FOLDER"],
            )
            if form.photo_file.data and form.photo_file.data.filename:
                saved_photo_filename, _ = save_upload(
                    form.photo_file.data,
                    current_app.config["PHOTO_UPLOAD_FOLDER"],
                )
        except ValueError as error:
            cleanup_saved_uploads(saved_stl_filename, saved_photo_filename)
            flash(str(error), "danger")
            return render_template("upload.html", form=form)
        except OSError:
            cleanup_saved_uploads(saved_stl_filename, saved_photo_filename)
            flash("Помилка збереження файлів. Перевірте розмір файлів і повторіть спробу.", "danger")
            return render_template("upload.html", form=form)

        model = Model(
            author=current_user,
            name=form.name.data.strip(),
            description=(form.description.data or "").strip() or None,
            original_filename=original_filename,
            stl_filename=saved_stl_filename,
            photo_filename=saved_photo_filename,
        )
        db.session.add(model)
        db.session.commit()
        flash("Модель успішно завантажено.", "success")
        return redirect(url_for("main.model_detail", model_id=model.id))

    return render_template("upload.html", form=form)


@main_bp.route("/profile")
@login_required
def profile():
    models = Model.query.filter_by(user_id=current_user.id).order_by(Model.created_at.desc()).all()
    return render_template("profile.html", models=models, delete_form=DeleteForm())


@main_bp.route("/model/<int:model_id>")
def model_detail(model_id):
    model = Model.query.get_or_404(model_id)
    return render_template("model_detail.html", model=model, delete_form=DeleteForm())


@main_bp.route("/download/<int:model_id>")
def download_model(model_id):
    model = Model.query.get_or_404(model_id)
    file_path = current_app.config["STL_UPLOAD_FOLDER"] / model.stl_filename
    if not file_path.exists():
        abort(404)

    model.downloads_count += 1
    db.session.commit()
    return send_from_directory(
        current_app.config["STL_UPLOAD_FOLDER"],
        model.stl_filename,
        as_attachment=True,
        download_name=secure_filename(model.original_filename) or "model.stl",
    )


@main_bp.route("/delete/<int:model_id>", methods=["POST"])
@login_required
def delete_model(model_id):
    form = DeleteForm()
    if not form.validate_on_submit():
        abort(400)

    model = Model.query.get_or_404(model_id)
    if model.user_id != current_user.id:
        abort(403)

    remove_file_if_exists(current_app.config["STL_UPLOAD_FOLDER"], model.stl_filename)
    remove_file_if_exists(current_app.config["PHOTO_UPLOAD_FOLDER"], model.photo_filename)
    db.session.delete(model)
    db.session.commit()
    flash("Модель видалено.", "info")
    return redirect(url_for("main.profile"))
