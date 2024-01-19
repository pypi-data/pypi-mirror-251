Use Excel file as BDD feature file, get example data from excel files, support automation tests

```
#pip install excelbdd
import pytest
from excelbdd.behavior import get_example_list
import FizzBuzz

excelBDDFile = "path of excel file" 
@pytest.mark.parametrize("HeaderName, Number1, Output1, Number2, Output2, Number3, Output3, Number4, Output4",
                        get_example_list(excelBDDFile,"FizzBuzz"))
def test_FizzBuzz(HeaderName, Number1, Output1, Number2, Output2, Number3, Output3, Number4, Output4):
    assert FizzBuzz.handle(Number1) == Output1
    assert FizzBuzz.handle(Number2) == Output2
    assert FizzBuzz.handle(Number3) == Output3
    assert FizzBuzz.handle(Number4) == Output4
```    

Get data from table in Excel, similar to get from csv file

```
from excelbdd.behavior import get_example_table
@pytest.mark.parametrize("Header01, Header02, Header03, Header04, Header05, Header06, Header07, Header08",
                         get_example_table(excelBDDFile, "DataTable4"))
def test_get_example_tableB(Header01, Header02, Header03, Header04, Header05, Header06, Header07, Header08):
    print(Header01, Header02, Header03, Header04, Header05, Header06, Header07, Header08)
    # add test code here
```

"Specification by testcase" is supported. the bdd excel files can be regarded as the test reports. 
The test format in excel is detected automatically, only extra parameters(expected, test result) are needed to take into test method.

Python unittest is also supported by ExcelBDD.
```
import unittest
from excelbdd.behavior import get_example_list
from parameterized import parameterized

class ExcelBDDTest(unittest.TestCase):
    @parameterized.expand(get_example_list(excelBDDFile))
    def test_get_example_tableB(self, HeaderName, ParamName1, ParamName2, ParamName3, ParamName4):
        print(HeaderName, ParamName1, ParamName2, ParamName3, ParamName4)
        # add test code here
        self.assertEqual(ParamName1, "P1")
        self.assertEqual(ParamName3, None)

```

 
more information at [ExcelBDD Guideline by Python](https://dev.azure.com/simplopen/ExcelBDD/_wiki/wikis/ExcelBDD.wiki/80/ExcelBDD-Guideline-by-Python)