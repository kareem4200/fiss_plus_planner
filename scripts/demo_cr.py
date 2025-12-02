import argparse
import os

import yaml

from planners.benchmark.planning import planning
from tqdm import tqdm
import pandas as pd

if __name__ == '__main__':
    repo_dir = os.getcwd()
    parser = argparse.ArgumentParser(description='Demo')
    parser.add_argument('--cfg_file', type=str, default=os.path.join(repo_dir, 'cfgs/demo_config.yaml'), help='specify the config file for the demo')
    args = parser.parse_args()
    
    with open(args.cfg_file, 'r') as file:
        cfg = yaml.safe_load(file)
        file.close()
        
    output_dir = os.path.join(os.getcwd(), cfg['OUTPUT_DIR'])
    input_dir = os.path.join(os.getcwd(), cfg['INPUT_DIR'])
    
    benchmark_results = []
    
    if cfg['FILES']:
        # Only run the specified scenario files under the input directory
        for i, file in enumerate(cfg['FILES']):
            planning(cfg, output_dir, input_dir, file, benchmark_results)
    else:
        # Read all scenario files under the input directory
        for file in tqdm(os.listdir(input_dir)):
            try:
                planning(cfg, output_dir, input_dir, file, benchmark_results)
            except:
                continue
            
    # Save all benchmark results to a single CSV file
    results_df = pd.DataFrame(benchmark_results)
    results_output_path = os.path.join(output_dir, f'benchmark_results_{cfg["PLANNER"]}.csv')
    results_df.to_csv(results_output_path, index=False)
    print("benchmark results saved to:", results_output_path)