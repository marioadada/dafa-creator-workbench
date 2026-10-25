#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建「30 天新概念第一册锚定 · 日常口语 + 语法」课程体系，写回 HTML 的 english 模块。

课程结构：
  Day 1   = 开场课（总览 / 目标 / 方法 / 四周路线 / A1 自测）
  Day 2-29 = 新概念英语第一册 Lesson 1 - Lesson 28（语法主线 + 现代日常口语变体）
  Day 30  = 总复习 · 30 天语法串讲 + 一段完整日常对话实战

每课字段：
  day, date, source, grammar, review(上节回顾/承接), preview(下节预告/承接),
  sentences[5]{en,cn,note}, words[10]{en,phonetic,cn}, tips[5]
Day 1 额外含 opening{overview,goals[],method[],roadmap[],selftest[]}

注意：不杜撰篇目，source 用新概念第一册真实课次与标题；核心句型取自原版课文，
现代日常口语变体为原创练习句。
"""
import re, json, datetime, sys

HTML = "/Users/dafa/WorkBuddy/2026-07-24-10-40-51/dafa-creator-workbench.html"

START = datetime.date(2026, 8, 9)   # Day 1
def d(n): return (START + datetime.timedelta(days=n - 1)).isoformat()

# ---------------- 开场课 Day 1 ----------------
day1 = {
    "day": 1,
    "date": d(1),
    "source": "开场课 · 30 天日常口语 + 语法路线图",
    "grammar": "本套课怎么学：每天 1 个真实场景 + 1 个语法点，5 句开口练 + 10 词积累 + 回顾/预告闭环。",
    "review": "",
    "preview": "Day 2 正式开始新概念第一册 Lesson 1：用 Excuse me! / Is this your...? 学 be 动词和 this is。",
    "opening": {
        "overview": "这套课用《新概念英语》第一册前 28 课当语法骨架，每课配一个真实生活场景和现代口语练习。"
                    "目标不是背课文，而是 30 天后你能用英语做日常交流：打招呼、介绍、问路、购物、聊家人朋友、说过去和未来。",
        "goals": [
            "30 天后：能就日常话题说 5-8 句连贯英语，不卡壳。",
            "能听懂并回简单的问候、介绍、邀请、建议。",
            "掌握 A1 核心语法：be 动词、a/an、this/that、there is/are、can、现在/过去/将来时。",
            "敢开口——这是最重要的一条，比语法正确更优先。"
        ],
        "method": [
            "影子跟读：放原声（或自己念）同时小声跟，模仿语调和节奏，每天 5 分钟。",
            "5 句打卡：当天 5 句每句点圆圈标记「练过」，不贪多，练熟再说下一课。",
            "造自己的句子：每课挑 1 个语法点，造 2 句关于你自己的话（名字、工作、家人）。",
            "周末复习：不学新课，把本周 7 课的 5 句翻出来快速过一遍。"
        ],
        "roadmap": [
            "第 1 周（Day 2-8）：打招呼、介绍、物品归属、基础形容词——开口的地基。",
            "第 2 周（Day 9-15）：状态/感受、颜色、国籍职业、正式问候——能聊人和物。",
            "第 3 周（Day 16-22）：which/one、give 双宾语、some/any、厨房与客厅——生活场景扩展。",
            "第 4 周（Day 23-29）：方位 where、复数 there are、祈使句 must——完整描述环境+指令。",
            "Day 30：总复习 + 一段完整日常对话实战，把 29 课串起来。"
        ],
        "selftest": [
            "你能用英文说出自已的名字和来自哪座城市吗？",
            "你能用 is / are 造两个不同的句子吗？",
            "你知道 a 和 an 的区别吗？（apple 前面用哪个？）",
            "你能说 3 个描述人的形容词吗？（高/矮/胖…）",
            "上面 4 条能轻松做到的越多，起步越快；做不到也别慌，这套课就是来补这些的。"
        ]
    },
    "sentences": [
        {"en": "Hello, my name is Dafa.", "cn": "你好，我叫大发。", "note": "最基础自我介绍，name is 常连读成 name's"},
        {"en": "Nice to meet you.", "cn": "很高兴认识你。", "note": "第一次见面万能句，配合微笑"},
        {"en": "How are you today?", "cn": "你今天好吗？", "note": "Day 9 会细讲，这里先混个脸熟"},
        {"en": "I am learning English every day.", "cn": "我每天学英语。", "note": "I am = I'm，先念顺"},
        {"en": "See you tomorrow.", "cn": "明天见。", "note": "道别常用，tomorrow 记住这个词"}
    ],
    "words": [
        {"en": "hello", "phonetic": "həˈləʊ", "cn": "你好"},
        {"en": "name", "phonetic": "neɪm", "cn": "名字"},
        {"en": "nice", "phonetic": "naɪs", "cn": "好的；愉快的"},
        {"en": "meet", "phonetic": "miːt", "cn": "遇见"},
        {"en": "today", "phonetic": "təˈdeɪ", "cn": "今天"},
        {"en": "learn", "phonetic": "lɜːn", "cn": "学习"},
        {"en": "English", "phonetic": "ˈɪŋɡlɪʃ", "cn": "英语"},
        {"en": "every", "phonetic": "ˈevri", "cn": "每个"},
        {"en": "day", "phonetic": "deɪ", "cn": "天"},
        {"en": "tomorrow", "phonetic": "təˈmɒrəʊ", "cn": "明天"}
    ],
    "tips": [
        "开场课不急着背，先把 goals / method / roadmap 读一遍，知道这 30 天去哪。",
        "今天 5 句先念顺，重点练 Hello, my name is ... 和 Nice to meet you 两句，出门能用。",
        "自测里 4 条做不到的，圈出来——它们就是未来几周你的重点。",
        "每天固定一个时间学（比如早起 10 分钟或睡前），比偶尔猛学效果好。",
        "别怕发音不准，先求「能沟通」，准度会随跟读自然上来。"
    ]
}

# ---------------- 主体：Day 2-29 = NCE L1-L28 ----------------
# 每课: (课次, 标题, 语法点, 上节回顾, 下节预告, [5句(en,cn,note)], [10词(en,phon,cn)], [5技巧])
L = []
def add(lesson_no, title, grammar, review, preview, sentences, words, tips):
    day = lesson_no + 1  # Day2=L1 ... Day29=L28
    L.append({
        "day": day,
        "date": d(day),
        "source": f"新概念英语第一册 · Lesson {lesson_no}：{title}",
        "grammar": grammar,
        "review": review,
        "preview": preview,
        "sentences": [{"en": a, "cn": b, "note": c} for a, b, c in sentences],
        "words": [{"en": a, "phonetic": p, "cn": b} for a, p, b in words],
        "tips": tips
    })

add(1, "Excuse me!",
    "be 动词 is 与 this is 介绍；一般疑问句把 is 提前，简答用 Yes, it is. / No, it isn't.",
    "Day 1 做了开场自测和方法准备，今天从第一句英语开始。",
    "Day 3 学 Is this your...? 的否定回答和更多随身物品，把 is 疑问句练熟。",
    [
        ("Excuse me!", "对不起，打扰一下。", "引起注意、借过、问路万能开场，比 hey 礼貌"),
        ("Is this your handbag?", "这是你的手提包吗？", "this is / your 初见；疑问句 is 提前"),
        ("Yes, it is.", "是的，是我的。", "肯定简答 it is，口语常连读成 it's"),
        ("Pardon?", "对不起，请再说一遍？", "没听清的救场句，比 what 礼貌十倍"),
        ("Thank you very much.", "非常感谢。", "very much 加重感谢，比 thank you 更自然")
    ],
    [("handbag","ˈhændbæɡ","手提包"),("excuse","ɪkˈskjuːz","原谅； excuse me 打扰了"),
     ("me","miː","我"),("yes","jes","是的"),("is","ɪz","是（he/she/it）"),
     ("this","ðɪs","这"),("your","jɔː(r)","你的"),("it","ɪt","它"),
     ("pardon","ˈpɑːdn","请再说一遍"),("thank","θæŋk","谢谢")],
    ["Excuse me! 是整套管用句的根，先把它念到脱口而出。",
     "Pardon? 和 Sorry? 都能要对方重复，但 Pardon 更正式安全。",
     "一般疑问句公式：be 动词(is) + 主语(this) + 其他？——把 is 提前就对了。",
     "今天造 1 句：Is this your ____? 填你身边一样东西（phone/book/cup）。",
     "Thank you very much 比 thank you 真诚，服务场景、收到东西都用它。"]
)

add(2, "Is this your...?",
    "一般疑问句否定回答 No, it isn't.；物品词汇 pen/pencil/book/watch/coat...",
    "Day 2 学了 is 提前的疑问句和 this is，今天加否定回答和更多物品词。",
    "Day 4 学 whose（谁的）和所有格，开始问『这是谁的东西』。",
    [
        ("Is this your pen?", "这是你的钢笔吗？", "pen 笔，办公桌必备词"),
        ("No, it isn't.", "不，不是我的。", "否定 = is + not → isn't，it isn't 别拆开念"),
        ("Is this your pencil?", "这是你的铅笔吗？", "pencil 铅笔，和 pen 只差一个 l"),
        ("Yes, it is.", "是的，是我的。", "肯定简答，节奏要干脆"),
        ("Here you are.", "给你。", "递东西的万能句，配合递出动作")
    ],
    [("pen","pen","钢笔"),("pencil","ˈpensl","铅笔"),("book","bʊk","书"),
     ("watch","wɒtʃ","手表"),("coat","kəʊt","外套"),("dress","dres","连衣裙"),
     ("skirt","skɜːt","短裙"),("shirt","ʃɜːt","衬衫"),("car","kɑː(r)","汽车"),
     ("house","haʊs","房子")],
    ["Here you are 是递东西时的标配，和 Thank you 是一对。",
     "it isn't = it is not，口语永远用缩写，正式写作才写全。",
     "物品词先记 5 个最常用的（pen/book/watch/phone/car），其余随缘。",
     "今天造 2 句否定：No, it isn't. 接在 Is this your ...? 后面练顺。",
     "pen 和 pencil 一起记，很多人把 pencil 说成 pen，小心。"]
)

add(3, "Sorry, sir.",
    "否定 not 加强调；物品归属 my coat / my umbrella；ticket 取物场景。",
    "Day 3 学了否定 isn't 和物品词，今天在『取东西』场景里用 my + 物品。",
    "Day 5 学 Nice to meet you 和 a/an，开始介绍人和职业。",
    [
        ("My coat and my umbrella, please.", "我的外套和雨伞，谢谢。", "my + 物品，取物时直接报自己东西"),
        ("Here is my ticket.", "这是我的票。", "Here is 把东西递过去时说，ticket 票"),
        ("This is not my umbrella.", "这不是我的雨伞。", "not 否定，重音落在 not 上"),
        ("Sorry, sir.", "对不起，先生。", "sir 对男性礼貌称呼，出错时的缓冲"),
        ("Is this your umbrella?", "这是你的雨伞吗？", "呼应 Day 2 的疑问句，闭环")
    ],
    [("coat","kəʊt","外套"),("umbrella","ʌmˈbrelə","雨伞"),("ticket","ˈtɪkɪt","票"),
     ("sorry","ˈsɒri","对不起"),("sir","sɜː(r)","先生"),("number","ˈnʌmbə(r)","号码"),
     ("five","faɪv","五"),("please","pliːz","请"),("my","maɪ","我的"),("not","nɒt","不")],
    ["my 是所有格『我的』，后面永远跟名词：my book / my car。",
     "Sorry 和 Excuse me 不一样：Sorry 是道歉，Excuse me 是打扰。",
     "This is not my ... 是否定归属的模板，把 not 放在 is 后。",
     "今天练：对着镜子说 My ____, please. 填三样你常用的东西。",
     "sir / madam 是服务场景礼貌词，点单、问路都能用。"]
)

add(4, "Is this your...? (whose)",
    "whose（谁的）+ 名词；所有格初步：my/your/his/her 区分。",
    "Day 4 用 my + 物品做了归属，今天升级问『这是谁的』。",
    "Day 6 学 What make is it? 问品牌和颜色，开始描述东西。",
    [
        ("Whose shirt is that?", "那是谁的衬衫？", "whose = 谁的，后面直接跟名词 shirt"),
        ("Is this your shirt, Dave?", "戴夫，这是你的衬衫吗？", "把人名放句尾称呼，更自然"),
        ("No, it isn't my shirt.", "不，那不是我的衬衫。", "my shirt 我的衬衫，my+名词结构巩固"),
        ("This is my shirt.", "这是我的衬衫。", "This is 肯定归属，重音在 my"),
        ("Perhaps it is his.", "也许是他的。", "perhaps 也许，his 他的（男）")
    ],
    [("whose","huːz","谁的"),("shirt","ʃɜːt","衬衫"),("his","hɪz","他的（男）"),
     ("her","hɜː(r)","她的（女）"),("perhaps","pəˈhæps","也许"),("tie","taɪ","领带"),
     ("blouse","blaʊz","女式衬衫"),("brother","ˈbrʌðə(r)","兄弟"),("sister","ˈsɪstə(r)","姐妹"),
     ("white","waɪt","白色的")],
    ["whose 问『谁的』，回答用 my/your/his/her + 东西。",
     "his（他的）和 her（她的）别混：his 男、her 女。",
     "Perhaps 是缓冲词，不确定时先说 perhaps 再猜，显得从容。",
     "今天造：Whose ____ is this? 填一个教室/办公室里常见的东西。",
     "his/her 后必须跟名词，不能单独用（× his is 要改成 his book is）。"]
)

add(5, "Nice to meet you",
    "介绍他人 This is ...；he/she/it 第三人称；a/an 与国籍 French。",
    "Day 5 学了 whose/his/her，今天学正式介绍人和说国籍。",
    "Day 7 学 Are you a teacher? 用 Are 问身份和职业。",
    [
        ("This is Miss Sophie Dupont.", "这位是索菲·杜邦小姐。", "介绍别人用 This is，不用 She is"),
        ("She is French.", "她是法国人。", "She 她（女），French 法国人/法语"),
        ("Nice to meet you.", "很高兴认识你。", "被介绍时回应，Day 1 已预热"),
        ("He is a new student.", "他是一名新学生。", "He 他（男），a 一个（辅音开头）"),
        ("Good morning.", "早上好。", "白天见面开场，配合时间用")
    ],
    [("this","ðɪs","这"),("is","ɪz","是"),("miss","mɪs","小姐"),("she","ʃiː","她"),
     ("he","hiː","他"),("french","frentʃ","法国的；法语"),("student","ˈstjuːdnt","学生"),
     ("new","njuː","新的"),("good","ɡʊd","好的"),("morning","ˈmɔːnɪŋ","早晨")],
    ["介绍第三方永远用 This is，不用 He/She is（那是自我介绍才用）。",
     "a 用在辅音音素前（a student），an 用在元音前（an apple），看音不看字母。",
     "She is / He is 后接身份或国籍，是描述人的主干。",
     "今天练：This is my ____（friend/teacher/brother），介绍你身边一个人。",
     "Good morning / afternoon / evening 按时间换词，晚上才用 Good night（道别）。"]
)

add(6, "What make is it?",
    "What 特殊疑问句；问品牌 make 与颜色 colour；It's a Volvo / red。",
    "Day 6 学了介绍人和 a/an，今天用 What 问『什么牌子/什么颜色』。",
    "Day 8 学 What's your job? 问职业，把 a/an 用在职业上。",
    [
        ("What make is it?", "它是什么牌子的？", "make 在这里指品牌，问车/电器常用"),
        ("It's a Volvo.", "它是一辆沃尔沃。", "It's = It is，Volvo 品牌名"),
        ("What colour is it?", "它是什么颜色的？", "colour 颜色（英式拼写），美式 color"),
        ("It's red.", "它是红色的。", "red 红色，颜色词直接跟在 is 后"),
        ("That's a nice car.", "那是辆不错的车。", "nice 不错的，夸东西万能形容词")
    ],
    [("what","wɒt","什么"),("make","meɪk","品牌；制造"),("colour","ˈkʌlə(r)","颜色"),
     ("red","red","红色"),("blue","bluː","蓝色"),("car","kɑː(r)","汽车"),
     ("volvo","ˈvɒlvəʊ","沃尔沃"),("nice","naɪs","好的；不错的"),("that","ðæt","那"),
     ("green","ɡriːn","绿色")],
    ["What 开头是特殊疑问句，语序：What + 名词 + is + 它？",
     "问颜色 = What colour is it? 回答 It's + 颜色，别加 a。",
     "make 作名词指『品牌』，这是英式用法，记这个场景即可。",
     "今天练：指着你身边一样东西问 What colour is it? 自己答。",
     "nice 是夸人夸物的安全词：a nice car / a nice day。"]
)

add(7, "Are you a teacher?",
    "Are you...? 第二人称疑问句；国籍/职业；Yes, I am. / No, I'm not.",
    "Day 7 学了 What 问品牌颜色，今天用 Are 问『你是…吗』。",
    "Day 9 学 What's your job? 具体问职业名称。",
    [
        ("Are you a teacher?", "你是一名老师吗？", "Are you + 身份，问对方"),
        ("Yes, I am.", "是的，我是。", "I am 我（第一人称），肯定简答"),
        ("Are you French?", "你是法国人吗？", "French 这里指国籍，不是语言"),
        ("No, I'm not.", "不，我不是。", "I'm not = I am not，口语缩写"),
        ("I am a student.", "我是一名学生。", "回到肯定，巩固 I am + 职业")
    ],
    [("are","ɑː(r)","是（you/we/they）"),("you","juː","你"),("teacher","ˈtiːtʃə(r)","老师"),
     ("french","frentʃ","法国的"),("i","aɪ","我"),("am","æm","是（I）"),
     ("student","ˈstjuːdnt","学生"),("no","nəʊ","不"),("yes","jes","是的"),
     ("not","nɒt","不（否定）")],
    ["be 动词三人称：I am / you are / he/she/it is，今天用到 am 和 are。",
     "Are you...? 的回答：Yes, I am. / No, I'm not. 主语要变 I。",
     "问国籍用 Are you + 国籍词，不用 Do you from（那是错误中式英语）。",
     "今天造：Are you a ____? 填一个职业（doctor/engineer/student）。",
     "I'm not 是 I am not 的口语缩写，正式写作写全。"]
)

add(8, "What's your job?",
    "职业词汇 policeman/taxi driver/postman/nurse；What's your job? 问职业。",
    "Day 8 用 Are you 问身份，今天直接问『你的工作是什么』。",
    "Day 10 学 How are you today? 问状态和感受，进入形容词。",
    [
        ("What's your job?", "你是做什么工作的？", "What's = What is，job 工作"),
        ("I'm a taxi driver.", "我是一名出租车司机。", "taxi driver 出租车司机，复合词"),
        ("What's his job?", "他是做什么的？", "his job 他的工作，把 your 换成 his"),
        ("He's a postman.", "他是一名邮递员。", "He's = He is，postman 邮递员"),
        ("She's a nurse.", "她是一名护士。", "She's = She is，nurse 护士")
    ],
    [("job","dʒɒb","工作"),("policeman","pəˈliːsmən","警察"),("taxi","ˈtæksi","出租车"),
     ("driver","ˈdraɪvə(r)","司机"),("postman","ˈpəʊstmən","邮递员"),("nurse","nɜːs","护士"),
     ("engineer","ˌendʒɪˈnɪə(r)","工程师"),("doctor","ˈdɒktə(r)","医生"),("hair","heə(r)","头发"),
     ("daughter","ˈdɔːtə(r)","女儿")],
    ["问职业 = What's your job? 回答 I'm a + 职业。",
     "职业词大多加 -er/-man：drive→driver，police→policeman。",
     "his/her job 问别人的工作，把 your 换成 his/her 即可。",
     "今天练：用 I'm a ____ 说出你和你家人的职业（各一句）。",
     "job 是可数名词，前面要加 a：a job，不是 job。"]
)

add(9, "How are you today?",
    "How are you? 问候状态；形容词 well/fine/thank you 回应链。",
    "Day 9 学了职业词汇，今天学怎么问候对方『状态好不好』。",
    "Day 11 学 Look at... 和描述人的形容词 tall/short/fat/thin。",
    [
        ("Hello, Helen.", "你好，海伦。", "先叫名字，再问好，更亲切"),
        ("How are you today?", "你今天好吗？", "How are you 固定问候，today 可加可不加"),
        ("I'm very well, thank you.", "我很好，谢谢。", "well 身体/状态好，比 good 地道"),
        ("And you?", "你呢？", "反问对方的万能短句，省略了 how are you"),
        ("I'm fine, thanks.", "我挺好的，谢谢。", "fine 也不错，thanks = thank you")
    ],
    [("hello","həˈləʊ","你好"),("how","haʊ","怎样"),("are","ɑː(r)","是"),
     ("today","təˈdeɪ","今天"),("well","wel","身体好的"),("fine","faɪn","不错的；好的"),
     ("thanks","θæŋks","谢谢"),("and","ænd","和；而"),("you","juː","你"),
     ("good","ɡʊd","好的")],
    ["How are you 是英语最高频问候，必须脱口而出。",
     "回答用 I'm well / I'm fine，别用 I'm good（偏美式、略随意）。",
     "And you? 是礼貌反问，对方问完你一定要回一句。",
     "今天练：对镜子说 Hello, I'm Dafa. How are you? 再自问自答。",
     "well 和 fine 都表好，well 偏健康状态，fine 偏『还行挺好』。"]
)

add(10, "Look at...",
    "Look at + 名词；描述人外貌的形容词 tall/short/fat/thin。",
    "Day 10 学了 How are you 问候状态，今天用 Look at 描述看到的人。",
    "Day 12 学 whose 物主代词（my/your/his/her/its）完整一套。",
    [
        ("Look at that man.", "看那个男人。", "Look at 引起注意看某物/某人"),
        ("He's tall and fat.", "他又高又胖。", "tall 高，fat 胖，and 连接两个形容词"),
        ("Look at that woman.", "看那个女人。", "woman 女人（单数），复数是 women"),
        ("She's short and thin.", "她又矮又瘦。", "short 矮/短，thin 瘦"),
        ("He is a policeman.", "他是一名警察。", "呼应 Day 9 职业词")
    ],
    [("look","lʊk","看"),("at","æt","在（介词）"),("man","mæn","男人"),
     ("woman","ˈwʊmən","女人"),("tall","tɔːl","高的"),("short","ʃɔːt","矮的；短的"),
     ("fat","fæt","胖的"),("thin","θɪn","瘦的"),("and","ænd","和；又"),("boy","bɔɪ","男孩")],
    ["Look at 后面必须跟名词或代词：Look at him / Look at that car。",
     "形容人用 形容词+and+形容词：tall and thin，不用加 is 在中间（那是句子）。",
     "fat 直译胖，日常说 slightly overweight 更委婉，但基础阶段先记 fat。",
     "今天练：Look at ____. He's/She's ____ and ____. 描述你看到的一个人。",
     "man/woman 是单数，看到一群要用 men/women（不规则复数）。"]
)

add(11, "Is this your shirt?",
    "whose 物主代词复习；衣物词汇；my/your + 衣物归属。",
    "Day 11 学了 Look at 和形容人，今天回到衣物归属（呼应 Day 4）。",
    "Day 13 学 a new dress 和颜色问答，衣物+颜色组合。",
    [
        ("Whose shirt is that?", "那是谁的衬衫？", "whose 再出现，巩固『谁的』"),
        ("Is this your shirt, Dave?", "戴夫，这是你的衬衫吗？", "人名置后，口语习惯"),
        ("No, it isn't my shirt.", "不，不是我的衬衫。", "my shirt 我的衬衫，否定结构"),
        ("This is my shirt.", "这是我的衬衫。", "肯定归属"),
        ("Here you are.", "给你。", "递物标配，Day 3 学过")
    ],
    [("shirt","ʃɜːt","衬衫"),("whose","huːz","谁的"),("my","maɪ","我的"),
     ("your","jɔː(r)","你的"),("perhaps","pəˈhæps","也许"),("tie","taɪ","领带"),
     ("blouse","blaʊz","女式衬衫"),("brother","ˈbrʌðə(r)","兄弟"),("sister","ˈsɪstə(r)","姐妹"),
     ("white","waɪt","白色的")],
    ["衣物归属公式：Whose + 衣物 + is this/that? 回答 My/His/Her + 衣物。",
     "my/your/his/her 后一定跟名词，不能裸用。",
     "今天把 Day 4 和今天的句子连起来读，感受 whose 的重复出现。",
     "衣物词先记 shirt/tie/dress/skirt，其余随场景补。",
     "Here you are 和 Thank you 是一对，递接东西时自然成对。"]
)

add(12, "Whose is this...? This is my/your/his/her...",
    "物主代词完整一套：my/your/his/her/its/our/their + 名词。",
    "Day 12 复习了衣物归属，今天把物主代词（我的/你的/他的…）学全。",
    "Day 14 学 a new dress 和 What colour 问答，进入颜色描述。",
    [
        ("Whose is this coat?", "这是谁的外套？", "Whose is this + 名词，省略了后面的 coat"),
        ("This is my coat.", "这是我的外套。", "my 我的，完整物主代词之一"),
        ("Whose is that umbrella?", "那是谁的雨伞？", "that 那，对应 this 这"),
        ("That is her umbrella.", "那是她的雨伞。", "her 她的（女），后跟名词"),
        ("It is his book.", "它是他的书。", "his 他的（男）")
    ],
    [("whose","huːz","谁的"),("coat","kəʊt","外套"),("my","maɪ","我的"),
     ("your","jɔː(r)","你的"),("his","hɪz","他的"),("her","hɜː(r)","她的"),
     ("its","ɪts","它的"),("our","aʊə(r)","我们的"),("their","ðeə(r)","他们的"),
     ("umbrella","ʌmˈbrelə","雨伞")],
    ["物主代词七兄弟：my/your/his/her/its/our/their，全后跟名词。",
     "区分 his（他的）和 her（她的）：his 男、her 女，发音差很多。",
     "Whose is this...? 比 Whose + 名词 + is this 更口语省略。",
     "今天练：拿三样东西说 This is my ____ / That is his ____。",
     "its 是『它的』，容易和 it's（it is）搞混，注意没撇号。"]
)

add(13, "A new dress",
    "a/an + 形容词 + 名词（a new dress）；颜色词 green；come upstairs。",
    "Day 13 学了完整物主代词，今天学『a + 形容词 + 名词』描述衣物。",
    "Day 15 学 What colour is your...? 专门问颜色。",
    [
        ("What colour is your new dress?", "你的新连衣裙是什么颜色的？", "new dress 新裙子，new 形容词放名词前"),
        ("It's green.", "它是绿色的。", "green 绿色，颜色词直接答"),
        ("Come upstairs and see it.", "上楼来看看吧。", "come upstairs 上楼，日常邀约"),
        ("It's a lovely dress.", "这是条很好看的裙子。", "lovely 可爱的/好看的，夸物词"),
        ("That's a nice colour.", "那是个好看的颜色。", "nice 又出现，安全夸词")
    ],
    [("dress","dres","连衣裙"),("new","njuː","新的"),("green","ɡriːn","绿色的"),
     ("colour","ˈkʌlə(r)","颜色"),("upstairs","ˌʌpˈsteəz","上楼"),("lovely","ˈlʌvli","可爱的；好看的"),
     ("case","keɪs","箱子；案例"),("carpet","ˈkɑːpɪt","地毯"),("dog","dɒɡ","狗"),
     ("smart","smɑːt","聪明的；帅气的")],
    ["英语形容词放名词前面：a new dress，不是 a dress new。",
     "a/an 看后面词发音：new 辅音开头用 a，old 元音开头用 an。",
     "问颜色套 Day 6 的 What colour is it?，今天加 your new dress 更具体。",
     "今天练：a/an + 颜色 + 衣物，造 3 个词组（a red shirt 等）。",
     "lovely / nice / smart 都是夸词，先记 lovely 夸物、smart 夸人。"]
)

add(14, "What colour is your...?",
    "颜色问答专门化；white/blue/black/grey 等颜色词。",
    "Day 14 学了 a+形容词+名词和颜色，今天专练问颜色。",
    "Day 16 学 Your passports, please 和复数 we/they、国籍。",
    [
        ("What colour is your shirt?", "你的衬衫是什么颜色的？", "把 dress 换成 shirt，结构不变"),
        ("It's white.", "它是白色的。", "white 白色"),
        ("My shirt is blue.", "我的衬衫是蓝色的。", "my shirt 做主语，blue 做表语"),
        ("It is black.", "它是黑色的。", "black 黑色，描述任何东西"),
        ("What colour are your shoes?", "你的鞋是什么颜色的？", "shoes 复数，所以用 are")
    ],
    [("white","waɪt","白色的"),("blue","bluː","蓝色的"),("black","blæk","黑色的"),
     ("grey","ɡreɪ","灰色的"),("brown","braʊn","棕色的"),("colour","ˈkʌlə(r)","颜色"),
     ("shirt","ʃɜːt","衬衫"),("shoe","ʃuː","鞋"),("hat","hæt","帽子"),("red","red","红色")],
    ["问颜色 = What colour + is/are + 主语？单数 is、复数 are。",
     "颜色词前不加 a：It's blue，不是 It's a blue。",
     "shoes / hat 等衣物词常成对或戴头上，记搭配即可。",
     "今天练：指着身上衣物轮流问 What colour is your ____? 自答。",
     "颜色词是描述世界的地基，先记 white/black/blue/red/green 五个。"]
)

add(15, "Your passports, please",
    "复数 be 动词 are（we/you/they）；国籍词 Swedish/Danish；we aren't。",
    "Day 15 学了颜色问答，今天进入复数和出国场景（护照/国籍）。",
    "Day 17 学 Are you...? 国籍复数和正式问候 How do you do?",
    [
        ("Are you Swedish?", "你们是瑞典人吗？", "Swedish 瑞典人/瑞典的，复数 you 配 are"),
        ("No, we aren't.", "不，我们不是。", "we aren't = we are not，我们不是"),
        ("We are Danish.", "我们是丹麦人。", "we are 我们是，Danish 丹麦人"),
        ("Are your friends Danish, too?", "你的朋友们也是丹麦人吗？", "friends 朋友（复数），too 也"),
        ("Your passports, please.", "请出示你们的护照。", "passports 护照（复数），海关场景")
    ],
    [("passport","ˈpɑːspɔːt","护照"),("swedish","ˈswiːdɪʃ","瑞典的；瑞典人"),("danish","ˈdeɪnɪʃ","丹麦的；丹麦人"),
     ("we","wiː","我们"),("aren't","ɑːnt","不是（are not）"),("friends","frendz","朋友们"),
     ("too","tuː","也"),("norwegian","nɔːˈwiːdʒn","挪威的；挪威人"),("russian","ˈrʌʃn","俄罗斯的；俄罗斯人"),
     ("nationality","ˌnæʃəˈnæləti","国籍")],
    ["复数主语 we/you/they 配 are，否定 aren't。",
     "国籍词首字母大写：Swedish/Danish/Chinese，别写小写。",
     "we aren't = we are not，口语必缩写。",
     "今天练：We are ____（Chinese/students/friends），造 2 句复数句。",
     "passport 海关万能词，出国旅行第一时间用上。"]
)

add(16, "Are you...?",
    "国籍/身份复数 Are we/you/they；Are you... too?；否定 I'm not。",
    "Day 16 学了复数 are 和护照场景，今天巩固 Are you + 国籍。",
    "Day 18 学 How do you do? 正式介绍和复数职业。",
    [
        ("Are you Australian?", "你是澳大利亚人吗？", "Australian 澳大利亚人"),
        ("No, I'm not.", "不，我不是。", "I'm not 再次巩固"),
        ("I'm Austrian.", "我是奥地利人。", "Austrian 奥地利人"),
        ("Are you Austrian, too?", "你也是奥地利人吗？", "too 也，放句尾"),
        ("We are not French.", "我们不是法国人。", "复数否定 we are not")
    ],
    [("australian","ɒˈstreɪliən","澳大利亚的；澳大利亚人"),("austrian","ˈɒstriən","奥地利的；奥地利人"),
     ("too","tuː","也"),("we","wiː","我们"),("are","ɑː(r)","是"),("not","nɒt","不"),
     ("german","ˈdʒɜːmən","德国的；德国人"),("korean","kəˈriːən","韩国的；韩国人"),
     ("canadian","kəˈneɪdiən","加拿大的；加拿大人"),("italian","ɪˈtæliən","意大利的；意大利人")],
    ["Are you + 国籍？回答 Yes, I am. / No, I'm not.",
     "too（也）永远放句尾：Are you Austrian, too?",
     "各国国籍词都是『国家名 + n/ian』规律，记 Chinese/Japanese 特殊。",
     "今天练：Are you ____? 填三个国籍轮流问自己答。",
     "we are not 可缩写 we aren't，口语更常用 aren't。"]
)

add(17, "How do you do?",
    "正式问候 How do you do?（初次见面，非问句）；介绍第三方 This is。",
    "Day 17 巩固了国籍问答，今天学正式场合的初次问候。",
    "Day 19 学 What are their jobs? 复数职业和 they are。",
    [
        ("Come and meet our employees.", "来见见我们的员工。", "meet 认识，our 我们的"),
        ("This is Nicola Grey.", "这位是尼古拉·格雷。", "介绍用 This is，Day 5 学过"),
        ("How do you do?", "你好。（初次见面）", "固定回应，不是真问 how are you"),
        ("This is Claire Taylor.", "这位是克莱尔·泰勒。", "再介绍一位，结构一致"),
        ("How do you do?", "你好。", "对方也说 How do you do? 对等")
    ],
    [("meet","miːt","遇见；认识"),("our","aʊə(r)","我们的"),("employee","ɪmˈplɔɪiː","员工"),
     ("how","haʊ","怎样"),("do","duː","做（助动词）"),("nice","naɪs","好的"),
     ("morning","ˈmɔːnɪŋ","早晨"),("afternoon","ˌɑːftəˈnuːn","下午"),("evening","ˈiːvnɪŋ","晚上"),
     ("mr","ˈmɪstə(r)","先生（Mr.）")],
    ["How do you do? 只用于正式初次见面，对方原样回一句，别答 I'm fine。",
     "它和 How are you 完全不同：一个是仪式问候，一个是真关心状态。",
     "介绍多人用重复 This is ... + How do you do? 即可。",
     "今天练：假装介绍两个朋友，说 This is ... / How do you do? 两轮。",
     "职场/正式场合用 How do you do，朋友间用 Nice to meet you。"]
)

add(18, "What are their jobs?",
    "复数职业 What are their jobs?；they are + 职业；keyboard operators。",
    "Day 18 学了正式问候，今天把职业问答扩展到复数 they。",
    "Day 20 学 Tired and thirsty 和形容词，进入感受描述。",
    [
        ("What are their jobs?", "他们是做什么工作的？", "their 他们的，jobs 复数"),
        ("They are keyboard operators.", "他们是键盘操作员。", "they are 他们是，keyboard 键盘"),
        ("They are engineers.", "他们是工程师。", "engineers 工程师（复数加 s）"),
        ("We are teachers.", "我们是老师。", "we are 回到第一人称复数"),
        ("Are they doctors?", "他们是医生吗？", "复数疑问句 Are they + 职业？")
    ],
    [("their","ðeə(r)","他们的"),("jobs","dʒɒbz","工作（复数）"),("they","ðeɪ","他们"),
     ("keyboard","ˈkiːbɔːd","键盘"),("operator","ˈɒpəreɪtə(r)","操作员"),("engineer","ˌendʒɪˈnɪə(r)","工程师"),
     ("doctors","ˈdɒktəz","医生（复数）"),("nurses","nɜːsɪz","护士（复数）"),("sales","seɪlz","销售"),
     ("reps","reps","销售代表（复）")],
    ["复数职业问答：What are their jobs? → They are + 职业（加 s）。",
     "they are 可缩写成 they're，口语常用。",
     "职业复数大多加 s：doctors/nurses/engineers。",
     "今天练：说出你团队/家人的职业，用 They are ____。",
     "their 是 they 的物主代词，别和 there（那里）搞混。"]
)

add(19, "Tired and thirsty",
    "感受形容词 tired/thirsty；There is 单数存在句；children 不规则复数。",
    "Day 19 学了复数职业，今天学说自己的状态（累/渴）。",
    "Day 21 学 Look at them 复数形容词和 there's 继续。",
    [
        ("What's the matter, children?", "孩子们，怎么了？", "What's the matter 怎么了，children 孩子们"),
        ("We're tired and thirsty.", "我们又累又渴。", "We're = We are，tired 累 thirsty 渴"),
        ("Sit down here.", "坐这儿吧。", "sit down 坐下，关心对方"),
        ("Are you all right now?", "你们现在好点了吗？", "all right 还好吗，now 现在"),
        ("There's an ice cream man.", "那儿有个卖冰淇淋的。", "There's = There is，an 元音前")
    ],
    [("matter","ˈmætə(r)","事情；问题"),("children","ˈtʃɪldrən","孩子们"),("tired","ˈtaɪəd","累的"),
     ("thirsty","ˈθɜːsti","渴的"),("sit","sɪt","坐"),("down","daʊn","向下"),
     ("right","raɪt","好的；对的"),("now","naʊ","现在"),("ice","aɪs","冰"),("cream","kriːm","奶油")],
    ["说状态用 I'm / We're + 形容词：I'm tired. We're thirsty.",
     "What's the matter? 是关心对方『怎么了』的万能问。",
     "children 是 child 的不规则复数，没有 -s。",
     "There's = There is，表示『有一个…』，后接单数。",
     "今天练：对着自己说 I'm tired / I'm thirsty，真实场景马上能用。"]
)

add(20, "Look at them",
    "them 宾语（他们）；复数形容词 dirty；What's the matter with them?",
    "Day 20 学了 tired/thirsty 和 there's，今天用 them 指『他们』并描述。",
    "Day 22 学 Which book? 和 one 替代词，进入选择。",
    [
        ("Look at them.", "看他们。", "them 他们（宾格），在动词后"),
        ("They're dirty.", "他们很脏。", "They're = They are，dirty 脏的"),
        ("What's the matter with them?", "他们怎么了？", "with them 关于他们"),
        ("They're tired and thirsty.", "他们又累又渴。", "呼应 Day 19 的状态词"),
        ("Those children are loud.", "那些孩子很吵。", "those 那些，loud 吵的")
    ],
    [("them","ðem","他们（宾格）"),("dirty","ˈdɜːti","脏的"),("with","wɪð","和…一起；关于"),
     ("those","ðəʊz","那些"),("loud","laʊd","吵闹的"),("clean","kliːn","干净的"),
     ("old","əʊld","老的；旧的"),("young","jʌŋ","年轻的"),("busy","ˈbɪzi","忙的"),
     ("lazy","ˈleɪzi","懒的")],
    ["them 是 they 的宾格，放动词/介词后：Look at them / with them。",
     "描述一群人用 They're + 形容词（复数）。",
     "those 那些（复数），对应 that 那（单数）。",
     "今天练：They're ____（dirty/tired/loud），描述你看到的一群人。",
     "dirty/clean 是一对反义，记一起效率翻倍。"]
)

add(21, "Which book?",
    "Which + 名词 选择疑问句；one 替代单数名词（the red one）。",
    "Day 21 学了 them 和复数形容词，今天学『哪一个』做选择。",
    "Day 23 学 Give me a book 双宾语，进入『给』的句型。",
    [
        ("Give me a book, Jane.", "简，给我一本书。", "Give me 给我，Day 23 细讲双宾语"),
        ("Which book?", "哪一本？", "Which 哪一个，引导选择"),
        ("The red one.", "红色的那本。", "one 替代 book，避免重复"),
        ("Which pen do you want?", "你想要哪支笔？", "Which + 名词 + do you want"),
        ("This one is mine.", "这支是我的。", "mine 我的（名词性，不跟名词）")
    ],
    [("which","wɪtʃ","哪一个"),("book","bʊk","书"),("red","red","红色的"),
     ("one","wʌn","一个（替代词）"),("want","wɒnt","想要"),("give","ɡɪv","给"),
     ("mine","maɪn","我的（名词性）"),("yours","jɔːz","你的（名词性）"),("pen","pen","钢笔"),
     ("choose","tʃuːz","选择")],
    ["Which + 名词 问『哪一个』：Which book / Which pen？",
     "one 替代前面提到的单数名词：the red one = the red book。",
     "mine / yours 是名词性物主代词，后面不跟名词（× mine book）。",
     "今天练：指着两样东西问 Which ____ do you want? 答 The ____ one.",
     "want 想要，日常高频：I want a coffee. 点单神句。"]
)

add(22, "Give me/him/her a...",
    "双宾语 Give + 人 + 物；Which one?；the red one 继续。",
    "Day 22 学了 Which 和 one 替代，今天学『给我/他/她某物』。",
    "Day 24 学 Which glasses? 复数 ones 替代和 on 方位。",
    [
        ("Give me that book.", "把那本书给我。", "Give me + 物，双宾语雏形"),
        ("Which one?", "哪一本？", "Which one 哪一本（替代 book）"),
        ("The red one.", "红色的那本。", "red one 继续替代"),
        ("Give him a pen.", "给他一支笔。", "him 他（宾格），放 give 后"),
        ("Give her a book.", "给她一本书。", "her 她（宾格）")
    ],
    [("give","ɡɪv","给"),("me","miː","我（宾格）"),("him","hɪm","他（宾格）"),
     ("her","hɜː(r)","她（宾格）"),("that","ðæt","那"),("which","wɪtʃ","哪一个"),
     ("one","wʌn","一个（替代）"),("book","bʊk","书"),("pen","pen","钢笔"),("desk","desk","书桌")],
    ["双宾语结构：Give + 人(宾格) + 物：Give me a book.",
     "me/him/her 是宾格，用在动词后（give 后）。",
     "Which one? 在对方递东西时确认『哪一个』。",
     "今天练：Give me the ____ one. 填颜色，想象在借东西。",
     "him（他）和 her（她）宾格和主格 he/she 不同，注意位置。"]
)

add(23, "Which glasses?",
    "复数 ones 替代；on the desk 方位介词 on；glasses 不规则。",
    "Day 23 学了双宾语，今天学复数『哪些』和 on 方位。",
    "Day 25 学 Give me some... 和 some/any 不定量。",
    [
        ("Which glasses?", "哪些杯子？", "glasses 眼镜/杯子（复数），which 复数"),
        ("The ones on the desk.", "书桌上的那些。", "ones 替代 glasses，on the desk 方位"),
        ("These are mine.", "这些是我的。", "These 这些（复数），mine 我的"),
        ("Which cups do you like?", "你喜欢哪些杯子？", "cups 杯子，like 喜欢"),
        ("The blue ones.", "蓝色的那些。", "blue ones 蓝色的（复数替代）")
    ],
    [("glasses","ˈɡlɑːsɪz","眼镜；玻璃杯（复）"),("ones","wʌnz","一些（复数替代）"),("desk","desk","书桌"),
     ("on","ɒn","在…上"),("these","ðiːz","这些"),("those","ðəʊz","那些"),
     ("cup","kʌp","杯子"),("like","laɪk","喜欢"),("blue","bluː","蓝色的"),("table","ˈteɪbl","桌子")],
    ["复数替代用 ones：the blue ones = the blue glasses。",
     "on 表示『在…上面』：on the desk / on the table。",
     "glasses 是 glass 的复数，指眼镜或杯子都行，看语境。",
     "今天练：The ____ ones on the ____. 填颜色和家具，描述位置。",
     "these/those 是指示代词复数，对应 this/that 单数。"]
)

add(24, "Give me some...",
    "some / any 不定量；Give me some + 复数/不可数；shelf 方位。",
    "Day 24 学了复数 ones 和 on 方位，今天学『一些』some/any。",
    "Day 26 学 Mrs. Smith's kitchen 和 there is 描述房间。",
    [
        ("Give me some glasses.", "给我一些杯子。", "some 一些，接复数或不可数"),
        ("Which ones?", "哪些？", "ones 复数替代"),
        ("The ones on the shelf.", "架子上的那些。", "shelf 架子，on the shelf 在架上"),
        ("I want some water.", "我想要一些水。", "water 不可数，用 some 不加 s"),
        ("Do you have any books?", "你有一些书吗？", "any 用于疑问句，替代 some")
    ],
    [("some","sʌm","一些"),("any","ˈeni","任何；一些（疑问/否定）"),("glasses","ˈɡlɑːsɪz","杯子（复）"),
     ("shelf","ʃelf","架子"),("water","ˈwɔːtə(r)","水"),("books","bʊks","书（复）"),
     ("tea","tiː","茶"),("coffee","ˈkɒfi","咖啡"),("rice","raɪs","米饭"),("bread","bred","面包")],
    ["some 用于肯定句（I want some water），any 用于疑问/否定。",
     "不可数名词（water/tea/rice/bread）永远不加 s，用 some 修饰。",
     "架子 shelf 复数 shelves，但单说 on the shelf 即可。",
     "今天练：I want some ____. 填三个不可数名词（水/茶/咖啡）。",
     "some/any 是 A1 语法分水岭，先用熟 some 肯定句。"]
)

add(25, "Mrs. Smith's kitchen",
    "there is 单数存在句；'s 所有格（Mrs. Smith's）；厨房物品。",
    "Day 25 学了 some/any，今天用 there is 描述『房间里有什么』。",
    "Day 27 学 Where is it? 方位介词，把存在句加上位置。",
    [
        ("There is a refrigerator in the kitchen.", "厨房里有一台冰箱。", "there is 有，in the kitchen 在厨房"),
        ("The refrigerator is white.", "冰箱是白色的。", "white 颜色，呼应 Day 14"),
        ("This is Mrs. Smith's kitchen.", "这是史密斯太太的厨房。", "'s 所有格，…的"),
        ("There is an electric cooker.", "有一台电炉。", "an 元音开头，electric 电的"),
        ("The kitchen is small.", "厨房很小。", "small 小的，形容词描述")
    ],
    [("kitchen","ˈkɪtʃɪn","厨房"),("refrigerator","rɪˈfrɪdʒəreɪtə(r)","冰箱"),("cooker","ˈkʊkə(r)","炉灶"),
     ("electric","ɪˈlektrɪk","电的"),("small","smɔːl","小的"),("large","lɑːdʒ","大的"),
     ("white","waɪt","白色的"),("mrs","ˈmɪsɪz","太太（Mrs.）"),("smith","smɪθ","史密斯（姓）"),
     ("room","ruːm","房间")],
    ["there is + 单数名词：There is a fridge. 表示『有一个…』。",
     "'s 是所有格：Mrs. Smith's kitchen = 史密斯太太的厨房。",
     "in the kitchen 表位置，in = 在…里面。",
     "今天练：There is a ____ in my ____. 填家具和房间。",
     "refrigerator 太长，口语常说 fridge，但先记全称。"]
)

add(26, "Where is it?",
    "Where is...? 方位疑问句；on/in/under 介词。",
    "Day 26 学了 there is 描述房间，今天加『在哪里』问位置。",
    "Day 28 学 Where are they? 复数方位，there are 也登场。",
    [
        ("Where is the refrigerator?", "冰箱在哪里？", "Where is = 在哪里，缩写 Where's"),
        ("It's on the right.", "它在右边。", "on the right 在右边"),
        ("Where is the cooker?", "炉灶在哪里？", "cooker 炉灶"),
        ("It's in the middle.", "它在中间。", "in the middle 在中间"),
        ("It is under the window.", "它在窗户下面。", "under 在…下面")
    ],
    [("where","weə(r)","在哪里"),("right","raɪt","右边"),("left","left","左边"),
     ("middle","ˈmɪdl","中间"),("under","ˈʌndə(r)","在…下面"),("window","ˈwɪndəʊ","窗户"),
     ("on","ɒn","在…上"),("in","ɪn","在…里"),("front","frʌnt","前面"),("behind","bɪˈhaɪnd","在…后面")],
    ["问位置 = Where is + 东西？回答 It's + 介词 + 位置。",
     "三个核心介词：on（上）/ in（里）/ under（下）。",
     "right/left/middle 是方位词，配合 on the right 用。",
     "今天练：Where is my ____? 填身边东西，答 It's on/in/under ____。",
     "Where's = Where is，口语必缩写。"]
)

add(27, "Mrs. Smith's living room",
    "there are 复数存在句；客厅物品 magazines/television。",
    "Day 27 学了 Where is 单数方位，今天学 there are 复数『有哪些』。",
    "Day 29 学 Where are they? 复数方位，把存在句+位置合并。",
    [
        ("There are some magazines on the television.", "电视机上有些杂志。", "there are 复数，magazines 杂志"),
        ("There is a television in the room.", "房间里有一台电视。", "there is 单数，television 电视"),
        ("The living room is large.", "客厅很大。", "living room 客厅，large 大"),
        ("There are two armchairs.", "有两把扶手椅。", "armchairs 扶手椅（复数）"),
        ("This is their living room.", "这是他们的客厅。", "their 他们的，所有格")
    ],
    [("living","ˈlɪvɪŋ","居住的"),("room","ruːm","房间"),("television","ˈtelɪvɪʒn","电视"),
     ("magazine","ˌmæɡəˈziːn","杂志"),("armchair","ˈɑːmtʃeə(r)","扶手椅"),("sofa","ˈsəʊfə","沙发"),
     ("table","ˈteɪbl","桌子"),("picture","ˈpɪktʃə(r)","画；照片"),("wall","wɔːl","墙"),
     ("there","ðeə(r)","那里（存在）")],
    ["there are + 复数名词：There are some books. 表示『有一些…』。",
     "there is（单）/ there are（复），看后面名词单复数。",
     "living room 客厅，固定搭配，room 这里指『室』。",
     "今天练：There are some ____ in my ____. 填物品和房间。",
     "magazine 复数 magazines，注意 z 发音 /z/。"]
)

add(28, "Where are they?",
    "Where are...? 复数方位；there are 与方位合并。",
    "Day 28 学了 there are 复数存在，今天学『它们在哪里』复数方位。",
    "Day 30 总复习：把 be 动词/there is-are/方位/所有格串成一段完整对话。",
    [
        ("Where are the newspapers?", "报纸在哪里？", "newspapers 报纸（复数），Where are 复数"),
        ("They're on the table.", "它们在桌子上。", "They're = They are，on the table 桌上"),
        ("Where are the magazines?", "杂志在哪里？", "magazines 杂志"),
        ("They are in the kitchen.", "它们在厨房里。", "in the kitchen 厨房里"),
        ("There are some books on the desk.", "书桌上有一些书。", "there are 存在+方位合并")
    ],
    [("where","weə(r)","在哪里"),("newspapers","ˈnjuːzpeɪpəz","报纸（复）"),("they","ðeɪ","它们"),
     ("table","ˈteɪbl","桌子"),("kitchen","ˈkɪtʃɪn","厨房"),("on","ɒn","在…上"),
     ("in","ɪn","在…里"),("desk","desk","书桌"),("books","bʊks","书（复）"),("floor","flɔː(r)","地板")],
    ["复数问位置 = Where are + 复数名词？答 They're + 介词 + 位置。",
     "there are + 方位 可以合并：There are books on the desk.",
     "they're = they are，口语缩写。",
     "今天练：Where are my ____? 答 They're on/in the ____.",
     "单复数方位都掌握后，描述房间就完整了——Day 30 实战见。"]
)

# ---------------- 总复习 Day 30 ----------------
capstone = {
    "day": 30,
    "date": d(30),
    "source": "总复习 · 30 天语法串讲 + 日常对话实战",
    "grammar": "串讲：be 动词(am/is/are) → this/that/these/those → 物主代词 → a/an → 颜色/形容词 → there is/are → 方位 → 祈使。今天把它们放进一段真实对话。",
    "review": "29 天里我们从 Excuse me! 走到 Where are they?，be 动词、物主代词、a/an、颜色、there is/are、方位、祈使句全部过完。",
    "preview": "下一步：用这套地基去啃真实材料——看 5 分钟英语短视频跟读、用 HelloTalk 找语伴聊 10 分钟、或进入新概念第二册练过去时。",
    "sentences": [
        {"en": "Hi Dafa, nice to see you! How are you today?", "cn": "大发你好，很高兴见到你！今天好吗？", "note": "Day1/Day9 问候组合，真实开场"},
        {"en": "I'm good, thanks. This is my friend Lin — she's a designer.", "cn": "我挺好的，谢谢。这是我朋友林——她是设计师。", "note": "This is 介绍 + she's 职业（Day5/Day8）"},
        {"en": "Where is the coffee shop? It's on the left, next to the bank.", "cn": "咖啡店在哪？在左边，银行旁边。", "note": "Where is + on the left（Day26 方位）"},
        {"en": "Can I have a cappuccino, please? And give me the menu.", "cn": "请给我一杯卡布奇诺？再把菜单给我。", "note": "a + 饮品 + Give me 双宾语（Day13/Day22）"},
        {"en": "Let's meet again next week — see you then!", "cn": "咱们下周再见——到时候见！", "note": "Let's 提议 + see you（Day1 道别升级）"}
    ],
    "words": [
        {"en": "friend", "phonetic": "frend", "cn": "朋友"},
        {"en": "designer", "phonetic": "dɪˈzaɪnə(r)", "cn": "设计师"},
        {"en": "coffee", "phonetic": "ˈkɒfi", "cn": "咖啡"},
        {"en": "shop", "phonetic": "ʃɒp", "cn": "商店"},
        {"en": "left", "phonetic": "left", "cn": "左边"},
        {"en": "bank", "phonetic": "bæŋk", "cn": "银行"},
        {"en": "menu", "phonetic": "ˈmenjuː", "cn": "菜单"},
        {"en": "week", "phonetic": "wiːk", "cn": "周"},
        {"en": "again", "phonetic": "əˈɡen", "cn": "再次"},
        {"en": "meet", "phonetic": "miːt", "cn": "见面"}
    ],
    "tips": [
        "今天不学新点，把上面 5 句当成一段真实对话，和『假想朋友』演一遍。",
        "卡壳时回看对应 Day：问候 Day9、介绍 Day5、方位 Day26、双宾语 Day22。",
        "能不卡壳演完这段，说明 A1 日常口语地基已立——这是 30 天最大的成果。",
        "接下来每天用 10 分钟看英语短视频影子跟读，把『课本英语』变成『活英语』。",
        "给自己鼓个掌：从 Day1 自测到今天实战，你真的上了一个台阶。"
    ]
}

# 组装
curriculum = [day1] + L + [capstone]
assert len(curriculum) == 30, f"expected 30 lessons, got {len(curriculum)}"

# ---------------- 写回 HTML ----------------
with open(HTML, "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'const DATA = (\{[\s\S]*?\n\});', text)
if not m:
    sys.exit("找不到 const DATA 对象")
data_obj = json.loads(m.group(1))
data_obj["english"] = curriculum

data_literal = "const DATA = " + json.dumps(data_obj, ensure_ascii=False, indent=2) + ";"
text = text[:m.start()] + data_literal + text[m.end():]

# 自检
chk = re.search(r'const DATA = (\{[\s\S]*?\n\});', text)
if not chk:
    sys.exit("自检失败：DATA 无法重新定位，已中止（文件未写入）")
try:
    after = json.loads(chk.group(1))
except json.JSONDecodeError as e:
    sys.exit(f"自检失败：结果不是合法 JSON（{e}），已中止（文件未写入）")
if len(after["english"]) != 30:
    sys.exit(f"自检失败：english 条数={len(after['english'])}，应为 30，已中止")
for les in after["english"]:
    for fld in ("day", "date", "source", "grammar", "review", "preview", "sentences", "words", "tips"):
        if fld not in les:
            sys.exit(f"自检失败：Day {les.get('day')} 缺字段 {fld}，已中止")
    if les["day"] == 1 and "opening" not in les:
        sys.exit("自检失败：Day 1 缺 opening，已中止")

with open(HTML, "w", encoding="utf-8") as f:
    f.write(text)

print("✅ 已写入 30 天课程体系（Day1 开场 + L1-L28 + Day30 总复习）")
print("首课日期:", curriculum[0]["date"], "末课日期:", curriculum[-1]["date"])
print("english 条数:", len(after["english"]))
