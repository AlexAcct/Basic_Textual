import pandas as pd
data=pd.read_csv(r'directory')
df=pd.DataFrame(data)
text=df.componenttext
g=df[['keydevid', 'componentorder']]

import language_tool_python
tool = language_tool_python.LanguageTool('en-US')
from tqdm import tqdm
g1=[len(tool.check(str(comp))) for comp in tqdm(text)]
g['grammar']=g1
g.to_csv(r'directory', index=False)