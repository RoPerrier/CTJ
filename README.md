# CTJ

## Table of contents
- [Description](#description)
- [Installation](#installation)
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
- [License](#license)

## Description <a name="#description"></a>

The `CTJ` package implements the comparative triple judgement algorithm devised by Dr. Kevin Kelly. The aim of this algorithm is to improve the accuracy of `ACJ` (adaptive comparative judgement). Instead of comparing elements two by two, they are compared three by three, and a notion of distance between elements is added to the algorithm. `CTJ` was devised by Dr. Kevin Kelly.

This package therefore proposes an implementation of the `CTJ`, the `ACJ`, and the `Rubric` judgment, to enable a more precise analysis of the `CTJ` and to compare its performance with other methods. To do this, pairs and trios are selected with similar methods using Shannon entropy.

## Installation 

```
pip install CTJ
```

Then you need to restart the Python kernel to finish the installation.

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

from CTJ import _rubric_assessment_method, _acj_assessment_method, _ctj_assessment_method

Rubric(worst_element, best_element, shade, assessment_method = _rubric_assessment_method)

ACJ(worst_element, best_element, shade, assessment_method = _acj_assessment_method, max_accuracy = 0.99)

CTJ(worst_element, best_element, shade, assessment_method = _ctj_assessment_method, max_accuracy = 0.99)

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

from CTJ import _rubric_assessment_method, _acj_assessment_method, _ctj_assessment_method

real_values = [160, 106, 209, 80, 135]

Rubric(worst_element, best_element, shade, true_values = real_values, assessment_method = _rubric_assessment_method)

ACJ(worst_element, best_element, shade, true_values = real_values, assessment_method = _acj_assessment_method)

CTJ(worst_element, best_element, shade, true_values = real_values , assessment_method = _ctj_assessment_method)

```

* ### For verifying purposes

You have the real values and want to check the efficiencies of the algorithms.

```py

real_values = [160, 106, 209, 80, 135]

Rubric(worst_element, best_element, shade, true_values = real_values)

ACJ(worst_element, best_element, shade, true_values = real_values)

CTJ(worst_element, best_element, shade, true_values = real_values)

```

Furthermore, in this case, you could use the sensibility parameter to introduce some bias.

The `Rubric`'s sensibility is a tuple containing two elements.
The first value corresponds to the mistake that the user could make by judging an item, the second value is the probability of making a mistake.

```py

Rubric(worst_element, best_element, shade, true_values = real_values, sensibility = (mistake, proba))

```

The `ACJ`'s sensibility is a list of tuples containing two elements.
Each tuple corresponds to the sensibility of a judge, the first tuple corresponds to the sensibility of the first judge, and etc..
The first value of each tuple corresponds to the gap that could lead to a misjudgement, the second value is the probability of making a mistake.

```py

ACJ(worst_element, best_element, shade, true_values = real_values, nb_judge = 2, sensibility = [(gap_1, proba_1), (gap_2, proba_2)])

```

The `CTJ`'s sensibility is a tuple containing three elements.
The first value corresponds to the distance between the nearest item that the judge could misjudge, the second value is the mistake made on the scale, and the third value is the probability of making one of those mistakes.

```py

CTJ(worst_element, best_element, shade, true_values = real_values, sensibility = (distance_error, scale_error, proba))

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
- `nb_bias` (*int*) – Number of biases.
- `assessments_time` (*int*) – The duration of the assessments.

#### ACJ Algorithm

#### `CTJ.ACJ(min_item, max_item, items, nb_judge=1, sensibility=[(0,0)], true_values=None, max_iteration=30, max_accuracy=0.9, assessment_method=None)`

Adaptive Comparative Judgment (`ACJ`) is an evaluation method based on the comparison of pairs of items. Rather than scoring each item on a fixed scale, evaluators directly compare two items at a time and judge which is better according to certain criteria.

**Parameters:**

- `min_item` (*tuple*) – The min_item we want to use. In the format (*int*, *string*).
- `max_item` (*tuple*) – The max_item we want to use. In the format (*int*, *string*).
- `items` (*list of string*) – A list of strings representing the items to be assessed.
- `nb_judge` (*int, optional*) – The number of judges that make the evaluation. The default is 1.
- `sensibility` (*list of tuple*) – A list of tuples containing the sensibility threshold for each simulated judge, and the probability of making a mistake. In the format (*int*, *double*). The default is [(0,0)].
- `true_values` (*list of int, optional*) – A list of int containing the true values corresponding to each item in the `items` list. The default is None.
- `max_iteration` (*int, optional*) – Number of maximum iterations of the algorithm. The default is 30.
- `max_accuracy` (*float, optional*) – Accuracy of the model. The default is 0.9.
- `assessment_method` (*function, optional*) – The assessment method. If None, the assessment is automatically performed using the true value. The default is None.

**Raises:**

- `Exception` – If the length of `sensibility` is not equal to the number of judges.

**Returns:**

- `estimated_values` (*list of int*) – A list of int containing the estimated values corresponding to each item in the `items` list.
- (*int*) – Number of iterations.
- `cond` (*float*) – Accuracy of estimated value at the end of the algorithm.
- `nb_bias` (*list of int*) – A list containing the number of biases for each judge.
- `assessments_time` (*int*) – The duration of the assessments.

#### CTJ Algorithm

#### `CTJ.CTJ(min_item, max_item, items, sensibility = (0,0,0), true_values = None, max_iteration = 30, max_accuracy = 0.9, scale = 10, assessment_method = None)`

Comparative Triple judgement (`CTJ`) is an evaluation method based on the comparison of a trio of elements. Rather than scoring each item on a fixed scale, evaluators directly compare three items at once, ranking them from best to worst, and then position the central item on a scale by moving it closer to the end that best matches it.  `CTJ` was devised by Dr Kevin Kelly.

**Parameters:**

- `min_item` (*tuple*) – The min_item we want to use. In the format (*int*, *string*).
- `max_item` (*tuple*) – The max_item we want to use. In the format (*int*, *string*).
- `items` (*list of string*) – A list of strings representing the items to be assessed.
- `sensibility` (*tuple*) – A tuple containing the sensibility threshold, the absolute value of the error on the scale, and the probability of making a mistake. In the format (*int*, *int*, *double*).
- `true_values` (*list of int, optional*) – A list of int containing the true values corresponding to each item in the `items` list. The default is None.
- `max_iteration` (*int, optional*) – Number of maximum iterations of the algorithm. The default is 30.
- `max_accuracy` (*float, optional*) – Accuracy of the model. The default is 0.9.
- `scale` (*int, optional*) – The value of the scale for the CTJ model. The default is 10.
- `assessment_method` (*function, optional*) – The assessment method. If None, the assessment is automatically performed using the true value. The default is None.

**Returns:**

- `estimated_values` (*list of int*) – A list of int containing the estimated values corresponding to each item in the `items` list.
- (*int*) – Number of iterations.
- `cond` (*float*) – Accuracy of estimated value at the end of the algorithm.
- `nb_bias` (*int*) – Number of biases.
- `assessments_time` (*int*) – The duration of the assessments.

### Assessment Methods

#### Rubric Assessment Method

#### `CTJ._rubric_assessment_method(item, nb_assessment)`

Generate a window to let the user make the `Rubric` assessment.

**Parameters:**

- `item` (*string*) – A string representing the item being assessed.
- `nb_assessment` (*int*) – The number of assessments done.

**Raises:**

- `Exception` – The assessment was not done.

**Returns:**

- (*int*) – The estimated value made by the user for this item.

#### ACJ Assessment Method

#### `CTJ._acj_assessment_method(id_judge, pair, nb_assessment)`

Generate a window to let the user make the `ACJ` assessment.

**Parameters:**

- `id_judge` (*int*) – The id of the judge making the assessment.
- `pair` (*list of string*) – A list of strings representing the pair of items being assessed.
- `nb_assessment` (*int*) – The number of assessments done.

**Raises:**

- `Exception` – The assessment was not done.

**Returns:**

- (*list of string*) – A list of strings containing the assessment results in the format [Max, Min].

#### CTJ Assessment Method

#### `CTJ._ctj_assessment_method(slider_range, trio, nb_assessment)`

Generate a window to let the user make the `CTJ` assessment.

**Parameters:**

- `slider_range` (*int*) – The range of the slider.
- `trio` (*list of string*) – A list of strings representing the trio of items being assessed.
- `nb_assessment` (*int*) – The number of assessments done.

**Returns:**

- (*tuple*) – A tuple containing the assessment results (Max, (dist, Average), Min). In the format (*int*, (*int*, *int*), *int*).

## License

This project is licensed under the Apache 2.0 License. See the LICENSE and NOTICE.txt files for more details.


