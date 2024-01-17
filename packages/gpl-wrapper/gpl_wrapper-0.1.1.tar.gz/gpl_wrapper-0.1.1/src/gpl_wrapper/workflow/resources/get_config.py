import click
import os

def validate_vcf_file(ctx, param, value):
    if value == "NOFILE":
        return value
    else:
        if not os.path.isfile(value):
            raise click.BadParameter(f"File '{value}' does not exist.")
        return value



def generate_nextflow_config(tumor_name, normal_name, tumor_bam, tumor_bam_index, normal_bam, normal_bam_index, output_dir, tumor_smlv_vcf, tumor_sv_vcf, ref_data_genome, ref_files_dir, publish_mode, cpus):
    # Handle missing file inputs

    config = f'''params {{
  // Input
  tumor_name = '{tumor_name}'
  normal_name = '{normal_name}'
  tumor_bam = '{tumor_bam}'
  normal_bam = '{normal_bam}'
  tumor_bam_index = '{tumor_bam_index}'
  normal_bam_index = '{normal_bam_index}'
  // Output
  output_dir = '{output_dir}'
  publish_mode = '{publish_mode}'

  // Resource allocation and software paths
  cpus = {cpus}
  // Maximum JVM stack size for relevant tools
  mem_amber = '14G'
  mem_cobalt = '14G'
  mem_gridss = '26G'
  mem_gripss = '14G'
  mem_linx = '14G'
  mem_purple = '14G'
  // JAR paths
  jar_amber = '/opt/hmftools/amber.jar'
  jar_cobalt = '/opt/hmftools/cobalt.jar'
  jar_gridss = '/opt/gridss/gridss.jar'
  jar_gripss = '/opt/hmftools/gripss.jar'
  jar_purple = '/opt/hmftools/purple.jar'
  jar_linx = '/opt/hmftools/linx.jar'
  // Misc paths
  path_circos = 'circos'

  // Reference data
  tumor_smlv_vcf = '{tumor_smlv_vcf}'
  tumor_sv_vcf = '{tumor_sv_vcf}'

  ref_data_genome = '{ref_data_genome}'

  // AMBER, COBALT
  ref_data_amber_loci = "{ref_files_dir}/copy_number/GermlineHetPon.38.vcf"
  ref_data_cobalt_gc_profile = "{ref_files_dir}/copy_number/GC_profile.1000bp.38.cnp"
  // GRIDSS
  ref_data_gridss_blacklist = "{ref_files_dir}/sv/gridss_blacklist.38.bed"
  ref_data_gridss_breakend_pon = "{ref_files_dir}/sv/sgl_pon.38.bed"
  ref_data_gridss_breakpoint_pon = "{ref_files_dir}/sv/sv_pon.38.bedpe"
  // LINX
  ref_data_linx_fragile_sites = "{ref_files_dir}/sv/fragile_sites_hmf.38.csv"
  ref_data_linx_line_elements = "{ref_files_dir}/sv/line_elements.38.csv"
  // Misc
  ref_data_ensembl_data_dir = "{ref_files_dir}/common/ensembl_data"
  ref_data_known_hotspots = "{ref_files_dir}/variants/KnownHotspots.somatic.38.vcf.gz"
  ref_data_known_fusions = "{ref_files_dir}/sv/known_fusions.38.bedpe"
  ref_data_known_fusion_data = "{ref_files_dir}/sv/known_fusion_data.38.csv"
  ref_data_driver_gene_panel = "{ref_files_dir}/common/DriverGenePanel.38.tsv"
}}

docker.enabled = false

process.container = 'labxa/gpl'
process.cpus = params.cpus
process.cache = 'lenient'
trace.overwrite = "false"
report.overwrite = "true"
timelime.overwrite = "true"

// Fail task if any command returns non-zero exit code
shell = ['/bin/bash', '-euo', 'pipefail']

dag {{
  enabled = true
  file = '{output_dir}/nextflow/reports/dag.svg'
  overwrite = true
}}

report {{
  enabled = true
  file = '{output_dir}/nextflow/reports/report.html'
}}

timeline {{
  enabled = true
  file = '{output_dir}/nextflow/reports/timeline.html'
  overwrite = true
}}

trace {{
  enabled = true
  file = '{output_dir}/nextflow/reports/trace.txt'
}}
'''
    return config

@click.command()
@click.option('--tumor_name', type=str, required=True)
@click.option('--normal_name', type=str, required=True)
@click.option('--tumor_bam', type=click.Path(exists=True), required=True)
@click.option('--tumor_bam_index', type=click.Path(exists=True), required=True)
@click.option('--normal_bam', type=click.Path(exists=True), required=True)
@click.option('--normal_bam_index', type=click.Path(exists=True), required=True)
@click.option('--output_dir', type=click.Path(), required=True)
@click.option('--tumor_smlv_vcf', type=str, callback=validate_vcf_file)
@click.option('--tumor_sv_vcf', type=str, callback=validate_vcf_file)
@click.option('--ref_data_genome', type=click.Path(exists=True), required=True)
@click.option('--ref_files_dir', type=click.Path(exists=True), required=True)
@click.option('--publish_mode', type=str, default='copy')
@click.option('--cpus', type=int, default=8)
def main(tumor_name, normal_name, tumor_bam, tumor_bam_index, normal_bam, normal_bam_index, output_dir, tumor_smlv_vcf, tumor_sv_vcf, ref_data_genome, ref_files_dir, publish_mode, cpus):
    config_content = generate_nextflow_config(tumor_name, normal_name, tumor_bam, tumor_bam_index, normal_bam, normal_bam_index, output_dir, tumor_smlv_vcf, tumor_sv_vcf, ref_data_genome, ref_files_dir, publish_mode, cpus)
    print(config_content)

if __name__ == '__main__':
    main()
