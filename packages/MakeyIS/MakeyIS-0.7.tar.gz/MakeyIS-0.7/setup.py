from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='MakeyIS',
    version='0.7',
    author='Makeenkov Igor',
    author_email='pro100igo228@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'allure-pytest',
        'allure-python-commons',
    ],
    description='Библиотека обеспечивает усовершенствованное управление параметрами PyTest и логирование, упрощая создание и отладку автоматизированных тестов за счет интуитивно понятных декораторов и продвинутых функций логирования. Она идеально подходит для повышения эффективности и наглядности процесса тестирования.',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
