import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import openmc
import openmc.deplete
import math
from matplotlib import pyplot

###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# OpenMC simulation parameters
batches = 20 #increase batch size, i took 100
inactive = 10
particles = 10000


###############################################################################
#                 Exporting to OpenMC materials.xml file
###############################################################################

# Instantiate some Materials and register the appropriate Nuclides
fuel1 = openmc.Material(material_id=1, name='fuel1')
fuel1.set_density('g/cc', 10.286)
fuel1.add_nuclide('U235',4.88,percent_type='wo' )
fuel1.add_nuclide('U238',83.267,percent_type='wo' )
fuel1.add_nuclide('O16',11.853,percent_type='wo' )
fuel1.deplete = True

fuel2 = openmc.Material(material_id=2, name='fuel2')
fuel2.set_density('g/cc', 10.286)
fuel2.add_nuclide('U235',2.82,percent_type='wo' )
fuel2.add_nuclide('U238',85.325,percent_type='wo' )
fuel2.add_nuclide('O16',11.853,percent_type='wo' )
fuel2.deplete = True


#in your code, add_element repeats twice, the one with atomic percentage should be deleted
moderator = openmc.Material(material_id=4, name='moderator')
moderator.set_density('g/cc', 1.0)
moderator.add_element('H',11.155,percent_type='wo' )
moderator.add_element('O',88.535,percent_type='wo' )
moderator.add_element('B',0.31,percent_type='wo' )
moderator.add_s_alpha_beta('c_H_in_H2O')

clad1 = openmc.Material(material_id=5, name='clad1')
clad1.set_density('g/cc', 6.56)
clad1.add_element('Sn',1.57,percent_type='wo' )
clad1.add_element('Fe',0.22,percent_type='wo' )
clad1.add_element('Cr',0.10,percent_type='wo' )
clad1.add_element('Ni',0.0035,percent_type='wo' )
clad1.add_element('H',0.0006,percent_type='wo' )
clad1.add_element('C',0.0014,percent_type='wo' )
clad1.add_element('N',0.0028,percent_type='wo' )
clad1.add_element('O',0.13,percent_type='wo' )
clad1.add_element('Zr',92.8717,percent_type='wo' )

poison=openmc.Material(material_id=6, name='poison')
poison.set_density('g/cc',2.299)
poison.add_nuclide('B10',0.699,percent_type='wo')
poison.add_nuclide('B11',3.207,percent_type='wo')
poison.add_element('O',53.902,percent_type='wo')
poison.add_element('Al',1.167,percent_type='wo')
poison.add_element('Si',37.856,percent_type='wo')
poison.add_element('K',0.332,percent_type='wo')
poison.add_element('Na',2.837,percent_type='wo')

helium=openmc.Material(material_id=7, name='helium')
helium.set_density('g/cc', 0.00225)
helium.add_element('He',1.0)

# Instantiate a Materials collection and export to XML
materials_file = openmc.Materials([fuel1,fuel2,moderator,clad1,poison,helium])
materials_file.export_to_xml()


###############################################################################
#                 Exporting to OpenMC geometry.xml file
###############################################################################

# Create the surface used for each pin
pin_rad = openmc.ZCylinder(x0=0, y0=0, r=0.4096, name='pin_rad')
clad_in=openmc.ZCylinder(x0=0, y0=0, r=0.41875, name='clad_in')
clad_out=openmc.ZCylinder(x0=0,y0=0,r=0.47500, name='clad_out')

# Create the cells which will be used to represent each pin type.
cells={}
universes={}
# Create the cell for the material inside the cladding
cells[fuel1] = openmc.Cell(name='fuel1',region = -pin_rad,fill = fuel1)


cells[helium] = openmc.Cell(name='helium',region = +pin_rad & -clad_in,fill = helium)


cells[clad1] = openmc.Cell(name='clad1',region = +clad_in & -clad_out,fill = clad1)


cells[moderator] = openmc.Cell(name='moderator',region = +clad_out,fill = moderator)


# Finally add the cells we just made to a Universe object
u1 = openmc.Universe()
u1.add_cells([cells[fuel1], cells[helium],cells[clad1],cells[moderator]])

# Create the cells which will be used to represent each pin type.
cells2={}
universes2={}
# Create the cell for the material inside the cladding
cells2[fuel2] = openmc.Cell(name='fuel2')
# Assign the half-spaces to the cell
cells2[fuel2].region = -pin_rad
# Register the material with this cell
cells2[fuel2].fill = fuel2

cells2[helium] = openmc.Cell(name='helium2')
# Assign the half-spaces to the cell
cells2[helium].region = +pin_rad & -clad_in
# Register the material with this cell
cells2[helium].fill = helium

cells2[clad1] = openmc.Cell(name='clad1')
# Assign the half-spaces to the cell
cells2[clad1].region = +clad_in & -clad_out
# Register the material with this cell
cells2[clad1].fill = clad1

cells2[moderator] = openmc.Cell(name='moderator')
# Assign the half-spaces to the cell
cells2[moderator].region = +clad_out
# Register the material with this cell
cells2[moderator].fill = moderator

# Finally add the cells we just made to a Universe object
u2= openmc.Universe()
u2.add_cells([cells2[fuel2], cells2[helium],cells2[clad1],cells2[moderator]])



poison_clad_in=openmc.ZCylinder(x0=0, y0=0, R=0.56150, name='poison_clad_in')
poison_clad_out=openmc.ZCylinder(x0=0,y0=0,R=0.61200, name='poison_clad_out')
# Create the cells which will be used to represent each pin type.
cells={}
universes={}
# Create the cell for the material inside the cladding
cells[poison] = openmc.Cell(name='poison')
# Assign the half-spaces to the cell
cells[poison].region = -poison_clad_in
# Register the material with this cell
cells[poison].fill = moderator

# Create the cell for the material inside the cladding
cells[clad1] = openmc.Cell(name='clad1')
# Assign the half-spaces to the cell
cells[clad1].region = +poison_clad_in & -poison_clad_out
# Register the material with this cell
cells[clad1].fill = clad1

# Create the cell for the material inside the cladding
cells[moderator] = openmc.Cell(name='moderator')
# Assign the half-spaces to the cell
cells[moderator].region = +poison_clad_out
# Register the material with this cell
cells[moderator].fill = moderator

g=openmc.Universe()
g.add_cells([cells[poison],cells[clad1],cells[moderator]])

#for creating an empty assembly
empty_plane1=openmc.XPlane(x0=10.71)
empty_plane2=openmc.YPlane(y0=10.71)
empty_plane3=openmc.XPlane(x0=-10.71)
empty_plane4=openmc.YPlane(y0=-10.71)
cells={}
universes={}
cells[moderator]= openmc.Cell(name='moderator')
cells[moderator].region=+empty_plane3 & -empty_plane1 & +empty_plane4 & -empty_plane2
cells[moderator].fill=moderator
m=openmc.Universe()
m.add_cells([cells[moderator]])



#A2
lattices2 = {}
# Instantiate the UO2 Lattice
lattices2['UO2 Assembly'] = openmc.RectLattice()
lattices2['UO2 Assembly'].dimension = [17, 17]
lattices2['UO2 Assembly'].lower_left = [-10.71, -10.71]
lattices2['UO2 Assembly'].pitch = [1.26, 1.26]
lattices2['UO2 Assembly'].universes = \
[[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, u2, u2, u2],
[u2, u2, u2, g, u2, u2, u2, u2, u2, u2, u2, u2, u2, g, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, g, u2, u2, u2, u2, u2, u2, u2, u2, u2, g, u2, u2, u2],
[u2, u2, u2, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2]]

# Create a containing cell and universe
cells2['UO2 Assembly'] = openmc.Cell()
cells2['UO2 Assembly'].fill = lattices2['UO2 Assembly']
universes2['UO2 Assembly'] = openmc.Universe(name='UO2 Assembly 2')
universes2['UO2 Assembly'].add_cell(cells2['UO2 Assembly'])

#A3
cells3={}
lattices3 = {}
universes3={}

# Instantiate the UO2 Lattice
lattices3['UO2 Assembly'] = openmc.RectLattice()
lattices3['UO2 Assembly'].dimension = [17, 17]
lattices3['UO2 Assembly'].lower_left = [-10.71, -10.71]
lattices3['UO2 Assembly'].pitch = [1.26, 1.26]
lattices3['UO2 Assembly'].universes = \
[[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, u2, u2, u2],
[u2, u2, u2, g, u2, u2, u2, u2, u2, u2, u2, u2, u2, g, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, g, u2, u2, u2, u2, u2, u2, u2, u2, u2, g, u2, u2, u2],
[u2, u2, u2, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2]]

# Create a containing cell and universe
cells3['UO2 Assembly'] = openmc.Cell()
cells3['UO2 Assembly'].fill = lattices3['UO2 Assembly']
universes3['UO2 Assembly'] = openmc.Universe(name='UO2 Assembly 3')
universes3['UO2 Assembly'].add_cell(cells3['UO2 Assembly'])

#B1
cells4={}
lattices4 = {}
universes4={}
# Instantiate the UO2 Lattice
lattices4['UO2 Assembly'] = openmc.RectLattice()
lattices4['UO2 Assembly'].dimension = [17, 17]
lattices4['UO2 Assembly'].lower_left = [-10.71, -10.71]
lattices4['UO2 Assembly'].pitch = [1.26, 1.26]
lattices4['UO2 Assembly'].universes = \
[[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, g, u1, u1, u1, u1, u1, u1, u1, u1, u1, g, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, g, u1, u1, u1, u1, u1, u1, u1, u1, u1, g, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1]]
# Create a containing cell and universe
cells4['UO2 Assembly'] = openmc.Cell(name='UO2 Assembly')
cells4['UO2 Assembly'].fill = lattices4['UO2 Assembly']
universes4['UO2 Assembly'] = openmc.Universe(name='UO2 Assembly 4')
universes4['UO2 Assembly'].add_cell(cells4['UO2 Assembly'])

#B2
cells5={}
lattices5 = {}
universes5={}
# Instantiate the UO2 Lattice
lattices5['UO2 Assembly'] = openmc.RectLattice()
lattices5['UO2 Assembly'].dimension = [17, 17]
lattices5['UO2 Assembly'].lower_left = [-10.71, -10.71]
lattices5['UO2 Assembly'].pitch = [1.26, 1.26]
lattices5['UO2 Assembly'].universes = \
[[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, g, u1, u1, u1, u1, u1, u1, u1, u1, u1, g, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, g, u1, u1, u1, u1, u1, u1, u1, u1, u1, g, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1]]
# Create a containing cell and universe
cells5['UO2 Assembly'] = openmc.Cell(name='UO2 Assembly')
cells5['UO2 Assembly'].fill = lattices5['UO2 Assembly']
universes5['UO2 Assembly'] = openmc.Universe(name='UO2 Assembly 5')
universes5['UO2 Assembly'].add_cell(cells5['UO2 Assembly'])

#B5
cells6={}
lattices6= {}
universes6={}
# Instantiate the UO2 Lattice
lattices6['UO2 Assembly'] = openmc.RectLattice()
lattices6['UO2 Assembly'].dimension = [17, 17]
lattices6['UO2 Assembly'].lower_left = [-10.71, -10.71]
lattices6['UO2 Assembly'].pitch = [1.26, 1.26]
lattices6['UO2 Assembly'].universes = \
[[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, g, u1, u1, u1, u1, u1, u1, u1, u1, u1, g, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, g, u1, u1, u1, u1, u1, u1, u1, u1, u1, g, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1]]
# Create a containing cell and universe
cells6['UO2 Assembly'] = openmc.Cell(name='UO2 Assembly')
cells6['UO2 Assembly'].fill = lattices6['UO2 Assembly']
universes6['UO2 Assembly'] = openmc.Universe(name='UO2 Assembly 6')
universes6['UO2 Assembly'].add_cell(cells6['UO2 Assembly'])


#B6
cells7={}
lattices7= {}
universes7={}
# Instantiate the UO2 Lattice
lattices7['UO2 Assembly'] = openmc.RectLattice()
lattices7['UO2 Assembly'].dimension = [17, 17]
lattices7['UO2 Assembly'].lower_left = [-10.71, -10.71]
lattices7['UO2 Assembly'].pitch = [1.26, 1.26]
lattices7['UO2 Assembly'].universes = \
[[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, g, u1, u1, u1, u1, u1, u1, u1, u1, u1, g, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1]]
# Create a containing cell and universe
cells7['UO2 Assembly'] = openmc.Cell(name='UO2 Assembly')
cells7['UO2 Assembly'].fill = lattices7['UO2 Assembly']
universes7['UO2 Assembly'] = openmc.Universe(name='UO2 Assembly 7')
universes7['UO2 Assembly'].add_cell(cells7['UO2 Assembly'])


lattices= {}
lattices['Core'] = openmc.RectLattice(name='11*11 core lattice')
lattices['Core'].dimension= [9,9]
lattices['Core'].lower_left = [-96.39, -96.39]
lattices['Core'].pitch = [21.42, 21.42]
lattices['Core'].outer= m
A2= universes2['UO2 Assembly']
A3 = universes3['UO2 Assembly']
B1 = universes4['UO2 Assembly']
B2 = universes5['UO2 Assembly']
B5 = universes6['UO2 Assembly']
B6 = universes7['UO2 Assembly']
lattices['Core'].universes = [[m, m, m, B1, B2, B1, m, m, m],
[m, m, B2, B5, B6, B5, B2, m, m],
[m, B2, B5, A3, A2, A3, B5, B2, m],
[B1, B5, A3, A2, A3, A2, A3, B5, B1],
[B2, B6, A2, A3, A2, A3, A2, B6, B2],
[B1, B5, A3, A2, A3, A2, A3, B5, B1],
[m, B2, B5, A3, A2, A3, B5, B2, m],
[m, m, B2, B5, B6, B5, B2, m, m],
[m, m, m, B1, B2, B1, m, m, m]]


# Create boundary planes to surround the geometry

# Create root Cell
core_os=openmc.ZCylinder(r=102,boundary_type='reflective')
root_cell = openmc.Cell(name='root cell')
root_cell.fill = lattices['Core']
root_cell.region = -core_os

# Create root Universe
root_universe = openmc.Universe(name='root universe', universe_id=0)
root_universe.add_cell(root_cell)

geometry = openmc.Geometry(root_universe)
geometry.export_to_xml()

###############################################################################
#                   Exporting to OpenMC settings.xml file
###############################################################################

# Instantiate a Settings object, set all runtime parameters, and export to XML
settings_file = openmc.Settings()
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = particles

# Create an initial uniform spatial source distribution over fissionable zones
bounds = [-97, -97, -200, 97, 97, 200] #your whole core should have uniformly distributed neutrons
#i picked the values for fuel boundary
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings_file.source = openmc.source.Source(space=uniform_dist)

settings_file.export_to_xml()


###############################################################################
#                   Exporting to OpenMC plots.xml file
###############################################################################

plot_xy = openmc.Plot(plot_id=1)
plot_xy.filename = 'plot_xy'
plot_xy.origin = [0, 0, 0]
plot_xy.width = [204, 204]
plot_xy.pixels = [10000, 10000] # a picture of 300Mb!!!!!!
plot_xy.color_by = 'material'

plot_yz = openmc.Plot(plot_id=2)
plot_yz.filename = 'plot_yz'
plot_yz.basis = 'yz'
plot_yz.origin = [0, 0, 0]
plot_yz.width = [250, 200]
plot_yz.pixels = [500, 500]
plot_yz.color_by = 'material'

# Instantiate a Plots collection, add plots, and export to XML
plot_file = openmc.Plots((plot_xy, plot_yz))
plot_file.export_to_xml()

###############################################################################
#                   Exporting to OpenMC tallies.xml file
###############################################################################
# Instantiate a tally mesh
mesh = openmc.RegularMesh()
mesh.dimension = [100, 100, 1]
mesh.lower_left = [-300, -300, -1e50] #do not use a dot eg=> 1.e50
mesh.upper_right = [300, 300, 1e50]

# Instantiate some tally Filters
energy_filter = openmc.EnergyFilter([0., 4., 20e6])
mesh_filter = openmc.MeshFilter(mesh)

# Instantiate the Tally
tally = openmc.Tally(tally_id=1, name='tally 1')
tally.filters = [energy_filter, mesh_filter]
tally.scores = ['flux', 'fission', 'nu-fission']

# Instantiate a Tallies collection and export to XML
tallies_file = openmc.Tallies([tally])
tallies_file.export_to_xml()

##################################################################################
#                   Depletion Calculation
##################################################################################

#volume specification
fuel1.volume = math.pi * 36 * 264 * 200 * 0.4096 ** 2
fuel2.volume = math.pi * 21 * 264 * 200 * 0.4096 ** 2
#depletion chain specification

operator = openmc.deplete.Operator(geometry, settings_file,"./chain_casl.xml")
power = 330e6 # W #this is thermal power, not linear power density
time_steps = [30 * 24 * 60 * 60] * 5 #set the depletion for a month or less, 100 days is too big


integrator = openmc.deplete.PredictorIntegrator(operator, time_steps, power)
integrator.integrate() 

openmc.run()
