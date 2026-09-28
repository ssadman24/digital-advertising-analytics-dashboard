import pandas as pd, requests, io
u="https://raw.githubusercontent.com/llimllib/nba_data/main/data/gamelog_2025.parquet"
r=requests.get(u,timeout=120); r.raise_for_status()
df=pd.read_parquet(io.BytesIO(r.content)); df.columns=[c.lower() for c in df.columns]
gid=df.game_id.astype(str).str.zfill(10)
x=df[gid.str.startswith("002")].copy()
x["gid"]=x.game_id.astype(str).str.zfill(10)
x["opponent"]=x.matchup.str.extract(r"(?:vs\\.|@)\\s+([A-Z]{2,3})",expand=False)
counts=x.groupby("gid").size()
bad=counts[counts.ne(2)]
print("rows",len(x),"unique",x.gid.nunique(),"bad_game_ids",bad.to_dict())
print("bad rows")
print(x[x.gid.isin(bad.index)][["gid","game_date","team_abbreviation","matchup","opponent","wl","plus_minus"]].to_string(index=False))
teams=set(x.team_abbreviation.dropna().unique())
badopp=x[~x.opponent.isin(teams)]
print("bad opponent rows",len(badopp))
print(badopp[["gid","game_date","team_abbreviation","matchup","opponent"]].to_string(index=False))
