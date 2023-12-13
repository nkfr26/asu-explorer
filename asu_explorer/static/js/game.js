function rangeShuffle(n) {
    const a = new Array(n);
    for (let i = 0; i < n; i++) {  // 連番の生成
        a[i] = i;
    }
    for (let i = 0, j; i < n - 1; i++) {  // by Durstenfeld
        j = Math.floor(Math.random() * (n - i) + i);
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

const NUM_IMAGES = 9, NUM_QUESTIONS = 3, RADIUS = 25;

if (localStorage.getItem("questions") === null) {
    localStorage.setItem("questions", JSON.stringify(
        rangeShuffle(NUM_IMAGES).slice(0, NUM_QUESTIONS)
    ));
    localStorage.setItem("currentIndex", "0");
}
const [questions, currentIndex] = [
    JSON.parse(localStorage.getItem("questions")),
    Number(localStorage.getItem("currentIndex"))
];

// パノラマ
document.querySelector("iframe").src = `https://cdn.pannellum.org/2.5/pannellum.htm#panorama=${
    location.origin
}/static/images/panorama/${questions[currentIndex]}.jpg&autoLoad=true`;

// マップ
init_map();
const map = document.querySelector("#iframeOverlay");

// チュートリアル
const driverObj = init_driverjs();

if (!localStorage.getItem("isVisited")) {
    driverObj.drive();
    localStorage.setItem("isVisited", true);
}

// Explore
const explore = document.querySelector("#center button");
const id = navigator.geolocation.watchPosition(
    function(pos) {
        const distance = geodesic.Geodesic.WGS84.Inverse(
            pos.coords.latitude, pos.coords.longitude,
            ...ANS_COORDS[questions[currentIndex]], geodesic.Geodesic.DISTANCE
        ).s12;
        explore.disabled = !(distance <= RADIUS);

        // document.querySelector("footer").textContent = `[${
        //     pos.coords.latitude.toFixed(6)}, ${pos.coords.longitude.toFixed(6)
        // }], ${distance.toFixed(2)}`;
    },
    function(err) {
        if (err.code === 1) {
            alert("位置情報の利用を許可してください。");
        } else {
            console.log("POSITION_UNAVAILABLE");
        }
    }, {enableHighAccuracy: true}
);

const [modalImg, modalMsg] = [
    document.querySelector("#modal img"),
    document.querySelector("#modal p")
];
const appOverlay = document.querySelector("#appOverlay");

explore.addEventListener("click", function() {
    navigator.geolocation.clearWatch(id);
    explore.disabled = true;
    map.classList.add("visibility-hidden"); driverObj.destroy();

    [modalImg.src, modalMsg.textContent] = [
        `${location.origin}/static/images/star/${currentIndex}.png`,
        ["Nice !", "Great !", "Excellent !"][currentIndex]
    ];
    appOverlay.style = null;
});

const next = document.querySelector("#next");
next.addEventListener("click", function() {
	next.disabled = true;  // 2度押し防止

    if (currentIndex !== NUM_QUESTIONS - 1) {
        localStorage.setItem("currentIndex", currentIndex + 1);
        location.reload();
    } else {
        localStorage.removeItem("questions");

        if (Cookies.get("progress") === undefined) {
            Cookies.set("progress", "register", {expires: 7});
        }
        location.href += "/register";
    }
});

// UI
document.querySelector("#lt").addEventListener("click", function() {
    map.classList.add("visibility-hidden"); driverObj.drive();
});

document.querySelector(
    "#round div:nth-child(2)"
).textContent = `${ currentIndex + 1 } / ${ NUM_QUESTIONS }`;

document.querySelector("#lb").addEventListener("click", function() {
    if (confirm("問題をリセットします。\nこの操作は取り消せません。よろしいですか？")) {
        localStorage.removeItem("questions");
        location.reload();
    }
});

document.querySelectorAll(".toggle").forEach(
    function(element) {
        element.addEventListener("click", function() {
            map.classList.toggle("visibility-hidden");
        });
    }
);

// 崩れ防止
document.querySelector("#app").style = null;

// 初期化用関数
function init_map() {
    const app = document.querySelector("#app");
    const bounds = [[0, 0], [app.clientWidth, app.clientWidth]];
    L.imageOverlay(
        "https://www.aasa.ac.jp/img/guidance/campus_guide/img_map_nagakute_230908.png", bounds
    ).addTo(L.map("map", {
        crs: L.CRS.Simple
    }).fitBounds(bounds).setMaxBounds(bounds));
}
function init_driverjs() {
    return driver.js.driver({
        stagePadding: 4, allowClose: false,
        showProgress: true, progressText: "{{current}} / {{total}}",
        nextBtnText: "進む", prevBtnText: "戻る", doneBtnText: "終了",

        steps: [{
            element: "iframe",
            popover: {
                description: "<budoux-ja>大学内を探検し、表示されている場所を見つけよう。360度、自由に動かせます。</budoux-ja>"
            }
        }, {
            element: "#center button",
            popover: {
                description: "<budoux-ja>たどり着くと中央のボタンが押せるようになり、次の問題へ進めます。</budoux-ja>"
            }
        }, {
            element: "#center button",
            popover: {
                description :"<budoux-ja>位置情報の精度により、動作しない可能性があります。ご了承ください。</budoux-ja>"
            }
        }, {
            element: "#lt",
            popover: {
                description: "<budoux-ja>現在のチュートリアルは<br>このボタンから再表示できます。</budoux-ja>"
            }
        }, {
            element: "#rt",
            popover: {
                description: `<budoux-ja>問題数は3問。いくつかの場所からランダムに選ばれます。全問正解すると<a href="${
                    location.origin
                }/leaderboard">クリア者一覧</a>に登録できます。</budoux-ja>`
            }
        }, {
            element: "#lb",
            popover: {
                description: "<budoux-ja>このボタンを押すことで<br>問題をリセットすることができます。</budoux-ja>"
            }
        }, {
            element: "#rb",
            popover: {
                description: "<budoux-ja>マップも活用してみてください。</budoux-ja>"
            }
        }, {
            popover: {
                description: "<budoux-ja>チュートリアルは以上です。最後までお読みいただきありがとうございます！</budoux-ja>"
            }
        }]
    });
}