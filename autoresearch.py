from __future__ import annotations
import argparse, csv, json, time
from pathlib import Path
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def evaluate(config: dict, X_train, X_test, y_train, y_test):
    model=make_pipeline(StandardScaler(),LogisticRegression(C=config["C"],max_iter=config["max_iter"],random_state=42))
    start=time.time(); model.fit(X_train,y_train); score=accuracy_score(y_test,model.predict(X_test))
    return float(score),round(time.time()-start,4)

def run(iterations=6, output="artifacts/autoresearch_results.csv"):
    X,y=make_classification(n_samples=700,n_features=12,n_informative=8,n_redundant=2,class_sep=1.15,random_state=42)
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    configs=[{"C":.01,"max_iter":100},{"C":.03,"max_iter":200},{"C":.1,"max_iter":300},{"C":.3,"max_iter":300},{"C":1.0,"max_iter":500},{"C":3.0,"max_iter":500}]
    rows=[]; best=-1
    for i,config in enumerate(configs[:iterations],1):
        score,seconds=evaluate(config,X_train,X_test,y_train,y_test); decision="keep" if score>best else "discard"
        if decision=="keep": best=score
        rows.append({"iteration":i,**config,"accuracy":score,"elapsed_s":seconds,"decision":decision})
    path=Path(output); path.parent.mkdir(exist_ok=True)
    with path.open("w",newline="") as f: writer=csv.DictWriter(f,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    summary={"iterations":len(rows),"best_accuracy":best,"best_config":next(r for r in rows if r["accuracy"]==best),"seed":42,"results":str(path)}
    Path("artifacts/autoresearch_summary.json").write_text(json.dumps(summary,indent=2)); return summary

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--iterations",type=int,default=6); args=p.parse_args(); print(json.dumps(run(args.iterations),indent=2))
