import pytest


@pytest.fixture
def season():
    return 'spring'


@pytest.fixture
def year():
    return 2019


@pytest.fixture
def series_dict_fixture():
    return {34134: 'One Punch Man Season 2',
            34620: 'Kono Yo no Hate de Koi wo Utau Shoujo YU-NO',
            36407: 'Kenja no Mago',
            37379: 'Chihayafuru 3',
            37426: 'Sarazanmai',
            37435: 'Carole & Tuesday',
            37614: 'Hitoribocchi no ○○ Seikatsu',
            37806: 'Gunjou no Magmel',
            37940: 'Yatogame-chan Kansatsu Nikki',
            37952: 'Shoumetsu Toshi',
            37964: 'Mayonaka no Occult Koumuin',
            38000: 'Kimetsu no Yaiba',
            38003: 'Bungou Stray Dogs 3rd Season',
            38004: 'World Witches Series: 501-butai Hasshin Shimasu!',
            38080: 'Kono Oto Tomare!',
            38091: 'Hachigatsu no Cinderella Nine',
            38098: 'Mix: Meisei Story',
            38161: 'Kabukichou Sherlock',
            38186: 'Bokutachi wa Benkyou ga Dekinai',
            38226: 'Chou Kadou Girl ⅙: Amazing Stranger',
            38268: 'Hangyakusei Million Arthur 2nd Season',
            38295: 'Joshikausei',
            38472: 'Isekai Quartet',
            38524: 'Shingeki no Kyojin Season 3 Part 2',
            38680: 'Fruits Basket (2019)',
            38707: 'RobiHachi',
            38759: 'Sewayaki Kitsune no Senko-san',
            38767: 'Cinderella Girls Gekijou: Climax Season',
            38778: 'Midara na Ao-chan wa Benkyou ga Dekinai',
            38787: 'Senryuu Shoujo',
            38814: 'Nobunaga-sensei no Osanazuma',
            38881: 'Jimoto ga Japan',
            39031: 'B Rappers Street',
            39039: 'Duel Masters!!',
            39040: 'Kedama no Gonjirou',
            39063: 'Fairy Gone',
            39078: 'Aikatsu Friends!: Kagayaki no Jewel'}


@pytest.fixture
def series():
    return [(34134, 'One Punch Man Season 2'),
            (38524, 'Shingeki no Kyojin Season 3 Part 2'),
            (38472, 'Isekai Quartet'),
            (38003, 'Bungou Stray Dogs 3rd Season'),
            (38680, 'Fruits Basket (2019)'),
            (36407, 'Kenja no Mago'),
            (37379, 'Chihayafuru 3'),
            (38000, 'Kimetsu no Yaiba'),
            (38186, 'Bokutachi wa Benkyou ga Dekinai'),
            (37614, 'Hitoribocchi no ○○ Seikatsu'),
            (37435, 'Carole & Tuesday'),
            (37426, 'Sarazanmai'),
            (34620, 'Kono Yo no Hate de Koi wo Utau Shoujo YU-NO'),
            (38080, 'Kono Oto Tomare!'),
            (37952, 'Shoumetsu Toshi'),
            (38787, 'Senryuu Shoujo'),
            (38759, 'Sewayaki Kitsune no Senko-san'),
            (38161, 'Kabukichou Sherlock'),
            (38778, 'Midara na Ao-chan wa Benkyou ga Dekinai'),
            (38004, 'World Witches Series: 501-butai Hasshin Shimasu!'),
            (37806, 'Gunjou no Magmel'),
            (37964, 'Mayonaka no Occult Koumuin'),
            (38268, 'Hangyakusei Million Arthur 2nd Season'),
            (38098, 'Mix: Meisei Story'),
            (38814, 'Nobunaga-sensei no Osanazuma'),
            (39063, 'Fairy Gone'),
            (38295, 'Joshikausei'),
            (38091, 'Hachigatsu no Cinderella Nine'),
            (38767, 'Cinderella Girls Gekijou: Climax Season'),
            (38707, 'RobiHachi'),
            (37940, 'Yatogame-chan Kansatsu Nikki'),
            (38226, 'Chou Kadou Girl ⅙: Amazing Stranger'),
            (38881, 'Jimoto ga Japan'),
            (39078, 'Aikatsu Friends!: Kagayaki no Jewel'),
            (39039, 'Duel Masters!!'),
            (39031, 'B Rappers Street'),
            (39040, 'Kedama no Gonjirou')]


@pytest.fixture
def series_titles():
    return ['One Punch Man Season 2',
            'Shingeki no Kyojin Season 3 Part 2',
            'Isekai Quartet',
            'Bungou Stray Dogs 3rd Season',
            'Fruits Basket (2019)',
            'Kenja no Mago',
            'Chihayafuru 3',
            'Kimetsu no Yaiba',
            'Bokutachi wa Benkyou ga Dekinai',
            'Hitoribocchi no ○○ Seikatsu',
            'Carole & Tuesday',
            'Sarazanmai',
            'Kono Yo no Hate de Koi wo Utau Shoujo YU-NO',
            'Kono Oto Tomare!',
            'Shoumetsu Toshi',
            'Senryuu Shoujo',
            'Sewayaki Kitsune no Senko-san',
            'Kabukichou Sherlock',
            'Midara na Ao-chan wa Benkyou ga Dekinai',
            'World Witches Series: 501-butai Hasshin Shimasu!',
            'Gunjou no Magmel',
            'Mayonaka no Occult Koumuin',
            'Hangyakusei Million Arthur 2nd Season',
            'Mix: Meisei Story',
            'Nobunaga-sensei no Osanazuma',
            'Fairy Gone',
            'Joshikausei',
            'Hachigatsu no Cinderella Nine',
            'Cinderella Girls Gekijou: Climax Season',
            'RobiHachi',
            'Yatogame-chan Kansatsu Nikki',
            'Chou Kadou Girl ⅙: Amazing Stranger',
            'Jimoto ga Japan',
            'Aikatsu Friends!: Kagayaki no Jewel',
            'Duel Masters!!',
            'B Rappers Street',
            'Kedama no Gonjirou']
