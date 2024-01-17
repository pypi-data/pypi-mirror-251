# パッケージのインポート
import requests
from bs4 import BeautifulSoup
import itertools
import networkx as nx
import matplotlib.pyplot as plt


def main():
    # URL(にじさんじ非公式wiki)
    url = "https://wikiwiki.jp/nijisanji/コラボ一覧表"

    # URLからページ内容を取得
    r = requests.get(url)
    html_contents = r.text

    # HTML構文解析
    html_soup = BeautifulSoup(html_contents, 'html.parser')

    # コラボ一覧表のテーブルを抽出
    combi_table = html_soup.find("div", class_="wikiwiki-tablesorter-wrapper").find("table")

    # テーブルの項目名の抽出
    headers = []
    for header in combi_table.find("tr").find_all("th"):
        headers.append(header.text)

    # 最初の行(項目名)以降の行に対して処理(各コラボの 人数/コラボ名/詳細の有無/メンバー の抽出)
    values = []
    for row in combi_table.find_all("tr")[1:]:
        temp_list = [] # 一時格納用リスト

        # th:コラボ名, td:それ以外の情報
        for col in row.find_all(["th", "td"]):
            temp_list.append(col.text)

        values.append(temp_list)





    # 名前を数値に置換していく

    s = set()
    name_to_int = {}

    # コラボしたメンバーの重複なしのセットを作成
    for i in range(len(values)):
        for name in values[i][3].split(", "):
            s.add(name)

    # 作成したセットから各メンバーの名前に番号を振る
    for name, i in zip(s, range(1, len(values)+1)):
        s_dict = {name:i}
        name_to_int.update(s_dict)

    # コラボしたメンバーに対応する数値の組を作っていく
    for i in range(len(values)):
        temp_list = []
        combi = []
        for name in values[i][3].split(", "):
            number = name_to_int[name]
            temp_list.append(number)

        for pair in itertools.combinations(temp_list, 2):
                combi.append(pair)

        values[i][3] = combi

    # 後でネットワークノードにラベルを付けるための辞書
    int_to_name = {v:k for k, v in name_to_int.items()}




    # ネットワークグラフの作成
    G = nx.Graph()
    G.add_nodes_from(list(range(1, len(s)+1)))

    for i in range(len(values)):
        for edge in values[i][3]:
            G.add_edge(edge[0], edge[1])

    # 各ノードにラベルを付与
    H = nx.relabel_nodes(G, int_to_name)
    # # Gephi用にGraphML形式に変換
    # nx.write_graphml_lxml(H, "nijisanji_combi.graphml")


    # # ネットワークグラフの描画
    # nx.draw(G, with_labels=True)


    # コラボの平均値グラフ
    Deg_list = [d for n, d in H.degree()]

    # ヒストグラムの表示
    plt.hist(Deg_list)

    # タイトルの設定
    plt.title("Number of collaborations by livers.")

    # 軸のラベルの設定
    plt.xlabel("Number of Collaborations")
    plt.ylabel("Number of Livers")

    # グラフの表示
    plt.show()


    # 次数中心性(どれほど多くの人とコラボしているかを測る指標)コラボ人数ランキング
    deg_C = nx.degree_centrality(H)
    # 次数中心性が大きい順にソート
    deg_C_list = sorted(deg_C.items(), key=lambda x:x[1], reverse=True)
    print('コラボ数ランキング',deg_C_list)
 

    print('--------------------------------------------------------')

    # 媒介中心性("橋渡し役"としてどれぐらい重要かを測る指標)
    bet_C = nx.betweenness_centrality(H)
    bet_C_list = sorted(bet_C.items(), key=lambda x:x[1], reverse=True)
    print('コラボの橋渡し役ランキング',bet_C_list)



if __name__ =='__main__':
    main()