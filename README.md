# CTJ

## Table of contents
- [Description](#description)
- [Installation](#installation)
- [Structure](#structure)
- [Usage](#usage)
    - [For predictive purposes](#for-predictive-purposes)
    - [For testing purposes](#for-testing-purposes)
    - [For verifying purposes](#for-verifying-purposes)
    - [Tutorial](#tutorial)
- [Dependencies](#dependencies)
- [Module Documentation](#module-documentation)
    - [Assessment Algorithms](#assessment-algorithms)
        - [Rubric Algorithm](#rubric-algorithm)
        - [ACJ Algorithm](#acj-algorithm)
        - [CTJ Algorithm](#ctj-algorithm)
    - [Assessment Methods](#assessment-methods)
        - [Rubric Assessment Method](#rubric-assessment-method)
        - [ACJ Assessment Method](#acj-assessment-method)
        - [CTJ Assessment Method](#ctj-assessment-method)

## Description <a name="#description"></a>

The `CTJ` package implements the comparative triple judgement algorithm devised by Dr. Kevin Kelly. The aim of this algorithm is to improve the accuracy of `ACJ` (adaptive comparative judgement). Instead of comparing elements two by two, they are compared three by three, and a notion of distance between elements is added to the algorithm. `CTJ` was devised by Dr. Kevin Kelly.

This package therefore proposes an implementation of the `CTJ`, the `ACJ`, and the `Rubric` judgment, to enable a more precise analysis of the `CTJ` and to compare its performance with other methods. To do this, pairs and trios are selected with similar methods using Shannon entropy.

## Installation 

Pull or fork the repository, navigate to the root directory, and use the following commands:

```
python setup.py sdist bdist_wheel
```

```
pip install ./dist/CTJ-1.1.6-py3-none-any.whl
```

Or depending of your version of python :

```
pip3 install ./dist/CTJ-1.1.6-py3-none-any.whl
```

Then you need to restart the Python kernel to finish the installation.

## Structure
```
CTJ/
    ├── CTJ/
    |       ├── __init__.py
    |       ├── ACJ.py
    |       ├── assessment_method.py
    |       ├── CTJ.py
    |       ├── Rubric.py
    |       ├── selection.py
    |       └── util.py
    ├── Notebook/
    |       ├── ACJ-Tutorial.ipynb
    |       ├── black.png
    |       ├── CTJ-Tutorial.ipynb
    |       ├── g1.png
    |       ├── g2.png
    |       ├── g3.png
    |       ├── g4.png
    |       ├── g5.png
    |       ├── Rubric-Tutorial.ipynb
    |       └── white.png
    ├── Test/
    |       ├── Manual_testing/
    |       |        ├── Accuracy.png
    |       |        ├── Analyse.py
    |       |        ├── README.txt
    |       |        ├── real_test.csv
    |       |        ├── threshold.py
    |       |        └── time.png
    |       ├── Nb_errors/
    |       |        ├── 30.csv
    |       |        ├── 30_accuracy.png
    |       |        ├── 30_iteration.png
    |       |        ├── 30_proba.png
    |       |        ├── 60.csv
    |       |        ├── 60_accuracy.png
    |       |        ├── 60_iteration.png
    |       |        ├── 60_proba.png
    |       |        ├── 90.csv
    |       |        ├── 90_accuracy.png
    |       |        ├── 90_iteration.png
    |       |        ├── 90_proba.png
    |       |        ├── gather_data.py
    |       |        ├── nb_errors_data.py
    |       |        └── README.txt
    |       ├── Scale_errors/
    |       |        ├── error_scale.py
    |       |        ├── error_scale_1.csv
    |       |        ├── error_scale_2.csv
    |       |        ├── error_scale_3.csv
    |       |        ├── error_scale_4.csv
    |       |        ├── eror_1.png
    |       |        ├── eror_2.png
    |       |        ├── eror_3.png
    |       |        ├── eror_4.png
    |       |        ├── gather_data.py
    |       |        └── README.txt
    |       └── Thresold/
    |                ├── accuracy.png
    |                ├── gather_data.py
    |                ├── Iteration.png
    |                ├── NB_of_errors.png
    |                ├── README.txt
    |                ├── thresold.csv
    |                └── thresold.py
    ├── fix_import_error_tkinter.md
    ├── Manifest.in
    ├── Readme.md
    └── setup.py
````

The CTJ project is organized into several directories and files that serve specific purposes. Here is a detailed explanation of each part of the project's architecture:

### Project Root

At the root of the project, you will find the main configuration files and basic documentation:

- **fix_import_error_tkinter.md**: Documentation to resolve Tkinter import errors.
- **Manifest.in**: Indicates which files should be included in the package distribution.
- **Readme.md**: General description of the project, installation, and usage instructions.
- **setup.py**: Configuration script for installing the package.

### CTJ Directory

This directory contains the main source code of the project:

- **CTJ/**
  - **\_\_init\_\_.py**: Initializes the CTJ package.
  - **ACJ.py**: Contains functions related to Adaptive Comparative Judgement (ACJ).
  - **assessment_method.py**: Implements visual assessment methods for each methods.
  - **CTJ.py**: Contains functions related to Comparative Triple Judgement (CTJ).
  - **Rubric.py**: Contains functions related to Rubric assessments.
  - **selection.py**: Contains selection logic, based on information theory.
  - **util.py**: Utility functions.

### Notebook Directory

This directory contains Jupyter notebooks for tutorials and visual examples:

- **ACJ-Tutorial.ipynb**: Tutorial on Adaptive Comparative Judgement.
- **CTJ-Tutorial.ipynb**: General tutorial on using the CTJ project.
- **Rubric-Tutorial.ipynb**: Tutorial on creating and using evaluation rubrics.
- **black.png, white.png, g1.png, g2.png, g3.png, g4.png, g5.png**: Images used in the notebooks for illustrations and graphs.

### Test Directory

This directory contains tests to validate the functionality of the project:

- **Manual_testing/**: Manual tests to verify accuracy and performance.
  - **Accuracy.png**: Accuracy graph of the tests.
  - **Analyse.py**: Script for analyzing test results.
  - **README.txt**: Instructions for manual tests.
  - **real_test.csv**: Real data for tests.
  - **threshold.py**:This script determines the threshold value set by a judge. It returns a list of points, with each subsequent point representing a less significant step than the previous one.
  - **time.png**: Execution time graph of the tests.

- **Nb_errors/**: Tests related to the number of errors.
  - **30.csv, 60.csv, 90.csv**: Data for tests with different error levels.
  - **30_accuracy.png, 60_accuracy.png, 90_accuracy.png**: Accuracy graphs for each error level.
  - **30_iteration.png, 60_iteration.png, 90_iteration.png**: Iteration graphs for each error level.
  - **30_proba.png, 60_proba.png, 90_proba.png**: Probability graphs for each error level.
  - **gather_data.py**: Script for gathering test data.
  - **nb_errors_data.py**: Main script for ploting result.
  - **README.txt**: Instructions for tests related to the number of errors.

- **Scale_errors/**: Tests related to error scaling.
  - **error_scale.py**: Main script for ploting result.
  - **error_scale_1.csv, error_scale_2.csv, error_scale_3.csv, error_scale_4.csv**: Data for each error scale.
  - **eror_1.png, eror_2.png, eror_3.png, eror_4.png**: Error graphs for each error scale.
  - **gather_data.py**: Script for gathering test data.
  - **README.txt**: Instructions for tests related to error scaling.

- **Thresold/**: Tests related to thresholds.
  - **accuracy.png**: Accuracy graph based on thresholds.
  - **gather_data.py**: Script for gathering test data.
  - **Iteration.png**: Iteration graph based on thresholds.
  - **NB_of_errors.png**: Number of errors graph based on thresholds.
  - **README.txt**: Instructions for tests related to thresholds.
  - **thresold.csv**: Threshold test data.
  - **thresold.py**: Main script for testing thresholds.

This structure organizes the source code, documentation, tests, and tutorials to facilitate the development, use, and maintenance of the CTJ project.

## Usage

```python
import CTJ

#OR

from CTJ import Rubric, ACJ, CTJ
```

You can use this package in three different ways.

For each of the ways, you will at least need to specify the list containing the names of your items, the two elements delimiting your sample (they may not be present in the items list, this is not a problem).

```py
# Here an example with shades of grey. All the items are present in the current directory, for example, 'g1' appears as 'g1.png' in the directory.
shade = ['g1', 'g2', 'g3', 'g4', 'g5']

# I use the grayscale from 0 to 255, so the highest score is 255 for white; it will be our best_element.
best_element = [255,'white']
worst_element = [0,'black']
```

* ### For predictive purposes

You have a list of elements that you want to evaluate, but you don't know their real values. In this case, you need to specify which method to use. You can use the method provided in the package or use a method that you've coded yourself.

Here the user needs to make assessments, so the items must be present in the directory where your script is located in PNG format. For example, if your script is named `myscript.py` and you use the shade and the bound defined before, your structure needs to be like this:

```
Your/Project/Folder/
    ├── myscript.py
    ├── black.png
    ├── g1.png
    ├── g2.png
    ├── g3.png
    ├── g4.png
    ├── g5.png
    └── white.png
````

I recommend using high accuracy because here, it is calculated with the previous estimation; a high accuracy will evaluate convergence of the estimated value in this case.

By using the incorporated function:

```py

from CTJ import rubric_assessment_method_image, acj_assessment_method_image, ctj_assessment_method_image

#OR IF YOU USE PDF

from CTJ import rubric_assessment_method_pdf, acj_assessment_method_pdf, ctj_assessment_method_pdf

Rubric(worst_element, best_element, shade, assessment_method = rubric_assessment_method_image)

ACJ(worst_element, best_element, shade, assessment_method = acj_assessment_method_image, max_accuracy = 0.99)

CTJ(worst_element, best_element, shade, assessment_method = ctj_assessment_method_image, max_accuracy = 0.99)

```

You can also use a modified version of ACJ, using the same optimisation than CTJ :

```py
ACJ(worst_element, best_element, shade, assessment_method = acj_assessment_method_image, entropy = True)
```
* ### For testing purposes

You have the real values and want to assess the value yourself. In this case, you need to specify which method to use. You can use the method provided in the package or use a method that you've coded yourself; also specify the real values in a list.

Here you don't need the representation of each item.

Here the user needs to make assessments, so the items must be present in the directory where your script is located in PNG format. For example, if your script is named `myscript.py` and you use the shade and the bound defined before, your structure needs to be like this:

```
Your/Project/Folder/
    ├── myscript.py
    ├── black.png
    ├── g1.png
    ├── g2.png
    ├── g3.png
    ├── g4.png
    ├── g5.png
    └── white.png
````

By using the incorporated function:

```py

from CTJ import rubric_assessment_method_image, acj_assessment_method_image, ctj_assessment_method_image

#OR IF YOU USE PDF

from CTJ import rubric_assessment_method_pdf, acj_assessment_method_pdf, ctj_assessment_method_pdf

real_values = [160, 106, 209, 80, 135]

Rubric(worst_element, best_element, shade, true_values = real_values, assessment_method = rubric_assessment_method_image)

ACJ(worst_element, best_element, shade, true_values = real_values, assessment_method = acj_assessment_method_image)

CTJ(worst_element, best_element, shade, true_values = real_values , assessment_method = ctj_assessment_method_image)

```

You can also use a modified version of ACJ, using the same optimisation than CTJ :

```py
ACJ(worst_element, best_element, shade, true_values = real_values, assessment_method = acj_assessment_method_image, entropy = True)
```

* ### For verifying purposes

You have the real values and want to check the efficiencies of the algorithms.

```py

real_values = [160, 106, 209, 80, 135]

Rubric(worst_element, best_element, shade, true_values = real_values)

ACJ(worst_element, best_element, shade, true_values = real_values)

CTJ(worst_element, best_element, shade, true_values = real_values)

```

You can also use a modified version of ACJ, using the same optimisation than CTJ :

```py
ACJ(worst_element, best_element, shade, true_values = real_values, entropy = True)
```

Furthermore, in this case, you could use the sensibility parameter to introduce some errors.

The `Rubric`'s sensibility is a tuple containing two elements.
The first value corresponds to the mistake that the user could make by judging an item, the second value is the probability of making a mistake.

```py

Rubric(worst_element, best_element, shade, true_values = real_values, sensibility = (mistake, proba))

```

The `ACJ`'s sensibility is a list of int.
Each int corresponds to the sensibility of a judge, the first int corresponds to the sensibility of the first judge, and etc..
The int represent the sensitivity threshold. If the margin between two items is equal to this value, there is a probability of 0.1 of inverting them. The probability is calculated with this sigmoid function:  $\frac{1}{1 + \exp\left(-\frac{\log\left(\frac{1}{9}\right)}{\text{sensibility}} \times x\right)}$ where x is the margin between two items. 

```py

ACJ(worst_element, best_element, shade, true_values = real_values, nb_judge = 2, sensibility = [gap_1, gap_2])

```

The `CTJ`'s sensibility is a tuple containing three elements.
The first value corresponds to the distance between the nearest item that the judge could misjudge with a propability of 0.1. We use also the sigmoid fonction to calculate the propability of inverting two element : $\frac{1}{1 + \exp\left(-\frac{\log\left(\frac{1}{9}\right)}{\text{sensibility[0]}} \times x\right)}$ where x is the absolute value of the gap betwween two items.. The second value is the mistake made on the scale, and the third value is the probability of making a scale error.

```py

CTJ(worst_element, best_element, shade, true_values = real_values, sensibility = (distance_error, scale_error, proba_scale_error))

```

### Tutorial

You can look at these jupyter notebook Tutorial :

- [Rubric Tutorial](https://github.com/RoPerrier/CTJ/blob/main/Notebook/Rubric-Tutorial.ipynb)
- [ACJ Tutorial](https://github.com/RoPerrier/CTJ/blob/main/Notebook/ACJ-Tutorial.ipynb)
- [CTJ Tutorial](https://github.com/RoPerrier/CTJ/blob/main/Notebook/CTJ-Tutorial.ipynb)

## Dependencies

- choix >= 0.3.5
- pillow >= 10.2.0
- numpy >= 1.24.3
- scikit-learn >= 1.3.0
- scipy >= 1.13.1
- random >= 1.2.4
- time >= 2.8.2
- itertools >= 8.12.0
- tkinter >= 8.6.12

## Module Documentation

### Assessment Algorithms

#### Rubric Algorithm

#### `CTJ.Rubric(min_item, max_item, items, sensibility=(0,0), true_values=None, assessment_method=None)`

`Rubric` Judgment is an evaluation method based on the direct notation of an item. An item is shown and we must evaluate it and give a value to it.

**Parameters:**

- `min_item` (*tuple*) – The min_item we want to use. In the format (*int*, *string*).
- `max_item` (*tuple*) – The max_item we want to use. In the format (*int*, *string*).
- `items` (*list of string*) – A list of strings representing the items to be assessed.
- `sensibility` (*tuple*) – A tuple containing the margin of error, and the probability of making a mistake. In the format (*int*, *double*).. The default is (0,0).
- `true_values` (*list of int, optional*) – A list of int containing the true values corresponding to each item in the `items` list. The default is None.
- `assessment_method` (*function, optional*) – The assessment method. If None, the assessment is automatically performed using the true value. The default is None.

**Returns:**

- `estimated_values` (*list of int*) – A list of int containing the estimated values corresponding to each item in the `items` list.
- (*int*) – Number of iterations.
- `cond` (*float*) – Accuracy of estimated value at the end of the algorithm.
- `error` (*int*) – Number of errors.
- `assessments_time` (*int*) – The duration of the assessments.

#### ACJ Algorithm

#### `CTJ.ACJ(min_item, max_item, items, nb_judge=1, sensibility=[0], true_values=None, max_iteration=30, max_accuracy=0.9, assessment_method=None)`

Adaptive Comparative Judgment (`ACJ`) is an evaluation method based on the comparison of pairs of items. Rather than scoring each item on a fixed scale, evaluators directly compare two items at a time and judge which is better according to certain criteria.

**Parameters:**

- `min_item` (*tuple*) – The min_item we want to use. In the format (*int*, *string*).
- `max_item` (*tuple*) – The max_item we want to use. In the format (*int*, *string*).
- `items` (*list of string*) – A list of strings representing the items to be assessed.
- `nb_judge` (*int, optional*) – The number of judges that make the evaluation. The default is 1.
- `sensibility` (*list of int*) – The sensitivity threshold. If the margin between two items is equal to this value, there is a 10% probability of inverting them. The probability is calculated with this sigmoid function:  1 / (1 + np.exp(-np.log(1/9) / sensibility * x)) where x is the margin between two items. The default is [0]

- `true_values` (*list of int, optional*) – A list of int containing the true values corresponding to each item in the `items` list. The default is None.
- `max_iteration` (*int, optional*) – Number of maximum iterations of the algorithm. The default is 30.
- `max_accuracy` (*float, optional*) – Accuracy of the model. The default is 0.9.
- `assessment_method` (*function, optional*) – The assessment method. If None, the assessment is automatically performed using the true value. The default is None.
- `entropy` : (*bool, optional*) – The method use to select items. The default is False

**Raises:**

- `Exception` – If the length of `sensibility` is not equal to the number of judges.

**Returns:**

- `estimated_values` (*list of int*) – A list of int containing the estimated values corresponding to each item in the `items` list.
- (*int*) – Number of iterations.
- `cond` (*float*) – Accuracy of estimated value at the end of the algorithm.
- `error` (*list of int*) – A list containing the number of errors for each judge.
- `assessments_time` (*int*) – The duration of the assessments.

#### CTJ Algorithm

#### `CTJ.CTJ(min_item, max_item, items, sensibility = (0,0,0), true_values = None, max_iteration = 30, max_accuracy = 0.9, scale = 10, assessment_method = None)`

Comparative Triple judgement (`CTJ`) is an evaluation method based on the comparison of a trio of elements. Rather than scoring each item on a fixed scale, evaluators directly compare three items at once, ranking them from best to worst, and then position the central item on a scale by moving it closer to the end that best matches it.  `CTJ` was devised by Dr Kevin Kelly.

**Parameters:**

- `min_item` (*tuple*) – The min_item we want to use. In the format (*int*, *string*).
- `max_item` (*tuple*) – The max_item we want to use. In the format (*int*, *string*).
- `items` (*list of string*) – A list of strings representing the items to be assessed.
- `sensibility` (*tuple*) – A tuple containing the sensibility threshold, the absolute value of the error on the scale, and the probability of making a scale mistake. In the format (*int*, *int*, *double*).
- `true_values` (*list of int, optional*) – A list of int containing the true values corresponding to each item in the `items` list. The default is None.
- `max_iteration` (*int, optional*) – Number of maximum iterations of the algorithm. The default is 30.
- `max_accuracy` (*float, optional*) – Accuracy of the model. The default is 0.9.
- `scale` (*int, optional*) – The value of the scale for the CTJ model. The default is 10.
- `assessment_method` (*function, optional*) – The assessment method. If None, the assessment is automatically performed using the true value. The default is None.

**Returns:**

- `estimated_values` (*list of int*) – A list of int containing the estimated values corresponding to each item in the `items` list.
- (*int*) – Number of iterations.
- `cond` (*float*) – Accuracy of estimated value at the end of the algorithm.
- `error` (*list of int*) – The first element is the number of inversion done in automated assessment, the second is the number of scale error. Default is [0,0].
- `assessments_time` (*int*) – The duration of the assessments.

### Assessment Methods

#### Rubric Assessment Method

#### `CTJ.rubric_assessment_method_image(item, nb_assessment)`

Generate a window to let the user make the `Rubric` assessment for image.

**Parameters:**

- `item` (*string*) – A string representing the item being assessed.
- `nb_assessment` (*int*) – The number of assessments done.
- `window` (*WindowManager*) – An object to manage human assessments.

**Raises**

- `Exception` –  No file in directory.
- `Exception` – The assessment was not done.

**Returns:**

- `item_value` (*int*) – The estimated value made by the user for this item.

#### `CTJ.rubric_assessment_method_pdf(item, nb_assessment)`

Generate a window to let the user make the `Rubric` assessment for pdf.

**Parameters:**

- `item` (*string*) – A string representing the item being assessed.
- `nb_assessment` (*int*) – The number of assessments done.
- `window` (*WindowManager*) – An object to manage human assessments.

**Raises**

- `Exception` –  No file in directory.
- `Exception` – The assessment was not done.

**Returns:**

- `item_value` (*int*) – The estimated value made by the user for this item.

#### ACJ Assessment Method

#### `CTJ.acj_assessment_method_image(id_judge, pair, nb_assessment)`

Generate a window to let the user make the `ACJ` assessment for image.

**Parameters:**

- `id_judge` (*int*) – The id of the judge making the assessment.
- `pair` (*list of string*) – A list of strings representing the pair of items being assessed.
- `nb_assessment` (*int*) – The number of assessments done.
- `window` (*WindowManager*) – An object to manage human assessments.

**Raises**

- `Exception` –  No file in directory.
- `Exception` – The assessment was not done.

**Returns:**

- `sort` (*list of string*) – A list of string containing the assessment results in the format [Max, Min].

#### `CTJ.acj_assessment_method_pdf(id_judge, pair, nb_assessment)`

Generate a window to let the user make the `ACJ` assessment for image for pdf.

**Parameters:**

- `id_judge` (*int*) – The id of the judge making the assessment.
- `pair` (*list of string*) – A list of strings representing the pair of items being assessed.
- `nb_assessment` (*int*) – The number of assessments done.
- `window` (*WindowManager*) – An object to manage human assessments.

**Raises**

- `Exception` –  No file in directory.
- `Exception` – The assessment was not done.

**Returns:**

- `sort` (*list of string*) – A list of string containing the assessment results in the format [Max, Min].
  
#### CTJ Assessment Method

#### `CTJ.ctj_assessment_method_image(slider_range, trio, nb_assessment)`

Generate a window to let the user make the `CTJ` assessment for image.

**Parameters:**

- `slider_range` (*int*) – The range of the slider.
- `trio` (*list of string*) – A list of strings representing the trio of items being assessed.
- `nb_assessment` (*int*) – The number of assessments done.
- `window` (*WindowManager*) – An object to manage human assessments.

**Raises**

- `Exception` –  No file in directory.
- `Exception` – The assessment was not done.

**Returns:**

- `tup` (*tuple*) – A tuple containing the assessment results ([Max, Average, Min], dist).

#### `CTJ.ctj_assessment_method_pdf(slider_range, trio, nb_assessment)`

Generate a window to let the user make the `CTJ` assessment for pdf.

**Parameters:**

- `slider_range` (*int*) – The range of the slider.
- `trio` (*list of string*) – A list of strings representing the trio of items being assessed.
- `nb_assessment` (*int*) – The number of assessments done.
- `window` (*WindowManager*) – An object to manage human assessments.

**Raises**

- `Exception` –  No file in directory.
- `Exception` – The assessment was not done.

**Returns:**

- `tup` (*tuple*) – A tuple containing the assessment results ([Max, Average, Min], dist).
  


