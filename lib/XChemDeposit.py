# last edited: 16/05/2017, 15:00

import sys
import fileinput
import os
import glob

from PyQt4 import QtGui, QtCore, QtWebKit

from lxml import etree

sys.path.append(os.getenv('XChemExplorer_DIR')+'/lib')
import XChemLog
import XChemDB
import XChemToolTips
import XChemMain
from XChemUtils import pdbtools
from XChemUtils import mtztools
from XChemUtils import smilestools


def create_SF_mmcif(outDir,mtzList):
    print 'hallo'

def get_protein_sequence(database,xtalID):
    print 'hallo'

def check_depositDict(depositDict):
    # check depositDict
    for entry in depositDict:
        if 'middle_name' in depositDict[entry]:
            continue
        elif 'State_or_Province' in depositDict[entry]:
            continue
        elif depositDict[entry] == '':
            print 'ERROR'

def update_title(depositDict):

    print 'hallo'

def create_data_template_text():

    data_template_text=data_template(depositDict,sequence)

def create_Model_mmcif(outDir,pdbList):
    print 'hallo'

#def update_file_locations_of_apo_structuresin_DB(database,projectDir,xce_logfile):
#    Logfile=XChemLog.updateLog(xce_logfile)
#    Logfile.insert('updating file information for apo structures')
#    db=XChemDB.data_source(database)
#    apo=db.execute_statement("select CrystalName from depositTable where StructureType is 'apo';")
#    for item in apo:
#        xtal=str(item[0])
#        db_dict={}
#        db_dict['label']=xtal+'-apo'
#        db_dict['description']='apo structure for pandda.analyse'
#        if os.path.isfile(os.path.join(projectDir,xtal,'dimple.pdb')):
#            db_dict['PDB_file']=os.path.realpath(os.path.join(projectDir,xtal,'dimple.pdb'))
#            if os.path.isfile(os.path.join(projectDir,xtal,'dimple.mtz')):
#                db_dict['MTZ_file']=os.path.realpath(os.path.join(projectDir,xtal,'dimple.mtz'))
#                Logfile.insert('updating depositTable for apo structure '+xtal)
#                db.update_depositTable(xtal,'apo',db_dict)



class templates:

    def data_template_cif(self,depositDict):

        taxonomy_dict=XChemMain.NCBI_taxonomy_ID()
        for key in taxonomy_dict:
            if taxonomy_dict[key]==depositDict['Source_organism_scientific_name']:
                pdbx_gene_src_ncbi_taxonomy_id=key
            if taxonomy_dict[key]==depositDict['Expression_system_scientific_name']:
                pdbx_host_org_ncbi_taxonomy_id=key

#        structure_author_name=''
#        for name in depositDict['structure_author_name'].split(';'):
#            structure_author_name+='<structure_author_name=  %s>\n' %name

        audit_author_name=''
        # one name must be within quotation, last name and first initial must be separated by comma and space
        for name in depositDict['structure_author_name'].split(';'):
            if name.replace(' ','') == '':
                continue
            if name[name.find(',')+1:name.find(',')+2] != ' ':
                name=name.replace(',',', ')
            audit_author_name+="'{0!s}'\n".format(name)

        primary_citation_author_name=''
        # one name must be within quotation, last name and first initial must be separated by comma and space
        for name in depositDict['primary_citation_author_name'].split(';'):
            if name.replace(' ','') == '':
                continue
            if name[name.find(',')+1:name.find(',')+2] != ' ':
                name=name.replace(',',', ')
            primary_citation_author_name+="primary '{0!s}'\n".format(name)

        molecule_one_letter_sequence=';'
        counter=1
        for aa in depositDict['molecule_one_letter_sequence']:
            if counter < 70:
                molecule_one_letter_sequence+=aa
            if counter == 70:
                molecule_one_letter_sequence+='\n'+aa
                counter = 0
            counter+=1

        data_template_cif = (
            'data_UNNAMED\n'
            '#\n'
            '_pdbx_database_status.entry_id                       UNNAMED\n'
            "_pdbx_database_status.dep_release_code_coordinates   '%s'\n"                       %depositDict['Release_status_for_coordinates']+
            "_pdbx_database_status.dep_release_code_sequence      '{0!s}'\n".format(depositDict['Release_status_for_sequence'])+
            '#\n'
            '_pdbx_deposit_group.group_id	   UNNAMED\n'
            '_pdbx_deposit_group.group_description  "%s"\n'                                     %depositDict['group_description']+
            '_pdbx_deposit_group.group_title        "{0!s}"\n'.format(depositDict['group_title'])+
            '_pdbx_deposit_group.group_type         "{0!s}"\n'.format(depositDict['group_type'])+
            '#\n'
            '_exptl_crystal_grow.crystal_id      1\n'
            "_exptl_crystal_grow.method          '%s'\n"                                        %depositDict['crystallization_method']+
            '_exptl_crystal_grow.pH              {0!s}\n'.format(depositDict['crystallization_pH'])+
            '_exptl_crystal_grow.temp            {0!s}\n'.format(depositDict['crystallization_temperature'])+
            '_exptl_crystal_grow.pdbx_details    "{0!s}"\n'.format(depositDict['crystallization_details'])+
            '#\n'
            '_diffrn.id                     1\n'
            '_diffrn.ambient_temp           %s\n'                                               %depositDict['data_collection_temperature']+
            '_diffrn.crystal_id             1\n'
            '#\n'
            '_diffrn_source.diffrn_id                       1\n'
            '_diffrn_source.source                          %s\n'                               %depositDict['radiation_source']+
            '_diffrn_source.type                            "{0!s}"\n'.format(depositDict['radiation_source_type'])+
            '_diffrn_source.pdbx_wavelength_list            {0!s}\n'.format(depositDict['radiation_wavelengths'])+
            '#\n'
            '_diffrn_detector.detector               %s\n'                                      %depositDict['radiation_detector']+
            "_diffrn_detector.type                   '{0!s}'\n".format(depositDict['radiation_detector_type'])+
            '_diffrn_detector.pdbx_collection_date   {0!s}\n'.format(depositDict['data_collection_date'])+
            '_diffrn_detector.diffrn_id              1\n'
            '#\n'
            '_diffrn_radiation.diffrn_id                        1\n'
            '_diffrn_radiation.wavelength_id                    1\n'
            "_diffrn_radiation.pdbx_diffrn_protocol             'SINGLE WAVELENGTH'\n"
            '#\n'
            '_diffrn_radiation_wavelength.id           1\n'
            '_diffrn_radiation_wavelength.wavelength   %s\n'                                    %depositDict['radiation_wavelengths']+
            '#\n'
            '#\n'
            'loop_\n'
            '_entity.id\n'
            '_entity.type\n'
            '_entity.src_method\n'
            '_entity.pdbx_description\n'
            '_entity.pdbx_mutation\n'
            '1 polymer     man "%s" %s\n'                                                          %(depositDict['Source_organism_gene'],depositDict['fragment_name_one_specific_mutation'])+
            '#\n'
            'loop_\n'
            '_entity_poly.entity_id\n'
            '_entity_poly.type\n'
            '_entity_poly.pdbx_seq_one_letter_code\n'
            '_entity_poly.pdbx_strand_id\n'
            '_entity_poly.pdbx_seq_db_id\n'
            '_entity_poly.pdbx_seq_db_name\n'
            '1 "polypeptide(L)"\n'
            +molecule_one_letter_sequence+'\n'
            ';\n'
            '%s %s UNP\n'                                        %(depositDict['protein_chains'],depositDict['molecule_one_letter_sequence_uniprot_id'])+
            '#\n'
            'loop_\n'
            '_entity_src_gen.entity_id\n'
            '_entity_src_gen.gene_src_strain\n'
            '_entity_src_gen.pdbx_gene_src_scientific_name\n'
            '_entity_src_gen.pdbx_gene_src_ncbi_taxonomy_id\n'
            '_entity_src_gen.pdbx_host_org_scientific_name\n'
            '_entity_src_gen.pdbx_host_org_ncbi_taxonomy_id\n'
            '1 ? "%s" %s  "%s" %s\n'                %(depositDict['Source_organism_scientific_name'],pdbx_gene_src_ncbi_taxonomy_id,depositDict['Expression_system_scientific_name'],pdbx_host_org_ncbi_taxonomy_id)+
            '#\n'
            'loop_\n'
            '_pdbx_contact_author.id                  \n'
            "_pdbx_contact_author.address_1           \n"
            '_pdbx_contact_author.address_2           \n'
            '_pdbx_contact_author.city                \n'
            "_pdbx_contact_author.state_province      \n"
            '_pdbx_contact_author.postal_code         \n'
            '_pdbx_contact_author.email               \n'
            '_pdbx_contact_author.name_first          \n'
            '_pdbx_contact_author.name_last           \n'
            '_pdbx_contact_author.country             \n'
            '_pdbx_contact_author.phone               \n'
            '_pdbx_contact_author.role                \n'
            '_pdbx_contact_author.organization_type   \n'
            "1 '%s' '%s' '%s' '%s' '%s' %s %s '%s' '%s' '%s' '%s' %s\n" %(depositDict['contact_author_PI_address'],depositDict['contact_author_PI_organization_name'],depositDict['contact_author_PI_city'],depositDict['contact_author_PI_State_or_Province'],depositDict['contact_author_PI_Zip_Code'],depositDict['contact_author_PI_email'],depositDict['contact_author_PI_first_name'],depositDict['contact_author_PI_last_name'],depositDict['contact_author_PI_Country'],depositDict['contact_author_PI_phone_number'],depositDict['contact_author_PI_role'],depositDict['contact_author_PI_organization_type'])+
            "2 '{0!s}' '{1!s}' '{2!s}' '{3!s}' '{4!s}' {5!s} {6!s} '{7!s}' '{8!s}' '{9!s}' '{10!s}' {11!s}\n".format(depositDict['contact_author_address'], depositDict['contact_author_organization_name'], depositDict['contact_author_city'], depositDict['contact_author_State_or_Province'], depositDict['contact_author_Zip_Code'].replace(' ',''), depositDict['contact_author_email'], depositDict['contact_author_first_name'], depositDict['contact_author_last_name'], depositDict['contact_author_Country'], depositDict['contact_author_phone_number'], depositDict['contact_author_role'], depositDict['contact_author_organization_type'])+
            '#\n'
            'loop_\n'
            '_audit_author.name\n'
            +audit_author_name+
#            "'%s, %s.'\n" %(depositDict['contact_author_last_name'],depositDict['contact_author_first_name'][0])+
            '#\n'
            '_citation.id                        primary\n'
            "_citation.title                     '%s'\n"   %depositDict['group_title']+
            "_citation.journal_abbrev            'To Be Published'\n"
            '#\n'
            'loop_\n'
            '_citation_author.citation_id\n'
            '_citation_author.name\n'
            +primary_citation_author_name+
#        "primary 'Krojer, T.'\n"
#        "primary 'Von Delft, F.'\n"
            '#\n'
            '_struct.entry_id                     UNNAMED\n'
            '_struct.title\n'
            ';%s\n'                                                         %depositDict['title']+
            ';\n'
            '#\n'
            '_struct_keywords.entry_id        UNNAMED\n'
            '_struct_keywords.text            "%s"\n'                       %depositDict['structure_keywords']+
            '#\n'
            '_pdbx_struct_assembly_depositor_info.id                   1\n'
            "_pdbx_struct_assembly_depositor_info.method_details       PISA\n"
            '_pdbx_struct_assembly_depositor_info.oligomeric_count     %s\n'        %depositDict['biological_assembly_chain_number']+
            '#\n'
            '#\n'
            )

        return data_template_cif



class update_depositTable(QtCore.QThread):
    def __init__(self,deposit_dict,database,xce_logfile):
        QtCore.QThread.__init__(self)
        self.deposit_dict=deposit_dict
        self.database=database
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.db=XChemDB.data_source(database)

    def run(self):
        self.Logfile.insert('all entries in the depositTable will be updated with the following values:')
        for key in self.deposit_dict:
            self.Logfile.insert(key+': '+self.deposit_dict[key])
        dbEntries=self.db.execute_statement("select CrystalName,StructureType from depositTable;")
        for item in dbEntries:
            xtal=str(item[0])
            type=str(item[1])
            db_dict=self.deposit_dict   # need to do this because individual fields might need updating for some xtals

            # try to get information about the diffraction experiment
            try:
                diffractionExperiment=self.db.execute_statement("select DataCollectionBeamline,DataCollectionDate from mainTable where CrystalName is '{0!s}'".format(xtal))
                beamline=str(diffractionExperiment[0][0])
                date=str(diffractionExperiment[0][1])
            except (UnboundLocalError,IndexError):
                self.Logfile.warning('%s: cannot find details about diffraction experiment in mainTable' %xtal)
                beamline = db_dict['radiation_source']
                date = db_dict['data_collection_date']
                self.Logfile.warning('%s: using values provided in depositTable for beamline and data collection date' %xtal)
            if beamline.lower() != 'none':
                db_dict=self.tweak_deposit_dict(xtal,db_dict)
            if date.lower() != 'none':
                db_dict['data_collection_date']=date.split()[0]

            self.Logfile.insert('updating depositTable for '+xtal+' @ '+type)
            self.db.update_depositTable(xtal,type,db_dict)
        self.Logfile.insert('Note: use DBbrowser to edit individual entries')

    def tweak_deposit_dict(self,xtal,db_dict):
        dls_beamlines=['i02','i03','i04','i04-1','i23','i24']
        dls_beamline_dict = {   'i02':      ['DIAMOND BEAMLINE I02',    'DECTRIS PILATUS 6M'],
                                'i03':      ['DIAMOND BEAMLINE I03',    'DECTRIS PILATUS 6M'],
                                'i04':      ['DIAMOND BEAMLINE I04',    'DECTRIS PILATUS 6M'],
                                'i04-1':    ['DIAMOND BEAMLINE I04-1',  'DECTRIS PILATUS 6M'],
                                'i23':      ['DIAMOND BEAMLINE I23',    'DECTRIS PILATUS 12M'],
                                'i24':      ['DIAMOND BEAMLINE I24',    'DECTRIS PILATUS 6M'] ,     }

        if db_dict['radiation_source_type'] in dls_beamlines:
            db_dict['radiation_source_type']=    dls_beamline_dict[db_dict['radiation_source_type']][0]
            db_dict['radiation_detector_type']=  dls_beamline_dict[db_dict['radiation_source_type']][1]
            db_dict['radiation_detector']=       'PIXEL'
            db_dict['radiation_source']=         'SYNCHROTRON'

        return db_dict




class prepare_mmcif_files_for_deposition(QtCore.QThread):

    def __init__(self,database,xce_logfile,overwrite_existing_mmcif,projectDir,ground_state):
        QtCore.QThread.__init__(self)
        self.database=database
        self.xce_logfile=xce_logfile
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.db=XChemDB.data_source(database)
        self.overwrite_existing_mmcif=overwrite_existing_mmcif
        self.projectDir=projectDir
        self.data_template_dict={}

        self.errorList = []
        self.eventList = []
        self.db_dict = None
        self.data_template_dict = None
        self.zenodo_dict = None
        self.pdb = None
        self.mtz = None

        self.ground_state = False
        self.ground_state_pdb = ''
        self.ground_state_mean_mtz = ''
        self.panddaDir = ''
        if ground_state != []:
            self.ground_state = True
            self.ground_state_pdb = ground_state[0]
            self.ground_state_mean_mtz = ground_state[1]
            self.panddaDir = ground_state[2]
            self.projectDir = self.panddaDir
            self.pdb = pdbtools(self.ground_state_pdb)
            self.mtz = mtztools(self.ground_state_mean_mtz)

    def run(self):

        self.Logfile.insert('======= preparing mmcif files for wwPDB deposition =======')
        self.Logfile.insert('checking DB for structures to deposit...')
        if self.ground_state:
            toDeposit = self.db.execute_statement("select CrystalName from depositTable where DimplePANDDApath = '%s';" %self.panddaDir)
        else:
            toDeposit = self.db.execute_statement("select CrystalName from mainTable where RefinementOutcome like '5%';")
        self.Logfile.insert('found ' + str(len(toDeposit)) + ' samples ready for deposition')

        progress_step=1
        if len(toDeposit) != 0:
            progress_step=100/float(len(toDeposit))
        else:
            progress_step=1
        progress=0
        self.emit(QtCore.SIGNAL('update_progress_bar'), progress)

        for item in sorted(toDeposit):
            xtal=str(item[0])
            if self.ground_state:
                os.chdir(self.projectDir)       # projectDir == referenceDir in this case
            else:
                os.chdir(os.path.join(self.projectDir, xtal))
            self.Logfile.insert('%s: ----- preparing files for deposition -----' %xtal)

            if self.ground_state:
                if not self.data_template_dict_exists(xtal):
                    continue

                if not self.zenodo_dict_exists(xtal):
                    continue

                if not self.save_data_template_dict(xtal):
                    continue

                if not self.create_model_mmcif(xtal):
                    continue

                if not self.create_sf_mmcif(xtal):
                    continue

                if not self.apo_mmcif_exists():
                    continue

                if not self.add_apo_sf_mmcif_to_ground_state_mmcif():
                    continue




            else:
                if not self.mmcif_files_can_be_replaced(xtal):
                    continue

                if not self.data_template_dict_exists(xtal):
                    continue

                if not self.db_dict_exists(xtal):
                    continue

                if not self.zenodo_dict_exists(xtal):
                    continue

                if not self.refine_bound_exists(xtal):
                    continue

                if not self.refine_mtz_exists(xtal):
                    continue

                if not self.aimless_logfile_exists(xtal):
                    continue

                if not self.ligand_in_pdb_file(xtal):
                    continue

                if not self.eventMTZ_exists((xtal)):
                    continue

                if not self.find_matching_event_map(xtal):
                    continue

                if not self.save_data_template_dict(xtal):
                    continue

                if not self.create_model_mmcif(xtal):
                    continue

                if not self.create_sf_mmcif(xtal):
                    continue

                if not self.event_maps_exist_in_sf_mmcif(xtal):
                    continue


        self.print_errorlist()
        self.Logfile.insert('======= finished preparing mmcif files for wwPDB deposition =======')

    def ground_state_mmcif_exists(self):
        mmcifStatus = False
        for dirs in glob.glob(os.path.join(self.panddaDir, 'processed_datasets', '*')):
            xtal = dirs[dirs.rfind('/') + 1:]
            if os.path.isfile(os.path.join(dirs, xtal + '_sf.mmcif')):
                self.Logfile.insert('%s: found mmcif file for apo structure' %xtal)
                mmcifStatus = True

        return mmcifStatus

    def data_template_dict_exists(self,xtal):
        dictStatus = False
        self.data_template_dict = None
        self.Logfile.insert('%s: reading information from depositTable for sample' % xtal)
        self.data_template_dict = self.db.get_deposit_dict_for_sample(xtal)
        if self.data_template_dict == {}:
            self.Logfile.error('%s: cannot find data_template dictionary in depositTable; moving to next dataset...' %xtal)
            self.add_to_errorList(xtal)
        else:
            self.Logfile.insert('%s: found data_template dictionary in depositTable' % xtal)
            dictStatus = True
        return  dictStatus

    def db_dict_exists(self,xtal):
        dictStatus = False
        self.db_dict = None
        self.Logfile.insert('%s: reading information from mainTable for sample' % xtal)
        self.db_dict = self.db.get_db_dict_for_sample(xtal)
        if self.db_dict == {}:
            self.Logfile.error('%s: cannot find db_dict dictionary in mainTable; moving to next dataset...' %xtal)
            self.add_to_errorList(xtal)
        else:
            self.Logfile.insert('%s: found db_dict dictionary in mainTable' % xtal)
            dictStatus = True
        return  dictStatus

    def zenodo_dict_exists(self,xtal):
        dictStatus = False
        self.zenodo_dict = None
        if self.ground_state:
            self.zenodo_dict = self.db.get_zenodo_dict_for_pandda_analysis(self.panddaDir)
        else:
            self.Logfile.insert('%s: reading information from zenodoTable for pandda run: %s' % (xtal, self.db_dict['DimplePANDDApath']))
            self.zenodo_dict = self.db.get_zenodo_dict_for_pandda_analysis(self.db_dict['DimplePANDDApath'])
        if self.zenodo_dict == {}:
            dictStatus = True
            self.zenodo_dict['ZenodoDOI'] = ''
            self.Logfile.warning('%s: cannot find information about zenodo deposition in zenodoTable!!!' %xtal)
#            self.Logfile.error('%s: cannot find information about zenodo deposition in zenodoTable; moving to next dataset...' %xtal)
#            self.add_to_errorList(xtal)
        else:
            self.Logfile.insert('%s: found zenodo_dict dictionary in zenodoTable' % xtal)
            dictStatus = True
        return  dictStatus


    def mmcif_files_can_be_replaced(self,xtal):
        status = True
        if self.overwrite_existing_mmcif:
            self.Logfile.insert('%s: removing existing mmcif files as chosen by user' %xtal)
            self.db.execute_statement("update depositTable set mmCIF_model_file='',mmCIF_SF_file='' where CrystalName is '{0!s}'".format(xtal))
            for mmcif in glob.glob('*.mmcif'):
                self.Logfile.warning('%s: removing %s' %(xtal,mmcif))
                os.system('/bin/rm ' + mmcif)
        else:
            for mmcif in glob.glob('*.mmcif'):
                self.Logfile.warning('%s: %s exists; skipping...' %(xtal,mmcif))
                status = False
        return status



    def refine_bound_exists(self,xtal):
        self.pdb = None
        self.Logfile.insert('%s: checking if refine.split.bound-state.pdb exists' %xtal)
        fileStatus = False
        if os.path.isfile('refine.split.bound-state.pdb'):
            self.Logfile.insert('%s: found refine.split.bound-state.pdb' %xtal)
            self.pdb = pdbtools('refine.split.bound-state.pdb')
            fileStatus = True
        else:
            self.Logfile.error('%s: cannot find refine.split.bound-state.pdb; moving to next dataset...' %xtal)
            self.add_to_errorList(xtal)
        return  fileStatus

    def refine_mtz_exists(self,xtal):
        self.mtz = None
        self.Logfile.insert('%s: checking if refine.mtz exists' %xtal)
        fileStatus = False
        if os.path.isfile('refine.mtz'):
            self.Logfile.insert('%s: found refine.mtz' %xtal)
            self.mtz = mtztools('refine.mtz')
            fileStatus = True
        else:
            self.Logfile.error('%s: cannot find refine.mtz; moving to next dataset...' %xtal)
            self.add_to_errorList(xtal)
        return  fileStatus

    def aimless_logfile_exists(self,xtal):
        self.Logfile.insert('%s: checking if aimless logfile, i.e. %s.log, exists' %(xtal,xtal))
        fileStatus = False
        if os.path.isfile('%s.log' %xtal):
            self.Logfile.insert('%s: found %s.log' %(xtal,xtal))
            fileStatus = True
        else:
            self.Logfile.error('%s: cannot find %s.log; moving to next dataset...' %(xtal,xtal))
            self.add_to_errorList(xtal)
        return  fileStatus


    def mtzFree_exisits(self,xtal):
        self.Logfile.insert('%s: checking if %s.free.mtz exists' %(xtal,xtal))
        fileStatus = False
        if os.path.isfile('%s.free.mtz' %xtal):
            self.Logfile.insert('%s: found %s.free.mtz' %(xtal,xtal))
            fileStatus = True
        else:
            self.Logfile.error('%s: cannot find %s.free.mtz; moving to next dataset...' %(xtal,xtal))
            self.add_to_errorList(xtal)
        return  fileStatus


    def ligand_in_pdb_file(self,xtal):
        self.Logfile.insert('%s: checking if refine.split.bound-state.pdb contains ligands of type LIG' %xtal)
        ligandStatus = False
        ligList = pdbtools('refine.split.bound-state.pdb').get_residues_with_resname('LIG')
        if ligList is []:
            self.Logfile.error('%s: refine.split.bound-state.pdb does not contain any modelled ligands of type LIG' %xtal)
            self.add_to_errorList(xtal)
        else:
            self.Logfile.insert(xtal + ': found ' + str(len(ligList)) + ' ligands of type LIG')
            ligandStatus = True
        return ligandStatus

    def eventMTZ_exists(self,xtal):
        self.Logfile.insert('%s: checking if mtz of event maps exists' %xtal)
        eventMTZlist = []
        eventMTZexists = False
        if os.path.isfile('no_pandda_analysis_performed'):
            self.Logfile.warning('%s: found empty file named "no_pandda_analysis_performed" which suggests we will ignore event maps for this sample' %xtal)
            eventMTZexists = True
        else:
            for mtz in glob.glob('*event*.native*P1.mtz'):
                eventMTZlist.append(mtz[mtz.rfind('/')+1:])
            if eventMTZlist is []:
                self.Logfile.error('%s: MTZ files of event maps do not exists! Go to PANDDA tab and run "Event Map -> SF"' %xtal)
                self.add_to_errorList(xtal)
            else:
                self.Logfile.insert(xtal + ': found ' + str(len(eventMTZlist)) + ' MTZ files of event maps')
                eventMTZexists = True
        return eventMTZexists


    def find_matching_event_map(self,xtal):
        self.eventList = []
        self.Logfile.insert('%s: trying to find fitting event maps for modelled ligands' %xtal)
        ligList = self.pdb.save_residues_with_resname(os.path.join(self.projectDir,xtal), 'LIG')
        foundMatchingMap = None
        if os.path.isfile('no_pandda_analysis_performed'):
            self.Logfile.warning('%s: found empty file named "no_pandda_analysis_performed" which suggests we will ignore event maps for this sample' %xtal)
            foundMatchingMap = True
            ligList = []
        for lig in sorted(ligList):
            ligID = lig.replace('.pdb','')
#            if os.path.isfile('no_pandda_analysis_performed'):
#                self.Logfile.warning('%s: no pandda analysis performed; skipping this step...' %xtal)
#                foundMatchingMap = True
#                break
            ligCC = []
            for mtz in sorted(glob.glob('*event*.native*P1.mtz')):
                self.get_lig_cc(xtal, mtz, lig)
                cc = self.check_lig_cc(mtz.replace('.mtz', '_CC'+ligID+'.log'))
                self.Logfile.insert('%s: %s -> CC = %s for %s' %(xtal,ligID,cc,mtz))
                try:
                    ligCC.append([mtz,float(cc)])
                except ValueError:
                    ligCC.append([mtz, 0.00])
            highestCC = max(ligCC, key=lambda x: x[0])[1]
            if highestCC == 0.00 or ligCC is []:
                self.Logfile.error('%s: best CC of ligand %s for any event map is 0!' %(xtal,lig))
                self.add_to_errorList(xtal)
                foundMatchingMap = False
            else:
                self.Logfile.insert('%s: selected event map -> CC(%s) = %s for %s' %(xtal,lig,highestCC,mtz[mtz.rfind('/')+1:]))
                if mtz not in self.eventList:
                    self.eventList.append(mtz)
                if foundMatchingMap is None:
                    foundMatchingMap = True
        return foundMatchingMap


    def get_lig_cc(self, xtal, mtz, lig):
        ligID = lig.replace('.pdb','')
        self.Logfile.insert('%s: calculating CC for %s in %s' %(xtal,lig,mtz))
        if os.path.isfile(mtz.replace('.mtz', '_CC'+ligID+'.log')):
            self.Logfile.warning('logfile of CC analysis exists; skipping...')
            return
        cmd = ( 'module load phenix\n'
                'phenix.get_cc_mtz_pdb %s %s > %s' % (mtz, lig, mtz.replace('.mtz', '_CC'+ligID+'.log')) )
        os.system(cmd)

    def check_lig_cc(self,log):
        cc = 'n/a'
        if os.path.isfile(log):
            for line in open(log):
                if line.startswith('local'):
                    cc = line.split()[len(line.split()) - 1]
        else:
            self.Logfile.error('logfile does not exist: %s' %log)
        return cc


    def add_to_errorList(self,xtal):
        if xtal not in self.errorList:
            self.errorList.append(xtal)

    def print_errorlist(self):
        if self.errorList == []:
            self.Logfile.insert('XCE did not detect any problems during mmcif file preparation. '
                                'It is however recommended to check the logfile.')
        else:
            self.Logfile.warning('The following samples had problems during mmcif creation. '
                                 'Please check the logfile for details!')
            for xtal in self.errorList:
                self.Logfile.error(xtal)


    def save_data_template_dict(self,xtal):
        # check if file exists
        noError = True
        self.Logfile.insert('%s: preparing data_template.cif file' %xtal)
        if self.overwrite_existing_mmcif:

            if self.ground_state:
                os.chdir(self.projectDir)
                self.data_template_dict['radiation_wavelengths'] = '1.000'
                self.data_template_dict['group_type'] = 'ground state'
                self.data_template_dict['group_title'] = 'PanDDA analysis group deposition of ground-state model'
                self.data_template_dict['group_description'] = self.data_template_dict['group_description'].replace('$ProteinName',
                                                                                                                    self.data_template_dict[
                                                                                                              'Source_organism_gene'])
                self.data_template_dict['title'] = self.data_template_dict['structure_title_apo'].replace('$ProteinName',
                                                                                                               self.data_template_dict[
                                                                                                         'Source_organism_gene'])
            else:
                os.chdir(os.path.join(self.projectDir, xtal))
                # edit wavelength
                self.data_template_dict['radiation_wavelengths'] = self.mtz.get_wavelength()

                title = self.data_template_dict['structure_title'].replace('$ProteinName', self.data_template_dict[
                    'Source_organism_gene']).replace('$CompoundName', self.db_dict['CompoundCode'])

                self.data_template_dict['group_type'] = 'changed state'


                # edit title
                self.data_template_dict['group_title'] = self.data_template_dict['group_deposition_title'].replace('$ProteinName',
                                                                                                               self.data_template_dict[
                                                                                                         'Source_organism_gene']).replace(
                                '$CompoundName', self.db_dict['CompoundCode'])

#            self.data_template_dict[
#                    'group_title'] = 'PanDDA analysis group deposition of models with modelled events (e.g. bound ligands)'
                self.data_template_dict['group_description'] = self.data_template_dict['group_description'].replace('$ProteinName',
                                                                                                                    self.data_template_dict[
                                                                                                              'Source_organism_gene'])
                self.data_template_dict['title'] = self.data_template_dict['group_title'] + ' -- ' + title

                if ('$ProteinName' or '$CompoundName') in self.data_template_dict['title']:
                    self.Logfile.error('%s: data_template - title not correctly formatted')
                    self.add_to_errorList(xtal)
                    noError = False

            # mutations
            mutations = self.data_template_dict['fragment_name_one_specific_mutation']
            if mutations.lower().replace(' ', '').replace('none', '').replace('null', '') == '':
                self.data_template_dict['fragment_name_one_specific_mutation'] = '?'
            else:
                self.data_template_dict['fragment_name_one_specific_mutation'] = '"' + mutations.replace(' ', '') + '"'

            # get protein chains
            self.data_template_dict['protein_chains'] = ''
            chains = self.pdb.GetProteinChains()
            for item in chains:
                self.data_template_dict['protein_chains'] += item + ','
            self.data_template_dict['protein_chains'] = self.data_template_dict['protein_chains'][:-1]

            data_template = templates().data_template_cif(self.data_template_dict)
#            site_details = self.make_site_description(xtal)
#            data_template += site_details
            if self.ground_state:
                f = open(os.path.join(self.projectDir, 'data_template.cif'), 'w')
            else:
                f = open(os.path.join(self.projectDir, xtal, 'data_template.cif'), 'w')

            f.write(data_template)
            f.close()

        return noError


    def create_model_mmcif(self,xtal):
        fileStatus = False
        if self.ground_state:
            os.chdir(os.path.join(self.projectDir))
        else:
            os.chdir(os.path.join(self.projectDir, xtal))
        refSoft = self.pdb.get_refinement_program()

        if os.path.isdir('/dls'):
            pdb_extract_init = 'source /dls/science/groups/i04-1/software/pdb-extract-prod/setup.sh\n'
            pdb_extract_init += '/dls/science/groups/i04-1/software/pdb-extract-prod/bin/pdb_extract'
        else:
            pdb_extract_init = 'source ' + os.path.join(os.getenv('XChemExplorer_DIR'),
                                                        'pdb_extract/pdb-extract-prod/setup.sh') + '\n'
            pdb_extract_init += +os.path.join(os.getenv('XChemExplorer_DIR'),
                                                  'pdb_extract/pdb-extract-prod/bin/pdb_extract')

        if self.ground_state:
            Cmd = (pdb_extract_init +
                   ' -r {0!s}'.format(refSoft) +
                   ' -iPDB {0!s}'.format(self.ground_state_pdb) +
                   ' -e MR'
                   ' -iENT data_template.cif'
                   ' -o {0!s}.mmcif > {1!s}.mmcif.log'.format(xtal, xtal))
        else:
            Cmd = (pdb_extract_init +
                   ' -r {0!s}'.format(refSoft) +
                   ' -iPDB {0!s}'.format('refine.split.bound-state.pdb') +
                   ' -e MR'
                   ' -s AIMLESS'
                   ' -iLOG {0!s}.log'.format(xtal) +
                   ' -iENT data_template.cif'
                   ' -o {0!s}.mmcif > {1!s}.mmcif.log'.format(xtal, xtal))

        self.Logfile.insert(xtal + ': running pdb_extract: ' + Cmd)
        os.system(Cmd)

        self.update_model_mmcif_header(xtal)

        if os.path.isfile(xtal+'.mmcif') and os.path.getsize(xtal+'.mmcif') > 20000 :
            self.Logfile.insert('%s: model mmcif file successfully created' %xtal)
            if self.ground_state:
                self.db.execute_statement(
                    "update depositTable set mmCIF_model_file='{0!s}.mmcif' where CrystalName is '{1!s}' and DimplePANDDApath is '{2!s}'".format(xtal,
                                                                                                                 xtal,self.panddaDir))
            else:
                self.db.execute_statement("update depositTable set mmCIF_model_file='{0!s}.mmcif' where CrystalName is '{1!s}'".format(xtal,xtal))
            fileStatus = True
        else:
            self.Logfile.error('%s: model mmcif file was not created successfully')
            self.add_to_errorList(xtal)

        return fileStatus

    def update_model_mmcif_header(self,xtal):
        self.Logfile.insert('%s: updating header of model mmcif file' %xtal)
        foundSoftwareBlock = False
        amendSoftwareBlock = False
        softwareEntry = []
        for i, line in enumerate(fileinput.input(xtal + '.mmcif', inplace=1)):
            #            if i == 4: sys.stdout.write('\n')  # write a blank line after the 5th line
            if '_software.pdbx_ordinal' in line:
                foundSoftwareBlock = True
            if foundSoftwareBlock:
                if not line.startswith('_'):
                    try:
                        softwareEntry.append(int(line.split()[0]))
                    except (ValueError,IndexError):
                        pass
                if '#' in line:
                    amendSoftwareBlock = True
                    foundSoftwareBlock = False
            if '_refine.pdbx_ls_cross_valid_method' in line:
                sys.stdout.write('_refine.pdbx_ls_cross_valid_method               THROUGHOUT \n')

            elif '_refine.pdbx_starting_model' in line:
                sys.stdout.write('_refine.pdbx_starting_model                      {0!s} \n'.format(
                    self.data_template_dict['pdbx_starting_model']))

            elif '_refine.pdbx_method_to_determine_struct' in line:
                sys.stdout.write("_refine.pdbx_method_to_determine_struct          'FOURIER SYNTHESIS'\n")
            elif amendSoftwareBlock:
                cifItem = (
                    "{0!s} {1!s} ? ? program ? ? 'data reduction' ? ?\n".format(str(max(softwareEntry) + 1),
                                                                                        self.data_template_dict[
                                                                                            'data_integration_software']) +
                    '{0!s} {1!s} ? ? program ? ? phasing ? ?\n'.format(str(max(softwareEntry) + 2),
                                                                               self.data_template_dict[
                                                                                   'phasing_software']) +
                    '#\n'
                    "loop_\n"
                    "_pdbx_related_exp_data_set.ordinal\n"
                    "_pdbx_related_exp_data_set.data_reference\n"
                    "_pdbx_related_exp_data_set.metadata_reference\n"
                    "_pdbx_related_exp_data_set.data_set_type\n"
                    "_pdbx_related_exp_data_set.details\n"
                    " 1  "
                    " 'doi:%s' "  %self.zenodo_dict['ZenodoDOI']+
                    " 'doi:%s' "  %self.zenodo_dict['ZenodoDOI']+
                    " 'other data'  "                 # 'other data' is only thing wwPDB accepts at the moment
                    " 'Complete PanDDA analysis'\n"
                    "\n" )

                sys.stdout.write(cifItem)
                amendSoftwareBlock = False

            else:
                sys.stdout.write(line)




#            elif '_reflns.d_resolution_low' in line and len(line.split()) == 2:
#                sys.stdout.write('_reflns.d_resolution_low             {0!s}\n'.format(min(low_reso_list)))
#
#            elif '_refine.ls_d_res_low' in line and len(line.split()) == 2:
#                sys.stdout.write('_refine.ls_d_res_low                             {0!s}\n'.format(min(low_reso_list)))


    def create_sf_mmcif(self,xtal):
        fileStatus = False
        if self.ground_state:
            os.chdir(self.projectDir)
        else:
            os.chdir(os.path.join(self.projectDir, xtal))

        if os.path.isfile('no_pandda_analysis_performed'):
            mtzin = 'refine.mtz '
        else:
            mtzin = 'refine.mtz ' + xtal + '.free.mtz '
            for event in self.eventList:
                mtzin += event + ' '

        if self.ground_state:
            mtzin = self.ground_state_mean_mtz

        if os.path.isdir('/dls'):
            pdb_extract_init = 'source /dls/science/groups/i04-1/software/pdb-extract-prod/setup.sh\n'
            pdb_extract_init += '/dls/science/groups/i04-1/software/pdb-extract-prod/bin/sf_convert'
        else:
            pdb_extract_init = 'source ' + os.path.join(os.getenv('XChemExplorer_DIR'),
                                                            'pdb_extract/pdb-extract-prod/setup.sh') + '\n'
            pdb_extract_init += +os.path.join(os.getenv('XChemExplorer_DIR'),
                                                  'pdb_extract/pdb-extract-prod/bin/sf_convert')

        Cmd = (pdb_extract_init +
                   ' -o mmcif'
                   ' -sf %s' % mtzin +
                   ' -out {0!s}_sf.mmcif  > {1!s}.sf_mmcif.log'.format(xtal, xtal))

        self.Logfile.insert(xtal + ': running sf_convert: ' + Cmd)
        os.system(Cmd)
        os.system('/bin/rm sf_format_guess.text mtzdmp.log SF_4_validate.cif sf_information.cif')

        self.update_sf_mmcif_file(xtal)

        if os.path.isfile(xtal+'_sf.mmcif') and os.path.getsize(xtal+'_sf.mmcif') > 20000 :
            self.Logfile.insert('%s: SF mmcif file successfully created' %xtal)
            if self.ground_state:
                self.db.execute_statement("update depositTable set mmCIF_SF_file='{0!s}_sf.mmcif' where CrystalName is '{1!s}' and DimplePANDDApath is '{2!s}'".format(xtal,xtal,self.panddaDir))
            else:
                self.db.execute_statement("update depositTable set mmCIF_SF_file='{0!s}_sf.mmcif' where CrystalName is '{1!s}'".format(xtal,xtal))
            fileStatus = True
        else:
            self.Logfile.error('%s: SF mmcif file was not created successfully')
            self.add_to_errorList(xtal)

        return fileStatus

    def apo_mmcif_exists(self):
        fileStatus = False
        self.Logfile.insert('checking if mmcif files of apo structures exist')
        counter = 0
        for mmcif in glob.glob(os.path.join(self.panddaDir,'processed_datasets','*','*.mmcif')):
            if os.path.isfile(mmcif):
                counter += 1
        if counter < 40:
            self.Logfile.error('found only %s apo mmcif files' %str(counter))
            self.Logfile.warning('you may need to run "PanDDA tab"/"apo -> mmcif"')
        else:
            self.Logfile.insert('found %s apo mmcif files; seems OK!' %str(counter))
            fileStatus = True
        return fileStatus

    def add_apo_sf_mmcif_to_ground_state_mmcif(self):
        os.chdir(self.projectDir)
        self.Logfile.insert('checking pandda directory for apo mmcif files: '+self.panddaDir)
        f = open('ground-state_sf.mmcif','a')
        counter = 1
        for dirs in glob.glob(os.path.join(self.panddaDir,'processed_datasets','*')):
            if not os.path.isdir(dirs):         # this is needed in case single files are in processed_datasets
                continue
            xtal = dirs[dirs.rfind('/')+1:]
            self.Logfile.insert('%s: reading saoked compound information from database' %xtal)
            xtalDict = self.db.get_db_dict_for_sample(xtal)
            if xtalDict['CompoundSMILES'].lower().replace(' ','') == '':
                smiles = 'none'
            elif 'none' in xtalDict['CompoundSMILES'].lower().replace(' ',''):
                smiles = 'none'
            elif 'null' in xtalDict['CompoundSMILES'].lower().replace(' ',''):
                smiles = 'none'
            else:
                smiles = xtalDict['CompoundSMILES'].replace(' ','')
            self.Logfile.insert('%s: compound SMILES -> %s' %(xtal,smiles))
            if os.path.isfile(os.path.join(dirs,xtal+'_sf.mmcif')):
                self.Logfile.insert('adding %s_sf.mmcif to ground-state_sf.mmcif' %xtal)
                for line in open(os.path.join(dirs,xtal+'_sf.mmcif')):
                    if line.startswith('_cell.angle_gamma'):
                        newLine = line
                        newLine += '#\n'
                        newLine += '_diffrn.id                  1\n'
                        newLine += '_diffrn.details             "diffraction data from crystal %s; soaked compound: %s"\n' %(str(counter),smiles)
                        f.write(newLine)
                        counter += 1
                    else:
                        f.write(line)
        f.close()


    def event_maps_exist_in_sf_mmcif(self,xtal):
        fileOK = False
        n_eventMTZ_found = -2  # set to -2 since first two data blocks are initial/final.mtz and data.mtz
        if os.path.isfile('no_pandda_analysis_performed'):
            self.Logfile.warning('%s: no pandda analysis performed; skipping this step...' %xtal)
            fileOK = True
        else:
            for line in open(xtal + '_sf.mmcif'):
                if line.startswith('_refln.crystal_id'):
                    n_eventMTZ_found += 1
            if n_eventMTZ_found == len(self.eventList):
                fileOK = True
                self.Logfile.insert('%s: %s_sf.mmcif should contains %s of %s event maps' %(xtal,xtal,n_eventMTZ_found,len(self.eventList)))
            else:
                self.Logfile.error('%s: %s_sf.mmcif should contains only %s of %s event maps' % (
                xtal, xtal, n_eventMTZ_found, len(self.eventList)))
                self.add_to_errorList(xtal)
        return fileOK


    def update_sf_mmcif_file(self,xtal):
        self.Logfile.insert('%s: updating %s_sf.mmcif' %(xtal,xtal))

        if self.ground_state:
            bound = [   "data for PanDDA ground-state-mean-map"  ]
        else:
            bound = [   "data from final refinement with ligand, final.mtz",
                        "data from original reflections, data.mtz",
                        "data for ligand evidence map (PanDDA event map), event_map_$.mtz"  ]

        block = -1

        self.Logfile.insert('%s: reading wavelength from mtz file; lambda = %s' %(xtal,self.mtz.get_wavelength()))

        if os.path.isfile('no_pandda_analysis_performed'):
            self.Logfile.warning('%s: apparently not a pandda deposition; will skip this step...' %xtal)
            return None

        for i, line in enumerate(fileinput.input(xtal + '_sf.mmcif', inplace=1)):

            if line.startswith('_cell.length_a'):
                block += 1

            if line.startswith('_cell.angle_gamma'):
                if block >= 2:
                    n = 2
                else:
                    n = block
                sys.stdout.write(line)
                newLines = ('#\n'
                            '_diffrn.id                  1\n'
                            '_diffrn.details             "%s"\n' % bound[n]).replace('$',str(block-1))
                sys.stdout.write(newLines)
            elif line.startswith('_diffrn_radiation_wavelength.wavelength'):
                sys.stdout.write('_diffrn_radiation_wavelength.wavelength   {0!s}\n'.format(self.mtz.get_wavelength()))
            else:
                sys.stdout.write(line)





class prepare_for_group_deposition_upload(QtCore.QThread):

    def __init__(self,database,xce_logfile,depositDir,projectDir,type):
        QtCore.QThread.__init__(self)
        self.database=database
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.db=XChemDB.data_source(database)
        self.depositDir=depositDir
        self.projectDir=projectDir
        self.type=type



    def run(self):

        TextIndex=''
        os.chdir(self.depositDir)

        # ligand bound structures
        if self.type == 'ligand_bound':
            self.Logfile.insert('checking depositionTable for mmcif files of ligand-bound structures')
            toDeposit=self.db.execute_statement("select CrystalName,mmCIF_model_file,mmCIF_SF_file from depositTable where StructureType is 'ligand_bound';")
        elif self.type == 'ground_state':
            self.Logfile.insert('checking depositionTable for mmcif files of ground-state structures')
            toDeposit = self.db.execute_statement("select CrystalName,mmCIF_model_file,mmCIF_SF_file from depositTable where StructureType is 'ground_state';")
        else:
            return

        for n,item in enumerate(sorted(toDeposit)):
            xtal=str(item[0])
            mmcif=os.path.join(self.projectDir,xtal,str(item[1]))
            mmcif_sf=os.path.join(self.projectDir,xtal,str(item[2]))
            self.Logfile.insert('%s: %s/ %s' %(xtal,mmcif,mmcif_sf))
            if os.path.isfile(mmcif) and os.path.isfile(mmcif_sf):
                self.Logfile.insert('copying {0!s} to {1!s}'.format(mmcif, self.depositDir))
                os.system('/bin/cp {0!s} .'.format(mmcif))
                if self.type == 'ground_state':
                    os.system('/bin/mv ground_state.mmcif ground_state_{0!s}.mmcif'.format(str(n)))
                    mmcif = mmcif.replace('ground_state.mmcif','ground_state_{0!s}.mmcif'.format(str(n)))
                self.Logfile.insert('copying {0!s} to {1!s}'.format(mmcif_sf, self.depositDir))
                os.system('/bin/cp {0!s} .'.format(mmcif_sf))
                if self.type == 'ground_state':
                    os.system('/bin/mv ground_state_sf.mmcif ground_state_{0!s}_sf.mmcif'.format(str(n)))
                    mmcif_sf = mmcif_sf.replace('ground_state_sf.mmcif', 'ground_state_{0!s}_sf.mmcif'.format(str(n)))
            else:
                self.Logfile.error('cannot find ligand_bound mmcif file for '+xtal)

            text = (    'label: {0!s}-{1!s}\n'.format(xtal,self.type)+
                        'description: {0!s} structure of {1!s}\n'.format(self.type,xtal)+
                        'model: {0!s}\n'.format(mmcif[mmcif.rfind('/')+1:])+
                        'sf: {0!s}\n\n'.format(mmcif_sf[mmcif_sf.rfind('/')+1:])          )
            TextIndex+=text

        f = open('index.txt','w')
        f.write(TextIndex)
        f.close()

        self.Logfile.insert('preparing tar archive...')
        os.system('tar -cvf ligand_bound_structures.tar *mmcif index.txt')
        self.Logfile.insert('bzipping archive...')
        os.system('bzip2 ligand_bound_structures.tar')
        self.Logfile.insert('removing all bound mmcif files and index.txt file from '+self.depositDir)
        os.system('/bin/rm -f *mmcif index.txt')
        self.Logfile.insert('done!')



#        # apo structures
#        TextIndex=''
#        toDeposit=self.db.execute_statement("select CrystalName,mmCIF_model_file,mmCIF_SF_file from depositTable where StructureType is 'apo';")
#        for item in sorted(toDeposit):
#            xtal=str(item[0])
#            mmcif=str(item[1])
#            mmcif_sf=str(item[2])
#            if os.path.isfile(mmcif) and os.path.isfile(mmcif_sf):
#                self.Logfile.insert('copying {0!s} to {1!s}'.format(mmcif, self.depositDir))
#                os.system('/bin/cp {0!s} .'.format(mmcif))
#                self.Logfile.insert('copying {0!s} to {1!s}'.format(mmcif_sf, self.depositDir))
#                os.system('/bin/cp {0!s} .'.format(mmcif_sf))
#            else:
#                self.Logfile.insert('cannot find apo mmcif file for '+xtal+' => ERROR')
#
#            text = (    'label: {0!s}-apo\n'.format(xtal)+
#                        'description: apo structure of {0!s}\n'.format(xtal)+
#                        'model: {0!s}\n'.format(mmcif[mmcif.rfind('/')+1:])+
#                        'sf: {0!s}\n\n'.format(mmcif_sf[mmcif_sf.rfind('/')+1:])          )
#            TextIndex+=text
#
#        f = open('index.txt','w')
#        f.write(TextIndex)
#        f.close()
#
#        self.Logfile.insert('preparing tar archive...')
#        os.system('tar -cvf apo_structures.tar *apo* index.txt')
#        self.Logfile.insert('bzipping archive...')
#        os.system('bzip2 apo_structures.tar')
#        self.Logfile.insert('removing all apo mmcif files and index.txt file from '+self.depositDir)
#        os.system('/bin/rm -f *apo*mmcif index.txt')
#        self.Logfile.insert('done!')
#



class import_PDB_IDs(QtCore.QThread):
    def __init__(self,pdbCodes,database,xce_logfile):
        QtCore.QThread.__init__(self)
        self.pdbCodes=pdbCodes
        self.database=database
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.db=XChemDB.data_source(database)

    def run(self):

        for line in self.pdbCodes.split('\n'):
            if len(line.split('/')) == 2 and '-ligand_bound' in line:
                xtal=line[:line.rfind('-ligand_bound')].replace(' ','')
                pdbID=line.split('/')[1].replace(' ','')
                self.Logfile.insert('setting PDB ID for '+xtal+' to '+pdbID)
                sqlite="UPDATE mainTable SET Deposition_PDB_ID='{0!s}',RefinementOutcome='6 - Deposited' where CrystalName is '{1!s}';".format(pdbID, xtal)
                self.db.execute_statement(sqlite)


class compare_smiles_in_db_with_ligand_in_pdb(QtCore.QThread):
    def __init__(self,projectDir,database,xce_logfile):
        QtCore.QThread.__init__(self)
        self.projectDir=projectDir
        self.database=database
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.db=XChemDB.data_source(database)
        self.ErrorDict={}

    def update_ErrorDict(self,xtal,message):
        if xtal not in self.ErrorDict:
            self.ErrorDict[xtal]=[]
        self.ErrorDict[xtal].append(message)

    def run(self):

        os.chdir(self.projectDir)

        progress_step=1
        if len(glob.glob('*')) != 0:
            progress_step=100/float(len(glob.glob('*')))
        else:
            progress_step=1
        progress=0
        self.emit(QtCore.SIGNAL('update_progress_bar'), progress)


        for xtal in sorted(glob.glob('*')):
            if os.path.isfile(os.path.join(xtal,'refine.pdb')):
                smiles=self.db.execute_statement("select CompoundSmiles,CompoundCode from mainTable where CrystalName is '{0!s}'".format(xtal))
                try:
                    LigandSmiles=str(smiles[0][0])
                    LigandCode=str(smiles[0][1])
                    elementDict_smiles=smilestools(LigandSmiles).ElementDict()
                except IndexError:
                    self.Logfile.error("{0!s}: something is seems to be wrong with the CompoundCode or SMILES string: {1!s}".format(xtal, str(smiles)))
                    continue

                pdb=pdbtools(os.path.join(xtal,'refine.pdb'))
                ligandList=pdb.ligand_details_as_list()
                for ligand in ligandList:
                    resname     = ligand[0]
                    chainID     = ligand[1]
                    resseq      = ligand[2]
                    altLoc      = ligand[3]
                    elementDict_ligand=pdb.ElementDict(resname,chainID,resseq,altLoc)
                    for element in elementDict_ligand:
                        if elementDict_ligand[element] != elementDict_smiles[element]:
                            self.Logfile.error('{0!s}: {1!s} {2!s} {3!s} {4!s} contains different number of atoms than smiles in DB: {5!s} -> {6!s}'.format(xtal, resname, chainID, resseq, altLoc, LigandSmiles, LigandCode))
                            self.update_ErrorDict(xtal, '{0!s} {1!s} {2!s} {3!s} contains different number of atoms than smiles in DB'.format(resname, chainID, resseq, altLoc))
                            break


            progress += progress_step
            self.emit(QtCore.SIGNAL('update_progress_bar'), progress)

        self.emit(QtCore.SIGNAL('show_error_dict'), self.ErrorDict)
