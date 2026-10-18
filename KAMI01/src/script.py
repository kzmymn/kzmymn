"""紙芝居版 試作：冒頭〜S01〜S02 の台本と絵の割り当て。

元原稿（Hototogisu_Three_Samurai_Kamishibai.pdf の S01・S02）を、
紙芝居の語りとして自然な日本語に直したもの。事実の範囲は元原稿から広げていない。

1ビート = 語りの一区切り。card が絵、say が読み上げ（表記の読み違い対策を含む）。
text は字幕ファイル（SRT）用。動画の画面には語りの文字を出さない。
"""

BEATS = [
    # ---- 冒頭 ----
    dict(card="hototogisu", text="ほととぎすの句で、よく比べられる三人の武将がいます。", pause=0.5),
    dict(card="hototogisu", text="けれど、本当の三人のあいだには、句だけでは分からない、深いつながりがありました。", pause=0.6),
    dict(card="hototogisu", text="さあ、はじまり、はじまり。", pause=0.2, claps="roll"),
    dict(card="title", text=None, hold=3.4),

    # ---- S01 三人 ----
    dict(card="nobunaga", text="織田信長。", pause=0.45, name="織田信長"),
    dict(card="hideyoshi", text="豊臣秀吉。", pause=0.45, name="豊臣秀吉"),
    dict(card="ieyasu", text="徳川家康。", pause=0.6, name="徳川家康"),
    dict(card="trio", text="三人とも、戦国の世を代表する武将です。", pause=0.3),
    dict(card="trio", text="あちこちで争っていた武士たちをまとめ、日本がひとつになっていく流れの中で、大きな働きをしました。", pause=0.45),
    dict(card="trio", text="けれど、三人が仲間どうしで、順番に天下を受け継いだわけではありません。", pause=0.35),
    dict(card="rivals", text="もとの立場もちがえば、敵として戦ったこともあるのです。", pause=0.6),
    dict(card="trio", text="このお話では、三人の人となりを知ってから、それぞれの人生の大事な場面を、ひとつずつ見ていきます。", pause=0.5),
    dict(card="omi", text="妹の嫁ぎ先と戦った、信長。", pause=0.45),
    dict(card="rivals", text="ぶつかり合った、秀吉と家康。", pause=0.45),
    dict(card="temple", text="そして、家康に背いた家臣の、その後。", pause=0.6),
    dict(card="trio", text="まずは、三人の関係から、ひもといていきましょう。", pause=0.9),

    # ---- S02 信長と大名 ----
    dict(card="nobunaga2", text="信長は、尾張の国の大名でした。", pause=0.35, name="織田信長"),
    dict(card="map", text="尾張は、いまの愛知県の西のほうです。", pause=0.5),
    dict(card="nobunaga3", text="大名というのは、自分の領地を治め、自分の軍勢を持つ、武士のかしらのこと。", pause=0.45),
    dict(card="kyoto", text="そのころの日本では、あちこちの大名が、土地をめぐって争っていました。", pause=0.35),
    dict(card="kyoto", text="京都には天皇と朝廷があり、将軍もいました。", pause=0.3),
    dict(card="kyoto", text="けれど、その命令だけで、国じゅうの争いを止めることは、できなかったのです。", pause=0.55),
    dict(card="rice", text="勢力を広げるには、戦う軍勢がいります。", pause=0.3),
    dict(card="rice", text="軍勢を養うには、領地でとれるお米と、人々の働きが欠かせません。", pause=0.5),
    dict(card="nobunaga4", text="信長も、まわりの勢力と戦ったり、手を結んだりしながら、治める土地を広げていきました。", pause=0.4),
    dict(card="nobunaga4", text="そして、やがては京都の政治にまで、大きな力を持つようになるのです。", pause=1.6),
]

# 絵の割り当て。cam は (中心x, 中心y, 見える幅の割合) の始点→終点。画像は左右反転しない（着物の合わせが逆になるため）
CARDS = {
    "hototogisu": dict(kind="img", src="hototogisu.png", cam=((0.5, 0.5, 1.0), (0.72, 0.42, 0.78))),
    "title": dict(kind="title", src="hototogisu.png", cam=((0.72, 0.42, 0.78), (0.70, 0.43, 0.74))),
    "nobunaga": dict(kind="img", src="nobunaga.png", cam=((0.62, 0.45, 0.9), (0.68, 0.36, 0.62))),
    "hideyoshi": dict(kind="img", src="hideyoshi.png", cam=((0.62, 0.45, 0.9), (0.70, 0.38, 0.62))),
    "ieyasu": dict(kind="img", src="ieyasu.png", cam=((0.6, 0.5, 0.95), (0.74, 0.36, 0.62))),
    "trio": dict(kind="trio"),
    "rivals": dict(kind="rivals"),
    "omi": dict(kind="img", src="omi_castle.png", cam=((0.45, 0.5, 1.0), (0.78, 0.35, 0.6))),
    "temple": dict(kind="img", src="temple.png", cam=((0.5, 0.5, 1.0), (0.72, 0.6, 0.7))),
    "nobunaga2": dict(kind="img", src="nobunaga.png", cam=((0.7, 0.3, 0.55), (0.66, 0.38, 0.75))),
    "map": dict(kind="map"),
    "nobunaga3": dict(kind="img", src="nobunaga.png", cam=((0.62, 0.5, 1.0), (0.80, 0.33, 0.55))),
    "kyoto": dict(kind="kyoto"),
    "rice": dict(kind="img", src="hideyoshi.png", crop=(0.0, 0.18, 0.5, 0.62), bright=1.35, cam=((0.45, 0.5, 1.0), (0.5, 0.55, 0.8))),
    "nobunaga4": dict(kind="img", src="nobunaga.png", cam=((0.6, 0.5, 0.75), (0.70, 0.33, 0.5))),
}

# 三人並び・対決の切り抜き（元画像に対する顔の位置と、縦の範囲）
FACES = {
    "nobunaga.png": (0.70, 0.52),
    "hideyoshi.png": (0.73, 0.52),
    "ieyasu.png": (0.77, 0.52),
}
