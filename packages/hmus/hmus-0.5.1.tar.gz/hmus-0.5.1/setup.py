from setuptools import setup, find_packages

"""
python setup.py sdist bdist_wheel
twine upload dist/*
"""

setup(
				name='hmus',
				version='0.5.1',
				author='LG125YT',
				author_email='lg125yt@gmail.com',
				description='This is a mirror package for hummus2016.py by LG125YT',
				long_description=open('README.md').read(),
				long_description_content_type='text/markdown',
				url='https://gitlab.com/lg125yt/hummus.py',
				packages=find_packages(),
				install_requires=[
								"discord.py",
								"asyncio",
								"fake_useragent",
								"websockets",
								"requests",
								"requests_toolbelt",
								"filetype",
								"Pillow",
				],
				classifiers=[
								'Development Status :: 3 - Alpha',
								'Intended Audience :: Developers',
								'License :: OSI Approved :: MIT License',
								'Operating System :: OS Independent',
								'Programming Language :: Python',
								'Programming Language :: Python :: 3',
								'Programming Language :: Python :: 3.6',
								'Programming Language :: Python :: 3.7',
								'Programming Language :: Python :: 3.8',
								'Programming Language :: Python :: 3.9',
								'Programming Language :: Python :: 3.10',
								'Programming Language :: Python :: 3.11',
				],
)