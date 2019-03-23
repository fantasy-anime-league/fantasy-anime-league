# ptw-script

Script to get PTW count of all anime in a certain season

## Running the script

1. Set the season and year in `config.ini`.
2. Run the script.
    ```shell
    $ python run_fal2.py --ptw-counter
    ```

## Output

The script will generate a CSV file with the name in the format `<season>-<year>-<date>.csv` in the ptw_csv directory.

For example, I ran the script on Spring 2019 on January 17, 2019. The filename was `Spring-2019-2019-01-19.csv`.

The output was:
```csv
Aikatsu Friends!: Kagayaki no Jewel,39078,569
B Rappers Street,39031,36
Bakumatsu: Crisis,38860,"1,089"
Beyblade Burst Gachi,39282,241
Bokutachi wa Benkyou ga Dekinai,38186,"11,278"
Bungou Stray Dogs 3rd Season,38003,"39,881"
Cardfight!! Vanguard: Zoku Koukousei-hen,39244,370
Carole & Tuesday,37435,"6,983"
Chihayafuru 3,37379,"16,023"
Chou Kadou Girl ⅙: Amazing Stranger,38226,808
Cinderella Girls Gekijou: Climax Season,38767,830
Diamond no Ace: Act II,38731,"5,725"
Duel Masters!!,39039,124
Fairy Gone,39063,"4,373"
Fruits Basket (2019),38680,"24,037"
Gunjou no Magmel,37806,"4,182"
Hachigatsu no Cinderella Nine,38091,"1,183"
Hangyakusei Million Arthur 2nd Season,38268,"2,833"
Hitoribocchi no ○○ Seikatsu,37614,"7,947"
Isekai Quartet,38472,"48,793"
Jimoto ga Japan,38881,491
Joshikausei,38295,"2,146"
Kabukichou Sherlock,38161,"4,869"
Kedama no Gonjirou,39040,31
Kenja no Mago,36407,"18,961"
Kimetsu no Yaiba,38000,"14,182"
Kiratto Pri☆chan 2nd Season,38804,186
Kono Oto Tomare!,38080,"5,761"
Kono Yo no Hate de Koi wo Utau Shoujo YU-NO,34620,"5,889"
Mayonaka no Occult Koumuin,37964,"3,237"
Midara na Ao-chan wa Benkyou ga Dekinai,38778,"4,767"
Mix: Meisei Story,38098,"2,143"
Namu Amida Butsu!: Rendai Utena,38150,788
Nande Koko ni Sensei ga!?,38397,"6,417"
Nobunaga-sensei no Osanazuma,38814,"2,568"
One Punch Man Season 2,34134,"306,672"
RobiHachi,38707,"1,041"
Sarazanmai,37426,"6,282"
Senryuu Shoujo,38787,"5,647"
Sewayaki Kitsune no Senko-san,38759,"5,655"
Shingeki no Kyojin Season 3 Part 2,38524,"94,489"
Shoumetsu Toshi,37952,"5,683"
World Witches Series: 501-butai Hasshin Shimasu!,38004,"3,277"
Yatogame-chan Kansatsu Nikki,37940,845
Youkai Watch (2019),39277,107
Yousei Chiitan☆,39110,23
```
