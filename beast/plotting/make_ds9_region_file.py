from astropy.table import Table
from astropy.coordinates import Angle
from astropy import units as u

def region_file_fits(input_file, col_color=None, col_thresh=None):
    """
    Make a ds9 region file out of the catalog or AST fits file.

    If you want some circles to be a different color, use the col_color and
    col_thresh to choose the column and threshold.

    The region file will be saved in the same place and with the same name as
    input file, but with .reg instead of .fits.

    Parameters
    ----------
    input_files : string
        path+file of the catalog or AST fits file

    col_color : string (default=None)
        name of the column to use for coloring region circles differently

    col_thresh : float (default=None)
        sources with values greater than this will have regions colored differently
    """

    with open(input_file.replace('.fits','.reg'),'w') as ds9_file:
        ds9_file.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
        ds9_file.write('fk5\n')

        # read in the catalog
        cat = Table.read(input_file)
        # figure out which column names are the RA and Dec
        ra_col = [x for x in cat.colnames if 'RA' in x.upper()][0]
        dec_col = [x for x in cat.colnames if 'DEC' in x.upper()][0]

        # no differently colored regions
        if col_color is None:
            for i in range(len(cat)):
                ds9_file.write('circle(' +
                    Angle(cat[ra_col][i], u.deg).to_string(unit=u.hour, sep=':')
                    + ',' +
                    Angle(cat[dec_col][i], u.deg).to_string(unit=u.deg, sep=':')
                    + ',0.1")\n' )

        # with differently colored regions
        if col_color is not None:
            for i in range(len(cat)):
                if cat[col_color][i] <= col_thresh:
                    ds9_file.write('circle(' +
                        Angle(cat[ra_col][i], u.deg).to_string(unit=u.hour, sep=':')
                        + ',' +
                        Angle(cat[dec_col][i], u.deg).to_string(unit=u.deg, sep=':')
                        + ',0.1")\n' )
                else:
                    ds9_file.write('circle(' +
                        Angle(cat[ra_col][i], u.deg).to_string(unit=u.hour, sep=':')
                        + ',' +
                        Angle(cat[dec_col][i], u.deg).to_string(unit=u.deg, sep=':')
                        + ',0.1") # color=magenta \n' )



def region_file_txt(input_file, col_color=None, col_thresh=None):
    """
    Same as the function above, but for a text file - specifically, the DOLPHOT
    artificial star input file generated by make_ast_xy_list.py.

    Parameters
    ----------
    input_files : string
        path+file of the AST input file

    col_color : string (default=None)
        name of the column to use for coloring region circles differently

    col_thresh : float (default=None)
        sources with values greater than this will have regions colored differently
    """

    with open(ast_file.replace('.txt','.reg'),'w') as ds9_file:
        ds9_file.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
        ds9_file.write('image\n')

        cat = Table.read(ast_file, format='ascii')

        # no differently colored regions
        if col_color is None:
            for i in range(len(cat)):
                ds9_file.write('circle({0},{1},0.1")\n'.format(cat['X'][i],cat['Y'][i]) )

        # with differently colored regions
        if col_color is not None:
            for i in range(len(cat)):
                if cat[col_color][i] <= col_thresh:
                    ds9_file.write('circle({0},{1},0.1")\n'.format(cat['X'][i],cat['Y'][i]) )
                else:
                    ds9_file.write('circle({0},{1},0.1") # color=magenta \n'.format(cat['X'][i],cat['Y'][i]) )
