#    PascalX - A python3 library for high precision gene and pathway scoring for 
#              GWAS summary statistics with C++ backend.
#              https://github.com/BergmannLab/PascalX
#
#    Copyright (C) 2021 Bergmann lab and contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import gzip


class mapper:
    def __init__(self):
        self._GENEIDtoSNP = {}
        self._SNPtoGENEID = {}
        self._GENEDATA = {}
        
    def load_mapping(self,file,gcol=0,rcol=1,wcol=None,a1col=None,a2col=None,bcol=None,delimiter="\t",pfilter=1,header=False):
        """
        Loads a SNP to gene mapping
        
        Args:
        
            file(string): File to load
            gcol(int): Column with gene id
            rcol(int): Column with SNP id
            wcol(int): Column with weight
            a1col(int): Column of alternate allele (None for ignoring alleles)
            a2col(int): Column of reference allele (None for ignoring alleles)
            bcol(int): Column with additional weight
            delimiter(string): Character used to separate columns
            header(bool): Header present
            pfilter(float): Only include rows with wcol < pfilter
        """
        self._GENEIDtoSNP = {}
        self._SNPtoGENEID = {}
        self._GENEDATA = {}
        
        try:
            f = gzip.open(file, "rt")
            if header:
                f.readline()
            else:
                f.readline()
                f.seek(0)
        except OSError:
            f = open(file, "r")
            if header:
                f.readline()

        c = 0
        for line in f:
            line = line.rstrip().split(delimiter)

            if wcol is None or float(line[wcol]) <= pfilter:

                gid = line[gcol]

                if gid not in self._GENEIDtoSNP:
                    self._GENEIDtoSNP[gid] = {} #[[],[],[],[],[]]

                    c = c + 1
                
                rid = line[rcol]
                
                self._GENEIDtoSNP[gid][rid] = [None,None,None,None]
                
                if wcol is not None:
                    self._GENEIDtoSNP[gid][rid][0] = float(line[wcol])
                
                if a1col is not None and a2col is not None:
                    self._GENEIDtoSNP[gid][rid][1] = line[a1col]
                    self._GENEIDtoSNP[gid][rid][2] = line[a2col]

                if bcol is not None:
                    self._GENEIDtoSNP[gid][rid][3] = float(line[bcol])
                                 
                if line[rcol] not in self._SNPtoGENEID:
                    self._SNPtoGENEID[line[rcol]] = [gid]
                else:
                    self._SNPtoGENEID[line[rcol]].append(gid)

        print(c,"gene to SNP mappings loaded")