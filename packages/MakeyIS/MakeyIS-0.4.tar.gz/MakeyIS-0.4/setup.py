from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='MakeyIS',
    version='0.4',
    author='Makeenkov Igor',
    author_email='pro100igo228@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'allure-pytest',
        'allure-python-commons',
    ],
    description='Упрощение работы с параметрами pytest и простое логирование',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
