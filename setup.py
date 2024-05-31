# -*- coding: utf-8 -*-
"""
Created on Tue May  7 10:09:21 2024

@author: Romain Perrier
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f :
    l_description = f.read()

setup(
      name = 'CTJ',
      version = '1.0.1',
      packages = find_packages(),
      url = 'https://github.com/RoPerrier/CTJ',
      install_requires =[
          'pillow>=10.2.0',
          'choix>=0.3.5',
          'numpy>=1.26.4',
          'scikit_learn>=1.2.2',
          'scipy>=1.11.4',
          'setuptools>=68.2.2',
            ],
      license = 'Apache 2.0',
      author = 'Romain Perrier',
      author_email ='romain.perrier2@etu.isima.fr',
      description = "Rubric Assesment, ACJ and CTJ Algorithms implementation.",
      long_description = l_description,
      long_description_content_type = "text/markdown",
      )
