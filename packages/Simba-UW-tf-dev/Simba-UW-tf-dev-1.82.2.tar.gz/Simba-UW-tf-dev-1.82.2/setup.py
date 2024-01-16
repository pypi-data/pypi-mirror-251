"""
SimBA (Simple Behavioral Analysis)
https://github.com/sgoldenlab/simba
Contributors.
https://github.com/sgoldenlab/simba#contributors-
Licensed under GNU Lesser General Public License v3.0
"""

import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="Simba-UW-tf-dev",
            version="1.82.2",
    author="Simon Nilsson, Jia Jie Choong, Sophia Hwang",
    author_email="sronilsson@gmail.com",
    description="Toolkit for classification of behaviors in experimental animals",
    long_description='''\
    
    SimBA (Simple Behavioral Analysis) is a platform for analyzing behaviors of experimental animals within video recordings.
    
    <p align="center" style="width: 65%;">
    ![SimBA splash](https://github.com/sgoldenlab/simba/blob/master/docs/_static/img/splash_soft.png)
    </p>
    
    See below for raison d'être, detailed API, tutorials, data, documentation, support, and walkthroughs:
    
    * [GitHub](https://github.com/sgoldenlab/simba)
    * [readthedocs](https://simba-uw-tf-dev.readthedocs.io/en/latest/)
    * [API](https://simba-uw-tf-dev.readthedocs.io/en/latest/api.html)
    * [Gitter](https://app.gitter.im/#/room/#SimBA-Resource_community:gitter.im)
    * [biorxiv](https://www.biorxiv.org/content/10.1101/2020.04.19.049452v2)
    * [OSF](https://osf.io/tmu6y/)
    
    For installation: 
    ```
    pip install simba-uw-tf-dev
    ```
    
    If you make use of the code, please cite:
    
    @article{Nilsson2020.04.19.049452,
    author = {Nilsson, Simon RO and Goodwin, Nastacia L. and Choong, Jia Jie and Hwang, Sophia and Wright, Hayden R and Norville, Zane C and Tong, Xiaoyu and Lin, Dayu and Bentzley, Brandon S. and Eshel, Neir and McLaughlin, Ryan J and Golden, Sam A.},
    title = {Simple Behavioral Analysis (SimBA) {\textendash} an open source toolkit for computer classification of complex social behaviors in experimental animals},
    elocation-id = {2020.04.19.049452},
    year = {2020},
    doi = {10.1101/2020.04.19.049452},
    publisher = {Cold Spring Harbor Laboratory},
    URL = {https://www.biorxiv.org/content/early/2020/04/21/2020.04.19.049452},
    eprint = {https://www.biorxiv.org/content/early/2020/04/21/2020.04.19.049452.full.pdf},
    journal = {bioRxiv}}

    ''',
    long_description_content_type='text/markdown',
    url="https://github.com/sgoldenlab/simba",
    install_requires=requirements,
    license='GNU Lesser General Public License v3 (LGPLv3)',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ),
    entry_points={'console_scripts':['simba=simba.SimBA:main'],}
)
