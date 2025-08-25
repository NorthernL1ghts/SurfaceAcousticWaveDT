# TODO

**Note:** Now that we have a simple prototype in Python, we can begin migrating it to a more powerful language like C++, turning these simulations into a real product.

- [ ] **Create Application & EntryPoint**  
  Set up a simple application structure with a main entry point.

- [ ] **Create Log Class**  
  Implement a `Log` class using the `spdlog` submodule. The base logging code is mostly reusable.

- [ ] **Create Wave Class**  
  Implement a `Wave` class to generate surface acoustic waves with parameters such as:  
  - `x, y, z` coordinates  
  - `amplitude`  
  - `pitch`  
  - `wavelength`  

- [ ] **Create DataTransfer Class**  
  Implement a `DataTransfer` class to handle transferring any type of file or data. Ensure it supports all file extensions and data types for universal applicability.
