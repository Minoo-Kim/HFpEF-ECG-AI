#!/usr/bin/env python
# coding: utf-8

# In[170]:


import pandas as pd
import os

# opening relevant files
icd_codes = pd.read_csv('/Users/minookim/Desktop/LCICM/mimic4_ehr/diagnoses_icd.csv')
icu_stays = pd.read_csv('/Users/minookim/Desktop/LCICM/mimic4_ehr/icustays.csv')
lab_events = pd.read_csv('/Users/minookim/Desktop/LCICM/mimic4_ehr/labevents.csv')
lab_events_id = pd.read_csv('/Users/minookim/Desktop/LCICM/mimic4_ehr/d_labitems.csv')
lab_events = pd.merge(lab_events, lab_events_id, on='itemid', how='left')
print ("File reading complete")


# In[171]:


# total ICU population
icu_stays = icu_stays.drop_duplicates("subject_id")
icu_ids = list(icu_stays.subject_id)
print(len(icu_ids)) # evalutes to 50920


# In[172]:


# filter every file with confirmed ICU stay
icd_codes = icd_codes[icd_codes['subject_id'].isin(icu_ids)]
lab_events = lab_events[lab_events['subject_id'].isin(icu_ids)]


# In[173]:


# extract patient IDs with 12-lead ECGs
ecg_ids = [f.name for f in os.scandir('/Users/minookim/Desktop/LCICM/ecg_extraction/mimic-iv-ecg/files/')]
ecg_ids.remove(".DS_Store")
# take out p and convert to number
ecg_ids = [id[1:] for id in ecg_ids]
ecg_ids = [int(i) for i in ecg_ids]
print(len(res)) # evaluates to 93
print(ecg_ids)


# In[174]:


# filter for HFpEF w/ ICD codes
hfpef_icd9 = icd_codes[icd_codes['icd_code'].str.startswith('4283')]
hfpef_icd10 = icd_codes[icd_codes['icd_code'].str.startswith('I503')]
hfpef_ids = pd.concat([hfpef_icd9, hfpef_icd10])
hfpef_ids = hfpef_ids.drop_duplicates('subject_id')
print(len(hfpef_ids))


# In[175]:


probnp_total = lab_events[(lab_events['itemid'] == 50963)]
probnp_total = probnp_total.drop_duplicates('subject_id')
print(len(probnp_total))

# filter for proBNP over and under 200

probnp_positive = probnp_total[probnp_total['valuenum'] > 200]
probnp_positive = probnp_positive.drop_duplicates('subject_id')
probnp_positive_ids = list(probnp_positive.subject_id)
print(len(probnp_positive))

# < 200
probnp_negative = probnp_total[probnp_total['valuenum'] <= 200]
probnp_negative = probnp_negative.drop_duplicates('subject_id')
probnp_negative_ids = list(probnp_negative.subject_id)
print(len(probnp_negative_ids))

print(probnp_total['valuenum'].isna().sum()) # patients with no proBNP value" 554


# In[176]:


# HFpEF: proBNP + ICD codes
hfpef_icd_positive = hfpef_ids[hfpef_ids['subject_id'].isin(probnp_positive_ids)]
print(len (hfpef_icd_positive)) # evaluates to 4669

# HFpEF: proBNP + ICD codes (false sample)
hfpef_icd_negative = hfpef_ids[hfpef_ids['subject_id'].isin(probnp_negative_ids)]
print(len (hfpef_icd_negative)) # evaluates to 408

# HFpEF: proBNP + ICD codes + ECG
hfpef_icd_ecg = hfpef_icd_positive[hfpef_icd_positive['subject_id'].isin(ecg_ids)]
print(len (hfpef_icd_ecg)) # evaluates to 5


# In[177]:


# filter for HFpEF w/ ICD codes
hfref_icd9 = icd_codes[icd_codes['icd_code'].str.startswith('4282')]
hfref_icd10 = icd_codes[icd_codes['icd_code'].str.startswith('I502')]
hfref_ids = pd.concat([hfref_icd9, hfref_icd10])
hfref_ids = hfref_ids.drop_duplicates('subject_id')
print(len(hfref_ids))


# In[178]:


# HFrEF: proBNP + ICD codes
hfref_icd_positive = hfref_ids[hfref_ids['subject_id'].isin(probnp_positive_ids)]
print(len (hfref_icd_positive)) # evaluates to 4669

# HFrEF: proBNP + ICD codes (false sample)
hfref_icd_negative = hfref_ids[hfref_ids['subject_id'].isin(probnp_negative_ids)]
print(len (hfref_icd_negative)) # evaluates to 408

# HFrEF: proBNP + ICD codes + ECG
hfref_icd_ecg = hfref_icd_positive[hfref_icd_positive['subject_id'].isin(ecg_ids)]
print(len (hfref_icd_ecg)) # evaluates to 5


# In[179]:


# all ICD patients
chf_codes = pd.concat([hfpef_ids, hfref_ids])
chf_codes = chf_codes.drop_duplicates("subject_id")
chf_codes_ids = list(chf_codes.subject_id)
print(len(chf_codes)) # evaluates to 12426
icu_notin_icd = icu_stays[-icu_stays['subject_id'].isin(chf_codes_ids)]
print(len(icu_notin_icd))

# no ICD but proBNP >200
icu_probnp_positive = icu_notin_icd[icu_notin_icd['subject_id'].isin(probnp_positive_ids)]
print(len(icu_probnp_positive))  # evalutes to 4514

# no ICD but proBNP >200 + ECGs
icu_probnp_positive_ecg = icu_probnp_positive[icu_probnp_positive['subject_id'].isin(ecg_ids)]
print(len(icu_probnp_positive_ecg))

# no ICD but proBNP <200
icu_probnp_negative = icu_notin_icd[icu_notin_icd['subject_id'].isin(probnp_negative_ids)]
print(len(icu_probnp_negative))  # evalutes to 1507

# no ICD but proBNP >200 + ECGs
icu_probnp_negative_ecg = icu_probnp_negative[icu_probnp_negative['subject_id'].isin(ecg_ids)]
print(len(icu_probnp_negative_ecg))




# In[180]:


# no ICD AND no proBNP
probnp_total_ids = list(probnp_total.subject_id)
icu_no_icd_no_probnp = icu_notin_icd[-icu_notin_icd['subject_id'].isin(probnp_total_ids)]
print(len(icu_no_icd_no_probnp)) #prints to 32167


# In[ ]:





# In[ ]:





# In[ ]:




