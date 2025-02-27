import pandas as pd

def csv_for_table(path: str = None, df=None, to_dict=True, aggf={}) -> list:
    if path is None and df is None:
        raise ValueError("You must provide a path or a dataframe")
    
    if path:
        df = pd.read_csv(path)
    
    # Convertir las columnas relevantes a tipo string
    df['tipos_envase'] = df['tipos_envase'].astype(str)
    df['guias_remision'] = df['guias_remision'].astype(str)
    df['cantidades'] = df['cantidades'].astype(str)
    
    aggF = {
        "guias_remision": lambda x: list(item for sublist in x for item in sublist),
        "tipos_envase": lambda x: list(item for sublist in x for item in sublist),
        "cantidades": lambda x: list(item for sublist in x for item in sublist),
        "fecha": "first"
    }
    
    if aggf:
        aggF.update(aggf)
    
    data = df \
        .assign(
            tipos_envase=lambda x: x['tipos_envase'].str.split(','),
            guias_remision=lambda x: x['guias_remision'].str.split(','),
            cantidades=lambda x: x['cantidades'].str.split(',')
        ) \
        .groupby("id") \
        .agg(aggF) \
        .reset_index() \
        .sort_values(by='fecha', ascending=True)
    
    if to_dict:
        data = data.to_dict("records")
    
    return data
