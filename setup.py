from setuptools import setup, find_packages
"""
https://stackoverflow.com/questions/39499453/package-only-binary-compiled-so-files-of-a-python-library-compiled-with-cython
set up the extensions 
supress gomodule
"""

def parse_requirements(filename):
    """
    load requirements from a pip requirements file
    """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


setup(
    name="Tameshite",
    version="1.0",
    description="""Tameshite Kudasai
            Lets you stress test your WebApp with various DDoS attacks""",
    author="LTIFI Azer",
    packages=find_packages(include=['tameshite', 'tameshite.*']),
    include_package_data=True,
    url="https://github.com/azseza/tamashite",
    install_requires=parse_requirements("requirements.txt"),
    classifiers=[
        'Development Status :: 1 - Beta',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers and linux users",
        "Environment :: Console"
        "Operating System :: Linux"
        ],
     entry_points='''
        [console_scripts]
        Tameshite=tameshite.Tameshite:main
    ''',
    )

