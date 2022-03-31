import os
from flask_wtf import FlaskForm
from flask import Flask, render_template
from wtforms import IntegerField, SelectField, widgets

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")


class MyForm(FlaskForm):
    test_points = IntegerField(
        "Písemná práce - počet bodů", widget=widgets.Input(input_type="number")
    )
    oral_exam_points = IntegerField(
        "Ústní zkouška - počet bodů", widget=widgets.Input(input_type="number")
    )
    languages = SelectField("Vyberte jazyk", choices=["anglický jazyk", "český jazyk"])


def calculate_score_eng(test_points, oral_exam_points):
    # kritéria pro hodnocení profilové části maturitní zkoušky jazyka anglického
    # rok 2022
    min_points_test = 16
    max_points_test = 36
    test_coef = 0.4
    min_points_oral_exam = 18
    max_point_oral_exam = 39
    oral_exam_coef = 0.6

    if test_points < min_points_test or oral_exam_points < min_points_oral_exam:
        return "Nedosažení minimálního počtu bodů - opakování příslušné části profilové maturitní zkoušky"
    elif test_points > max_points_test:
        return "Maximální počet bodů pro písemnou práci je 36"
    elif oral_exam_points > max_point_oral_exam:
        return "Maximální počet bodů pro ústní zkoušku je 39"
    else:
        test_perc = test_points / (max_points_test / 100) * test_coef
        oral_exam_perc = oral_exam_points / (max_point_oral_exam / 100) * oral_exam_coef
        perc = test_perc + oral_exam_perc
        if 87 < perc <= 100:
            return "Výborný - 1"
        elif 73 < perc <= 87:
            return "Chvalitebný - 2"
        elif 58 < perc <= 73:
            return "Dobrý - 3"
        elif 44 <= perc <= 58:
            return "Dostatečný - 4"
        elif perc < 44:
            return "Nedostatečný - 5"
        else:
            return "Někde se stala chyba."


def calculate_score_cze(test_points, oral_exam_points):
    # kritéria pro hodnocení profilové části maturitní zkoušky jazyka českého
    # rok 2022
    min_points_test = 12
    max_points_test = 30
    test_coef = 0.4
    min_points_oral_exam = 13
    max_point_oral_exam = 28
    oral_exam_coef = 0.6

    if test_points < min_points_test or oral_exam_points < min_points_oral_exam:
        return "Nedosažení minimálního počtu bodů - opakování příslušné části profilové maturitní zkoušky"
    elif test_points > max_points_test:
        return "Maximální počet bodů pro písemnou práci je 30"
    elif oral_exam_points > max_point_oral_exam:
        return "Maximální počet bodů pro ústní zkoušku je 28"
    else:
        test_perc = test_points / (max_points_test / 100) * test_coef
        oral_exam_perc = oral_exam_points / (max_point_oral_exam / 100) * oral_exam_coef
        perc = test_perc + oral_exam_perc
        if 87 < perc <= 100:
            return "Výborný - 1"
        elif 73 < perc <= 87:
            return "Chvalitebný - 2"
        elif 58 < perc <= 73:
            return "Dobrý - 3"
        elif 44 <= perc <= 58:
            return "Dostatečný - 4"
        elif perc < 44:
            return "Nedostatečný - 5"
        else:
            return "Někde se stala chyba."


@app.route("/", methods=["GET", "POST"])
def show_score():
    form = MyForm()
    if form.validate_on_submit():
        test_points = form.test_points.data
        oral_exam_points = form.oral_exam_points.data
        language = form.languages.data

        if language == "anglický jazyk":
            result = calculate_score_eng(test_points, oral_exam_points)
            return render_template("index.html", result=result, form=form)
        elif language == "český jazyk":
            result = calculate_score_cze(test_points, oral_exam_points)
            return render_template("index.html", result=result, form=form)

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run()
    # app.run(debug=False)
