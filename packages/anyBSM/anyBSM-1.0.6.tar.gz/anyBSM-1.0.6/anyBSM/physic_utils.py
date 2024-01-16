import cmath

def RunAlfas(Qstart, Qend, AlfasIn):
    """Performs 1L leading-log running of $\\alpha_s$ in the SM.

    Args:
        Qstart: the input scale in GeV.
        Qend: the end scale in GeV.
        AlfasIn: $\\alpha_s(Q_\\text{start})$.

    Returns:
        $\\alpha_s(Q_\\text{end})$
    """
    return AlfasIn/(1 + (11 - 10/3.)/(4*cmath.pi)*AlfasIn*cmath.log((Qend/Qstart)**2))

def MZfw(MZrun, GammaZ = 2.4952):
    """Converts $M_Z$ defined with running width to $M_Z$ defined with fixed width.

    Args:
        MZrun: $M_Z$ defined with running width
        GammaZ: total decay width of the $Z$ boson

    Returns:
        $M_Z$ defined with fixed width
    """
    return MZrun - 0.5*GammaZ**2/MZrun

def MZrun(MZfw, GammaZ = 2.4952):
    """Converts $M_Z$ defined with fixed width to $M_Z$ defined with running width.

    Args:
        MZfw: $M_Z$ defined with fixed width
        GammaZ: total decay width of the $Z$ boson

    Returns:
        $M_Z$ defined with running width
    """
    return MZfw + 0.5*GammaZ**2/MZfw

def MWfw(MWrun, AlfasMW, GF):
    """Converts $M_W$ defined with running width to $M_W$ defined with fixed width.

    Args:
        MWrun: $M_W$ defined with running width
        AlfasMW: $\\alpha_s(M_W)$
        GF: the Fermi constant $G_F$

    Returns:
        $M_W$ defined with fixed width
    """
    return MWrun*(1 - (3/(4*cmath.pi)*GF*MWrun**2*(1 + 2/(3*cmath.pi)*AlfasMW))**2)

def MWrun(MWfw, AlfasMW, GF):
    """Converts $M_W$ defined with fixed width to $M_W$ defined with running width.

    Args:
        MWfw: $M_W$ defined with fixed width
        AlfasMW: $\\alpha_s(M_W)$
        GF: the Fermi constant $G_F$

    Returns:
        $M_W$ defined with running width
    """
    return MWfw*(1 + (3/(4*cmath.pi)*GF*MWfw**2*(1 + 2/(3*cmath.pi)*AlfasMW))**2)
