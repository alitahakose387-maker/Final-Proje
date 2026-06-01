from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app import db
from app.auth import auth_bp
from app.auth.email import send_email
from app.auth.forms import LoginForm, RegisterForm
from app.auth.utils import confirm_token, generate_confirmation_token
from app.models import User


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_confirmed=False,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Token üret ve aktivasyon maili gönder
        token = generate_confirmation_token(user.email)
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)
        html = render_template(
            "auth/email/activate.html", confirm_url=confirm_url, user=user
        )
        subject = "Hesabınızı Aktifleştirin — PromptHub"
        try:
            send_email(user.email, subject, html)
            flash(
                "Hesabınız başarıyla oluşturuldu! Lütfen e-postanıza gönderilen onay linkine tıklayarak hesabınızı aktifleştirin.",
                "info",
            )
        except Exception as e:
            flash(
                f"Hesabınız oluşturuldu ancak onay e-postası gönderilirken bir hata oluştu: {str(e)}",
                "warning",
            )

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Geçersiz e-posta veya şifre.", "danger")
            return redirect(url_for("auth.login"))

        if not user.is_confirmed:
            flash(
                "Lütfen e-posta adresinize gönderilen onay linkine tıklayın.",
                "warning",
            )
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)
        flash("Giriş başarılı! Hoş geldiniz.", "success")

        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.index"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash("Onaylama linki geçersiz veya süresi dolmuş.", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        flash("Hesabınız zaten doğrulanmış. Lütfen giriş yapın.", "info")
    else:
        user.is_confirmed = True
        db.session.commit()
        flash(
            "Hesabınız başarıyla doğrulandı! Şimdi giriş yapabilirsiniz.", "success"
        )

    return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Çıkış yaptınız.", "info")
    return redirect(url_for("auth.login"))
