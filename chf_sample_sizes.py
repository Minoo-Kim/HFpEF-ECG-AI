#!/usr/bin/env python
# coding: utf-8

# In[112]:


import pandas as pd
import os

# opening relevant files
icd_codes = pd.read_csv('/Users/minookim/Desktop/LCICM/mimic4_ehr/diagnoses_icd.csv')
icu_stays = pd.read_csv('/Users/minookim/Desktop/LCICM/mimic4_ehr/icustays.csv')
lab_events = pd.read_csv('/Users/minookim/Desktop/LCICM/mimic4_ehr/labevents.csv')
lab_events_id = pd.read_csv('/Users/minookim/Desktop/LCICM/mimic4_ehr/d_labitems.csv')
lab_events = pd.merge(lab_events, lab_events_id, on='itemid', how='left')
print ("File reading complete")


# In[155]:


# extract patient IDs with 12-lead ECGs
ecg_ids = [f.name for f in os.scandir('/Users/minookim/Desktop/LCICM/ecg_extraction/mimic-iv-ecg/files/')]
ecg_ids.remove(".DS_Store")
# take out p and convert to number
ecg_ids = [id[1:] for id in ecg_ids]
ecg_ids = [int(i) for i in ecg_ids]
print(len(ecg_ids)) # evaluates to 93
print(ecg_ids)


# In[156]:


# total ICU population
print(len(icu_stays))

# ICU population w/ 24 hour data
icu_stays = icu_stays[icu_stays['los']>=1]
icu_stays=icu_stays.drop_duplicates('hadm_id')
icu_ids = list(icu_stays.hadm_id)
print(len(icu_ids)) 
print(icu_stays['subject_id'].nunique()) # e: 53034, p: 42264


# In[157]:


# filter every file with confirmed ICU stay
icd_codes = icd_codes[icd_codes['hadm_id'].isin(icu_ids)]
lab_events = lab_events[lab_events['hadm_id'].isin(icu_ids)]


# In[158]:


# filter for HFpEF w/ ICD codes
hfpef_icd9 = icd_codes[icd_codes['icd_code'].str.startswith('4283')]
hfpef_icd10 = icd_codes[icd_codes['icd_code'].str.startswith('I503')]
hfpef_ids = pd.concat([hfpef_icd9, hfpef_icd10])
hfpef_ids = hfpef_ids.drop_duplicates('hadm_id')
# for encounter 
print(len(hfpef_ids))
# for patient 
print(hfpef_ids['subject_id'].nunique())


# In[159]:


probnp_total = lab_events[(lab_events['itemid'] == 50963)]
probnp_total = probnp_total.dropna(subset=['valuenum'])
probnp_total = probnp_total.drop_duplicates('hadm_id')
probnp_total_ids  = list(probnp_total.hadm_id)
print(len(probnp_total_ids))

# filter for proBNP over and under 200
probnp_positive = probnp_total[probnp_total['valuenum'] > 200]
probnp_positive_ids = list(probnp_positive.hadm_id)
print(len(probnp_positive_ids))

# < 200
probnp_negative = probnp_total[probnp_total['valuenum'] <= 200]
probnp_negative_ids = list(probnp_negative.hadm_id)
print(len(probnp_negative_ids))


# In[168]:


# HFpEF: proBNP + ICD codes
hfpef_icd_positive = hfpef_ids[hfpef_ids['hadm_id'].isin(probnp_positive_ids)]
print(len (hfpef_icd_positive)) 
print(hfpef_icd_positive['subject_id'].nunique()) # e: 1501, p: 1401

# HFpEF: proBNP + ICD codes (false sample)
hfpef_icd_negative = hfpef_ids[hfpef_ids['hadm_id'].isin(probnp_negative_ids)]
print(len (hfpef_icd_negative)) 
print(hfpef_icd_negative['subject_id'].nunique()) # e: 54, p: 54

# HFpEF: no proBNP + ICD codes
hfpef_icd_no_probnp = hfpef_ids[~hfpef_ids['hadm_id'].isin(probnp_total_ids)]
print(len (hfpef_icd_no_probnp)) 
print(hfpef_icd_no_probnp['subject_id'].nunique()) # e: 4561, p: 3667

# HFpEF: proBNP + ICD codes + ECG
hfpef_icd_ecg = hfpef_icd_positive[hfpef_icd_positive['subject_id'].isin(ecg_ids)]
print(len (hfpef_icd_ecg)) 
print(hfpef_icd_ecg['subject_id'].nunique()) # e: 4 p: 3


# In[161]:


# filter for HFrEF w/ ICD codes
hfref_icd9 = icd_codes[icd_codes['icd_code'].str.startswith('4282')]
hfref_icd10 = icd_codes[icd_codes['icd_code'].str.startswith('I502')]
hfref_ids = pd.concat([hfref_icd9, hfref_icd10])
hfref_ids = hfref_ids.drop_duplicates('hadm_id')
# for encounter 
print(len(hfref_ids))
# for patient 
print(hfref_ids['subject_id'].nunique())


# In[162]:


# HFrEF: proBNP + ICD codes
hfref_icd_positive = hfref_ids[hfref_ids['hadm_id'].isin(probnp_positive_ids)]
print(len (hfref_icd_positive)) 
print(hfref_icd_positive['subject_id'].nunique()) # e: 1321, p: 1229

# HFrEF: proBNP + ICD codes (false sample)
hfref_icd_negative = hfref_ids[hfref_ids['hadm_id'].isin(probnp_negative_ids)]
print(len (hfref_icd_negative)) 
print(hfref_icd_negative['subject_id'].nunique()) # e: 15, p: 15

# HFrEF: no proBNP + ICD codes
hfref_icd_no_probnp = hfref_ids[~hfref_ids['hadm_id'].isin(probnp_total_ids)]
print(len (hfref_icd_no_probnp)) 
print(hfref_icd_no_probnp['subject_id'].nunique()) # e: 4588, p: 3805

# HFrEF: proBNP + ICD codes + ECG
hfref_icd_ecg = hfref_icd_positive[hfref_icd_positive['subject_id'].isin(ecg_ids)]
print(len (hfref_icd_ecg)) 
print(hfref_icd_ecg['subject_id'].nunique()) # e: 1 p: 1


# In[163]:


# all ICD patients
chf_codes = pd.concat([hfpef_ids, hfref_ids])
chf_codes = chf_codes.drop_duplicates('hadm_id')
chf_codes_ids = list(chf_codes.hadm_id)
print(len(chf_codes)) 
print(chf_codes['subject_id'].nunique()) # e: 12015 p: 9232

icu_notin_icd = icu_stays[~icu_stays['hadm_id'].isin(chf_codes_ids)]
print(len(icu_notin_icd)) # evaluates to 41019

# no ICD but has proBNP
icu_has_probnp = icu_notin_icd[icu_notin_icd['hadm_id'].isin(probnp_total_ids)]
print(len(icu_has_probnp)) 
print(icu_has_probnp['subject_id'].nunique()) # e: 2662, p: 2591

# no ICD but proBNP >200
icu_probnp_positive = icu_notin_icd[icu_notin_icd['hadm_id'].isin(probnp_positive_ids)]
print(len(icu_probnp_positive))
print(icu_probnp_positive['subject_id'].nunique()) # e: 2404, p: 2342

# no ICD but proBNP > 200 + ECGs
icu_probnp_positive_ecg = icu_probnp_positive[icu_probnp_positive['subject_id'].isin(ecg_ids)]
print(len(icu_probnp_positive_ecg)) 
print(icu_probnp_positive_ecg['subject_id'].nunique()) # e: 6, p: 6

# no ICD but proBNP < 200
icu_probnp_negative = icu_notin_icd[icu_notin_icd['hadm_id'].isin(probnp_negative_ids)]
print(len(icu_probnp_negative))  
print(icu_probnp_negative['subject_id'].nunique()) # e: 258, p: 257

# no ICD but proBNP >200 + ECGs
icu_probnp_negative_ecg = icu_probnp_negative[icu_probnp_negative['subject_id'].isin(ecg_ids)]
print(len(icu_probnp_negative_ecg)) 
print(icu_probnp_negative_ecg['subject_id'].nunique()) # e: 1, p: 1


# In[164]:


# no ICD AND no proBNP
icu_no_icd_no_probnp = icu_notin_icd[~icu_notin_icd['hadm_id'].isin(probnp_total_ids)]
print(len(icu_no_icd_no_probnp)) 
print(icu_no_icd_no_probnp['subject_id'].nunique()) # e: 38357, p: 32690

icu_no_icd_no_probnp2 = icu_notin_icd[icu_notin_icd['hadm_id'].isin(probnp_total_ids)]
print(len(icu_no_icd_no_probnp2)) 


# no ICD AND no proBNP + ECGs
icu_no_icd_no_probnp_ecg = icu_no_icd_no_probnp[icu_no_icd_no_probnp['subject_id'].isin(ecg_ids)]
print(len(icu_no_icd_no_probnp_ecg)) 
print(icu_no_icd_no_probnp_ecg['subject_id'].nunique()) # e: 76, p: 67


# In[ ]:





# In[170]:


# export csvs for feature extraction

hfpef_icd_ecg.to_csv("hfpef_icd_ecg.csv", sep=',', index=False, encoding='utf-8')
hfref_icd_ecg.to_csv("hfref_icd_ecg.csv", sep=',', index=False, encoding='utf-8')
icu_probnp_positive_ecg.to_csv("icu_probnp_positive_ecg.csv", sep=',', index=False, encoding='utf-8')
icu_probnp_negative_ecg.to_csv("icu_probnp_negative_ecg.csv", sep=',', index=False, encoding='utf-8')
icu_no_icd_no_probnp_ecg.to_csv("icu_no_icd_no_probnp_ecg.csv", sep=',', index=False, encoding='utf-8')


# In[ ]:





# In[ ]:





# In[ ]:




