
import os
import pandas as pd

from mailmerge import MailMerge

template_dir = "docs"
output_dir   = "output"

# import the keys
df = pd.read_excel('Dennenhof-adressen.xlsx')
for idx, user in df.iterrows():
    key = user['secret_key']
    adr = user['Huisnr']
    docx_filename = os.path.join( output_dir, f'Dennenhof-{adr}-{key}.docx')
    
    with MailMerge(os.path.join(template_dir, 'letter-template.docx')) as doc:
        doc.merge(secret_key=key, huisnr=str(adr))
        doc.write(docx_filename)

    print(f'Saved {docx_filename}')
 