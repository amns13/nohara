from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class CreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = CKEditorField('Body', validators=[DataRequired()])
    save = SubmitField(label='Save', id='save-submit-btn')
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})


class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()], render_kw={"rows": 7, "cols": 40})