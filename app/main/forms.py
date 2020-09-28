from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class CreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = CKEditorField('Body', validators=[DataRequired()])
    save = SubmitField(label='Save', id='save-submit-btn')
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})