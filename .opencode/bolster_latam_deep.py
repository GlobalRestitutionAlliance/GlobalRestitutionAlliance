import csv, json, hashlib, os, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"W:\Legal\LATIN_AMERICA")
TODAY = "2026-11-21"

# High-level, publicly documented anchors only. No fabricated citations/case numbers.
# Pools/instruments here are planning scaffolds; existing manifests may override.
PROFILES = {
  "US_AG_ANTIGUA_AND_BARBUDA": {"country":"Antigua and Barbuda","iso":"AG","pool":"$2,000,000,000","instruments":25,"issues":"Climate vulnerability, offshore financial governance pressures, post-colonial economic constraints","anchors":["Colonial-era extraction and labor systems in the Caribbean","Climate change loss and damage exposure","Sovereign debt and external economic pressure"]},
  "US_AR_ARGENTINA": {"country":"Argentina","iso":"AR","pool":"$250,000,000,000","instruments":25,"issues":"Dirty War, sovereign debt, external political intervention","anchors":["1976-1983 military dictatorship and human rights violations (CONADEP/Nunca Mas public record)","Operation Condor regional repression (declassified public records)","Sovereign debt crises and external creditor pressure"]},
  "US_BB_BARBADOS": {"country":"Barbados","iso":"BB","pool":"$5,000,000,000","instruments":25,"issues":"Climate, colonial legacy, economic transition","anchors":["Plantation slavery and colonial extraction legacy","Climate vulnerability and adaptation costs","Post-independence economic restructuring pressures"]},
  "US_BO_BOLIVIA": {"country":"Bolivia","iso":"BO","pool":"$20,000,000,000","instruments":25,"issues":"Indigenous rights, resource extraction, political intervention","anchors":["Resource extraction and nationalization disputes (tin, gas, lithium)","Indigenous rights and political marginalization history","1970s authoritarian period and external influence concerns"]},
  "US_BR_BRAZIL": {"country":"Brazil","iso":"BR","pool":"$200,000,000,000","instruments":25,"issues":"Amazon, dictatorship, indigenous and Afro-Brazilian harms","anchors":["1964-1985 military dictatorship (National Truth Commission public record)","Operation Condor and regional repression","Amazon deforestation and indigenous land rights impacts"]},
  "US_BS_BAHAMAS": {"country":"Bahamas","iso":"BS","pool":"$15,000,000,000","instruments":25,"issues":"Tourism dependency, climate exposure, financial governance pressure","anchors":["Colonial trade and slavery legacy","Climate change and hurricane exposure","Offshore finance and external regulatory pressure"]},
  "US_BZ_BELIZE": {"country":"Belize","iso":"BZ","pool":"$3,000,000,000","instruments":25,"issues":"Territorial claim pressures, colonial legacy, climate","anchors":["British colonial extraction and land tenure legacy","Guatemala territorial claim and regional security pressures","Climate and coastal vulnerability"]},
  "US_CL_CHILE": {"country":"Chile","iso":"CL","pool":"$60,000,000,000","instruments":25,"issues":"Pinochet dictatorship, neoliberal restructuring, human rights","anchors":["1973 coup and Pinochet dictatorship (Rettig/Valech Commission public records)","Operation Condor participation","Economic shock therapy and social impacts"]},
  "US_CO_COLOMBIA": {"country":"Colombia","iso":"CO","pool":"$80,000,000,000","instruments":25,"issues":"Armed conflict, coca eradication impacts, displacement","anchors":["Decades-long armed conflict and civilian displacement","Plan Colombia and security cooperation impacts (public policy record)","Land dispossession and transitional justice processes"]},
  "US_CR_COSTA_RICA": {"country":"Costa Rica","iso":"CR","pool":"$25,000,000,000","instruments":25,"issues":"Environmental protection costs, regional security pressures","anchors":["Abolition of military and peace model","Environmental conservation and climate adaptation burden","Regional Contra-era security pressures (public historical record)"]},
  "US_DM_DOMINICA": {"country":"Dominica","iso":"DM","pool":"$2,000,000,000","instruments":25,"issues":"Climate, hurricane damage, small-island vulnerability","anchors":["Colonial plantation legacy","Hurricane Maria and climate resilience costs","Sovereign debt and recovery financing pressure"]},
  "US_DO_DOMINICAN_REPUBLIC": {"country":"Dominican Republic","iso":"DO","pool":"$30,000,000,000","instruments":25,"issues":"Haiti border harms, sugar labor, authoritarian legacy","anchors":["Trujillo dictatorship legacy (1930-1961)","1965 US intervention and civil conflict (public historical record)","Sugar industry labor and migration/human rights concerns"]},
  "US_EC_ECUADOR": {"country":"Ecuador","iso":"EC","pool":"$40,000,000,000","instruments":25,"issues":"Oil extraction, indigenous rights, debt","anchors":["Oil extraction and environmental harm in Amazon (public litigation record, incl. Chevron/Texaco disputes context)","Indigenous rights and territorial protection","Dollarization and external debt pressures"]},
  "US_GD_GRENADA": {"country":"Grenada","iso":"GD","pool":"$2,000,000,000","instruments":25,"issues":"US invasion 1983, climate vulnerability","anchors":["1983 US invasion (Operation Urgent Fury, public record)","Colonial legacy and small-island economic constraints","Climate vulnerability"]},
  "US_GT_GUATEMALA": {"country":"Guatemala","iso":"GT","pool":"$30,000,000,000","instruments":25,"issues":"1954 coup, genocide/civil war, indigenous harms","anchors":["1954 coup and subsequent instability (declassified public records)","Internal armed conflict and genocide findings (CEH public report)","Indigenous land and human rights harms"]},
  "US_GY_GUYANA": {"country":"Guyana","iso":"GY","pool":"$20,000,000,000","instruments":25,"issues":"Oil governance, border dispute, colonial legacy","anchors":["Colonial plantation and indenture legacy","Essequibo border dispute context","Oil boom governance and environmental risk"]},
  "US_HN_HONDURAS": {"country":"Honduras","iso":"HN","pool":"$15,000,000,000","instruments":25,"issues":"Coup, migration, labor and land conflicts","anchors":["2009 coup and political instability (public record)","Banana republic era corporate influence (historical public record)","Migration drivers and human rights concerns"]},
  "US_HT_HAITI": {"country":"Haiti","iso":"HT","pool":"$15,000,000,000","instruments":25,"issues":"Indemnity legacy, occupation, governance instability","anchors":["Independence debt/indemnity imposed by France (1825, public historical record)","1915-1934 US occupation (public historical record)","Disaster recovery and external governance interventions"]},
  "US_JM_JAMAICA": {"country":"Jamaica","iso":"JM","pool":"$20,000,000,000","instruments":25,"issues":"Reparations, debt, colonial extraction","anchors":["Slavery and plantation extraction legacy","Structural adjustment and debt burden (public record)","CARICOM reparations movement context"]},
  "US_KN_SAINT_KITTS_AND_NEVIS": {"country":"Saint Kitts and Nevis","iso":"KN","pool":"$2,000,000,000","instruments":25,"issues":"Colonial legacy, climate, economic vulnerability","anchors":["Sugar plantation slavery legacy","Climate and small-island vulnerability","Post-colonial economic transition"]},
  "US_LC_SAINT_LUCIA": {"country":"Saint Lucia","iso":"LC","pool":"$2,000,000,000","instruments":25,"issues":"Tourism dependency, climate, colonial legacy","anchors":["Colonial extraction legacy","Climate vulnerability and disaster recovery costs","Tourism dependency and external shocks"]},
  "US_MX_MEXICO": {"country":"Mexico","iso":"MX","pool":"$150,000,000,000","instruments":25,"issues":"Drug war cooperation impacts, NAFTA/USMCA pressures, migration","anchors":["1846-1848 war and territorial loss (Treaty of Guadalupe Hidalgo, public record)","Bracero program and labor exploitation concerns (historical public record)","Drug war/security cooperation and human rights impacts (public record)"]},
  "US_NI_NICARAGUA": {"country":"Nicaragua","iso":"NI","pool":"$15,000,000,000","instruments":25,"issues":"Contra war, intervention, sovereignty","anchors":["US military interventions and occupation era (early 20th century)","Contra war and ICJ Nicaragua v. US (1986) judgment context","Economic sanctions and sovereignty disputes"]},
  "US_PA_PANAMA": {"country":"Panama","iso":"PA","pool":"$25,000,000,000","instruments":25,"issues":"Canal, 1989 invasion, sovereignty","anchors":["Panama Canal construction/control and sovereignty history","1989 US invasion (Operation Just Cause, public record)","Financial hub and sanctions/external pressure issues"]},
  "US_PE_PERU": {"country":"Peru","iso":"PE","pool":"$50,000,000,000","instruments":25,"issues":"Internal conflict, extractivism, political instability","anchors":["1980-2000 internal conflict (CVR Truth and Reconciliation Commission public record)","Extractive industry and indigenous land impacts","Political instability and external economic pressure"]},
  "US_PR_PUERTO_RICO": {"country":"Puerto Rico","iso":"PR","pool":"$100,000,000,000","instruments":25,"issues":"Territorial status, PROMESA, disaster recovery","anchors":["1898 cession and territorial status (public legal record)","PROMESA/FOMB fiscal oversight (public record)","Hurricane Maria response and infrastructure recovery"]},
  "US_PY_PARAGUAY": {"country":"Paraguay","iso":"PY","pool":"$15,000,000,000","instruments":25,"issues":"Stroessner dictatorship, hydro governance, land inequality","anchors":["Stroessner dictatorship (1954-1989) and Operation Condor links (public record)","Itaipu/Yacyreta hydro governance and debt context","Land inequality and indigenous rights"]},
  "US_SR_SURINAME": {"country":"Suriname","iso":"SR","pool":"$10,000,000,000","instruments":25,"issues":"Bauxite extraction, coups, colonial legacy","anchors":["Colonial plantation and indenture legacy","Resource extraction (bauxite/gold) impacts","Political instability and post-colonial governance pressures"]},
  "US_SV_EL_SALVADOR": {"country":"El Salvador","iso":"SV","pool":"$15,000,000,000","instruments":25,"issues":"Civil war, migration, security policy impacts","anchors":["1980-1992 civil war and human rights abuses (UN Truth Commission public record)","US security assistance and conflict dynamics (public record)","Gang violence and migration drivers"]},
  "US_TT_TRINIDAD_AND_TOBAGO": {"country":"Trinidad and Tobago","iso":"TT","pool":"$30,000,000,000","instruments":25,"issues":"Oil/gas transition, colonial legacy, climate exposure","anchors":["Colonial plantation and indenture legacy","Oil/gas extraction and economic transition","Climate and coastal vulnerability"]},
  "US_UY_URUGUAY": {"country":"Uruguay","iso":"UY","pool":"$25,000,000,000","instruments":25,"issues":"Dictatorship legacy, financial stability pressures","anchors":["1973-1985 civic-military dictatorship (public record)","Operation Condor participation","Banking crisis and external economic pressures"]},
  "US_VC_SAINT_VINCENT_AND_THE_GRENADINES": {"country":"Saint Vincent and the Grenadines","iso":"VC","pool":"$2,000,000,000","instruments":25,"issues":"Volcano/climate vulnerability, colonial legacy","anchors":["La Soufriere eruptions and climate resilience costs","Colonial plantation legacy","Small-island economic vulnerability"]},
  "US_VE_VENEZUELA": {"country":"Venezuela","iso":"VE","pool":"$80,000,000,000","instruments":25,"issues":"Sanctions, oil, political intervention claims","anchors":["Oil nationalization/expropriation disputes (public record)","Sanctions and economic impacts (public policy record)","Political crisis and external intervention allegations (public record)"]},
}

def slug(name):
    parts=name.split('_')
    return f"latam-{parts[1].lower()}-" + "-".join(p.lower() for p in parts[2:]) + "-master-litigation"

def ensure(p: Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(content, encoding='utf-8', newline='\n')
        return True
    return False

def backup_if_exists(p: Path, country_dir: Path):
    if p.exists():
        bak_dir = country_dir / '99_Archives_and_Manifests' / 'pre_bolster_backup'
        bak_dir.mkdir(parents=True, exist_ok=True)
        bak = bak_dir / p.name
        if not bak.exists():
            bak.write_bytes(p.read_bytes())

_CURRENT_COUNTRY_DIR = None

def write(p: Path, content: str, country_dir: Path = None):
    global _CURRENT_COUNTRY_DIR
    if country_dir is None:
        country_dir = _CURRENT_COUNTRY_DIR
    p.parent.mkdir(parents=True, exist_ok=True)
    if country_dir is not None:
        backup_if_exists(p, country_dir)
    p.write_text(content, encoding='utf-8', newline='\n')

def sha256_file(p: Path):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def build_manifest(name, prof):
    s=slug(name)
    rows=[]
    for i in range(1, prof['instruments']+1):
        vid=f"{prof['iso']}-{i:03d}"
        anchor=prof['anchors'][(i-1)%len(prof['anchors'])]
        rows.append(f"| **{vid}** | {anchor} | United States / associated actors (to be evidentiary verified) | Historical/legal liability vector (pending evidentiary development) | {prof['pool']} pool allocation TBD | Federal / international / administrative forum TBD | `SCAFFOLDED` |")
    table='\n'.join(rows)
    return f"""# Master Armory Manifest: {prof['country']} Restitution Instruments

> **Repository:** `GlobalRestitutionAlliance/{s}`  
> **Release:** v1.1.0-scaffold  
> **Total Actionable Instruments:** {prof['instruments']} (`{prof['iso']}-001` through `{prof['iso']}-{prof['instruments']:03d}`)  
> **Target Restitution Pool:** **{prof['pool']} USD (planning scaffold; subject to evidentiary validation)**  
> **Status:** ACTIVE SCAFFOLD - COUNTRY-SPECIFIC EVIDENTIARY DEVELOPMENT REQUIRED

---

## 1. Instrumentation Inventory

| Instrument ID | Historical Anchor / Claim Vector | Target Entity / Counterparty | Asset Category & Enforcement Vector | Audited Pool | Primary Enforcement Forum | Status |
|:---|:---|:---|:---|:---|:---|:---|
{table}

---

## 2. Evidentiary Development Guardrails

- No fabricated citations, case numbers, or archival IDs.
- Every instrument must be upgraded with primary-source citations before filing use.
- All monetary figures remain planning estimates until supported by forensic/economic analysis.
- Use `Expansion_and_Audit_Log.md` to record evidentiary upgrades and verification events.
"""

def build_audit(name, prof):
    s=slug(name)
    return f"""# Expansion and Audit Log - {prof['country']}

| Date | Event | Scope | Status | Notes |
|---|---|---|---|---|
| {TODAY} | LATAM baseline bolstering | Directory scaffold, .github baseline, README uplift | COMPLETE | Cuba-template structural alignment applied; no fabricated claims added. |
| {TODAY} | Deep scaffold generation | Manifest, crosswalk, core legal docs, .antigravity baseline | COMPLETE | Country-specific anchors seeded from public high-level historical record; evidentiary verification pending. |

## Pending Verification
- Replace planning placeholders with primary-source citations.
- Validate forum selection, standing, sovereign immunity, and limitations defenses per instrument.
- Attach forensic valuation support to pool figures.
"""

def build_coc(name, prof):
    return f"""# Master Chain of Custody Log - {prof['country']}

## Integrity Protocol
- All evidentiary artifacts must be hashed (SHA-256) upon creation/modification.
- No fabricated citations or unverified archival references.
- Every legal claim requires source provenance before external filing.

## Log
| Date (UTC) | Artifact | Action | Hash | Actor | Notes |
|---|---|---|---|---|---|
| {TODAY} | Repository scaffold | Baseline bolstering | PENDING_REFRESH | OpenCode/Iceman | Run manifest/hash refresh after stabilization. |
"""

def build_crosswalk_csv(p: Path, prof, country_dir: Path):
    backup_if_exists(p, country_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['instrument_id','country','iso','anchor','claim_vector','forum_tbd','pool_planning','status','evidence_status'])
        for i in range(1, prof['instruments']+1):
            anchor=prof['anchors'][(i-1)%len(prof['anchors'])]
            w.writerow([f"{prof['iso']}-{i:03d}", prof['country'], prof['iso'], anchor, 'Pending evidentiary development', 'TBD', prof['pool'], 'SCAFFOLDED', 'PENDING_PRIMARY_SOURCE'])

def build_crosswalk_md(p: Path, prof, country_dir: Path):
    lines=[f"# {prof['country']} Master Restitution Crosswalk Dashboard", "", f"- **ISO:** {prof['iso']}", f"- **Planning Pool:** {prof['pool']} USD (subject to evidentiary validation)", f"- **Instruments:** {prof['instruments']}", "", "## Evidentiary Anchors (High-Level, Public Record)", ""]
    for a in prof['anchors']:
        lines.append(f"- {a}")
    lines += ["", "## Instrument Matrix", "", "| ID | Anchor | Status | Evidence |", "|---|---|---|---|"]
    for i in range(1, prof['instruments']+1):
        anchor=prof['anchors'][(i-1)%len(prof['anchors'])]
        lines.append(f"| {prof['iso']}-{i:03d} | {anchor} | SCAFFOLDED | PENDING_PRIMARY_SOURCE |")
    lines += ["", "## Guardrail", "No fabricated citations, docket numbers, or archive IDs. All entries require primary-source verification before filing use."]
    write(p, '\n'.join(lines)+'\n', country_dir)

def build_doc(p: Path, title: str, prof: dict, body: str, country_dir: Path):
    content=f"""# {title}

**Jurisdiction:** United States – {prof['country']} ({prof['iso']})  
**Generated:** {TODAY}  
**Status:** ACTIVE SCAFFOLD - EVIDENTIARY VERIFICATION REQUIRED

---

{body}

---

## Verification Guardrail
This document is a litigation/research scaffold. It contains no fabricated citations, docket numbers, or archival identifiers. All factual assertions, legal citations, and valuations must be verified against primary sources before external use.
"""
    write(p, content, country_dir)

def build_antigravity(country_dir: Path, name: str, prof: dict):
    global _CURRENT_COUNTRY_DIR
    _CURRENT_COUNTRY_DIR = country_dir
    ag = country_dir / '.antigravity'
    # project.yaml
    write(ag/'project.yaml', f"""project:
  id: LATAM-{prof['iso']}-MASTER-LITIGATION
  name: "US-{prof['iso']} {prof['country']} Master Litigation"
  version: 1.1.0
  status: ACTIVE_SCAFFOLD
  root_directory: W:\\Legal\\LATIN_AMERICA\\{name}
  target_sovereign: United States Government and associated actors (claims pending evidentiary verification)
  temporal_scope: "Historical to Present (country-specific; to be verified)"
  modules:
    agents: agents/agent-registry.yaml
    skills: skills/skill-registry.yaml
    tools: tools/tool-registry.yaml
    workflows: workflows/workflow-registry.yaml
    templates: templates/template-registry.yaml
    rules: rules/
""")
    # registries
    write(ag/'agents/agent-registry.yaml', f"""registry: Agent Registry
version: 1.0.0
agents:
  - id: agent-{prof['iso'].lower()}-lead-counsel
    file: agent-lead-counsel.yaml
    status: ACTIVE
    role: Lead Strategic Counsel & Campaign Coordination
  - id: agent-{prof['iso'].lower()}-archival-sentinel
    file: agent-archival-sentinel.yaml
    status: ACTIVE
    role: Archival Retrieval, Evidence Authentication & Chain of Custody
  - id: agent-{prof['iso'].lower()}-procedural-blacksmith
    file: agent-procedural-blacksmith.yaml
    status: ACTIVE
    role: Pleadings, Motions, Procedural Compliance
  - id: agent-{prof['iso'].lower()}-tribunals-envoy
    file: agent-tribunals-envoy.yaml
    status: ACTIVE
    role: International Tribunals, Exequatur, Transnational Enforcement
""")
    write(ag/'skills/skill-registry.yaml', f"""registry: Skill Registry
version: 1.0.0
skills:
  - id: {prof['iso'].lower()}-historical-timeline-audit
    file: historical-timeline-audit.yaml
    status: ACTIVE
  - id: {prof['iso'].lower()}-evidentiary-crosswalk-build
    file: evidentiary-crosswalk-build.yaml
    status: ACTIVE
  - id: {prof['iso'].lower()}-federal-complaint-drafting
    file: federal-complaint-drafting.yaml
    status: ACTIVE
  - id: {prof['iso'].lower()}-international-tribunal-submission
    file: international-tribunal-submission.yaml
    status: ACTIVE
  - id: {prof['iso'].lower()}-qsf-restitution-execution
    file: qsf-restitution-execution.yaml
    status: ACTIVE
""")
    write(ag/'tools/tool-registry.yaml', """registry: Tool Registry
version: 1.0.0
tools:
  - id: cross-nation-toolkit
    file: cross_nation_toolkit_manifest.yaml
    status: ACTIVE
""")
    write(ag/'workflows/workflow-registry.yaml', """registry: Workflow Registry
version: 1.0.0
workflows:
  - id: autonomous-expansion
    file: autonomous-expansion.yaml
    status: ACTIVE
  - id: evidentiary-harvest
    file: evidentiary-harvest.yaml
    status: ACTIVE
  - id: red-team-audit
    file: red-team-audit.yaml
    status: ACTIVE
""")
    write(ag/'templates/template-registry.yaml', """registry: Template Registry
version: 1.0.0
templates:
  - federal-complaint.yaml
  - memorandum-of-law.yaml
  - motion-template.yaml
  - discovery-matrix.yaml
  - international-petition.yaml
""")
    # minimal agents/skills/workflows/templates/rules
    for aid, role in [
        ('agent-lead-counsel','Lead Strategic Counsel & Campaign Coordination'),
        ('agent-archival-sentinel','Archival Retrieval, Evidence Authentication & Chain of Custody'),
        ('agent-procedural-blacksmith','Pleadings, Motions, Procedural Compliance'),
        ('agent-tribunals-envoy','International Tribunals, Exequatur, Transnational Enforcement'),
    ]:
        ensure(ag/f'agents/{aid}.yaml', f"agent:\n  id: {aid}\n  jurisdiction: {prof['country']}\n  status: ACTIVE\n  role: {role}\n  guardrails:\n    - no_fabricated_citations\n    - primary_source_verification_required\n")
    for sid in ['historical-timeline-audit','evidentiary-crosswalk-build','federal-complaint-drafting','international-tribunal-submission','qsf-restitution-execution']:
        ensure(ag/f'skills/{sid}.yaml', f"skill:\n  id: {sid}\n  jurisdiction: {prof['country']}\n  status: ACTIVE\n  guardrails:\n    - no_fabricated_citations\n    - primary_source_verification_required\n")
    for wf in ['autonomous-expansion','evidentiary-harvest','red-team-audit','deep-forge-pipeline','international-dual-track']:
        ensure(ag/f'workflows/{wf}.yaml', f"workflow:\n  id: {wf}\n  jurisdiction: {prof['country']}\n  status: ACTIVE\n  steps:\n    - inspect\n    - verify\n    - draft\n    - audit\n")
    for tpl in ['federal-complaint','memorandum-of-law','motion-template','discovery-matrix','expert-affidavit','international-petition']:
        ensure(ag/f'templates/{tpl}.yaml', f"template:\n  id: {tpl}\n  jurisdiction: {prof['country']}\n  status: ACTIVE\n")
    for rule in ['engagement-rules','escalation-protocols','ethical-guardrails']:
        ensure(ag/f'rules/{rule}.yaml', f"rules:\n  id: {rule}\n  jurisdiction: {prof['country']}\n  status: ACTIVE\n  - no_fabricated_citations\n  - primary_source_verification_required\n  - preserve_existing_evidence\n")
    # knowledge
    anchors = '\n'.join([f"  - \"{a}\"" for a in prof['anchors']])
    ensure(ag/'knowledge/historical-timeline.yaml', f"timeline:\n  jurisdiction: {prof['country']}\n  iso: {prof['iso']}\n  anchors:\n{anchors}\n  note: High-level public-record anchors only; verify before filing.\n")
    ensure(ag/'knowledge/legal-precedents.yaml', f"precedents:\n  jurisdiction: {prof['country']}\n  items: []\n  note: Add verified precedents only; no fabricated citations.\n")
    vec = ag/'knowledge/vector-index/vectors-0001-0100.yaml'
    if not vec.exists():
        lines=[f"vector_index:\n  jurisdiction: {prof['country']}\n  iso: {prof['iso']}\n  vectors:"]
        for i in range(1, prof['instruments']+1):
            anchor=prof['anchors'][(i-1)%len(prof['anchors'])]
            lines.append(f"    - vector_id: \"{prof['iso']}-{i:03d}\"\n      anchor: \"{anchor}\"\n      status: SCAFFOLDED\n      evidence_status: PENDING_PRIMARY_SOURCE")
        vec.write_text('\n'.join(lines)+'\n', encoding='utf-8', newline='\n')
    ensure(ag/'tools/cross_nation_toolkit_manifest.yaml', "toolkit:\n  status: ACTIVE\n  note: Use shared cross-nation tools; verify jurisdiction-specific adaptations.\n")

def build_country(name, prof):
    cdir = ROOT/name
    # root docs
    write(cdir/'Master_Armory_Manifest.md', build_manifest(name, prof), cdir)
    write(cdir/'Expansion_and_Audit_Log.md', build_audit(name, prof), cdir)
    write(cdir/'Master_Chain_of_Custody_Log.md', build_coc(name, prof), cdir)
    # knowledge base
    build_crosswalk_csv(cdir/'00_Master_Knowledge_Base'/f"Master_{name}_Restitution_Crosswalk_Matrix.csv", prof, cdir)
    build_crosswalk_md(cdir/'00_Master_Knowledge_Base'/f"Master_{name}_Restitution_Crosswalk_Dashboard.md", prof, cdir)
    build_doc(cdir/'00_Master_Knowledge_Base'/'executive_summary_dossier.md', f"Executive Summary Dossier - {prof['country']}", prof,
              f"""## Mission
Establish a verifiable, country-specific restitution litigation scaffold for US–{prof['country']} claims, aligned to Cuba-template structure.

## Key Issues
{prof['issues']}

## High-Level Anchors
""" + '\n'.join([f"- {a}" for a in prof['anchors']]) + f"""

## Planning Metrics
- Instruments: {prof['instruments']}
- Planning Pool: {prof['pool']} USD (subject to evidentiary validation)

## Immediate Next Actions
1. Attach primary-source citations to each instrument.
2. Validate legal theories, fora, and procedural requirements.
3. Build forensic valuation and damages model per instrument.""", cdir)
    # core legal docs
    build_doc(cdir/'01_Pleadings_and_Complaints'/f"master_federal_court_complaint_{prof['iso'].lower()}_v1.md", f"Master Federal Court Complaint - {prof['country']} (Scaffold)", prof,
              """## Parties, Jurisdiction, Venue
To be completed with verified claimant classes, defendants, jurisdictional bases, and venue analysis.

## Factual Allegations
Populate with verified, source-cited historical and contemporary facts. Do not fabricate events, citations, or damages.

## Causes of Action
To be selected after legal verification (e.g., statutory, constitutional, tort, international law domestication pathways as applicable).

## Relief Requested
Declaratory relief, damages/restitution accounting, equitable remedies, and enforcement mechanisms - all subject to evidentiary and legal validation.""", cdir)
    build_doc(cdir/'02_Discovery_and_Evidentiary'/f"discovery_plan_{prof['iso'].lower()}_v1.md", f"Discovery & Evidentiary Plan - {prof['country']}", prof,
              """## Discovery Priorities
- Identify custodians, archives, agencies, and corporate records.
- Issue preservation notices/litigation holds where appropriate.
- Map each instrument to documentary, testimonial, and expert evidence.

## Evidence Classes
- Primary government records (declassified/public archives)
- Treaty/diplomatic records
- Financial/transactional records
- Expert reports (historical, economic, forensic)""", cdir)
    build_doc(cdir/'03_Motions_and_Briefs'/f"motions_and_briefs_index_{prof['iso'].lower()}_v1.md", f"Motions & Briefs Index - {prof['country']}", prof,
              """## Planned Motions/Briefs
- Motion for preservation / anti-spoliation
- Motion for judicial notice / treaty recognition (as applicable)
- Opposition templates for immunity, standing, limitations, political question defenses
- Summary judgment / evidentiary motions (post-discovery)""", cdir)
    build_doc(cdir/'04_International_Tribunals'/f"international_tribunal_strategy_{prof['iso'].lower()}_v1.md", f"International Tribunal Strategy - {prof['country']}", prof,
              """## Forum Assessment
Evaluate ICJ, IACHR, UN treaty bodies, UNCITRAL/PCA, and domestic exequatur pathways based on verified facts and standing.

## Filing Readiness Checklist
- Verified claimant/standing
- Exhaustion/admissibility analysis
- Evidence authentication
- Remedies/enforcement pathway""", cdir)
    build_doc(cdir/'05_Strategic_Doctrines_and_Red_Team'/f"red_team_doctrine_{prof['iso'].lower()}_v1.md", f"Strategic Doctrine & Red Team - {prof['country']}", prof,
              """## Adversarial Stress Tests
- Sovereign immunity and act-of-state defenses
- Statute of limitations / prescription
- Causation and damages attribution
- Political question / comity
- Evidence authenticity and chain-of-custody challenges""", cdir)
    build_doc(cdir/'06_Trial_and_Appellate_Prep'/f"trial_appellate_prep_{prof['iso'].lower()}_v1.md", f"Trial & Appellate Preparation - {prof['country']}", prof,
              """## Trial Prep
- Witness/expert matrix
- Exhibit authentication plan
- Verdict/ruling theory mapping

## Appellate Prep
- Preservation checklist
- Issue framing and standard-of-review matrix
- Record build plan""", cdir)
    build_doc(cdir/'07_Enforcement_and_Restitution'/f"enforcement_restitution_plan_{prof['iso'].lower()}_v1.md", f"Enforcement & Restitution Plan - {prof['country']}", prof,
              """## Enforcement Pathways
- Domestic judgment enforcement
- Foreign recognition/exequatur
- Asset tracing and recovery
- Qualified Settlement Fund / restitution trust administration (jurisdiction-specific, legally verified)""", cdir)
    # antigravity
    build_antigravity(cdir, name, prof)
    global _CURRENT_COUNTRY_DIR
    _CURRENT_COUNTRY_DIR = None

def main():
    count=0
    for name, prof in PROFILES.items():
        if name == 'US_CU_CUBA':
            continue
        cdir=ROOT/name
        if not cdir.exists():
            continue
        build_country(name, prof)
        count+=1
        print('BUILT', name)
    print('TOTAL', count)

if __name__=='__main__':
    main()
