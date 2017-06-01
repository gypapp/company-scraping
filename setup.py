from setuptools import setup, find_packages

setup(
    name='companyscraping',
    version='0.1',
    packages=find_packages(),
    package_data={
        'companyscraping': ['resources/*.csv']
    },
    entry_points={
        'scrapy': ['settings = companyscraping.settings']
    },
    include_package_data=True,
    zip_safe=False,
)
