from setuptools import setup, find_packages

setup(
    name='framecraft',
    version='0.2.3',
    description='by hyeonwoo jeong',
    author='hyeonu',
    author_email='hyeonu4945@gmail.com',
    url='https://github.com/HyeonuJeong/frame_craft',
    install_requires=['opencv-python','concurrent.futures','multiprocessing',],
    packages=find_packages(),
    keywords=['frame','video','capture'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
)