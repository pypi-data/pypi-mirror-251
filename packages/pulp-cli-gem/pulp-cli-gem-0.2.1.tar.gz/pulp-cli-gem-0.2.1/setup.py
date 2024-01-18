from setuptools import setup

try:
    from setuptools import find_namespace_packages

    plugin_packages = find_namespace_packages(include=["pulpcore.cli.*"])

except ImportError:
    # Old versions of setuptools do not provide `find_namespace_packages`
    # see https://github.com/pulp/pulp-cli/issues/248
    from setuptools import find_packages

    plugins = find_packages(where="pulpcore/cli")
    plugin_packages = [f"pulpcore.cli.{plugin}" for plugin in plugins]

plugin_entry_points = [(package.rsplit(".", 1)[-1], package) for package in plugin_packages]


setup(
    name="pulp-cli-gem",
    description="Command line interface to talk to pulpcore's REST API. (Gem plugin commands)",
    url="https://github.com/pulp/pulp-cli-gem",
    version="0.2.1",
    packages=plugin_packages,
    package_data={package: ["py.typed"] for package in plugin_packages},
    python_requires=">=3.6",
    install_requires=["pulp-cli>=0.20.0,<0.23.0.dev", "pulp-glue-gem==0.2.1"],
    entry_points={
        "pulp_cli.plugins": [f"{name}={module}" for name, module in plugin_entry_points],
    },
    license="GPLv2+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Software Distribution",
        "Typing :: Typed",
    ],
)
