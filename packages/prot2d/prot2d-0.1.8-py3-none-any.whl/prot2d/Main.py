import svgwrite
import re
import Graphical
import Main_functions as Mafu
import os
import csv
from Structure_Database import *

def check_pdb_path(pdb_file):
    match = re.search(r'([a-zA-Z0-9]+)\.pdb$', pdb_file)
    if match:
        base_name = os.path.basename(pdb_file)
        file_id = os.path.splitext(base_name)[0]
        print("Creating 2D SVG image for: "+file_id)
        return file_id
    else:
        return None  

def visualize(dwg,protein,vis_type, AS_annotation, mark_endings, simple_helix, cysteins, simple_coil_avg):
    if len(protein.secondary_structures) == 0:
        return
    general_opacity=0.9
    only_path = False
    if(vis_type=='only-path'):
        #protein.get_protein_ordered_vis_objects(1, mark_endings)
        avg_path = Mafu.create_simplified_path(protein.residues,averaging=simple_coil_avg)
        dwg.add(svgwrite.shapes.Polyline(points=avg_path, stroke='black', stroke_width=5, fill="none"))
        only_path=True
    
    elif vis_type=='simple-coil':
        protein.get_protein_ordered_vis_objects(simple_coil_avg, mark_endings)
        # vis non-coil ss noraml but connect by simplifying coil structure
        Mafu.visualize_ordered_elements(Graphical,dwg,protein.ordered_vis_elements, simple_helix, 10, general_opacity, cysteins)

    elif vis_type=='normal':
        protein.get_protein_ordered_vis_objects(1, mark_endings)
        Mafu.visualize_ordered_elements(Graphical,dwg,protein.ordered_vis_elements, simple_helix,avg_coil=1, general_opacity=general_opacity,cysteins=cysteins)
    
    elif vis_type=='testing':
        protein.get_protein_ordered_vis_objects(1)
        Mafu.create_testing_vis(Graphical,dwg,ss_objects=protein.secondary_structures)
    
    elif vis_type=='fruchtermann':
        protein.get_protein_ordered_vis_objects(1)
        # vis of non coil ss segments that are pushe apart using Fruchtermann Reingold layout connected with simple lines
        Mafu.do_fruchtermann_reingold_layout(protein.secondary_structures, k=0.5, iter=50)
        protein.scale_shift_coords(scale=1,shift=20, make_positive=True) #make everything positive
        Mafu.visualize_ordered_elements(Graphical,dwg,protein.ordered_vis_elements, simple_helix,avg_coil=10,general_opacity=general_opacity, cysteins=cysteins)
    
    else:
        raise ValueError("Error: Please provide a valid vis_type!")
        # additional:

    if AS_annotation:
        Mafu.add_residue_annotations(dwg, protein.secondary_structures,only_path)

def get_best_rotation(pdb_file):
    file_id = check_pdb_path(pdb_file)
    protein = Mafu.Protein()
    pdb_element = protein.parse_pdb(pdb_file)
    protein.get_secondary_structure(pdb_element,pdb_file)
    
    #rotate protein
    protein.find_best_view_angle()
    print()
    print("Best found rotation: ")
    print(protein.best_rotation)
    return protein.best_rotation

def db_get_SF_info():
    """
    user can input a SCOP SF and get information on the representative etc
    """
    pass
def db_set_fixed_SF_rot():
    """
    user can input a SF and a rotation(format: pymol / UT).
    This is than set as fixe rotation for the SF in the db
    """
    pass

def format_domain_annotation_file_chainsaw(chainsaw_annotation_tsv, output_dir):
    with open(chainsaw_annotation_tsv, 'r', newline='', encoding='utf-8') as file:
        tsv_reader = csv.reader(file, delimiter='\t')
        header = next(tsv_reader)
        chain_id_index = header.index("chain_id")
        chopping_index = header.index("chopping")
        
        # Extract chain ID (assuming it's the same for all rows)
        chain_id = None
        for row in tsv_reader:
            if row[chopping_index] == "NULL":
                print("0 domains found in chainsaw annotation")
                return None
            chain_id = row[chain_id_index]
            row[chopping_index]=row[chopping_index].replace('_',',')
            string_domains = row[chopping_index].split(',')
            string_domains = sorted(string_domains, key=lambda x: int(x.split('-')[0]))

        # Read in finished, do TSV writing in the correct format
        directory, file_name = os.path.split(chainsaw_annotation_tsv)
        new_file_name = file_name.replace('.tsv', '_prot2DFormattedDomains.tsv')   
        domain_annotation_formatted_file = os.path.join(output_dir, new_file_name)
        
        with open(domain_annotation_formatted_file, 'w', newline='', encoding='utf-8') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['chain_id', 'domain', 'domain_start', 'domain_end'])
            
            for idx, domain in enumerate(string_domains, start=1):
                start, end = map(int, domain.split('-'))
                tsv_writer.writerow([chain_id, idx, start, end])

        return domain_annotation_formatted_file

def create_2DSVG_from_pdb(pdb_file, result_dir, tmp_dir, family_vis=True, fam_aligned_splitting = True, drop_family_prob = 0.5,foldseek_executable=None, domain_splitted=False, domain_annotation_file=None, domain_hull=True, visualisation_type ="normal", 
                    cysteins=True, as_annotation=False, mark_endings=True, simple_helix=True, show_aligned_lddt=False, find_best_rot_step = 30, simple_coil_avg=10):
    """
    Args:
    - pdb_file (str): Path to pdb file the visualisation file is generated on.
    - result_dir (str): Path to dir, where the output file is saved (file name is automatically set based on input file name).
    - tmp_dir (str): Path to dir, where temporary files needed for analyis (e.g. foldseek) and visualisations are saved.
    
    - family_vis (bool): If True, enables family-wise visualization, uses SCOP SF database with calculated representatives. Default is True.
    - fam_aligned_splitting (bool): If True, the protein is split into SF-aligned (is rotated based on this segment) and not-aligned parts. THey are connected with a dashed line. Default is True.
    - drop_family_prob (float): Allows the program to drop a chosen SF if the FoldSeek probability is smaller than given cut-off. In this case the protein rotation is determined using the implemented "find_best_view_angle" method. Default is 0.5. 
    - show_aligned_lddt (bool): LDDT scores from FoldSeek alignment to best matching SF is shown per residue (color + value). Default is False. 
    - foldseek_executable (str): Path....

    - domain_splitted (bool): If True, protein is split into domains using the provided domain annotation file. Can be used in combination with family_vis which is then applied on each domain seperatly. Default is False.
    - domain_annotation_file (str): Path to the domain annotation file. Required if domain_splitted is True.
    - domain_hull (bool): If True sourounds domains with smoothed convex hull colored based on the secondary structure composition (R,G,B) <-> (helix,sheet,coil). Default is True

    - visualisation_type (string): "only-path", "normal", or "simple-coil". Default is "normal".
    - cysteins (bool): If True, includes calculated cystein bonds in the visualisation. Default is True.
    - as_annotation (bool): If True, includes AS-annotation. Default is False.
    - mark_endings (bool): If True, marks the endings. Default is True.
    - simple_helix (bool): If True, helix are represented in a simple way (file size eficient). Default is True.
    - find_best_rot_step (int): Is the size of steps per 3D rotation angle (total=3) taken to find the rotatoin showing the most of the input protein. Increasing leads to faster runtime but worse visualisations. Default is 30.
    - simple_coil_avg (int): Coil structures will be summarised together. e.g. 10 means that every 10 coil-residues will be averaged and treated as one point. Bigger values lead to higher simplification. Is only used when "simple-coil" or "only-path" is used. Default is 10
    
    Returns:
    - result: Creates a SVG file containing the 2D visualisation of the input protein in the given result_dir.
    """
    ############## Validate arguments ##############
    if domain_splitted and not domain_annotation_file:
        raise ValueError("Domain annotation file is required for domain-split analysis.")
    if visualisation_type=="split-alignment" and not family_vis:
        raise ValueError("Alignment split option can only be used when doing the family visualisation (aligned part is used for splitting).")
    valid_vis_types = ["only-path","normal","simple-coil"]
    if visualisation_type not in valid_vis_types:
        raise ValueError(f'"{visualisation_type}" is not a valid visualisation type. Please use one of the following: {valid_vis_types}')
    file_id = check_pdb_path(pdb_file)
    if file_id ==None:
        raise ValueError(f'"{pdb_file}" is not a valid pdb input. Please check the path and the file.')
    #counteract impossible combinations
    if not family_vis:
        fam_aligned_splitting=False
        drop_family_prob=False
    
    structure_database_obj = Structure_Database(foldseek_executable,tmp_dir)


    ############## 1) Split into domains if used ##############
    if domain_splitted:
        domain_files = Mafu.get_domain_pdbs(pdb_file,domain_annotation_file,tmp_dir)
    else:
        domain_files = []
        domain_files.append(pdb_file)


    ############## 2) Get rotation of protein (family-vis / best rotation) ##############
    dom_proteins = []
    for dom_file in domain_files:
        if family_vis:
            sf_aligned_pdb_file, aligned_region,lddtfull = structure_database_obj.initial_and_fixed_Sf_rot_region(dom_file)
            Mafu.add_header_to_pdb(sf_aligned_pdb_file)
            dom_prot = Mafu.Protein()
            pdb_element = dom_prot.parse_pdb(sf_aligned_pdb_file)
            dom_prot.get_secondary_structure(pdb_element,sf_aligned_pdb_file)
            dom_prot.scale_shift_coords(scale=30,x_shift=0,y_shift=0, make_positive=False)
            dom_prot.add_lddt_to_aligned_residues(aligned_region,lddtfull) if show_aligned_lddt else None
            if fam_aligned_splitting:
                # split protein in 3 segments (aligment-based)
                front_part,aligned_part,end_part = dom_prot.split_aligned_part(aligned_region)
                # shift left and right part to the sides and make positive again
                front_aligned_x_shift = Mafu.calc_overlap_distance_between_prots(front_part,aligned_part) + 200
                aligned_end_x_shift = Mafu.calc_overlap_distance_between_prots(aligned_part,end_part) + 200
                end_part.scale_shift_coords(scale=1,x_shift=aligned_end_x_shift,y_shift=0,make_positive=False)
                front_part.scale_shift_coords(scale=1,x_shift=-front_aligned_x_shift,y_shift=0,make_positive=False)
            #TODO check for prob > threshhold
        else:
            # manually find best rotation and continue with that
            Mafu.add_header_to_pdb(dom_file)
            dom_prot = Mafu.Protein()
            pdb_element = dom_prot.parse_pdb(dom_file)
            dom_prot.get_secondary_structure(pdb_element,dom_file)
            dom_prot.scale_shift_coords(scale=30,x_shift=0,y_shift=0, make_positive=False)
            dom_prot.find_best_view_angle(step_width = find_best_rot_step)
        dom_proteins.append(dom_prot)
    
    # push domains apart if necceray 
    #Mafu.repeat_layout_pairwise(domains=dom_proteins, k=1, iter_steps=20)

    # make all coords postive
    full_prot_residues = [res for dom in dom_proteins for res in dom.residues]
    full_prot = Mafu.Protein()
    full_prot.residues = full_prot_residues
    full_prot.scale_shift_coords(scale=1,x_shift=0,y_shift=0,make_positive=True)

    #shift domains to be in linear line:
    Mafu.shift_domains_in_origin_line(dom_proteins, 100)
    #shift for border space
    full_prot.scale_shift_coords(scale=1,x_shift=100,y_shift=100,make_positive=False)
    
    ############## 3) & 4) Create visualisatoin as wanted: only-path / normal / simple-coil (+ fam_aligned_splitting) ##############
    viewbox = Mafu.calculate_viewbox(full_prot.residues,50) #TODO should be used for final usage but for now shit because browser view is wrong --> when using make_postive can be false for true coords
    dwg = svgwrite.Drawing(result_dir+file_id+'_'+visualisation_type+'_vis.svg', size=('2000mm', '2000mm'), viewBox=viewbox)
    last_dom=None

    for dom_prot in dom_proteins: 
        if fam_aligned_splitting:
            front_part, aligned_part, end_part = dom_prot.fam_aligned_parts
            visualize(dwg,front_part,visualisation_type, as_annotation, mark_endings, simple_helix, cysteins, simple_coil_avg)
            visualize(dwg,aligned_part,visualisation_type, as_annotation, mark_endings, simple_helix, cysteins,simple_coil_avg)
            visualize(dwg,end_part,visualisation_type, as_annotation, mark_endings, simple_helix, cysteins,simple_coil_avg)
            Mafu.add_dashed_line_between_proteins(dwg,front_part,aligned_part,end_part)
        else:
            visualize(dwg,dom_prot,visualisation_type, as_annotation, mark_endings, simple_helix, cysteins,simple_coil_avg)
        
        if domain_splitted:
            dom_prot.add_hull(dwg,dom_prot.get_hull_color(), opacity=0.4) if domain_hull else None
            dwg.add(last_dom.connect_to_protein_dashline(dom_prot)) if last_dom != None else None
        last_dom=dom_prot
    
    dwg.save()


#formatted_domain_annotation_file = helper.format_domain_annotation_file_chainsaw("/Users/constantincarl/Uni/chainsaw-main/results/1kt1.tsv","/Users/constantincarl/Uni/BA_pdb_files_senorer/own_domain_annotation/")
#helper.add_header_to_predicted_pdb("/Users/constantincarl/Uni/BA_pdb_files_senorer/trimmed_proteins/pdb/SP|P0C555|Bungarus_fasciatus.pdb")


# three finger pdb: /Users/constantincarl/Uni/BachelorThesis/pdb_files/SP|P0DP58|Homo_sapiens.pdb
# 3 domain pdb : /Users/constantincarl/Uni/BachelorThesis/pdb_files/1kt1.pdb
# 3 domain annotation file: temp/1kt1_prot2DFormattedDomains.tsv


foldseek_executable = '/Users/constantincarl/Uni/BachelorThesis/FoldSeek/foldseek/bin/foldseek'

create_2DSVG_from_pdb(pdb_file="/Users/constantincarl/Uni/BachelorThesis/pdb_files/1kt1.pdb",result_dir="results/",tmp_dir="temp/",family_vis=True, fam_aligned_splitting=False, domain_splitted=True, visualisation_type ="normal", 
                    cysteins=True, as_annotation=False, mark_endings=True, simple_helix=True, show_aligned_lddt=True,
                    domain_annotation_file="tests/1kt1_prot2DFormattedDomains.tsv", drop_family_prob = 0.5,foldseek_executable=foldseek_executable, find_best_rot_step=30, simple_coil_avg=10)





####  program options: ####
    
# 1) domain-splitted / total  --> domain annotation file needed
# 2) family-vis / best rotation --> db needed (if domain: do rest per domain)
# 3) only-path / normal / simple-coil / family-alignement splitting (only when family-vis is chosen)
# 4) cysteins & AS-annotation & mark-endings & simple-helix &