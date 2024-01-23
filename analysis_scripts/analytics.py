import pandas as pd
import matplotlib.pyplot as plt
import datetime
import re

anon_pattern = (r'Patient Name|D.O.B|DOB|NHS|Referring Hospital|Referring Consultant')
end_pattern = (r'4ways|GMC|Dr\b|Radiologist|Sonographer|Radiographer|Cardiologist|[0-9]{5,7}')

def anonymise(report) :
    report = str(report)
    lines =  report.split('\n')
    processed_report = ''
    for i, l in enumerate(lines) :
        if re.findall(end_pattern, l, re.IGNORECASE) :
            return processed_report
        if i < len(lines)-1 :
            if re.findall(end_pattern, lines[i+1], re.IGNORECASE) :
                return processed_report
        if re.findall(anon_pattern, l, re.IGNORECASE) :
            pass
        else :
            processed_report+='\n'+l

    return processed_report

def within_time_interval(t, reference_time, delta, direction='forwards') :
    ''' 
    Test if time t lies within an interval of width |delta| (days) of reference_time
    Allowable directions are 'forwards' ie if t is later than reference_time by
    no more than delta, 'backwards' if t is earlier than reference_time by no more
    than delta, or 'centred' ie |t-reference_time|<delta/2
    t and reference_time are datetime objects, delta is a numeric type
    '''
    delta = abs(delta)
    one_day = datetime.timedelta(days=1)
    zero_time = datetime.timedelta(days=0)
    dt = pd.to_datetime(t, dayfirst=True)-pd.to_datetime(reference_time, dayfirst=True)
    if direction == 'forwards':
        return (dt > zero_time) and (dt < delta*one_day)
    dt = -dt
    if direction == 'backwards':
        return (dt > zero_time) and (dt < delta*one_day)
    if direction == 'centred' :
        return abs(dt) < delta*one_day/2
    print ("Invalid 'direction' argument in function 'within_time_interval'")
    raise SystemExit(0)

def text_template(modality):
    return f'''
## Inpatient {modality}

Inpatient imaging under 24h

![]({{{{'/assets/images/IP{modality}_imaging_24h.png' | relative_url}}}})

Inpatient reporting under 4h

![]({{{{'/assets/images/IP{modality}_reporting_4h.png' | relative_url}}}})
'''

def process_csv(csv_path, assets_folder, md_file):

    modalities = ['CT', 'MRI', 'US']
    page = '''---
layout: post
title:  "Inpatient statistics"
date:   2024-01-01 18:23:09 +0000
categories: jekyll update
---
For the first two weeks of January 2024


'''

    for modality in modalities :
    
        risData = pd.read_csv(csv_path, low_memory=False, parse_dates=True, dayfirst=True)
        risData = risData.drop_duplicates(subset=["Accession No"])
        risData = risData[risData['Is Addendum Report'] == 'No']
        risData = risData[risData['Visit Type'] == 'In Patient']
        risData = risData[risData['Modality'] == modality]

        risData['IP within 1 day'] = ''
        risData['IP report within 4h'] = ''

        for idx, row in risData.iterrows() :
            less_than_day = within_time_interval(row['Authorised Date'], row['Requested Date'], 1.0)
            if less_than_day :
                risData['IP within 1 day'].loc[idx] = 'Within 1 day'
            else :
                risData['IP within 1 day'].loc[idx] = 'Exceeded 1 day'
            
            rep_less_than_4h = within_time_interval(row['Authorised Date'], row['Completed Date'], 4.0/24)
            if rep_less_than_4h :
                risData['IP report within 4h'].loc[idx] = 'Within 4h'
            else :
                risData['IP report within 4h'].loc[idx] = 'Exceeded 4h'


        value_counts = risData['IP within 1 day'].value_counts()

        # Plotting a pie chart with angles proportional to the counts
        plt.figure(figsize=(8, 8))
        plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title(f'Inpatient {modality} within 1 day')
        plt.savefig(f'{assets_folder}IP{modality}_imaging_24h.png')

        value_counts = risData['IP report within 4h'].value_counts()

        # Plotting a pie chart with angles proportional to the counts
        plt.figure(figsize=(8, 8))
        plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title(f'Inpatient {modality} reporting within 4 hours')
        plt.savefig(f'{assets_folder}IP{modality}_reporting_4h.png')
    
        page = page + '\n' + text_template(modality) + '\n'
    
    
    with open(md_file, 'w') as f :
        f.write(page)

# csv_path='../data/Jan24_1.csv'
# asset_folder='../assets/images/'
# md_file = '../_posts/2024-01-07-inpatient.markdown'
# process_csv(csv_path, asset_folder, md_file)
