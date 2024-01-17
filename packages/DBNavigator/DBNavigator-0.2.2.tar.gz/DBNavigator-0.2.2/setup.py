import setuptools
with open(r'C:\Users\rost\Downloads\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='DBNavigator',
	version='0.2.2',
	author='Super_Zombi',
	author_email='super.zombi.yt@gmail.com',
	description='DataBase Navigator for Flask',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/SuperZombi/DBNavigator',
	packages=['db_navigator'],
	install_requires=["Jinja2", "Flask"],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)