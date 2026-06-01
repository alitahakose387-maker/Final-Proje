from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PromptForm(FlaskForm):
    title = StringField("Başlık", validators=[DataRequired(), Length(max=200)])
    prompt_text = TextAreaField("Prompt Metni", validators=[DataRequired()])
    ai_tool = SelectField(
        "AI Aracı",
        choices=[
            ("ChatGPT", "ChatGPT"),
            ("Gemini", "Gemini"),
            ("Midjourney", "Midjourney"),
            ("DALL-E", "DALL-E"),
            ("Claude", "Claude"),
            ("Copilot", "Copilot"),
            ("Diğer", "Diğer"),
        ],
    )
    submit = SubmitField("Paylaş")


class CommentForm(FlaskForm):
    body = TextAreaField("Yorumunuz", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Yorum Yap")

