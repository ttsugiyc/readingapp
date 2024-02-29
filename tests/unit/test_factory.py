import readingapp


def test_config():
    assert not readingapp.create_app().testing
    assert readingapp.create_app({}).testing
