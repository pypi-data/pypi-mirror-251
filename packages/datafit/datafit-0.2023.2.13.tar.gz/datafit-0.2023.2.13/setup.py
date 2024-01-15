from setuptools import setup, find_packages

longDescription = """
# DataFit: Automated Data Preprocessing in Python

**Note: This package is actively under development and is open source.**

## Overview

DataFit is a powerful Python package developed by Syed Syab and Hamza Rustam for automating data preprocessing tasks. Initiated as part of our Final Year Project at the University of Swat, this tool streamlines the data preprocessing pipeline, making it user-friendly for machine learning engineers and data scientists.

- **Project Initialization Date:** 01/OCT/2023
- **Expected Project Finalization Date:** 01/Dec/2023 (Initial Release) (Still under development)

## Team Members

1. **Professor Naeem Ullah (Supervisor)**
    - [Facebook](https://facebook.com/Naeem-Munna?mibextid=PzaGJu)
    - Email: naeem@uswat.edu.pk

2. **Syed Syab (Student)**
    - [GitHub](https://github.com/SyabAhmad)
    - [LinkedIn](https://linkedin.com/SyedSyab)
    - Email: syab.se@hotmail.com

3. **Hamza Rustam (Student)**
    - [GitHub](https://github.com/Hamza-Rustam)
    - [LinkedIn](https://linkedin.com/hamza-rustam-845a2b209)
    - Email: hs4647213@gmail.com

## Package Functionality

The DataFit package is designed with a user-friendly interface, ensuring accessibility for all users. Its current functionality includes:

- Displaying information about the dataset
- Handling null values
- Deleting multiple columns
- Handling categorical values
- Normalization
- Standardization
- Extracting numeric values
- Tokenization

## Usage

To use the package, install it using:

```bash
pip install datafit
```

Once installed, import it like Pandas and start using it:

```python
import datafit.datafit as df

# Display information about the data
df.information(data)
```

To handle categorical values:

```python
import datafit.datafit as df

# Specify columns to handle or use None for all columns
df.handleCategoricalValues(data, ["column1", "column2"])
```

To extract numerical values from columns:

```python
import datafit.datafit as df

# Specify columns for extraction
df.extractValues(data, ["column1", "column2"])
```

New Updates in **version=0.2023.2.13**:

```Description updated```

**Note:** This package is actively under development. Feel free to share and follow on [GitHub](https://github.com/SyabAhmad) and [LinkedIn](https://linkedin.com/SyedSyab) for updates.

Your support is appreciated!

"""


setup(
    name='datafit',
    version='0.2023.2.13',
    description='This is a Python package that automates the data preprocessing',
    long_description=longDescription,
    long_description_content_type='text/markdown',  # Specify the type of content as Markdown
    author='Naeem Ullah, Syed Syab, Hamza Rustam',
    #secondauthor = 'Hamza Rustam',
    #supervisor = 'Naeem Ullah',
    #author_email='syab.se@hotmail.com',
    #secondauthor_email = 'hs4647213@gmail.com',
    #supervisor_email = 'naeem@uswat.edu.pk',
    url='https://github.com/SyabAhmad/datafit',
    license='MIT',

    packages=find_packages(),
    install_requires=[
        'numpy>=1.0',
        'pandas>=1.0',
        'scikit-learn',

    ],
    #
    # # Entry points for command-line scripts if applicable
    # entry_points={
    #     'console_scripts': [
    #         'my_script = __init__.py',
    #     ],
    # },

    # Other optional metadata
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        # Add more classifiers as appropriate
    ],
)