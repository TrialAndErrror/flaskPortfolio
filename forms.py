from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job_title = StringField('Title', validators=[DataRequired()])
    employer = StringField('Employer', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    important = BooleanField('Highlight')

    start_date = DateField('Start Date', format='%m/%d/%Y', validators=[DataRequired()])
    present_job = BooleanField('Current Job?')
    end_date = DateField('End Date', format='%m/%d/%Y')

    line_1 = StringField('Desc Line 1')
    line_2 = StringField('Desc Line 2')
    line_3 = StringField('Desc Line 3')
    line_4 = StringField('Desc Line 4')

    submit = SubmitField('Post')


class SchoolForm(FlaskForm):
    degree = StringField('Degree', validators=[DataRequired()])
    school_name = StringField('School Name', validators=[DataRequired()])

    graduation_date = DateField('Graduation Date', format='%m/%d/%Y', validators=[DataRequired()])

    line_1 = StringField('Desc Line 1')
    line_2 = StringField('Desc Line 2')
    line_3 = StringField('Desc Line 3')
    line_4 = StringField('Desc Line 4')

    submit = SubmitField('Post')


class ExtraForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    text = StringField('Description', validators=[DataRequired()])

    submit = SubmitField('Post')
