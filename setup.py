import setuptools


long_description = """
# test.helper.yandex.alice.flask

Class for autotests YandexAlice skill, that implemented as flask application
"""

setuptools.setup(
    name = 'tester_alice_skill_flask',
    version = '1.1',
    author = 'Vitaly Bogomolov',
    author_email = 'mail@vitaly-bogomolov.ru',
    description = 'Class for autotests YandexAlice skill, that implemented as flask application',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/vb64/test.helper.yandex.alice.flask',
    packages = ['tester_alice_skill_flask'],
    download_url = 'https://github.com/vb64/test.helper.yandex.alice.flask/archive/v1.1.tar.gz',
    keywords = ['python', 'Yandex.Alice', 'flask', 'unittest'],
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
