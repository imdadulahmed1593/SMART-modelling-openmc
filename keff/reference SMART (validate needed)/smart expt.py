import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import openmc

###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# OpenMC simulation parameters500/100/1000000
batches = 100
inactive = 10
particles = 10000


###############################################################################
#                 Exporting to OpenMC materials.xml file

#moderator.add_element('H',11.155,percent_type='wo' )
#moderator.add_element('O',88.535,percent_type='wo' )
#moderator.add_nuclide('B10',0.31,percent_type='wo' )
###############################################################################

# Instantiate some Materials and register the appropriate Nuclides
fuel1 = openmc.Material(material_id=1, name='fuel1')
fuel1.set_density('g/cc', 10.286)
fuel1.add_nuclide('U235',4.88,percent_type='wo' )
fuel1.add_nuclide('U238',83.267,percent_type='wo' )
fuel1.add_nuclide('O16',11.853,percent_type='wo' )
fuel1.temperature = 293.6

fuel2 = openmc.Material(material_id=2, name='fuel2')
fuel2.set_density('g/cc', 10.286)
fuel2.add_nuclide('U235',2.82,percent_type='wo' )
fuel2.add_nuclide('U238',85.325,percent_type='wo' )
fuel2.add_nuclide('O16',11.853,percent_type='wo' )
fuel2.temperature = 293.6

IFBA=openmc.Material(material_id=3, name='ifba')
IFBA.set_density('g/cc', 10.017)
IFBA.add_element('U',81.09,percent_type='wo' )
IFBA.add_element('Gd',6.9408,percent_type='wo' )
IFBA.add_nuclide('O16',11.9692,percent_type='wo' )
IFBA.temperature = 293.6

moderator = openmc.Material(material_id=4, name='moderator')
moderator.set_density('g/cc', 1.0)
moderator.add_element('H', 2.)
moderator.add_element('O', 1.)
moderator.add_s_alpha_beta('c_H_in_H2O')
moderator.temperature = 293.6

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
clad1.temperature = 293.6

poison=openmc.Material(material_id=6, name='poison')
poison.set_density('g/cc',2.299)
poison.add_nuclide('B10',0.699,percent_type='wo')
poison.add_nuclide('B11',3.207,percent_type='wo')
poison.add_element('O',53.902,percent_type='wo')
poison.add_element('Al',1.167,percent_type='wo')
poison.add_element('Si',37.856,percent_type='wo')
poison.add_element('K',0.332,percent_type='wo')
poison.add_element('Na',2.837,percent_type='wo')
poison.temperature = 293.6

helium=openmc.Material(material_id=7, name='helium')
helium.set_density('g/cc', 0.00225)
helium.add_element('He',1.0)
helium.temperature = 293.6

# Instantiate a Materials collection and export to XML
materials_file = openmc.Materials([fuel1,fuel2,IFBA,moderator,clad1,poison,helium])
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
cells2[fuel2] = openmc.Cell(name='fuel2',region = -pin_rad,fill = fuel2)


cells2[helium] = openmc.Cell(name='helium2',region = +pin_rad & -clad_in,fill = helium)


cells2[clad1] = openmc.Cell(name='clad1',region = +clad_in & -clad_out,fill = clad1)


cells2[moderator] = openmc.Cell(name='moderator',region = +clad_out,fill = moderator)


# Finally add the cells we just made to a Universe object
u2= openmc.Universe()
u2.add_cells([cells2[fuel2], cells2[helium],cells2[clad1],cells2[moderator]])

# Create the cells which will be used to represent each pin type.
cells3={}
universes3={}
# Create the cell for the material inside the cladding
cells3[IFBA] = openmc.Cell(name='fuel3',region = -pin_rad,fill = IFBA)


cells3[helium] = openmc.Cell(name='helium',region = +pin_rad & -clad_in,fill = helium)


cells3[clad1] = openmc.Cell(name='clad1',region = +clad_in & -clad_out,fill = clad1)


cells3[moderator] = openmc.Cell(name='moderator',region = +clad_out,fill = moderator)


# Finally add the cells we just made to a Universe object
u3 = openmc.Universe()
u3.add_cells([cells3[IFBA], cells3[helium],cells3[clad1],cells3[moderator]])

poison_clad_in=openmc.ZCylinder(x0=0, y0=0, R=0.56150, name='poison_clad_in')
poison_clad_out=openmc.ZCylinder(x0=0,y0=0,R=0.61200, name='poison_clad_out')
# Create the cells which will be used to represent each pin type.
cells={}
universes={}
# Create the cell for the material inside the cladding


cells[poison] = openmc.Cell(name='poison',region = -poison_clad_in,fill = helium)


cells[clad1] = openmc.Cell(name='clad1',region = +poison_clad_in & -poison_clad_out,fill = clad1)


cells[moderator] = openmc.Cell(name='moderator',region = +poison_clad_out ,fill = moderator)

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
[u2, u2, u3, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, u3, u2, u2],
[u2, u2, u2, g, u2, u2, u2, u2, u2, u2, u2, u2, u2, g, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u3, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u3, g, u2, u2, g, u2, u2, g, u3, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u3, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, g, u2, u2, u2, u2, u2, u2, u2, u2, u2, g, u2, u2, u2],
[u2, u2, u3, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, u3, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2]]

# Create a containing cell and universe
cells2['UO2 Assembly'] = openmc.Cell()
cells2['UO2 Assembly'].fill = lattices2['UO2 Assembly']
universes2['UO2 Assembly'] = openmc.Universe(name='UO2 Assembly 2')
universes2['UO2 Assembly'].add_cell(cells2['UO2 Assembly'])

#A3
lattices3 = {}
# Instantiate the UO2 Lattice
lattices3['UO2 Assembly'] = openmc.RectLattice()
lattices3['UO2 Assembly'].dimension = [17, 17]
lattices3['UO2 Assembly'].lower_left = [-10.71, -10.71]
lattices3['UO2 Assembly'].pitch = [1.26, 1.26]
lattices3['UO2 Assembly'].universes = \
[[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u3, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, u3, u2, u2],
[u2, u2, u2, g, u2, u2, u2, u2, u2, u2, u2, u2, u2, g, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u3, u2, u2, u2, u3, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u3, u2, u2, u2, u2, u2, u2, u2, u3, u2, u2, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, u2, u3, u2, u2, u2, u2, u2, u2, u2, u3, u2, u2, u2, u2],
[u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2],
[u2, u2, u2, u2, u2, u2, u3, u2, u2, u2, u3, u2, u2, u2, u2, u2, u2],
[u2, u2, u2, g, u2, u2, u2, u2, u2, u2, u2, u2, u2, g, u2, u2, u2],
[u2, u2, u3, u2, u2, g, u2, u2, g, u2, u2, g, u2, u2, u3, u2, u2],
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
[u1, u1, u3, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u3, u1, u1],
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
[u1, u1, u3, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u3, u1, u1],
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
[u1, u1, u3, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u3, u1, u1],
[u1, u1, u1, g, u1, u1, u1, u1, u1, u1, u1, u1, u1, g, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u3, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u3, g, u1, u1, g, u1, u1, g, u3, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u3, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, g, u1, u1, u1, u1, u1, u1, u1, u1, u1, g, u1, u1, u1],
[u1, u1, u3, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u3, u1, u1],
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
[u1, u1, u1, u1, u3, u1, u1, u1, u1, u1, u1, u1, u3, u1, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, g, u1, u1, u3, u1, u1, u1, u3, u1, u1, g, u1, u1, u1],
[u1, u3, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u3, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u3, u1, u1, u3, u1, u1, u1, u3, u1, u1, u3, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u3, u1, u1, u3, u1, u1, u1, u3, u1, u1, u3, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u3, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u1, u3, u1],
[u1, u1, u1, g, u1, u1, u3, u1, u1, u1, u3, u1, u1, g, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, u1, u3, u1, u1, u1, u1, u1, u1, u1, u3, u1, u1, u1, u1],
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
[u1, u1, u1, u3, u1, u1, u1, u1, u1, u1, u1, u1, u1, u3, u1, u1, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u3, u1, g, u1, u1, u1, u3, u1, u3, u1, u1, u1, g, u1, u3, u1],
[u1, u1, u1, u1, u3, u1, u1, u1, u1, u1, u1, u1, u3, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u1, u1, u3, u1, u1, u1, u3, u1, u1, u1, u1, u1, u1],
[u1, u1, u1, u3, u1, u1, u1, u1, u1, u1, u1, u1, u1, u3, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u3, u1, u1, u1, u1, u1, u1, u1, u1, u1, u3, u1, u1, u1],
[u1, u1, u1, u1, u1, u1, u3, u1, u1, u1, u3, u1, u1, u1, u1, u1, u1],
[u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1],
[u1, u1, u1, u1, u3, u1, u1, u1, u1, u1, u1, u1, u3, u1, u1, u1, u1],
[u1, u3, u1, g, u1, u1, u1, u3, u1, u3, u1, u1, u1, g, u1, u3, u1],
[u1, u1, u1, u1, u1, g, u1, u1, g, u1, u1, g, u1, u1, u1, u1, u1],
[u1, u1, u1, u3, u1, u1, u1, u1, u1, u1, u1, u1, u1, u3, u1, u1, u1],
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
settings_file.temperature = {'method':'interpolation'}
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = particles

# Create an initial uniform spatial source distribution over fissionable zones
bounds = [-97, -97, -200, 97, 97, 200]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings_file.source = openmc.source.Source(space=uniform_dist)

settings_file.trigger_active = True
settings_file.trigger_max_batches = 100
settings_file.export_to_xml()


###############################################################################
#                   Exporting to OpenMC plots.xml file
###############################################################################

plot_xy = openmc.Plot(plot_id=1)
plot_xy.filename = 'plot_xy'
plot_xy.origin = [0, 0, 0]
plot_xy.width = [204, 204]
plot_xy.pixels = [10000, 10000]
plot_xy.color_by = 'material'
plot_xy.colors=colors={fuel1:(102,0,0),
fuel2:(153,0,0),
IFBA:(0,0,0),
moderator:(51,153,255),
clad1:(128,128,128),
poison:(255,0,0),
helium:(102,255,102)}

plot_yz = openmc.Plot(plot_id=2)
plot_yz.filename = 'plot_yz'
plot_yz.basis = 'yz'
plot_yz.origin = [0, 0, 0]
plot_yz.width = [250, 200]
plot_yz.pixels = [500, 500]
plot_yz.color_by = 'material'
plot_yz.colors=colors={fuel1:(102,0,0),
fuel2:(153,0,0),
IFBA:(0,0,0),
moderator:(51,153,255),
clad1:(128,128,128),
poison:(255,0,0),
helium:(102,255,102)}

# Instantiate a Plots collection, add plots, and export to XML
plot_file = openmc.Plots((plot_xy, plot_yz))
plot_file.export_to_xml()

###############################################################################
#                   Exporting to OpenMC tallies.xml file
###############################################################################
tallies_file = openmc.Tallies()
# Instantiate a tally mesh
mesh = openmc.RegularMesh(mesh_id=1)
mesh.dimension = [17*3, 17*3]
mesh.lower_left = [-32.13, -10.71]
mesh.upper_right=[+10.71,+32.13]


# Instantiate tally Filter
mesh_filter = openmc.MeshFilter(mesh)

# Instantiate tally Trigger
trigger = openmc.Trigger(trigger_type='rel_err', threshold=1E-2)
trigger.scores = ['all']

# Instantiate the Tally
tally = openmc.Tally(tally_id=1)
tally.filters = [mesh_filter]
tally.scores = ['flux','fission']
tally.triggers = [trigger]
tallies_file.append(tally)
# Instantiate a Tallies collection and export to 
tallies_file.export_to_xml()
