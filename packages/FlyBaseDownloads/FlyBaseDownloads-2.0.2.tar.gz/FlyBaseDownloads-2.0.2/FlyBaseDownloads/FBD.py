#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 14:19:10 2024

@author: javicolors
"""

"""

Unofficial wrapper of FlyBase Database

"""
from .classes.Synonyms import Synonyms
from .classes.Genes import Genes
from .classes.Gene_Ontology_annotation import Gene_Ontology_annotation
from .classes.Gene_groups import Gene_groups
from .classes.Homologs import Homologs
from .classes.Ontology_Terms import Ontology_Terms
from .classes.Organisms import Organisms
from .classes.Insertions import Insertions
from .classes.Clones import Clones
from .classes.References import References
from .classes.Alleles_Stocks import Alleles_Stocks
from .classes.Human_disease import Human_disease

from .utilities.authentication import Authentication
from .utilities.database import RTD
from .utilities.internet import Check_internet

#%%

class FBD():
    
    def __name__(self):
        self.__name__ = 'FlyBase Downloads'
    
    def __init__(self, email):
        continue_ = Check_internet.check_internet_connection()
        self.email = email
        
        auth = Authentication(continue_)
        credential_key = auth.get_user(self.email)
        self.rtd = RTD(credential_key)
        
        main_url = 'ftp://ftp.flybase.net/releases/current/precomputed_files/'
        
        self.Synonyms = Synonyms(main_url, credential_key, continue_)
        self.Genes = Genes(main_url, credential_key, continue_)
        self.GOAnn = Gene_Ontology_annotation(main_url, credential_key, continue_) 
        self.Gene_groups = Gene_groups(main_url, credential_key, continue_)
        self.Homologs = Homologs(main_url, credential_key, continue_)
        self.Ontology_Terms = Ontology_Terms(main_url, credential_key, continue_)
        self.Organisms = Organisms(main_url, credential_key, continue_)
        self.Insertions = Insertions(main_url, credential_key, continue_)
        self.Clones = Clones(main_url, credential_key, continue_)
        self.References = References(main_url, credential_key, continue_)
        self.Alleles_Stocks = Alleles_Stocks(main_url, credential_key, continue_)
        self.Human_disease = Human_disease(main_url, credential_key, continue_)
            
        

    def close_app(self):
        try:
            self.rtd.def_reg()
        except:
            pass
        

        
    