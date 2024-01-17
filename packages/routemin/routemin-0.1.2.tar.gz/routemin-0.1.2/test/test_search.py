import unittest
from routemin.routemin import create_graph, calculate_shortest_path

class TestRouteSearch(unittest.TestCase):

    def test_calculate_shortest_path(self):
        G = create_graph()  # テスト用のグラフを作成
        start_station = '三鷹'
        end_station = '大崎'
        include_dash = False  # ダッシュを含まない

        path, total_time, compact_lines = calculate_shortest_path(G, start_station, end_station, include_dash)

        # 期待される結果に基づいて検証
        self.assertIsNotNone(path)  # 経路がNoneでないことを確認
        self.assertIn('三鷹', path)  # 新宿が経路に含まれていることを確認
        self.assertIn('大崎', path)  # 東京が経路に含まれていることを確認

if __name__ == '__main__':
    unittest.main()
