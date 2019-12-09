import factory

from test.unit.factories.orm import OrmAnimeFactory
from fal.models import Anime


class AnimeFactory(factory.Factory):
    class Meta:
        model = Anime

    @factory.lazy_attribute
    def entity(self):
        return OrmAnimeFactory(
            id=self.mal_id,
            restricted=self.restricted,
            eligible=self.eligible,
            name=list(self.names)[0],
        )

    session = None
    mal_id = factory.Sequence(lambda x: x)
    restricted = False
    eligible = True

    @factory.sequence
    def names(n):  # pylint: disable=no-self-argument
        name = ANIME_LIST[n % len(ANIME_LIST)]
        if n // len(ANIME_LIST) > 1:
            name = f"{name} {n // len(ANIME_LIST)}"
        return {name}


ANIME_LIST = [
    "One Punch Man Season 2",
    "Kono Yo no Hate de Koi wo Utau Shoujo YU-NO",
    "SSSS.Gridman",
    "Sora to Umi no Aida",
    "Kenja no Mago",
    "Toaru Majutsu no Index III",
    "Himote House",
    "Radiant",
    "Merc Storia: Mukiryoku no Shounen to Bin no Naka n",
    "Sarazanmai",
    "Tensei shitara Slime Datta Ken",
    "Carole & Tuesday",
    "Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo",
    "Hangyakusei Million Arthur",
    "Bakumatsu",
    "Hitoribocchi no ○○ Seikatsu",
    "Gakuen Basara",
    "Gunjou no Magmel",
    "Yatogame-chan Kansatsu Nikki",
    "Shoumetsu Toshi",
    "Mayonaka no Occult Koumuin",
    "Kaze ga Tsuyoku Fuiteiru",
    "Jojo no Kimyou na Bouken: Ougon no Kaze",
    "Jingai-san no Yome",
    "Kimetsu no Yaiba",
    "Bungou Stray Dogs 3rd Season",
    "World Witches Series: 501-butai Hasshin Shimasu!",
    "Kono Oto Tomare!",
    "Hachigatsu no Cinderella Nine",
    "Mix: Meisei Story",
    "Namu Amida Butsu!: Rendai Utena",
    "Kabukichou Sherlock",
    "Bokutachi wa Benkyou ga Dekinai",
    "Chou Kadou Girl ⅙: Amazing Stranger",
    "Hangyakusei Million Arthur 2nd Season",
    "Joshikausei",
    "Nande Koko ni Sensei ga!?",
    "Isekai Quartet",
    "Shingeki no Kyojin Season 3 Part 2",
    "Fruits Basket (2019)",
    "RobiHachi",
    "Diamond no Ace: Act II",
    "Sewayaki Kitsune no Senko-san",
    "Cinderella Girls Gekijou: Climax Season",
    "Midara na Ao-chan wa Benkyou ga Dekinai",
    "Senryuu Shoujo",
    "Kiratto Pri☆chan 2nd Season",
    "Nobunaga-sensei no Osanazuma",
    "Bakumatsu: Crisis",
    "Jimoto ga Japan",
    "Neko no Nyagh: Nya Misérables",
    "B Rappers Street",
    "Duel Masters!!",
    "Kedama no Gonjirou",
    "Fairy Gone",
    "Aikatsu Friends!: Kagayaki no Jewel",
    "Yousei Chiitan☆",
    "Cardfight!! Vanguard: Zoku Koukousei-hen",
    "Youkai Watch (2019)",
    "Beyblade Burst Gachi",
    "Araiya-san!: Ore to Aitsu ga Onnayu de!?",
    "Shounen Ashibe: Go! Go! Goma-chan 4",
]
