try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='simple_message_queue)',
    description='Simple message queue implemented by redis.',
    version='0.0.0',
    packages=['simple_message_queue',],
    license='MIT',
    author='jokaye',
    author_email='jokaye@gmail.com',
    url='https://github.com/jokaye/simple-message-queue',
    keywords='redis message queue',
    long_description='',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
