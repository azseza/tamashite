from setuptools import setup

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]
setup(
    name="Tameshite",
    py_modules=["Tameshite","ntpL4"],
    version="1.0",
    description="""Tameshite Kudasai
            Lets you stress test your WebApp with various DDoS attacks""",
    author="LTIFI Azer",
    url="https://github.com/azseza/tamashite",
    install_requires=load_requirements("requirements.txt"),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers and linux power users",
        "Environment :: Console"
        "Operating System :: Linux"
        ],
     entry_points='''
        [console_scripts]
        Tameshite=Tameshite:main
    ''',
    )