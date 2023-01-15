const getRandomInt = (min, max) =>
      Math.floor(Math.random() * (max - min + 1) + min)

const BANNERS = [
    "10.png",
    "12.png",
    "14.png",
    "17.png",
    "19.png",
    "1b.png",
    "20.png",
    "22.png",
    "24.png",
    "27.png",
    "2.png ",
    "4.png ",
    "8.png",
    "11.png",
    "13.png",
    "16.png",
    "18.png",
    "1a.png",
    "1c.png",
    "21.png",
    "23.png",
    "26.png",
    "28.png",
    "3.png",
    "5.png"
]

document.getElementById('ad-hell').src =
    '/' + base_url + '/static/ad-hell/' + BANNERS[getRandomInt(0, BANNERS.length - 1)]
