# ERTool

**ERTool** is a Python package designed for simple and efficient implementation of Evidential Reasoning (ER) methods. It aims to provide an intuitive and flexible approach for integrating ER processes, particularly suitable for data analysis and decision support systems.

## Features

- Easy-to-use implementation of Evidential Reasoning.
- Efficient in handling complex ER tasks.
- Flexible interface suitable for various application scenarios.

## Installation

You can install **ERTool** directly from PyPI using pip:

```
pip install ertool
```

## Using Instruction

```
er_example = ertool.ER()
er_example.er_algorithm(B, W, DBF, numOfChildren, numOfGrades)
```

#### Introduction to Input Variables
- ***B***: A one-dimensional array of floats. This array is the output of the algorithm and should initially be an array of zeros. After the completion of the algorithm, this array will contain the final computed results.
- ***W***: A one-dimensional array of floats. It represents the weights of each child node. Tese weights are used in the algorithm to adjust the influence of each child node.

- ***DBF***: A two-dimensional array of floats. It stands for "Degrees of Belief" and is one of the main inputs to the algorithm, used to represent the initial belief degrees for each category or grade.
- ***numOfChildren***: An integer. It indicates the number of child nodes. In the DBF array, this typically corresponds to the number of rows.
- ***numOfGrades***: An integer. It indicates the number of categories or grades. In the DBF array, this typically corresponds to the number of columns.

#### Introduction to Output Values
- ***Return Value***: Boolean. It returns True if the algorithm successfully executes and completes all computations. If any error is encountered during execution (e.g., division by zero), it returns False.
- ***B Array***: Upon completion of the algorithm, the B array is updated with the final calculation results. It reflects the degrees of belief that have been weighted and normalized.


## Quick Start
Here is a basic usage example of **ERTool**:

```python
from ertool import er
import numpy as np

er_example = er.ER()
B = np.zeros(5)
W = np.array([0.2, 0.3, 0.5])
DBF = np.array([[0.1, 0.2, 0.3, 0.4], 
                [0.3, 0.3, 0.2, 0.2], 
                [0.25, 0.25, 0.25, 0.25]])
numOfChildren = 3
numOfGrades = 4

if er_example.er_algorithm(B, W, DBF, numOfChildren, numOfGrades):
    print("Result:", B)
else:
    print("An error occurred during the execution of the algorithm.")
```

## Contributing
Contributions to **ERTool** are welcome. Please concat *tyshipku@gmail.com* for how to contribute to the project.

## License
This project is licensed under the MIT License. For more information, please see the LICENSE file.

## Contact
This project is supported by the **[National Institute of Health Data Science](https://www.nihds.pku.edu.cn/en/), [Peking University](https://english.pku.edu.cn/)**. For any questions or suggestions, please contact us at *tyshipku@gmail.com*. 
