from setuptools import find_packages, setup

package_name = "crazyflies"
data_files = []
data_files.append(
    ("share/ament_index/resource_index/packages", ["resource/" + package_name])
)
data_files.append(("share/" + package_name, ["package.xml"]))
data_files.append(("share/" + package_name + "/launch", ["launch/framework.launch.py"]))
data_files.append(("share/" + package_name + "/launch", ["launch/safeflie.launch.py"]))


setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=data_files,
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="winni",
    maintainer_email="winni@todo.todo",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["crazyflie = crazyflies.crazyflie:main"],
        "console_scripts": ["safeflie = crazyflies.safeflie:main"],
        "console_scripts": [
            "position_visualization = crazyflies.position_visualization:main"
        ],
    },
)
