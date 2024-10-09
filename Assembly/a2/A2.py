import openmc

###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# OpenMC simulation parameters
batches = 100
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

fuel2 = openmc.Material(material_id=2, name='fuel2')
fuel2.set_density('g/cc', 10.286)
fuel2.add_nuclide('U235',2.82,percent_type='wo' )
fuel2.add_nuclide('U238',85.325,percent_type='wo' )
fuel2.add_nuclide('O16',11.853,percent_type='wo' )


IFBA=openmc.Material(material_id=3, name='ifba')
IFBA.set_density('g/cc', 10.017)
IFBA.add_element('U',81.09,percent_type='wo' )
IFBA.add_element('Gd',6.9408,percent_type='wo' )
IFBA.add_nuclide('O16',11.9692,percent_type='wo' )

moderator = openmc.Material(material_id=4, name='moderator')
moderator.set_density('g/cc', 1.0)
moderator.add_element('H', 2.)
moderator.add_element('O', 1.)
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
materials_file = openmc.Materials([fuel1,fuel2,IFBA,moderator,clad1,poison,helium])
materials_file.export_to_xml()

###############################################################################
#                 Exporting to OpenMC geometry.xml file
###############################################################################
p=1.26
n=17
l=(n*p)/2
k=(n*p)

# Instantiate Surfaces and boundary type
left = openmc.XPlane(surface_id=1, x0=-l, name='left')
right = openmc.XPlane(surface_id=2, x0=l, name='right')
bottom = openmc.YPlane(surface_id=3, y0=-l, name='bottom')
top = openmc.YPlane(surface_id=4, y0=l, name='top')

pinrad = openmc.ZCylinder(surface_id=5, x0=0, y0=0, r=0.4096)
cladin = openmc.ZCylinder(surface_id=6, x0=0, y0=0, r=0.41875)
cladout = openmc.ZCylinder(surface_id=7, x0=0, y0=0, r=0.47500)


cri = openmc.ZCylinder(surface_id=8, x0=0, y0=0, r=0.56150)
cro = openmc.ZCylinder(surface_id=9, x0=0, y0=0, r=0.61200)

ifrad = openmc.ZCylinder(surface_id=10, x0=0, y0=0, r=0.4096)
cladfin = openmc.ZCylinder(surface_id=11, x0=0, y0=0, r=0.41875)
cladfout = openmc.ZCylinder(surface_id=12, x0=0, y0=0, r=0.47500)

left.boundary_type = 'reflective'
right.boundary_type = 'reflective'
top.boundary_type = 'reflective'
bottom.boundary_type = 'reflective'


# Instantiate Cells
rootcell = openmc.Cell()
cell1 =openmc.Cell()
cell2 =openmc.Cell()
cell3 = openmc.Cell()
cell4 = openmc.Cell()
cell5 = openmc.Cell()
cell6 = openmc.Cell()
cell7 = openmc.Cell()
cell8 = openmc.Cell()
cell9 = openmc.Cell()
cell10 = openmc.Cell()
cell11 = openmc.Cell()
cell12 = openmc.Cell()
cell13 = openmc.Cell()
cell14 = openmc.Cell()
cell15 = openmc.Cell()

# fuel type 1 cell definition
cell1.region = -pinrad
cell2.region = +pinrad & -cladin
cell3.region = +cladin & - cladout
cell4.region = +cladout
#Assigning materials to fuel type 1 cell
cell1.fill = fuel1
cell2.fill = helium
cell3.fill = clad1
cell4.fill = moderator
# Fuel type 1 universe
u1 = openmc.Universe()
u1.add_cells([cell1, cell2, cell3, cell4])
# fuel type 2 cell definition
cell5.region = -pinrad
cell6.region = +pinrad & -cladin
cell7.region = +cladin & - cladout
cell8.region = +cladout
#Assigning materials to fuel  type 2 cell
cell5.fill = fuel2
cell6.fill = helium
cell7.fill = clad1
cell8.fill = moderator
# Fuel type 2 universe
u2 = openmc.Universe()
u2.add_cells([cell5, cell6, cell7, cell8])
# IFBA definition
cell9.region = -ifrad
cell10.region = +ifrad & -cladfin
cell11.region = +cladfin & - cladfout
cell12.region = +cladfout
#Assigning materials to IFBA
cell9.fill = IFBA
cell10.fill = helium
cell11.fill = clad1
cell12.fill = moderator
# IFBA universe
u3 = openmc.Universe()
u3.add_cells([cell9, cell10, cell11, cell12])
# Guide tube definition
cell13.region = -cri
cell14.region = +cri & -cro
cell15.region = +cro
#Assigning materials to guide tube
cell13.fill = helium
cell14.fill = clad1
cell15.fill = moderator
# guide tube universe
g=openmc.Universe()
g.add_cells([cell13,cell14,cell15])

# Instantiate a Lattice
lattice = openmc.RectLattice()
lattice.lower_left = [-l, -l]

lattice.pitch = [p, p]
lattice.universes = \
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


#ROOT cell definition
rootcell.region = +left & -right & +bottom & -top
rootcell.fill = lattice
root = openmc.Universe( name='root universe', cells=[rootcell])

# Instantiate a Geometry, register the root Universe, and export to XML
geometry = openmc.Geometry(root)
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
bounds = [-1, -1, -1, 1, 1, 1]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings_file.source = openmc.source.Source(space=uniform_dist)

settings_file.trigger_active = True
settings_file.trigger_max_batches = 100
settings_file.export_to_xml()


###############################################################################
#                   Exporting to OpenMC plots.xml file
###############################################################################

plot = openmc.Plot(plot_id=1)
plot.origin = [0, 0, 0]
plot.width = [k, k]
plot.pixels = [800, 800]
plot.color_by = 'material'
plot.colors = {
fuel1: 'red',
fuel2: 'pink',
IFBA: 'purple',
clad1: 'black',
moderator: 'blue',
helium: 'green',
poison: 'yellow' }


# Instantiate a Plots collection and export to XML
plot_file = openmc.Plots([plot])
plot_file.export_to_xml()


###############################################################################
#                   Exporting to OpenMC tallies.xml file
###############################################################################

# Instantiate a tally mesh
mesh = openmc.RegularMesh(mesh_id=1)
mesh.dimension = [4, 4]
mesh.lower_left = [-2, -2]
mesh.width = [1, 1]

# Instantiate tally Filter
mesh_filter = openmc.MeshFilter(mesh)

#Create a flux tally
flux_tally = openmc.Tally()
flux_tally.scores = ['flux']

# Instantiate a Tallies collection and export to XML
tallies_file = openmc.Tallies([flux_tally])
tallies_file.export_to_xml()

