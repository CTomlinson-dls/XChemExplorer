# last edited: 05/07/2017, 15:00

import os,sys

sys.path.append(os.getenv('XChemExplorer_DIR')+'/lib')
import XChemLog
import XChemDB
import XChemMain

from XChemUtils import pdbtools
from XChemUtils import mtztools


def create_ICM_input_file(html_export_directory,database):

    if os.getcwd().startswith('/work'):
        panddaDir='panddaDir="%s"\n' %html_export_directory.replace('/work','W:')
        molcart='connect molcart filename="%s"\n' %database.replace('/work','W:')
    else:
        panddaDir='panddaDir="%s"\n' %html_export_directory
        molcart='connect molcart filename="%s"\n' %database

    icm_in = (
        '#!/usr/local/bin/icm\n'
        '# Author: Brian Marsden\n'
        +panddaDir+
#        'panddaDir="%s"\n' %html_export_directory+
        '\n'
        'set directory panddaDir\n'
        +molcart+
#        'connect molcart filename="%s"\n' %database+

#        'query molcart "select p.ID,p.CrystalName,p.PANDDA_site_event_index,p.PANDDA_site_confidence,p.CrystalName || '_event'|| p.PANDDA_site_event_index as ModelName,m.CompoundCode,m.CompoundSMILES,p.PANDDA_site_name,p.PANDDA_site_confidence as LigandConfidence,p.RefinementOutcome as ModelStatus,p.PANDDA_site_comment,p.PANDDA_site_x,p.PANDDA_site_y,p.PANDDA_site_z, p.PANDDA_site_spider_plot,m.DataProcessingResolutionHigh,m.DataProcessingSpaceGroup,m.DataProcessingUnitCell,m.RefinementPDB_latest,m.RefinementMTZ_latest,p.PANDDA_site_event_map from panddaTable as p, mainTable as m where p.CrystalName=m.CrystalName and p.PANDDA_site_ligand_placed='True' and (LigandConfidence like '1%' or LigandConfidence like '2%' or LigandConfidence like '3%' or LigandConfidence like '4%') order by p.CrystalName,ModelStatus desc,PANDDA_site_event_index" name="T"\n'

#        'query molcart "select p.ID,p.CrystalName,p.PANDDA_site_event_index,p.PANDDA_site_confidence,p.CrystalName || '
#        "'_event'|| p.PANDDA_site_event_index as ModelName,m.CompoundCode,m.CompoundSMILES,p.PANDDA_site_name,p.PANDDA_site_confidence "
#        "as LigandConfidence,p.RefinementOutcome as ModelStatus,p.PANDDA_site_comment,p.PANDDA_site_x,p.PANDDA_site_y,p.PANDDA_site_z, "
#        "p.PANDDA_site_spider_plot,m.DataProcessingResolutionHigh,m.DataProcessingSpaceGroup,m.DataProcessingUnitCell,"
#        "m.RefinementPDB_latest,m.RefinementMTZ_latest,p.PANDDA_site_event_map from panddaTable as p, mainTable as m "
#        "where p.CrystalName=m.CrystalName and p.PANDDA_site_ligand_placed='True' and (LigandConfidence like '1%' "
#        "or LigandConfidence like '2%' or LigandConfidence like '3%' or LigandConfidence like '4%') "
#        'order by p.CrystalName,ModelStatus desc,PANDDA_site_event_index" name="T"\n'

#        'query molcart "select p.ID,p.CrystalName,p.PANDDA_site_event_index,p.PANDDA_site_confidence,p.CrystalName || '
#        "'_event'|| p.PANDDA_site_event_index as ModelName,m.CompoundCode,m.CompoundSMILES,p.PANDDA_site_name,p.PANDDA_site_confidence "
#        "as LigandConfidence,p.RefinementOutcome as ModelStatus,p.PANDDA_site_comment,p.PANDDA_site_x,p.PANDDA_site_y,p.PANDDA_site_z, "
#        "p.PANDDA_site_spider_plot,m.DataProcessingResolutionHigh,m.DataProcessingSpaceGroup,m.DataProcessingUnitCell,"
#        "m.RefinementBoundConformation,m.RefinementMTZ_latest,p.PANDDA_site_event_map from panddaTable as p, mainTable as m "
#        "where p.CrystalName=m.CrystalName and p.PANDDA_site_ligand_placed='True' and (p.RefinementOutcome like '4%' or p.RefinementOutcome like '5%' or p.RefinementOutcome like '6%') "
#        'order by p.CrystalName,ModelStatus desc,PANDDA_site_event_index" name="T"\n'

#        'query molcart "select p.ID,p.CrystalName,p.PANDDA_site_event_index,p.PANDDA_site_confidence,p.CrystalName || '
#        "'_event'|| p.PANDDA_site_event_index as ModelName,m.CompoundCode,m.CompoundSMILES,p.PANDDA_site_name,p.PANDDA_site_confidence "
#        "as LigandConfidence,p.RefinementOutcome as ModelStatus,p.PANDDA_site_comment,p.PANDDA_site_x,p.PANDDA_site_y,p.PANDDA_site_z, "
#        "p.PANDDA_site_spider_plot,m.DataProcessingResolutionHigh,m.DataProcessingSpaceGroup,m.DataProcessingUnitCell,"
#        "m.RefinementBoundConformation,m.RefinementMTZ_latest,p.PANDDA_site_event_map from panddaTable as p, mainTable as m "
#        "where p.CrystalName=m.CrystalName and p.PANDDA_site_ligand_placed='True' and (p.RefinementOutcome like '4%' or p.RefinementOutcome like '5%' or p.RefinementOutcome like '6%') "
#        " and (p.PANDDA_site_confidence like '1%' or p.PANDDA_site_confidence like '2%' or p.PANDDA_site_confidence like '3%' or p.PANDDA_site_confidence like '4%')"
#        'order by p.CrystalName,ModelStatus desc,PANDDA_site_event_index" name="T"\n'

        'query molcart "select p.ID,p.CrystalName,p.PANDDA_site_event_index,p.PANDDA_site_confidence,p.CrystalName || '
        "'_event'|| p.PANDDA_site_event_index as ModelName,m.CompoundCode,m.CompoundSMILES,p.PANDDA_site_name,p.PANDDA_site_confidence "
        "as LigandConfidence,p.RefinementOutcome as ModelStatus,p.PANDDA_site_comment,p.PANDDA_site_x,p.PANDDA_site_y,p.PANDDA_site_z, "
        "p.PANDDA_site_spider_plot,m.DataProcessingResolutionHigh,m.DataProcessingSpaceGroup,m.DataProcessingUnitCell,"
        "m.RefinementBoundConformation,m.RefinementMTZ_latest,p.PANDDA_site_event_map from panddaTable as p, mainTable as m "
        "where p.CrystalName=m.CrystalName and p.PANDDA_site_ligand_placed='True' and (m.RefinementOutcome like '4%' or m.RefinementOutcome like '5%' or m.RefinementOutcome like '6%') "
        " and (p.PANDDA_site_confidence like '1%' or p.PANDDA_site_confidence like '2%' or p.PANDDA_site_confidence like '3%' or p.PANDDA_site_confidence like '4%')"
        'order by p.CrystalName,ModelStatus desc,PANDDA_site_event_index" name="T"\n'


        'numToDo=Nof(T)\n'
        '\n'
        'macro generateICB s_eventID s_pdb s_ligandSMILES s_eventMap R_coords\n'
        'l_confirm=no\n'
        'l_info=no\n'
        'l_commands=no\n'
        'l_warn=no\n'
        'print s_eventID s_pdb s_ligandSMILES s_eventMap R_coords\n'
        '# Read pdb\n'
        'read pdb s_pdb\n'
        'if Nof(a_1.?lig)==0 then\n'
        '  print "No ligand!"\n'
        '  delete a_*.*\n'
        '  return\n'
        'endif\n'
        '# Fix ligand topology\n'
        'set bond topology a_1.?lig s_ligandSMILES\n'
        '# Read event map\n'
        'read map s_eventMap\n'
        'contourEDS Name( map )[1] {2.0} {"cyan"} a_1.?lig | Sphere(a_1.?lig !a_1.?lig 7.5) yes yes\n'
        'assign sstructure\n'
        'cool a_ no\n'
        'color background refresh rgb={0,0,0}\n'
        'display xstick Res(Sphere(a_1.?lig !a_1.?lig 7.5))\n'
        'read binary s_icmhome+"shapes" name="star"\n'
        'display star\n'
        'translate star R_coords\n'
        'center star margin=0.0\n'
        'undisplay star\n'
        'center a_1.?lig\n'
        'write png "mapImages/"+s_eventID+"_large.png" window={800,600} GRAPHICS.quality=Max(image graphic)\n'
        'write png "mapImages/"+s_eventID+"_small.png" window={150,150} GRAPHICS.quality=Max(image graphic)\n'
        'delete star\n'
        'writeProject "icbs/"+s_eventID+".icb" no\n'
        'delete maps\n'
        'delete a_*.\n'
        'delete grob\n'
        'endmacro\n'
        '\n'
        'for i=1,numToDo\n'
        '  ligandSMILES=T.CompoundSMILES[i]\n'
        '  # PDB file path\n'
        '  pdbID="pdbs/"+T.ModelName[i]+".pdb"\n'
        '  if (T.PANDDA_site_name[i]!="" & T.PANDDA_site_confidence[i]!="None") then\n'
        '  # Get event ID\n'
        '  eventID=T.ModelName[i]+"_"+T.CompoundCode[i]\n'
#        '  eventID=T.ModelName[i]\n'
        '  # Event map path\n'
        '  eventMap="maps/"+T.ModelName[i]+".ccp4"\n'
        '  # Ligand centre\n'
        '  ligR3={$T.PANDDA_site_x[i],$T.PANDDA_site_y[i],$T.PANDDA_site_z[i]}\n'
        '  generateICB eventID,pdbID,ligandSMILES,eventMap,ligR3\n'
        '  endif\n'
        'endfor\n'
        )

    f=open('%s/dsEvent_sqlite.icm' %html_export_directory,'w')
    f.write(icm_in)
    f.close()

class export_to_html:

    def __init__(self,htmlDir,projectDir,database,xce_logfile):
        self.htmlDir = htmlDir
        self.projectDir = projectDir
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.db=XChemDB.data_source(database)
        self.db_dict = None
        self.pdb = None

    def prepare(self):
        self.Logfile.insert('======== preparing HTML summary ========')
        self.makeFolders()
#        self.write_HTML_header()
        for xtal in self.db.samples_for_html_summary():
            self.db_dict = self.db.get_db_dict_for_sample(xtal)
            self.copy_pdb(xtal)
            self.copy_electron_density(xtal)
            self.copy_ligand_files(xtal)
            for ligand in self.ligands_in_pdbFile(xtal):
                print ligand


    def makeFolders(self):
        self.Logfile.insert('preparing folders in html directory')
        os.chdir(self.htmlDir)
        if not os.path.isdir('js'):
            os.mkdir('js')
        if not os.path.isdir('css'):
            os.mkdir('css')
        if not os.path.isdir('compoundFiles'):
            os.mkdir('compoundFiles')
        if not os.path.isdir('residueplots'):
            os.mkdir('residueplots')
        if not os.path.isdir('pdbs'):
            os.mkdir('pdbs')
        if not os.path.isdir('maps'):
            os.mkdir('maps')

    def write_HTML_header(self):
        os.chdir(self.htmlDir)
        self.Logfile.insert('writing html header')
        if os.path.isfile('index.html'):
            os.system('/bin/rm -f index.html')
        f = open('index.html','w')
        f.write(XChemMain.html_header)
        f.close()

    def copy_pdb(self,xtal):
        os.chdir(os.path.join(self.htmlDir, 'pdbs'))
        self.pdb = None
        if os.path.isfile(os.path.join(self.projectDir,xtal,'refine.split.bound-state.pdb')):
            self.pdb = pdbtools('refine.split.bound-state.pdb')
            self.Logfile.insert('%s: copying refine.split.bound-state.pdb to html directory' %xtal)
            os.system('/bin/cp %s/refine.split.bound-state.pdb %s.pdb' %(os.path.join(self.projectDir,xtal),xtal))
        else:
            self.Logfile.error('%s: cannot find refine.split.bound-state.pdb')

    def copy_electron_density(self,xtal):
        os.chdir(os.path.join(self.htmlDir, 'maps'))

        if os.path.isfile(os.path.join(self.projectDir,xtal,'2fofc.map')):
            self.Logfile.insert('%s: copying 2fofc.map to html directory' %xtal)
            os.system('/bin/cp %s/2fofc.map %s_2fofc.ccp4' %(os.path.join(self.projectDir,xtal),xtal))
        else:
            self.Logfile.error('%s: cannot find 2fofc.map')

        if os.path.isfile(os.path.join(self.projectDir,xtal,'fofc.map')):
            self.Logfile.insert('%s: copying fofc.map to html directory' %xtal)
            os.system('/bin/cp %s/fofc.map %s_fofc.ccp4' %(os.path.join(self.projectDir,xtal),xtal))
        else:
            self.Logfile.error('%s: cannot find fofc.map')

    def copy_ligand_files(self,xtal):
        os.chdir(os.path.join(self.htmlDir,'compoundFiles'))

        if os.path.isfile(os.path.join(self.projectDir,xtal,self.db_dict['CompoundCode']+'.cif')):
            self.Logfile.insert('%s: copying compound cif file' %xtal)
            os.system('/bin/cp %s %s_%s' %(os.path.join(self.projectDir,xtal,self.db_dict['CompoundCode']+'.cif'),xtal,self.db_dict['CompoundCode']+'.cif'))
        else:
            self.Logfile.error('%s: cannot find compound cif file')

        if os.path.isfile(os.path.join(self.projectDir,xtal,self.db_dict['CompoundCode']+'.png')):
            self.Logfile.insert('%s: copying compound png file' %xtal)
            os.system('/bin/cp %s %s_%s' %(os.path.join(self.projectDir,xtal,self.db_dict['CompoundCode']+'.png'),xtal,self.db_dict['CompoundCode']+'.png'))
        else:
            self.Logfile.error('%s: cannot find compound png file')

    def ligands_in_pdbFile(self,xtal):
        os.chdir(os.path.join(self.projectDir,xtal))
        ligPDB = []
        ligList = []
        self.Logfile.insert('%s: reading ligands to type LIG in refine.split.bound-state.pdb' %xtal)
        if os.path.isfile('refine.split.bound-state.pdb'):
            ligPDB = self.pdb.save_residues_with_resname(os.path.join(self.projectDir, xtal), 'LIG')
        else:
            self.Logfile.error('%s: cannot find refine.split.bound-state.pdb')
        if ligPDB == []:
            self.Logfile.error('%s; cannot find any ligands of type LIG in refine.split.bound-state.pdb')
        else:
            for lig in sorted(ligPDB):
                ligList.append(lig.replace('.pdb', ''))
        return ligList


    def find_matching_event_map(self,xtal,ligID):
        os.chdir(os.path.join(self.projectDir, xtal))
        self.Logfile.insert('%s: trying to find fitting event maps for modelled ligands' %xtal)
        if os.path.isfile('no_pandda_analysis_performed'):
            self.Logfile.warning('%s: no pandda analysis performed; skipping this step...' %xtal)
            return
        ligCC = []
        for mtz in sorted(glob.glob('*event*.native*P1.mtz')):
            self.get_lig_cc(xtal, mtz, ligID+'.pdb')
            cc = self.check_lig_cc(mtz.replace('.mtz', '_CC'+ligID+'.log'))
            self.Logfile.insert('%s: %s -> CC = %s for %s' %(xtal,ligID,cc,mtz))
            try:
                ligCC.append([mtz,float(cc)])
            except ValueError:
                ligCC.append([mtz, 0.00])
        highestCC = max(ligCC, key=lambda x: x[0])[1]
        if highestCC == 0.00 or ligCC is []:
            self.Logfile.error('%s: best CC of ligand %s for any event map is 0!' %(xtal,lig))
        else:
            self.Logfile.insert('%s: selected event map -> CC(%s) = %s for %s' %(xtal,lig,highestCC,mtz[mtz.rfind('/')+1:]))
            print '====>',xtal.ligID,mtz


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

