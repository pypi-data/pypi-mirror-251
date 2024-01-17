from setuptools import setup

setup(
    name="copilotsdk",
    version="0.1.0",
    author="Won Zhou",
    author_email="wanzhou@cisco.com",
    description="A SDK for Webex troubleshooting copilot",
    url="https://sqbu-github.cisco.com/WebexAI/webex-ai",
    py_modules=["copilotsdk/__init__", "copilotsdk/copilot", "copilotsdk/ws"],
    data_files=[("", ["copilotsdk/README.md"])],
    package_dir={'': 'src'}
)
