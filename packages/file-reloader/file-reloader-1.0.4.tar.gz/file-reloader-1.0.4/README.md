# AutoReload Library

The Reloader library provides a convenient way for users to automatically reload their Python programs whenever the source code changes. This can be particularly useful during development and testing phases.

## Usage

1. Import the `reloader` module from the Reloader library.

   ```python
   from reloader import Reloader
   ```

2. Create an instance of the `Reloader` class.

   ```python
   my_reloader = Reloader()
   ```

3. Add the following code at the end of your program to enable automatic reloading.

   ```python
   my_reloader.reloader()
   ```
   
## Parameters

- **file_path** (str): Absolute path of the file (default is `sys.argv[0]`).
- **args** (List[str]): Extra arguments required for the program (default is `None`).
- **reload_time** (int): Expected amount of time after which the reloader checks for updates (default is `5 sec`).

Now, whenever you make changes to your source code and save the file, the program will automatically reload without the need to restart it manually.

## Example

```python
# your_program.py

import reloader

# Your program code goes here...

my_reloader = reloader.Reloader()

my_reloader.reloader()
```

## Important Note

Ensure that you place the `reloader()` call at the end of your program to avoid any interference with the rest of your code.
