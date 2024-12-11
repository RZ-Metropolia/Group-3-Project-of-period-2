from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, HiddenField  
from wtforms.validators import InputRequired, EqualTo, DataRequired

class SignupForm(FlaskForm):
    username = StringField(label="Username", validators=[InputRequired()])
    password = PasswordField(label="Password", validators=[InputRequired()])
    confirm_password = PasswordField(label="Confirm Password", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField(label="Sign Up")

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[InputRequired()])
    password = PasswordField(label="Password", validators=[InputRequired()])
    submit = SubmitField(label="Log In")  

class TravelForm(FlaskForm):
    destination = RadioField(label="Destination", choices=[])
    submit = SubmitField(label="Travel")

class BuyForm(FlaskForm):
    goods_id = HiddenField(label="Goods ID", validators=[DataRequired()])
    number = IntegerField(label="Number")
    submit = SubmitField(label="Buy")

class SellForm(FlaskForm):
    goods_id = HiddenField(label="Goods ID", validators=[DataRequired()])
    number = IntegerField(label="Number")
    submit = SubmitField(label="Sell")