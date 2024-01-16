
import sys 

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# invalid email
# download url
# url
# project urls

setup(
    name = "M4Z4LWJsiOWnNGQzNy1i",
    packages=[],
    version='0.0.0',
    options={
        'sdist': {'formats': ['zip']},
    },
    zip_safe=False,
    description='DESCRIPTION',
    long_description="LONG_DESCRIPTION",
    long_description_content_type='text/markdown',
    author='Development Team',
    author_email='test@test.com',
    url='https://url.com',
    download_url='https://download_url.com',
    keywords="python3 python",
    project_urls={
            'Source': 'https://github.com/source',
    },
    install_requires="",
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    license='MIT',
)

    