# -*- coding: utf-8 -*-
import json
import sys
import io
import contextlib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def execute_notebook():
    notebook_path = "Seasonal_Agriculture_Performance_Analysis.ipynb"
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    execution_context = {
        '__name__': '__main__',
        'display': lambda x: print(x)
    }
    
    exec_count = 1
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            code = "".join(cell['source'])
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            try:
                with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                    # Intercept display function for tabular data
                    def custom_display(obj):
                        if isinstance(obj, (pd.DataFrame, pd.Series)):
                            print(obj.to_string())
                        else:
                            print(repr(obj))
                    execution_context['display'] = custom_display
                    exec(code, execution_context)
                    
                output_text = stdout_capture.getvalue()
                err_text = stderr_capture.getvalue()
                
                outputs = []
                if output_text:
                    outputs.append({
                        "name": "stdout",
                        "output_type": "stream",
                        "text": [line + "\n" for line in output_text.splitlines()]
                    })
                if err_text:
                    # Filter out non-fatal deprecation warnings
                    cleaned_err = [line for line in err_text.splitlines() if "warning" not in line.lower()]
                    if cleaned_err:
                        outputs.append({
                            "name": "stderr",
                            "output_type": "stream",
                            "text": [line + "\n" for line in cleaned_err]
                        })
                        
                cell['outputs'] = outputs
                cell['execution_count'] = exec_count
                exec_count += 1
                print(f"Executed code cell {exec_count-1} successfully.")
                
            except Exception as e:
                print(f"Error in cell {exec_count}: {e}")
                cell['outputs'] = [{
                    "ename": type(e).__name__,
                    "evalue": str(e),
                    "output_type": "error",
                    "traceback": [str(e)]
                }]
                cell['execution_count'] = exec_count
                exec_count += 1
                
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)
        
    print(f"All code cells in {notebook_path} executed and populated with live outputs!")

if __name__ == '__main__':
    execute_notebook()
