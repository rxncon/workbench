<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <graph directed="1"  xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://www.cs.rpi.edu/XGMML">
    <att name="selected" value="1" type="boolean" />
    <att name="name" value="warzenschwein" type="string"/>
    <att name="shared name" value="warzenschwein" type="string"/>
    
<node id="Yfg2" label="Yfg2"><att name="type" value="state" /></node>
<node id="Yfg2_[DomainA]_ipi_Yfg2_[DomainB]" label="Yfg2_[DomainA]_ipi_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg2_[DomainB]-{ub}" label="Yfg2_[DomainB]-{ub}"><att name="type" value="state" /></node>
<node id="Yfg1_[DomainA]_cut_Yfg2_[DomainB]" label="Yfg1_[DomainA]_cut_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]_p-_Yfg2_[DomainB]" label="Yfg1_[DomainA]_p-_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg2_[DomainA]--[DomainB]" label="Yfg2_[DomainA]--[DomainB]"><att name="type" value="state" /></node>
<node id="Yfg2_[DomainB]-{truncated}" label="Yfg2_[DomainB]-{truncated}"><att name="type" value="state" /></node>
<node id="Yfg1_[DomainA]_ub+_Yfg2_[DomainB]" label="Yfg1_[DomainA]_ub+_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg2_[DomainB]-{p}" label="Yfg2_[DomainB]-{p}"><att name="type" value="state" /></node>
<node id="Yfg1_[DomainA]_pt_Yfg2_[DomainB]" label="Yfg1_[DomainA]_pt_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]_gef_Yfg2_[DomainB]" label="Yfg1_[DomainA]_gef_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]_deg_Yfg2_[DomainB]" label="Yfg1_[DomainA]_deg_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]--Yfg2_[DomainB]" label="Yfg1_[DomainA]--Yfg2_[DomainB]"><att name="type" value="state" /></node>
<node id="Yfg1_[DomainA]_bind_Yfg2_[DomainB]" label="Yfg1_[DomainA]_bind_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]_ppi_Yfg2_[DomainB]" label="Yfg1_[DomainA]_ppi_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]_trsc_Yfg2_[DomainB]" label="Yfg1_[DomainA]_trsc_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]_i_Yfg2_[DomainB]" label="Yfg1_[DomainA]_i_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]_syn_Yfg2_[DomainB]" label="Yfg1_[DomainA]_syn_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]_p+_Yfg2_[DomainB]" label="Yfg1_[DomainA]_p+_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]_gap_Yfg2_[DomainB]" label="Yfg1_[DomainA]_gap_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg2_[DomainB]-{gtp}" label="Yfg2_[DomainB]-{gtp}"><att name="type" value="state" /></node>
<node id="Yfg1_[DomainA]_trsl_Yfg2_[DomainB]" label="Yfg1_[DomainA]_trsl_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<node id="Yfg1_[DomainA]_ap_Yfg2_[DomainB]" label="Yfg1_[DomainA]_ap_Yfg2_[DomainB]"><att name="type" value="reaction" /></node>
<edge source="Yfg2_[DomainA]_ipi_Yfg2_[DomainB]" target="Yfg2_[DomainA]--[DomainB]"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_cut_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{truncated}"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_p-_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{p}"><att name="interaction" value="consume"/></edge>
<edge source="Yfg1_[DomainA]_ub+_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{ub}"><att name="interaction" value="produce"/></edge>
<edge source="Yfg2_[DomainB]-{p}" target="Yfg1_[DomainA]_gef_Yfg2_[DomainB]"><att name="interaction" value="!"/></edge>
<edge source="Yfg1_[DomainA]_pt_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{p}"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_gef_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{gtp}"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_deg_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{truncated}"><att name="interaction" value="consume"/></edge>
<edge source="Yfg1_[DomainA]_deg_Yfg2_[DomainB]" target="Yfg2"><att name="interaction" value="consume"/></edge>
<edge source="Yfg1_[DomainA]_deg_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{p}"><att name="interaction" value="consume"/></edge>
<edge source="Yfg1_[DomainA]_deg_Yfg2_[DomainB]" target="Yfg1_[DomainA]--Yfg2_[DomainB]"><att name="interaction" value="consume"/></edge>
<edge source="Yfg1_[DomainA]_deg_Yfg2_[DomainB]" target="Yfg2_[DomainA]--[DomainB]"><att name="interaction" value="consume"/></edge>
<edge source="Yfg1_[DomainA]_deg_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{ub}"><att name="interaction" value="consume"/></edge>
<edge source="Yfg1_[DomainA]_deg_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{gtp}"><att name="interaction" value="consume"/></edge>
<edge source="Yfg1_[DomainA]_bind_Yfg2_[DomainB]" target="Yfg1_[DomainA]--Yfg2_[DomainB]"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_ppi_Yfg2_[DomainB]" target="Yfg1_[DomainA]--Yfg2_[DomainB]"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_trsc_Yfg2_[DomainB]" target="Yfg2"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_i_Yfg2_[DomainB]" target="Yfg1_[DomainA]--Yfg2_[DomainB]"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_syn_Yfg2_[DomainB]" target="Yfg2"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_p+_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{p}"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_gap_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{gtp}"><att name="interaction" value="consume"/></edge>
<edge source="Yfg2_[DomainB]-{gtp}" target="Yfg1_[DomainA]_p+_Yfg2_[DomainB]"><att name="interaction" value="k-"/></edge>
<edge source="Yfg1_[DomainA]_trsl_Yfg2_[DomainB]" target="Yfg2"><att name="interaction" value="produce"/></edge>
<edge source="Yfg1_[DomainA]_ap_Yfg2_[DomainB]" target="Yfg2_[DomainB]-{p}"><att name="interaction" value="produce"/></edge>
</graph>