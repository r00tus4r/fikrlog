from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(label='Foydalanuvchi nomi', validators=[DataRequired(message='Foydalanuvchi nomi kiritilishi shart.'), Length(min=3, max=64, message='Foydalanuvchi nomi 3 dan 64 ta belgigacha bo‘lishi kerak.')], description='Iltimos, foydalanuvchi nomingizni kiriting.')
    password = PasswordField(label='Parol', validators=[DataRequired(message='Parol kiritilishi shart.'), Length(min=12, message='Parol kamida 12 ta belgidan iborat bo‘lishi kerak.')], description='Parolingizni kiriting.')
    submit = SubmitField(label='Tizimga kirish')

class FikrForm(FlaskForm):
    title = StringField(label='Sarlavha', validators=[DataRequired(message='Sarlavha kiritilishi shart.'), Length(max=128, message='Sarlavha 128 belgidan oshmasligi kerak.')], description='Fikringiz uchun qisqa sarlavha kiriting.')
    content = TextAreaField(label='Fikr matni', validators=[DataRequired(message='Fikr matni bo‘sh bo‘lishi mumkin emas.')], description='Fikringizni shu yerga yozing.')
    submit = SubmitField(label='Saqlash')