"""EP01 v3.1 のビート定義。

1ビート = ナレーション1区間 = 字幕1枚 = 画面の1変化。
  scene : 画面の場面ID（render.py の SCENES）
  text  : 字幕に出す文（\n で改行位置を指定）
  say   : 読み上げ用の文（読み間違い対策。省略時は text）
  head  : 大見出し（省略時は直前の見出しを維持、"" で消す）
  pause : このビートの後の無音（秒）
"""

BEATS = [
    # --- 冒頭：連絡できない ---
    dict(scene="hook", head="30分遅刻。", text="待ち合わせに、30分遅刻。", pause=0.35),
    dict(scene="hook", head="「遅れる」が送れない", text="でも、「ごめん、遅れる」が送れません。", pause=0.45),
    dict(scene="hook", head="", text="携帯を持っていない二人は、\nどうやって会っていたのでしょう。", pause=0.6),

    # --- 電話はある。でも本人がいない ---
    dict(scene="phone", head="公衆電話なら？", text="「公衆電話から、かければいいのでは？」", pause=0.35),
    dict(scene="phone", head="相手は、もう外。", text="ところが、相手はもう家を出ています。", pause=0.3),
    dict(scene="phone", head="本人には届かない", text="家の電話を鳴らしても、\n駅で待つ本人は出られません。", pause=0.45),
    dict(scene="phone", head="電話はある。でも、本人がいない。", text="電話はある。でも、かける先に本人がいない。", pause=0.3),
    dict(scene="phone", text="ここが、今の待ち合わせとの大きな違いです。", pause=0.7),

    # --- 再現の宣言（短く） ---
    dict(scene="recon", head="", text="1980年代後半を想定した、\n架空の二人で再現してみます。",
         say="千九百八十年代後半を想定した、架空の二人で再現してみます。", pause=0.7),

    # --- 約束の場所 ---
    dict(scene="plan", head="午後2時、駅で。", text="午後2時、駅で待ち合わせ。", pause=0.3),
    dict(scene="plan", head="「駅で」の、どこ？", text="ただし、「駅で」だけでは心配です。", pause=0.25),
    dict(scene="plan", text="改札の中？ 外？ 東口？ 西口？", say="改札の中？ 外？ 東口？ 西口？", pause=0.4),
    dict(scene="plan", head="写真で「ここ」は送れない", text="今なら「ここにいる」と写真を送れます。\nでも、この二人にはできません。", pause=0.35),
    dict(scene="plan", head="東口の改札を出て、時計の下", text="そこで、「東口の改札を出て、時計の下」と決めました。", pause=0.7),

    # --- 当日 ---
    dict(scene="missed", head="当日、電車を逃す", text="ところが当日、一人が電車を逃してしまいます。", pause=0.4),
    dict(scene="missed", head="何も届かない", text="待つ側には、何も届きません。", pause=0.3),
    dict(scene="missed", text="遅れている？ 場所を間違えた？ 忘れた？", pause=0.6),

    # --- 動くか、待つか ---
    dict(scene="dilemma", head="探しに行く？", text="別の出口を探しに行けば、会えるかも。", pause=0.25),
    dict(scene="dilemma", head="動いた間に来たら？", text="でも、自分が動いた間に相手が来たら？", pause=0.3),
    dict(scene="dilemma", head="すれ違い", text="二人とも探し回ると、\nかえってすれ違うかもしれません。", pause=0.6),

    # --- 家族経由の伝言 ---
    dict(scene="relay", head="家に伝言を頼む", text="遅れる側が、公衆電話から\n自分の家に伝言を頼む手もあります。",
         say="遅れるがわが、公衆電話から自分の家に伝言を頼む手もあります。", pause=0.3),
    dict(scene="relay", head="待つ側が電話しないと届かない", text="ただ、待つ側がその家へ電話しない限り、\n伝言は届きません。", pause=0.3),
    dict(scene="relay", text="事前に決めていなければ、伝わる保証はありません。", pause=0.7),

    # --- 伝言板 ---
    dict(scene="board", head="駅の伝言板", text="そこで使われた道具の一つが、駅の伝言板。", pause=0.3),
    dict(scene="board", head="改札横や待合室の黒板", text="改札横や待合室の黒板に、\n相手への言葉を残す方法です。", pause=0.35),
    dict(scene="board", head="", text="「東口で待っています」。\nあるいは、「先に喫茶店へ行きます」。", pause=0.45),
    dict(scene="board", text="相手が板を見れば、居場所が分かる。", pause=0.35),

    # --- 今のメッセージとの比較 ---
    dict(scene="compare", head="通知なし・既読なし", text="ただし、通知は来ません。既読も付きません。", pause=0.3),
    dict(scene="compare", head="誰でも読める", text="周りの人にも読めます。", pause=0.3),
    dict(scene="compare", text="今のメッセージとは、ずいぶん違いますね。", pause=0.8),

    # --- 結末 ---
    dict(scene="reunion", head="30分遅れで、会えた", text="今回の二人は、30分遅れで会えました。", pause=0.3),
    dict(scene="reunion", head="時計の下から動かなかった", text="待つ側が、約束した時計の下から\n動かなかったからです。", pause=0.4),
    dict(scene="reunion", head="", text="もし違う出口へ探しに行っていたら、\n結末は変わったかもしれません。", pause=0.5),
    dict(scene="reunion", head="出かける前の約束", text="連絡できないからこそ、\n出かける前の約束が二人を助けます。", pause=0.35),
    dict(scene="reunion", text="場所、時間、会えなかった場合の行動。", pause=0.8),

    # --- 注意と史実 ---
    dict(scene="caveat", head="方法は人それぞれ", text="もちろん、時代や地域、人によって、\n使った方法は違います。", pause=0.25),
    dict(scene="caveat", text="伝言板があった駅も、なかった駅もあります。", pause=0.5),
    dict(scene="history", head="全国一斉に消えたわけではない", text="その後、ポケベルや携帯が広まりますが、\n伝言板が全国一斉に消えたわけではありません。", pause=0.35),
    dict(scene="history", head="日本地理学会の発表要旨", text="日本地理学会の発表要旨では、\n使われ方の変化などにより、",
         say="にほん地理学会の発表要旨では、使われ方の変化などにより、", pause=0.15),
    dict(scene="history", head="1990年前後から、一部で撤去", text="一部の鉄道会社で1990年前後から\n撤去が始まったと報告されています。",
         say="一部の鉄道会社で、千九百九十年前後から、撤去が始まったと報告されています。", pause=0.4),
    dict(scene="history", head="「携帯のせい」だけではない", text="「携帯が普及したから」だけでは、説明できないのです。", pause=0.8),

    # --- 今 ---
    dict(scene="now", head="家を出たあとも、変えられる", text="今は、家を出たあとも約束を変えられます。", pause=0.3),
    dict(scene="now", text="「あと5分」「店に入ってる」。", say="「あと五分」。「店に入ってる」。", pause=0.35),
    dict(scene="now", head="たった一言", text="たった一言が、待ち合わせの不安を減らしています。", pause=0.8),

    # --- 問いかけ ---
    dict(scene="cta", head="あなたは、どこで待ち合わせていましたか？", text="あなたは携帯を持つ前、\nどこで待ち合わせていましたか？", pause=0.5),
    dict(scene="cta", head="知らない世代なら、何分待てる？", text="当時を知らない人なら、\n何分まで待てそうですか？", pause=1.6),
]
