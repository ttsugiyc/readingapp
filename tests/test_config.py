def test_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_pass(app):
        Recorder.called = True

    monkeypatch.setattr('readingapp.config.init_pass', fake_init_pass)
    init_pass_result = runner.invoke(args=['init-pass'])
    assert 'configuration' in init_pass_result.output
    assert Recorder.called


def test_set_config():
    pass
