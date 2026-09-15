SYNTHETIC_DRUG_INTERACTIONS = {
    ("warfarin", "ibuprofen"): {
        "severity" : "high",
        "message" : "Concurrent use of warfarin and ibuprofen may increase the risk of bleeding."

    },

    ("simvastatin", "clarithomycin"): {
        "severity" : "high",
        "message" : "Concurrent use of simvastatin and clarithomycin may increase the risk of myopathy."
    },
}



def find_drug_interaction(proposed_medication, current_medications):
    proposed_name = proposed_medication.name.lower()

    for medication in current_medications:
        current_name = medication.name.lower()

        pair = (proposed_name, current_name)
        reverse_pair = (current_name, proposed_name)

        if pair in SYNTHETIC_DRUG_INTERACTIONS:
            return SYNTHETIC_DRUG_INTERACTIONS[pair]


        if reverse_pair in SYNTHETIC_DRUG_INTERACTIONS:
            return SYNTHETIC_DRUG_INTERACTIONS[reverse_pair]

    return None


SYNTHETIC_DOSAGE_LIMITS = {
    "warfarin" : {
        "max_amount" : 10,
        "unit": "mg",

    },
    "ibruprofen": {
        "max_amount" : 800,
        "unit" : "mg",
    },

    "simvastatin" : {
        "max_amount" : 40,
        "unit": "mg",

    },
}

def get_dosage_limit(medication_name):
    return SYNTHETIC_DOSAGE_LIMITS.get(medication_name.lower())


SYNTHETIC_THERAPEUTIC_CATEGORIES = {
    "warfarin": "anticoagulent",
    "ibruprofen": "nsaid",
    "simvastatin": "statin",
    "clarithromycin": "macrolide_antibiotic",
}

def get_therapeuric_category(medication_name):
    return SYNTHETIC_THERAPEUTIC_CATEGORIES.get(medication_name.lower())