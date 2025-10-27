""" Practise of Base module structure -diffrent archtypes obj, class,  global variables
implementation interface import statements use of python inline
entry point of application and tests"""

# imports
import math;

#declaration of global variable
let global_value: int = 42;

#object declaration
obj Myobject {
    has value: int = 8;
}

# methods in jac
def add(a:int, b:int) -> int {
   return a + b;
}

# object implementation
impl Myobject {
    def get_value() -> int{
        return self.value;
    } 
}

# sem strings for giving LLm contecxt
sem Myobject.value =  "A value stored in my object";

#main emtry point
with entry {
    print("addition in practice: ", add(3,3));
}

#only executed when we run the module
with entry:__main__{
    print("addition in practice: ", add(5,3));
}

#python inline
::py::
def multiply(a:int, b:int):
    return a * b
::py::

# writing tests in jac
test basic_test {
    result = add(2,3);
    assert result == 5;
    assert multiply(2,3) == 6;
}