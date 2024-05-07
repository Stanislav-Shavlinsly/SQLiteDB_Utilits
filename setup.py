from setuptools import setup, find_packages

setup(
    name='SQLiteDB_utils',
    version='0.1.3',
    author='Stanislav Shavlinsky',
    author_email='stanislave777@gmail.com',
    description='Набор утилит для работы с БД SQLite',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Stanislav-Shavlinsly/web3_utils',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    entry_points={
        # Ваши консольные скрипты или точки входа
    },
    include_package_data=True,
    package_data={
        # Опционально: включаемые данные пакета
    },
    # Другие параметры...
)
