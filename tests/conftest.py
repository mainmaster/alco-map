def pytest_addoption(parser):
    parser.addoption("--ci", action="store", default=False
                     )

