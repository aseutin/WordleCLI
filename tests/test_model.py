from model.wordle_model import WordleModel, Accuracy


def test_outcome_exists():
    model = WordleModel()
    winning_word = model.winning_word
    outcome = model.guess(winning_word)
    assert outcome is not None


def test_outcome_for_winning_word():
    model = WordleModel()
    winning_word = model.winning_word
    outcome = model.guess(winning_word)
    assert all([accuracy == Accuracy.CORRECT for accuracy in outcome])


def test_outcome_for_non_winning_word():
    model = WordleModel()
    winning_word = model.winning_word

    # non zero chance winning word is hardcoded word -> add backup
    word_to_guess = (
        model.vocabulary[0]
        if winning_word != model.vocabulary[0]
        else model.vocabulary[1]
    )

    outcome = model.guess(word_to_guess)
    assert outcome is not None
    assert not all([accuracy == Accuracy.CORRECT for accuracy in outcome])


def test_no_outcome_for_short_word():
    model = WordleModel()
    outcome = model.guess("ok")
    assert outcome is None


def test_no_outcome_for_fake_word():
    model = WordleModel()
    outcome = model.guess("abcde")
    assert outcome is None


def test_outcome_for_second_guess():
    model = WordleModel()
    winning_word = model.winning_word

    for i in range(2):
        # non zero chance winning word is hardcoded word -> add backup
        # also guarantee that second word cannot be the same as first
        word_to_guess = (
            model.vocabulary[2 * i]
            if winning_word != model.vocabulary[2 * i]
            else model.vocabulary[(2 * i) + 1]
        )

        outcome = model.guess(word_to_guess)
        assert outcome is not None
        assert not all([accuracy == Accuracy.CORRECT for accuracy in outcome])


def test_no_outcome_for_seventh_bad_guess():
    model = WordleModel()
    winning_word = model.winning_word

    for i in range(6):
        # non zero chance winning word is hardcoded word -> add backup
        # also guarantee that second word cannot be the same as first
        word_to_guess = (
            model.vocabulary[2 * i]
            if winning_word != model.vocabulary[2 * i]
            else model.vocabulary[(2 * i) + 1]
        )

        outcome = model.guess(word_to_guess)
        assert outcome is not None
        assert not all([accuracy == Accuracy.CORRECT for accuracy in outcome])

    final_guess = (
        model.winning_word
    )  # safe to use because we have not tried this yet and it is guaranteed to be a valid word
    outcome = model.guess(final_guess)
    assert outcome is None
