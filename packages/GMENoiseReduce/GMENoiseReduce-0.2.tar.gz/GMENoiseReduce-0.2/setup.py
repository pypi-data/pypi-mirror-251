from distutils.core import setup
setup(
  name = 'GMENoiseReduce',         # How you named your package folder (MyLib)
  packages = ['GMENoiseReduce'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Generalised Maximum Entropy white noise Elimination',   # Give a short description about your library
  author = 'Eric Homan',                   # Type in your name
  author_email = 'ejhoman92@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/erichoman/GMENoiseReduce',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Noise', 'Noise-reduction', 'Noise removal'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy'
      ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)