from setuptools import setup

setup(
    name='hvae_backbone',         # How you named your package folder (MyLib)
    packages=['hvae_backbone', 'hvae_backbone/elements'],
    version='0.1.8',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="Universal and customizable implementation of the Hierarchical Variational Autoencoder architecture.",   # Give a short description about your library
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='László Freund',                   # Type in your name
    author_email='freundl0509@gmail.com',      # Type in your E-Mail
    url='https://github.com/lacykaltgr/hvae-backbone',   # Provide either the link to your github or to your website
    keywords=['vae', 'hierarchical vae', 'generative model'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
        'torch',
        'numpy',
        'wandb',
        'tqdm',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)