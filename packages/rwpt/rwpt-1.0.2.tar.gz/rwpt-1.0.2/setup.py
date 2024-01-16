from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
readme_file = this_directory / 'README.md'

with open(readme_file, mode='r', encoding='utf-8') as f:
    readme_text = ''.join(f.readlines())
# end with

setup(
    name='rwpt',
    version='1.0.2',
    description='A Romanian WordPiece tokenizer',
    url='https://github.com/racai-ai/ro-wordpiece-tokenizer',
    author='Radu Ion',
    author_email='radu@racai.ro',
    license='MIT License',
    packages=['rwpt'],
    # Developed with tokenizers==0.13.3 and transformers==4.33.3
    install_requires=['tokenizers>=0.13.0', 'transformers<5.0.0'],
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description=readme_text,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Natural Language :: Romanian',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: Linguistic'
    ]
)
