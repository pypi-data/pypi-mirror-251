from setuptools import setup, find_packages

with open("README.md","r",encoding="utf-8") as f:
    long_des=f.read()
    
setup(
    name='voicetranslator',
    version='1.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={'voicetranslator': ['*.pyd', '*.exe','*.txt']},
    description="Real time translation for live streams",
    long_description=long_des,
    long_description_content_type="text/markdown",
    url="https://github.com/voicetranslator/voicetranslator",
    project_urls={"Documentation":"https://github.com/voicetranslator/voicetranslator"},
    install_requires=[
        # Lista de dependencias requeridas para tu proyecto
    ],
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
)

    
    
