
# **Turtle Extentions**
![LOGO](https://i.postimg.cc/y6JWpLvM/Untitled-design.png)

## Docs:
### Install:
- Open CMD Prompt by pressing the windows button and typing cmd, then hit enter
- Type ```py -m pip install TurtleExtentions``` (Windows) or 
```python pip install TurtleExtentions``` (Linux/MacOS)
- Import the module inside the code like this: 
```python
import TurtleExtentions as TE
# Code here
```
### Basic shapes and arguments:
#### Basic Shapes:
- The `Shape` class contains all basic shapes
- To use it, just type 
```python
import TurtleExtentions as TE
TE.Shape.ShapeHere(params)
```
- Lets make a hexagon appear
```python
TE.Shape.Hexagon(Size=50) # The size by default is 20
```
- To change its position just use the pos1 and pos2 arguments
```python
TE.Shape.Hexagon(Size=50, pos1=150, pos2=150) # Default positons are 100, 100
```
- Now by default this would not be filled in. To do so set the DoFill paramater to True 
- You can also edit the fillcolor with the FillColor paramater like this
```python
TE.Shape.Hexagon(Size=50, pos1=150, pos2=150, DoFill=True, FillColor="Green")
```
- That would result in this
![HEXAGON-SHAPE-DOCS](https://i.postimg.cc/VLpqHSqR/image.png)


## Release 0.1.0
- Basic shape functions
- Highly customisable