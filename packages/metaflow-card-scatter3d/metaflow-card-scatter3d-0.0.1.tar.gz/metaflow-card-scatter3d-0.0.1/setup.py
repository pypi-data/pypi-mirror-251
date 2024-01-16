from setuptools import setup, find_namespace_packages

version = "0.0.1"

setup(
    name="metaflow-card-scatter3d",
    version=version,
    description="A dynamic card for Metaflow showing 2D or 3D scatter plots",
    author="Ville Tuulos",
    author_email="ville@outerbounds.co",
    packages=find_namespace_packages(include=["metaflow_extensions.*"]),
    py_modules=[
        "metaflow_extensions",
    ],
    install_requires=[
         "metaflow"
    ],
    package_data={"": ["scatter.js", "three.js", "base.html"]},
    include_package_data=True
)
