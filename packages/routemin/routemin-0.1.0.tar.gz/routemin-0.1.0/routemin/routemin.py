import networkx as nx

def create_graph():
    G = nx.MultiGraph()

    # 山手線の駅をノードとして追加
    stations = [
        '東京', '神田', '秋葉原', '御徒町', '上野', '鶯谷', '日暮里',
        '西日暮里', '田端', '駒込', '巣鴨', '大塚', '池袋',
        '目白', '高田馬場', '新大久保', '新宿', '代々木', '原宿',
        '渋谷', '恵比寿', '目黒', '五反田', '大崎', '品川', '田町',
        '浜松町', '新橋', '有楽町'
    ]

    # 中央線の駅をノードとして追加
    chuo_stations = [
        '新宿', '四ツ谷', '御茶ノ水', '神田', '東京', '中野',
        '高円寺', '阿佐ヶ谷', '荻窪', '西荻窪', '吉祥寺', '三鷹'
    ]
    stations.extend([station for station in chuo_stations if station not in stations])

    # 総武線の駅をノードとして追加
    sobu_stations = [
        '新宿', '大久保', '東中野', '中野', '高円寺', '阿佐ヶ谷', 
        '荻窪', '西荻窪', '吉祥寺', '三鷹', '代々木', '千駄ヶ谷', 
        '信濃町', '四ツ谷', '市ヶ谷', '飯田橋', '水道橋', '御茶ノ水', '秋葉原'
    ]
    stations.extend([station for station in sobu_stations if station not in stations])

    # ダッシュで移動できる駅をノードとして追加
    walk = ['大久保', '新大久保', '御茶ノ水', '御徒町']

    G.add_nodes_from(stations)

    # 駅間のエッジを追加
    G.add_edge('東京', '神田', weight=1.0, line='山手線')
    G.add_edge('神田', '秋葉原', weight=2.0, line='山手線')
    G.add_edge('秋葉原', '御徒町', weight=3.0, line='山手線')
    G.add_edge('御徒町', '上野', weight=2.0, line='山手線')
    G.add_edge('上野', '鶯谷', weight=2.0, line='山手線')
    G.add_edge('鶯谷', '日暮里', weight=2.0, line='山手線')
    G.add_edge('日暮里', '西日暮里', weight=1.0, line='山手線')
    G.add_edge('西日暮里', '田端', weight=2.0, line='山手線')
    G.add_edge('田端', '駒込', weight=2.0, line='山手線')
    G.add_edge('駒込', '巣鴨', weight=2.0, line='山手線')
    G.add_edge('巣鴨', '大塚', weight=2.0, line='山手線')
    G.add_edge('大塚', '池袋', weight=2.0, line='山手線')
    G.add_edge('池袋', '目白', weight=3.0, line='山手線')
    G.add_edge('目白', '高田馬場', weight=2.0, line='山手線')
    G.add_edge('高田馬場', '新大久保', weight=2.0, line='山手線')
    G.add_edge('新大久保', '新宿', weight=2.0, line='山手線')
    G.add_edge('新宿', '代々木', weight=2.0, line='山手線')
    G.add_edge('代々木', '原宿', weight=2.0, line='山手線')
    G.add_edge('原宿', '渋谷', weight=2.0, line='山手線')
    G.add_edge('渋谷', '恵比寿', weight=2.0, line='山手線')
    G.add_edge('恵比寿', '目黒', weight=3.0, line='山手線')
    G.add_edge('目黒', '五反田', weight=2.0, line='山手線')
    G.add_edge('五反田', '大崎', weight=2.0, line='山手線')
    G.add_edge('大崎', '品川', weight=3.0, line='山手線')
    G.add_edge('品川', '田町', weight=2.0, line='山手線')
    G.add_edge('田町', '浜松町', weight=2.0, line='山手線')
    G.add_edge('浜松町', '新橋', weight=2.0, line='山手線')
    G.add_edge('新橋', '有楽町', weight=2.0, line='山手線')
    G.add_edge('有楽町', '東京', weight=2.0, line='山手線')

    # 中央線の駅間のエッジを追加
    G.add_edge('四ツ谷', '新宿', weight=5.0, line='中央線')
    G.add_edge('御茶ノ水', '四ツ谷', weight=5.0, line='中央線')
    G.add_edge('神田', '御茶ノ水', weight=2.0, line='中央線')
    G.add_edge('東京', '神田', weight=1.0, line='中央線')
    G.add_edge('新宿', '中野', weight=5.0, line='中央線')
    G.add_edge('中野', '高円寺', weight=2.0, line='中央線')
    G.add_edge('高円寺', '阿佐ヶ谷', weight=2.0, line='中央線')
    G.add_edge('阿佐ヶ谷', '荻窪', weight=2.0, line='中央線')
    G.add_edge('荻窪', '西荻窪', weight=3.0, line='中央線')
    G.add_edge('西荻窪', '吉祥寺', weight=2.0, line='中央線')
    G.add_edge('吉祥寺', '三鷹', weight=3.0, line='中央線')

    # 総武線の駅間のエッジを追加
    G.add_edge('新宿', '代々木', weight=1.0, line='総武線')
    G.add_edge('代々木', '千駄ヶ谷', weight=2.0, line='総武線')
    G.add_edge('千駄ヶ谷', '信濃町', weight=2.0, line='総武線')
    G.add_edge('信濃町', '四ツ谷', weight=2.0, line='総武線')
    G.add_edge('四ツ谷', '市ヶ谷', weight=2.0, line='総武線')
    G.add_edge('市ヶ谷', '飯田橋', weight=2.0, line='総武線')
    G.add_edge('飯田橋', '水道橋', weight=2.0, line='総武線')
    G.add_edge('水道橋', '御茶ノ水', weight=2.0, line='総武線')
    G.add_edge('御茶ノ水', '秋葉原', weight=3.0, line='総武線')

    # 新宿から中野までのエッジを追加（新たに追加したコード）
    G.add_edge('新宿', '大久保', weight=3.0, line='総武線')
    G.add_edge('大久保', '東中野', weight=2.0, line='総武線')
    G.add_edge('東中野', '中野', weight=2.0, line='総武線')
    G.add_edge('中野', '高円寺', weight=2.0, line='総武線')
    G.add_edge('高円寺', '阿佐ヶ谷', weight=2.0, line='総武線')
    G.add_edge('阿佐ヶ谷', '荻窪', weight=2.0, line='総武線')
    G.add_edge('荻窪', '西荻窪', weight=3.0, line='総武線')
    G.add_edge('西荻窪', '吉祥寺', weight=2.0, line='総武線')
    G.add_edge('吉祥寺', '三鷹', weight=3.0, line='総武線')

    # ダッシュで移動できる駅間のエッジを追加
    G.add_edge('新大久保', '大久保', weight=1.0, line='ダッシュ')
    G.add_edge('御茶ノ水', '御徒町', weight=5.0, line='ダッシュ')

    return G

# 最短経路の計算と結果の表示
def calculate_shortest_path(G, start_station, end_station, include_dash):
    # ダッシュの路線を含まない場合、該当するエッジを削除
    if not include_dash:
        G = G.copy()  # グラフをコピーして元のグラフに影響を与えないようにする
        edges_to_remove = [(u, v, key) for u, v, key, data in G.edges(keys=True, data=True) if data['line'] == 'ダッシュ']
        G.remove_edges_from(edges_to_remove)

    if start_station == end_station:
        return None, "違う駅を選択してください。", None

    try:
        path = nx.shortest_path(G, source=start_station, target=end_station, weight='weight')
        total_time = 0
        path_lines = []  # 経路の路線を格納するリスト
        
        for u, v in zip(path[:-1], path[1:]):
            # MultiGraphでは同じノード間に複数のエッジが存在するときに最小のweightを持つエッジを選択
            # 同じlineであれば変更しないようにする
            min_edge = min(G[u][v].values(), key=lambda x: (x['weight'], path_lines[-1] != x['line'] if path_lines else False))
            total_time += min_edge['weight']
            path_lines.append(min_edge['line'])  # 路線名を追加
        
        # 路線ごとに経路をまとめる
        compact_lines = []
        start = path[0]
        current_line = path_lines[0]

        for i, station in enumerate(path[:-1]):
            if path_lines[i] != current_line:
                compact_lines.append((start, station, current_line))
                start = station
                current_line = path_lines[i]
        compact_lines.append((start, path[-1], current_line))  # 最後の区間を追加


        return path, total_time, compact_lines
    except nx.NetworkXNoPath:
        return None, "経路が存在しません。", None
    except nx.NodeNotFound:
        return None, "駅が見つかりません。", None

# メイン関数（CLIインターフェースや他のPythonスクリプトから呼び出し可能）
def main(start_station, end_station, include_dash=False):
    G = create_graph()
    return calculate_shortest_path(G, start_station, end_station, include_dash)