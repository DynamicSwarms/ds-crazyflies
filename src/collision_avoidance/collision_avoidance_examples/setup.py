from setuptools import find_packages, setup

package_name = "collision_avoidance_examples"

data_files = []
data_files.append(
    ("share/ament_index/resource_index/packages", ["resource/" + package_name])
)
data_files.append(("share/" + package_name, ["package.xml"]))

data_files.append(("share/" + package_name + "/launch", ["launch/test.launch.py"]))


setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=data_files,
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="winni",
    maintainer_email="vinzenz@malke.info",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "collision_avoidance_test = collision_avoidance_examples.collision_avoidance_test:main"
        ],
    },
)
