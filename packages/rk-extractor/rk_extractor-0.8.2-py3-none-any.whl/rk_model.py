import re
import os
import zfit
import numpy
import pprint
import zutils.utils      as zut
import utils_noroot      as utnr
import hqm.model         as hqm_model
import matplotlib.pyplot as plt

from importlib.resources import files
from rkex_model          import model
from zutils.plot         import plot                     as zfp
from scales              import scales                   as scl
from stats.average       import average                  as stav
from logzero             import logger                   as log
from builder             import builder                  as cb_builder
from misID_tools.zmodel  import misID_real_model_builder as msid

#---------------------------------------------------------------
class rk_model(model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._d_val = {} 
        self._d_var = {} 

        self._nsig_ee    = None
        self._nsig_mm    = None
        self._read_yields= True
    #---------------------------------------------------------------
    @property
    def read_yields(self):
        return self._read_yields

    @read_yields.setter
    def read_yields(self, value):
        '''
        If true, will try to read yields from JSON files. This is needed to make toys
        not for actual fit to data
        '''
        self._read_yields= value
    #---------------------------------------------------------------
    def _preffix_to_info(self, preffix):
        regex = '(ee|mm)_(r1|r2p1|2017|2018|all)_(TOS|TIS)_.*'
        mtch  = re.match(regex, preffix)
        try:
            [chan, dset, trg] = mtch.groups()
        except:
            log.error(f'Cannot extract dataset and trigger from: {preffix}')
            raise

        trig = {'mm_TOS' : 'MTOS', 'mm_TIS' : 'MTIS', 'ee_TOS' : 'ETOS', 'ee_TIS' : 'GTIS'} [f'{chan}_{trg}']

        return dset, trig
    #---------------------------------------------------------------
    def _add_constraints(self, d_cns):
        d_val = { name : cns[0]    for name, cns in d_cns.items() }
        d_var = { name : cns[1]**2 for name, cns in d_cns.items() }

        self._d_val.update(d_val)
        self._d_var.update(d_var)
    #---------------------------------------------------------------
    def _get_combinatorial(self, preffix, fix_norm=False):
        dset, trig    = self._preffix_to_info(preffix) 
        obj           = cb_builder(dset=dset, trigger=trig, vers=self._comb_vers, q2bin='high', const=False)
        log.warning(f'Not using OS-SS correction, just SS to get combinatorial')
        cmb, d_cns    = obj.get_pdf(obs=self._obs, unc=0, preffix=f'cb_{preffix}', name='Combinatorial') 

        self._add_constraints(d_cns)

        name  = r'$\mu\mu$' if preffix.startswith('mm_') else 'ee'
        nent  = self._get_entries(nsig=None, kind='cmb', trigger=trig, year=dset)
        ncb   = zfit.Parameter(f'ncb_{preffix}', nent, 0, 100000)
        ncb.floating = not fix_norm 

        cmb.set_yield(ncb)

        return cmb 
    #---------------------------------------------------------------
    def _get_rare_scale(self, year, trigger, kind):
        l_all_year = ['2011', '2012', '2015', '2016', '2017', '2018']

        if   year in l_all_year:
            obj      = scl(dset=year, trig=trigger, kind=kind)
            val, err = obj_1.get_scale()

            return val, err
        elif year == 'r1':
            l_year = ['2011', '2012']
        elif year == 'r2p1':
            l_year = ['2015', '2016']
        elif year == 'all':
            l_year = l_all_year 
        else:
            log.error(f'Invalid year: {year}')
            raise

        l_val = []
        l_err = []
        for dset in l_year: 
            obj      = scl(dset=dset, trig=trigger, kind=kind)
            val, err = obj.get_scale()
            l_val.append(val)
            l_err.append(err)

        arr_val     = numpy.array(l_val)
        arr_err     = numpy.array(l_err)
        val, err, _ = stav(arr_val, arr_err)

        return val, err
    #---------------------------------------------------------------
    def _get_entries_from_json(self, kind=None, trig=None, year=None):
        if not self._read_yields:
            log.warning(f'Not reading yields from JSON for {kind}/{trig}/{year}, using zero events')
            return 0

        json_path = files('extractor_data').joinpath(f'sb_fits/{self._norm_vers}/{year}_{trig}.json')
        if not os.path.isfile(json_path):
            log.error(f'Cannot find: {json_path}')
            raise FileNotFoundError

        d_par = utnr.load_json(json_path)
        for key, [val, _] in d_par.items():
            flg_1 = key.startswith('ncb_') and kind == 'cmb'
            flg_2 = key.startswith('npr_') and kind == 'prc'
            if flg_1 or flg_2:
                return val

        log.error(f'Cannot find yield for {kind} among:')
        pprint.pprint(d_par)
        raise
    #---------------------------------------------------------------
    def _get_entries(self, nsig=None, kind=None, trigger=None, year=None):
        if   kind in ['prc', 'cmb']:
            nent  = self._get_entries_from_json(kind=kind, trig=trigger, year=year)

            log.info(f'Taking {kind} yield from JSON as: {nent:.0f}')
        elif kind in ['bpks', 'bdks', 'bsph', 'bpk1', 'bpk2']:
            scale = self._get_rare_scale(year, trigger, kind)
            scl   = scale[0]
            nent  = nsig * scl

            log.info(f'Taking {kind} yield as {nent:.0f}={scl:.3f} * {nsig:.0f}')
        else:
            log.error(f'Invalid kind: {kind}')
            raise

        return nent
    #---------------------------------------------------------------
    def _get_signal(self, preffix, nent=None):
        year, trig = self._preffix_to_info(preffix)
        log.warning(f'Using 2018 signal for {year}')
        year = '2018'
        sig, d_cns = hqm_model.get_signal_shape(dataset=year, trigger=trig, parameter_name_prefix=preffix)

        self._add_constraints(d_cns)

        nsg    = zfit.Parameter(f'nsg_{preffix}', nent, 0, 100000)
        esig   = sig.create_extended(nsg, name='Signal')

        if   preffix.startswith('ee_'):
            self._nsig_ee = nsg 
        elif preffix.startswith('mm_'):
            self._nsig_mm = nsg 
        else:
            log.error(f'Invalid preffix: {preffix}')
            raise ValueError

        return esig
    #---------------------------------------------------------------
    def _get_rare_kind(self, kind, year, trig):
        log.debug(f'Building: {kind}')

        if   kind == 'bpks':
            pdf = hqm_model.get_Bu2Ksee_shape(dataset=year, trigger=trig)
        elif kind == 'bdks':
            pdf = hqm_model.get_Bd2Ksee_shape(dataset=year, trigger=trig)
        elif kind == 'bsph':
            pdf = hqm_model.get_Bs2phiee_shape(dataset=year, trigger=trig)
        elif kind == 'bpk1':
            pdf = hqm_model.get_Bu2K1ee_shape(dataset=year, trigger=trig)
        elif kind == 'bpk2':
            pdf = hqm_model.get_Bu2K2ee_shape(dataset=year, trigger=trig)
        else:
            log.error(f'Invalid kind: {kind}')
            raise ValueError

        return pdf
    #---------------------------------------------------------------
    def _get_rare(self, preffix, nent=None, kind=None):
        year, trig = self._preffix_to_info(preffix)

        if year == 'all':
            d_pdf = { dset : self._get_rare_kind(kind, dset, trig) for dset in self._l_all_dset }
            pdf   = self._merge_year_pdf(d_pdf, preffix, kind)
        else:
            pdf   = self._get_rare_kind(kind, year, trig) 

        nrare   = self._get_entries(nent, kind, trigger=trig, year=year)
        ns_o_nr = self._nsig_ee.value() / nrare 
        nbkg    = zfit.ComposedParameter(f'nr{kind}_{preffix}', lambda ns : ns / ns_o_nr, params=[self._nsig_ee])
        pdf.set_yield(nbkg)

        return pdf 
    #---------------------------------------------------------------
    def _merge_year_pdf(self, d_pdf, preffix, kind):
        l_dset  = list(d_pdf.keys())
        l_lumi  = [ self._d_lumi[dset] for dset in l_dset ]
        tot_lum = sum(l_lumi)
        d_frac  = { dset : lumi / tot_lum for dset, lumi in zip(l_dset, l_lumi) }

        l_lfr_par = []
        for dset in d_pdf:
            frac= d_frac[dset]
            lfr = zfit.Parameter(f'lfr_{dset}_{preffix}_{kind}', frac , 0., 1.)
            lfr.floating = False
            l_lfr_par.append(lfr)

        l_pdf = [ pdf for pdf in d_pdf.values()]
        pdf   = zfit.pdf.SumPDF(l_pdf, l_lfr_par, name=kind)

        return pdf
    #---------------------------------------------------------------
    def _get_prec(self, preffix):
        log.debug(f'Getting cc PRec: {preffix}')

        year, trig = self._preffix_to_info(preffix)

        if year == 'all':
            d_pdf = { dset : hqm_model.get_part_reco(dataset=dset, trigger=trig, parameter_name_prefix=preffix) for dset in self._l_all_dset }
            pdf   = self._merge_year_pdf(d_pdf, preffix, 'prc')
        else:
            pdf   = hqm_model.get_part_reco(dataset=year, trigger=trig, parameter_name_prefix=preffix)

        nent= self._get_entries(nsig=None, kind='prc', trigger=trig, year=year)
        npr = zfit.Parameter(f'npr_{preffix}', nent, 0, 100000)
        pdf.set_yield(npr)

        return pdf 
    #---------------------------------------------------------------
    def _get_msid(self, preffix):
        log.debug(f'Getting mis-ID for: {preffix}')

        dset, trig    = self._preffix_to_info(preffix)
        bld= msid(name='Mis-ID', version=self._msid_vers, obs=self._obs, preffix=preffix)
        bld.load_model(dset, trig)
        pdf=bld.build_model() 

        return pdf
    #---------------------------------------------------------------
    def _add_combinatorial(self, l_pdf, preffix):
        log.debug(f'Adding combinatorial for {preffix}')

        cbkg      = self._get_combinatorial(preffix, fix_norm = False)
        l_pdf.insert(0, cbkg)

        return l_pdf
    #---------------------------------------------------------------
    def _get_pdf(self, preffix='', nent=None):
        preffix   = f'{preffix}_{self._preffix}'
        _, trig   = self._preffix_to_info(preffix)
        if trig == 'MTIS':
            return None

        esig      = self._get_signal(preffix, nent=nent)
        self._obs = esig.space

        if   preffix.startswith('ee_'):
            erbp  = self._get_rare(preffix, nent=nent, kind='bpks')
            erbd  = self._get_rare(preffix, nent=nent, kind='bdks')
            erbs  = self._get_rare(preffix, nent=nent, kind='bsph')
            erb1  = self._get_rare(preffix, nent=nent, kind='bpk1')
            erb2  = self._get_rare(preffix, nent=nent, kind='bpk2')
            eprc  = self._get_prec(preffix)
            emis  = self._get_msid(preffix)

            l_pdf = [eprc, erbp, erbd, erbs, erb1, erb2, emis, esig]
        elif preffix.startswith('mm_'):
            l_pdf = [esig]
        else:
            log.error(f'Invalid preffix: {preffix}')
            raise

        l_pdf = self._add_combinatorial(l_pdf, preffix)
        pdf   = l_pdf[0] if len(l_pdf) == 1 else zfit.pdf.SumPDF(l_pdf) 

        return pdf 
    #---------------------------------------------------------------
    def _get_pdf_names(self):
        d_leg = {}
        d_leg['part_reco_2018_GTIS'] = r'$\psi(2S) + c\bar{c}$'
        d_leg['Bu2Ksee_2018_GTIS']   = r'$B^+\to K^{*+}e^+e^-$'
        d_leg['Bd2Ksee_2018_GTIS']   = r'$B^0\to K^{*0}e^+e^-$'
        d_leg['Bs2phiee_2018_GTIS']  = r'$B_s\to \phi e^+e^-$'
        d_leg['Bu2K1ee_2018_GTIS']   = r'$B^+\to K_{1}e^+e^-$'
        d_leg['Bu2K2ee_2018_GTIS']   = r'$B^+\to K_{2}e^+e^-$'

        d_leg['part_reco_2018_ETOS'] = r'$\psi(2S) + c\bar{c}$'
        d_leg['Bu2Ksee_2018_ETOS']   = r'$B^+\to K^{*+}e^+e^-$'
        d_leg['Bd2Ksee_2018_ETOS']   = r'$B^0\to K^{*0}e^+e^-$'
        d_leg['Bs2phiee_2018_ETOS']  = r'$B_s\to \phi e^+e^-$'
        d_leg['Bu2K1ee_2018_ETOS']   = r'$B^+\to K_{1}e^+e^-$'
        d_leg['Bu2K2ee_2018_ETOS']   = r'$B^+\to K_{2}e^+e^-$'

        return d_leg
    #---------------------------------------------------------------
    def _plot_model(self, key, mod):
        if self._out_dir is None:
            return

        plt_dir = f'{self._out_dir}/plots/models'
        os.makedirs(plt_dir, exist_ok=True)

        obj= zfp(data=mod.create_sampler(fixed_params=False), model=mod)
        obj.plot(nbins=50, d_leg=self._get_pdf_names(), ext_text=key, stacked=True, skip_pulls=False)

        log.info(f'Saving to: {plt_dir}/{key}.png')
        plt.savefig(f'{plt_dir}/{key}.png')
        plt.close('all')

        d_const = {}
        for name in self._d_val:
            val = self._d_val[name]
            var = self._d_var[name]
            d_const[name] = [val, var]

        log.info(f'Saving to: {plt_dir}/{key}.txt')
        zut.print_pdf(mod, d_const=d_const, txt_path=f'{plt_dir}/{key}.txt')
    #---------------------------------------------------------------
    def get_cons(self):
        '''
        Will return constraints on model parameters 

        Returns
        -----------
        d_val, d_var: Tuple of dictionaries pairing parameter name with value (mu of Gaussian) and 
        variance respectively.
        '''
        self._initialize()

        log.debug('-' * 20)
        log.debug(f'{"Name":<40}{"Value":<15}{"Variance":<15}')
        log.debug('-' * 20)
        for name in self._d_val:
            val = self._d_val[name]
            var = self._d_var[name]

            log.debug(f'{name:<40}{val:<15.3f}{var:<15.3f}')
        log.debug('-' * 20)

        return self._d_val, self._d_var
#---------------------------------------------------------------

