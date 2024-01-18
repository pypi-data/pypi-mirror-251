__all__ = ['enquire', 'get_charge_string']

from rdkit import Chem
from typing import Mapping, Sequence, Union, List
from IPython.display import Image as IPyImage
from PIL import Image as PILImage
import requests
import io
import warnings


def enquire(mol: Chem.Mol,
                replacements: Mapping[int, Union[str, None]] = {},
                rgroups: Sequence[int] = {},
                generic_arocarbons: bool = False) -> Chem.Mol:
    """
    Given a molecule, convert it to a molecule with query atoms,
    with correct element, number of hydrogens and charge,
    but with overridden values as given by ``replacements`` argument,
    which accepts a dictionary of index (int) to SMARTS (str) or None (delete atom).

    A ``Chem.QueryAtom`` is a special atom with encoded ambiguity.
    ``Chem.MolFromSmarts`` will create a molecule with query atoms, but not a regular mol.
    A query atom has the additional methods
    ``.HasQuery()``, ``.GetQueryType()``, ``.DescribeQuery()``.
    cannot be instantiated from Python, but can be using ``Chem.AtomFromSmarts``.

    Additionally, any atom idx in argument ``rgroups`` will get a sequential isotope number from one
    and property 'R-group' of R + off-by-one number.
    If this index was not in replacements, then the SMARTS will have one connection more than there are
    and one implict hydrogen less.

    This function requires ``mol`` to have implicit hydrogens.

    ..code-block::python
       queried:Chem.Mol = enquire(Chem.MolFromSmiles('c1cnccc1'), {2: '[c,n]'})
       Chem.MolToSmarts(queried)
       # '[c&H1]1:[c&H1]:[c,n]:[c&H1]:[c&H1]:[c&H1]:1'

    Note 1. ``atom.GetSmarts()`` is a method, but it could return '[N+]' already,
    which is complicated to deal with as appending at given positions may muck things up.
    And certain SMILES are not legal, for example 'CC[O+H2]' should be 'CC[OH2+]'

    This method was formerly called ``querimonate``.
    Querimony is a complaint. There is no verb form. This is a jocular neologism,
    as RDKit will complain... But the name is too confusing to write.
    """
    removals: List[int] = []
    mod = Chem.RWMol(mol)
    atom: Chem.Atom
    for smarts in replacements.values():
        if not smarts:
            continue
        else:
            assert Chem.MolFromSmarts(smarts) is not None, f'Could not parse SMARTS {smarts}'
    for atom in mod.GetAtoms():
        assert atom.GetNumRadicalElectrons() == 0, 'This molecule has a radical'
        idx: int = atom.GetIdx()
        n_Hs: int = atom.GetImplicitValence() + atom.GetNumExplicitHs()
        symbol: str = atom.GetSymbol().lower() if atom.GetIsAromatic() else atom.GetSymbol()
        scharge: str = get_charge_string(atom)
        # pick relevant SMARTS
        if idx in replacements:
            # user override replacement
            if isinstance(replacements[idx], str) and replacements[idx] != '':
                smarts: str = replacements[idx]
            else:
                removals.append(idx)
                smarts: str = ''
        elif idx in rgroups:
            # user override rgroups
            assert n_Hs == 0, 'R-group requested for zero Hs. Use charge or change element via ``replacement``'
            n_Xs: int = len(atom.GetNeighbors())
            smarts = f'[{symbol}H{n_Hs - 1}X{n_Xs + 1}]'
        elif not generic_arocarbons or symbol != 'c' or scharge != '':
            # keep as is
            smarts = f'[{symbol}H{n_Hs}{scharge}]'
        elif n_Hs == 1:
            # degenerate aromatic carbon w/ one hydrogen
            smarts = '[aH0X2,aH1X3]'
        else:
            # degenerate aromatic carbon w/ zero hydrogens
            smarts = '[aH0]'
        # swap
        if smarts == '':
            pass  # delete
        elif isinstance(atom, Chem.QueryAtom):
            # weird it is already a query atom
            atom.SetQuery(smarts)
        else:
            mod.ReplaceAtom(idx, Chem.AtomFromSmarts(smarts), preserveProps=True)
    for r, idx in enumerate(rgroups):
        atom = mod.GetAtomWithIdx(idx)
        atom.SetIsotope(r + 1)
        atom.SetProp('R-group', f'R{r + 1}')
    mod.BeginBatchEdit()
    for idx in removals:
        mod.RemoveAtom(idx)
    mod.CommitBatchEdit()
    return mod.GetMol()

def querimonate(*args, **kwargs):
    """
    See ``enquire``.
    """
    warnings.warn('`querimonate` has been renamed `eniquire`. Use `enquire` instead.', DeprecationWarning)
    return enquire(*args, **kwargs)

def get_charge_string(atom: Chem.Atom) -> str:
    """
    Returns a plus or minus string for the charge of an atom.
    :param atom: Chem.Atom
    :return:
    """
    # charge
    charge: int = atom.GetFormalCharge()
    if charge > 0:
        return '+' * abs(charge)
    elif charge < 0:
        return '-' * abs(charge)
    else:
        return ''


def retrieve_smartsplus(smarts: Union[str, Chem.Mol], PIL_image=True, **options) -> Union[IPyImage, PILImage.Image]:
    """
    Given a SMARTS query, retrieve the image from https://smarts.plus.
    The returned object is an IPython.display.Image not a PIL.Image.
    If using this image remember to cite it as
    "SMARTSviewer smartsview.zbh.uni-hamburg.de, ZBH Center for Bioinformatics, University of Hamburg"

    :param smarts: SMARTS query or Chem.Mol
    :param PIL_image: return PIL.Image instead of IPython.display.Image
    :param options: See https://smarts.plus/rest
    :return:
    """
    if isinstance(smarts, Chem.Mol):
        q = smarts
        smarts: str = Chem.MolFromSmarts(q)
    # retrieve from smarts.plus
    response: requests.Response = requests.get('https://smarts.plus/smartsview/download_rest', # noqa to sensitive data in options
                                               {'smarts': smarts, **options}
                                              )
    png_binary: bytes = response.content
    if PIL_image:
        return PILImage.open(io.BytesIO(png_binary))
    else:
        return IPyImage(data=png_binary)
