from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.main import main_bp
from app.main.forms import PromptForm
from app.models import Prompt, Comment
from app.main.forms import CommentForm


@main_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    prompts = Prompt.query.order_by(Prompt.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template("main/index.html", prompts=prompts)


@main_bp.route("/prompt/<int:id>", methods=["GET", "POST"])
def detail(id):
    prompt = db.get_or_404(Prompt, id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Yorum yapabilmek için giriş yapmalısınız.", "warning")
            return redirect(url_for("auth.login"))
        comment = Comment(
            body=form.body.data, user_id=current_user.id, prompt_id=prompt.id
        )
        db.session.add(comment)
        db.session.commit()
        flash("Yorumunuz başarıyla eklendi.", "success")
        return redirect(url_for("main.detail", id=prompt.id))
    comments = prompt.comments.order_by(Comment.created_at.desc()).all()
    return render_template(
        "main/detail.html", prompt=prompt, form=form, comments=comments
    )


@main_bp.route("/prompt/new", methods=["GET", "POST"])
@login_required
def new_prompt():
    form = PromptForm()
    if form.validate_on_submit():
        prompt = Prompt(
            title=form.title.data,
            prompt_text=form.prompt_text.data,
            ai_tool=form.ai_tool.data,
            user_id=current_user.id,
        )
        db.session.add(prompt)
        db.session.commit()
        flash("Promptunuz başarıyla paylaşıldı!", "success")
        return redirect(url_for("main.detail", id=prompt.id))

    return render_template("main/form.html", form=form, title="Yeni Prompt Paylaş")


@main_bp.route("/prompt/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_prompt(id):
    prompt = db.get_or_404(Prompt, id)
    if prompt.user_id != current_user.id:
        abort(403)

    form = PromptForm(obj=prompt)
    if form.validate_on_submit():
        prompt.title = form.title.data
        prompt.prompt_text = form.prompt_text.data
        prompt.ai_tool = form.ai_tool.data
        db.session.commit()
        flash("Prompt başarıyla güncellendi.", "success")
        return redirect(url_for("main.detail", id=prompt.id))

    return render_template("main/form.html", form=form, title="Promptu Düzenle")


@main_bp.route("/prompt/delete/<int:id>", methods=["POST"])
@login_required
def delete_prompt(id):
    prompt = db.get_or_404(Prompt, id)
    if prompt.user_id != current_user.id:
        abort(403)

    db.session.delete(prompt)
    db.session.commit()
    flash("Prompt silindi.", "info")
    return redirect(url_for("main.index"))


@main_bp.route("/comment/delete/<int:id>", methods=["POST"])
@login_required
def delete_comment(id):
    comment = db.get_or_404(Comment, id)
    if comment.user_id != current_user.id:
        abort(403)
    prompt_id = comment.prompt_id
    db.session.delete(comment)
    db.session.commit()
    flash("Yorumunuz silindi.", "info")
    return redirect(url_for("main.detail", id=prompt_id))

