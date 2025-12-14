from setuptools import setup, find_packages

# VULNERABILITY: Yet another set of dependency versions
setup(
    name="billing-service",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.60.0",
        "uvicorn>=0.11.0",
        "sqlalchemy>=1.3.0",
        # VULNERABILITY: Overly permissive version ranges
        "PyYAML>=5.0",
        "Pillow>=7.0.0",
        "requests>=2.18.0",
        "Jinja2>=2.10",
        # VULNERABILITY: No upper bounds on versions
        "stripe",
        "python-jose",
        "passlib",
    ],
    python_requires=">=3.7",
)
