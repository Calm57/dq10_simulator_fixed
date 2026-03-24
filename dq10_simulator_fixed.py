import streamlit as st
import math

# ============================================================
# DATA MASTER
# ============================================================

# 形式: [倍率(float/list), 準備s, 硬直s, CTs, 上限, 特技固定値, 特技補正%, 属性]
DATA_MAP = {
    "武闘家": {
        "ツメ": {
            "タイガークロー":           [[1.7, 1.65, 1.6], 0.6, 1.8, 0, 1999, 0, 0, "無"],
            "ライガークラッシュ(CT)":   [[3.2, 3.15, 3.1, 3.05, 3.05], 1.0, 2.5, 65, 9999, 0, 0, "無"],
            "ゴッドスマッシュ(CT)":     [[1.0], 0.7, 1.9, 60, 9999, 0, 0, "光"],
            "打成一片(CT)":             [[3.4], 0.8, 1.0, 60, 9999, 0, 0, "無"],
        },
        "ヤリ": {
            "一閃突き・改":             [[2.25], 1.0, 1.5, 0, 3999, 0, 0, "無"],
            "さみだれ突き(CT)":         [[0.8]*4, 0.7, 2.0, 45, 1999, 5, 0, "無"],
            "超さみだれ突き(CT)":       [[0.8]*5, 1.2, 3.8, 80, 1999, 5, 0, "無"],
        },
        "棍": {
            "氷結らんげき・改":         [[0.55]*4, 0.0, 2.8, 0, 1999, 5, 0, "氷"],
            "豪雪乱舞(CT)":             [[0.8]*5, 1.4, 3.1, 80, 1999, 5, 0, "氷"],
        },
    },
    "戦士": {
        "片手剣": {
            "はやぶさ斬り":             [[1.0, 1.0], 1.0, 1.5, 0, 1999, 0, 0, "無"],
            "超はやぶさ斬り(CT)":       [[0.75]*4, 1.5, 2.1, 45, 1999, 0, 0, "無"],
            "不死鳥天舞(CT)":           [[0.9]*4, 1.8, 2.3, 75, 1999, 0, 0, "無"],
            "アルテマソード(CT)":       [[4.5], 1.0, 2.4, 60, 9999, 0, 0, "無"],
        },
        "両手剣": {
            "ブレイブスラッシュ":       [[3.0], 0.0, 2.6, 0, 3999, 0, 0, "無"],
            "全身全霊斬り(CT)":         [[4.0], 1.5, 3.0, 60, 9999, 0, 0, "無"],
        },
        "オノ": {
            "かぶと割り":               [[1.5], 0.5, 2.6, 0, 3999, 0, 0, "無"],
            "真・オノむそう(CT)":       [[3.2], 3.0, 1.8, 60, 1999, 0, 0, "無"],
        },
    },
    "バト": {
        "片手剣": {
            "天下無双":                 [[0.9]*6, 1.5, 3.2, 0, 1999, 0, 0, "無"],
            "古今無双(CT)":             [[1.75]*4, 0.9, 3.0, 60, 9999, 0, 0, "無"],
            "ラッシュバーン(CT)":       [[4.7]*4, 1.2, 2.9, 90, 9999, 0, 0, "無"],
            "はやぶさ斬り":             [[1.0, 1.0], 1.0, 1.5, 0, 1999, 0, 0, "無"],
            "超はやぶさ斬り(CT)":       [[0.75]*4, 1.5, 2.1, 45, 1999, 0, 0, "無"],
            "不死鳥天舞(CT)":           [[0.9]*4, 1.8, 2.3, 75, 1999, 0, 0, "無"],
            "アルテマソード(CT)":       [[4.5], 1.0, 2.4, 60, 9999, 0, 0, "無"],
        },
        "両手剣": {
            "ブレイブスラッシュ":       [[3.0], 0.0, 2.6, 0, 3999, 0, 0, "無"],
            "全身全霊斬り(CT)":         [[4.0], 1.5, 3.0, 60, 9999, 0, 0, "無"],
            "はやぶさ斬り":             [[1.0, 1.0], 1.0, 1.5, 0, 1999, 0, 0, "無"],
            "超はやぶさ斬り(CT)":       [[0.75]*4, 1.5, 2.1, 45, 1999, 0, 0, "無"],
            "不死鳥天舞(CT)":           [[0.9]*4, 1.8, 2.3, 75, 1999, 0, 0, "無"],
            "アルテマソード(CT)":       [[4.5], 1.0, 2.4, 60, 9999, 0, 0, "無"],
        },
        "ハンマー": {
            "ランドインパクト":         [[1.8], 2.5, 1.7, 0, 1999, 0, 0, "土"],
            "アースクラッシュ(CT)":     [[3.5], 1.9, 1.9, 60, 2999, 0, 0, "土"],
        },
    },
    "パラ": {
        "ヤリ": {
            "さみだれ突き・零":         [[1.2]*4, 0.7, 2.0, 0, 1999, 10, 0, "無"],
            "超さみだれ突き(CT)":       [[0.8]*5, 1.2, 3.8, 80, 1999, 5, 0, "無"],
        },
        "片手剣": {
            "はやぶさ斬り":             [[1.0, 1.0], 1.0, 1.5, 0, 1999, 0, 0, "無"],
            "超はやぶさ斬り(CT)":       [[0.75]*4, 1.5, 2.1, 45, 1999, 0, 0, "無"],
        },
    },
    "レン": {
        "ツメ": {
            "タイガークロー":           [[1.3]*3, 1.0, 1.8, 0, 1999, 0, 0, "無"],
            "フェンリルアタック(CT)":   [[1.5]*4, 1.6, 2.9, 60, 1999, 0, 0, "無"],
            "ケルベロスロンド(CT)":     [[2.0]*3, 2.0, 3.6, 110, 1999, 0, 0, "無"],
        },
        "ブメ": {
            "レボルスライサー(CT)":     [[5.0], 1.0, 1.0, 90, 9999, 0, 0, "無"],
        },
    },
    "まもの": {
        "ツメ": {
            "タイガークロー":           [[1.3]*3, 1.0, 1.8, 0, 1999, 0, 0, "無"],
        },
        "ムチ": {
            "双竜打ち":                 [[2.0, 2.0], 1.2, 2.8, 0, 1999, 0, 0, "無"],
            "極竜打ち(CT)":             [[1.6]*3, 1.2, 3.3, 50, 9999, 0, 0, "無"],
            "悶絶全方打ち(CT)":         [[5.0], 1.7, 2.6, 120, 9999, 0, 0, "無"],
            "ビーストファング(CT)":     [[2.0]*4, 0.0, 2.8, 60, 9999, 0, 0, "無"],
        },
    },
    "踊り子": {
        "短剣": {
            "タナトスハント":           [[1.5], 0.7, 1.8, 0, 1999, 10, 170, "無"],
        },
        "扇": {
            "おうぎ乱舞(CT)":           [[0.9]*6, 1.0, 3.6, 110, 9999, 0, 0, "無"],
        },
    },
    "魔剣士": {
        "片手剣": {
            "暗黒連撃":                 [[0.9]*5, 1.0, 2.4, 0, 1999, 0, 0, "闇"],
            "煉獄魔斬(CT)":             [[1.5]*3, 1.9, 2.5, 60, 9999, 0, 0, "闇"],
            "ダークマター(CT)":         [[5.0], 1.9, 2.6, 50, 9999, 0, 0, "闇"],
        },
        "短剣": {
            "暗黒連撃":                 [[0.9]*5, 1.0, 2.4, 0, 1999, 0, 0, "闇"],
            "煉獄魔斬(CT)":             [[1.5]*3, 1.9, 2.5, 60, 9999, 0, 0, "闇"],
            "ダークマター(CT)":         [[5.0], 1.9, 2.6, 50, 9999, 0, 0, "闇"],
            "タナトスハント":           [[1.5]*2, 0.7, 1.8, 0, 3999, 10, 170, "無"],
        },
        "鎌": {
            "暗黒連撃":                 [[0.9]*5, 1.0, 2.4, 0, 1999, 0, 0, "闇"],
            "煉獄魔斬(CT)":             [[1.5]*3, 1.9, 2.5, 60, 9999, 0, 0, "闇"],
            "ダークマター(CT)":         [[5.0], 1.9, 2.6, 50, 9999, 0, 0, "闇"],
        },
    },
    "ガデ": {
        "両手剣": {
            "天光連斬":                 [[0.9]*4, 1.7, 2.1, 0, 1999, 0, 0, "光"],
            "プラーナソード(CT)":       [[3.5], 2.0, 3.1, 60, 9999, 0, 0, "光"],
            "はやぶさ斬り":             [[1.0, 1.0], 1.0, 1.5, 0, 1999, 0, 0, "無"],
            "超はやぶさ斬り(CT)":       [[0.75]*4, 1.5, 2.1, 45, 1999, 0, 0, "無"],
            "不死鳥天舞(CT)":           [[0.9]*4, 1.8, 2.3, 75, 1999, 0, 0, "無"],
            "アルテマソード(CT)":       [[4.5], 1.0, 2.4, 60, 9999, 0, 0, "無"],
        },
        "片手剣": {
            "天光連斬":                 [[0.9]*4, 1.7, 2.1, 0, 1999, 0, 0, "光"],
            "プラーナソード(CT)":       [[3.5], 2.0, 3.1, 60, 9999, 0, 0, "光"],
            "はやぶさ斬り":             [[1.0, 1.0], 1.0, 1.5, 0, 1999, 0, 0, "無"],
            "超はやぶさ斬り(CT)":       [[0.75]*4, 1.5, 2.1, 45, 1999, 0, 0, "無"],
            "不死鳥天舞(CT)":           [[0.9]*4, 1.8, 2.3, 75, 1999, 0, 0, "無"],
            "アルテマソード(CT)":       [[4.5], 1.0, 2.4, 60, 9999, 0, 0, "無"],
        },
        "ヤリ": {
            "さみだれ突き・零":         [[1.2]*4, 0.7, 2.0, 0, 1999, 10, 0, "無"],
            "超さみだれ突き(CT)":       [[0.8]*5, 1.2, 3.8, 80, 1999, 5, 0, "無"],
            "はやぶさ斬り":             [[1.0, 1.0], 1.0, 1.5, 0, 1999, 0, 0, "無"],
        },
    },
    "魔法使い": {
        "両手杖": {
            "メラゾーマ":               ["formula_merazoma", 1.0, 2.6, 0, 5999, 0, 0, "炎"],
            "メラガイアー(CT)":         ["formula_meragaia", 1.0, 3.6, 60, 9999, 0, 0, "炎"],
            "マヒャデドス(CT)":         ["formula_dedos", 1.0, 3.5, 60, 9999, 0, 0, "氷"],
            "メドローア(CT)":           ["formula_medoroa", 2.0, 2.0, 120, 29999, 0, 0, "無"],
        },
    },
}

# 職業・武器ごとの初期ステータス
JOB_STATS = {
    ("武闘家", "ツメ"):     {"atk": 970,  "spd": 954,  "weapon_fixed": 150},
    ("武闘家", "ヤリ"):     {"atk": 1100, "spd": 954,  "weapon_fixed": 0},
    ("武闘家", "棍"):       {"atk": 1050, "spd": 954,  "weapon_fixed": 0},
    ("戦士",   "片手剣"):   {"atk": 920,  "spd": 450,  "weapon_fixed": 0},
    ("戦士",   "両手剣"):   {"atk": 1080, "spd": 450,  "weapon_fixed": 0},
    ("戦士",   "オノ"):     {"atk": 1120, "spd": 450,  "weapon_fixed": 0},
    ("バト",   "片手剣"):   {"atk": 1090, "spd": 635,  "weapon_fixed": 30},
    ("バト",   "両手剣"):   {"atk": 1200, "spd": 635,  "weapon_fixed": 60},
    ("バト",   "ハンマー"): {"atk": 1100, "spd": 635,  "weapon_fixed": 0},
    ("パラ",   "ヤリ"):     {"atk": 1081, "spd": 653,  "weapon_fixed": 100},
    ("パラ",   "片手剣"):   {"atk": 920,  "spd": 653,  "weapon_fixed": 0},
    ("レン",   "ツメ"):     {"atk": 900,  "spd": 750,  "weapon_fixed": 0},
    ("レン",   "ブメ"):     {"atk": 880,  "spd": 750,  "weapon_fixed": 0},
    ("まもの", "ツメ"):     {"atk": 960,  "spd": 800,  "weapon_fixed": 0},
    ("まもの", "ムチ"):     {"atk": 1050, "spd": 800,  "weapon_fixed": 0},
    ("踊り子", "短剣"):     {"atk": 880,  "spd": 850,  "weapon_fixed": 0},
    ("踊り子", "扇"):       {"atk": 870,  "spd": 850,  "weapon_fixed": 0},
    ("魔剣士", "片手剣"):   {"atk": 980,  "spd": 550,  "weapon_fixed": 0},
    ("魔剣士", "短剣"):     {"atk": 920,  "spd": 550,  "weapon_fixed": 0},
    ("魔剣士", "鎌"):       {"atk": 1050, "spd": 550,  "weapon_fixed": 0},
    ("ガデ",   "両手剣"):   {"atk": 1080, "spd": 450,  "weapon_fixed": 0},
    ("ガデ",   "片手剣"):   {"atk": 960,  "spd": 450,  "weapon_fixed": 0},
    ("ガデ",   "ヤリ"):     {"atk": 1040, "spd": 450,  "weapon_fixed": 0},
    ("魔法使い","両手杖"):  {"atk": 1500, "spd": 800,  "weapon_fixed": 0},
}

# 二刀流可能な職業・武器の組み合わせ
DUAL_WIELD_JOBS = {
    "バト":   ["片手剣"],
    "踊り子": ["短剣", "扇"],
    "魔剣士": ["片手剣", "短剣"],
    "ガデ":   ["片手剣"],
}

# テンション倍率
TENSION_MULT = {0: 1.0, 5: 1.5, 20: 2.0, 50: 3.0, 100: 4.0}
TENSION_STAGES = [0, 5, 20, 50, 100]

# テンションインジケータ
def tension_indicator(tension):
    mapping = {0: "◯◯◯◯", 5: "●◯◯◯", 20: "●●◯◯", 50: "●●●◯", 100: "●●●●"}
    return mapping.get(tension, "◯◯◯◯")

# コンボ用特殊行動
SPECIAL_ACTIONS = {
    "バト": {
        "テンションブースト": {"mult": [0], "prep": 0.0, "rigid": 1.5, "ct": 0, "limit": 0, "fixed": 0, "boost_pct": 0, "attr": "無", "special": "tension_boost"},
    },
    "武闘家": {
        "ためる弐":           {"mult": [0], "prep": 0.0, "rigid": 2.3, "ct": 0, "limit": 0, "fixed": 0, "boost_pct": 0, "attr": "無", "special": "tameru2"},
        "ためる参":           {"mult": [0], "prep": 0.0, "rigid": 2.0, "ct": 0, "limit": 0, "fixed": 0, "boost_pct": 0, "attr": "無", "special": "tameru3"},
        "行雲流水(CT)":       {"mult": [0], "prep": 2.3, "rigid": 2.5, "ct": 110, "limit": 0, "fixed": 0, "boost_pct": 0, "attr": "無", "special": "ikuun"},
    },
    "パラ": {
        "鉄壁の進軍(CT)":     {"mult": [0], "prep": 0.0, "rigid": 1.9, "ct": 120, "limit": 0, "fixed": 0, "boost_pct": 0, "attr": "無", "special": "teppeki"},
    },
    "魔法使い": {
        "超暴走魔法陣":        {"mult": [0], "prep": 0.0, "rigid": 2.0, "ct": 0, "limit": 0, "fixed": 0, "boost_pct": 0, "attr": "無", "special": "cho_bousoujin"},
    },
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_job_list():
    return list(DATA_MAP.keys())

def get_weapon_list(job):
    return list(DATA_MAP.get(job, {}).keys())

def get_skill_list(job, weapon):
    skills = list(DATA_MAP.get(job, {}).get(weapon, {}).keys())
    specials = SPECIAL_ACTIONS.get(job, {})
    return skills + list(specials.keys())

def get_skill_data(job, weapon, skill_name):
    """特技データをリスト形式で返す [倍率list, 準備s, 硬直s, CTs, 上限, 特技固定値, 特技補正%, 属性]"""
    skill = DATA_MAP.get(job, {}).get(weapon, {}).get(skill_name)
    if skill:
        mult = skill[0] if isinstance(skill[0], list) else [skill[0]]
        return mult, skill[1], skill[2], skill[3], skill[4], skill[5], skill[6], skill[7]
    # 特殊行動を確認
    special = SPECIAL_ACTIONS.get(job, {}).get(skill_name)
    if special:
        return special["mult"], special["prep"], special["rigid"], special["ct"], special["limit"], special["fixed"], special["boost_pct"], special["attr"]
    return None

def is_dual_wield_possible(job, weapon):
    return weapon in DUAL_WIELD_JOBS.get(job, [])

def is_magic_job(job):
    return job == "魔法使い"

def get_tension_mult(tension):
    return TENSION_MULT.get(tension, 1.0)

def raise_tension(current, steps):
    idx = TENSION_STAGES.index(current) if current in TENSION_STAGES else 0
    new_idx = min(idx + steps, len(TENSION_STAGES) - 1)
    return TENSION_STAGES[new_idx]

# ============================================================
# MAGIC FORMULA
# ============================================================

def calc_magic_base(skill_name, magic_atk):
    if skill_name == "メラゾーマ" or "merazoma" in skill_name.lower():
        if magic_atk < 1000:
            return math.floor((magic_atk - 288) * 522 / 711 + 158)
        else:
            return math.floor((magic_atk - 999) / 4 + 680)
    elif "メラガイアー" in skill_name or "meragaia" in skill_name.lower():
        if magic_atk < 1500:
            return math.floor((magic_atk - 400) * 1060 / 1099 + 680)
        else:
            return math.floor((magic_atk - 1499) / 2 + 1740)
    elif "マヒャデドス" in skill_name or "dedos" in skill_name.lower():
        if magic_atk < 1500:
            return math.floor((magic_atk - 400) * 755 / 1099 + 520)
        else:
            return math.floor((magic_atk - 1499) / 3 + 1275)
    elif "メドローア" in skill_name or "medoroa" in skill_name.lower():
        if magic_atk < 1000:
            return math.floor(magic_atk * 9.0)
        else:
            return math.floor((magic_atk - 1000) * 6 + 9000)
    return 0

# ============================================================
# DAMAGE CALCULATION (Physical)
# ============================================================

def calc_final_atk(display_atk, total_adj, has_baiki=True, has_gajin=False):
    atk_for_buff = display_atk - total_adj
    if has_baiki:
        return math.floor(atk_for_buff * 1.4) + total_adj + (60 if has_gajin else 0)
    else:
        return atk_for_buff + total_adj + (60 if has_gajin else 0)

def calc_base_dmg(skill_name, final_atk, eff_dfn):
    if "ゴッドスマッシュ" in skill_name:
        capped_atk = min(final_atk, 1000)
        return (capped_atk - 300) * 2 + 800
    return max(1.0, (final_atk / 2) - (eff_dfn / 4))

def calc_single_hit(base_dmg, mult, boost_pct, attr_mult, tension, debuff_mult, const_dmg, limit, is_first_hit=True):
    d1 = math.floor(base_dmg * mult)
    d2 = math.floor(d1 * (1.0 + boost_pct / 100.0))
    d_elem = math.floor(d2 * attr_mult)
    if is_first_hit:
        d3 = math.floor(d_elem * tension)
    else:
        d3 = d_elem
    d4 = math.floor(d3 * debuff_mult)
    return min(d4 + const_dmg, limit)

def calc_skill_damage(
    job, weapon, skill_name,
    display_atk, total_adj, eff_dfn,
    species_pct, gem_pct, skill_pct, attr_pct,
    attr_resist,
    tension, debuff_mult,
    const_dmg,
    has_baiki=True, has_gajin=False,
    dual=False, left_display_atk=0, left_total_adj=0
):
    """物理特技の全HIT合計ダメージを計算して返す。戻り値: (total, hit_list, log)"""
    skill = DATA_MAP.get(job, {}).get(weapon, {}).get(skill_name)
    if skill is None:
        return 0, [], []

    mult_list = skill[0] if isinstance(skill[0], list) else [skill[0]]
    limit = skill[4]
    skill_fixed = skill[5]
    skill_boost_pct = skill[6]
    attr_name = skill[7]

    final_atk = calc_final_atk(display_atk, total_adj, has_baiki, has_gajin)
    base = calc_base_dmg(skill_name, final_atk, eff_dfn)

    boost_pct = species_pct + gem_pct + skill_pct + skill_boost_pct
    a_resist = attr_resist.get(attr_name, 1.0)
    attr_mult = a_resist + attr_pct / 100.0
    ten_mult = get_tension_mult(tension)
    total_const = const_dmg + skill_fixed

    hits = []
    log_lines = []
    log_lines.append(f"最終攻撃力: {final_atk} (表示{display_atk} - バイキ対象外{total_adj}) × 1.4 + {total_adj} + 牙神{60 if has_gajin else 0}")
    log_lines.append(f"基礎ダメージ: {base:.1f}")
    log_lines.append(f"倍率強化合計: {boost_pct:.1f}%  属性倍率: {attr_mult:.2f}  テンション倍率: {ten_mult:.1f}")

    for i, mult in enumerate(mult_list):
        is_first = (i == 0)
        h = calc_single_hit(base, mult, boost_pct, attr_mult, ten_mult, debuff_mult, total_const, limit, is_first)
        hits.append(h)
        log_lines.append(f"  HIT{i+1}: floor({base:.1f}×{mult}) →d1={math.floor(base*mult)} → boost → elem → {'TEN×' if is_first else ''}debuff + 固定 = {h}")

    right_total = sum(hits)
    left_dmg = 0

    if dual and is_dual_wield_possible(job, weapon):
        left_final_atk = calc_final_atk(left_display_atk, left_total_adj, has_baiki, has_gajin)
        left_base = max(1.0, (left_final_atk / 2) - (eff_dfn / 4))
        first_mult = mult_list[0]
        left_mult = math.floor(left_base * first_mult)
        left_d = math.floor(left_mult * (1.0 + boost_pct / 100.0))
        left_d_elem = math.floor(left_d * attr_mult)
        left_d4 = math.floor(left_d_elem * debuff_mult)
        left_dmg = min(left_d4 + total_const, limit)
        log_lines.append(f"  左手: final_atk={left_final_atk} base={left_base:.1f} → {left_dmg}")

    total = right_total + left_dmg
    return total, hits, log_lines

# ============================================================
# DAMAGE CALCULATION (Magic)
# ============================================================

def calc_magic_damage(
    skill_name, magic_atk,
    species_pct, skill_pct, attr_pct,
    attr_resist,
    tension, debuff_mult,
    is_awakened=False, is_crit=False, is_limit_break=False
):
    """魔法ダメージ計算。戻り値: (total, base, log)"""
    base = calc_magic_base(skill_name, magic_atk)
    log_lines = [f"基礎ダメージ: {base} (攻撃魔力{magic_atk})"]

    is_medoroa = "メドローア" in skill_name

    if is_crit and not is_medoroa:
        base_after_crit = math.floor(base * 2.3)
        log_lines.append(f"呪文暴走: floor({base} × 2.3) = {base_after_crit}")
        base = base_after_crit
    else:
        log_lines.append("呪文暴走: なし")

    kakusei_pct = 100 if is_awakened else 0
    boost_pct = kakusei_pct + species_pct + skill_pct
    d2 = math.floor(base * (1.0 + boost_pct / 100.0))
    log_lines.append(f"割合強化: {boost_pct:.1f}% → {d2}")

    # 属性適用
    skill = None
    for wep_dict in DATA_MAP.get("魔法使い", {}).values():
        if skill_name in wep_dict:
            skill = wep_dict[skill_name]
            break
    attr_name = skill[7] if skill else "無"
    a_resist = attr_resist.get(attr_name, 1.0)
    attr_mult_val = a_resist + attr_pct / 100.0
    d_elem = math.floor(d2 * attr_mult_val)
    log_lines.append(f"属性({attr_name}): {attr_mult_val:.2f} → {d_elem}")

    ten_mult = get_tension_mult(tension)
    d3 = math.floor(d_elem * ten_mult)
    log_lines.append(f"テンション×{ten_mult:.1f} → {d3}")

    d4 = math.floor(d3 * debuff_mult)
    log_lines.append(f"デバフ×{debuff_mult:.2f} → {d4}")

    # 上限適用
    if skill:
        raw_limit = skill[4]
        if is_limit_break:
            if "メラゾーマ" in skill_name:
                limit = 9999
            elif "(CT)" in skill_name:
                limit = 19999
            else:
                limit = raw_limit
        else:
            limit = raw_limit
    else:
        limit = 9999

    final = min(d4, limit)
    log_lines.append(f"上限({limit}): {final}")

    return final, base, log_lines

# ============================================================
# CYCLE TIME CALCULATION
# ============================================================

def calc_wait(spd, piori):
    return 7.0 * (1.0 - spd / 2048) * (1.0 - piori / 14)

def calc_cycle(spd, piori, prep, rigid, input_delay):
    wait_basic = calc_wait(spd, piori)
    wait_adopted = max(wait_basic, rigid + 0.53)
    return wait_adopted + prep + input_delay, wait_adopted

def calc_debuff_mult(revol, kasama, gusha):
    return 1.0 + (0.5 if revol else 0) + (0.5 if kasama else 0) + (0.2 if gusha else 0)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def init_session_state():
    if "job" not in st.session_state:
        st.session_state.job = "武闘家"
    if "weapon" not in st.session_state:
        st.session_state.weapon = "ツメ"
    if "skill" not in st.session_state:
        st.session_state.skill = "タイガークロー"
    if "display_atk" not in st.session_state:
        st.session_state.display_atk = 970
    if "display_spd" not in st.session_state:
        st.session_state.display_spd = 954
    if "weapon_fixed" not in st.session_state:
        st.session_state.weapon_fixed = 150
    if "piori" not in st.session_state:
        st.session_state.piori = 2
    if "input_delay" not in st.session_state:
        st.session_state.input_delay = 1.0
    if "species_pct" not in st.session_state:
        st.session_state.species_pct = 23.0
    if "gem_pct" not in st.session_state:
        st.session_state.gem_pct = 18.0
    if "skill_pct" not in st.session_state:
        st.session_state.skill_pct = 5.0
    if "attr_pct" not in st.session_state:
        st.session_state.attr_pct = 0.0
    if "equip_fixed" not in st.session_state:
        st.session_state.equip_fixed = 0
    if "job_fixed" not in st.session_state:
        st.session_state.job_fixed = 20
    if "dual" not in st.session_state:
        st.session_state.dual = False
    if "left_atk" not in st.session_state:
        st.session_state.left_atk = 776
    if "combo_list" not in st.session_state:
        st.session_state.combo_list = []
    if "prev_job" not in st.session_state:
        st.session_state.prev_job = "武闘家"

def on_job_change():
    new_job = st.session_state.job_selection
    st.session_state.job = new_job
    weapons = get_weapon_list(new_job)
    if weapons:
        st.session_state.weapon = weapons[0]
        skills = list(DATA_MAP.get(new_job, {}).get(weapons[0], {}).keys())
        if skills:
            st.session_state.skill = skills[0]
    stats = JOB_STATS.get((new_job, st.session_state.weapon), {})
    if stats:
        st.session_state.display_atk = stats.get("atk", 1000)
        st.session_state.display_spd = stats.get("spd", 700)
        st.session_state.weapon_fixed = stats.get("weapon_fixed", 0)
    st.session_state.combo_list = []
    st.session_state.prev_job = new_job

def on_weapon_change():
    job = st.session_state.job
    weapon = st.session_state.weapon_selection
    st.session_state.weapon = weapon
    skills = list(DATA_MAP.get(job, {}).get(weapon, {}).keys())
    if skills:
        st.session_state.skill = skills[0]
    stats = JOB_STATS.get((job, weapon), {})
    if stats:
        st.session_state.display_atk = stats.get("atk", 1000)
        st.session_state.display_spd = stats.get("spd", 700)
        st.session_state.weapon_fixed = stats.get("weapon_fixed", 0)
    st.session_state.combo_list = []

def on_skill_change():
    skill = st.session_state.skill_selection
    st.session_state.skill = skill
    is_ct = "(CT)" in skill
    st.session_state.gem_pct = 12.0 if is_ct else 18.0
    st.session_state.skill_pct = 5.0

# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar():
    st.sidebar.title("🛡️ 共通設定")

    # ------- 職業・武器・特技選択 -------
    st.sidebar.subheader("職業・武器・特技")

    job_list = get_job_list()
    job_idx = job_list.index(st.session_state.job) if st.session_state.job in job_list else 0
    st.sidebar.selectbox(
        "職業",
        job_list,
        index=job_idx,
        key="job_selection",
        on_change=on_job_change,
    )
    job = st.session_state.job

    weapon_list = get_weapon_list(job)
    weapon_idx = weapon_list.index(st.session_state.weapon) if st.session_state.weapon in weapon_list else 0
    st.sidebar.selectbox(
        "武器",
        weapon_list,
        index=weapon_idx,
        key="weapon_selection",
        on_change=on_weapon_change,
    )
    weapon = st.session_state.weapon

    skill_list_for_job = list(DATA_MAP.get(job, {}).get(weapon, {}).keys())
    skill_idx = skill_list_for_job.index(st.session_state.skill) if st.session_state.skill in skill_list_for_job else 0
    st.sidebar.selectbox(
        "特技",
        skill_list_for_job,
        index=skill_idx,
        key="skill_selection",
        on_change=on_skill_change,
    )
    skill = st.session_state.skill

    # 特技情報表示
    sdata = DATA_MAP.get(job, {}).get(weapon, {}).get(skill)
    if sdata:
        mult = sdata[0] if isinstance(sdata[0], list) else [sdata[0]]
        prep, rigid, ct, limit = sdata[1], sdata[2], sdata[3], sdata[4]
        attr = sdata[7]
        st.sidebar.caption(
            f"倍率: {mult}  /  CT: {ct}s  /  準備: {prep}s  /  硬直: {rigid}s  /  属性: {attr}  /  上限: {limit}"
        )

    st.sidebar.divider()

    # ------- ステータス -------
    st.sidebar.subheader("ステータス")
    atk_label = "攻撃魔力" if is_magic_job(job) else "右手攻撃力"
    display_atk = st.sidebar.number_input(atk_label, min_value=0, value=st.session_state.display_atk, step=1)
    st.session_state.display_atk = display_atk

    display_spd = st.sidebar.number_input("素早さ", min_value=0, value=st.session_state.display_spd, step=1)
    st.session_state.display_spd = display_spd

    # 二刀流
    dual_possible = is_dual_wield_possible(job, weapon)
    if dual_possible:
        dual = st.sidebar.checkbox("二刀流ON", value=st.session_state.dual)
        st.session_state.dual = dual
        if dual:
            left_atk_default = math.floor(display_atk * 0.8)
            left_atk = st.sidebar.number_input("左手攻撃力", min_value=0, value=left_atk_default, step=1)
            st.session_state.left_atk = left_atk
        else:
            st.session_state.left_atk = 0
    else:
        st.sidebar.checkbox("二刀流ON", value=False, disabled=True)
        st.session_state.dual = False
        st.session_state.left_atk = 0

    st.sidebar.divider()

    # ------- バイキ対象外 -------
    with st.sidebar.expander("⚙️ バイキ対象外ステータス", expanded=False):
        alchemy_opts = [0, 21, 22, 23, 24, 25, 26, 27]
        alchemy = st.selectbox("武器錬金", alchemy_opts, index=alchemy_opts.index(25))
        kisho_opts = {"Lv0(+0)":0,"Lv1(+7)":7,"Lv2(+10)":10,"Lv3(+13)":13,"Lv4(+17)":17,"Lv5(+21)":21,"Lv6(+25)":25,"Lv7(+29)":29,"Lv8(+33)":33}
        kisho_label = st.selectbox("輝晶核", list(kisho_opts.keys()), index=5)
        kisho = kisho_opts[kisho_label]
        neck_opts = {"ラストチョーカー(40)": 40, "その他(0)": 0}
        neck = neck_opts[st.selectbox("首アクセ", list(neck_opts.keys()), index=0)]
        ring_opts = {"断罪のゆびわ(6)": 6, "その他(0)": 0}
        ring = ring_opts[st.selectbox("指輪", list(ring_opts.keys()), index=0)]
        ank_opts = {"セトのアンク(12)": 12, "その他(0)": 0}
        ank = ank_opts[st.selectbox("アンク", list(ank_opts.keys()), index=0)]
        belt_opts = {"戦神のベルト(25)": 25, "その他(0)": 0}
        belt = belt_opts[st.selectbox("ベルト", list(belt_opts.keys()), index=0)]
        card_opts = {"ふしぎのカード(15)": 15, "その他(0)": 0}
        card = card_opts[st.selectbox("カード", list(card_opts.keys()), index=0)]
        mon_opts = {"ハルファスの大紋章(20)": 20, "その他(0)": 0}
        mon = mon_opts[st.selectbox("紋章", list(mon_opts.keys()), index=0)]
        food_opts = {"バトルステーキ★3(15)": 15, "その他(0)": 0}
        food = food_opts[st.selectbox("料理", list(food_opts.keys()), index=0)]

        total_adj = alchemy + kisho + neck + ring + ank + belt + card + mon + food
        st.metric("バイキ対象外攻撃力の合計", f"+{total_adj}")

    # ------- 割合強化 -------
    with st.sidebar.expander("📊 ダメージ割合強化・固定加算", expanded=False):
        species_pct = st.number_input("種族ダメージ (%)", value=st.session_state.species_pct, step=0.5)
        gem_pct = st.number_input("宝珠強化 (%)", value=st.session_state.gem_pct, step=0.5)
        skill_pct = st.number_input("スキル160-200強化 (%)", value=st.session_state.skill_pct, step=0.5)
        attr_pct = st.number_input("属性強化 (%)", value=st.session_state.attr_pct, step=0.5)
        st.markdown("---")
        equip_fixed = st.number_input("装備固定加算", value=st.session_state.equip_fixed, step=1)
        job_fixed = st.number_input("職業スキル固定", value=st.session_state.job_fixed, step=1)
        weapon_fixed = st.number_input("武器スキル固定", value=st.session_state.weapon_fixed, step=1)
        st.session_state.weapon_fixed = weapon_fixed

    st.session_state.species_pct = species_pct
    st.session_state.gem_pct = gem_pct
    st.session_state.skill_pct = skill_pct
    st.session_state.attr_pct = attr_pct
    st.session_state.equip_fixed = equip_fixed
    st.session_state.job_fixed = job_fixed

    st.sidebar.divider()

    # ------- 共通バフ -------
    st.sidebar.subheader("共通バフ")
    piori = st.sidebar.slider("ピオリム段階", 0, 5, st.session_state.piori)
    st.session_state.piori = piori
    input_delay = st.sidebar.number_input("入力遅延 (s)", value=st.session_state.input_delay, step=0.1, min_value=0.0)
    st.session_state.input_delay = input_delay

    # 合計固定
    total_const = equip_fixed + job_fixed + weapon_fixed

    return {
        "job": job,
        "weapon": weapon,
        "skill": skill,
        "display_atk": display_atk,
        "display_spd": display_spd,
        "dual": st.session_state.dual,
        "left_atk": st.session_state.left_atk,
        "total_adj": total_adj,
        "species_pct": species_pct,
        "gem_pct": gem_pct,
        "skill_pct": skill_pct,
        "attr_pct": attr_pct,
        "total_const": total_const,
        "equip_fixed": equip_fixed,
        "job_fixed": job_fixed,
        "weapon_fixed": weapon_fixed,
        "piori": piori,
        "input_delay": input_delay,
    }

# ============================================================
# TAB 1: 単発ダメージ計算
# ============================================================

def render_tab_single(cfg):
    job = cfg["job"]
    weapon = cfg["weapon"]
    skill = cfg["skill"]
    display_atk = cfg["display_atk"]
    display_spd = cfg["display_spd"]
    total_adj = cfg["total_adj"]
    species_pct = cfg["species_pct"]
    gem_pct = cfg["gem_pct"]
    skill_pct = cfg["skill_pct"]
    attr_pct = cfg["attr_pct"]
    total_const = cfg["total_const"]
    piori = cfg["piori"]
    input_delay = cfg["input_delay"]
    dual = cfg["dual"]
    left_atk = cfg["left_atk"]

    left_col, right_col = st.columns([1, 1])

    # ----- 左カラム：敵ステータス -----
    with left_col:
        st.subheader("🐉 敵ステータス")
        eff_dfn_input = st.number_input("敵守備力", value=1490, step=10, key="single_eff_dfn")
        dfn_zero = st.checkbox("守備力0設定", key="single_dfn_zero")
        eff_dfn = 0 if dfn_zero else eff_dfn_input

        with st.expander("属性耐性設定", expanded=False):
            attr_resist = {}
            for attr_name in ["炎", "氷", "風", "雷", "土", "光", "闇"]:
                attr_resist[attr_name] = st.number_input(
                    f"{attr_name}耐性倍率", value=1.0, step=0.05, key=f"single_resist_{attr_name}"
                )
            attr_resist["無"] = 1.0

    # ----- 右カラム：環境・バフ -----
    with right_col:
        st.subheader("⚔️ 環境・バフ設定")
        revol = st.checkbox("レボルスライサー (+50%)", key="single_revol")
        kasama = st.checkbox("災禍の陣 (+50%)", key="single_kasama")
        gusha = st.checkbox("愚者の陣 (+20%)", key="single_gusha")
        gajin = st.checkbox("牙神昇誕 (+60固定攻撃力)", key="single_gajin")
        tension_options = [0, 20, 50, 100]
        tension = st.selectbox("テンション段階", tension_options, key="single_tension")

    debuff_mult = calc_debuff_mult(revol, kasama, gusha)

    # ----- 計算実行 -----
    sdata = DATA_MAP.get(job, {}).get(weapon, {}).get(skill)
    if sdata is None:
        st.warning("この特技のデータが見つかりません。")
        return

    # 魔法使いは魔法計算タブへ誘導
    if isinstance(sdata[0], str) and sdata[0].startswith("formula_"):
        st.info("✨ 魔法使いの呪文は「魔法ダメージ計算」タブで計算してください。")
        return

    mult_list = sdata[0] if isinstance(sdata[0], list) else [sdata[0]]
    prep, rigid, ct, limit, skill_fixed, skill_boost_pct, attr_name = sdata[1], sdata[2], sdata[3], sdata[4], sdata[5], sdata[6], sdata[7]

    final_atk = calc_final_atk(display_atk, total_adj, True, gajin)
    base = calc_base_dmg(skill, final_atk, eff_dfn)
    boost_pct = species_pct + gem_pct + skill_pct + skill_boost_pct
    a_resist = attr_resist.get(attr_name, 1.0)
    attr_mult_val = a_resist + attr_pct / 100.0
    ten_mult = get_tension_mult(tension)
    all_const = total_const + skill_fixed

    hits = []
    hit_logs = []
    for i, mult in enumerate(mult_list):
        is_first = (i == 0)
        h = calc_single_hit(base, mult, boost_pct, attr_mult_val, ten_mult, debuff_mult, all_const, limit, is_first)
        hits.append(h)
        hit_logs.append(f"HIT{i+1}={h}")

    right_total = sum(hits)
    left_dmg = 0
    left_log = ""
    if dual and is_dual_wield_possible(job, weapon):
        left_total_adj = total_adj
        left_final_atk = calc_final_atk(left_atk, left_total_adj, True, gajin)
        left_base = max(1.0, (left_final_atk / 2) - (eff_dfn / 4))
        first_mult = mult_list[0]
        left_mult_d = math.floor(left_base * first_mult)
        left_d = math.floor(left_mult_d * (1.0 + boost_pct / 100.0))
        left_d_elem = math.floor(left_d * attr_mult_val)
        left_d4 = math.floor(left_d_elem * debuff_mult)
        left_dmg = min(left_d4 + all_const, limit)
        left_log = f" + 左手={left_dmg}"

    total = right_total + left_dmg
    cycle, wait_adopted = calc_cycle(display_spd, piori, prep, rigid, input_delay)
    dps = total / cycle if cycle > 0 else 0

    # ----- 結果表示 -----
    st.divider()
    st.subheader("📊 計算結果")
    r1, r2 = st.columns(2)
    with r1:
        st.metric(
            "合計ダメージ",
            f"{total:,}",
            delta=f"({' + '.join(hit_logs)}{left_log})",
        )
    with r2:
        st.metric(
            "推定DPS",
            f"{dps:,.1f}",
            delta=f"サイクル: {cycle:.2f}s",
        )

    with st.expander("🔍 詳細計算ログ", expanded=False):
        st.markdown("**ステータス根拠**")
        st.text(
            f"表示攻撃力: {display_atk}\n"
            f"バイキ対象外合計: {total_adj}\n"
            f"バイキ対象攻撃力: {display_atk - total_adj}\n"
            f"最終攻撃力(バイキ後): {final_atk}\n"
            f"有効守備力: {eff_dfn}\n"
            f"基礎ダメージ: {base:.2f}\n"
        )
        st.markdown("**ダメージ計算過程**")
        st.text(
            f"倍率強化合計: {boost_pct:.1f}%\n"
            f"属性({attr_name}) 耐性倍率: {a_resist:.2f}  属性強化: {attr_pct:.1f}%  → attr_mult: {attr_mult_val:.3f}\n"
            f"テンション({tension}): ×{ten_mult:.1f}\n"
            f"デバフ倍率: ×{debuff_mult:.2f}\n"
            f"固定ダメージ合計: +{all_const}\n"
            f"各HIT: {hit_logs}\n"
            f"右手合計: {right_total}  左手: {left_dmg}  総計: {total}\n"
        )
        st.markdown("**DPS計算根拠**")
        wait_basic = calc_wait(display_spd, piori)
        st.text(
            f"基本待機秒数: {wait_basic:.3f}s (素早さ{display_spd}, ピオリム{piori}段)\n"
            f"硬直制限: {rigid}s + 0.53 = {rigid+0.53:.2f}s\n"
            f"採用待機秒数: max({wait_basic:.3f}, {rigid+0.53:.2f}) = {wait_adopted:.3f}s\n"
            f"準備時間: {prep}s\n"
            f"入力遅延: {input_delay}s\n"
            f"1サイクル: {wait_adopted:.3f} + {prep} + {input_delay} = {cycle:.3f}s\n"
            f"DPS: {total} / {cycle:.3f} = {dps:.1f}\n"
        )

# ============================================================
# TAB 2: コンボ入力・DPS計測
# ============================================================

def reset_combo():
    st.session_state.combo_list = []

def add_to_combo(entry):
    st.session_state.combo_list.append(entry)

def remove_from_combo(idx):
    if 0 <= idx < len(st.session_state.combo_list):
        st.session_state.combo_list.pop(idx)

def calc_combo_time_up_to(combo_list, n, spd, piori, input_delay):
    """combo_list[0..n-1] の累積時間を返す"""
    t = 0.0
    for i in range(n):
        entry = combo_list[i]
        if entry.get("no_time"):
            continue
        rigid = entry.get("rigid", 0)
        prep = entry.get("prep", 0)
        wait_basic = calc_wait(spd, piori)
        wait_adopted = max(wait_basic, rigid + 0.53)
        t += wait_adopted + prep + input_delay
    return t

def calc_combo_results(combo_list, cfg, attr_resist_combo, piori_boost=0):
    """コンボ全体を計算して (total_dmg, total_time, rows) を返す"""
    job = cfg["job"]
    weapon = cfg["weapon"]
    display_atk = cfg["display_atk"]
    display_spd = cfg["display_spd"]
    total_adj = cfg["total_adj"]
    species_pct = cfg["species_pct"]
    gem_pct = cfg["gem_pct"]
    skill_pct = cfg["skill_pct"]
    attr_pct = cfg["attr_pct"]
    total_const = cfg["total_const"]
    piori = cfg["piori"]
    input_delay = cfg["input_delay"]
    dual = cfg["dual"]
    left_atk = cfg["left_atk"]

    total_dmg = 0
    total_time = 0.0
    rows = []

    # テンション・バフ状態管理
    tension = 0
    boost_active = False
    boost_start = 0.0
    ikuun_active = False
    ikuun_start = 0.0
    ikuun_prob_active = False
    ikuun_prob_start = 0.0
    teppeki_active = False
    teppeki_start = 0.0
    teppeki_atk = 390
    cho_bousoujin_active = False
    cho_bousoujin_start = 0.0

    # デバフ状態
    revol_start = -999.0
    kasama_start = -999.0
    dfn0_start = -999.0

    for idx, entry in enumerate(combo_list):
        skill_name = entry["name"]
        is_debuf = entry.get("is_debuf", False)
        no_time = entry.get("no_time", False)

        # 時間加算
        if not no_time:
            rigid = entry.get("rigid", 1.8)
            prep = entry.get("prep", 0.6)
            wait_basic = calc_wait(display_spd, piori)
            wait_adopted = max(wait_basic, rigid + 0.53)
            duration = wait_adopted + prep + input_delay
            total_time += duration
        else:
            duration = 0.0

        T_now = total_time

        # デバフボタン処理
        if is_debuf:
            if skill_name == "レボル":
                revol_start = T_now
            elif skill_name == "災禍":
                kasama_start = T_now
            elif skill_name == "守備0":
                dfn0_start = T_now
            rows.append({
                "順": idx+1,
                "経過": f"{T_now:.1f}s",
                "特技名": f"[{skill_name}]",
                "ダメージ": "-",
                "テンション": "-",
                "所要": "0.0s",
            })
            continue

        # 特殊行動処理
        special = SPECIAL_ACTIONS.get(job, {}).get(skill_name)
        if special:
            sp_type = special.get("special")
            if sp_type == "tension_boost":
                tension = 100
                boost_active = True
                boost_start = T_now
            elif sp_type == "tameru2":
                tension = raise_tension(tension, 2)
            elif sp_type == "tameru3":
                tension = raise_tension(tension, 3)
            elif sp_type == "ikuun":
                ikuun_active = True
                ikuun_start = T_now
                ikuun_prob_active = True
                ikuun_prob_start = T_now
            elif sp_type == "teppeki":
                teppeki_active = True
                teppeki_start = T_now
            elif sp_type == "cho_bousoujin":
                cho_bousoujin_active = True
                cho_bousoujin_start = T_now

            ten_ind = tension_indicator(tension)
            rows.append({
                "順": idx+1,
                "経過": f"{T_now:.1f}s",
                "特技名": skill_name,
                "ダメージ": 0,
                "テンション": f"{ten_ind} ({tension})",
                "所要": f"{duration:.1f}s",
            })
            continue

        # 攻撃特技ダメージ計算
        sdata = DATA_MAP.get(job, {}).get(weapon, {}).get(skill_name)
        if sdata is None:
            rows.append({"順": idx+1, "経過": f"{T_now:.1f}s", "特技名": skill_name, "ダメージ": "?", "テンション": "-", "所要": f"{duration:.1f}s"})
            continue

        limit = sdata[4]
        attr_name = sdata[7]

        # 動的デバフ判定
        revol = (T_now - revol_start) < 20.0
        kasama = (T_now - kasama_start) < 20.0
        eff_dfn_now = 0 if (T_now - dfn0_start) < 12.0 else 1490
        debuff_mult_now = calc_debuff_mult(revol, kasama, False)

        # テンション維持判定
        maintain_ten = False
        if boost_active and (T_now - boost_start) < 30.0:
            maintain_ten = True
        if ikuun_active and (T_now - ikuun_start) < 40.0:
            maintain_ten = True

        ten_at_fire = tension

        # 攻撃後テンションリセット（維持なし時）
        if not maintain_ten:
            tension_after = 0
        else:
            tension_after = tension

        # 魔法呪文の場合は魔法計算ルートへ
        if isinstance(sdata[0], str) and sdata[0].startswith("formula_"):
            a_resist_m = attr_resist_combo.get(attr_name, 1.0)
            attr_mult_m = a_resist_m + attr_pct / 100.0
            magic_base = calc_magic_base(skill_name, display_atk)
            # 超暴走魔法陣が有効な場合は呪文暴走（×2.3）を適用（メドローア除外）
            is_cho_active = cho_bousoujin_active and (T_now - cho_bousoujin_start) < 120.0
            is_medoroa = "メドローア" in skill_name
            if is_cho_active and not is_medoroa:
                magic_base = math.floor(magic_base * 2.3)
            boost_pct_m = species_pct + skill_pct
            d2 = math.floor(magic_base * (1.0 + boost_pct_m / 100.0))
            d_elem = math.floor(d2 * attr_mult_m)
            ten_mult_m = get_tension_mult(ten_at_fire)
            d3 = math.floor(d_elem * ten_mult_m)
            dmg = min(math.floor(d3 * debuff_mult_now), limit)
            ten_ind = tension_indicator(ten_at_fire)
            crit_mark = " 💥暴走" if (is_cho_active and not is_medoroa) else ""
            rows.append({
                "順": idx+1,
                "経過": f"{T_now:.1f}s",
                "特技名": skill_name + crit_mark,
                "ダメージ": f"{dmg:,}",
                "テンション": f"{ten_ind} ({ten_at_fire})",
                "所要": f"{duration:.1f}s",
            })
            total_dmg += dmg
            tension = tension_after
            continue

        # 物理特技の計算
        mult_list = sdata[0] if isinstance(sdata[0], list) else [sdata[0]]
        skill_fixed = sdata[5]
        skill_boost_pct = sdata[6]

        # 鉄壁加算
        extra_atk = teppeki_atk if (teppeki_active and (T_now - teppeki_start) < 45.0) else 0
        eff_atk = display_atk + extra_atk

        final_atk = calc_final_atk(eff_atk, total_adj, True, False)
        base = calc_base_dmg(skill_name, final_atk, eff_dfn_now)
        boost_pct = species_pct + gem_pct + skill_pct + skill_boost_pct
        a_resist = attr_resist_combo.get(attr_name, 1.0)
        attr_mult_val = a_resist + attr_pct / 100.0
        ten_mult = get_tension_mult(ten_at_fire)
        all_const = total_const + skill_fixed

        hits = []
        for i, mult in enumerate(mult_list):
            is_first = (i == 0)
            h = calc_single_hit(base, mult, boost_pct, attr_mult_val, ten_mult, debuff_mult_now, all_const, limit, is_first)
            hits.append(h)

        dmg = sum(hits)

        # 左手
        if dual and is_dual_wield_possible(job, weapon):
            left_total_adj = total_adj
            left_final_atk = calc_final_atk(left_atk, left_total_adj, True, False)
            left_base = max(1.0, (left_final_atk / 2) - (eff_dfn_now / 4))
            first_mult = mult_list[0]
            left_mult_d = math.floor(left_base * first_mult)
            left_d = math.floor(left_mult_d * (1.0 + boost_pct / 100.0))
            left_d_elem = math.floor(left_d * attr_mult_val)
            left_d4 = math.floor(left_d_elem * debuff_mult_now)
            left_dmg = min(left_d4 + all_const, limit)
            dmg += left_dmg

        total_dmg += dmg

        ten_ind = tension_indicator(ten_at_fire)
        rows.append({
            "順": idx+1,
            "経過": f"{T_now:.1f}s",
            "特技名": skill_name,
            "ダメージ": f"{dmg:,}",
            "テンション": f"{ten_ind} ({ten_at_fire})",
            "所要": f"{duration:.1f}s",
        })

        tension = tension_after

        # 行雲テンション期待値
        if ikuun_prob_active and (T_now - ikuun_prob_start) < 90.0:
            if not maintain_ten:
                # 期待値加算
                prob = 0.5
                stage_probs = {0: 1.0, 5: 0.8, 20: 0.6, 50: 0.25}
                stage_gains = {0: 5, 5: 20, 20: 50, 50: 100}
                cur = tension
                expected = 0.0
                for stage, sp in stage_probs.items():
                    if cur == stage:
                        expected = prob * sp
                        break
                if expected > 0.3:
                    tension = raise_tension(tension, 1)

    return total_dmg, total_time, rows

def get_ct_status(combo_list, skill_name, spd, piori, input_delay):
    """
    combo_listに基づき、skill_nameのCT残り秒数を返す。
    0以下 = 使用可能。正の値 = 残りCT秒数。
    """
    job_skills = {}
    for job_key in DATA_MAP:
        for wpn_key in DATA_MAP[job_key]:
            job_skills.update(DATA_MAP[job_key][wpn_key])
    for job_key in SPECIAL_ACTIONS:
        for sk, val in SPECIAL_ACTIONS[job_key].items():
            job_skills[sk] = {"ct": val["ct"]}

    sdata = None
    for job_key in DATA_MAP:
        for wpn_key in DATA_MAP[job_key]:
            if skill_name in DATA_MAP[job_key][wpn_key]:
                sdata = DATA_MAP[job_key][wpn_key][skill_name]
                break
    for job_key in SPECIAL_ACTIONS:
        if skill_name in SPECIAL_ACTIONS[job_key]:
            sdata_sp = SPECIAL_ACTIONS[job_key][skill_name]
            return 0  # 特殊行動はCT判定しない

    if sdata is None:
        return 0
    ct = sdata[3] if not isinstance(sdata[0], str) else 0
    if ct == 0:
        return 0

    # 最後に使用した時刻を探す
    last_used = -1
    last_time = -1.0
    cum_time = 0.0
    for i, entry in enumerate(combo_list):
        if not entry.get("no_time", False) and not entry.get("is_debuf", False):
            rigid = entry.get("rigid", 1.8)
            prep = entry.get("prep", 0.6)
            w = calc_wait(spd, piori)
            w_adopted = max(w, rigid + 0.53)
            cum_time += w_adopted + prep + input_delay
        if entry["name"] == skill_name:
            last_used = i
            last_time = cum_time

    if last_used < 0:
        return 0  # まだ使用していない → 使用可能（開幕CT撤廃）

    # 現在の累積時間
    total_t = cum_time
    elapsed = total_t - last_time
    remaining = ct - elapsed
    return remaining

def render_tab_combo(cfg):
    job = cfg["job"]
    weapon = cfg["weapon"]
    display_spd = cfg["display_spd"]
    piori = cfg["piori"]
    input_delay = cfg["input_delay"]

    # コンボページ用属性耐性（固定値で設定）
    attr_resist_combo = {a: 1.0 for a in ["炎", "氷", "風", "雷", "土", "光", "闇", "無"]}

    # 結果の事前計算
    total_dmg, total_time, rows = calc_combo_results(
        st.session_state.combo_list, cfg, attr_resist_combo
    )
    dps = total_dmg / total_time if total_time > 0 else 0

    # --- サマリー ---
    st.subheader("📈 コンボサマリー")
    sc1, sc2, sc3, sc4 = st.columns([2, 2, 2, 1])
    with sc1:
        st.metric("合計ダメージ", f"{total_dmg:,}")
    with sc2:
        st.metric("平均DPS", f"{dps:,.1f}")
    with sc3:
        st.metric("経過時間", f"{total_time:.1f}s")
    with sc4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ リセット", type="primary", key="combo_reset"):
            reset_combo()
            st.rerun()

    st.divider()

    # --- クイック選択ボタン ---
    st.subheader("⚡ 特技・デバフ クイック選択")
    btn_col, debuf_col = st.columns([2, 1])

    with btn_col:
        st.markdown("**特技選択**")
        skills_in_weapon = list(DATA_MAP.get(job, {}).get(weapon, {}).keys())
        specials_in_job = list(SPECIAL_ACTIONS.get(job, {}).keys())
        all_skills = skills_in_weapon + specials_in_job

        num_cols = 4
        rows_btns = [all_skills[i:i+num_cols] for i in range(0, len(all_skills), num_cols)]
        for row_btns in rows_btns:
            cols = st.columns(num_cols)
            for ci, sk_name in enumerate(row_btns):
                with cols[ci]:
                    remaining_ct = get_ct_status(st.session_state.combo_list, sk_name, display_spd, piori, input_delay)
                    is_disabled = remaining_ct > 0.05

                    if st.button(sk_name, disabled=is_disabled, key=f"combo_btn_{sk_name}"):
                        # エントリ作成
                        sdata = DATA_MAP.get(job, {}).get(weapon, {}).get(sk_name)
                        if sdata:
                            mult_list = sdata[0] if isinstance(sdata[0], list) else [sdata[0]]
                            prep, rigid, ct = sdata[1], sdata[2], sdata[3]
                        else:
                            sp = SPECIAL_ACTIONS.get(job, {}).get(sk_name, {})
                            mult_list = sp.get("mult", [0])
                            prep = sp.get("prep", 0)
                            rigid = sp.get("rigid", 1.8)
                            ct = sp.get("ct", 0)
                        add_to_combo({
                            "name": sk_name,
                            "prep": prep,
                            "rigid": rigid,
                            "ct": ct,
                        })
                        st.rerun()

                    if is_disabled:
                        st.caption(f":green[残り {remaining_ct:.1f}s]")

    with debuf_col:
        st.markdown("**デバフ・状態付与**")
        debuf_defs = [
            ("＋レボル", "レボル", 20.0),
            ("＋災禍",   "災禍",   20.0),
            ("＋守備0",  "守備0",  12.0),
        ]
        for label, dname, dur in debuf_defs:
            if st.button(label, key=f"debuf_btn_{dname}"):
                add_to_combo({
                    "name": dname,
                    "is_debuf": True,
                    "no_time": True,
                    "prep": 0,
                    "rigid": 0,
                    "ct": 0,
                })
                st.rerun()

    st.divider()

    # --- コンボリスト ---
    st.subheader("📋 コンボリスト（クリックで削除）")
    if not st.session_state.combo_list:
        st.info("特技を選択してください")
    else:
        num_cols = 4
        list_rows = [
            (i, e) for i, e in enumerate(st.session_state.combo_list)
        ]
        chunked = [list_rows[i:i+num_cols] for i in range(0, len(list_rows), num_cols)]
        for chunk in chunked:
            cols = st.columns(num_cols)
            for ci, (i, entry) in enumerate(chunk):
                with cols[ci]:
                    label = entry["name"]
                    if entry.get("is_debuf"):
                        label = f"[{label}]"
                    if st.button(f"✕ {label}", key=f"del_combo_{i}"):
                        remove_from_combo(i)
                        st.rerun()

    st.divider()

    # --- 詳細内訳テーブル ---
    st.subheader("📊 コンボ実行詳細内訳")
    if rows:
        import pandas as pd
        df = pd.DataFrame(rows)
        df.columns = ["実行順", "経過時間", "特技名", "ダメージ", "テンション", "所要秒数"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("コンボリストが空です")

# ============================================================
# TAB 3: 魔法ダメージ計算
# ============================================================

def render_tab_magic(cfg):
    job = cfg["job"]
    display_atk = cfg["display_atk"]
    display_spd = cfg["display_spd"]
    species_pct = cfg["species_pct"]
    skill_pct = cfg["skill_pct"]
    attr_pct = cfg["attr_pct"]
    piori = cfg["piori"]
    input_delay = cfg["input_delay"]

    # 魔法使いでない場合は案内
    if job != "魔法使い":
        st.info("このタブは「魔法使い」職業専用です。サイドバーで職業を「魔法使い」に変更してください。")
        return

    magic_atk = cfg["display_atk"]

    left_col, right_col = st.columns([1, 1])

    # 魔法スキル選択
    magic_skills = list(DATA_MAP.get("魔法使い", {}).get("両手杖", {}).keys())

    with left_col:
        st.subheader("✨ 魔法スキル設定")
        magic_skill = st.selectbox("魔法スキル", magic_skills, key="magic_skill_select")

        with st.expander("属性耐性設定", expanded=False):
            attr_resist_m = {}
            for attr_name in ["炎", "氷", "風", "雷", "土", "光", "闇"]:
                attr_resist_m[attr_name] = st.number_input(
                    f"{attr_name}耐性倍率", value=1.0, step=0.05, key=f"magic_resist_{attr_name}"
                )
            attr_resist_m["無"] = 1.0

    with right_col:
        st.subheader("⚔️ 環境・バフ設定")
        is_awakened = st.checkbox("魔力覚醒（種族+100%）", key="magic_awakened")
        is_crit = st.checkbox("呪文暴走（×2.3）", key="magic_crit")
        is_limit_break = st.checkbox("ダメージ上限突破", key="magic_limit_break")
        revol_m = st.checkbox("レボルスライサー (+50%)", key="magic_revol")
        kasama_m = st.checkbox("災禍の陣 (+50%)", key="magic_kasama")
        tension_m_options = [0, 20, 50, 100]
        tension_m = st.selectbox("テンション段階", tension_m_options, key="magic_tension")

    debuff_mult_m = calc_debuff_mult(revol_m, kasama_m, False)

    sdata = DATA_MAP["魔法使い"]["両手杖"].get(magic_skill)
    if sdata is None:
        st.warning("魔法データが見つかりません。")
        return

    prep_m = sdata[1]
    rigid_m = sdata[2]
    raw_limit = sdata[4]
    attr_name_m = sdata[7]

    total, base, log_lines = calc_magic_damage(
        magic_skill, magic_atk,
        species_pct, skill_pct, attr_pct,
        attr_resist_m,
        tension_m, debuff_mult_m,
        is_awakened, is_crit, is_limit_break
    )

    cycle_m, wait_m = calc_cycle(display_spd, piori, prep_m, rigid_m, input_delay)
    dps_m = total / cycle_m if cycle_m > 0 else 0

    st.divider()
    st.subheader("📊 計算結果")
    r1, r2 = st.columns(2)
    with r1:
        st.metric("合計ダメージ", f"{total:,}")
    with r2:
        st.metric("推定DPS", f"{dps_m:,.1f}", delta=f"サイクル: {cycle_m:.2f}s")

    with st.expander("🔍 詳細計算ログ", expanded=False):
        for line in log_lines:
            st.text(line)
        wait_basic_m = calc_wait(display_spd, piori)
        st.text(
            f"\n--- DPS根拠 ---\n"
            f"基本待機: {wait_basic_m:.3f}s\n"
            f"硬直制限: {rigid_m}s + 0.53 = {rigid_m+0.53:.2f}s\n"
            f"採用待機: {wait_m:.3f}s\n"
            f"1サイクル: {wait_m:.3f} + {prep_m} + {input_delay} = {cycle_m:.3f}s\n"
            f"DPS: {total} / {cycle_m:.3f} = {dps_m:.1f}"
        )

# ============================================================
# MAIN
# ============================================================

def main():
    st.set_page_config(
        page_title="DQ10 物理DPSシミュレーター",
        layout="wide",
        page_icon="🛡️",
    )

    st.title("🛡️ DQ10 物理DPSシミュレーター")

    init_session_state()
    cfg = render_sidebar()

    tab1, tab2, tab3 = st.tabs(["⚔️ 単発ダメージ計算", "🔗 コンボ入力・DPS計測", "✨ 魔法ダメージ計算"])

    with tab1:
        render_tab_single(cfg)

    with tab2:
        render_tab_combo(cfg)

    with tab3:
        render_tab_magic(cfg)


if __name__ == "__main__":
    main()