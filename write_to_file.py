import numpy as np
from typing import Optional
import datetime

def make_up_arrays(size:int=260):
    """
    Just making up some arrays for testing

    Parameters
    ----------
    size : int, optional
        DESCRIPTION. The default is 260.

    Returns
    -------
    atoms : TYPE
        DESCRIPTION.
    bonds : TYPE
        DESCRIPTION.
    angles : TYPE
        DESCRIPTION.

    """
    #arrays
    atoms = np.random.rand(size,6).astype(np.float32)
    atoms =atoms*120-60
    bonds = np.ones([size,4]).astype(int)
    angles = np.ones([size,5]).astype(int)
    
    #setting their ids
    atoms[:,0] = np.arange(len(atoms))+1
    bonds[:,0] = np.arange(len(bonds))+1
    angles[:,0] = np.arange(len(angles))+1
    
    #setting the types
    #for atoms
    atoms[:,1] = 1
    atoms[:100,1] = 2
    atoms[-100:,1] = 3
    atoms[:,2] = atoms[:,1]
    
    #for bonds
    bonds[:,1] = 1
    bonds[:100,1] = 2
    bonds[-100:,1] = 3
    
    #for angles
    angles[:,1] = 1
    angles[:100,1] = 2
    angles[-100:,1] = 3
    
    return atoms,bonds,angles

def arr2str(arr:np.ndarray,name:str,style:Optional[str]=None)->str:
    """
    Turn array into str with the LAMMPS data file format.

    Parameters
    ----------
    arr : np.ndarray
        Array to be t.
    name : str
        Name of the array (Atoms, Angles, Bonds,...)
    style : str
        Style of the given array.

    Returns
    -------
    str
        String version of the array with the title of 'name # style'.

    """
    
    name = name.capitalize() #a precaution for format req.
    #initing strimng with the title 
    if style:
        style = style.lower()#another precuation for format req.
        string = f'{name} # {style}\n\n'
    else:
        string = f'{name}\n\n'
    
    #browsing through every value
    for row in arr:
        for val in row:
            #if the value is integer they are removed off their decimals
            if int(val) == val:
                string+= f'{int(val)} '
            else:
                string+= f'{val} '
        
        #go next line after every row        
        string+='\n'
    
    #leaving a gap for the next array to be written
    string+='\n'
    
    return string #final str is returned


def describe(*arr_tup:tuple)->str:
    """
    Description part of the data file.
    e.g.,
    1234 atoms
    12 atom type
    ...

    Parameters
    ----------
    *arr_tup : tuple
        Array itself and its Name as such (arr,tuple) e.g. (atoms,'atoms')

    Returns
    -------
    str
        Description of the simulation components.

    """
    date = datetime.datetime.now().date()
    text = f'LAMMPS Data file -- Created in:{date}\n\n'
    for tup in arr_tup:
        #seperating array and its name
        arr = tup[0]
        name = tup[1].lower()
        
        #forming the count line e.g., 1234 atoms
        count = len(arr) #size
        number_line = f'{count} {name}\n'
        
        #forming the type number line 
        type_column = arr[:,1]
        type_num = len(np.unique(type_column))
        type_line = f'{type_num} {name[:-1]} types\n'
        
        text+=number_line+type_line
    
    text += '\n\n'
    
    return  text
        

def simulation_box(xhi:float,yhi:float,zhi:float,
                   mirror:bool=True,**xyz_lows)->str:
    """
    

    Parameters
    ----------
    xhi : float
        x high boundary.
    yhi : float
        y high boundary.
    zhi : float
        z high boundary.
    mirror : bool, optional
        When True, mirrors the high boundaries as their negatives.
        The default is True.
    **xyz_lows : kwargs
        xlo,ylo,zlo.

    Raises
    ------
    ValueError
        if mirror==False and no xlo,ylo,zlo value given.

    Returns
    -------
    str
        Simulation box description text.

    """
    
    text = ''
    err = 'if mirror=False Keyword values of xlo,ylo,zlo must be given --> '
    eg =  'e.g xlo=value1,ylo=value2,zlo=value3'
    if mirror:
        xline=f'{-xhi} {xhi} xlo xhi\n'
        yline=f'{-yhi} {yhi} ylo yhi\n'
        zline=f'{-zhi} {zhi} zlo zhi\n'
        text+=xline+yline+zline
    else:
        if xyz_lows == dict():
            raise ValueError(err+eg)
        xlo = xyz_lows['xlo']
        ylo = xyz_lows['ylo']
        zlo = xyz_lows['zlo']    
            
        xline=f'{xlo} {xhi} xlo xhi\n'
        yline=f'{ylo} {yhi} ylo yhi\n'
        zline=f'{zlo} {zhi} zlo zhi\n'
        text+=xline+yline+zline
            
    text+='\n\n'
            
    return text

def unite_strings(*strings)->str:
    """
    Takes strings and unites them in input order.
    

    Parameters
    ----------
    *strings : str
        String parts.

    Returns
    -------
    str
        United string.

    """
    
    full_str = ''
    
    for string in strings:
        full_str+=string
    
    return full_str

        
if __name__ ==  '__main__':
    
    #some arrays 
    atoms,bonds,angles = make_up_arrays(size=20000)
    
    #initial text describing component
    description = describe((atoms,'atoms'),
                           (bonds,'bonds'),
                           (angles,'angles'))
    
    #simulation box boundaries
    box_str = simulation_box(60.123,60.123,60.123,mirror=1,
                             xlo=55,ylo=31,zlo=15)
    
    #strings of arrays
    atoms_str = arr2str(arr=atoms,name='Atoms',style='angle')
    bonds_str = arr2str(arr=bonds,name='Bonds')
    angles_str = arr2str(arr=angles,name='Angles')
    
    #arrays united --note that order is important
    whole_str = unite_strings(description,
                             box_str,
                             atoms_str,
                             bonds_str,
                             angles_str)
    
    with open('deneme.data','w') as f:
        f.write(whole_str)
    
    
    love = datetime.datetime.now().date()