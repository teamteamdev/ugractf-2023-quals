# Прямо как у NSA: Write-up

К таску приложен файл вроде следующего:

```
KLUv/WCIA+UXAEpIyAsTUEU+AAAAAEAIBLiQ3amqqmqAAbcAtgC1AN/S93EwyiOqlQ8V9Vi04o9GwnTiSqmD7CgtxWDcX4LvyTbxsQ0oCxtJ+i1BARAbZ3cakrly6LZwHb/n+hxH56x3lLEApOsh15RHVpUzhpMxfDMrtvcAfLkuHwlgLyztlOwM8l5vIKWNhvWVxvterCu3MAZthewqetz8dgubeGUAdtBNrBqO56o+XaWKZYaQ4YCWj+lEivY2+TivKa7wWQKAKRoVC3UrpRCzltI9YGhhYrVJqmJjAfkwBqO8z9HvK9IJPUbLI8opZsMuTddexB8lNGEEYI2xFWJGTlMbh9Uh6Pg1Sot2JgrcYTY0TcELzzgo/a9xQ1HkhVLxjiAU8D8Aql6AUh88uROdbc4wMEA9M3YgOIZMGSXDYFxxySbJclP6flq5IQJskZ7ldXy+hKG9HM4r2RiEp31YyF6S/HvepuEJZbNZB6fvRIO6qngTUZsMYmkyrXN+RJEdKJUrjCqNw6R+oHgMpOSGk8Yb3BIq7mQLZ/qMYRLchO9yGaJ657uAcFQe2sh1UnvhcHRvRXxjs19ViunHPd4P+DfbBuL2isC1VTQ4qHs7i4uvZyuhnDhqSdkMIJlO8dYSw0s1/FTGSJkbFi7nG+o25ww75B5Mm7Vi98Qho15RaeR2uqwelC7MM7kkyi5HqXDOZKkCpHW9qxpbx6lVL68QVPzmcirx/sROZy3LSA+6y2GTGMaQfC0wvfNGck3zDQsp5POixLuHAoFAIBAIFGLWUpo+pvc0uTnA/F1ZU75Yj9Bw6EQJq56VyYscwwwVW64Jls0OENqAp7KNHODt9M9YBs9LPfmZ4Vb4xQFZtb7Bzt3P4P/MhzhK9afV/NwFA1Eb9AT319pEk7Rb3BQHyP7EjnFaVZILIiOxymxi+Pq9vfRwtcgpopFs1qD1/FEJyO/dy+RNmm6dHecvFMzSe9+mrsI+xqXhJ8tgPMDNigw7b6Z43vFounPAhjDBc4b0AQDtDVQU
```

Видим здесь какой-то мусор, состоящий из заглавных и строчных букв, цифр, и знаков `/` и `+` — ровно 64 символа (или 65, если вам не повезло, и в конце строки еще оказались символы `=`). 64 — это вообще очень хорошее число, и даже если вы никогда не слышали о таком методе кодирования, фраза «кодирование 64 символа» в гугле в числе первых ссылок выдаст метод base64.

Для декодирования base64 во многих языках есть встроенные функции, но можно обойтись и консольной утилитой `base64`, флаг `-d` которой позволяет декодировать данные:

```shell
$ base64 -d correspondence.txt
(�/�`��JH�
...
```

Что ж, это выглядит как мусор, но по крайней мере ошибок при декодировании нет. Сохраним этот мусор в файл и проанализируем его тип. Для этого существует консольная утилита `file`:

```shell
$ base64 -d correspondence.txt >step1
$ file step1
step1: Zstandard compressed data (v0.8+), Dictionary ID: None
```

Как видно из вывода `file`, это архив в формате zstd. Как и для многих других форматов, для работы с zstd существует консольная утилита. Воспользуемся ей для расжатия файла:

```shell
$ zstdcat step1
IJNGQOJRIFMSMU2ZWGHHB5AAAJWMSADWAB76APYAKABTPNE5XLJ3O5ZBCVJ7YBDDIVIGQRKPZGTCNUJGUPKMKU7VHUPIATJEPKCQGTIMRSMIIVJ7YATAKSAZEL4FHZIBNSOO6TRZYMIZOGKWH2LI7OCVKTAE74XXIGVPLMUVC2NPORH5LABT5CRWD7SBGCLHCCDYKLRVZENWYASZ2VHP5MWKZPNS57A6ATZ5OBUHA7XILNBX5ELMFLZUUBAAQQKV6WOOT3KP25J4ENHDSCR3QCVHGN4VDUC4ZEFJETNQPMXOGD44UQ2ER5UKBOR42HOQQ2X5G5LVVWWIPFIDBFSQDPL3RHR6QFXZC6WVSJOMPUJBXVZEYOFLIMS4ZQE26NSFHVUKHXDI5TVE4RYSLF3X7DMXOSPELQQXOV5PIOYGYI42OGBGIMUY36X4BLG7U42PPJPQFXOL6EGG7TRG74EE7Q53CL3QQAYNDQBYJLEWG2UVYAY3PFQBVMZU3NBKWAQQJLUZ62WS4NSQWKDVN2HIIJI7DUFQ5QLYDTSTFQTIBVNFVDNYSNNZ2CF3TXEDYETONMIICVDLKE3GAYEO3O3UJEBPHODXVXWI2JLODIIB5PICAXQ4WDVISSKPS5EZYFGKHPLUR62HVLGSQYKSUWRKEHRQM2GOVBKK3QQKHSG5OYPCP2KOMLGVKPSYNQR3TR45C3LKURRPJB2ZV2X2PPPJWMXYYT2IBYVF44AFEMWQTMUOWXUQZBF7BJOOHGC3KG3GXCRE3YHCJZWMK2QGSWY23TSYD4JSJEY6ETNZUEWIGGRLXBUXYDRTTDYC2LJFCHOBW4VGC27TLPTRDMVKHTUFT65UIIEQVUHIPT3Q5SYZ5BKL6B34I6VXQWCNXVYGIXVX2OAIXM2YI4AOLUJAUUES3RWPJELLFIUA2LYYKVWXQWFTOITTLLV7OQLYEHDBSJODW5GKDSRULFLJZERE2NBVORN5IN6KFAGSPNNX3LZO7YGJUSZQOJ3JRREXMFZ6SQD46KYEVRJCEGONUMEPCEE6PEKYZMJEHGSD2UTYAJUIVEOLGHVY4ANPEWKXU6V4JOQE7XDD6XBVI3JKHIGMVMUYNL5VHCRH2A3KMYBMNZIHYQWVHTEB7YXOJCTQUEQWGHHB5A======
```

Вот, другое дело. Это тоже похоже на base64, но только без строчных букв. Если этот формат вам не знаком, вы могли бы о нем узнать так:

- Можно посчитать число различных символов (кроме `=` — они явно лишние), их будет ровно 32, и по аналогии загуглить «base32».
- Либо можно загуглить «base64 without small letters» (на русском, к сожалению, полезной информации не находится) и увидеть ссылку на base32 в каком-нибудь ответе на Stack Overflow.

Так или иначе, для декодирования base32 также есть утилита:

```shell
$ zstdcat step1 >step2
$ base32 -d step2
BZh91AY&SY��p�l�v�?P7���ӷw!S�cEPhEOɦ&�&���S�=�M$z�M
...
```

Что ж, ничего нового, но на этот раз это не zstd:

```shell
$ base32 -d step2 >step3
$ file step3
step3: bzip2 compressed data, block size = 900k
```

Декодируем bzip2:

```shell
$ bzcat step3
fd377a585a000004e6d6b4460200210116000000742fe5a3e002b0023b5d003119492a42a8aac4e3fa53e00985e4522b0f041549928b40d026a563b45c8a7955acf558c9048e1e102e1a88db3a5242ba4417c987c769b37edbdf278f15e11fd85b4f75a5d0deb4d6aa6176825d0a473b2f260fa8fa9b0fb893daf72e7fd7da62f90fe77f38e37af6cf5f2dca8e47f7d1ea54020c4b17cf6c759c975bb0fb8dcb7a56e4aab6c455deaac400d5162a5d3c39b501b98454e8dac1ed3e53f34102b1dbf818463564f268c74d6dc09c3f39463fd6d4f457df094c02dced52c7cde5614ad8a231434d65fe604e981426e8cb26cea6ac0287b899ca36dbf6fd93fdfa588baef240518d65dff2c02504e19b658684ce360b77a6e79f42e1dcfe40779340cdfed93c023d2ad6818c95364eab2de426b5b87fff3f455d6a119f40feeecb2a2b2ffc36e6c2b26e3591f318e3c31aa87c8f15635d5f7220737421039996ea52c3e313995c64ceeb0bc6ce2378b6a429ac90b706684018bb56fc365b95da1bec6d0cf5d552cbe78a4ea0a1385d83869b298c652aca382b925fed0d712ed4356927541dd3112bd4f2bccad776e9e9d2a5cd02bfe84aa417b2424195730828268a882203232bb47981335efa80d6f4ec16d27c102387096b294adf8bb9c440bbf2b3c36d43dd3ccd531a00c41e8c135713f5a098fe36d7da3254fee289bec6a8fca699b48e47e4ef14e1fb05a88c1b44dc32ee3bd29eaff9dabfdd7efba6936147622e6f902952f85fbe60b08c78dfed070a2215be2ca8780d290b1aa63956144b22e0448d92f8c0ecb1ef39389a330666436f8b7ee01ee89300000000438f9fd521cf6e970001d704b10500009eb5eb9ab1c467fb020000000004595a
```

Это явно hex. Его тоже можно декодировать из консоли:

```shell
$ bzcat step3 >step4
$ xxd -r -p step4
�7zXZ�ִF!t/���;]1I*B�����S� ��R+I��@�&�c�\�yU��X��.���:RB�Dɇ�i�~��'���[Ou��޴֪av�]
...
```

Опять смотрим тип:

```shell
$ xxd -r -p step4 >step5
$ file step5
step5: XZ compressed data, checksum CRC64
```

И снова декодируем:

```shell
$ xzcat step5
begin 666 <data>
M'XL( &2%P&,"_U63O:[;, R%]SP%.V4QLA4M[E)<=$J'#DE1H).A6+3,1A93
MD8[A/GTIQ4F3R1+$GW,^T@<^859XWT'D$- #I\WF&\OP="_7-SL@Z,R/KV=8
M>(*,SG_9; [W.F_P"P6$\H?-FMA3<C$N#>B X-V8[$ IP,SY+&O,7K<")\0$
M\^"TJ0U&3CK(:^T?]FJ1[L230J8PZ.[>YL@P\ R"W9012$H7 8]7ZA!<6F:W
MO-;Z:@?JJ7-*G*RF98E2C$ )+IE#1I&F.&G@9-UXRM#EY:)L9$C43+H%\&J:
MOQ_?S<T4?=JJN3!YT1BQA;ON#&0:G]K^Y 1')<R1]"]TG'K*HX%6LV9)_##D
MAN9_X&X'^^T((3I?E52;I$LQ:GH#LX?!)7\'ZF*E8R2S2S*2:D%>)G#&!1+/
M:]P4LFMMCFV8%FF-01NPQK:8JEMCTWZ^_HGX4=TG0?^"\, !<U7>P![F L_2
MX51LZVT_3%Q/5X21TJ1X _K$ R+V>G=\?4:S*Y:MBI;E,=;SC5!RH\V)1YP'
MM(EA%%RS,UH/+V#OW,-A$B$'/><:7?94'KN<"MO(?!:(=+:!F>P\NE2KKS&C
?6VR4!+\GL:Y8)L3572TG$?%R_U.*A7\37-G^20,     
 
end
```

Тут уже чуть интереснее, потому что этот формат — UUE — сильно менее популярен. Гуглится он, например, по фразе `begin 666 <data>`.

```shell
$ xzcat step5 >step6
$ uudecode -o - step6
d��c�U����0
...
```

Опять:

```shell
$ uudecode -o step7 step6
$ file step7
step7: gzip compressed data, last modified: Thu Jan 12 22:10:44 2023, max compression, original size modulo 2^32 841
$ zcat step7
Robert A. logged on

Josh logged on
Josh: one two one two do you read?

Robert A.: Yes sir!

Josh: finally, the damn thing works
Josh: It's been what, two months?

Robert A.: That's about right.

Josh: So how secure is this device anyway?

Robert A.: Certifications are still in progress, sir, but our cryptologists say even NSA wouldn't be able to crack it.
Robert A.: Von Stierlitz confirmed that too.

Josh: ah, Stierlitz.. I'm glad our security is in good hands
Josh: alright, transmitting the key now
Josh: ugra_you_guys_are_getting_encryption_8vqle5ta7sed

Robert A.: Roger that, I will get back to you in five minutes, sir.
Robert A. left

Josh: von Stierlitz... I totally saw that name somewhere else
Josh: reminds me of Russia for some reason
Josh: nah, looks like a german name
Josh: maybe i just need to get some sleep

Josh left
```

После долгих мучений, получаем *его*:

Флаг: **ugra_you_guys_are_getting_encryption_8vqle5ta7sed**
