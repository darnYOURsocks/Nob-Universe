from setuptools import find_packages, setup


setup(
    name="python-engine",
    version="0.1.0",
    description="Nob-Universe Phase 1 Python FastAPI engine",
    packages=find_packages(include=["app", "app.*"]),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "pydantic==2.5.0",
    ],
)
