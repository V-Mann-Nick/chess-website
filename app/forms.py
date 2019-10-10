from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, FloatField, SelectMultipleField, RadioField, SelectField, StringField, TextAreaField
from wtforms.validators import NumberRange, Optional, Regexp
from wtforms.widgets import html_params
from flask_wtf.file import FileField, FileRequired, FileAllowed


def select_multi_checkbox(field, ul_class='', **kwargs):
    kwargs.setdefault('type', 'checkbox')
    field_id = kwargs.pop('id', field.id)
    html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
    current_halfmove = 0
    for value, label, checked in field.iter_choices():
        choice_id = u'%s-%s' % (field_id, value)
        options = dict(kwargs, name=field.name, value=value, id=choice_id)
        if current_halfmove % 2 == 0:
            html.append(f'<strong> {int((current_halfmove + 2) / 2)}.</strong>')
        current_halfmove += 1
        if checked:
            options['checked'] = 'checked'
        html.append(u'<li><input %s /> ' % html_params(**options))
        html.append(u'<label for="%s">%s</label></li>' % (field_id, label))
    html.append(u'</ul>')
    return u''.join(html)


class NoValidationSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        """per_validation is disabled"""


class NoValidationSelectField(SelectField):
    def pre_validate(self, form):
        """per_validation is disabled"""


class NoValidationRadioField(RadioField):
    def pre_validate(self, form):
        """per_validation is disabled"""


class Upload(FlaskForm):
    pgn_text = TextAreaField('paste pgn')
    # upload = FileField('select pgn file', validators=[FileRequired(), FileAllowed(['pgn'], 'only pgn files')])
    upload = FileField('select pgn file', validators=[FileAllowed(['pgn'], 'only pgn files')])
    submit = SubmitField('upload')


class Options(FlaskForm):
    # (light_tile_color, dark_tile_color)
    color_pairs = [('#DCD7BC', '#7C7671'),
                   ('#C4BBAF', '#5C4742'),
                   ('#decdc3', '#7c4222')]
    color_choices = [(f'{pair[0]}/{pair[1]}',
                      f'<div class="colorPair">\
                            <div class="colorBox" style="background-color: {pair[0]}"></div>\
                            <div class="colorBox" style="background-color: {pair[1]}"></div>\
                        </div>') for pair in color_pairs]
    halfmoves = NoValidationSelectMultipleField('select moves to print board',
                                                widget=select_multi_checkbox,
                                                coerce=int)
    color = NoValidationRadioField('color templates', choices=color_choices, validators=[Optional()])
    color_custom_light = StringField('light-tile color',
                                     validators=[Optional(), Regexp('^#[\w\d]{6}$', message='Please give a hex-coded color')])
    color_custom_dark = StringField('dark-tile color',
                                    validators=[Optional(), Regexp('^#[\w\d]{6}$', message='Please give a hex-coded color')])
    paragraph_arrangement = NoValidationRadioField('paragraph arrangement',
                                                   choices=[('move-board-comment', 'move-board-comment (default)'),
                                                            ('board-move-comment', 'board-move-comment'),
                                                            ('move-comment-board', 'move-comment-board')],
                                                   validators=[Optional()])
    font_size = IntegerField('font size', validators=[Optional(), NumberRange(min=6, max=30)])
    font_name = NoValidationSelectField('font', choices=[('Helvetica', 'Helvetica'),
                                                         ('Courier', 'Courier'),
                                                         ('Times-Roman', 'Times-Roman')])
    page_margin = FloatField('page margin (cm)', validators=[Optional(), NumberRange(min=0, max=5)])
    page_format = NoValidationSelectField('page format', choices=[('A4', 'A4'), ('letter', 'letter')])
    column_gap = FloatField('column gap (cm)', validators=[Optional(), NumberRange(min=0, max=6)])
    submit = SubmitField('refresh')
