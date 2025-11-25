from setuptools import find_packages, setup

package_name = "rqt_crazyflies_add"

data_files = []


data_files.append(
    ("share/ament_index/resource_index/packages", ["resource/" + package_name])
)

data_files.append(
    (
        "share/" + package_name + "/resource",
        [
            "resource/crazyflies_add.ui",
        ],
    )
)

data_files.append(("share/" + package_name, ["package.xml"]))
data_files.append(("share/" + package_name, ["add_plugin.xml"]))

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=data_files,
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="winni",
    maintainer_email="vinzenz.malke@uni-a.de",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [],
    },
)
