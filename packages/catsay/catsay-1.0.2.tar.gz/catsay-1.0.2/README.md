# CatSay

## Make your cat say Anything you like

## Overview

The ASCII Art Cat Speaking package provides a simple Python function to display a cat "speaking" a message using ASCII art. The cat's message is presented in a thought bubble beside the cat.

## Installation

```bash
pip install catsay
```
## Usage

1. Import the `catsay` function from the `cat` package.
2. Call the function, passing the desired message as an argument.

Example:

```python
from cat import catsay

message = "Hello, I am a cat!"
catsay(message)
```
```
     ------------------       
    (Hello, I am a cat!)
     ------------------   
                   \/     
                 /\_/\
                ( o.o )
                 > ^ <  ,"",
                 ( " ) :
                  (|)""
```
This will print a cat with a thought bubble beside it, containing the specified message.

### Customization
Feel free to customize the ASCII art or modify the function according to your preferences. Or make a pull request, You can change the cat's appearance, the thought bubble, or any other aspect of the output.

### License
This package is provided under the MIT License.

Feel free to use and modify it as needed!