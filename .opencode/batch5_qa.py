import csv, json, os, subprocess, re, hashlib
from pathlib import Path

ROOT = Path(r"W:\Legal")

LATAM_W2 = [
    ROOT/'LATIN_AMERICA'/'US_AG_ANTIGUA_AND_BARBUDA',ROOT/'LATIN_AMERICA'/'US_AR_ARGENTINA',ROOT/'LATIN_AMERICA'/'US_BB_BARBADOS',ROOT/'LATIN_AMERICA'/'US_BO_BOLIVIA',
    ROOT/'LATIN_AMERICA'/'US_BR_BRAZIL',ROOT/'LATIN_AMERICA'/'US_BS_BAHAMAS',ROOT/'LATIN_AMERICA'/'US_BZ_BELIZE',ROOT/'LATIN_AMERICA'/'US_CL_CHILE',
]
LATAM_W3 = [
    ROOT/'LATIN_AMERICA'/'US_CO_COLOMBIA',ROOT/'LATIN_AMERICA'/'US_CR_COSTA_RICA',ROOT/'LATIN_AMERICA'/'US_DM_DOMINICA',ROOT/'LATIN_AMERICA'/'US_DO_DOMINICAN_REPUBLIC',
    ROOT/'LATIN_AMERICA'/'US_EC_ECUADOR',ROOT/'LATIN_AMERICA'/'US_GD_GRENADA',ROOT/'LATIN_AMERICA'/'US_GY_GUYANA',ROOT/'LATIN_AMERICA'/'US_JM_JAMAICA',
]
LATAM_W4 = [
    ROOT/'LATIN_AMERICA'/'US_KN_SAINT_KITTS_AND_NEVIS',ROOT/'LATIN_AMERICA'/'US_LC_SAINT_LUCIA',ROOT/'LATIN_AMERICA'/'US_PE_PERU',ROOT/'LATIN_AMERICA'/'US_PY_PARAGUAY',
    ROOT/'LATIN_AMERICA'/'US_SR_SURINAME',ROOT/'LATIN_AMERICA'/'US_TT_TRINIDAD_AND_TOBAGO',ROOT/'LATIN_AMERICA'/'US_UY_URUGUAY',ROOT/'LATIN_AMERICA'/'US_VC_SAINT_VINCENT_AND_THE_GRENADINES',
]
LATAM_W5 = [
    ROOT/'LATIN_AMERICA'/'US_VE_VENEZUELA',
]
TURTLE8 = [
    ROOT/"US_TURTLE_ISLAND_NATIVES"/"EASTERN_OKLAHOMA"/"US_OK_CHEROKEE_NATION",
    ROOT/"US_TURTLE_ISLAND_NATIVES"/"GREAT_PLAINS"/"US_SD_OGLALA_SIOUX_TRIBE",
    ROOT/"US_TURTLE_ISLAND_NATIVES"/"EASTERN_OKLAHOMA"/"US_OK_THE_CHOCTAW_NATION_OF_OKLAHOMA",
    ROOT/"US_TURTLE_ISLAND_NATIVES"/"EASTERN_OKLAHOMA"/"US_OK_THE_SEMINOLE_NATION_OF_OKLAHOMA",
    ROOT/"US_TURTLE_ISLAND_NATIVES"/"WESTERN"/"US_AZ_HOPI_TRIBE_OF_ARIZONA",
    ROOT/"US_TURTLE_ISLAND_NATIVES"/"GREAT_PLAINS"/"US_SD_ROSEBUD_SIOUX_TRIBE_OF_THE_ROSEBUD_INDIA",
    ROOT/"US_TURTLE_ISLAND_NATIVES"/"GREAT_PLAINS"/"US_ND_STANDING_ROCK_SIOUX_TRIBE_OF_NORTH_SOUTH",
    ROOT/"US_TURTLE_ISLAND_NATIVES"/"ROCKY_MOUNTAIN"/"US_MT_BLACKFEET_TRIBE_OF_THE_BLACKFEET_INDIAN_",
]

ASIA8_W2 = [
    ROOT/'ASIA'/'US_AE_UNITED_ARAB_EMIRATES',
    ROOT/'ASIA'/'US_AM_ARMENIA',
    ROOT/'ASIA'/'US_AZ_AZERBAIJAN',
    ROOT/'ASIA'/'US_BD_BANGLADESH',
    ROOT/'ASIA'/'US_BH_BAHRAIN',
    ROOT/'ASIA'/'US_BN_BRUNEI',
    ROOT/'ASIA'/'US_BT_BHUTAN',
    ROOT/'ASIA'/'US_CN_CHINA',
]
ASIA8_W3 = [
    ROOT/'ASIA'/'US_CY_CYPRUS',
    ROOT/'ASIA'/'US_GE_GEORGIA',
    ROOT/'ASIA'/'US_IN_INDIA',
    ROOT/'ASIA'/'US_JO_JORDAN',
    ROOT/'ASIA'/'US_JP_JAPAN',
    ROOT/'ASIA'/'US_KG_KYRGYZSTAN',
    ROOT/'ASIA'/'US_KP_NORTH_KOREA',
    ROOT/'ASIA'/'US_KW_KUWAIT',
]
ASIA8_W4 = [
    ROOT/'ASIA'/'US_KZ_KAZAKHSTAN',
    ROOT/'ASIA'/'US_LA_LAOS',
    ROOT/'ASIA'/'US_LB_LEBANON',
    ROOT/'ASIA'/'US_LK_SRI_LANKA',
    ROOT/'ASIA'/'US_MM_MYANMAR',
    ROOT/'ASIA'/'US_MN_MONGOLIA',
    ROOT/'ASIA'/'US_MV_MALDIVES',
    ROOT/'ASIA'/'US_MY_MALAYSIA',
]
ASIA8_W5 = [
    ROOT/'ASIA'/'US_NP_NEPAL',
    ROOT/'ASIA'/'US_OM_OMAN',
    ROOT/'ASIA'/'US_PK_PAKISTAN',
    ROOT/'ASIA'/'US_PS_PALESTINE',
    ROOT/'ASIA'/'US_QA_QATAR',
    ROOT/'ASIA'/'US_SA_SAUDI_ARABIA',
    ROOT/'ASIA'/'US_SG_SINGAPORE',
    ROOT/'ASIA'/'US_SY_SYRIA',
]
ASIA8_W6 = [
    ROOT/'ASIA'/'US_TH_THAILAND',
    ROOT/'ASIA'/'US_TJ_TAJIKISTAN',
    ROOT/'ASIA'/'US_TL_TIMOR_LESTE',
    ROOT/'ASIA'/'US_TM_TURKMENISTAN',
    ROOT/'ASIA'/'US_TR_TURKEY',
    ROOT/'ASIA'/'US_TW_TAIWAN',
    ROOT/'ASIA'/'US_UZ_UZBEKISTAN',
    ROOT/'ASIA'/'US_YE_YEMEN',
]
LATAM8 = [
    ROOT/"LATIN_AMERICA"/"US_MX_MEXICO",
    ROOT/"LATIN_AMERICA"/"US_GT_GUATEMALA",
    ROOT/"LATIN_AMERICA"/"US_HN_HONDURAS",
    ROOT/"LATIN_AMERICA"/"US_SV_EL_SALVADOR",
    ROOT/"LATIN_AMERICA"/"US_NI_NICARAGUA",
    ROOT/"LATIN_AMERICA"/"US_PA_PANAMA",
    ROOT/"LATIN_AMERICA"/"US_HT_HAITI",
    ROOT/"LATIN_AMERICA"/"US_PR_PUERTO_RICO",
]

ASIA8 = [
    ROOT/"ASIA"/"US_VN_VIETNAM",
    ROOT/"ASIA"/"US_PH_PHILIPPINES",
    ROOT/"ASIA"/"US_ID_INDONESIA",
    ROOT/"ASIA"/"US_KR_SOUTH_KOREA",
    ROOT/"ASIA"/"US_IQ_IRAQ",
    ROOT/"ASIA"/"US_AF_AFGHANISTAN",
    ROOT/"ASIA"/"US_IR_IRAN",
    ROOT/"ASIA"/"US_KH_CAMBODIA",
]

PACIFIC8 = [
    ROOT/"PACIFIC"/"US_AS_AMERICAN_SAMOA",
    ROOT/"PACIFIC"/"US_CK_COOK_ISLANDS",
    ROOT/"PACIFIC"/"US_FJ_FIJI",
    ROOT/"PACIFIC"/"US_FM_MICRONESIA_FSM",
    ROOT/"PACIFIC"/"US_GU_GUAM",
    ROOT/"PACIFIC"/"US_KI_KIRIBATI",
    ROOT/"PACIFIC"/"US_MP_NORTHERN_MARIANA_ISLANDS",
    ROOT/"PACIFIC"/"US_NR_NAURU",
]


def find_repos():
    repos = []
    for base in ["AFRICA", "ASIA", "PACIFIC", "US_DOMESTIC_VICTIMS"]:
        p = ROOT / base
        if p.exists():
            for d in p.iterdir():
                if d.is_dir() and (d / ".git").exists():
                    repos.append(d)
    ti = ROOT / "US_TURTLE_ISLAND_NATIVES"
    if ti.exists():
        for gd in ti.rglob(".git"):
            if gd.is_dir():
                repos.append(gd.parent)
    for n in ["US_AFRICAN_AMERICAN_REPARATIONS"]:
        p = ROOT / n
        if p.exists() and (p / ".git").exists():
            repos.append(p)
        if p.exists():
            for d in p.iterdir():
                if d.is_dir() and (d / ".git").exists():
                    repos.append(d)
    # include explicit wave targets
    for d in PACIFIC8 + ASIA8 + ASIA8_W2 + ASIA8_W3 + ASIA8_W4 + ASIA8_W5 + ASIA8_W6 + LATAM8 + LATAM_W2 + LATAM_W3 + LATAM_W4 + LATAM_W5 + TURTLE8:
        if d.exists():
            repos.append(d)
    seen = set()
    out = []
    for r in repos:
        k = str(r).lower()
        if k not in seen:
            seen.add(k)
            out.append(r)
    return sorted(out)


def sha256_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<16), b''):
            h.update(chunk)
    return h.hexdigest()


def check(repo):
    issues = []
    # legacy manifest
    if (repo/"VERIFICATION_KEYS/sha256_manifest.txt").exists() or (repo/".git").exists():
        if not (repo/"VERIFICATION_KEYS/sha256_manifest.txt").exists() and (repo/".git").exists():
            # some git repos may not have it; keep original strictness only when expected? original: missing_manifest
            issues.append("missing_manifest")
    # new manifest layout
    mcsv = repo/"99_Archives_and_Manifests"/"MANIFEST_SHA256.csv"
    if mcsv.exists():
        with mcsv.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                rel=(row.get('path') or '').replace('\\','/')
                if rel == '99_Archives_and_Manifests/MANIFEST_SHA256.csv':
                    issues.append('manifest_self_entry_present')
                    break
                fp = repo/rel
                if not fp.exists():
                    issues.append('manifest_missing_file')
                    break
                if fp.is_file():
                    try:
                        if sha256_file(fp) != (row.get('sha256') or ''):
                            issues.append('manifest_hash_mismatch')
                            break
                    except Exception:
                        issues.append('manifest_hash_error')
                        break
    # citation index: no VERIFIED, required fields present for PACIFIC8-like layout
    for ci in [repo/"03_Evidentiary_Exhibits/CITATION_INDEX.csv", repo/"99_Archives_and_Manifests/CITATION_INDEX.csv"]:
        if ci.exists():
            with ci.open("r", encoding="utf-8", newline="") as f:
                reader=csv.DictReader(f)
                fields=set(reader.fieldnames or [])
                # enforce new schema when repo has adopted it (manifest or any new field present) or is an active wave target
                is_wave_target = repo in set(PACIFIC8+ASIA8+ASIA8_W2+ASIA8_W3+ASIA8_W4+ASIA8_W5+ASIA8_W6+LATAM8+LATAM_W2+LATAM_W3+LATAM_W4+LATAM_W5+TURTLE8)
                has_new_schema = mcsv.exists() or any(f in fields for f in ["verification_status","verification_rule","quality_flag","substantive","capture_access","provenance"])
                if is_wave_target or has_new_schema:
                    for req in ["verification_status","verification_rule","legal_review_status","quality_flag","substantive"]:
                        if req not in fields:
                            issues.append(f"citation_missing_field:{req}")
                            break
                for row in reader:
                    vs=(row.get("verification_status") or "").strip().upper()
                    lrs=(row.get("legal_review_status") or "").strip().upper()
                    if vs == "VERIFIED" or lrs == "VERIFIED":
                        issues.append("verified_citation_without_gate")
                        break
                    qf=(row.get('quality_flag') or '')
                    sub=(row.get('substantive') or '').strip().lower()
                    local=(row.get('local_artifact') or row.get('local_path') or '').strip()
                    sha=(row.get('sha256') or '').strip()
                    if (qf.startswith('NO_CAPTURE') or qf.startswith('NOT_SUBSTANTIVE')) and sub not in ('false','0'):
                        issues.append('nocapture_substantive_not_false')
                        break
                    # artifact-backed rows should have explicit substantive and basic provenance fields (enforced for wave targets/new-layout repos)
                    if (is_wave_target or mcsv.exists()) and local and sha and not qf.startswith('NO_CAPTURE') and not qf.startswith('NOT_SUBSTANTIVE'):
                        if sub not in ('true','1','false','0'):
                            issues.append('artifact_substantive_empty')
                            break
                        if not (row.get('provenance') or '').strip():
                            issues.append('artifact_provenance_empty')
                            break
                        if not (row.get('capture_access') or '').strip():
                            issues.append('artifact_capture_access_empty')
                            break
                if "verified_citation_without_gate" in issues or 'nocapture_substantive_not_false' in issues:
                    break
    # valuation workbook legacy
    wb = repo/"00_Master_Knowledge_Base/VALUATION_WORKBOOK.csv"
    if wb.exists():
        with wb.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                vs = (row.get("verification_status") or "").strip().upper()
                for k in ["low", "base", "high", "baseline_amount"]:
                    v = (row.get(k) or "").strip()
                    if v and v.upper() != "TBD":
                        if re.fullmatch(r"[0-9,.\-]+", v):
                            if vs == "VERIFIED" and not (row.get("reviewer") or "").strip():
                                issues.append("verified_valuation_missing_reviewer")
                                break
                if "verified_valuation_missing_reviewer" in issues:
                    break
    # valuation worksheet canonical checks
    ws = repo/"00_Master_Knowledge_Base"/"VALUATION_WORKSHEET.csv"
    if ws.exists():
        with ws.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                for k in ["low_usd","base_usd","high_usd"]:
                    v=(row.get(k) or '').strip()
                    if v and v.upper() != 'TBD':
                        issues.append('valuation_not_tbd'); break
                if (row.get('valuation_status') or '').strip().upper() not in ('','TBD'):
                    issues.append('valuation_status_not_tbd')
                if issues: break
    # vector registry flags
    vr = repo/"99_Archives_and_Manifests"/"claim_vector_registry_3000.json"
    if vr.exists():
        try:
            obj=json.loads(vr.read_text(encoding='utf-8'))
            vecs=obj if isinstance(obj,list) else (obj.get('vectors') or obj.get('claims') or obj.get('items') or obj.get('registry') or [])
            for v in vecs:
                if not isinstance(v,dict): continue
                if v.get('valuation_status')!='TBD': issues.append('vector_valuation_not_tbd'); break
                if v.get('evidence_mapping_status') not in ('AUTO_CANDIDATE_PENDING_REVIEW','PENDING_EVIDENCE_MAPPING_REVIEW'):
                    issues.append('vector_mapping_status_bad'); break
                if v.get('review_status')!='PENDING_LEGAL_REVIEW': issues.append('vector_review_status_bad'); break
        except Exception as e:
            issues.append(f'vector_read_error:{e}')
    # dedupe
    dedup=[]; seen=set()
    for i in issues:
        if i not in seen: seen.add(i); dedup.append(i)
    return dedup


def main():
    repos = find_repos()
    bad = []
    for r in repos:
        try:
            iss = check(r)
            if iss:
                bad.append((r.name, iss))
        except Exception as e:
            bad.append((r.name, [f"error:{e}"]))
    print(f"CHECKED {len(repos)}")
    print(f"ISSUES {len(bad)}")
    for n, iss in bad[:50]:
        print(n, ";".join(iss))
    out = ROOT / ".opencode/batch5_qa_report.txt"
    with out.open("w", encoding="utf-8") as f:
        f.write(f"CHECKED {len(repos)}\nISSUES {len(bad)}\n")
        for n, iss in bad:
            f.write(f"{n}\t{';'.join(iss)}\n")
    print(f"REPORT {out}")


if __name__ == "__main__":
    main()
