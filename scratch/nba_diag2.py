import pandas as pd,requests,io
u="https://raw.githubusercontent.com/llimllib/nba_data/main/data/gamelog_2025.parquet"
d=pd.read_parquet(io.BytesIO(requests.get(u,timeout=120).content)); d.columns=[c.lower() for c in d.columns]
d=d[d.game_id.astype(str).str.zfill(10).str.startswith("002")].copy()
d["gid"]=d.game_id.astype(str).str.zfill(10)
d["homeflag"]=d.matchup.str.contains(r"vs\.",regex=True).astype(int)
z=d.groupby("gid").agg(rows=("gid","size"),homes=("homeflag","sum"),dates=("game_date","nunique"))
bad=z[(z.homes!=1)|(z.rows!=2)|(z.dates!=1)]
print("row count",len(d),"unique",d.gid.nunique(),"home rows",d.homeflag.sum(),"away rows",(1-d.homeflag).sum())
print("bad pairing count",len(bad))
print(bad.to_string())
print(d[d.gid.isin(bad.index)][["gid","game_date","team_abbreviation","matchup","wl","plus_minus"]].sort_values(["gid","team_abbreviation"]).to_string(index=False))
