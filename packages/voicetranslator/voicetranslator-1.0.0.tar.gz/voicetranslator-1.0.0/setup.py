from setuptools import setup, find_packages

setup(
    name='voicetranslator',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={'voicetranslator': ['*.pyd', '*.exe','*.txt']},
    install_requires=[
        # Lista de dependencias requeridas para tu proyecto
    ],
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
)

    
    
