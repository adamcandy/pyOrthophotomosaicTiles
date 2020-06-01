pyOrthophotomosaicTiles
=======================

Project to create image tile sets for orthophotomosaics.

Usage
-----

```python
import orthophotomosaictiles
filename = '/path/to/file.png'
s = orthophotomosaictiles.Tile(filename)
s.process()
s.show() 

outputname = '/path/to/output.png'
s.save(outputname)
```

Command line
------------

```script
$ orthophotomosaictiles --show '/path/to/file.png'

```

Contact
-------

For further information and updates, please contact the lead author Dr Adam S. Candy at
[Adam.Candy@nioz.nl](mailto:Adam.Candy@nioz.nl),
[adam@candylab.org](mailto:adam@candylab.org)
or see the webpages at
[candylab.org](https://candylab.org).

