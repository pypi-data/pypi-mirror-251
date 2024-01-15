import setuptools

PACKAGE_NAME = "google-contact-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
     name='google-contact-local',
     version='0.0.1',  # https://pypi.org/project/google-contact-local-python-package/
     author="Circles",
     author_email="valeria.e@circ.zone",
     description="PyPI Package for Circles google-contact-local Python",
     long_description="PyPI Package for Circles google-contact-local Python",
     long_description_content_type="text/markdown",
     url="https://github.com/circles-zone/google-contact-local-python-package",
     packages=[package_dir],
     package_dir={package_dir: f'{package_dir}/src'},
     package_data={package_dir: ['*.py']},
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
     ],
 )
