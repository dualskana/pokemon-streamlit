import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Pokemon",
    layout="wide",
)


st.title("Pokemon")


@st.cache_data
def read_data():
    return pd.read_json("pokemon.json")


pokemon = read_data()

# 在 file_name 增加前缀
pokemon["file_name"] = (
    "https://www.pokemon.cn/play/resources/pokedex" + pokemon["file_name"]
)

# 如果 pokemon_sub_name 不是空字符串 则 将 pokemon_name 和 pokemon_sub_name 合并成 pokemon_name 否则 保留 pokemon_name
pokemon.loc[pokemon["pokemon_sub_name"] != "", "pokemon_name"] = (
    pokemon["pokemon_name"] + "·" + pokemon["pokemon_sub_name"]
)

# 删除 pokemon_sub_name
pokemon.drop(columns=["pokemon_sub_name"], inplace=True)
pokemon.drop(columns=["pokemon_type_id"], inplace=True)
pokemon.drop(columns=["zukan_sub_id"], inplace=True)

# pokemon_type_name 转为列表
pokemon["pokemon_type_name"] = pokemon["pokemon_type_name"].str.split(",")

# pokemon_type_name 包含多个属性类型，统计出所有属性类型
pokemon_type_all = (
    pokemon["pokemon_type_name"].explode().value_counts().to_frame().reset_index()
)

# pokemon_type_all 中增加 编号
types = st.multiselect(
    "筛选属性",
    pokemon_type_all["pokemon_type_name"],
    [],
    placeholder="请选择属性",
)

if types != []:
    # 筛选数据, 只要pokemon_type_name 中出现了 types 中的元素 就保留
    pokemon = pokemon[
        pokemon["pokemon_type_name"].apply(lambda x: any(item in x for item in types))
    ]

st.data_editor(
    pokemon,
    column_config={
        "file_name": st.column_config.ImageColumn(label="图片"),
        "pokemon_name": "名称",
        "pokemon_sub_name": "副名称",
        "weight": "体重/kg",
        "height": "身高/m",
        "zukan_id": "编号",
        "pokemon_type_name": st.column_config.ListColumn(label="属性"),
    },
    hide_index=True,
    use_container_width=True,
)
