# bempy - Python Block-Element-Modifier Library
`bempy` is a library for building complex classes using BEM (Block-Element-Modifier) methodology.

`bempy` provides approach for block composition that allows you to tackle a wide range of tasks with ease. Whether you're generating intricate `Character(...)` designs for video games, constructing robust `Server(...)` infrastructure for your backend systems, placing precise `Resistor(...)` configurations for your electronics projects, or creating interactive `Button(...)` interfaces for your frontend applications, bempy has you covered. Additionally, with the ability to define complex `Model(...)` structures for advanced data processing and science computing, bempy offers limitless possibilities for innovation and creativity.

With `bempy`, you can build reusable blocks of code that can be easily inherited, modified, and extended to create new and complex classes. The library uses a hierarchical structure to define blocks, elements, and modifiers, making it simple to understand and maintain large projects.

## Features
* Simple and easy-to-use syntax for defining blocks, elements, and modifiers
* Support for inheritance, allowing blocks to inherit and extend the properties of other blocks
* Ability to define default arguments and properties for blocks, making it easier to create instances of blocks
* Support for automatic documentation extraction, allowing you to easily keep track of the purpose and usage of blocks and their components

## Concept
`bempy` is a library for building complex classes based on the BEM methodology.

### BEM
BEM, or Block Element Modifier, is a methodology that helps developers build scalable, maintainable and reusable components for their projects.

The main idea behind BEM is to encapsulate appearance, logic and content of a component into distinct blocks that can be easily re-used and modified without affecting the rest of the application. Each block is treated as an independent entity and can be combined with other blocks to create complex structures.

In BEM, a block is the main building block of the application, and it can consist of multiple elements and modifiers. An element is a part of a block that cannot be used independently, and it provides additional functionality and styling to the block. A modifier is a variation of a block or element that changes its appearance or behavior.

Using BEM helps to create well-structured, modular and maintainable code that can be easily adapted to changing requirements. It also makes it easier for developers to collaborate on a project, as each block can be worked on independently and the resulting code is easy to understand and integrate into the rest of the application.

### BEM Python
The blocks are stored in a specific directory structure:
```
blocks/
    game/
        Character/
            _gender/
                male.py
                female.py
                non-binary.py
            _race/
                human.py
                elf.py
                orc.py
            _class/
                warrior.py
                mage.py
                rogue.py
            __init__.py

     data_science/
        Model/
            _algorithm/
                logistic_regression.py
                decision_tree.py
            _hyperparameters/
                default.py
                optimized.py
            _preprocessing/
                standard_scaler.py
                normalizer.py
            __init__.py

      scientific_computing/
         Solver/
            _method/
                finite_difference.py
                monte_carlo.py
                particle_swarm.py
            _precision/
                low.py
                high.py
            __init__.py
```

With these modificators, you can create any combination of characters that represent the type of person you want in the game. In the example, the `Character` block is stored in the `game` directory, and it has several modificators such as `_gender`, `_race`, and `_abilities`.

To use the `Character` block in your game, you can create an instance of the block with specific modificator values. For example:
```python
from bem.game import Character

FemaleElf = Character(
    gender='female',
    race='elf',
    abilities=['agility', 'intelligence']
)

gamer = FemaleElf(
    level=3,
    fertility=75,
    mana=50
)
```

Here, we are creating a female elf character by passing the values for the `gender`, `race`, and `abilities` modificators to the `Character` block.

Additionally, we can define the level, health, and mana for this specific character instance by passing those values to `gamer = FemaleElf(...)`.

With this, we have successfully created a unique instance of a female elf character with specific abilities and attributes that can be used in your game.

The `Character` class is defined in `Character/__init__.py`:
```python
from bempy import Block

class Base(Block):
    """
        A basic Character implementation
    """

    def init(self, level=1):
        """
            level -- The level of character
        """

        print(self.name + ': Character created with level =', level)
```

The Female `Modificator` class is defined in `Character/_gender/female.py`:
```python
class Modificator:
    """
        A Female gender implementation
    """

    def init(self, fertility=100):
        """
            fertility -- is the capability to produce offspring through reproduction
        """

        print(self.name + ': Female created with fertility =', fertility)
```

The Elf `Modificator` class is defined in `Character/_race/elf.py`:
```python
class Modificator:
    """
        A Elf race implementation
    """

    def init(self, mana=0):
        """
            mana -- The amount of mana
        """

        print(self.name + ': Elf created with mana =', mana)
```


```python
>>> from bempy.game import Character
>>> FemaleElf = Character(gender='female', race='elf')
>>> gamer = FemaleElf(level=10, fertility=75, mana=50)
game.Character: Character created with level = 10
game.Character: Female created with fertility = 75
game.Character: Elf created with mana = 50


>>> Female = Character(gender='female', race='human')
>>> ma = Female(level=86, fertility=100)
game.Character: Character created with level = 86
game.Character: Female created with fertility = 100
```

You could create instances of machine learning models using different algorithms, hyperparameters, and data preprocessing techniques. For example:
```python
from bempy.data_science import Model

dt_model = Model(
    algorithm='decision_tree',
    hyperparameters='optimized',
    preprocessing='normalizer'
)
```

You could create instances of different types of solvers for scientific computing problems. For example:
```python
from bem.scientific_computing import Solver

fd_solver = Solver(
    method='finite_difference',
    precision='high'
)
```

Here is an example of how you could create instances of a backend using different components and configurations:
```
blocks/
    backend/
        Server/
            _backend/
                flask.py
                django.py
            _config/
                debug.py
                production.py
            _extensions/
                cors.py
                db.py
            __init__.py
        Database/
            _backend/
                mongodb.py
                mysql.py
            _config/
                local.py
                remote.py
            __init__.py
```

Using the backend directory structure, you could create instances of the backend with specific configurations and components. For example:
```python
from bempy.backend import Server

FlaskApp = Server(
    backend='flask',
    config='debug',
    extensions=['cors', 'db']
)

FlaskApp(
    host='localhost',
    port=8080,
    db='mongodb'
)
```
In this example, `FlaskApp = Server(backend='flask', ...)` is the construction of a server block with the specified modificator. And `FlaskApp(...)` is creating an instance of the defined optimized server block.

REPL Example:
```python
>>> from bempy.backend import Server, Database
>>> FlaskApp = Server(backend='flask', config='debug', extensions=['db', 'cors'])
>>> app = FlaskApp(host='localhost', port=8080, db='mongodb')
backend.Server: Server created with host = localhost
backend.Server: Flask server created on port = 8080
backend.Server: Debug configuration enabled
backend.Database: Database connection with name = localhost
backend.Database: Mongodb initialized
backend.Database: Local Database created from path = /var/db
backend.Server: Database connection with db = mongodb
```

## Installation
You can install `bempy` library via `pip` by running the following command in your terminal:
```
pip install bempy
```

After installation, you can import the library in your Python code by using:
```
import bempy
```

You can also install the latest version of the library directly from the source code by cloning the repository and running the following command:
`python setup.py install`

You can play with examples in `tests` folder where some Blocks from documentation available in `blocks` directory.

## Use Cases
`bempy` has a wide range of use cases, beyond the original intended purpose of helping developers build complex UI components. Here are a few examples of how BEMPy can be applied:
* **Data Science**: To data science projects to help structure and organize code. By breaking down data processing into blocks, it becomes easier to create and maintain complex data pipelines.
* **Scientific Computing**: To structure complex mathematical models in a way that makes them more understandable, manageable and maintainable.
* **Game Development**: The BEM methodology provides a way to structure game objects in a way that makes them easier to manage and maintain.
* **API Development**: To build APIs that are easy to consume and understand. By breaking down a complex system into blocks and applying modularization techniques, it becomes easier to test, debug and maintain the API.
* **Front-end Development**: To write clean, scalable and maintainable HTML, CSS and JavaScript for web front-end development. BEM methodology helps to encapsulate styles and behavior into blocks, making it easy to build and reuse UI components.
* **Back-end Development**: By using BEM methodology to structure and organize code, it becomes easier to create and maintain complex systems.

In each of these cases, **bempy**'s structure and methodology helps developers to create complex systems that are maintainable and scalable over time. Whether you are working on a small project or a large enterprise application, `bempy` can help you write clean, modular and maintainable code.

## Contributing
I'm appreciate and welcome contributions to `bempy`. If you are interested in contributing, there are several ways to get started:
* **Report a bug**: If you find a bug or an issue in the library, please open an issue in the Github repository with a description of the problem and steps to reproduce it.
* **Fix a bug**: If you have a fix for a bug, please submit a pull request with a description of the bug and how you fixed it.
* **Implement a new feature**: If you want to add a new feature to the library, please open an issue in the Github repository to discuss your idea and the implementation details. After the discussion, you can submit a pull request with your implementation.
* **Improve documentation**: If you see an opportunity to improve the documentation, feel free to submit a pull request with changes.
* **Test the library**: If you have time, you can help us by testing the library and submitting bug reports or even fixes.

## License
The `bempy` library is licensed under the terms of the GNU General Public License v3.0 (GPL-3.0). This means that you have the freedom to use, modify, and distribute the software and its source code.

By contributing to `bempy`, you agree to license your contributions under the same terms. This allows everyone to benefit from your contributions, while also protecting the future of the project.

## References
These references provide additional information on BEM methodology and its implementation in various technologies. They can help you understand the concept and best practices of BEM and provide guidance on how to apply it in your work:
* [From Components to Systems: BEM Code for System-Level Design](https://medium.com/@fefa4ka/from-components-to-systems-bem-for-system-level-design-d6d4437b8a4)
* [Coding Modular and Flexible Electronic Circuits with BEM Methodology and Parametric Design](https://medium.com/@fefa4ka/building-modular-and-flexible-electronic-circuits-with-bem-methodology-and-parametric-design-6e2637ce0c16)
* BEM (Block Element Modifier) Methodology - https://en.bem.info/methodology/
* CSS BEM - https://css-tricks.com/bem-101/
* BEM Naming Convention - https://en.bem.info/methodology/naming-convention/
* BEM Metodology in React - https://github.com/bem/bem-react
* BEM Components Library - https://github.com/bem/bem-components
* BEM Tools - https://en.bem.info/tools/

## Credits

-   Alexander Kodratev (alex@nder.work)
