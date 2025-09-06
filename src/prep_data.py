import pandas as pd
import argparse
import os
import csv

def main(source, outpath):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    first = True

    for chunk in pd.read_csv(source, usecols=["paperID","title","abstract"], chunksize=50000):
        # Drop rows with missing title or abstract
        chunk = chunk.dropna(subset=["title","abstract"])

        # Append each chunk to the output file
        chunk.to_csv(outpath, mode="a", index=False, header=first, quoting=csv.QUOTE_MINIMAL)
        first = False

    print(f"Cleaned file saved to {outpath}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    main(args.input, args.out)