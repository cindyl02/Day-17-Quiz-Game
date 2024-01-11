from quiz_brain import QuizBrain
from data import question_data
from question_model import Question
import pytest


@pytest.fixture
def my_quiz_brain():
    question_bank = []

    for question in question_data:
        question_text = question["question"]
        question_answer = question["correct_answer"]
        new_question = Question(question_text, question_answer)
        question_bank.append(new_question)

    return QuizBrain(question_bank)


def test_next_question(my_quiz_brain, monkeypatch):
    inputs = ["True", "True", "True", "False", "False", "False", "True", "True", "False", "True"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

    assert my_quiz_brain.still_has_questions()
    for _ in range(len(question_data)):
        my_quiz_brain.next_question()
    assert not my_quiz_brain.still_has_questions()

def test_correct_answer(my_quiz_brain, monkeypatch, capfd):
    inputs = ["True"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    my_quiz_brain.next_question()
    out, err = capfd.readouterr()
    assert "You got it right!" in out
    assert "The correct answer was: True"
    assert "Your current score is: 1 / 1"
    assert my_quiz_brain.score == 1

def test_wrong_answer(my_quiz_brain, monkeypatch, capfd):
    inputs = ["False"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    my_quiz_brain.next_question()
    out, err = capfd.readouterr()
    assert "That's wrong." in out
    assert "The correct answer was: True"
    assert "Your current score is: 0 / 1"
    assert my_quiz_brain.score == 0

