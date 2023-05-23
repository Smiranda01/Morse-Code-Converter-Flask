from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp
from _datetime import datetime
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
load_dotenv()

morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..'
}


class MorseConvertForm(FlaskForm):
    string = StringField("Enter the string you want to convert", validators=[DataRequired(), Regexp(r'^[a-zA-Z\s]*$', message="Only letters are allowed.")])
    submit = SubmitField(label="Submit")


def convert_to_morse(string):
    string_list = list(string)
    morse_word_list = []
    for char in string_list:
        if char == " ":
            morse_word_list.append("  ")
        else:
            morse_char = morse_code[char] + "/"
            morse_word_list.append(morse_char)
    morse_word = "".join(morse_word_list)
    return morse_word


@app.route("/", methods=["GET", "POST"])
def convert():
    year = datetime.now().year
    form = MorseConvertForm()
    if form.validate_on_submit():
        string = form.string.data.upper()
        converted_word = convert_to_morse(string)
        print(converted_word)
        return render_template("converted.html", word=string, converted_word=converted_word)
    return render_template("index.html", form=form, current_year=year)


if __name__ == "__main__":
    app.run(debug=True)
